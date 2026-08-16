"""OpenWiki opt-in, staging boundary, and adapter coexistence tests."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import tempfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
LAUNCH = ROOT / "scripts" / "launch_project.sh"
BEGIN = "<!-- OPENWIKI:START -->"
END = "<!-- OPENWIKI:END -->"


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def digest_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if item.is_file():
            digest.update(item.relative_to(path).as_posix().encode())
            digest.update(b"\0")
            digest.update(item.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def make_fake(path: Path, *, mutate_okf: bool = False, symlink_output: bool = False) -> None:
    mutation = "printf '\\nMUTATED\\n' >> .okf/project.md\n" if mutate_okf else ""
    symlink = "ln -s /etc/hosts openwiki/external.md\n" if symlink_output else ""
    path.write_text(
        "#!/usr/bin/env bash\n"
        "set -Eeuo pipefail\n"
        "case \"${1:-}\" in --init|--update) ;; *) exit 2;; esac\n"
        f"{mutation}"
        "mkdir -p openwiki\n"
        f"{symlink}"
        "printf '# Generated sidecar\\n' > openwiki/generated.md\n"
        "for file in AGENTS.md CLAUDE.md; do\n"
        "  printf '\\n<!-- OPENWIKI:START -->\\nOpenWiki generated guidance.\\n<!-- OPENWIKI:END -->\\n' >> \"$file\"\n"
        "done\n",
        encoding="utf-8",
    )
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def launch(target: Path, with_openwiki: bool) -> subprocess.CompletedProcess[str]:
    command = [
        str(LAUNCH),
        "--name",
        target.name,
        "--profile",
        "default",
        "--target-dir",
        str(target),
        "--non-interactive",
    ]
    if with_openwiki:
        command.append("--with-openwiki")
    return run(command)


def test_sidecar_is_opt_in() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-openwiki-off-") as td:
        target = Path(td) / "sidecar-off"
        completed = launch(target, False)
        if completed.returncode != 0:
            raise AssertionError(completed.stdout + completed.stderr)
        config = yaml.safe_load((target / "project.config.yaml").read_text())
        if config["integrations"]["openwiki"]["enabled"] is not False:
            raise AssertionError(config["integrations"])
        if (target / "openwiki" / "INSTRUCTIONS.md").exists():
            raise AssertionError("OpenWiki overlay was emitted without opt-in")


def test_staged_run_imports_only_bounded_outputs_and_sync_preserves_blocks() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-openwiki-on-") as td:
        temp = Path(td)
        target = temp / "sidecar-on"
        completed = launch(target, True)
        if completed.returncode != 0:
            raise AssertionError(completed.stdout + completed.stderr)
        config = yaml.safe_load((target / "project.config.yaml").read_text())
        if config["integrations"]["openwiki"]["enabled"] is not True:
            raise AssertionError(config["integrations"])
        instructions = target / "openwiki" / "INSTRUCTIONS.md"
        if not instructions.is_file() or ".okf/" not in instructions.read_text():
            raise AssertionError("missing bounded sidecar instructions")

        fake = temp / "fake-openwiki"
        make_fake(fake)
        wrapper = target / "scripts" / "openwiki-sidecar"
        before_okf = digest_tree(target / ".okf")

        status = run([str(wrapper), "status", "--command", str(fake)], cwd=target)
        if status.returncode != 0:
            raise AssertionError(status.stdout + status.stderr)
        status_payload = json.loads(status.stdout)
        if not status_payload["enabled"] or not status_payload["command_available"]:
            raise AssertionError(status_payload)

        dry = run([str(wrapper), "init", "--command", str(fake), "--dry-run"], cwd=target)
        if dry.returncode != 0 or json.loads(dry.stdout)["protected_path"] != ".okf":
            raise AssertionError(dry.stdout + dry.stderr)
        if (target / "openwiki" / "generated.md").exists():
            raise AssertionError("dry-run imported generated output")

        init = run([str(wrapper), "init", "--command", str(fake)], cwd=target)
        if init.returncode != 0:
            raise AssertionError(init.stdout + init.stderr)
        if not (target / "openwiki" / "generated.md").is_file():
            raise AssertionError("bounded generated output was not imported")
        if digest_tree(target / ".okf") != before_okf:
            raise AssertionError("live .okf changed during staged OpenWiki run")
        for name in ("AGENTS.md", "CLAUDE.md"):
            text = (target / name).read_text()
            if text.count(BEGIN) != 1 or text.count(END) != 1:
                raise AssertionError((name, text))

        synced = run([str(target / "scripts" / "okf-sync-skills")], cwd=target)
        if synced.returncode != 0:
            raise AssertionError(synced.stdout + synced.stderr)
        for name in ("AGENTS.md", "CLAUDE.md"):
            text = (target / name).read_text()
            if text.count(BEGIN) != 1 or "OpenWiki generated guidance." not in text:
                raise AssertionError((name, text))

        agents = target / "AGENTS.md"
        agents.write_text(agents.read_text() + "\n" + BEGIN + "\n")
        before_agents = agents.read_text()
        before_claude = (target / "CLAUDE.md").read_text()
        rejected = run([str(target / "scripts" / "okf-sync-skills")], cwd=target)
        if rejected.returncode == 0 or "adapter preflight" not in rejected.stderr:
            raise AssertionError(rejected.stdout + rejected.stderr)
        if agents.read_text() != before_agents or (target / "CLAUDE.md").read_text() != before_claude:
            raise AssertionError("adapter preflight failure partially wrote adapters")


def test_attempted_okf_mutation_fails_without_import() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-openwiki-guard-") as td:
        temp = Path(td)
        target = temp / "sidecar-guard"
        completed = launch(target, True)
        if completed.returncode != 0:
            raise AssertionError(completed.stdout + completed.stderr)
        fake = temp / "mutating-openwiki"
        make_fake(fake, mutate_okf=True)
        before_okf = digest_tree(target / ".okf")
        before_instructions = (target / "openwiki" / "INSTRUCTIONS.md").read_text()

        rejected = run(
            [str(target / "scripts" / "openwiki-sidecar"), "update", "--command", str(fake)],
            cwd=target,
        )
        if rejected.returncode != 9 or "attempted to change .okf" not in rejected.stderr:
            raise AssertionError(rejected.stdout + rejected.stderr)
        if digest_tree(target / ".okf") != before_okf:
            raise AssertionError("live .okf changed after rejected sidecar run")
        if (target / "openwiki" / "generated.md").exists():
            raise AssertionError("rejected sidecar output was imported")
        if (target / "openwiki" / "INSTRUCTIONS.md").read_text() != before_instructions:
            raise AssertionError("operator instructions changed after rejected sidecar run")


def test_generated_symlink_is_not_imported() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-openwiki-symlink-") as td:
        temp = Path(td)
        target = temp / "sidecar-symlink"
        completed = launch(target, True)
        if completed.returncode != 0:
            raise AssertionError(completed.stdout + completed.stderr)
        fake = temp / "symlink-openwiki"
        make_fake(fake, symlink_output=True)
        rejected = run(
            [str(target / "scripts" / "openwiki-sidecar"), "init", "--command", str(fake)],
            cwd=target,
        )
        if rejected.returncode != 9 or "prohibited symlink" not in rejected.stderr:
            raise AssertionError(rejected.stdout + rejected.stderr)
        if (target / "openwiki" / "external.md").exists():
            raise AssertionError("generated symlink was imported")


def test_concurrent_run_lock_fails_closed() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-openwiki-lock-") as td:
        temp = Path(td)
        target = temp / "sidecar-lock"
        completed = launch(target, True)
        if completed.returncode != 0:
            raise AssertionError(completed.stdout + completed.stderr)
        fake = temp / "locked-openwiki"
        make_fake(fake)
        lock = target / ".okf-runtime" / "openwiki-sidecar.lock"
        lock.parent.mkdir(parents=True)
        lock.write_text("held", encoding="utf-8")
        rejected = run(
            [str(target / "scripts" / "openwiki-sidecar"), "init", "--command", str(fake)],
            cwd=target,
        )
        if rejected.returncode != 9 or "another OpenWiki sidecar run" not in rejected.stderr:
            raise AssertionError(rejected.stdout + rejected.stderr)
        if lock.read_text(encoding="utf-8") != "held":
            raise AssertionError("wrapper removed another process's lock")
        if (target / "openwiki" / "generated.md").exists():
            raise AssertionError("locked run imported output")


def main() -> int:
    tests = [
        test_sidecar_is_opt_in,
        test_staged_run_imports_only_bounded_outputs_and_sync_preserves_blocks,
        test_attempted_okf_mutation_fails_without_import,
        test_generated_symlink_is_not_imported,
        test_concurrent_run_lock_fails_closed,
    ]
    for test in tests:
        test()
    print(f"OpenWiki sidecar tests passed ({len(tests)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
