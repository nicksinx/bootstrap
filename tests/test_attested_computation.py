"""Determinism, tamper, containment, and concept-contract tests for attestation."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EXECUTOR = ROOT / "scripts" / "attest" / "okf_bundle_digest.py"
ATTESTER = ROOT / "scripts" / "attest" / "verify_okf_bundle_digest.py"
WRAPPER = ROOT / "scripts" / "okf-attest-experiment"


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def copy_bundle(target: Path) -> None:
    shutil.copytree(ROOT / ".okf", target / ".okf")
    (target / "scripts" / "lib").mkdir(parents=True)
    for name in ("okf_attestation.py", "okf_tooling.py", "okf_validation.py"):
        shutil.copy2(ROOT / "scripts" / "lib" / name, target / "scripts" / "lib" / name)


def test_receipt_is_deterministic_and_verifies() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-attest-repeat-") as td:
        temp = Path(td)
        first = temp / "first.json"
        second = temp / "second.json"
        for output in (first, second):
            completed = run([str(EXECUTOR), "--root", str(ROOT), "--output", str(output)])
            if completed.returncode != 0:
                raise AssertionError(completed.stdout + completed.stderr)
        if first.read_bytes() != second.read_bytes():
            raise AssertionError("identical OKF inputs produced different receipts")
        receipt = json.loads(first.read_text())
        paths = [item["path"] for item in receipt["manifest"]]
        if paths != sorted(paths) or ".okf/computations/bootstrap-integrity.md" not in paths:
            raise AssertionError(paths)
        verified = run([str(ATTESTER), str(first), "--root", str(ROOT)])
        if verified.returncode != 0 or json.loads(verified.stdout)["verdict"] != "pass":
            raise AssertionError(verified.stdout + verified.stderr)


def test_tampering_and_live_changes_fail() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-attest-tamper-") as td:
        temp = Path(td)
        project = temp / "project"
        copy_bundle(project)
        receipt_path = temp / "receipt.json"
        generated = run(
            [str(EXECUTOR), "--root", str(project), "--output", str(receipt_path)]
        )
        if generated.returncode != 0:
            raise AssertionError(generated.stdout + generated.stderr)

        tampered = json.loads(receipt_path.read_text())
        tampered["bundle_digest"] = "sha256:" + "0" * 64
        tampered_path = temp / "tampered.json"
        tampered_path.write_text(json.dumps(tampered), encoding="utf-8")
        rejected = run([str(ATTESTER), str(tampered_path), "--root", str(project)])
        payload = json.loads(rejected.stdout)
        if rejected.returncode != 1 or payload["verdict"] != "fail":
            raise AssertionError(rejected.stdout + rejected.stderr)
        if next(c for c in payload["checks"] if c["name"] == "receipt-digest")["passed"]:
            raise AssertionError(payload)

        project_file = project / ".okf" / "project.md"
        project_file.write_text(project_file.read_text() + "\nChanged after receipt.\n")
        stale = run([str(ATTESTER), str(receipt_path), "--root", str(project)])
        stale_payload = json.loads(stale.stdout)
        if stale.returncode != 1 or next(
            c for c in stale_payload["checks"] if c["name"] == "live-manifest"
        )["passed"]:
            raise AssertionError(stale_payload)


def test_runtime_output_and_symlink_boundaries() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-attest-boundary-") as td:
        temp = Path(td)
        project = temp / "project"
        copy_bundle(project)
        forbidden = project / ".okf" / "receipt.json"
        rejected = run(
            [str(EXECUTOR), "--root", str(project), "--output", str(forbidden)]
        )
        if rejected.returncode != 2 or "must not be written under .okf" not in rejected.stderr:
            raise AssertionError(rejected.stdout + rejected.stderr)
        if forbidden.exists():
            raise AssertionError("forbidden receipt was written under .okf")

        external = temp / "external.md"
        external.write_text(
            "---\ntype: Reference\ntitle: Outside\ndescription: Outside.\nstatus: stable\n---\n# Outside\n",
            encoding="utf-8",
        )
        link = project / ".okf" / "references" / "external-link.md"
        link.symlink_to(external)
        symlink_receipt = temp / "symlink.json"
        symlinked = run(
            [str(EXECUTOR), "--root", str(project), "--output", str(symlink_receipt)]
        )
        if symlinked.returncode != 2 or "symlink concepts are not attested" not in symlinked.stderr:
            raise AssertionError(symlinked.stdout + symlinked.stderr)


def test_wrapper_and_okf_concept_contract() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-attest-wrapper-") as td:
        receipt = Path(td) / "wrapper.json"
        executed = run(
            [str(WRAPPER), "run", "--root", str(ROOT), "--receipt", str(receipt)]
        )
        if executed.returncode != 0 or json.loads(executed.stdout)["verdict"] != "pass":
            raise AssertionError(executed.stdout + executed.stderr)
        verified = run(
            [str(WRAPPER), "verify", "--root", str(ROOT), "--receipt", str(receipt)]
        )
        if verified.returncode != 0 or json.loads(verified.stdout)["verdict"] != "pass":
            raise AssertionError(verified.stdout + verified.stderr)

    validation = run([str(ROOT / "scripts" / "okf-validate"), "--strict"])
    if validation.returncode != 0:
        raise AssertionError(validation.stdout + validation.stderr)


def main() -> int:
    tests = [
        test_receipt_is_deterministic_and_verifies,
        test_tampering_and_live_changes_fail,
        test_runtime_output_and_symlink_boundaries,
        test_wrapper_and_okf_concept_contract,
    ]
    for test in tests:
        test()
    print(f"Attested computation tests passed ({len(tests)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
