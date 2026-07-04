---
type: Reference
title: Claude project instructions and local context
description: Claude Code uses CLAUDE.md as a local instruction file and supports project-level context alongside user memory.
status: draft
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/claude-project-instructions.md
tags: [okf, reference, perplexity, deep-research, shared-services]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-27T19:42:00+02:00
---

# Source

- **Title:** CLAUDE.md documentation
- **URL:** https://code.claude.com/docs/en/claudemd
- **Retrieval date:** 2026-06-27
- **Source type:** primary product documentation

# Summary

Claude Code documents CLAUDE.md as a project instruction file for repo-scoped guidance carried into sessions. It is intended for durable project-level instructions rather than one-off prompts.

# Relevant claims

- CLAUDE.md is a documented instruction file for Claude Code.
- It is intended for project-level guidance rather than ephemeral prompting.

# Limitations and uncertainty

Priority rules between CLAUDE.md, user prompts, and other context files should be rechecked in current product docs before codifying as OKF requirements.

# Suggested OKF links

- `.okf/handoffs/`
- `CLAUDE.md`
- `.okf/context-packs/`
