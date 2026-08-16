# OpenWiki as an OKF Sidecar

OpenWiki is an optional generated documentation sidecar. Curated project truth remains under `.okf`; OpenWiki output remains under `openwiki/`. The two stores have different ownership and must not overwrite each other.

The reviewed upstream boundary and links are recorded in `.okf/references/integration-protocol-boundaries.md`.
Follow `.okf/workflows/optional-integration-review.md` for enablement and evidence gates.

## Enable at Scaffold Time

```bash
scripts/launch_project.sh \
  --name example-project \
  --target-dir /path/to/example-project \
  --with-openwiki \
  --non-interactive
```

This records `integrations.openwiki.enabled: true` in `project.config.yaml` and creates operator-owned `openwiki/INSTRUCTIONS.md`. OpenWiki itself is not installed or run by the launcher.

## Run the Sidecar

Install the official OpenWiki CLI outside the repository, configure provider credentials in its user-level configuration, and then run:

```bash
scripts/openwiki-sidecar status
scripts/openwiki-sidecar init --dry-run
scripts/openwiki-sidecar init
scripts/openwiki-sidecar update
```

The wrapper copies the working tree to an isolated temporary directory, runs `openwiki --init` or `openwiki --update` there, verifies that staged `.okf` did not change, and imports only:

- generated `openwiki/` content;
- complete `<!-- OPENWIKI:START -->` blocks from `AGENTS.md` and `CLAUDE.md`.

Malformed marker blocks or any attempted `.okf` mutation fail closed before output is imported. A runtime lock prevents concurrent wrapper runs. `scripts/okf-sync-skills` preserves valid OpenWiki-owned blocks when regenerating OKF adapters.

`status` reports `lock_held`. Remove a stale `.okf-runtime/openwiki-sidecar.lock` only after confirming that no wrapper process is active.

## Ownership Boundary

| Path | Owner | Editing rule |
|------|-------|-------------|
| `.okf/` | Project operators and reviewed agents | Curated through OKF workflows and strict validation |
| `openwiki/INSTRUCTIONS.md` | Project operator | Durable guidance for generated wiki behavior |
| Other `openwiki/` files | OpenWiki | Regenerate through the wrapper; do not promote automatically |
| OpenWiki marker blocks | OpenWiki | Preserved by OKF adapter sync |
| Content outside marker blocks | Project Bootstrap / operators | OpenWiki must preserve it |

Generated wiki prose is navigation support, not accepted requirements or decisions. Promote any useful finding through normal OKF review and record provenance.

## Security

- Never place provider keys, tokens, `.env` content, or private credentials in `.okf`, `openwiki/`, instructions, or agent adapters.
- The staging copy excludes common secret/runtime locations, including `.env`, `.git`, `.okf-runtime`, `.venv`, and `node_modules`, and removes symlinks before execution.
- `OPENWIKI_COMMAND` is an operator-controlled local command override for testing or installation wrappers. Do not commit it.
- OpenWiki-generated OKF v0.1 output, when present, is a sidecar format and must not be copied into the curated OKF v0.2 bundle without migration and review.
