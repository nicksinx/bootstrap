"""Canonical launcher and standalone create-new-okf-project parity tests."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CREATE = ROOT / "skills" / "create-new-okf-project" / "scripts" / "create_okf_project.py"
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from okf_validation import load_frontmatter  # noqa: E402


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def assert_strict_project(target: Path) -> None:
    validate = run([str(target / "scripts" / "okf-validate"), "--strict"], cwd=target)
    if validate.returncode != 0:
        raise AssertionError(validate.stdout + validate.stderr)
    migrate = run([str(target / "scripts" / "okf-migrate"), "--check"], cwd=target)
    if migrate.returncode != 0:
        raise AssertionError(migrate.stdout + migrate.stderr)
    adapters = run([str(target / "scripts" / "okf-check-adapters")], cwd=target)
    if adapters.returncode != 0:
        raise AssertionError(adapters.stdout + adapters.stderr)


def test_repo_script_delegates_to_canonical_launcher() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-canonical-scaffold-") as td:
        target = Path(td) / "product"
        command = run(
            [
                sys.executable,
                str(CREATE),
                str(target),
                "--name",
                "Product Display Name",
                "--owner",
                "team-platform",
            ]
        )
        if command.returncode != 0:
            raise AssertionError(command.stdout + command.stderr)
        if "Scaffold source: canonical Project Bootstrap launcher" not in command.stdout:
            raise AssertionError(command.stdout)
        project, _ = load_frontmatter(target / ".okf" / "project.md")
        if project is None or project["title"] != "Product Display Name":
            raise AssertionError(project)
        if project["owner"] != "team-platform":
            raise AssertionError(project)
        assert_strict_project(target)


def test_standalone_skill_fallback_is_v02_clean() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-standalone-skill-") as td:
        temp = Path(td)
        skill = temp / "installed" / "create-new-okf-project"
        shutil.copytree(ROOT / "skills" / "create-new-okf-project", skill)
        target = temp / "fallback-project"
        command = run(
            [
                sys.executable,
                str(skill / "scripts" / "create_okf_project.py"),
                str(target),
                "--name",
                "Fallback Project",
                "--owner",
                "team-fallback",
            ],
            cwd=temp,
        )
        if command.returncode != 0:
            raise AssertionError(command.stdout + command.stderr)
        if "minimal embedded fallback" not in command.stderr:
            raise AssertionError(command.stderr)
        assert_strict_project(target)


def test_bundled_runtime_matches_canonical_runtime() -> None:
    canonical = ROOT / "scripts" / "lib"
    bundled = ROOT / "skills" / "create-new-okf-project" / "scripts" / "lib"
    for name in ("okf_validation.py", "okf_migration.py"):
        if (canonical / name).read_bytes() != (bundled / name).read_bytes():
            raise AssertionError(f"bundled runtime drift: {name}")
    if (
        ROOT / "scripts" / "okf-check-adapters"
    ).read_bytes() != (
        ROOT / "skills" / "create-new-okf-project" / "assets" / "scripts" / "okf-check-adapters"
    ).read_bytes():
        raise AssertionError("bundled runtime drift: okf-check-adapters")


def main() -> int:
    tests = [
        test_repo_script_delegates_to_canonical_launcher,
        test_standalone_skill_fallback_is_v02_clean,
        test_bundled_runtime_matches_canonical_runtime,
    ]
    for test in tests:
        test()
    print(f"scaffold consolidation tests passed ({len(tests)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
