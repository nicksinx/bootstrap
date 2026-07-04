---
type: Reference
title: Cross-platform skill adapter pattern
description: Canonical skills can stay in one place while thin adapters translate them into AGENTS.md, CLAUDE.md, Cursor rules, and Perplexity skill files.
status: draft
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/cross-platform-skill-adapters.md
tags: [okf, reference, perplexity, deep-research, shared-services]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-27T19:42:00+02:00
---

# Source

- **Title:** Agent Skills – Codex
- **URL:** https://developers.openai.com/codex/skills
- **Retrieval date:** 2026-06-27
- **Source type:** primary product documentation

# Summary

Codex treats skills as directories with SKILL.md plus optional assets, using concise metadata for selection before loading full instructions. That pattern supports canonical-skill-plus-adapter design where platform files are small pointers rather than duplicated policy.

# Relevant claims

- Codex skills are directory-based and support optional scripts, references, and assets.
- Codex relies on skill descriptions for selection and loads the full file later.
- Codex can disable implicit invocation per skill via metadata.

# Limitations and uncertainty

Cursor and Perplexity parsing rules were not fully re-verified. Adapter pattern follows documented Codex selection model; validate per platform before hard requirements.

# Suggested OKF links

- `skills/*/SKILL.md`
- `scripts/okf-sync-skills`
- `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/okf.mdc`, `PERPLEXITY.md`
