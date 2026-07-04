"""Tests for project-intake CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTAKE = ROOT / "scripts" / "project-intake"
EXAMPLE = ROOT / "skills" / "bootstrap-okf-forge-project" / "references" / "intake-example.yaml"
SCHEMA = ROOT / "schemas" / "project-intake.schema.json"


def run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INTAKE), *argv],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


def test_intake_schema_loads() -> None:
    doc = json.loads(SCHEMA.read_text())
    assert doc["title"] == "ProjectIntake"


def test_example_validates_except_paths() -> None:
    import tempfile

    import yaml

    sys.path.insert(0, str(ROOT / "scripts" / "lib"))
    from copy_okf_skills import copy_okf_skills  # noqa: E402

    data = yaml.safe_load(EXAMPLE.read_text())
    with tempfile.TemporaryDirectory() as td:
        target = Path(td) / "acme-signals"
        data["paths"]["target_dir"] = str(target)
        data["paths"]["bootstrap_root"] = str(ROOT)
        data["paths"]["forge_siblings_parent"] = str(Path(td))
        intake = Path(td) / "intake.yaml"
        intake.write_text(yaml.safe_dump(data, sort_keys=False))
        out = run(["validate", str(intake)])
        if out.returncode != 0:
            raise SystemExit(out.stderr or out.stdout)


def test_init_writes_file() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        target = Path(td) / "demo-product"
        out_path = Path(td) / "demo.yaml"
        out = run(
            [
                "init",
                "--project-id",
                "demo-product",
                "--target-dir",
                str(target),
                "-o",
                str(out_path),
            ]
        )
        if out.returncode != 0:
            raise SystemExit(out.stderr or out.stdout)
        if not out_path.is_file():
            raise SystemExit("init did not write file")


def test_copy_okf_skills_excludes_bootstrap_only() -> None:
    import tempfile

    from copy_okf_skills import copy_okf_skills

    with tempfile.TemporaryDirectory() as td:
        bootstrap = Path(td) / "bootstrap"
        product = Path(td) / "product"
        (bootstrap / "skills" / "okf-reader").mkdir(parents=True)
        (bootstrap / "skills" / "okf-reader" / "SKILL.md").write_text("---\nname: okf-reader\n---\n")
        (bootstrap / "skills" / "bootstrap-okf-forge-project").mkdir(parents=True)
        (bootstrap / "skills" / "bootstrap-okf-forge-project" / "SKILL.md").write_text(
            "---\nname: bootstrap-okf-forge-project\n---\n"
        )
        copied = copy_okf_skills(bootstrap, product)
        if copied != ["okf-reader"]:
            raise SystemExit(f"unexpected copied list: {copied}")
        if not (product / "skills" / "okf-reader" / "SKILL.md").is_file():
            raise SystemExit("okf-reader not copied")
        if (product / "skills" / "bootstrap-okf-forge-project").exists():
            raise SystemExit("bootstrap-only skill should be excluded")


def main() -> int:
    test_intake_schema_loads()
    test_example_validates_except_paths()
    test_init_writes_file()
    test_copy_okf_skills_excludes_bootstrap_only()
    print("project-intake tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
