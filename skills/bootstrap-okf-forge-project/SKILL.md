---
name: bootstrap-okf-forge-project
description: >-
  Guide operators through standardized intake and launch of a new OKF + Forge
  integrated product using the bootstrap toolkit. Collects project configuration
  into project-intake.yaml, validates it, and runs scripts/project-intake to
  launch the scaffold. Use when starting a new product, standing up a project,
  bootstrap launch, OKF Forge project setup, or project intake.
---

# Bootstrap OKF + Forge Project

Use this skill in the **bootstrap repository** (or with `bootstrap_root` pointing at it) to stand up a new integrated OKF + Forge product with standardized configuration.

Canonical scripts:

```bash
scripts/project-intake init|validate|render|apply
```

Field reference: [references/intake-fields.md](references/intake-fields.md)  
Example intake: [references/intake-example.yaml](references/intake-example.yaml)  
**User copy-paste prompt:** [references/user-intake-prompt.md](references/user-intake-prompt.md)

## When to use

- User wants a **new OKF + Forge product** (not the bootstrap toolkit repo itself).
- User asks to "stand up", "bootstrap", or "scaffold" a project with dispatch and Forge MCP.
- User needs a **repeatable intake** instead of ad-hoc `launch_project.sh` flags.

Do **not** use for Project-1 harness work (use `integration-harness` Cursor rule) or legacy ai-task-only products unless operator explicitly chooses `legacy-task` profile.

## Agent workflow

### 1. Confirm context

- Working directory is bootstrap repo OR `paths.bootstrap_root` is set in intake.
- Target path does not contain unrelated production code unless user confirms `--force` on launch.

### 2. Collect intake (interactive)

Use **AskQuestion** (or structured chat) for **required** phases only. Apply v2 defaults for profile, services, Forge, and dispatch unless the user opts out.

**Phase A — Identity (required)**

| Field | Question |
|-------|----------|
| `project.id` | Project id (lowercase-dashes, 3–64 chars)? |
| `project.display_name` | Human display name? |
| `project.purpose` | One paragraph — why does this product exist? |
| `project.owner` | Team or person owning the OKF bundle? |

Optional in same phase: `scope_summary`, `out_of_scope`.

**Phase B — Paths (required)**

| Field | Question |
|-------|----------|
| `paths.target_dir` | Absolute path for the new repo? (basename **must** equal `project.id`) |

`paths.forge_siblings_parent` defaults to parent of `target_dir`.

**Phase D — GitHub (required)**

| Field | Question |
|-------|----------|
| `github.enabled` | Create GitHub repo with `gh`? |
| `github.owner` | Org or user (prefill from `gh api user` when available)? |
| `github.visibility` | `private` or `public`? |

**Optional overrides** — ask only when the user deviates:

| Phase | Defaults |
|-------|----------|
| C — Profile | `default` (v2). `legacy-task` only on request. `forge-lifecycle` = alias of `default`. |
| E — OKF services | cursor, codex, claude, perplexity on; xcode off. Advisory for setup guides only. |
| F — Forge | enabled, clone siblings yes, build siblings no, org `nicksinx`. |
| G — Dispatch | builder→codex, tester→claude, reviewer→cursor, integrator→codex. |

**Express alternative:** `scripts/project-intake quick` with `--project-id`, `--target-dir`, `--purpose`, `--owner`.

### 3. Write and validate intake

```bash
# Option A — agent writes YAML directly to a path, e.g.:
#   bootstrap/intake/<project-id>.yaml

scripts/project-intake validate intake/<project-id>.yaml
scripts/project-intake render intake/<project-id>.yaml
```

Or seed then edit:

```bash
scripts/project-intake init \
  --project-id <id> \
  --target-dir <abs-path> \
  -o intake/<id>.yaml
```

Set `collected_at` (ISO UTC), `collected_by` (agent/session id), then fill `purpose`, GitHub, and service flags.

### 4. User approval gate

Show `render` output (launch commands + checklist). **Do not** run `--execute` until the user confirms:

- project id and target path
- GitHub owner/visibility (if enabled)
- Forge clone/build plan

### 5. Apply

```bash
# Safe check — launch dry-run only
scripts/project-intake apply intake/<project-id>.yaml

# Full standup
scripts/project-intake apply intake/<project-id>.yaml --execute
```

`--execute` runs: `launch_project.sh` → copy `skills/` → patch `.okf/project.md` → `okf-sync-skills` → validation → optional `forge-clone-siblings` → operator handoff.

Skills and **Cursor rules** are included automatically on v2 `default` launch. No manual `rsync` or rules install.

### 6. Post-standup instructions (tell the user)

1. Open **target_dir** as the Cursor workspace root.
2. Reload Cursor window (MCP + project rules).
3. Run `scripts/operator-ready-check.sh`.
4. Read `.okf/handoffs/*-operator-standup.md` and `docs/okf-service-operator-skills.md`.
5. Follow `docs/create-new-okf-project-in-*.md` for **enabled services you will configure first**.
6. Read `docs/okf-ways-of-working-brief.md` and `.okf/workflows/okf-forge-lifecycle-bridge.md` when starting Forge work.

**Troubleshooting:** pre-v2 scaffolds missing rules — bootstrap `docs/install-cursor-rules.md` section B.

## Quick non-interactive path

When the user already has a filled intake file:

```bash
scripts/project-intake validate path/to/intake.yaml
scripts/project-intake apply path/to/intake.yaml --execute
```

## Validation failures (common)

| Error | Fix |
|-------|-----|
| basename ≠ project.id | Rename folder or change id |
| github.enabled without owner | Set `github.owner` |
| `okf-validate` fails after launch | Fix OKF frontmatter; re-run validate |

## Relationship to other skills

| Skill | Role |
|-------|------|
| `create-new-okf-project` | OKF-only scaffold inside an existing folder (no bootstrap launcher) |
| **this skill** | Full bootstrap v2 product via `launch_project.sh` + Forge + intake record |

## Additional resources

- [user-intake-prompt.md](references/user-intake-prompt.md) — copy-paste prompt for operators
- [intake-fields.md](references/intake-fields.md)
- [intake-example.yaml](references/intake-example.yaml)
- `docs/new-okf-forge-project-standup.md` — operator cheat sheet
- `docs/install-cursor-rules.md` — pre-v2 rule repair only
- `docs/migration-from-legacy-bootstrap.md`
