---
type: Agent Rule
title: Codex OKF Agent Rule
description: Codex-specific rules for working with the Project-1 OKF bundle.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/agents/codex.md
tags: [okf, codex, agent-rule]
applies_to: [codex]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# Purpose

Make Codex project work traceable to OKF context.

# Applies To

Codex tasks that inspect, create, modify, test, or document this project.

# Required Behaviour

Read `.okf/index.md`, `.okf/project.md`, and relevant concepts before substantive edits. Update `.okf/log.md` and affected concepts after substantive changes.

# Prohibited Behaviour

Do not invent project requirements not represented in OKF. Do not store secrets in OKF.

# Pre-Task Checklist

- Load OKF index and project files.
- Check recent handoffs.
- Identify relevant requirement or decision.

# Post-Task Checklist

- Update changed concepts.
- Record validation evidence.
- Create handoff if work is incomplete.

# Escalation Conditions

Escalate when requested work conflicts with accepted OKF concepts.
