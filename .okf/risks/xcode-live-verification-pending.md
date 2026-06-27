---
type: Risk
title: Xcode Live Verification Pending
description: Service 4 agent rule and step-4 setup may be dry-verified only until real Xcode build and test evidence exists.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/risks/xcode-live-verification-pending.md
tags: [okf, risk, xcode, verification, dispatch]
applies_to: [xcode-claude, cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-28T16:00:00+02:00
---

# Risk

OKF documents Xcode-connected Claude Agent as service 4, but `.okf/agents/xcode-claude.md` may remain at `status: draft` and `verification_status: unverified` when only **dry** repo verification has run (file presence, dispatch packet exercise, validate pass).

Operators or agents may assume step 4 is fully complete and promote the agent rule without live build, simulator, or signing validation.

# Impact

- Dispatch packets assigned to `xcode-claude` may stall if the Xcode agent cannot consume them in practice.
- Apple-platform constraints (signing, SPM, simulator) discovered late may invalidate handoffs to Perplexity step 5.
- False confidence in five-service setup order before Perplexity research begins.

# Likelihood

High for bootstrap-only work (Project-1 kit). Medium once a real macOS/iOS target project exists but live verification is skipped.

# Mitigations

- Run `.okf/prompts/xcode-step4-verification-checklist.md` before claiming dry PASS.
- Record dry results in `.okf/tests/YYYY-MM-DD-xcode-step4-dry-verification.md`.
- Use `.okf/handoffs/TEMPLATE-xcode-step4.md` with explicit **dry / live / deferred** verification level.
- Promote `.okf/agents/xcode-claude.md` to `active` / `reviewed` **only** after live build/test evidence.
- Keep signing secrets out of OKF; document constraints as risks or handoff notes.

# Monitoring

- Check handoffs for "verification level: dry" vs "live"
- Revisit when first real Apple target project (e.g. ProcureLex) enters Xcode step 4
- Close or downgrade this risk after live evidence and agent rule promotion

# Related Concepts

- `.okf/agents/xcode-claude.md`
- `docs/create-new-okf-project-in-xcode.md`
- `.okf/prompts/xcode-step4-verification-checklist.md`
- `.okf/tests/2026-06-28-xcode-step4-dry-verification.md`
