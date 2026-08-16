#!/usr/bin/env python3
"""Path-contained, read-only MCP query server for an OKF v0.2 bundle."""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path
from typing import Any, Callable

sys.dont_write_bytecode = True


MODERN_PROTOCOL = "2026-07-28"
LEGACY_PROTOCOLS = (
    "2025-11-25",
    "2025-06-18",
    "2025-03-26",
    "2024-11-05",
)
SERVER_INFO = {
    "name": "okf-readonly",
    "version": "0.1.0",
    "description": "Read-only, repository-local queries over curated OKF concepts.",
}
SERVER_INFO_KEY = "io.modelcontextprotocol/serverInfo"
PROTOCOL_KEY = "io.modelcontextprotocol/protocolVersion"
CAPABILITIES_KEY = "io.modelcontextprotocol/clientCapabilities"
MAX_MESSAGE_BYTES = 10 * 1024 * 1024


def _load_runtime(root: Path):
    lib = root / "scripts" / "lib"
    if str(lib) not in sys.path:
        sys.path.insert(0, str(lib))
    try:
        from okf_tooling import MARKDOWN_LINK_RE, ToolingError, load_concepts
    except ImportError as exc:  # pragma: no cover - exercised by operator diagnostics
        raise RuntimeError(f"OKF runtime unavailable under {lib}: {exc}") from exc
    return MARKDOWN_LINK_RE, ToolingError, load_concepts


class ToolInputError(ValueError):
    """Raised for a rejected read-only tool request."""


