# Changelog

## 2.3.0 - 2026-08-16

- Add an opt-in OpenWiki sidecar that runs in staging and imports only bounded generated output.
- Preserve valid OpenWiki-owned blocks when regenerating `AGENTS.md` and `CLAUDE.md`.
- Add a path-contained, read-only OKF MCP pilot with modern and legacy stdio protocol tests.
- Add one deterministic OKF v0.2 `Attested Computation` and an explicitly experimental receipt/verdict ABI.
- Extend launch validation, canonical scaffolding, and CI checks across all three integration surfaces.

## 2.2.0 - 2026-08-16

- Add deterministic generated blocks for root and per-directory OKF indexes.
- Add JSON and self-contained HTML concept graph exports.
- Add `stale_after` freshness inventory and CI-friendly check modes.
- Include indexing, graph, and freshness tooling in canonical and standalone project scaffolds.
- Restore canonical scaffold parity for five-service agent rules, prompts, handoff templates, context-pack guidance, Xcode risk material, and Codex installation instructions.

## 2.1.0 - 2026-08-16

### Added

- OKF v0.2 strict validator with real YAML parsing and JSON output
- Idempotent `scripts/okf-migrate` check/apply workflow
- Canonical scaffold delegation from `create-new-okf-project`
- Strict skill/adaptor and generated-project validation gates

### Changed

- OKF concepts and templates use v0.2 generated/status metadata
- Launcher accepts a separate display name and OKF owner
- Generated service adapters are synchronized during launch
- Template version bumped to `2.1.0`

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
