---
type: Handoff
title: Project-1 Bootstrap Handoff
description: Continuity note for the initial OKF bootstrap project setup.
status: active
lifecycle_stage: build
owner: project
source_of_truth: true
resource: .okf/handoffs/2026-06-24-project-bootstrap.md
tags: [okf, handoff, bootstrap]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# Current State

Project-1 has been scaffolded as an OKF bootstrap kit.

# Completed Work

- Created `.okf` concept set.
- Created tool adapters.
- Created helper script placeholders and install instructions.
- Created Codex skill folders.
- Added continuous-improvement repository under `.okf/improvements/`.
- Added `create-new-okf-project` skill for scaffolding future OKF projects.

# Decisions Made

- `.okf` is the durable source of curated context.
- Tool adapters remain thin.
- Skills are installed manually by copying folders into Codex's skill directory.

# Files Changed

- `Project-1/.okf/`
- `Project-1/AGENTS.md`
- `Project-1/CLAUDE.md`
- `Project-1/.cursor/rules/okf.mdc`
- `Project-1/scripts/`
- `Project-1/skills/`
- `Project-1/templates/`
- `Project-1/.okf/improvements/`

# Known Issues

- Future projects may need stricter validators for organization-specific policies.

# Next Recommended Actions

1. Run `scripts/okf-validate`.
2. Run skill validation for all skills.
3. Install skills with `CODEX-SKILL-INSTALL.md` if desired.

# Validation Needed

Run the validation plan in `.okf/tests/okf-validation-plan.md`.

# Context Pack

Use `scripts/okf-context-pack` for larger follow-up work.
