---
type: Improvement
title: Continuous Improvement Repository
description: Defines the OKF repository for lessons learned, retrospectives, and process improvements.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/improvements/continuous-improvement-repository.md
tags: [okf, continuous-improvement, lessons-learned]
applies_to: [cursor, claude, codex, chatgpt, ollama, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# Purpose

Capture lessons learned over the life of the project so operational knowledge improves instead of disappearing into chat history, handoffs, or individual memory.

# Repository Scope

Use `.okf/improvements/` for:

- Lessons learned from implementation, testing, releases, incidents, and handoffs.
- Retrospectives after milestones or failures.
- Improvement actions for project workflow, agent instructions, tools, tests, and OKF conventions.
- Reusable practices that should be promoted into templates, scripts, skills, or adapters.

# Concept Types

Use these concept types:

- `Lesson Learned`
- `Improvement`
- `Retrospective`

# Required Sections

Improvement concepts should include:

- `# Observation`
- `# Context`
- `# Impact`
- `# Recommendation`
- `# Action Items`
- `# Related Concepts`
- `# Review Cadence`

# Operating Rules

Agents should add or update an improvement concept when a task reveals a reusable process lesson, a recurring failure mode, a better prompt pattern, a tool limitation, or a workflow change.

Accepted improvements should be promoted into the relevant OKF template, skill, script, adapter, or agent rule.
