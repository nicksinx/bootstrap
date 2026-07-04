---
type: Feature
title: Codex OKF Skills (Superseded)
description: Project-1 provides reusable Codex skills for reading, writing, auditing, and validating OKF.
status: superseded
lifecycle_stage: build
owner: project
source_of_truth: true
resource: .okf/features/codex-okf-skills.md
tags: [okf, codex, skills]
applies_to: [codex, cursor, claude, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T12:00:00+01:00
---

# Superseded

This feature is superseded by `.okf/features/shared-okf-skills.md`. Canonical skills are shared across Codex, Claude Code, Cursor, and future services.

# User Value

Codex can consistently work with OKF-enabled projects without relearning the project memory workflow each time.

# Scope

The project includes these skills:

- `create-new-okf-project`
- `okf-reader`
- `okf-concept-writer`
- `okf-handoff-writer`
- `okf-requirements-auditor`
- `okf-citation-steward`
- `okf-risk-scanner`
- `okf-context-pack-builder`
- `okf-conformance-validator`

# Out of Scope

- Installing skills automatically outside this workspace.
- Implementing product-specific MCP servers.
- Replacing repository-level adapters.

# Behaviour

Each skill includes a valid `SKILL.md` and `agents/openai.yaml`. Skills are installed by copying their folders into `${CODEX_HOME:-$HOME/.codex}/skills`.

`create-new-okf-project` shall scaffold `.okf/improvements/` by default so lessons learned and improvement actions are captured from project inception.

# UX Notes

Install instructions live in `CODEX-SKILL-INSTALL.md`.

# Data / API Impact

No external API is required.

# Test Expectations

Each skill should pass the Codex skill quick validator.

# Related Concepts

- `.okf/requirements/okf-bootstrap-kit.md`
- `.okf/workflows/agent-okf-lifecycle.md`