class Catalog:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.okf = (self.root / ".okf").resolve()
        if not self.okf.is_dir():
            raise RuntimeError(f".okf directory not found under {self.root}")
        self.link_re, self.tooling_error, self.load_concepts = _load_runtime(self.root)

    def _concepts(self):
        symlinks = [
            path.relative_to(self.root).as_posix()
            for path in sorted(self.okf.rglob("*.md"))
            if path.is_symlink()
        ]
        if symlinks:
            raise ToolInputError(
                "symlink concepts are not readable through MCP: " + ", ".join(symlinks)
            )
        return self.load_concepts(self.root)

    def _concept_map(self):
        return {concept.relative: concept for concept in self._concepts()}

    @staticmethod
    def _count(values: list[str]) -> list[dict[str, Any]]:
        counts = collections.Counter(values)
        return [{"name": name, "count": counts[name]} for name in sorted(counts)]

    @staticmethod
    def _verification(data: dict[str, Any]) -> str:
        value = data.get("verification_status")
        if isinstance(value, str) and value:
            return value
        return "verified" if data.get("verified") else "unverified"

    def bundle_summary(self, arguments: dict[str, Any]) -> dict[str, Any]:
        _reject_extra(arguments, set())
        concepts = self._concepts()
        return {
            "okf_version": "0.2",
            "bundle_path": ".okf",
            "concept_count": len(concepts),
            "types": self._count([str(c.data.get("type", "Unknown")) for c in concepts]),
            "statuses": self._count([str(c.data.get("status", "unspecified")) for c in concepts]),
            "verification": self._count([self._verification(c.data) for c in concepts]),
        }

    def search_concepts(self, arguments: dict[str, Any]) -> dict[str, Any]:
        _reject_extra(arguments, {"query", "type", "tag", "limit"})
        query = _required_string(arguments, "query").casefold()
        type_filter = _optional_string(arguments, "type")
        tag_filter = _optional_string(arguments, "tag")
        limit = arguments.get("limit", 20)
        if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
            raise ToolInputError("limit must be an integer from 1 to 100")

        matches = []
        for concept in self._concepts():
            data = concept.data
            tags = [str(tag) for tag in data.get("tags", []) if isinstance(tag, str)]
            if type_filter and str(data.get("type", "")).casefold() != type_filter.casefold():
                continue
            if tag_filter and tag_filter.casefold() not in {tag.casefold() for tag in tags}:
                continue
            haystack = "\n".join(
                (concept.relative, concept.title, concept.description, concept.body)
            ).casefold()
            if query not in haystack:
                continue
            matches.append(
                {
                    "path": concept.relative,
                    "title": concept.title,
                    "description": concept.description,
                    "type": data.get("type"),
                    "status": data.get("status"),
                    "verification_status": self._verification(data),
                    "tags": tags,
                }
            )
        matches.sort(key=lambda item: item["path"])
        return {"query": query, "count": min(len(matches), limit), "matches": matches[:limit]}

    def read_concept(self, arguments: dict[str, Any]) -> dict[str, Any]:
        _reject_extra(arguments, {"path"})
        requested = _required_string(arguments, "path")
        relative = self._contained_concept_path(requested)
        concept = self._concept_map().get(relative)
        if concept is None:
            raise ToolInputError(f"concept not found: {requested}")
        return {
            "path": concept.relative,
            "frontmatter": concept.data,
            "body": concept.body,
        }

    def get_neighbors(self, arguments: dict[str, Any]) -> dict[str, Any]:
        _reject_extra(arguments, {"path"})
        requested = _required_string(arguments, "path")
        relative = self._contained_concept_path(requested)
        concepts = self._concept_map()
        concept = concepts.get(relative)
        if concept is None:
            raise ToolInputError(f"concept not found: {requested}")

        outgoing = []
        for label, raw_target in self.link_re.findall(concept.body):
            target = self._resolve_markdown_target(concept.path, raw_target)
            if target in concepts:
                outgoing.append({"path": target, "label": " ".join(label.split())})

        incoming = []
        for candidate in concepts.values():
            for label, raw_target in self.link_re.findall(candidate.body):
                target = self._resolve_markdown_target(candidate.path, raw_target)
                if target == relative:
                    incoming.append(
                        {"path": candidate.relative, "label": " ".join(label.split())}
                    )
        return {
            "path": relative,
            "outgoing": sorted(outgoing, key=lambda item: (item["path"], item["label"])),
            "incoming": sorted(incoming, key=lambda item: (item["path"], item["label"])),
        }

    def list_types(self, arguments: dict[str, Any]) -> dict[str, Any]:
        _reject_extra(arguments, set())
        return {
            "types": self._count(
                [str(concept.data.get("type", "Unknown")) for concept in self._concepts()]
            )
        }

    def list_tags(self, arguments: dict[str, Any]) -> dict[str, Any]:
        _reject_extra(arguments, set())
        tags = []
        for concept in self._concepts():
            tags.extend(str(tag) for tag in concept.data.get("tags", []) if isinstance(tag, str))
        return {"tags": self._count(tags)}

    def _contained_concept_path(self, raw: str) -> str:
        path = Path(raw)
        if path.is_absolute():
            raise ToolInputError("absolute paths are not allowed")
        candidate = (self.root / path).resolve()
        try:
            candidate.relative_to(self.okf)
        except ValueError as exc:
            raise ToolInputError("path must stay inside .okf") from exc
        if candidate.suffix.lower() != ".md":
            raise ToolInputError("path must identify an OKF Markdown concept")
        return candidate.relative_to(self.root).as_posix()

    def _resolve_markdown_target(self, source: Path, raw: str) -> str | None:
        target = raw.strip().split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "data:")):
            return None
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        candidate = (
            (source.parent / target).resolve()
            if not target.startswith("/")
            else (self.okf / target.lstrip("/")).resolve()
        )
        try:
            candidate.relative_to(self.okf)
            return candidate.relative_to(self.root).as_posix()
        except ValueError:
            return None


def _reject_extra(arguments: dict[str, Any], allowed: set[str]) -> None:
    extras = sorted(set(arguments) - allowed)
    if extras:
        raise ToolInputError(f"unexpected argument(s): {', '.join(extras)}")


def _required_string(arguments: dict[str, Any], key: str) -> str:
    value = arguments.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ToolInputError(f"{key} must be a non-empty string")
    return value.strip()


def _optional_string(arguments: dict[str, Any], key: str) -> str | None:
    value = arguments.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ToolInputError(f"{key} must be a non-empty string when provided")
    return value.strip()


