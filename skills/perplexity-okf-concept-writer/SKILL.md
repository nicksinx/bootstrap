---
name: perplexity-okf-concept-writer
description: Draft OKF concept documents from Perplexity Desktop Pro for Cursor or Codex to save. Use when Perplexity produces Reference concepts in MODE A research, OKF update drafts in MODE B integrator overflow, or structured concept output that must follow OKF frontmatter without becoming accepted truth until reviewed.
applies_to: [perplexity]
okf_mode: [research, overflow]
canonical_skill: skills/okf-concept-writer/SKILL.md
---

# Perplexity OKF Concept Writer

Use this skill when Perplexity output should become **draft OKF concepts** in the repository.

## When to use

- MODE A — drafting `Reference` concepts under `.okf/references/`
- MODE B integrator — drafting `.okf/log.md` entries, handoff concept bodies, or risk/requirement **drafts** for integrator review
- User asks for OKF-formatted Markdown with YAML frontmatter

## Perplexity constraint

Output complete Markdown files for Cursor or Codex to save. Perplexity must not claim concepts were committed or promoted.

## Frontmatter rules

Every concept draft must include valid OKF frontmatter:

```yaml
---
type: Reference
title: Human-readable title
description: One-sentence summary.
status: draft
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/example.md
tags: [okf]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: YYYY-MM-DDTHH:MM:SS+00:00
---
```

Use the correct `type`, `resource` path, and fields for the concept kind (Reference, Risk, Handoff, etc.).

## Perplexity defaults

- Perplexity-sourced concepts: always `verification_status: unverified` unless the user explicitly pastes already-reviewed OKF material.
- Reference concepts: always `source_of_truth: false` until promoted through review.
- Do not upgrade to `reviewed`, `tested`, or `accepted` from Perplexity alone.

## Reference sections

For `.okf/references/` drafts, include:

- `# Source`
- `# Summary`
- `# Relevant claims`
- `# Limitations and uncertainty`
- `# Suggested OKF links`

## Overflow integrator drafts

When completing integrator overflow, may draft:

- Short `.okf/log.md` append entry (text block for integrator)
- Handoff body sections (see `perplexity-okf-handoff-writer`)
- Draft risk or requirement **snippets** clearly marked for human review

Never overwrite accepted requirements or decisions directly.

## Guardrails

- Link to sources and paths; do not copy large authoritative artifacts into OKF.
- Never store secrets in concept drafts.

For full concept-writing contract, see `skills/okf-concept-writer/SKILL.md`.
