---
name: claude-okf-operator
description: Operate as Claude Code in OKF + Forge v2 projects — tester dispatch role and validation evidence. Use when Claude runs tests, reviews dispatch packets as tester, or completes tester-phase work. Does not wire Forge lifecycle MCPs (Cursor hosts Forge).
applies_to: [claude]
canonical_skills: [okf-reader, okf-handoff-writer]
---

# Claude Code OKF Operator

Claude Code is **service 3** in the five-service order. Default dispatch role: **tester**.

## Layer boundaries (v2)

| Job | Use | Do not use |
|-----|-----|------------|
| Test / verify implementation | `scripts/okf-dispatch` as tester | Forge lifecycle MCP tools |
| Lifecycle planning | Read promoted OKF only | Direct Forge workspace writes |
| Repo apply | Produce evidence; integrator merges | Auto-set `verification_status: accepted` on Forge decisions |

Forge MCP runs in **Cursor only**. Claude consumes tester packets and records evidence.

## Before substantive work

1. Run `skills/okf-reader/SKILL.md`.
2. Read latest handoff from builder (`.okf/handoffs/` or dispatch packet context).
3. Check `.okf/dispatch/ready/` for `tester` role packets.

## Dispatch (tester)

```bash
scripts/okf-dispatch status
scripts/okf-dispatch consume --role tester
# after validation:
scripts/okf-dispatch complete --role tester --evidence <path>
scripts/okf-dispatch advance --from claude   # explicit — no Stop hook
```

Claude has **no automatic Stop hook**. Advance dispatch explicitly during the session.

## Evidence

- Capture test output paths under `runs/` or `.okf/tests/` as project conventions dictate.
- Link evidence to OKF concepts and dispatch `packet_id` in handoffs.
- Run `scripts/okf-validate` when adding or editing OKF test evidence concepts.

## After work

1. Hand off to reviewer (Cursor) via dispatch or `.okf/handoffs/TEMPLATE-tester.md`.
2. Append `.okf/log.md` when OKF changed.

## References

- `docs/create-new-okf-project-in-claude.md`
- `docs/okf-dispatch-orchestration.md`
- `.claude/commands/okf-sync.md`
- `CLAUDE.md` (thin adapter)
