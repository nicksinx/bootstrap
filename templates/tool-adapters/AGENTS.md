# Codex OKF Adapter

This repository uses `.okf` as the durable project context layer across Cursor, Codex, Claude Code, Xcode-connected Claude Agent, and Perplexity Desktop Pro.

Before substantive changes, read `.okf/index.md`, `.okf/project.md`, relevant concepts, and recent handoffs.

Keep changes traceable to OKF requirements, features, decisions, risks, runbooks, or handoffs.

After substantive changes, update affected OKF concepts, append to `.okf/log.md`, and create a handoff when work pauses or transfers.

For OKF-related delivery, read and follow the relevant canonical skill under `skills/*/SKILL.md` instead of improvising workflows. Run `scripts/okf-sync-skills` to add a generated skill index to this file after skills are installed.

Perplexity Desktop Pro is service 5 for cited research and an ad hoc overflow substitute when a primary runner is blocked. Perplexity never writes the repository directly; Cursor or Codex ingests output and runs validation.

Do not store secrets in OKF.
