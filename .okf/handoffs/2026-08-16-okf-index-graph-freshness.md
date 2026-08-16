---
type: Handoff
title: Work Package 3 - OKF Index, Graph, and Freshness
description: Completed deterministic indexes, read-only graph exports, freshness checks, generated-project propagation, and strict release gates.
status: stable
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/handoffs/2026-08-16-okf-index-graph-freshness.md
tags: [okf, handoff, index, graph, freshness, pr-3]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: tested
stale_after: 2026-11-16
generated: { by: process:okf-index-graph-freshness, at: 2026-08-16T17:39:00+01:00 }
---

# Current State

Work package 3 is implementation-complete on `agent/okf-v02-03-index-graph-freshness`, stacked on the migration/scaffold package. It is ready to serve as the base for optional integrations and the experimental attestation slice.

# Completed Work

- Added safe generated blocks and per-directory `index.md` generation with check/write modes.
- Added deterministic JSON and self-contained HTML graph exports from internal Markdown links.
- Added `stale_after` inventory with reproducible audit dates and CI-friendly failure modes.
- Added 90-day freshness deadlines to canonical and standalone project scaffolds.
- Propagated all commands, shared runtime, docs, Make targets, and launch validation gates.
- Restored canonical scaffold parity for the Perplexity/Xcode agent and prompt layer, handoff templates, context-pack guide, and Codex install guide.
- Added deterministic compatibility handling for legacy case-variant `INDEX.md` landing pages.
- Added focused rollback, idempotence, relationship, HTML, freshness, and scaffold tests.

# Decisions Made

- Operators own prose outside index markers; `scripts/okf-index` owns only the marked block.
- Graph generation is read-only and local, with no CDN or runtime service dependency.
- A concept becomes stale only after its `stale_after` date, not on the date itself.
- Missing deadlines remain visible but fail only under `--require-deadlines`; historical evidence is not rewritten solely to satisfy coverage.

# Files Changed

Core changes are under `scripts/lib/okf_tooling.py`, `scripts/okf-index`, `scripts/okf-freshness`, `scripts/okf-visualize`, `templates/new-project/`, `skills/create-new-okf-project/`, `tests/test_okf_tooling.py`, `tests/test_launch_smoke.py`, `docs/`, `Makefile`, and the affected `.okf/` concepts and indexes.

# Known Issues

- OpenWiki remains an optional external sidecar and is not yet represented in launcher configuration.
- The repository has no first-party read-only MCP query surface.
- Attested Computation has schema validation but no executable sample receipt/attester experiment.

# Next Recommended Actions

1. Add opt-in OpenWiki sidecar configuration without allowing generated wiki output to overwrite curated OKF.
2. Add a path-contained, read-only MCP pilot for concept summary/search/read/neighbor operations.
3. Add one deterministic Attested Computation and clearly label its receipt/verdict transport as experimental.

# Validation Needed

Completed: focused tooling, scaffold, and launch tests; full `make check`; strict OKF, migration, index, freshness, adapter, skill-sync, compilation, and whitespace gates all pass. Re-run after conflict resolution or stacked-branch rebases.

# Context Pack

- [Requirement](../requirements/okf-bootstrap-kit.md)
- [Architecture](../architecture/okf-bootstrap-layout.md)
- [Workflow](../workflows/okf-index-graph-freshness-review.md)
- [Validation evidence](../tests/2026-08-16-okf-index-graph-freshness.md)
- [Lessons learned](../improvements/2026-08-16-okf-index-graph-freshness-lessons.md)
- [Operator guide](../../docs/okf-index-graph-freshness.md)
