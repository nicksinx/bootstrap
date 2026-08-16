#!/usr/bin/env python3
"""Deterministic receipt and verdict helpers for the OKF attestation experiment."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from okf_tooling import load_concepts


EXPERIMENT_VERSION = "project-bootstrap/okf-attestation-experiment-v1"
COMPUTATION = ".okf/computations/bootstrap-integrity.md"
ALGORITHM = "sha256"
RECEIPT_KEYS = {
    "experiment_version",
    "okf_version",
    "computation",
    "algorithm",
    "manifest",
    "bundle_digest",
}


class AttestationError(ValueError):
    """Raised when a receipt cannot be generated or verified safely."""


def _sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")


def _manifest(root: Path) -> list[dict[str, str]]:
    root = root.resolve()
    okf = (root / ".okf").resolve()
    symlinks = [
        path.relative_to(root).as_posix()
        for path in sorted(okf.rglob("*.md"))
        if path.is_symlink()
    ]
    if symlinks:
        raise AttestationError(
            "symlink concepts are not attested: " + ", ".join(symlinks)
        )
    items = []
    for concept in load_concepts(root):
        if concept.path.is_symlink():
            raise AttestationError(f"symlink concepts are not attested: {concept.relative}")
        resolved = concept.path.resolve()
        try:
            resolved.relative_to(okf)
        except ValueError as exc:
            raise AttestationError(f"concept escapes .okf: {concept.relative}") from exc
        items.append({"path": concept.relative, "sha256": _sha256_bytes(concept.path.read_bytes())})
    return sorted(items, key=lambda item: item["path"])


def build_receipt(root: Path) -> dict[str, Any]:
    root = root.resolve()
    manifest = _manifest(root)
    return {
        "experiment_version": EXPERIMENT_VERSION,
        "okf_version": "0.2",
        "computation": COMPUTATION,
        "algorithm": ALGORITHM,
        "manifest": manifest,
        "bundle_digest": _sha256_bytes(_canonical_json(manifest)),
    }


def _check(name: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"name": name, "passed": passed, "detail": detail}


def verify_receipt(root: Path, receipt: Any) -> dict[str, Any]:
    checks = []
    if not isinstance(receipt, dict):
        checks.append(_check("receipt-shape", False, "receipt must be a JSON object"))
        return _verdict(checks)

    checks.append(
        _check(
            "receipt-keys",
            set(receipt) == RECEIPT_KEYS,
            "top-level keys match the experimental ABI",
        )
    )
    checks.append(
        _check(
            "experiment-version",
            receipt.get("experiment_version") == EXPERIMENT_VERSION,
            f"expected {EXPERIMENT_VERSION}",
        )
    )
    checks.append(
        _check("okf-version", receipt.get("okf_version") == "0.2", "expected OKF v0.2")
    )
    checks.append(
        _check(
            "computation",
            receipt.get("computation") == COMPUTATION,
            f"expected {COMPUTATION}",
        )
    )
    checks.append(
        _check("algorithm", receipt.get("algorithm") == ALGORITHM, f"expected {ALGORITHM}")
    )

    manifest = receipt.get("manifest")
    valid_manifest = isinstance(manifest, list) and all(
        isinstance(item, dict)
        and set(item) == {"path", "sha256"}
        and isinstance(item.get("path"), str)
        and isinstance(item.get("sha256"), str)
        for item in (manifest or [])
    )
    checks.append(_check("manifest-shape", valid_manifest, "manifest entries are path/hash pairs"))

    if valid_manifest:
        sorted_manifest = sorted(manifest, key=lambda item: item["path"])
        checks.append(
            _check("manifest-order", manifest == sorted_manifest, "manifest is path-sorted")
        )
        duplicate_free = len({item["path"] for item in manifest}) == len(manifest)
        checks.append(_check("manifest-unique", duplicate_free, "manifest paths are unique"))
        expected_digest = _sha256_bytes(_canonical_json(manifest))
        checks.append(
            _check(
                "receipt-digest",
                receipt.get("bundle_digest") == expected_digest,
                "bundle digest matches the receipt manifest",
            )
        )
        try:
            current = _manifest(root)
        except (AttestationError, OSError, UnicodeDecodeError, ValueError) as exc:
            checks.append(_check("live-manifest", False, str(exc)))
        else:
            checks.append(
                _check(
                    "live-manifest",
                    manifest == current,
                    "receipt exactly matches the current curated concept set and bytes",
                )
            )
    else:
        checks.extend(
            [
                _check("manifest-order", False, "manifest shape invalid"),
                _check("manifest-unique", False, "manifest shape invalid"),
                _check("receipt-digest", False, "manifest shape invalid"),
                _check("live-manifest", False, "manifest shape invalid"),
            ]
        )
    return _verdict(checks)


def _verdict(checks: list[dict[str, Any]]) -> dict[str, Any]:
    passed = all(check["passed"] for check in checks)
    return {
        "experiment_version": EXPERIMENT_VERSION,
        "verdict": "pass" if passed else "fail",
        "checks": checks,
    }


def write_json(path: Path, value: Any, root: Path) -> None:
    path = path.expanduser().resolve()
    okf = (root.resolve() / ".okf").resolve()
    try:
        path.relative_to(okf)
    except ValueError:
        pass
    else:
        raise AttestationError("attestation runtime output must not be written under .okf")
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(value, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False, newline=""
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.replace(temporary, path)
