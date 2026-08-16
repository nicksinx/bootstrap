---
type: Test Evidence
title: OKF v0.2 Conformance Validation
description: Strict validation evidence for work package 1 covering the live bundle, parser, schema, templates, and fresh project launch.
status: stable
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/tests/2026-08-16-okf-v02-conformance.md
tags: [okf, v0.2, conformance, validation, pr-1]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: tested
generated: { by: process:okf-v02-conformance, at: 2026-08-16T17:02:47+01:00 }
---

# Scope

Validate the work package against [the bootstrap requirement](../requirements/okf-bootstrap-kit.md) and the repository's v0.2 profile.

# Test Matrix

| Command | Result | Coverage |
|---------|--------|----------|
| `python3 tests/test_okf_conformance.py` | PASS | Valid bundle, malformed/duplicate YAML, reserved files, legacy metadata, JSON output |
| `python3 tests/test_contracts.py` | PASS | Updated OKF v0.2 JSON Schema plus existing contracts |
| `python3 tests/test_launch_smoke.py` | PASS | Default and Forge alias scaffolds; generated strict OKF validation |
| `PYTHONPYCACHEPREFIX=/private/tmp/okf-pycache python3 -m compileall -q scripts tests` | PASS | Python syntax without writing into the macOS protected cache |
| `scripts/okf-validate --strict --format json` | PASS | 73 pre-evidence concepts, zero errors, zero warnings |
| `make check` | PASS | Full contracts, launch, intake, conformance, and strict live-bundle suite |
| GitHub Actions `bootstrap-ci / validate` on PR #2 | PASS | Ubuntu/Python 3.11 dependency install and the full `make check` gate after removing unsupported pip caching |
| `scripts/okf-check-adapters` | PASS | 18 canonical skills, zero drift warnings |
| `scripts/okf-sync-skills --dry-run` | PASS | All five generated adapter targets render successfully |
| `PYTHONPYCACHEPREFIX=/private/tmp/okf-pycache-pr1 python3 -m compileall -q scripts skills tests` | PASS | Final package-wide Python compilation |

# Result

PASS. The full package gate completed locally and on GitHub Actions with 76 live concepts, zero strict OKF warnings, zero adapter-drift warnings, and no known conformance defects.
