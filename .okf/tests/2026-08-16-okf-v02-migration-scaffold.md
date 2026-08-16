---
type: Test Evidence
title: OKF v0.2 Migration and Scaffold Validation
description: Strict validation evidence for work package 2 covering migration, canonical scaffold delegation, standalone fallback, skills, and adapters.
status: stable
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/tests/2026-08-16-okf-v02-migration-scaffold.md
tags: [okf, v0.2, migration, scaffold, skills, validation, pr-2]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: tested
generated: { by: process:okf-v02-migration-scaffold, at: 2026-08-16T17:25:01+01:00 }
---

# Scope

Validate work package 2 against [the bootstrap requirement](../requirements/okf-bootstrap-kit.md) and [the shared skills feature](../features/shared-okf-skills.md).

# Test Matrix

| Command | Result | Coverage |
|---------|--------|----------|
| `python3 tests/test_okf_migration.py` | PASS | Check/apply, idempotence, generated metadata, parse-error rollback |
| `python3 tests/test_scaffold_consolidation.py` | PASS | Canonical delegation, owner/display-name propagation, standalone v0.2 fallback, bundled runtime parity |
| `python3 tests/test_skill_contracts.py` | PASS | Minimal Codex frontmatter, extended Perplexity contract, v0.2 examples |
| `make check` | PASS | Full repository suite, launch smoke tests, strict validation, migration and adapter gates |
| `scripts/okf-migrate --check` | PASS | Live bundle requires no migration |
| `scripts/okf-validate --strict --format json` | PASS | Live bundle has zero errors and zero warnings |
| `scripts/okf-check-adapters` | PASS | Generated adapters match canonical skills |
| `scripts/okf-sync-skills --dry-run` | PASS | All generated adapter targets render successfully |
| Codex `quick_validate.py` over non-Perplexity skills | PASS | All 14 Codex-compatible skill folders validate |
| Package-wide `compileall` and `git diff --check` | PASS | Python syntax and patch whitespace |

# Result

PASS. Migration and both scaffold paths are deterministic and strict-v0.2 clean. The four Perplexity service adapters retain their required extended metadata and are validated by the repository contract suite rather than the Codex-only frontmatter validator.
