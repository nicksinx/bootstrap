#!/usr/bin/env python3
"""OKF v0.2 validation shared by the bootstrap kit and generated projects."""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised by operator environments
    raise SystemExit(
        "PyYAML is required for OKF validation. Install it with: python3 -m pip install PyYAML"
    ) from exc


OKF_VERSION = "0.2"
STATUS_VALUES = {"draft", "stable", "deprecated"}
VERIFICATION_VALUES = {"unverified", "cited", "reviewed", "tested", "accepted"}
CRITICAL_TYPES = {
    "Project",
    "Requirement",
    "Feature",
    "Architecture",
    "Decision",
    "Workflow",
    "Runbook",
    "Agent Rule",
    "Agent Skill",
    "Tool Adapter",
    "Risk",
    "Test Case",
    "Test Evidence",
    "Release",
    "Handoff",
    "Improvement",
    "Lesson Learned",
    "Retrospective",
}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bghp_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(
        r"(?i)\b(password|api[_-]?key|token|secret)\s*[:=]\s*['\"]?"
        r"[A-Za-z0-9_./+=-]{12,}"
    ),
)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(
    r"\A---[ \t]*\r?\n(?P<yaml>.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL
)
ACTOR_RE = re.compile(r"^(?:human:[^\s:]+|process:[^\s:]+|[^\s/:]+/[^\s/]+)$")
LOG_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
RELAY_PLACEHOLDERS = frozenset(
    {"<from forgerelay artifact>", "<from forgerelay>", "pending", "n/a", "tbd", ""}
)


class FrontmatterError(ValueError):
    """Raised when a YAML frontmatter block cannot be parsed safely."""


class _OKFLoader(yaml.SafeLoader):
    pass


# Keep dates as strings so ISO validation is deterministic across Python/PyYAML versions.
for _first, _resolvers in list(_OKFLoader.yaml_implicit_resolvers.items()):
    _OKFLoader.yaml_implicit_resolvers[_first] = [
        (_tag, _rx)
        for _tag, _rx in _resolvers
        if _tag != "tag:yaml.org,2002:timestamp"
    ]


def _construct_mapping(loader: _OKFLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise FrontmatterError("YAML mapping keys must be scalar values") from exc
        if duplicate:
            raise FrontmatterError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_OKFLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


@dataclass(frozen=True)
class Issue:
    severity: str
    path: str
    message: str

    def as_dict(self) -> dict:
        return {"severity": self.severity, "path": self.path, "message": self.message}


@dataclass(frozen=True)
class ValidationResult:
    root: Path
    concepts: int
    errors: tuple[Issue, ...]
    warnings: tuple[Issue, ...]

    @property
    def passed(self) -> bool:
        return not self.errors


def find_project_root(start: Optional[Path] = None) -> Path:
    current = (start or Path.cwd()).resolve()
    if current.name == ".okf" and current.is_dir():
        return current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".okf").is_dir():
            return candidate
    return current


def split_frontmatter(text: str) -> tuple[Optional[str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    return match.group("yaml"), text[match.end() :]


def parse_yaml_mapping(raw: str) -> dict:
    try:
        value = yaml.load(raw, Loader=_OKFLoader)
    except (yaml.YAMLError, FrontmatterError) as exc:
        raise FrontmatterError(str(exc)) from exc
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise FrontmatterError("frontmatter must be a YAML mapping")
    if not all(isinstance(key, str) for key in value):
        raise FrontmatterError("frontmatter keys must be strings")
    return value


def load_frontmatter(path: Path) -> tuple[Optional[dict], str]:
    text = path.read_text(encoding="utf-8")
    raw, body = split_frontmatter(text)
    if raw is None:
        return None, body
    return parse_yaml_mapping(raw), body


def _is_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _is_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        dt.date.fromisoformat(value)
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))
    except ValueError:
        return False


def _is_actor(value: Any) -> bool:
    return isinstance(value, str) and bool(ACTOR_RE.fullmatch(value))


