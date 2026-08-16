---
type: Improvement
title: OKF Index, Graph, and Freshness Lessons
description: Reusable lessons from adding deterministic navigation and knowledge-maintenance signals without weakening human ownership.
status: stable
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/improvements/2026-08-16-okf-index-graph-freshness-lessons.md
tags: [okf, index, graph, freshness, deterministic, continuous-improvement]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: reviewed
stale_after: 2026-11-16
generated: { by: process:okf-index-graph-freshness, at: 2026-08-16T17:39:00+01:00 }
---

# Observation

A fully generated index is deterministic but can erase operator guidance. A fully manual index preserves judgment but drifts as concepts move. Freshness fields are similarly useful only when overdue dates trigger review rather than automatic rewriting.

# Impact

Navigation automation that owns the whole file discourages useful authored context. Time-based automation that mutates trust or lifecycle state can turn a review signal into fabricated knowledge.

# Recommendation

- Give generators an explicit marked block and preserve all content outside it.
- Parse the entire bundle and validate marker pairs before the first index write.
- Make check mode and a second no-op run part of the release gate.
- Derive graph edges only from resolvable Markdown links; keep exports read-only and local by default.
- Calculate freshness against an explicit audit date in tests.
- Treat `stale_after` as a review deadline only; require evidence before changing content, trust, or lifecycle state.
- Seed reasonable deadlines in new scaffolds while allowing historical evidence to remain untracked.
- Assert documented five-service artifacts in launch smoke tests; delegating to one launcher does not by itself prove template parity.
- Treat case-variant landing pages such as `INDEX.md` explicitly so macOS and Linux generate the same navigation without self-links.
