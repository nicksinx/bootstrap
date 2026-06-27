---
type: Reference
title: Codex skills and progressive disclosure
description: Codex loads skill metadata first and only opens full SKILL.md content when a skill is selected.
status: draft
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/codex-skills-disclosure.md
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

Codex skills are directory-based reusable workflows with required SKILL.md metadata and optional scripts, references, and assets. Codex uses progressive disclosure: it starts with skill name, description, and path, then loads full instructions only when needed.

# Relevant claims

- Skills are reusable workflows composed of instructions, resources, and optional scripts.
- Codex uses progressive disclosure to manage context efficiently.
- A skill directory may include SKILL.md, scripts, references, assets, and agents/openai.yaml.

# Limitations and uncertainty

This is Codex-specific behavior. Size budgets and truncation heuristics are implementation guidance for Codex, not universal across Cursor or Perplexity.

# Suggested OKF links

- `skills/*/SKILL.md`
- `.okf/context-packs/`
- `.okf/improvements/`
