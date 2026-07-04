---
name: perplexity-okf-citation-steward
description: Produce cited external research for OKF Reference concepts in Perplexity Desktop Pro. Use when Perplexity runs MODE A deep research, vendor scans, compliance checks, or any task where web-backed claims must become draft .okf/references/ material with verification_status unverified.
applies_to: [perplexity]
okf_mode: [research]
canonical_skill: skills/okf-citation-steward/SKILL.md
---

# Perplexity OKF Citation Steward

Use this skill for **service 5 (deep research)** in Perplexity Desktop Pro.

## When to use

- MODE A — RESEARCH sessions
- Domain, technology, compliance, vendor, or risk research for an OKF project
- User needs draft Reference concepts for Cursor or Codex to save under `.okf/references/`

## Workflow

1. Identify claims that depend on external sources.
2. Prefer primary sources for technical, legal, security, financial, or policy claims.
3. Use **Sonar 2** or **Best** when citation retrieval quality matters most.
4. Output one OKF `Reference` concept draft per research topic with:
   - YAML frontmatter: `type: Reference`, `verification_status: unverified`, `source_of_truth: false`
   - Source title, URL, retrieval date, source type
   - Summary in your own words (no long copyrighted paste)
   - Relevant claims, limitations, suggested OKF links
5. End with **Research index**, **Gap analysis**, and **Handoff block** for Cursor/Codex ingest.

## Reference frontmatter template

```yaml
---
type: Reference
title: Short descriptive title
description: One-sentence summary.
status: draft
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/slug-from-title.md
tags: [okf, reference, perplexity, deep-research]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: YYYY-MM-DDTHH:MM:SS+00:00
---
```

## Guardrails

- Do not invent citations or treat snippets as verified fact.
- Do not overwrite accepted OKF requirements or decisions from research alone.
- Do not set `verification_status` to `reviewed`, `tested`, or `accepted`.
- Do not store secrets or confidential third-party material in OKF drafts.
- Include a **Routing note** (search-heavy vs reasoning-heavy subtasks).

For full citation contract, see `skills/okf-citation-steward/SKILL.md`.
