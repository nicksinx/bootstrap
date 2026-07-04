---
type: Agent Rule
title: Claude OKF Agent Rule
description: Claude-specific rules for using the Project-1 OKF bundle.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/agents/claude.md
tags: [okf, claude, agent-rule]
applies_to: [claude]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# Purpose

Keep Claude work aligned with the shared OKF context bundle.

# Applies To

Claude Desktop and Claude Code workflows.

# Required Behaviour

Read the OKF bundle before project changes, preserve citations, and update concepts when project state changes.

# Prohibited Behaviour

Do not let Claude-specific notes become the only durable project memory.

# Pre-Task Checklist

- Read `.okf/index.md`.
- Read `.okf/project.md`.
- Read relevant concepts and recent handoffs.

# Post-Task Checklist

- Update OKF concepts.
- Append to `.okf/log.md`.
- Create handoff when needed.

# Escalation Conditions

Escalate when external claims are uncited or unreviewed.
