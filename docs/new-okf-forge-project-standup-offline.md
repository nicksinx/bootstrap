# New OKF + Forge project standup (offline export)

**Purpose:** Self-contained copy for notes apps (Apple Notes, Obsidian, Bear, etc.).  
**Canonical source (edit there first):** `bootstrap/docs/new-okf-forge-project-standup.md`  
**Last synced with canonical:** 2026-07-04  
**Bootstrap profile:** `default` v2.0.0

---

## Prerequisites

- Bootstrap repo cloned locally (`/path/to/bootstrap`)
- Cursor (agent-guided standup or post-standup Forge work)
- `gh auth status` if creating GitHub repos
- Python: PyYAML + jsonschema (same as `make check` in bootstrap)

---

## One-time Cursor skill setup

### Repeat operators (recommended)

```bash
mkdir -p ~/.cursor/skills
cp -R /path/to/bootstrap/skills/bootstrap-okf-forge-project ~/.cursor/skills/
```

### Bootstrap repo only (if skill not indexed)

```bash
cd /path/to/bootstrap
mkdir -p .cursor/skills
ln -sf ../../skills/bootstrap-okf-forge-project .cursor/skills/bootstrap-okf-forge-project
```

---

## Express standup (CLI — default path)

```bash
cd /path/to/bootstrap
chmod +x scripts/project-intake

scripts/project-intake quick \
  --project-id my-product \
  --target-dir "$HOME/projects/my-product" \
  --purpose "One paragraph: why this product exists." \
  --owner platform-team

# Optional: --no-github  |  --github-owner my-org  |  --github-visibility public

scripts/project-intake validate intake/my-product.yaml
scripts/project-intake render intake/my-product.yaml
scripts/project-intake apply intake/my-product.yaml              # launch dry-run
scripts/project-intake apply intake/my-product.yaml --execute    # after you approve
```

Edit YAML before `apply` only for non-defaults (legacy profile, disable a service, Forge build-now, dispatch overrides).

### What `--execute` runs automatically

1. `launch_project.sh` — OKF, Forge launchers, dispatch, Cursor rules, docs
2. Copy `skills/` (excludes bootstrap-only `bootstrap-okf-forge-project`)
3. Patch `.okf/project.md` from intake
4. `scripts/okf-sync-skills`
5. `scripts/validate_launch.sh` + `scripts/okf-validate`
6. `scripts/forge-clone-siblings.sh` when Forge enabled
7. `.okf/project-intake.yaml` + `.okf/handoffs/YYYY-MM-DD-operator-standup.md`

No manual skill `rsync`. No separate Cursor rules install on v2 `default` launch.

---

## Guided standup (Cursor Agent)

Invoke in bootstrap repo:

```text
Use the bootstrap-okf-forge-project skill to stand up a new OKF + Forge project.
```

### Short agent prompt (recommended)

```text
Use bootstrap-okf-forge-project skill. Collect identity (id, name, purpose, owner), paths (target_dir), and GitHub (create repo? owner, visibility). Apply v2 defaults for profile, services, Forge, and dispatch unless I opt out. Write intake/<id>.yaml, validate, render plan, wait for my "approve standup" before apply --execute.
```

### Full agent prompt

```text
BOOTSTRAP OKF + FORGE PROJECT SETUP — guided intake

Use the bootstrap-okf-forge-project skill (skills/bootstrap-okf-forge-project/SKILL.md).

Collect required setup information, write intake/<project-id>.yaml, validate with scripts/project-intake, show the rendered launch plan, and only run scripts/project-intake apply … --execute after I explicitly approve.

Rules:
- Ask questions one phase at a time.
- project.id = lowercase-dashes, 3–64 chars; basename of paths.target_dir must match.
- Default profile: default (v2). legacy-task only on request.
- Apply v2 defaults for services, Forge, dispatch unless I opt out.
- okf.services booleans are advisory only (setup guides), not scaffold toggles.
- Wait for "approve standup" before --execute.
- After apply: .okf/handoffs/*-operator-standup.md and scripts/operator-ready-check.sh.

Required phases:
A — Identity: id, display name, purpose, owner
B — Paths: absolute target_dir (siblings parent = parent of target by default)
D — GitHub: create with gh? owner, visibility (prefill owner from gh api user)

Optional (only if I deviate):
C — Profile: default | legacy-task
E — Services: cursor, codex, claude, perplexity on; xcode off
F — Forge: enabled, clone yes, build no, org nicksinx
G — Dispatch: builder→codex, tester→claude, reviewer→cursor, integrator→codex

Start with Phase A.
```

