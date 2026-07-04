# Changelog

## 2.0.0 — 2026-06-27

**Breaking:** `default` profile v2.0.0 replaces ai-task MCP and worker orchestration with OKF + Forge + `okf-dispatch`.

### Added

- Forge MCP launchers, integration docs, and OKF workflows in `default` profile
- `scripts/okf-dispatch`, `okf-sync-skills`, adapter and forge receipt checks
- Five-service operator setup guides
- `profiles/legacy-task.yaml` for deprecated ai-task path
- `docs/migration-from-legacy-bootstrap.md`

### Changed

- `profiles/forge-lifecycle.yaml` is now a deprecated alias for `default` v2
- Launcher auto-writes Forge `.cursor/mcp.json` for non-legacy profiles
- Template version bumped to `2.0.0`

### Removed from default profile

- `scripts/mcp/*` (ai-task wrappers)
- `scripts/workers/*` (background worker dispatch)
- Separate `templates/forge-lifecycle` overlay (merged into `new-project`)

### Migration

See [docs/migration-from-legacy-bootstrap.md](docs/migration-from-legacy-bootstrap.md).

## 1.1.0

- OKF bundle, backlog contracts, optional ai-task MCP, worker stubs
- `forge-lifecycle` profile overlay
