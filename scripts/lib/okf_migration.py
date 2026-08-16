#!/usr/bin/env python3
"""Idempotent OKF v0.1-to-v0.2 migration support."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

import yaml

from okf_validation import (
    ACTOR_RE,
    FrontmatterError,
    OKF_VERSION,
    find_project_root,
    parse_yaml_mapping,
    split_frontmatter,
    validate_bundle,
)


LEGACY_STATUS_MAP = {
    "active": "stable",
    "superseded": "deprecated",
    "archived": "deprecated",
}
LOG_HEADING_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})(?: \((.+)\))?$")


@dataclass(frozen=True)
class MigrationChange:
    path: str
    actions: tuple[str, ...]
    content: str


@dataclass(frozen=True)
class MigrationResult:
    root: Path
    scanned: int
    changes: tuple[MigrationChange, ...]
    errors: tuple[str, ...]


class _QuotedStringDumper(yaml.SafeDumper):
    pass


def _represent_string(dumper: yaml.Dumper, value: str) -> yaml.ScalarNode:
    style = '"' if re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:T.*)?", value) else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_QuotedStringDumper.add_representer(str, _represent_string)


def _render_frontmatter(data: dict, body: str) -> str:
    raw = yaml.dump(
        data,
        Dumper=_QuotedStringDumper,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    ).rstrip()
    return f"---\n{raw}\n---\n{body.lstrip(chr(10))}"


def _profile_extensions(data: dict) -> dict:
    extension = data.get("project_bootstrap")
    if extension is None:
        extension = {}
        data["project_bootstrap"] = extension
    if not isinstance(extension, dict):
        raise FrontmatterError("project_bootstrap extension exists but is not a mapping")
    return extension


def _migrate_concept(text: str, actor: str) -> tuple[str, list[str]]:
    raw, body = split_frontmatter(text)
    if raw is None:
        raise FrontmatterError("concept is missing YAML frontmatter")
    data = parse_yaml_mapping(raw)
    actions = []

    legacy_status = data.get("status")
    if legacy_status in LEGACY_STATUS_MAP:
        data["status"] = LEGACY_STATUS_MAP[legacy_status]
        actions.append(f"status {legacy_status} -> {data['status']}")
        if legacy_status in {"superseded", "archived"}:
            _profile_extensions(data).setdefault("legacy_status", legacy_status)
            actions.append("preserved legacy status in project_bootstrap")

    if "timestamp" in data:
        legacy_timestamp = data.pop("timestamp")
        if "generated" not in data:
            data["generated"] = {"by": actor, "at": legacy_timestamp}
            actions.append("timestamp -> generated")
        else:
            _profile_extensions(data).setdefault("legacy_timestamp", legacy_timestamp)
            actions.append("preserved redundant timestamp in project_bootstrap")

    if not actions:
        return text, actions
    return _render_frontmatter(data, body), actions


def _migrate_index(path: Path, okf: Path, text: str) -> tuple[str, list[str]]:
    raw, body = split_frontmatter(text)
    if path.parent == okf:
        expected = {"okf_version": OKF_VERSION}
        if raw is not None:
            data = parse_yaml_mapping(raw)
            if data == expected:
                return text, []
        return _render_frontmatter(expected, body if raw is not None else text), [
            "normalized root index metadata"
        ]
    if raw is not None:
        return body.lstrip("\n"), ["removed nested index frontmatter"]
    return text, []


def _migrate_log(text: str) -> tuple[str, list[str]]:
    raw, body = split_frontmatter(text)
    source = body if raw is not None else text
    lines = source.splitlines()
    header = []
    groups: dict[str, list[str]] = {}
    current: Optional[str] = None
    changed_headings = False
    for line in lines:
        match = LOG_HEADING_RE.fullmatch(line)
        if match:
            current = match.group(1)
            groups.setdefault(current, [])
            if match.group(2):
                label = match.group(2).strip()
                groups[current].extend(["", f"### {label[:1].upper()}{label[1:]}"])
                changed_headings = True
            continue
        if current is None:
            header.append(line)
        else:
            groups[current].append(line)

    if not groups:
        candidate = source.lstrip("\n")
    else:
        output = header[:]
        while output and not output[-1].strip():
            output.pop()
        output.append("")
        for date in sorted(groups, reverse=True):
            output.extend([f"## {date}", ""])
            content = groups[date][:]
            while content and not content[0].strip():
                content.pop(0)
            while content and not content[-1].strip():
                content.pop()
            output.extend(content)
            output.append("")
        candidate = "\n".join(output).rstrip() + "\n"

    actions = []
    if raw is not None:
        actions.append("removed log frontmatter")
    if changed_headings:
        actions.append("normalized dated log subheadings")
    if candidate != source and groups:
        actions.append("sorted log dates newest first")
    if not actions and candidate == text:
        return text, []
    return candidate, list(dict.fromkeys(actions or ["normalized log formatting"]))


def plan_migration(root: Path, actor: str) -> MigrationResult:
    root = root.resolve()
    okf = root / ".okf"
    if not okf.is_dir():
        return MigrationResult(root, 0, (), (".okf directory not found",))
    if not ACTOR_RE.fullmatch(actor):
        return MigrationResult(root, 0, (), (f"invalid OKF actor: {actor}",))

    changes = []
    errors = []
    paths = sorted(okf.rglob("*.md"))
    for path in paths:
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
            if path.name == "index.md":
                migrated, actions = _migrate_index(path, okf, text)
            elif path.name == "log.md":
                migrated, actions = _migrate_log(text)
            else:
                migrated, actions = _migrate_concept(text, actor)
        except (UnicodeDecodeError, FrontmatterError, yaml.YAMLError) as exc:
            errors.append(f"{rel}: {exc}")
            continue
        if migrated != text:
            changes.append(MigrationChange(rel, tuple(actions), migrated))
    return MigrationResult(root, len(paths), tuple(changes), tuple(errors))


def _atomic_write(path: Path, content: str) -> None:
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    temp = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as stream:
            stream.write(content)
        temp.chmod(mode)
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def apply_migration(result: MigrationResult) -> None:
    if result.errors:
        raise FrontmatterError("migration plan contains errors; no files were written")
    for change in result.changes:
        _atomic_write(result.root / change.path, change.content)


def _payload(result: MigrationResult, mode: str, validation: Optional[dict] = None) -> dict:
    payload = {
        "mode": mode,
        "root": str(result.root),
        "okf_version": OKF_VERSION,
        "scanned": result.scanned,
        "changed": len(result.changes),
        "changes": [
            {"path": change.path, "actions": list(change.actions)} for change in result.changes
        ],
        "errors": list(result.errors),
    }
    if validation is not None:
        payload["validation"] = validation
    return payload


def cli(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Check or apply an idempotent OKF v0.2 migration.")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="Report migration drift without writing")
    modes.add_argument("--apply", action="store_true", help="Apply migration atomically")
    parser.add_argument("--root", type=Path, help="Project root containing .okf")
    parser.add_argument("--actor", default="process:okf-migrate", help="Actor for migrated generated metadata")
    parser.add_argument("--strict", action="store_true", help="Require warning-free validation after apply")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    mode = "apply" if args.apply else "check"
    root = find_project_root(args.root) if args.root else find_project_root()
    result = plan_migration(root, args.actor)
    validation_payload = None

    if mode == "apply" and not result.errors:
        apply_migration(result)
        validation = validate_bundle(root)
        validation_payload = {
            "passed": not validation.errors and not (args.strict and validation.warnings),
            "errors": [issue.as_dict() for issue in validation.errors],
            "warnings": [issue.as_dict() for issue in validation.warnings],
        }

    if args.format == "json":
        print(json.dumps(_payload(result, mode, validation_payload), indent=2, sort_keys=True))
    else:
        for change in result.changes:
            print(f"CHANGE: {change.path}: {', '.join(change.actions)}")
        for error in result.errors:
            print(f"FAIL: {error}")
        if mode == "apply" and validation_payload is not None:
            state = "passed" if validation_payload["passed"] else "failed"
            print(
                f"OKF migration applied: {len(result.changes)} file(s); validation {state}"
            )
        elif result.errors:
            print(f"OKF migration check failed: {len(result.errors)} error(s)")
        elif result.changes:
            print(f"OKF migration needed: {len(result.changes)} of {result.scanned} file(s)")
        else:
            print(f"OKF migration check passed: {result.scanned} file(s), no changes")

    if result.errors:
        return 2
    if mode == "check":
        return 1 if result.changes else 0
    if validation_payload and not validation_payload["passed"]:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(cli())
