---
name: okf-concept-writer
description: Create or update Open Knowledge Format concept documents for software and agentic projects. Use when an agent needs to add requirements, features, architecture notes, decisions, workflows, risks, tests, releases, handoffs, references, agent rules, or tool adapters inside an .okf bundle.
---

# OKF Concept Writer

Use this skill when durable project knowledge should be added to or updated in `.okf`, including lessons learned and continuous-improvement concepts.

## Frontmatter

Every concept document should include:

```yaml
---
type: Requirement
title: Human-readable title
description: One-sentence summary.
status: draft
generated: { by: process:concept-authoring, at: 2026-08-16T10:00:00Z }
lifecycle_stage: planning
owner: project
source_of_truth: true
resource: .okf/requirements/example.md
tags: [okf]
applies_to: [codex, local-agent]
sensitivity: internal
verification_status: unverified
---
```

Use `status: draft`, `stable`, or `deprecated`. Use `generated.by` and `verified[].by` actors that follow the OKF convention. Add `stale_after` when a concept has a known review horizon. Preserve unknown frontmatter fields when editing existing concepts.

Do not put concept metadata on `index.md` or `log.md`. Only the bundle-root index may carry `okf_version: "0.2"`; logs use date headings and no frontmatter.

## Section Templates

For requirements, include:

- `# Intent`
- `# Requirement`
- `# Acceptance Criteria`
- `# Dependencies`
- `# Risks`
- `# Verification`
- `sources` frontmatter entries and keyed Markdown footnotes for externally sourced claims

For features, include:

- `# User Value`
- `# Scope`
- `# Out of Scope`
- `# Behaviour`
- `# UX Notes`
- `# Data / API Impact`
- `# Test Expectations`
- `# Related Concepts`

For decisions, include:

- `# Decision`
- `# Context`
- `# Options Considered`
- `# Rationale`
- `# Consequences`
- `# Reversal Conditions`
- `# Related Concepts`

For handoffs, include:

- `# Current State`
- `# Completed Work`
- `# Decisions Made`
- `# Files Changed`
- `# Known Issues`
- `# Next Recommended Actions`
- `# Validation Needed`
- `# Context Pack`

For improvements, lessons learned, and retrospectives, include:

- `# Observation`
- `# Context`
- `# Impact`
- `# Recommendation`
- `# Action Items`
- `# Related Concepts`
- `# Review Cadence`

## Writing Rules

Keep concepts human-readable. Link to source files, tests, APIs, issues, and external references instead of copying large authoritative artifacts into OKF.

Omit `verified` for uncertain material. Add a verification event only when the named actor actually checked the concept. The Project Bootstrap `verification_status` field may remain as a local workflow extension, but it does not replace the v0.2 trust tier derived from `verified`.

Store continuous-improvement concepts under `.okf/improvements/` and promote accepted improvements into templates, scripts, skills, adapters, or agent rules.

Never store secrets in OKF.
