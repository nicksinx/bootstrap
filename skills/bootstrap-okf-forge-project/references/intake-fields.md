# Project intake fields

Schema: `schemas/project-intake.schema.json`

## Required sections

| Section | Purpose |
|---------|---------|
| `project` | Identity — `id` must match `basename(target_dir)` |
| `paths` | `target_dir`, optional `forge_siblings_parent` (defaults to parent of target) |
| `profile` | `default` (v2 OKF + Forge + dispatch) recommended |

## Project id rules

- Lowercase letters, digits, dashes
- 3–64 characters
- Must match regex in `schemas/project.schema.json`

## GitHub block

When `github.enabled: true`, set `github.owner` (org or user). Requires `gh` authenticated locally.

## OKF services block

Records which of the five services the operator plans to configure. Does not auto-install tools; drives handoff and checklist.

| Service | Typical role |
|---------|----------------|
| cursor | IDE, reviewer, Forge MCP host |
| codex | builder, dispatch automation |
| claude | tester |
| xcode | Apple-platform integrator |
| perplexity | cited research + overflow |

## Forge block

| Field | Notes |
|-------|-------|
| `clone_siblings` | Runs `scripts/forge-clone-siblings.sh` post-launch |
| `build_siblings` | Runs `npm ci && npm run build` in each sibling (slow; optional) |
| `trusted_approver_keys_path` | Local path only — never commit keys |

## Dispatch runners

Defaults match Project-1 harness. Override only when operator has a documented reason.

## Post-launch flags

All default `true`. Set `forge_clone_siblings: false` when siblings already exist.

## Artifacts written by `project-intake apply --execute`

| Path | Content |
|------|---------|
| `<target>/.okf/project-intake.yaml` | Copy of intake (audit trail) |
| `<target>/.okf/project.md` | Purpose / scope patched from intake |
| `<target>/.okf/handoffs/YYYY-MM-DD-operator-standup.md` | Initial operator handoff |