EMPTY_SCHEMA = {"type": "object", "additionalProperties": False}
TOOL_DEFINITIONS = (
    {
        "name": "okf_bundle_summary",
        "title": "OKF Bundle Summary",
        "description": "Summarize concept, type, status, and verification counts in .okf.",
        "inputSchema": EMPTY_SCHEMA,
    },
    {
        "name": "okf_get_neighbors",
        "title": "OKF Concept Neighbors",
        "description": "List incoming and outgoing links for one path-contained OKF concept.",
        "inputSchema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Repo-relative .okf/*.md path."}},
            "required": ["path"],
            "additionalProperties": False,
        },
    },
    {
        "name": "okf_list_tags",
        "title": "OKF Tags",
        "description": "List OKF tags and their concept counts.",
        "inputSchema": EMPTY_SCHEMA,
    },
    {
        "name": "okf_list_types",
        "title": "OKF Concept Types",
        "description": "List OKF concept types and their counts.",
        "inputSchema": EMPTY_SCHEMA,
    },
    {
        "name": "okf_read_concept",
        "title": "Read OKF Concept",
        "description": "Read one repo-relative Markdown concept from .okf; traversal is rejected.",
        "inputSchema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Repo-relative .okf/*.md path."}},
            "required": ["path"],
            "additionalProperties": False,
        },
    },
    {
        "name": "okf_search_concepts",
        "title": "Search OKF Concepts",
        "description": "Search curated OKF concepts by text with optional type and tag filters.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "minLength": 1},
                "type": {"type": "string", "minLength": 1},
                "tag": {"type": "string", "minLength": 1},
                "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
)

for _tool in TOOL_DEFINITIONS:
    _tool["annotations"] = {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }


class Server:
    def __init__(self, catalog: Catalog) -> None:
        self.catalog = catalog
        self.legacy_protocol = "2025-06-18"
        self.handlers: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
            "okf_bundle_summary": catalog.bundle_summary,
            "okf_get_neighbors": catalog.get_neighbors,
            "okf_list_tags": catalog.list_tags,
            "okf_list_types": catalog.list_types,
            "okf_read_concept": catalog.read_concept,
            "okf_search_concepts": catalog.search_concepts,
        }

    @staticmethod
    def _modern_result(payload: dict[str, Any]) -> dict[str, Any]:
        result = dict(payload)
        result.setdefault("resultType", "complete")
        meta = dict(result.get("_meta") or {})
        meta[SERVER_INFO_KEY] = SERVER_INFO
        result["_meta"] = meta
        return result

    @staticmethod
    def _is_modern(request: dict[str, Any]) -> bool:
        params = request.get("params")
        meta = params.get("_meta") if isinstance(params, dict) else None
        return request.get("method") == "server/discover" or (
            isinstance(meta, dict) and meta.get(PROTOCOL_KEY) == MODERN_PROTOCOL
        )

    @staticmethod
    def _validate_modern_meta(request: dict[str, Any]) -> None:
        params = request.get("params")
        meta = params.get("_meta") if isinstance(params, dict) else None
        if not isinstance(meta, dict):
            raise ToolInputError("modern MCP requests require params._meta")
        if meta.get(PROTOCOL_KEY) != MODERN_PROTOCOL:
            raise ToolInputError(f"{PROTOCOL_KEY} must be {MODERN_PROTOCOL}")
        if not isinstance(meta.get(CAPABILITIES_KEY), dict):
            raise ToolInputError(f"{CAPABILITIES_KEY} must be an object")
        client_info = meta.get("io.modelcontextprotocol/clientInfo")
        if client_info is not None and (
            not isinstance(client_info, dict)
            or not isinstance(client_info.get("name"), str)
            or not client_info.get("name")
            or not isinstance(client_info.get("version"), str)
            or not client_info.get("version")
        ):
            raise ToolInputError("io.modelcontextprotocol/clientInfo must contain name and version")

    def handle(self, request: Any) -> dict[str, Any] | None:
        if not isinstance(request, dict) or request.get("jsonrpc") != "2.0":
            return _error(None, -32600, "Invalid Request")
        method = request.get("method")
        if not isinstance(method, str):
            return _error(request.get("id"), -32600, "Invalid Request")
        if "id" not in request:
            return None
        request_id = request["id"]
        if isinstance(request_id, bool) or not isinstance(request_id, (str, int)):
            return _error(None, -32600, "Invalid Request")

        params = request.get("params")
        meta = params.get("_meta") if isinstance(params, dict) else None
        requested_protocol = meta.get(PROTOCOL_KEY) if isinstance(meta, dict) else None
        if requested_protocol is not None and requested_protocol != MODERN_PROTOCOL:
            return _error(
                request_id,
                -32022,
                "Unsupported protocol version",
                {"supported": [MODERN_PROTOCOL], "requested": requested_protocol},
            )

        modern = self._is_modern(request)
        try:
            if modern:
                self._validate_modern_meta(request)
            if method == "server/discover":
                return _result(
                    request_id,
                    self._modern_result(
                        {
                            "supportedVersions": [MODERN_PROTOCOL],
                            "capabilities": {"tools": {"listChanged": False}},
                            "instructions": "Query curated .okf concepts only; this server exposes no write operations.",
                        }
                    ),
                )
            if method == "initialize":
                params = request.get("params") or {}
                requested = params.get("protocolVersion")
                self.legacy_protocol = requested if requested in LEGACY_PROTOCOLS else "2025-06-18"
                return _result(
                    request_id,
                    {
                        "protocolVersion": self.legacy_protocol,
                        "capabilities": {"tools": {"listChanged": False}},
                        "serverInfo": SERVER_INFO,
                        "instructions": "Read-only queries over curated OKF concepts.",
                    },
                )
            if method == "ping":
                payload: dict[str, Any] = {}
                return _result(request_id, self._modern_result(payload) if modern else payload)
            if method == "tools/list":
                payload = {"tools": list(TOOL_DEFINITIONS)}
                if modern:
                    payload = self._modern_result(payload)
                return _result(request_id, payload)
            if method == "tools/call":
                params = request.get("params")
                if not isinstance(params, dict):
                    raise ToolInputError("tools/call params must be an object")
                name = params.get("name")
                arguments = params.get("arguments", {})
                if name not in self.handlers:
                    raise ToolInputError(f"unknown tool: {name}")
                if not isinstance(arguments, dict):
                    raise ToolInputError("tool arguments must be an object")
                value = self.handlers[name](arguments)
                payload = {
                    "content": [{"type": "text", "text": json.dumps(value, sort_keys=True)}],
                    "structuredContent": value,
                    "isError": False,
                }
                if modern:
                    payload = self._modern_result(payload)
                return _result(request_id, payload)
            return _error(request_id, -32601, "Method not found")
        except (ToolInputError, self.catalog.tooling_error) as exc:
            if method == "tools/call":
                payload = {
                    "content": [{"type": "text", "text": str(exc)}],
                    "isError": True,
                }
                if modern:
                    payload = self._modern_result(payload)
                return _result(request_id, payload)
            return _error(request_id, -32602, "Invalid params", str(exc))
        except Exception as exc:  # keep protocol output valid while avoiding stack leaks
            print(f"okf-readonly internal error: {type(exc).__name__}: {exc}", file=sys.stderr)
            return _error(request_id, -32603, "Internal error")


