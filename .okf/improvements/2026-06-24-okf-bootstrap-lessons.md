---
type: Lesson Learned
title: OKF Bootstrap Lessons
description: Initial lessons learned while creating the Project-1 OKF bootstrap kit.
status: active
lifecycle_stage: build
owner: project
source_of_truth: true
resource: .okf/improvements/2026-06-24-okf-bootstrap-lessons.md
tags: [okf, lessons-learned, bootstrap, codex-skills]
applies_to: [codex, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# Observation

An OKF project needs a continuous-improvement repository from the beginning, not only after the first retrospective.

# Context

Project-1 initially captured requirements, architecture, decisions, risks, handoffs, tests, releases, and references. The missing long-lived repository was a place to convert workflow lessons into reusable improvements.

# Impact

Without a first-class improvement area, useful lessons can remain trapped in chat, generated handoffs, or one-off validation notes.

# Recommendation

Every new OKF project should include `.okf/improvements/` and a seed concept that explains how to capture lessons learned, retrospectives, and improvement actions.

# Action Items

- Add `.okf/improvements/` to the Project-1 OKF bundle.
- Add improvement templates to `templates/okf/improvements/`.
- Teach `create-new-okf-project` to scaffold continuous improvement by default.
- Update validators to treat improvement concept types as project-critical.

# Related Concepts

- `.okf/improvements/continuous-improvement-repository.md`
- `.okf/architecture/okf-bootstrap-layout.md`
- `.okf/workflows/agent-okf-lifecycle.md`

# Review Cadence

Review improvement concepts at milestone boundaries, before release, after incidents, and after substantial agent handoffs.
