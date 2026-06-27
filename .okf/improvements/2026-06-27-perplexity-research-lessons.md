---
type: Improvement
title: Perplexity research lessons for shared OKF services
description: Accepted lessons from 2026-06-27 Perplexity deep research on configuring Cursor, Codex, Claude, Xcode, and Perplexity.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/improvements/2026-06-27-perplexity-research-lessons.md
tags: [okf, improvement, perplexity, shared-services, research]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T20:00:00+02:00
---

# Observation

Perplexity research confirmed OKF direction (thin adapters, canonical skills, file-based handoffs) and surfaced gaps in attachment strategy, overflow formalization, and scaffold propagation.

# Context

Research pack ingested from Perplexity MODE A session on Project-1 shared services configuration. References saved under `.okf/references/`.

# Impact

- Operators may over-attach files to Perplexity Spaces without curation.
- Adapter drift remains a risk if scaffold does not run `okf-sync-skills`.
- Unverified research could be mistaken for requirements without validation gates.

# Recommendation

1. **Curated attachment bundles** — cap Perplexity Project Files at ~8–14; document in `docs/perplexity-project-files-and-skills.md`.
2. **Handoff vs context-pack split** — handoffs for active transfer; context packs for ephemeral paste (` .okf/handoffs/README.md`, `.okf/context-packs/INDEX.md`).
3. **Spaces terminology** — document Spaces as verified Perplexity surface; do not assume separate “Desktop Pro Projects” spec beyond help center docs.
4. **Sync-driven adapters** — treat `scripts/okf-sync-skills` as source of truth for adapter regeneration (partially addresses P0 scaffold gap).
5. **Reference validation** — draft references must stay `verification_status: unverified` and `source_of_truth: false` until review.
6. **Overflow packet** — use `.okf/handoffs/TEMPLATE.md` overflow fields; `scripts/okf-dispatch overflow` records metadata and writes handoff.

# Action Items

- [x] Save research references to `.okf/references/`
- [x] Add handoff README and template
- [x] Add context-pack index and Perplexity files/skills guide
- [x] Add skill frontmatter compatibility doc
- [x] Extend `scripts/okf-validate` for Reference draft rules
- [x] Update `create-new-okf-project` scaffold to emit Perplexity + handoff README (follow-up)
- [x] Add dispatch overflow metadata fields (follow-up)
- [x] Stale-adapter diff script (P2 follow-up)

# Related Concepts

- `.okf/references/multi-agent-risks.md`
- `.okf/handoffs/2026-06-27-perplexity-okf-configuration.md`
- `docs/configure-perplexity-okf.md`

# Review Cadence

Revisit when Perplexity product docs change or after first live overflow failover on a real project.

When `.okf/log.md` records material operating-model changes, refresh `docs/okf-ways-of-working-brief.md` per its **Brief Maintenance** section and re-attach in Perplexity Project Files if applicable.
