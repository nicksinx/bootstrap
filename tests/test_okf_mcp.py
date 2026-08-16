"""Protocol, containment, determinism, and read-only tests for the OKF MCP pilot."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SERVER = ROOT / "scripts" / "okf-mcp-server"
MODERN = "2026-07-28"


def meta() -> dict[str, Any]:
    return {
        "io.modelcontextprotocol/protocolVersion": MODERN,
        "io.modelcontextprotocol/clientInfo": {"name": "okf-contract-test", "version": "1.0.0"},
        "io.modelcontextprotocol/clientCapabilities": {},
    }


def request(request_id: int, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params is not None:
        value["params"] = params
    return value


def run_messages(messages: list[Any]) -> tuple[subprocess.CompletedProcess[str], list[Any]]:
    raw = "\n".join(
        item if isinstance(item, str) else json.dumps(item, separators=(",", ":"))
        for item in messages
    ) + "\n"
    completed = subprocess.run(
        [str(SERVER)],
        cwd=str(ROOT),
        input=raw,
        text=True,
        capture_output=True,
        check=False,
    )
    replies = [json.loads(line) for line in completed.stdout.splitlines() if line]
    return completed, replies


def okf_digest() -> str:
    digest = hashlib.sha256()
    for path in sorted((ROOT / ".okf").rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(ROOT).as_posix().encode())
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def repository_digest() -> str:
    digest = hashlib.sha256()
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def test_modern_discovery_and_tool_catalog() -> None:
    completed, replies = run_messages(
        [
            request(1, "server/discover", {"_meta": meta()}),
            request(2, "tools/list", {"_meta": meta()}),
        ]
    )
    if completed.returncode != 0 or completed.stderr:
        raise AssertionError((completed.returncode, completed.stderr))
    if len(replies) != 2:
        raise AssertionError(replies)
    discovery = replies[0]["result"]
    if discovery["supportedVersions"] != [MODERN] or discovery["resultType"] != "complete":
        raise AssertionError(discovery)
    tools = replies[1]["result"]
    names = [tool["name"] for tool in tools["tools"]]
    expected = [
        "okf_bundle_summary",
        "okf_get_neighbors",
        "okf_list_tags",
        "okf_list_types",
        "okf_read_concept",
        "okf_search_concepts",
    ]
    if names != expected or tools["resultType"] != "complete":
        raise AssertionError(tools)
    for tool in tools["tools"]:
        annotations = tool.get("annotations", {})
        if annotations.get("readOnlyHint") is not True or annotations.get("destructiveHint") is not False:
            raise AssertionError(tool)
        if any(token in tool["name"] for token in ("write", "update", "delete", "execute")):
            raise AssertionError(tool["name"])


def test_modern_queries_are_contained_and_do_not_write() -> None:
    before = okf_digest()
    before_repository = repository_digest()
    completed, replies = run_messages(
        [
            request(
                10,
                "tools/call",
                {"name": "okf_bundle_summary", "arguments": {}, "_meta": meta()},
            ),
            request(
                11,
                "tools/call",
                {
                    "name": "okf_search_concepts",
                    "arguments": {"query": "bootstrap", "limit": 5},
                    "_meta": meta(),
                },
            ),
            request(
                12,
                "tools/call",
                {
                    "name": "okf_read_concept",
                    "arguments": {"path": ".okf/project.md"},
                    "_meta": meta(),
                },
            ),
            request(
                13,
                "tools/call",
                {
                    "name": "okf_get_neighbors",
                    "arguments": {"path": ".okf/project.md"},
                    "_meta": meta(),
                },
            ),
            request(
                14,
                "tools/call",
                {
                    "name": "okf_read_concept",
                    "arguments": {"path": "../.env"},
                    "_meta": meta(),
                },
            ),
        ]
    )
    if completed.returncode != 0 or len(replies) != 5:
        raise AssertionError((completed.returncode, completed.stderr, replies))
    if replies[0]["result"]["structuredContent"]["okf_version"] != "0.2":
        raise AssertionError(replies[0])
    if replies[1]["result"]["structuredContent"]["count"] < 1:
        raise AssertionError(replies[1])
    read = replies[2]["result"]
    if read["isError"] or read["structuredContent"]["path"] != ".okf/project.md":
        raise AssertionError(read)
    if replies[3]["result"]["structuredContent"]["path"] != ".okf/project.md":
        raise AssertionError(replies[3])
    rejected = replies[4]["result"]
    if rejected["isError"] is not True or "inside .okf" not in rejected["content"][0]["text"]:
        raise AssertionError(rejected)
    if ".env" in rejected["content"][0]["text"] and "../.env" not in rejected["content"][0]["text"]:
        raise AssertionError("unexpected secret-path disclosure")
    if okf_digest() != before:
        raise AssertionError("MCP query changed .okf")
    if repository_digest() != before_repository:
        raise AssertionError("MCP query changed repository file bytes")


def test_legacy_flow_and_protocol_errors() -> None:
    completed, replies = run_messages(
        [
            request(
                20,
                "initialize",
                {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "legacy-test", "version": "1.0.0"},
                },
            ),
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
            request(21, "tools/list", {}),
            request(22, "tools/call", {"name": "okf_list_types", "arguments": {}}),
            "{not-json",
        ]
    )
    if completed.returncode != 0 or len(replies) != 4:
        raise AssertionError((completed.returncode, completed.stderr, replies))
    if replies[0]["result"]["protocolVersion"] != "2025-06-18":
        raise AssertionError(replies[0])
    if "resultType" in replies[1]["result"] or not replies[1]["result"]["tools"]:
        raise AssertionError(replies[1])
    if replies[2]["result"]["isError"] or not replies[2]["result"]["structuredContent"]["types"]:
        raise AssertionError(replies[2])
    if replies[3]["error"]["code"] != -32700:
        raise AssertionError(replies[3])


def test_modern_metadata_is_mandatory() -> None:
    completed, replies = run_messages([request(30, "server/discover", {})])
    if completed.returncode != 0 or replies[0]["error"]["code"] != -32602:
        raise AssertionError((completed.returncode, completed.stderr, replies))


def test_modern_version_identity_and_request_ids_are_validated() -> None:
    unsupported_meta = meta()
    unsupported_meta["io.modelcontextprotocol/protocolVersion"] = "2099-01-01"
    malformed_meta = meta()
    malformed_meta["io.modelcontextprotocol/clientInfo"] = {"name": "missing-version"}
    completed, replies = run_messages(
        [
            request(31, "tools/list", {"_meta": unsupported_meta}),
            request(32, "tools/list", {"_meta": malformed_meta}),
            {"jsonrpc": "2.0", "id": None, "method": "ping", "params": {}},
        ]
    )
    if completed.returncode != 0 or len(replies) != 3:
        raise AssertionError((completed.returncode, completed.stderr, replies))
    unsupported = replies[0]["error"]
    if unsupported["code"] != -32022 or unsupported["data"] != {
        "supported": [MODERN],
        "requested": "2099-01-01",
    }:
        raise AssertionError(unsupported)
    if replies[1]["error"]["code"] != -32602:
        raise AssertionError(replies[1])
    if replies[2]["error"]["code"] != -32600 or replies[2]["id"] is not None:
        raise AssertionError(replies[2])


def test_symlink_concepts_are_rejected_before_read() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-mcp-symlink-") as td:
        temp = Path(td)
        project = temp / "project"
        shutil.copytree(ROOT / ".okf", project / ".okf")
        (project / "scripts" / "lib").mkdir(parents=True)
        for name in ("okf_tooling.py", "okf_validation.py"):
            shutil.copy2(ROOT / "scripts" / "lib" / name, project / "scripts" / "lib" / name)
        external = temp / "secret.md"
        external.write_text("DO-NOT-READ-EXTERNAL-CONTENT", encoding="utf-8")
        (project / ".okf" / "references" / "external-link.md").symlink_to(external)
        message = request(
            40,
            "tools/call",
            {"name": "okf_bundle_summary", "arguments": {}, "_meta": meta()},
        )
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "mcp_server" / "okf_readonly_server.py"),
                "--root",
                str(project),
            ],
            input=json.dumps(message) + "\n",
            text=True,
            capture_output=True,
            check=False,
        )
        reply = json.loads(completed.stdout)
        result = reply["result"]
        if completed.returncode != 0 or result["isError"] is not True:
            raise AssertionError((completed.returncode, completed.stderr, reply))
        text = result["content"][0]["text"]
        if "symlink concepts are not readable" not in text or "DO-NOT-READ" in text:
            raise AssertionError(text)


def main() -> int:
    tests = [
        test_modern_discovery_and_tool_catalog,
        test_modern_queries_are_contained_and_do_not_write,
        test_legacy_flow_and_protocol_errors,
        test_modern_metadata_is_mandatory,
        test_modern_version_identity_and_request_ids_are_validated,
        test_symlink_concepts_are_rejected_before_read,
    ]
    for test in tests:
        test()
    print(f"OKF MCP tests passed ({len(tests)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
