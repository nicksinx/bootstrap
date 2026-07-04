---
name: codex-okf-operator
description: Operate as Codex in OKF + Forge v2 projects — builder/integrator dispatch, hooks, and OKF promotion. Use when Codex implements or integrates work, runs okf-dispatch, advances pipelines from Stop hooks, or ingests handoffs. Does not wire Forge lifecycle MCPs (Cursor hosts Forge).
applies_to: [codex]
canonical_skills: [okf-reader, okf-handoff-writer, okf-concept-writer]
---

# Codex OKF Operator

Codex is **service 2** in the five-service order. Default dispatch roles: **builder** and **integrator**.

## Layer boundaries (v2)

| Job | Use | Do not use |
|-----|-----|------------|
| Implementation / integration | `scripts/okf-dispatch`, OKF skills | Forge lifecycle MCP tools |
| Lifecycle planning | Read **promoted** OKF from Cursor integrator | `scripts/mcp/*`, `scripts/workers/*` (legacy) |
| External research | Wait for Perplexity → `.okf/references/` | Forge MCP as research substitute |

Forge MCP runs in **Cursor only**. Codex reads `.okf/` and executes dispatch.

## Before substantive work

1. Run `skills/okf-reader/SKILL.md` (or read `.okf/index.md`, `.okf/project.md`, recent handoffs).
2. Check `.okf/dispatch/ready/` for `builder` or `integrator` packets if dispatch is enabled.
3. Confirm task traces to OKF requirement, decision, or handoff.

## Dispatch (builder / integrator)

```bash
scripts/okf-dispatch status
scripts/okf-dispatch consume --role builder   # or integrator
# after work:
scripts/okf-dispatch complete --role builder --evidence <path>
```

- `.codex/hooks.json` may call `scripts/okf-dispatch advance --from codex` on Stop.
- Never invoke Claude, Cursor, or Xcode directly — file-queue only (decision 0003).

## After substantive changes

1. Update affected OKF concepts; append `.okf/log.md`.
2. Run `scripts/okf-validate` when OKF concepts changed.
3. Handoff to next role or `.okf/handoffs/` if pausing.

## Canonical skills

Use shared skills for delivery work: `okf-concept-writer`, `okf-handoff-writer`, `okf-context-pack-builder`, `okf-risk-scanner`, etc.

## References

- `docs/okf-dispatch-orchestration.md`
- `docs/create-new-okf-project-in-codex.md`
- `.okf/workflows/multi-agent-delivery-pipeline.md`
- `AGENTS.md` (thin adapter — regenerate with `scripts/okf-sync-skills`)