---

## Intake phases (summary)

| Phase | Required? | Collect |
|-------|-----------|---------|
| A Identity | Yes | id, name, purpose, owner |
| B Paths | Yes | target_dir (basename = id) |
| D GitHub | Yes | create? owner, visibility |
| C Profile | If non-default | default (v2) |
| E Services | If deviating | all on except xcode off |
| F Forge | If deviating | clone yes, build no |
| G Dispatch | If deviating | codex/claude/cursor/codex |

---

## After standup

1. Open **product folder** as Cursor workspace root (not bootstrap).
2. Reload Cursor window (MCP + rules).
3. Run `scripts/operator-ready-check.sh`.
4. Read `.okf/handoffs/*-operator-standup.md` and `docs/okf-service-operator-skills.md`.
5. Service guides for enabled services you configure first (`docs/create-new-okf-project-in-cursor.md`, etc.).
6. Forge siblings — skip if apply already cloned.

Do **not** re-run `okf-sync-skills` or install rules unless something looks stale.

---

## Cursor rules (v2 products)

Included automatically on `default` profile launch. Verify:

```bash
ls .cursor/rules/
# okf.mdc  okf-ecosystem-routing.mdc  okf-forge-operator.mdc
# okf-dispatch.mdc  okf-forge-promotion.mdc  okf-legacy-aitask.mdc

ls skills/*-okf-operator/
```

| Rule | Always on? | Purpose |
|------|------------|---------|
| okf.mdc | Yes | OKF context + skill index |
| okf-ecosystem-routing.mdc | Yes | Forge MCP vs dispatch vs ForgeRelay |
| okf-forge-operator.mdc | Scoped | Forge launchers, .okf/forge/, MCP |
| okf-dispatch.mdc | Scoped | Dispatch queues, okf-dispatch |
| okf-forge-promotion.mdc | Scoped | Forge → OKF promotion (Option C) |
| okf-legacy-aitask.mdc | Scoped | Legacy scripts/mcp, scripts/workers |

Sanity check in Agent chat: “Which layer for lifecycle planning vs code delivery?” → Forge MCP vs okf-dispatch.

**Pre-v2 repair:** bootstrap `docs/install-cursor-rules.md` section B (bootstrap repo only).

---

## Design choices

| Choice | Rationale |
|--------|-----------|
| intake/*.yaml | Single config artifact |
| Skill = interview | Script = validation + execution |
| create-new-okf-project | OKF-only in existing folder |
| bootstrap-okf-forge-project | Full v2 product + Forge + dispatch |
| legacy-task | Deprecated ai-task MCP |

---

## CLI without agent (full init)

```bash
scripts/project-intake init \
  --project-id my-product \
  --target-dir "$HOME/projects/my-product" \
  -o intake/my-product.yaml
# edit purpose, GitHub, flags
scripts/project-intake validate intake/my-product.yaml
scripts/project-intake apply intake/my-product.yaml --execute
```

---

## Troubleshooting

- Missing rules on old scaffolds: bootstrap docs/install-cursor-rules.md section B
- Stale adapters: scripts/okf-sync-skills && scripts/okf-validate
- github.enabled without owner: set github.owner in intake YAML before apply

---

*End of offline export. Sync from bootstrap/docs/new-okf-forge-project-standup.md when the workflow changes.*
