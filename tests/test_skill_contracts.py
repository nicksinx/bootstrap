"""Cross-platform OKF skill frontmatter and v0.2 contract tests."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
PERPLEXITY_KEYS = {"name", "description", "applies_to", "okf_mode", "canonical_skill"}
CANONICAL_KEYS = {"name", "description"}


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"missing frontmatter: {path}")
    _, raw, _ = text.split("---\n", 2)
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise AssertionError(f"invalid frontmatter: {path}")
    return data


def test_frontmatter_shapes_and_links() -> None:
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        data = frontmatter(path)
        folder = path.parent.name
        if data.get("name") != folder:
            raise AssertionError(f"skill name/folder mismatch: {path}")
        if not isinstance(data.get("description"), str) or not data["description"].strip():
            raise AssertionError(f"empty description: {path}")
        if folder.startswith("perplexity-okf-"):
            if set(data) != PERPLEXITY_KEYS:
                raise AssertionError(f"invalid Perplexity adapter keys: {path}: {set(data)}")
            if data["applies_to"] != ["perplexity"]:
                raise AssertionError(f"invalid applies_to: {path}")
            if not set(data["okf_mode"]).issubset({"research", "overflow"}):
                raise AssertionError(f"invalid okf_mode: {path}")
            canonical = ROOT / data["canonical_skill"]
            if not canonical.is_file():
                raise AssertionError(f"missing canonical skill: {path}: {canonical}")
        elif set(data) != CANONICAL_KEYS:
            raise AssertionError(f"Codex-facing skill must use name/description only: {path}")


def test_skill_examples_use_v02_metadata() -> None:
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if re.search(r"^timestamp:", text, re.MULTILINE):
            raise AssertionError(f"legacy timestamp example: {path}")
        if re.search(r"^status: (active|superseded|archived)$", text, re.MULTILINE):
            raise AssertionError(f"legacy status example: {path}")
    concept_writer = (SKILLS / "okf-concept-writer" / "SKILL.md").read_text()
    for required in ("generated:", "sources", "stale_after", "verified"):
        if required not in concept_writer:
            raise AssertionError(f"concept writer missing v0.2 guidance: {required}")


def main() -> int:
    tests = [test_frontmatter_shapes_and_links, test_skill_examples_use_v02_metadata]
    for test in tests:
        test()
    print(f"skill contract tests passed ({len(tests)} cases, 18 skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
