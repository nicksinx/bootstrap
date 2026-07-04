---
type: Feature
title: Shared OKF Skills
description: Project-1 provides reusable OKF skills and thin adapters so Codex, Claude Code, Cursor, Perplexity, and future services share the same skill contracts and project context.
status: active
lifecycle_stage: build
owner: project
source_of_truth: true
resource: .okf/features/shared-okf-skills.md
tags: [okf, skills, shared-operating-model, cursor, claude, codex, xcode, perplexity]
applies_to: [cursor, claude, codex, xcode-claude, chatgpt, perplexity, ollama, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T12:00:00+01:00
---

# User Value

Agents across Codex, Claude Code, Cursor, Perplexity, and future services can work from the same OKF project context, skill contracts, handoff format, and validation flow without relearning the project memory workflow each time.

# Scope

Canonical skill definitions live under `skills/*/SKILL.md`.

The project includes these skills:

Canonical OKF skills:

- `create-new-okf-project`
- `okf-reader`
- `okf-concept-writer`
- `okf-handoff-writer`
- `okf-requirements-auditor`
- `okf-citation-steward`
- `okf-risk-scanner`
- `okf-context-pack-builder`
- `okf-conformance-validator`

Perplexity Project Skills:

- `perplexity-okf-reader`
- `perplexity-okf-citation-steward`
- `perplexity-okf-handoff-writer`
- `perplexity-okf-concept-writer`

Thin adapters are refreshed by `scripts/okf-sync-skills` for:

- Codex: `AGENTS.md`
- Claude Code: `CLAUDE.md`
- Cursor: `.cursor/rules/okf.mdc` (project-local overlay; does not replace Cursor global skills)
- Perplexity: `PERPLEXITY.md` (Desktop Pro custom-instructions companion; agent rules under `.okf/agents/`)
- Future services: `.okf/agents/future-service.md`

Perplexity configuration guide: `docs/configure-perplexity-okf.md`
Xcode setup guide: `docs/create-new-okf-project-in-xcode.md`

# Out of Scope

- Modifying Cursor global skills or user-level Cursor configuration.
- Installing skills automatically outside this workspace.
- Implementing product-specific MCP servers.
- Duplicating canonical skill bodies inside tool adapters.

# Behaviour

Each skill includes a valid `SKILL.md` and, where applicable, `agents/openai.yaml`.

Canonical skill changes propagate by editing `skills/*/SKILL.md` once, then running `scripts/okf-sync-skills`.

Codex installs skills by copying folders from `skills/` per `CODEX-SKILL-INSTALL.md`.

`create-new-okf-project` shall scaffold `.okf/improvements/` by default so lessons learned and improvement actions are captured from project inception.

`create-new-okf-project` shall also scaffold Perplexity MODE A/MODE B prompts, workflows, agent rules, `PERPLEXITY.md`, dispatch directories, and the bundled `skills/` tree when available.

# UX Notes

Shared operating model documentation lives in `docs/shared-okf-skills.md`.

Codex install instructions live in `CODEX-SKILL-INSTALL.md`.

# Data / API Impact

No external API is required.

# Test Expectations

- `scripts/okf-validate` passes after adapter sync.
- `scripts/okf-sync-skills --dry-run` lists expected adapter updates.
- Each Codex skill folder should pass the Codex skill quick validator when installed.

# Related Concepts

- `.okf/features/codex-okf-skills.md` (superseded alias)
- `.okf/requirements/okf-bootstrap-kit.md`
- `.okf/workflows/agent-okf-lifecycle.md`
- `docs/shared-okf-skills.md`
