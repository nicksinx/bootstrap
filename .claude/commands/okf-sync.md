Refresh all OKF tool adapters from canonical skill definitions.

Run this after editing any `skills/*/SKILL.md` file to propagate changes to `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/okf.mdc`, and `.okf/agents/future-service.md`.

Steps:
1. Run `scripts/okf-sync-skills` from the project root.
2. Run `scripts/okf-validate` to confirm the bundle passes.
3. Append a short note to `.okf/log.md` describing what changed.

If you only want to preview changes without writing files, run `scripts/okf-sync-skills --dry-run`.
To refresh a single adapter, run `scripts/okf-sync-skills --target <codex|claude|cursor|future>`.
