---
type: Workflow
title: OKF Index, Graph, and Freshness Review
description: Deterministic operating sequence for keeping navigation current, inspecting concept relationships, and reviewing stale knowledge.
status: stable
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/workflows/okf-index-graph-freshness-review.md
tags: [okf, workflow, index, graph, freshness]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: reviewed
stale_after: 2026-11-16
generated: { by: process:okf-index-graph-freshness, at: 2026-08-16T17:39:00+01:00 }
---

# Purpose

Keep OKF navigation deterministic and make stale knowledge visible without replacing human review or changing concept trust automatically.

# Triggers

- After adding, moving, renaming, or removing an OKF concept.
- Before a substantive handoff, commit, pull request, or release.
- At the project's agreed knowledge-review cadence.

# Required Sequence

1. Run `scripts/okf-migrate --check`.
2. Run `scripts/okf-validate --strict` and fix structural or safety issues.
3. Run `scripts/okf-index --write`, then `scripts/okf-index --check` to prove convergence.
4. Run `scripts/okf-freshness --check`; review every stale result before extending or replacing its deadline.
5. Use `scripts/okf-visualize --format html --output /tmp/okf-graph.html` when relationship or orphan analysis is useful.
6. Run `scripts/okf-check-adapters` after canonical skill changes.
7. Record test evidence, lessons, and a handoff for substantive work.

# Freshness Disposition

- `current`: no freshness action is required.
- `stale`: review the concept against current authoritative evidence; update content and deadline only when justified.
- `untracked`: add `stale_after` when the concept needs a review cadence; historical evidence may remain untracked.
- `deprecated`: retain for history unless the repository retention policy says otherwise.

Do not invent `verified` events, silently promote draft research, or delete a concept solely because its review date passed.

# Related Material

- [Bootstrap requirement](../requirements/okf-bootstrap-kit.md)
- [Architecture](../architecture/okf-bootstrap-layout.md)
- [Operator guide](../../docs/okf-index-graph-freshness.md)
