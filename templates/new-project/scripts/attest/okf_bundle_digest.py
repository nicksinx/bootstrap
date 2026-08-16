#!/usr/bin/env python3
"""Generate a deterministic experimental receipt for curated OKF concepts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, help="Receipt path outside .okf; stdout if omitted.")
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    sys.path.insert(0, str(root / "scripts" / "lib"))
    try:
        from okf_attestation import AttestationError, build_receipt, write_json

        receipt = build_receipt(root)
        if args.output:
            write_json(args.output, receipt, root)
            print(args.output.expanduser().resolve())
        else:
            print(json.dumps(receipt, indent=2, sort_keys=True))
    except (AttestationError, OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"okf-bundle-digest: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
