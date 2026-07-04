#!/usr/bin/env python3
"""Copy canonical OKF skills from bootstrap kit into a launched product."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

BOOTSTRAP_ONLY = frozenset({"bootstrap-okf-forge-project"})


def copy_okf_skills(bootstrap_root: Path, target_root: Path, dry_run: bool = False) -> list[str]:
    """Copy skills/*/ from bootstrap into target/skills/, excluding bootstrap-only skills."""
    src_root = bootstrap_root / "skills"
    dest_root = target_root / "skills"
    if not src_root.is_dir():
        raise FileNotFoundError(f"skills source missing: {src_root}")

    copied: list[str] = []
    for skill_dir in sorted(src_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        name = skill_dir.name
        if name.startswith("."):
            continue
        if name in BOOTSTRAP_ONLY:
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        dest = dest_root / name
        if dry_run:
            print(f"[dry-run] would copy {skill_dir} -> {dest}")
            copied.append(name)
            continue
        dest_root.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(skill_dir, dest)
        copied.append(name)
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy OKF skills tree into a product repo")
    parser.add_argument("bootstrap_root", type=Path)
    parser.add_argument("target_root", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        copied = copy_okf_skills(
            args.bootstrap_root.expanduser().resolve(),
            args.target_root.expanduser().resolve(),
            dry_run=args.dry_run,
        )
    except FileNotFoundError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 3

    if not copied:
        print("WARN: no skills copied", file=sys.stderr)
        return 1

    print(f"copied {len(copied)} skill(s): {', '.join(copied)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
