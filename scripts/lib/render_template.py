#!/usr/bin/env python3
"""Render a template file by substituting __VAR__ placeholders from the
BOOTSTRAP_VAR_* environment variables.

Reads the file at $BOOTSTRAP_TEMPLATE_INPUT and writes rendered content
to stdout. Unknown placeholders are left untouched and a warning is
emitted on stderr (so the launcher can fail-fast under strict mode).
"""

from __future__ import annotations

import os
import re
import sys

PLACEHOLDER = re.compile(r"__([A-Z][A-Z0-9_]*)__")


def main() -> int:
    src = os.environ.get("BOOTSTRAP_TEMPLATE_INPUT")
    if not src:
        print("BOOTSTRAP_TEMPLATE_INPUT is required", file=sys.stderr)
        return 2

    with open(src, "r", encoding="utf-8") as fh:
        content = fh.read()

    vars_seen: set[str] = set()
    missing: list[str] = []

    def repl(match: "re.Match[str]") -> str:
        key = match.group(1)
        vars_seen.add(key)
        env_key = f"BOOTSTRAP_VAR_{key}"
        if env_key in os.environ:
            return os.environ[env_key]
        missing.append(key)
        return match.group(0)

    rendered = PLACEHOLDER.sub(repl, content)

    if missing and os.environ.get("BOOTSTRAP_STRICT_VARS", "1") == "1":
        print(
            f"missing template variables: {sorted(set(missing))}",
            file=sys.stderr,
        )
        return 3

    sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
