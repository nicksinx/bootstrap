---
name: perplexity-okf-handoff-writer
description: Write OKF handoff and ingest blocks from Perplexity Desktop Pro when research or overflow work pauses or transfers to Cursor or Codex. Use when Perplexity completes MODE A research, MODE B overflow deliverables, or the user ends a session before repo changes are applied.
applies_to: [perplexity]
okf_mode: [research, overflow]
canonical_skill: skills/okf-handoff-writer/SKILL.md
---

# Perplexity OKF Handoff Writer

Use this skill at the **end** of every substantive Perplexity session on an OKF project.

## When to use

- MODE A research cycle complete (references ready for ingest)
- MODE B overflow deliverable complete (integrator must apply changes)
- User pauses work that Cursor, Codex, Claude, or Xcode may continue

## Perplexity constraint

Perplexity does **not** write to the repository. Produce handoff **content** for Cursor or Codex to save under `.okf/handoffs/YYYY-MM-DD-short-task-name.md`.

## Required sections

Include these sections in the handoff block:

- `# Current State`
- `# Completed Work`
- `# Decisions Made`
- `# Files Changed` (paths to create or update in the repo)
- `# Known Issues`
- `# Next Recommended Actions`
- `# Validation Needed`
- `# Context Pack`

## MODE A — Research closing block

Also include:

- **References produced** — list draft filenames for `.okf/references/`
- **Highest-confidence findings** — 3–5 bullets
- **Findings that must not become requirements without review**
- **Integrator commands** — `scripts/okf-validate`, update `.okf/index.md`, append `.okf/log.md`

## MODE B — Overflow closing block

Also include:

- **Role completed** — builder | tester | reviewer | integrator
- **Primary runner blocked** — codex | claude | cursor | xcode-claude
- **Failover reason** — usage_limit | outage | policy | user_choice
- **Overflow model used** — best | sonar-2 | gpt-5.4 | etc.
- **Routing note**
- **Resume primary runner when**

## Content rules

Write for the next agent, not the transcript. Use concrete paths and validation steps.

Do not include secrets. Do not claim repo changes were applied.

For full handoff contract, see `skills/okf-handoff-writer/SKILL.md`.