def _non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _load_forge_validators(root: Path) -> Optional[Any]:
    path = root / "scripts" / "okf_dispatch_schema.py"
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("okf_dispatch_schema", path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _parse_context_pack_field(text: str, field_name: str) -> Optional[str]:
    prefixes = (f"- **{field_name}:**", f"- {field_name}:")
    for line in text.splitlines():
        stripped = line.strip().lower()
        for prefix in prefixes:
            if stripped.startswith(prefix.lower()):
                return line.split(":", 1)[1].strip().strip("*").strip()
    return None


def _check_relay_handoff(root: Path, rel: str, text: str, data: dict) -> list[str]:
    failures = []
    if Path(rel).name.startswith("TEMPLATE") or Path(rel).name == "README.md":
        return failures
    if "relay_session_id" not in text.lower():
        return failures
    relay_id = _parse_context_pack_field(text, "relay_session_id")
    dispatch_id = _parse_context_pack_field(text, "dispatch_packet_id")
    if relay_id and relay_id.lower() in RELAY_PLACEHOLDERS:
        failures.append("relay_session_id is a placeholder; set a real session id or remove it")
        return failures
    if relay_id and not dispatch_id:
        failures.append("relay_session_id is set but dispatch_packet_id is missing")
    elif relay_id and dispatch_id.lower() in {"pending", "tbd", "<if pipeline active, or n/a>"}:
        failures.append("dispatch_packet_id is a placeholder; set a packet id or N/A")

    state_path = root / ".okf" / "forge" / "relay" / "state.json"
    if not relay_id or not state_path.is_file():
        return failures
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return failures
    session = next(
        (item for item in state.get("sessions", []) if item.get("relaySessionId") == relay_id),
        None,
    )
    generated = data.get("generated") if isinstance(data.get("generated"), dict) else {}
    handoff_at = generated.get("at")
    session_at = (session or {}).get("updatedAt") or (session or {}).get("createdAt")
    if handoff_at and session_at and session_at > handoff_at:
        failures.append("relay session is newer than the handoff; refresh the handoff before resume")
    return failures


def _check_links(okf: Path, path: Path, body: str) -> Iterable[str]:
    for raw in LINK_RE.findall(body):
        target = raw.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if target.startswith("/"):
            target_path = okf / target.lstrip("/")
        else:
            target_path = path.parent / target
        if not target_path.resolve().exists():
            yield f"broken concept link (tolerated by OKF): {raw}"


def _validate_generated(rel: str, value: Any, errors: list[Issue]) -> None:
    if not isinstance(value, dict):
        errors.append(Issue("error", rel, "generated must be a mapping"))
        return
    if not _is_actor(value.get("by")):
        errors.append(Issue("error", rel, "generated.by must use the OKF actor convention"))
    if "at" in value and not _is_datetime(value.get("at")):
        errors.append(Issue("error", rel, "generated.at must be an ISO 8601 datetime"))


def _verification_events(value: Any) -> Optional[list]:
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return value
    return None


def _validate_verified(rel: str, value: Any, errors: list[Issue]) -> None:
    events = _verification_events(value)
    if events is None or not events:
        errors.append(Issue("error", rel, "verified must be a mapping or non-empty list"))
        return
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            errors.append(Issue("error", rel, f"verified[{index}] must be a mapping"))
            continue
        if not _is_actor(event.get("by")):
            errors.append(
                Issue("error", rel, f"verified[{index}].by must use the OKF actor convention")
            )
        if not _is_datetime(event.get("at")):
            errors.append(
                Issue("error", rel, f"verified[{index}].at must be an ISO 8601 datetime")
            )


def _validate_sources(rel: str, value: Any, errors: list[Issue], warnings: list[Issue]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(Issue("error", rel, "sources must be a non-empty list"))
        return
    ids = set()
    for index, source in enumerate(value):
        if not isinstance(source, dict):
            errors.append(Issue("error", rel, f"sources[{index}] must be a mapping"))
            continue
        if not _non_empty(source.get("resource")):
            errors.append(Issue("error", rel, f"sources[{index}].resource is required"))
        source_id = source.get("id")
        if source_id is not None:
            if not _non_empty(source_id):
                errors.append(Issue("error", rel, f"sources[{index}].id must be non-empty"))
            elif source_id in ids:
                errors.append(Issue("error", rel, f"duplicate sources id: {source_id}"))
            ids.add(source_id)
        if "usage_count" in source and (
            not isinstance(source["usage_count"], int) or source["usage_count"] < 0
        ):
            errors.append(Issue("error", rel, f"sources[{index}].usage_count must be >= 0"))
        if "last_modified" in source and not _is_date(source["last_modified"]):
            errors.append(
                Issue("error", rel, f"sources[{index}].last_modified must be YYYY-MM-DD")
            )
    if all(not source.get("id") for source in value if isinstance(source, dict)):
        warnings.append(Issue("warning", rel, "sources have no ids for per-claim attribution"))


def _validate_attested_computation(rel: str, data: dict, body: str, errors: list[Issue]) -> None:
    if data.get("type") != "Attested Computation":
        return
    if not _non_empty(data.get("runtime")):
        errors.append(Issue("error", rel, "Attested Computation requires runtime"))
    if "parameters" in data and not isinstance(data["parameters"], list):
        errors.append(Issue("error", rel, "parameters must be a list"))
    for field in ("executor", "attester"):
        value = data.get(field)
        if not isinstance(value, dict) or not _non_empty(value.get("resource")):
            errors.append(Issue("error", rel, f"{field}.resource is required"))
    has_file = _non_empty(data.get("computation"))
    has_inline = bool(re.search(r"^# Computation\s*$.*?```.+?```", body, re.MULTILINE | re.DOTALL))
    if has_file == has_inline:
        errors.append(
            Issue(
                "error",
                rel,
                "provide exactly one computation: frontmatter path or fenced # Computation body",
            )
        )


def _validate_index(path: Path, okf: Path, text: str, errors: list[Issue]) -> None:
    rel = path.relative_to(okf.parent).as_posix()
    raw, _ = split_frontmatter(text)
    if path.parent != okf:
        if raw is not None:
            errors.append(Issue("error", rel, "nested index.md must not have frontmatter"))
        return
    if raw is None:
        return
    try:
        data = parse_yaml_mapping(raw)
    except FrontmatterError as exc:
        errors.append(Issue("error", rel, f"invalid YAML frontmatter: {exc}"))
        return
    if set(data) != {"okf_version"}:
        errors.append(Issue("error", rel, "root index frontmatter may contain only okf_version"))
    if str(data.get("okf_version")) != OKF_VERSION:
        errors.append(Issue("error", rel, f"okf_version must be {OKF_VERSION}"))


def _validate_log(path: Path, okf: Path, text: str, errors: list[Issue]) -> None:
    rel = path.relative_to(okf.parent).as_posix()
    raw, body = split_frontmatter(text)
    if raw is not None:
        errors.append(Issue("error", rel, "log.md must not have frontmatter"))
        return
    headings = LOG_HEADING_RE.findall(body)
    dates = []
    for heading in headings:
        if not _is_date(heading):
            errors.append(Issue("error", rel, f"log heading must be YYYY-MM-DD: {heading}"))
            continue
        dates.append(heading)
    if dates != sorted(dates, reverse=True):
        errors.append(Issue("error", rel, "log date headings must be newest first"))


def validate_bundle(root: Path) -> ValidationResult:
    root = root.resolve()
    okf = root / ".okf"
    errors: list[Issue] = []
    warnings: list[Issue] = []
    concepts = 0
    if not okf.is_dir():
        return ValidationResult(
            root,
            0,
            (Issue("error", ".okf", ".okf directory not found"),),
            (),
        )

    forge = _load_forge_validators(root)
    for path in sorted(okf.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(Issue("error", rel, "file is not valid UTF-8"))
            continue

        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(Issue("error", rel, "likely secret detected"))
                break

        if path.name == "index.md":
            _validate_index(path, okf, text, errors)
            continue
        if path.name == "log.md":
            _validate_log(path, okf, text, errors)
            continue

        concepts += 1
        raw, body = split_frontmatter(text)
        if raw is None:
            errors.append(Issue("error", rel, "missing YAML frontmatter"))
            continue
        try:
            data = parse_yaml_mapping(raw)
        except FrontmatterError as exc:
            errors.append(Issue("error", rel, f"invalid YAML frontmatter: {exc}"))
            continue

        if not _non_empty(data.get("type")):
            errors.append(Issue("error", rel, "missing non-empty type"))
        status = data.get("status")
        if status is not None and status not in STATUS_VALUES:
            errors.append(
                Issue("error", rel, "status must be draft, stable, or deprecated")
            )
        if "timestamp" in data:
            warnings.append(
                Issue("warning", rel, "timestamp is legacy v0.1 metadata; use generated.at")
            )
        if "generated" in data:
            _validate_generated(rel, data["generated"], errors)
        if "verified" in data:
            _validate_verified(rel, data["verified"], errors)
        if "stale_after" in data and not _is_date(data["stale_after"]):
            errors.append(Issue("error", rel, "stale_after must be YYYY-MM-DD"))
        if "sources" in data:
            _validate_sources(rel, data["sources"], errors, warnings)
        if "usage_window" in data:
            window = data["usage_window"]
            if not isinstance(window, dict) or not all(
                _is_date(window.get(key)) for key in ("from", "to")
            ):
                errors.append(
                    Issue("error", rel, "usage_window must contain YYYY-MM-DD from and to")
                )

        concept_type = data.get("type")
        if concept_type in CRITICAL_TYPES and not _non_empty(data.get("sensitivity")):
            warnings.append(Issue("warning", rel, "project-critical concept missing sensitivity"))
        if concept_type in CRITICAL_TYPES and data.get("verification_status") not in VERIFICATION_VALUES:
            warnings.append(
                Issue("warning", rel, "project-critical concept missing valid verification_status")
            )
        if concept_type == "Reference" and data.get("status") == "draft":
            if data.get("verification_status") != "unverified":
                errors.append(
                    Issue("error", rel, "draft Reference must have verification_status: unverified")
                )
            if data.get("source_of_truth") is True:
                errors.append(
                    Issue("error", rel, "draft Reference must have source_of_truth: false")
                )

        _validate_attested_computation(rel, data, body, errors)
        for warning in _check_links(okf, path, body):
            warnings.append(Issue("warning", rel, warning))

        if forge is not None:
            forge_failures: list[str] = []
            for name in (
                "validate_forge_lineage_concept",
                "validate_forge_envelope_decision_state",
                "validate_forge_approval_decision",
            ):
                validator = getattr(forge, name, None)
                if validator:
                    validator(rel, text, data, forge_failures)
            errors.extend(Issue("error", rel, message) for message in forge_failures)
        if concept_type == "Handoff":
            errors.extend(
                Issue("error", rel, message)
                for message in _check_relay_handoff(root, rel, text, data)
            )

    return ValidationResult(root, concepts, tuple(errors), tuple(warnings))


def _print_text(result: ValidationResult, strict: bool) -> None:
    for issue in result.warnings:
        print(f"WARN: {issue.path}: {issue.message}")
    for issue in result.errors:
        print(f"FAIL: {issue.path}: {issue.message}")
    if result.errors or (strict and result.warnings):
        print(
            "OKF validation failed: "
            f"{len(result.errors)} failure(s), {len(result.warnings)} warning(s), "
            f"{result.concepts} concept(s)"
        )
    else:
        print(
            "OKF validation passed: "
            f"{len(result.warnings)} warning(s), {result.concepts} concept(s), "
            f"OKF v{OKF_VERSION}"
        )


def cli(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an OKF v0.2 bundle.")
    parser.add_argument("--root", type=Path, help="Project root containing .okf")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail when warnings are present as well as errors",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    result = validate_bundle(find_project_root(args.root) if args.root else find_project_root())
    failed = bool(result.errors or (args.strict and result.warnings))
    if args.format == "json":
        print(
            json.dumps(
                {
                    "okf_version": OKF_VERSION,
                    "root": str(result.root),
                    "concepts": result.concepts,
                    "strict": args.strict,
                    "passed": not failed,
                    "errors": [issue.as_dict() for issue in result.errors],
                    "warnings": [issue.as_dict() for issue in result.warnings],
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        _print_text(result, args.strict)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(cli())
