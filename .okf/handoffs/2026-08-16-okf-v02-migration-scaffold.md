---
type: Handoff
title: Work Package 2 - OKF v0.2 Migration and Scaffold
description: Completed migration, canonical scaffold delegation, portable fallback, v0.2 skill contracts, and strict adapter drift gates.
status: stable
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/handoffs/2026-08-16-okf-v02-migration-scaffold.md
tags: [okf, handoff, v0.2, migration, scaffold, skills, pr-2]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: tested
generated: { by: process:okf-v02-migration-scaffold, at: 2026-08-16T17:25:01+01:00 }
---

# Current State

Work package 2 is implementation-complete on `agent/okf-v02-02-migration-scaffold`, stacked on the conformance package. It is ready to serve as the base for deterministic index, graph, and freshness tooling.

# Completed Work

- Added atomic, idempotent `scripts/okf-migrate` check/apply behavior with JSON output and strict post-apply validation.
- Consolidated normal project creation onto `scripts/launch_project.sh` and the canonical template tree.
- Preserved a self-contained v0.2 fallback for installations that only have the Codex skill folder.
- Bundled shared validation, migration, skill-sync, and adapter-check behavior in emitted projects.
- Updated canonical skills and the four Perplexity adapters to current v0.2 contracts.
- Made adapter drift fail by default and expanded strict launch validation.

# Decisions Made

- `templates/new-project/` is the scaffold authority; embedded Python content is a portability fallback, not a second preferred path.
- Migration preserves unknown fields and Markdown bodies, maps legacy lifecycle values conservatively, and never invents `verified` metadata.
- Codex-compatible skills retain minimal `name` and `description` frontmatter. Perplexity adapters retain documented service-specific keys.
- Exact scaffold file counts are informational because profiles evolve; required artifacts and strict gates are authoritative.

# Files Changed

Core changes are under `scripts/okf-migrate`, `scripts/lib/okf_migration.py`, `scripts/launch_project.sh`, `scripts/validate_launch.sh`, `skills/`, `templates/new-project/`, `tests/`, `docs/`, `Makefile`, and the affected `.okf/` concepts.

# Known Issues

- Per-directory index content is still manually maintained; work package 3 owns deterministic generation and drift checking.
- The bundle has no first-party graph export or automated `stale_after` inventory; work package 3 owns both.

# Next Recommended Actions

1. Add deterministic generated index blocks without overwriting operator-authored prose.
2. Add machine-readable and human-readable graph exports from Markdown concept links.
3. Add freshness reporting for `stale_after` metadata and make it available to CI.

# Validation Needed

Completed: migration, scaffold consolidation, skill contract tests, full `make check`, strict live validation, migration drift, adapter drift, adapter regeneration dry run, Codex quick validation, package-wide Python compilation, and whitespace checks all pass. Re-run after conflict resolution or stacked-branch rebases.

# Context Pack

- [Requirement](../requirements/okf-bootstrap-kit.md)
- [Shared skills feature](../features/shared-okf-skills.md)
- [Validation evidence](../tests/2026-08-16-okf-v02-migration-scaffold.md)
- [Lessons learned](../improvements/2026-08-16-okf-v02-migration-scaffold-lessons.md)
- [Migration guide](../../docs/migrate-okf-v02.md)
