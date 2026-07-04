# Migration from legacy bootstrap (v1.x)

Bootstrap **v2.0.0** unifies OKF + Forge + OKF dispatch in the `default` profile. The ai-task MCP track and worker orchestration are deprecated.

## What changed

| Area | v1.x (`default` v1.1.0) | v2.0.0 (`default`) |
|------|-------------------------|---------------------|
| MCP | Optional ai-task (`--with-mcp`) | Forge lifecycle MCP (auto `.cursor/mcp.json`) |
| Delivery | `scripts/workers/*` + `scripts/mcp/*` | `scripts/okf-dispatch` |
| Profile `forge-lifecycle` | Overlay on default | Alias for `default` v2 |
| Template version | `1.1.0` | `2.0.0` |

## New projects

Use `default` profile (no flags required for Forge MCP config):

```bash
./scripts/launch_project.sh --name my-product --profile default --target-dir ./out/my-product
```

## Existing projects on v1.x

1. Read [okf-forge-bootstrap-alignment-plan.md](okf-forge-bootstrap-alignment-plan.md).
2. Compare your tree to a fresh v2 launch (`--dry-run` diff).
3. Adopt incrementally:
   - Copy Forge launchers and `scripts/okf-dispatch*` from a v2 scaffold.
   - Replace `.cursor/mcp.json` with forge-lifecycle example.
   - Remove or archive `scripts/mcp/` and `scripts/workers/` if unused.
   - Update `Makefile` targets to `okf-dispatch-status` instead of `worker-*`.
4. Re-run `scripts/validate_launch.sh`.

## Deprecated `legacy-task` profile

For short-term compatibility only:

```bash
./scripts/launch_project.sh --name my-legacy --profile legacy-task --with-mcp --with-mcp-config
```

This restores ai-task MCP wrappers and worker scripts via `templates/legacy-task/` overlay. New products should not use this profile.

## Related

- [Project-1 harness](https://github.com/nicksinx/Project-1) — integration reference
- `profiles/legacy-task.yaml` — deprecated profile definition
