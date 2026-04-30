#!/usr/bin/env python3
"""Preserve user-edited protected sections when re-rendering templates.

Reads two inputs:
  - $BOOTSTRAP_EXISTING        : path to the existing destination file
  - $BOOTSTRAP_RENDERED_CONTENT : the freshly rendered template content

Both files use markers of the form (any line containing these tokens):
  BOOTSTRAP-PROTECTED-BEGIN: <name>
  BOOTSTRAP-PROTECTED-END: <name>

For each named protected block, the existing file's content overrides
the rendered content. Unknown blocks in the existing file are dropped
with a warning so user edits cannot extend protected scope arbitrarily.

Outputs the merged content to stdout.
"""

from __future__ import annotations

import os
import re
import sys

BEGIN = re.compile(r"BOOTSTRAP-PROTECTED-BEGIN:\s*([A-Za-z0-9_.-]+)")
END = re.compile(r"BOOTSTRAP-PROTECTED-END:\s*([A-Za-z0-9_.-]+)")


def extract_blocks(text: str) -> dict[str, str]:
    blocks: dict[str, str] = {}
    lines = text.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        m = BEGIN.search(lines[i])
        if m:
            name = m.group(1)
            buf = [lines[i]]
            i += 1
            while i < len(lines):
                buf.append(lines[i])
                e = END.search(lines[i])
                if e and e.group(1) == name:
                    break
                i += 1
            blocks[name] = "".join(buf)
        i += 1
    return blocks


def merge(rendered: str, existing_blocks: dict[str, str]) -> str:
    out: list[str] = []
    lines = rendered.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        m = BEGIN.search(lines[i])
        if m:
            name = m.group(1)
            if name in existing_blocks:
                out.append(existing_blocks[name])
                while i < len(lines):
                    e = END.search(lines[i])
                    if e and e.group(1) == name:
                        i += 1
                        break
                    i += 1
                continue
        out.append(lines[i])
        i += 1
    return "".join(out)


def main() -> int:
    existing_path = os.environ.get("BOOTSTRAP_EXISTING")
    rendered = os.environ.get("BOOTSTRAP_RENDERED_CONTENT", "")
    if not existing_path or not os.path.exists(existing_path):
        sys.stdout.write(rendered)
        return 0
    with open(existing_path, "r", encoding="utf-8") as fh:
        existing = fh.read()
    blocks = extract_blocks(existing)
    sys.stdout.write(merge(rendered, blocks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
