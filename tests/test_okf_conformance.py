"""Strict OKF v0.2 validator regression tests."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = ROOT / "scripts" / "okf-validate"
LIB = ROOT / "scripts" / "lib"
sys.path.insert(0, str(LIB))

from okf_validation import validate_bundle  # noqa: E402


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_valid_bundle(root: Path) -> None:
    write(
        root / ".okf" / "index.md",
        """---
okf_version: "0.2"
---

# Bundle Index

* [Project](project.md) - Project context.
""",
    )
    write(
        root / ".okf" / "project.md",
        """---
type: Project
title: Validation Fixture
description: A strict OKF v0.2 validation fixture.
status: stable
generated: { by: process:test-suite, at: 2026-08-16T10:00:00Z }
sensitivity: internal
verification_status: reviewed
---

# Validation Fixture
""",
    )
    write(
        root / ".okf" / "log.md",
        """# Bundle Log

## 2026-08-16

* **Validation**: Added the fixture.

## 2026-08-15

* **Creation**: Created the fixture.
""",
    )
    write(root / ".okf" / "notes" / "index.md", "# Notes\n")


def run_validator(root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(VALIDATOR), "--root", str(root), *extra],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


def test_valid_bundle_passes_strict() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-v02-valid-") as td:
        root = Path(td)
        create_valid_bundle(root)
        result = validate_bundle(root)
        if result.errors or result.warnings:
            raise AssertionError((result.errors, result.warnings))
        command = run_validator(root, "--strict")
        if command.returncode != 0:
            raise AssertionError(command.stdout + command.stderr)


def test_real_yaml_parser_rejects_duplicate_and_malformed_keys() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-v02-yaml-") as td:
        root = Path(td)
        create_valid_bundle(root)
        write(
            root / ".okf" / "bad.md",
            """---
type: Requirement
type: Decision
title: [unterminated
---
""",
        )
        result = validate_bundle(root)
        messages = "\n".join(issue.message for issue in result.errors)
        if "invalid YAML frontmatter" not in messages:
            raise AssertionError(messages)


def test_reserved_index_and_log_contracts() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-v02-reserved-") as td:
        root = Path(td)
        create_valid_bundle(root)
        write(
            root / ".okf" / "notes" / "index.md",
            """---
type: Reference
---
# Invalid nested index
""",
        )
        write(
            root / ".okf" / "log.md",
            """# Bundle Log

## 2026-08-16T10:00:00Z

* Invalid date heading.
""",
        )
        result = validate_bundle(root)
        messages = "\n".join(issue.message for issue in result.errors)
        if "nested index.md must not have frontmatter" not in messages:
            raise AssertionError(messages)
        if "log heading must be YYYY-MM-DD" not in messages:
            raise AssertionError(messages)


def test_v01_metadata_is_not_strictly_accepted() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-v01-legacy-") as td:
        root = Path(td)
        create_valid_bundle(root)
        project = root / ".okf" / "project.md"
        project.write_text(
            project.read_text(encoding="utf-8").replace(
                "generated: { by: process:test-suite, at: 2026-08-16T10:00:00Z }",
                "timestamp: 2026-08-16T10:00:00Z",
            ),
            encoding="utf-8",
        )
        normal = run_validator(root)
        strict = run_validator(root, "--strict")
        if normal.returncode != 0 or strict.returncode == 0:
            raise AssertionError(
                f"normal={normal.returncode} strict={strict.returncode}\n{strict.stdout}"
            )


def test_json_output_is_machine_readable() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-v02-json-") as td:
        root = Path(td)
        create_valid_bundle(root)
        command = run_validator(root, "--strict", "--format", "json")
        payload = json.loads(command.stdout)
        if command.returncode != 0 or not payload["passed"]:
            raise AssertionError(payload)
        if payload["okf_version"] != "0.2" or payload["concepts"] != 1:
            raise AssertionError(payload)


def main() -> int:
    tests = [
        test_valid_bundle_passes_strict,
        test_real_yaml_parser_rejects_duplicate_and_malformed_keys,
        test_reserved_index_and_log_contracts,
        test_v01_metadata_is_not_strictly_accepted,
        test_json_output_is_machine_readable,
    ]
    for test in tests:
        test()
    print(f"OKF v0.2 conformance tests passed ({len(tests)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
