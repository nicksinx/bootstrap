---
type: Reference
title: Perplexity skills for repeatable workflows
description: Perplexity Computer skills are reusable instructions with YAML frontmatter and file/zip import support, suggesting a portable skill-conversion layer for OKF.
status: draft
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/perplexity-skills-format.md
tags: [okf, reference, perplexity, deep-research, shared-services]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-27T19:42:00+02:00
---

# Source

- **Title:** How to use Computer Skills
- **URL:** https://www.perplexity.ai/help-center/en/articles/13914413-how-to-use-computer-skills.html
- **Retrieval date:** 2026-06-27
- **Source type:** primary product documentation

# Summary

Perplexity Computer skills are reusable instruction sets. Users can create skills by chatting or upload a `.md` or `.zip` file with a root `SKILL.md` containing YAML frontmatter with at least `name` and `description`. Relevant skills may load automatically based on the task.

# Relevant claims

- Skills are reusable instruction sets.
- Uploading a `.md` file or `.zip` with root `SKILL.md` is supported.
- `SKILL.md` must contain YAML frontmatter with `name` and `description`.
- Perplexity says relevant skills load automatically based on the task.

# Limitations and uncertainty

Documentation targets Perplexity Computer; Spaces and Desktop Pro project skills may differ. The portable `SKILL.md` pattern still applies to OKF `perplexity-okf-*` skills attached in project settings.

# Suggested OKF links

- `skills/perplexity-okf-*/SKILL.md`
- `PERPLEXITY.md`
- `docs/skill-frontmatter-compatibility.md`
