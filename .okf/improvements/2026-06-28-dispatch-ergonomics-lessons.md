---
type: Improvement
title: Dispatch ergonomics Wave 2 lessons
description: Lessons from role-specific handoff templates and live dispatch dry-run (pipe-cb8dc04e).
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/improvements/2026-06-28-dispatch-ergonomics-lessons.md
tags: [okf, improvement, dispatch, tester, reviewer, overflow]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-28T23:00:00+02:00
---

# Observation

Wave 2 added role-specific handoff templates and live pipeline evidence. Tester and reviewer roles now have structured deliverable tables instead of improvising from the generic template alone.

# Context

Claude Code Wave 2 after Cursor Wave 1 (scaffold parity) and Wave 3 dry (Xcode step 4). Dry-run pipeline `pipe-cb8dc04e` exercised builder → tester → reviewer → integrator with overflow metadata on tester packet.

# Impact

- Reduced ambiguity at role boundaries in multi-agent delivery.
- Overflow handoff stub auto-generation confirmed (`context.overflow`, next_steps).
- Operators must still select the correct template (see `.okf/handoffs/README.md` selection table).

# Recommendation

1. Use `TEMPLATE-tester.md` when completing the **tester** role — include command → PASS/FAIL/SKIP table and evidence paths.
2. Use `TEMPLATE-reviewer.md` for **reviewer** — requirements-checked table, findings with severity, explicit verdict.
3. On primary-runner block, run `scripts/okf-dispatch overflow` before Perplexity MODE B; do not skip metadata.
4. Reference `docs/okf-dispatch-orchestration.md` § Role handoff expectations for completion commands.
5. Full-kit scaffolds should copy all four handoff templates via `BOOTSTRAP_COPY_PATHS`.

# Action Items

- [x] `TEMPLATE-tester.md`, `TEMPLATE-reviewer.md`
- [x] README template selection table
- [x] `.okf/tests/2026-06-28-dispatch-dry-run.md`
- [x] Orchestration doc role expectations section
- [x] Bootstrap copy paths for all handoff templates
- [ ] First production pipeline using role templates on a real task

# Related Concepts

- `.okf/handoffs/TEMPLATE-tester.md`
- `.okf/handoffs/TEMPLATE-reviewer.md`
- `.okf/tests/2026-06-28-dispatch-dry-run.md`
- `docs/okf-dispatch-orchestration.md`

# Review Cadence

Revisit after first live overflow failover on a real project task.
