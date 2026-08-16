#!/usr/bin/env python3
"""Verify an experimental OKF bundle receipt against current concept bytes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    sys.path.insert(0, str(root / "scripts" / "lib"))
    try:
        from okf_attestation import verify_receipt

        receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
        verdict = verify_receipt(root, receipt)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        verdict = {
            "experiment_version": "project-bootstrap/okf-attestation-experiment-v1",
            "verdict": "fail",
            "checks": [{"name": "receipt-load", "passed": False, "detail": str(exc)}],
        }
    print(json.dumps(verdict, indent=2, sort_keys=True))
    return 0 if verdict["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
