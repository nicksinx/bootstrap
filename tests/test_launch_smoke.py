"""Launch/worker smoke checks for bootstrap templates."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LAUNCH = ROOT / "scripts" / "launch_project.sh"


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd or ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


def test_launch_and_validate() -> None:
    with tempfile.TemporaryDirectory(prefix="bootstrap-smoke-") as td:
        target = Path(td) / "demo-proj"
        out = run(
            [
                str(LAUNCH),
                "--name",
                "demo-proj",
                "--profile",
                "default",
                "--target-dir",
                str(target),
                "--non-interactive",
            ]
        )
        if out.returncode != 0:
            raise SystemExit(
                "launch failed\nstdout:\n"
                + out.stdout
                + "\nstderr:\n"
                + out.stderr
            )

        validate = run([str(target / "scripts" / "validate_launch.sh")], cwd=target)
        if validate.returncode != 0:
            raise SystemExit(
                "validate failed\nstdout:\n"
                + validate.stdout
                + "\nstderr:\n"
                + validate.stderr
            )

        expected_okf = [
            ".okf/index.md",
            ".okf/project.md",
            ".okf/improvements/continuous-improvement-repository.md",
            "AGENTS.md",
            "CLAUDE.md",
            ".cursor/rules/okf.mdc",
            "docs/okf-integration.md",
            "scripts/okf-validate",
            "scripts/okf-dispatch",
            ".cursor/mcp.json",
        ]
        missing = [rel for rel in expected_okf if not (target / rel).exists()]
        if missing:
            raise SystemExit(f"missing OKF scaffold files: {missing}")


def test_okf_dispatch_status() -> None:
    with tempfile.TemporaryDirectory(prefix="bootstrap-dispatch-") as td:
        target = Path(td) / "demo-proj"
        out = run(
            [
                str(LAUNCH),
                "--name",
                "demo-proj",
                "--profile",
                "default",
                "--target-dir",
                str(target),
                "--non-interactive",
            ]
        )
        if out.returncode != 0:
            raise SystemExit(out.stderr)

        status = run([str(target / "scripts" / "okf-dispatch"), "status"], cwd=target)
        if status.returncode != 0:
            raise SystemExit(
                "okf-dispatch status failed\nstdout:\n"
                + status.stdout
                + "\nstderr:\n"
                + status.stderr
            )


def test_forge_lifecycle_alias_launch_and_validate() -> None:
    with tempfile.TemporaryDirectory(prefix="bootstrap-forge-") as td:
        target = Path(td) / "forge-demo"
        out = run(
            [
                str(LAUNCH),
                "--name",
                "forge-demo",
                "--profile",
                "forge-lifecycle",
                "--target-dir",
                str(target),
                "--non-interactive",
            ]
        )
        if out.returncode != 0:
            raise SystemExit(
                "forge-lifecycle launch failed\nstdout:\n"
                + out.stdout
                + "\nstderr:\n"
                + out.stderr
            )

        validate = run([str(target / "scripts" / "validate_launch.sh")], cwd=target)
        if validate.returncode != 0:
            raise SystemExit(
                "forge-lifecycle validate failed\nstdout:\n"
                + validate.stdout
                + "\nstderr:\n"
                + validate.stderr
            )

        expected_forge = [
            "docs/forge-lifecycle-integration.md",
            "scripts/forgerelay-mcp.sh",
            "scripts/forge-clone-siblings.sh",
            ".okf/decisions/0002-okf-forge-integration.md",
            ".cursor/mcp-forge-lifecycle.json.example",
            ".cursor/mcp.json",
        ]
        missing = [rel for rel in expected_forge if not (target / rel).exists()]
        if missing:
            raise SystemExit(f"missing forge-lifecycle scaffold files: {missing}")


def main() -> int:
    test_launch_and_validate()
    test_forge_lifecycle_alias_launch_and_validate()
    test_okf_dispatch_status()
    print("launch smoke tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
