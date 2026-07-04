---
type: Agent Rule
title: Cursor OKF Agent Rule
description: Cursor-specific rules for using Project-1 shared OKF context alongside existing Cursor global skills.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/agents/cursor.md
tags: [okf, cursor, agent-rule, shared-skills]
applies_to: [cursor]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T12:00:00+01:00
---

# Purpose

Make Cursor participate in the shared OKF operating model as a project-local overlay without replacing Cursor global skills.

# Applies To

`.cursor/rules/okf.mdc` and Cursor-assisted implementation in this repository.

# Required Behaviour

- Read `.okf/index.md` and `.okf/project.md` before substantive project changes.
- For OKF-related delivery, follow canonical skills in `skills/*/SKILL.md`.
- Keep Cursor global skills valid; use them when they fit the task.
- Update OKF after material changes and create handoff notes before stopping unfinished work.
- Refresh thin adapters with `scripts/okf-sync-skills` after canonical skill changes.

# Prohibited Behaviour

- Do not duplicate durable project knowledge or canonical skill bodies in Cursor rules.
- Do not modify Cursor global skills or user-level Cursor configuration from this project.

# Pre-Task Checklist

- Read OKF index and project.
- Check recent handoffs.
- Identify the matching canonical skill under `skills/`.

# Post-Task Checklist

- Update concepts and log.
- Add handoff if needed.

# Escalation Conditions

Escalate if code changes cannot be traced to an OKF concept.
