---
name: xcode-okf-operator
description: Operate as Xcode-connected Claude Agent in OKF + Forge v2 projects — Apple-platform dispatch consumer and integrator. Use when Xcode builds, tests, or completes platform-specific dispatch work. Does not wire Forge lifecycle MCPs (Cursor hosts Forge).
applies_to: [xcode-claude]
canonical_skills: [okf-reader, okf-handoff-writer]
---

# Xcode OKF Operator

Xcode-connected Claude Agent is **service 4** in the five-service order. Dispatch runner: **`xcode-claude`** (often integrator or platform-specific builder).

## Layer boundaries (v2)

| Job | Use | Do not use |
|-----|-----|------------|
| Apple-platform build/test/dispatch | `.okf/dispatch/` packets, `.okf/agents/xcode-claude.md` | Forge lifecycle MCP tools |
| Lifecycle / release planning | Promoted OKF + handoffs from Cursor | Forge MCP from Xcode session |
| Signing secrets | Keychain / local only | `.okf/` or committed files |

Forge MCP runs in **Cursor only**.

## Before substantive work

1. Read `.okf/agents/xcode-claude.md` and `skills/okf-reader/SKILL.md`.
2. Read Claude Code handoff (step 3 complete).
3. Check dispatch packets for `xcode-claude` or integrator role if mapped.

## Dispatch

Consume typed JSON from `.okf/dispatch/ready/`. Complete with `scripts/okf-dispatch` flags documented in `docs/okf-dispatch-orchestration.md`.

Do not call other agents directly. Update OKF risks for signing, simulator, or platform blockers.

## Verification

- Follow `.okf/prompts/xcode-step4-verification-checklist.md` for setup claims.
- Record evidence in `.okf/tests/` (command summary, PASS/FAIL).
- Run `scripts/okf-validate` before claiming step 4 complete.

## Handoff

Write handoff for **Perplexity service 5** using `.okf/handoffs/TEMPLATE-xcode-step4.md` when applicable.

## References

- `docs/create-new-okf-project-in-xcode.md`
- `.okf/workflows/multi-agent-delivery-pipeline.md`
