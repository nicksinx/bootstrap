# New OKF + Forge project standup

> **Canonical operator guide** (bootstrap repo).  
> Offline self-contained copy for notes apps: `docs/new-okf-forge-project-standup-offline.md`  
> Index: `docs/operator-guides.md`

Operator cheat sheet for bootstrap v2 products: OKF bundle, Forge MCP launchers, OKF dispatch, service operator skills, and Cursor rules — all from one intake file.

**Heavy lifting:** `scripts/project-intake`  
**Guided agent skill:** `skills/bootstrap-okf-forge-project/SKILL.md`  
**Copy-paste agent prompt:** `skills/bootstrap-okf-forge-project/references/user-intake-prompt.md`

---

## Prerequisites

- Bootstrap repo cloned locally
- Cursor (for agent-guided standup or post-standup Forge work)
- `gh` authenticated if you want GitHub repo creation (`gh auth status`)
- Python deps for bootstrap (`PyYAML`, `jsonschema` — same as `make check`)

---

## One-time Cursor skill setup

### Repeat operators (recommended)

Install the intake skill once for all workspaces:

```bash
mkdir -p ~/.cursor/skills
cp -R /path/to/bootstrap/skills/bootstrap-okf-forge-project ~/.cursor/skills/
```

Edit `~/.cursor/skills/bootstrap-okf-forge-project/SKILL.md` only if your bootstrap clone path differs from what agents infer.

### Bootstrap-repo-only

Open bootstrap in Cursor. Most builds index `skills/*/SKILL.md` automatically.

If the skill is not discovered:

```bash
cd /path/to/bootstrap
mkdir -p .cursor/skills
ln -sf ../../skills/bootstrap-okf-forge-project .cursor/skills/bootstrap-okf-forge-project
```

---

## Express standup (CLI — default path)

Minimal fields; everything else uses v2 defaults (profile `default`, dispatch runners, Forge clone without build, skills copy, validation).

```bash
cd /path/to/bootstrap
chmod +x scripts/project-intake

# Writes intake/<id>.yaml with purpose + GitHub owner prefilled when gh is logged in
scripts/project-intake quick \
  --project-id my-product \
  --target-dir "$HOME/projects/my-product" \
  --purpose "One paragraph: why this product exists." \
  --owner platform-team

# Optional: --no-github  or  --github-owner my-org  --github-visibility public

scripts/project-intake validate intake/my-product.yaml
scripts/project-intake render intake/my-product.yaml
scripts/project-intake apply intake/my-product.yaml              # launch dry-run
scripts/project-intake apply intake/my-product.yaml --execute    # full standup (after you approve)
```

Edit the YAML before `apply` only if you need non-defaults (disable a service, `legacy-task` profile, Forge build-now, dispatch overrides).

### What `--execute` runs automatically

1. `launch_project.sh` — full v2 scaffold (OKF, Forge launchers, dispatch, **Cursor rules**, docs)
2. Copy `skills/` into the product (excludes bootstrap-only `bootstrap-okf-forge-project`)
3. Patch `.okf/project.md` from intake
4. `scripts/okf-sync-skills` — refresh thin adapters (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules/okf.mdc`, …)
5. `scripts/validate_launch.sh` + `scripts/okf-validate`
6. `scripts/forge-clone-siblings.sh` when Forge enabled (default)
7. Write `.okf/project-intake.yaml` and `.okf/handoffs/YYYY-MM-DD-operator-standup.md`

No manual `rsync` of skills. No separate Cursor rules install on v2 `default` launch.

---

## Guided standup (Cursor Agent)

From the bootstrap repo, invoke:

```text
Use the bootstrap-okf-forge-project skill to stand up a new OKF + Forge project.
```

Or paste the full prompt from `skills/bootstrap-okf-forge-project/references/user-intake-prompt.md`.

The agent collects **three required phases** (identity, paths, GitHub), applies v2 defaults for everything else, writes `intake/<project-id>.yaml`, shows `render` output, and only runs `--execute` after you reply **approve standup**.

---

## Design choices

| Choice | Rationale |
|--------|-----------|
| Intake YAML | Single standardized config artifact (not scattered CLI flags) |
| Skill = interview + policy | Script = validation + execution |
| `create-new-okf-project` | OKF-only scaffold inside an existing folder — no bootstrap launcher |
| **This skill / `project-intake`** | Full bootstrap v2 product with Forge + dispatch |
| `legacy-task` profile | Deprecated ai-task MCP; mention only on explicit request |
| `okf.services` booleans | Advisory for operator handoff — which setup guides to follow; scaffold unchanged |

---

## After standup (operator)

1. **Open the product folder** as the Cursor workspace root (not bootstrap, not a monorepo parent).
2. **Reload the Cursor window** so MCP and project rules load.
3. **Run** `scripts/operator-ready-check.sh` (rules, skills, validation in one pass).
4. **Read** `.okf/handoffs/*-operator-standup.md` and `docs/okf-service-operator-skills.md`.
5. **Service setup guides** — only for services you will configure first (usually `docs/create-new-okf-project-in-cursor.md`, then codex/claude).
6. **Forge siblings** — skip if `apply` already ran `forge-clone-siblings.sh`. Optional slow step: build siblings (`npm ci && npm run build` per repo) when you need MCP servers immediately.

You do **not** need to run `okf-sync-skills` or install Cursor rules unless something looks stale or missing.

---

## Post-standup verification (rules + skills)

```bash
cd /path/to/my-product
scripts/operator-ready-check.sh
```

Manual spot-check:

```bash
ls .cursor/rules/
# okf.mdc  okf-ecosystem-routing.mdc  okf-forge-operator.mdc
# okf-dispatch.mdc  okf-forge-promotion.mdc  okf-legacy-aitask.mdc

ls skills/*-okf-operator/
# codex-okf-operator  claude-okf-operator  cursor-okf-operator  xcode-okf-operator
```

In Cursor **Settings → Rules**, confirm project rules are listed. Sanity check in Agent chat: *“Which layer for lifecycle planning vs code delivery?”* — should cite Forge MCP vs `okf-dispatch` per `okf-ecosystem-routing.mdc`.

### Troubleshooting (pre-v2 or broken scaffold)

- Missing rules: [install-cursor-rules.md](install-cursor-rules.md) section B (bootstrap kit only — not copied into products by design).
- Stale adapters: `scripts/okf-sync-skills` then `scripts/okf-validate`.

---

## Intake phases (guided agent)

| Phase | Required? | Collect |
|-------|-----------|---------|
| **A — Identity** | Yes | id, display name, purpose, owner |
| **B — Paths** | Yes | absolute `target_dir` (basename = id); siblings parent defaults to parent of target |
| **D — GitHub** | Yes | create with `gh`? owner, visibility |
| **C — Profile** | Only if non-default | `default` (v2). `legacy-task` only on request |
| **E — OKF services** | Only if deviating | Defaults: cursor, codex, claude, perplexity on; xcode off |
| **F — Forge** | Only if deviating | Defaults: enabled, clone siblings, no build-now |
| **G — Dispatch** | Only if deviating | Defaults: builder→codex, tester→claude, reviewer→cursor, integrator→codex |

---

## Related

- [install-bootstrap-okf-forge-skill.md](install-bootstrap-okf-forge-skill.md) — skill install options
- [install-cursor-rules.md](install-cursor-rules.md) — repair guide for older products
- [migration-from-legacy-bootstrap.md](migration-from-legacy-bootstrap.md)
- [okf-service-operator-skills.md](okf-service-operator-skills.md)
- `schemas/project-intake.schema.json`
