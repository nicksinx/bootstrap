---
type: Reference
title: Claude and AGENTS.md instruction layering
description: Claude Code and AGENTS.md both support local instruction files, so OKF should keep shared meaning in canonical skills and platform-specific wrappers thin.
status: draft
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/claude-agents-layering.md
tags: [okf, reference, perplexity, deep-research, shared-services]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-27T19:42:00+02:00
---

# Source

- **Title:** CLAUDE.md documentation; AGENTS.md
- **URL:** https://code.claude.com/docs/en/claudemd ; https://agents.md
- **Retrieval date:** 2026-06-27
- **Source type:** primary product documentation and convention document

# Summary

Claude Code’s project instruction file and the AGENTS.md ecosystem both support local, repo-scoped context. The maintainable pattern is durable instructions in one canonical source exposed through thin platform-specific adapters.

# Relevant claims

- Claude Code documents a local instruction file for project guidance.
- AGENTS.md is plain Markdown and can be nested with nearest-file precedence.

# Limitations and uncertainty

Exact machine-read format differences between platforms were not fully re-verified. Layering recommendation is an inference about maintainability, not a formal interoperability guarantee.

# Suggested OKF links

- `CLAUDE.md`, `AGENTS.md`
- `skills/*/SKILL.md`
- `docs/skill-frontmatter-compatibility.md`
