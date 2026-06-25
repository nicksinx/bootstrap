"""Launch/worker smoke checks for bootstrap templates."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LAUNCH = ROOT / "scripts" / "launch_project.sh"


def run(cmd: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd or ROOT),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_launch_and_validate() -> None:
    with tempfile.TemporaryDirectory(prefix="bootstrap-smoke-", dir=str(ROOT)) as td:
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
        ]
        missing = [rel for rel in expected_okf if not (target / rel).exists()]
        if missing:
            raise SystemExit(f"missing OKF scaffold files: {missing}")


def test_worker_stub_flow() -> None:
    with tempfile.TemporaryDirectory(prefix="bootstrap-worker-", dir=str(ROOT)) as td:
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

        env = dict(os.environ)
        env["WORKER_CODEX_BIN"] = "true"
        dispatch = run(
            [
                str(target / "scripts" / "workers" / "dispatch_task.sh"),
                "start",
                "--task-id",
                "TASK-0001",
                "--foreground",
                "--max-retries",
                "0",
            ],
            cwd=target,
            env=env,
        )
        if dispatch.returncode != 0:
            raise SystemExit(
                "worker dispatch failed\nstdout:\n"
                + dispatch.stdout
                + "\nstderr:\n"
                + dispatch.stderr
            )

        manifests = sorted(target.glob("runs/codex/*/manifest.json"))
        if not manifests:
            raise SystemExit("worker manifest not found")
        manifest = json.loads(manifests[-1].read_text())
        if manifest.get("phase") != "completed":
            raise SystemExit(f"unexpected worker phase: {manifest.get('phase')}")


def main() -> int:
    test_launch_and_validate()
    test_worker_stub_flow()
    print("launch smoke tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
