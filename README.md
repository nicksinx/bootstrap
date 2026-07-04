# Bootstrap Launcher Toolkit

Reusable project bootstrap toolkit for deterministic scaffolding, optional GitHub setup, backlog initialization, OKF project context, MCP wrappers, and local worker dispatch.

## Profiles

| Profile | Use when |
|---------|----------|
| `default` | Standard OKF product project with ai-task-orchestrator MCP wrappers |
| `forge-lifecycle` | Product project that will wire the Forge MCP portfolio (sibling clones, Cursor launchers, Option C integration docs) |

## Prerequisites

- `bash`
- `python3` with `pyyaml` and `jsonschema`
- `git`
- optional: `gh` for `--with-github`
- optional (forge-lifecycle): `node` + built sibling Forge repos

## Common commands

```bash
make test-contracts
make test-launch-smoke
make check
```

## Manual launch example

```bash
./scripts/launch_project.sh \
  --name demo-proj \
  --profile default \
  --target-dir ./out/demo-proj \
  --non-interactive
```

## Forge lifecycle launch example

```bash
./scripts/launch_project.sh \
  --name my-product \
  --profile forge-lifecycle \
  --target-dir ./out/my-product \
  --non-interactive

cd ./out/my-product
scripts/forge-clone-siblings.sh    # optional — clones nicksinx/*Forge peers
# build siblings, reload Cursor MCP
```

Writes `.cursor/mcp.json` from the forge example automatically. Lessons: `.okf/improvements/forge-lifecycle-bootstrap-lessons.md`.

## Repository layout

- `scripts/` launcher, validation, github/bootstrap helpers, workers
- `templates/new-project/` generated project template tree, including OKF context
- `templates/forge-lifecycle/` overlay for `forge-lifecycle` profile only
- `schemas/` JSON schema contracts
- `profiles/` launcher profile defaults
- `tests/` contract and smoke checks
