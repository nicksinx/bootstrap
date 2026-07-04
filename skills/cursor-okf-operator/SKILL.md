---
name: cursor-okf-operator
description: Operate as Cursor in OKF + Forge v2 projects — reviewer dispatch role, Forge MCP lifecycle host, and OKF promotion integrator. Use when Cursor reviews work, runs Forge stage tools, promotes Forge artifacts to OKF, or consumes reviewer dispatch packets.
applies_to: [cursor]
canonical_skills: [okf-reader, okf-handoff-writer, okf-concept-writer]
---

# Cursor OKF Operator

Cursor is **service 1** in the five-service order. Default dispatch role: **reviewer**. **Forge MCP control plane** for lifecycle planning.

## Layer boundaries (v2)

| Job | Use | Do not use |
|-----|-----|------------|
| Lifecycle planning (Concept→Sunset) | Forge MCP via `.cursor/mcp.json` | `scripts/okf-dispatch` for planning |
| Code delivery review | Dispatch `reviewer` role | Forge stage tools for implementation |
| Promote Forge → OKF | Integrator-reviewed concepts + checklists | Auto `verification_status: accepted` |
| Cross-tool resume | ForgeRelay MCP | Dispatch role order |

Rules: `.cursor/rules/okf-ecosystem-routing.mdc`, `okf-forge-operator.mdc`, `okf-dispatch.mdc`, `okf-forge-promotion.mdc`.

## Before Forge MCP calls

1. `skills/okf-reader/SKILL.md`
2. `.okf/workflows/okf-forge-lifecycle-bridge.md`
3. Sibling Forge repos built; reload MCP after config changes.

## Dispatch (reviewer)

```bash
scripts/okf-dispatch consume --role reviewer
scripts/okf-dispatch complete --role reviewer
```

Advance explicitly when acting as reviewer (Cursor has no Codex-style Stop hook unless project adds one).

## Promotion (integrator hat)

When promoting Forge workspace output to OKF:

1. Server-specific checklist under `.okf/workflows/forge-*-promotion-checklist.md`
2. Lineage fields + decision 0004 receipt rules
3. `scripts/okf-validate` after edits

## References

- `docs/create-new-okf-project-in-cursor.md`
- `docs/forge-lifecycle-integration.md`
- `docs/install-cursor-rules.md`
- `.cursor/rules/okf.mdc`