def _result(request_id: Any, value: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": value}


def _error(request_id: Any, code: int, message: str, data: Any = None) -> dict[str, Any]:
    error: dict[str, Any] = {"code": code, "message": message}
    if data:
        error["data"] = data
    return {"jsonrpc": "2.0", "id": request_id, "error": error}


def _handle_payload(server: Server, payload: Any) -> Any:
    if isinstance(payload, list):
        if not payload:
            return _error(None, -32600, "Invalid Request")
        replies = [reply for item in payload if (reply := server.handle(item)) is not None]
        return replies or None
    return server.handle(payload)


def serve(server: Server) -> int:
    for raw in sys.stdin.buffer:
        if len(raw) > MAX_MESSAGE_BYTES:
            reply = _error(None, -32700, "Parse error", "message exceeds 10 MiB")
        else:
            try:
                payload = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                reply = _error(None, -32700, "Parse error")
            else:
                reply = _handle_payload(server, payload)
        if reply is not None:
            sys.stdout.write(json.dumps(reply, separators=(",", ":"), sort_keys=True) + "\n")
            sys.stdout.flush()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Project root containing .okf (default: server parent repository).",
    )
    args = parser.parse_args()
    try:
        catalog = Catalog(args.root)
    except RuntimeError as exc:
        print(f"okf-readonly: {exc}", file=sys.stderr)
        return 2
    return serve(Server(catalog))


if __name__ == "__main__":
    raise SystemExit(main())
