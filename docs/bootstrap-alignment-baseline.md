# Bootstrap alignment baseline (v2.0.0)

Recorded before/after expectations for OKF + Forge bootstrap alignment.

## Pre-alignment (v1.1.0 default)

- Shipped `scripts/mcp/*` (ai-task orchestrator wrappers)
- Shipped `scripts/workers/*` background worker dispatch
- Forge content only via `forge-lifecycle` profile overlay
- `cursor-ai-task-mcp-server-updated` documented as primary MCP path

## Post-alignment (v2.0.0 default)

- Ships Forge MCP launchers, `.cursor/mcp-forge-lifecycle.json.example`, auto-written `.cursor/mcp.json`
- Ships `scripts/okf-dispatch`, adapter checks, forge receipt checks, `okf-sync-skills`
- Ships five-service operator docs and OKF workflows (bridge, multi-agent pipeline, Perplexity)
- No `scripts/mcp/*` or `scripts/workers/*` in default tree
- `legacy-task` profile restores v1 ai-task + workers via overlay
- `forge-lifecycle` profile is deprecated alias for `default` v2

## Validation gates

```bash
make check                    # bootstrap repo
scripts/validate_launch.sh    # generated project
scripts/okf-validate        # OKF bundle
scripts/okf-dispatch status # dispatch spine
```

## Reference harness

[Project-1](https://github.com/nicksinx/Project-1) — canonical integration layout promoted into bootstrap templates.
