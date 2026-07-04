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

Use **AskQuestion** (or structured chat) for each phase. Record answers in `project-intake.yaml`.

**Phase A — Identity**

| Field | Question |
|-------|----------|
| `project.id` | Project id (lowercase-dashes, 3–64 chars)? |
| `project.display_name` | Human display name? |
| `project.purpose` | One paragraph — why does this product exist? |
| `project.scope_summary` | Initial in-scope bullets or paragraph? |
| `project.out_of_scope` | Explicit exclusions? |
| `project.owner` | Team or person owning the OKF bundle? |

**Phase B — Paths**

| Field | Question |
|-------|----------|
| `paths.target_dir` | Absolute path for the new repo? (basename **must** equal `project.id`) |
| `paths.forge_siblings_parent` | Parent directory for Forge sibling clones? (default: parent of `target_dir`) |

**Phase C — Profile**

| Field | Question |
|-------|----------|
| `profile.name` | `default` (recommended), `forge-lifecycle` (alias), or `legacy-task` (deprecated)? |

**Phase D — GitHub**

| Field | Question |
|-------|----------|
| `github.enabled` | Create GitHub repo with `gh`? |
| `github.owner` | Org or user (required if enabled)? |
| `github.visibility` | `private` or `public`? |

**Phase E — OKF services**

Which services will operators configure? (cursor, codex, claude, xcode, perplexity) — set booleans under `okf.services`.

**Phase F — Forge**

| Field | Question |
|-------|----------|
| `forge.enabled` | Enable Forge MCP integration? (default yes for `default` profile) |
| `forge.clone_siblings` | Clone `nicksinx/*Forge` peers after launch? |
| `forge.build_siblings` | Run `npm ci && npm run build` in each sibling now? (slow) |
| `forge.github_org` | GitHub org for Forge repos (default `nicksinx`)? |

**Phase G — Dispatch**

Confirm or override default runners: builder→codex, tester→claude, reviewer→cursor, integrator→codex.

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

Skills are copied automatically (excluding bootstrap-only `bootstrap-okf-forge-project`). No manual `rsync` required.

### 6. Post-standup instructions (tell the user)

1. Open **target_dir** as the Cursor workspace root.
2. Reload MCP after verifying `.cursor/mcp.json`.
3. Follow `docs/create-new-okf-project-in-*.md` for each enabled service.
4. Read `docs/okf-ways-of-working-brief.md` and `.okf/workflows/okf-forge-lifecycle-bridge.md`.
5. Install Cursor rules if missing — see `docs/install-cursor-rules.md`.

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
- `docs/install-cursor-rules.md`
- `docs/migration-from-legacy-bootstrap.md`
