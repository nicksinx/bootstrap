# OKF service operator skills (v2)

Thin **per-service** skills align Codex, Claude, Xcode, Cursor, and Perplexity with bootstrap v2: OKF dispatch, Forge-on-Cursor-only, and no legacy ai-task path.

## Skill map

| Service | Operator skill | Dispatch role | Forge MCP |
|---------|----------------|---------------|-----------|
| Cursor | `cursor-okf-operator` | reviewer (+ integrator promotion) | **Yes — host** |
| Codex | `codex-okf-operator` | builder, integrator | No — read promoted OKF |
| Claude | `claude-okf-operator` | tester | No |
| Xcode | `xcode-okf-operator` | `xcode-claude` runner | No |
| Perplexity | `perplexity-okf-*` (4 skills) | overflow substitute | **No — by design** |

Shared canonical skills (`okf-reader`, `okf-handoff-writer`, `okf-concept-writer`, …) still apply to all services.

## Install in a product project

Skills are **copied automatically** when you launch via `launch_project.sh` or `project-intake apply --execute`. They land under `skills/` in the product repo (bootstrap-only `bootstrap-okf-forge-project` is excluded).

Manual refresh from bootstrap kit:

```bash
python3 /path/to/bootstrap/scripts/lib/copy_okf_skills.py \
  /path/to/bootstrap /path/to/product

cd /path/to/product
scripts/okf-sync-skills
scripts/okf-validate
```

### Codex

Install operator + canonical skills into Codex home per `CODEX-SKILL-INSTALL.md`. Start sessions with `codex-okf-operator` for dispatch work.

### Claude Code

Reference `skills/claude-okf-operator/SKILL.md` in session; slash command `/okf-sync` runs adapter refresh.

### Cursor

Use `.cursor/rules/*.mdc` for always-on routing; invoke `cursor-okf-operator` skill when doing Forge or reviewer work.

### Xcode

Read `skills/xcode-okf-operator/SKILL.md` alongside `.okf/agents/xcode-claude.md`.

### Perplexity

Attach the four `perplexity-okf-*/SKILL.md` files as Project Skills in Perplexity Desktop.

## Bootstrap-only skills

| Skill | Scope |
|-------|--------|
| `bootstrap-okf-forge-project` | Intake + launch from bootstrap repo only |

Do not copy into product repos.

## Related

- `docs/shared-okf-skills.md`
- `docs/forge-mcp-hosting-policy.md` (if added)
- `.cursor/rules/okf-ecosystem-routing.mdc`
- `docs/migration-from-legacy-bootstrap.md`
