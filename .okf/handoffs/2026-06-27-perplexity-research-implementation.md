---
type: Handoff
title: Perplexity Research Implementation Handoff
description: Cursor implementation of P0/P1 items from Perplexity OKF shared services research pack.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/handoffs/2026-06-27-perplexity-research-implementation.md
tags: [okf, handoff, perplexity, research, implementation]
applies_to: [cursor, codex, claude, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T20:00:00+02:00
---

# Current State

Perplexity research pack ingested. P0/P1 improvements implemented in bootstrap repo. References remain `unverified` until human promotion.

# Completed Work

- Saved 11 references under `.okf/references/`
- Added handoff README + TEMPLATE, context-pack index
- Added `docs/perplexity-project-files-and-skills.md`, `docs/skill-frontmatter-compatibility.md`
- Added improvement concept with accepted lessons
- Extended `scripts/okf-validate` for draft Reference rules
- Updated index, log, configure-perplexity doc

# Decisions Made

- Spaces documented as verified Perplexity surface; no single Desktop Pro Projects spec assumed.
- Attachment budget policy: curated ~8–14 files, no hard-coded byte cap until in-product verification.
- `scripts/okf-sync-skills` remains adapter source of truth (scaffold parity deferred).

# Files Changed

See `.okf/log.md` entry 2026-06-27 (Perplexity research implementation).

# Known Issues

- `create-new-okf-project` scaffold not yet updated to emit new Perplexity/handoff files.
- `scripts/okf-dispatch` overflow metadata not automated.
- Stale-adapter diff script (P2) not implemented.

# Next Recommended Actions

1. Run Codex bootstrap propagation prompt to sync scaffold with bootstrap repo.
2. Live-test Perplexity attachment tier list on a real project (e.g. ProcureLex).
3. Promote selected research findings to `.okf/decisions/` or requirements after review.

# Validation Needed

- `scripts/okf-validate` after merge
- Confirm no draft Reference uses `source_of_truth: true`

# Context Pack

- Improvement: `.okf/improvements/2026-06-27-perplexity-research-lessons.md`
- References index: `.okf/references/multi-agent-risks.md` and siblings
