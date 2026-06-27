---
type: Workflow
title: Agent OKF Lifecycle
description: Standard pre-task, implementation, post-task, and handoff workflow for OKF-aware agents.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/workflows/agent-okf-lifecycle.md
tags: [okf, workflow, agents]
applies_to: [cursor, claude, codex, chatgpt, ollama, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# Purpose

Keep project memory consistent across humans, agents, and tools.

# Applies To

Any agent making substantive changes to project files, requirements, architecture, tests, releases, or tool adapters.

# Required Behaviour

1. Locate `.okf`.
2. Read `.okf/index.md` and `.okf/project.md`.
3. Read concepts relevant to the task.
4. Check recent handoffs.
5. Link implementation to an OKF concept.
6. Update affected OKF concepts after substantive changes.
7. Append to `.okf/log.md`.
8. Capture durable lessons learned or process improvements under `.okf/improvements/`.
9. Create a handoff when stopping before work is complete.

# Prohibited Behaviour

- Do not store secrets in OKF.
- Do not treat deprecated, superseded, or archived concepts as current implementation guidance.
- Do not preserve durable decisions only in chat.
- Do not duplicate long-lived project knowledge into tool adapters.

# Pre-Task Checklist

- Read project and index concepts.
- Identify relevant concepts.
- Check status and verification fields.
- Identify likely affected source and test files.

# Post-Task Checklist

- Update changed concepts.
- Add or update test evidence.
- Record lessons learned when a workflow, risk, tool behavior, or project assumption changed.
- Append to log.
- Create a handoff when needed.

# Escalation Conditions

Ask the user before changing project direction, accepting unverified external claims, or storing any sensitive material.
