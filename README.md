# Bootstrap Launcher Toolkit

Reusable project bootstrap toolkit for deterministic scaffolding, optional GitHub setup, backlog initialization, MCP wrappers, and local worker dispatch.

## Prerequisites

- `bash`
- `python3` with `pyyaml` and `jsonschema`
- `git`
- optional: `gh` for `--with-github`

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

## Repository layout

- `scripts/` launcher, validation, github/bootstrap helpers, workers
- `templates/new-project/` generated project template tree
- `schemas/` JSON schema contracts
- `profiles/` launcher profile defaults
- `tests/` contract and smoke checks
