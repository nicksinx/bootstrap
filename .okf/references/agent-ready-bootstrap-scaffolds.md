---
type: Reference
title: Agent-ready bootstrap scaffold patterns
description: Agent-ready repos work best when the scaffold generates shared instructions, validation, and reusable skills from one canonical source.
status: draft
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/agent-ready-bootstrap-scaffolds.md
tags: [okf, reference, perplexity, deep-research, shared-services]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-27T19:42:00+02:00
---

# Source

- **Title:** AGENTS.md; Agent Skills – Codex
- **URL:** https://agents.md ; https://developers.openai.com/codex/skills
- **Retrieval date:** 2026-06-27
- **Source type:** primary convention and product documentation

# Summary

AGENTS.md recommends separating agent instructions from human README content and supports nested files for monorepos. Codex documents repo-scoped directory-based skills. Scaffolds should generate a small number of canonical sources plus repeatable adapters refreshed by sync scripts.

# Relevant claims

- AGENTS.md is intended for agent-focused project guidance.
- Nested agent instruction files are supported.
- Codex skills are directory-based and reusable.

# Limitations and uncertainty

Exact generator coverage in `skills/create-new-okf-project` was not audited in the research pass. Scaffold recommendations require separate code review.

# Suggested OKF links

- `skills/create-new-okf-project`
- `scripts/okf-sync-skills`
- `.okf/improvements/`
