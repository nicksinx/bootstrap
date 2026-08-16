# Operator guides (bootstrap)

Curated operator documentation for standing up OKF + Forge v2 products.

| Document | Use |
|----------|-----|
| [new-okf-forge-project-standup.md](new-okf-forge-project-standup.md) | **Canonical** cheat sheet — edit here first |
| [new-okf-forge-project-standup-offline.md](new-okf-forge-project-standup-offline.md) | **Offline export** — copy into Apple Notes, Obsidian, etc. |
| [install-bootstrap-okf-forge-skill.md](install-bootstrap-okf-forge-skill.md) | Cursor skill install (personal vs repo) |
| [install-cursor-rules.md](install-cursor-rules.md) | Repair rules on pre-v2 products only |
| [okf-readonly-mcp.md](okf-readonly-mcp.md) | Configure and audit the local read-only OKF query pilot |
| [okf-attested-computation-experiment.md](okf-attested-computation-experiment.md) | Run deterministic local receipt/verdict checks |
| [openwiki-okf-sidecar.md](openwiki-okf-sidecar.md) | Enable generated wiki output without allowing `.okf` writes |

**Workflow:** express CLI (`project-intake quick`) or guided agent (`bootstrap-okf-forge-project` skill).

**After standup:** open product as workspace → reload Cursor → `scripts/operator-ready-check.sh`.

When the canonical guide changes, refresh the offline export in the same commit.
