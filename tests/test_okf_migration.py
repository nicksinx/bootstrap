"""OKF v0.2 migration command tests."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MIGRATE = ROOT / "scripts" / "okf-migrate"
LIB = ROOT / "scripts" / "lib"
sys.path.insert(0, str(LIB))

from okf_migration import apply_migration, plan_migration  # noqa: E402
from okf_validation import load_frontmatter, validate_bundle  # noqa: E402


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def legacy_bundle(root: Path) -> str:
    body = "# Legacy Concept\n\nBody text must survive byte-for-byte.\n"
    write(
        root / ".okf" / "index.md",
        """---
type: Reference
title: Legacy index
status: active
timestamp: 2026-06-01T10:00:00Z
---
# Index
""",
    )
    write(
        root / ".okf" / "log.md",
        """---
type: Reference
status: active
timestamp: 2026-06-01T10:00:00Z
---
# Log

## 2026-06-01

* First.

## 2026-08-16 (migration)

* Latest.
""",
    )
    write(
        root / ".okf" / "legacy.md",
        """---
type: Custom Knowledge
title: Legacy concept
status: active
timestamp: 2026-06-01T10:00:00Z
custom_extension:
  nested: true
---
"""
        + body,
    )
    write(
        root / ".okf" / "old.md",
        """---
type: Custom Knowledge
status: superseded
timestamp: 2026-06-02T10:00:00Z
---
# Old
""",
    )
    write(
        root / ".okf" / "notes" / "index.md",
        """---
type: Reference
---
# Notes
""",
    )
    return body


def run(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(MIGRATE), "--root", str(root), *args],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


def test_check_apply_and_idempotence() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-migrate-") as td:
        root = Path(td)
        expected_body = legacy_bundle(root)
        check = run(root, "--check", "--format", "json")
        payload = json.loads(check.stdout)
        if check.returncode != 1 or payload["changed"] != 5:
            raise AssertionError((check.returncode, payload))

        applied = run(root, "--apply", "--strict", "--format", "json")
        applied_payload = json.loads(applied.stdout)
        if applied.returncode != 0 or not applied_payload["validation"]["passed"]:
            raise AssertionError((applied.returncode, applied_payload, applied.stderr))

        second = run(root, "--check", "--format", "json")
        second_payload = json.loads(second.stdout)
        if second.returncode != 0 or second_payload["changed"] != 0:
            raise AssertionError((second.returncode, second_payload))

        data, body = load_frontmatter(root / ".okf" / "legacy.md")
        if data is None or data["status"] != "stable":
            raise AssertionError(data)
        if data["generated"]["by"] != "process:okf-migrate":
            raise AssertionError(data)
        if data["custom_extension"] != {"nested": True}:
            raise AssertionError(data)
        if body != expected_body:
            raise AssertionError(repr(body))

        old, _ = load_frontmatter(root / ".okf" / "old.md")
        if old is None or old["project_bootstrap"]["legacy_status"] != "superseded":
            raise AssertionError(old)
        if (root / ".okf" / "notes" / "index.md").read_text() != "# Notes\n":
            raise AssertionError("nested index frontmatter was not removed")
        log = (root / ".okf" / "log.md").read_text()
        if log.index("## 2026-08-16") > log.index("## 2026-06-01"):
            raise AssertionError(log)
        if "### Migration" not in log:
            raise AssertionError(log)


def test_existing_generated_metadata_wins() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-migrate-generated-") as td:
        root = Path(td)
        write(root / ".okf" / "index.md", "---\nokf_version: \"0.2\"\n---\n# Index\n")
        write(root / ".okf" / "log.md", "# Log\n")
        write(
            root / ".okf" / "concept.md",
            """---
type: Custom Knowledge
status: active
timestamp: 2026-06-01T10:00:00Z
generated: { by: human:author, at: 2026-06-02T10:00:00Z }
---
# Concept
""",
        )
        result = plan_migration(root, "process:test")
        apply_migration(result)
        data, _ = load_frontmatter(root / ".okf" / "concept.md")
        if data is None or data["generated"]["by"] != "human:author":
            raise AssertionError(data)
        if data["project_bootstrap"]["legacy_timestamp"] != "2026-06-01T10:00:00Z":
            raise AssertionError(data)


def test_parse_error_prevents_all_writes() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-migrate-invalid-") as td:
        root = Path(td)
        legacy_bundle(root)
        bad = root / ".okf" / "broken.md"
        write(bad, "---\ntype: [broken\n---\n# Broken\n")
        before = (root / ".okf" / "legacy.md").read_text()
        result = plan_migration(root, "process:test")
        if not result.errors:
            raise AssertionError("expected a parse error")
        command = run(root, "--apply")
        if command.returncode != 2:
            raise AssertionError((command.returncode, command.stdout, command.stderr))
        if (root / ".okf" / "legacy.md").read_text() != before:
            raise AssertionError("migration wrote files despite a parse error")


def test_current_bundle_needs_no_migration() -> None:
    command = run(ROOT, "--check", "--format", "json")
    payload = json.loads(command.stdout)
    if command.returncode != 0 or payload["changed"] != 0:
        raise AssertionError((command.returncode, payload))
    validation = validate_bundle(ROOT)
    if validation.errors or validation.warnings:
        raise AssertionError((validation.errors, validation.warnings))


def main() -> int:
    tests = [
        test_check_apply_and_idempotence,
        test_existing_generated_metadata_wins,
        test_parse_error_prevents_all_writes,
        test_current_bundle_needs_no_migration,
    ]
    for test in tests:
        test()
    print(f"OKF migration tests passed ({len(tests)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
