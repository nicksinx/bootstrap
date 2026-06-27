---
type: Reference
title: Xcode Step 4 Dry Verification Checklist
description: Repo-only verification for OKF service 4 before live Xcode build/test evidence exists.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/prompts/xcode-step4-verification-checklist.md
tags: [okf, prompt, xcode, verification, dry-run, step-4]
applies_to: [cursor, claude, codex, xcode-claude, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-28T16:00:00+02:00
---

# Purpose

Verify OKF **service 4 readiness** from the repository alone — no Xcode build, simulator, or signing required.

Use before live verification and before promoting `.okf/agents/xcode-claude.md` from `draft`.

Setup guide: `docs/create-new-okf-project-in-xcode.md`

# When to run

- After Claude Code step 3 handoff exists
- After scaffold from bootstrap kit
- Before claiming Xcode step 4 complete on a new project
- After changing dispatch runner maps or `xcode-claude` agent rule

# Checklist (run from project root)

## A. File presence

| # | Check | Command / path | Pass |
|---|-------|----------------|------|
| A1 | Xcode setup guide | `docs/create-new-okf-project-in-xcode.md` exists | ☐ |
| A2 | Xcode agent rule | `.okf/agents/xcode-claude.md` exists | ☐ |
| A3 | Operator brief | `docs/okf-ways-of-working-brief.md` exists | ☐ |
| A4 | Dispatch script (if dispatch enabled) | `scripts/okf-dispatch` executable | ☐ |
| A5 | Dispatch directories | `.okf/dispatch/{ready,running,done,failed,pipelines}/` | ☐ |
| A6 | Orchestration doc | `docs/okf-dispatch-orchestration.md` | ☐ |
| A7 | Step 3 handoff | Latest `.okf/handoffs/*` from Claude Code | ☐ |

## B. Agent rule state (expected before live Xcode)

| # | Check | Expected | Pass |
|---|-------|----------|------|
| B1 | Agent status | `status: draft` (until live verification) | ☐ |
| B2 | Verification | `verification_status: unverified` (until live evidence) | ☐ |
| B3 | Applies to | `applies_to` includes `xcode-claude` | ☐ |
| B4 | Live risk documented | `.okf/risks/xcode-live-verification-pending.md` read or present | ☐ |

## C. Dispatch runner support

| # | Check | Command | Pass |
|---|-------|---------|------|
| C1 | `xcode-claude` in RUNNERS | `scripts/okf-dispatch` accepts `--runner xcode-claude` | ☐ |
| C2 | Pipeline init with xcode-claude | See command block below | ☐ |
| C3 | Packet JSON valid | `runner` field is `xcode-claude`; `context.okf_paths` populated | ☐ |
| C4 | Consume moves to running | `scripts/okf-dispatch consume --runner xcode-claude --json` | ☐ |

**C2 — dry-run command (use a test pipeline id; clean up after):**

```bash
scripts/okf-dispatch init-pipeline "Xcode step 4 dry verification" \
  --pipeline-id xcode-dry-verify-test \
  --runners builder:xcode-claude,tester:claude,reviewer:cursor,integrator:codex \
  --okf .okf/agents/xcode-claude.md docs/create-new-okf-project-in-xcode.md
```

**Cleanup after C2–C4:**

```bash
scripts/okf-dispatch fail --packet-id <id> --reason "dry-run cleanup"
rm -f .okf/dispatch/failed/*<id>* .okf/dispatch/pipelines/xcode-dry-verify-test.json
```

## D. Validation

| # | Check | Command | Pass |
|---|-------|---------|------|
| D1 | OKF validate | `scripts/okf-validate` → 0 warnings | ☐ |
| D2 | Adapter check | `scripts/okf-check-adapters` → no drift | ☐ |

## E. Explicit negatives

Confirm each:

- [ ] Dry verification does **not** promote `.okf/agents/xcode-claude.md` to `active`
- [ ] Dry verification does **not** claim live build/test passed
- [ ] No signing secrets or provisioning profiles stored in OKF
- [ ] Perplexity step 5 not configured during step 4 dry checks

# Verdict

**DRY VERIFICATION:** PASS | PARTIAL | FAIL

| Verdict | Meaning |
|---------|---------|
| **PASS** | A1–A6, B1–B4, C1–C4, D1–D2, all negatives confirmed |
| **PARTIAL** | Core files present; dispatch or validate gap documented |
| **FAIL** | Missing agent rule, guide, or `xcode-claude` not supported in dispatch |

Record results in `.okf/tests/YYYY-MM-DD-xcode-step4-dry-verification.md` and append one line to `.okf/log.md`.

# After dry PASS (live verification still required)

1. Build and test on real Apple target
2. Record evidence in `.okf/tests/` or handoff
3. Promote `.okf/agents/xcode-claude.md` only after live evidence
4. Resolve or close `.okf/risks/xcode-live-verification-pending.md`
