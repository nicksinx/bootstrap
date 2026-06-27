---
type: Reference
title: Shared agent memory and file-based handoffs
description: Project-local memory works best when AGENTS.md/CLAUDE.md-style instructions are small, layered, and nearest-file wins.
status: draft
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/shared-agent-memory-handoffs.md
tags: [okf, reference, perplexity, deep-research, shared-services]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-27T19:42:00+02:00
---

# Source

- **Title:** AGENTS.md
- **URL:** https://agents.md
- **Retrieval date:** 2026-06-27
- **Source type:** primary project convention document

# Summary

AGENTS.md is a shared, open Markdown format for agent instructions, separate from human README content. It recommends focused guidance on build steps, tests, code style, and project conventions, and supports nested files where the nearest file in the directory tree takes precedence when instructions conflict.

# Relevant claims

- AGENTS.md is plain Markdown with no required fields.
- Closest AGENTS.md wins when instructions conflict.
- Nested AGENTS.md files are supported for large repos and monorepos.

# Limitations and uncertainty

The source is a project website rather than a formal standard; runtime behavior may differ across tools. Nearest-file precedence is stated on agents.md but should be verified per agent before hard-coding as OKF requirements.

# Suggested OKF links

- `.okf/handoffs/`
- `.okf/context-packs/`
- `skills/*/SKILL.md`
- `AGENTS.md`
