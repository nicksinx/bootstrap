---
type: Improvement
title: Xcode step 4 dry verification lessons
description: Lessons from Wave 3 dry verification of service 4 without live Xcode.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/improvements/2026-06-28-xcode-step4-dry-lessons.md
tags: [okf, improvement, xcode, step-4, verification]
applies_to: [cursor, claude, codex, xcode-claude, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-28T16:00:00+02:00
---

# Observation

Wave 3 closed most service-4 gaps without Xcode: expanded setup guide, dry checklist, dispatch dry-run, agent rule depth, risk note, and handoff template. Live verification remains a separate gate.

# Context

Project-1 bootstrap refinement backlog item 3. Prior xcode guide was ~43 lines; Claude step-3 guide ~360 lines.

# Impact

- Operators can run step 4 dry verification on any scaffolded OKF project before Apple hardware work.
- Reduces false promotion of `xcode-claude` agent rule from chat assumptions alone.
- Dispatch `xcode-claude` runner proven at file-queue level; Xcode UI consumption still unverified.

# Recommendation

1. Always record **dry vs live** verification level in step 4 handoffs.
2. Run `.okf/prompts/xcode-step4-verification-checklist.md` before Perplexity step 5 on Apple-target projects.
3. Keep `.okf/risks/xcode-live-verification-pending.md` open until first live evidence.
4. Clean up dispatch dry-run test pipelines after evidence capture.

# Action Items

- [x] Expand `docs/create-new-okf-project-in-xcode.md`
- [x] Add dry verification checklist prompt
- [x] Dispatch dry-run evidence
- [x] Risk + handoff template
- [ ] Live Xcode verification (user / ProcureLex)
- [ ] Promote `.okf/agents/xcode-claude.md` after live evidence

# Related Concepts

- `.okf/tests/2026-06-28-xcode-step4-dry-verification.md`
- `.okf/risks/xcode-live-verification-pending.md`
- `.okf/handoffs/TEMPLATE-xcode-step4.md`

# Review Cadence

Revisit when ProcureLex or another Apple target enters Xcode step 4.
