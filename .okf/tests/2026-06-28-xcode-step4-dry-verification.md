---
type: Test Evidence
title: Xcode Step 4 Dry Verification
description: Repo-only Wave 3 evidence for xcode-claude dispatch runner and step-4 file presence without live Xcode.
status: active
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/tests/2026-06-28-xcode-step4-dry-verification.md
tags: [okf, test-evidence, xcode, step-4, dry-verification, dispatch]
applies_to: [cursor, claude, codex, xcode-claude, local-agent]
sensitivity: internal
verification_status: tested
timestamp: 2026-06-28T16:00:00+02:00
---

# Test Objective

Confirm OKF service 4 readiness from the repository without live Xcode build/test — file presence, agent rule state, dispatch `xcode-claude` runner, and validation.

Checklist: `.okf/prompts/xcode-step4-verification-checklist.md`

# Scope

**In scope:** docs, agent rule, dispatch JSON, validate, adapter-check.

**Out of scope:** simulator, signing, `xcodebuild`, promoting agent rule to `active`.

# Section A — File presence

| Check | Result |
|-------|--------|
| A1 `docs/create-new-okf-project-in-xcode.md` | PASS — expanded step-4 guide present |
| A2 `.okf/agents/xcode-claude.md` | PASS — `status: draft`, `verification_status: unverified` |
| A3 `docs/okf-ways-of-working-brief.md` | PASS |
| A4 `scripts/okf-dispatch` | PASS — executable |
| A5 dispatch directories | PASS — `{ready,running,done,failed,pipelines}/` |
| A6 `docs/okf-dispatch-orchestration.md` | PASS |
| A7 step 3 handoff | PASS — `.okf/handoffs/2026-06-28-scaffold-parity.md` (prior continuity) |

# Section B — Agent rule state

| Check | Result |
|-------|--------|
| B1 status draft | PASS |
| B2 verification unverified | PASS |
| B3 applies_to xcode-claude | PASS |
| B4 live risk documented | PASS — `.okf/risks/xcode-live-verification-pending.md` |

# Section C — Dispatch dry-run

Commands run:

```bash
cd /Users/dv/Projects/testrunner/Project-1

scripts/okf-dispatch init-pipeline "Xcode step 4 dry-run verification" \
  --pipeline-id xcode-dry-20260628 \
  --runners builder:xcode-claude,tester:claude,reviewer:cursor,integrator:codex \
  --okf .okf/agents/xcode-claude.md docs/create-new-okf-project-in-xcode.md

scripts/okf-dispatch consume --runner xcode-claude --json
```

Results:

| Check | Result |
|-------|--------|
| C1 xcode-claude runner accepted | PASS |
| C2 pipeline init | PASS — `pipeline_id=xcode-dry-20260628`, `packet_id=builder-01c24942` |
| C3 packet JSON | PASS — `runner: xcode-claude`, `role: builder`, `context.okf_paths` includes agent rule + xcode guide |
| C4 consume → running | PASS — packet moved to `.okf/dispatch/running/` |

Sample packet fields verified:

```json
{
  "runner": "xcode-claude",
  "role": "builder",
  "pipeline_id": "xcode-dry-20260628",
  "context": {
    "okf_paths": [
      ".okf/agents/xcode-claude.md",
      "docs/create-new-okf-project-in-xcode.md"
    ]
  }
}
```

Test artifacts removed after capture (`failed/` packet and `pipelines/xcode-dry-20260628.json`).

# Section D — Validation

```bash
scripts/okf-validate          # 0 warnings
scripts/okf-check-adapters    # pass, 13 skills
```

# Section E — Negatives

- Agent rule **not** promoted to `active` — confirmed
- No live build/test claimed — confirmed
- No secrets in OKF — confirmed
- Perplexity step 5 not configured during test — confirmed

# Verdict

**DRY VERIFICATION: PASS**

Live Xcode verification remains pending per `.okf/risks/xcode-live-verification-pending.md`.

# Follow-Up

- User: live build/test on real Apple target when ready (e.g. ProcureLex)
- Promote `.okf/agents/xcode-claude.md` only after live evidence
- Wave 2 dispatch ergonomics (tester/reviewer templates) — independent
