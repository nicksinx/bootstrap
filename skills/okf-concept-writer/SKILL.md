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
lifecycle_stage: planning
owner: project
source_of_truth: true
resource: .okf/requirements/example.md
tags: [okf]
applies_to: [codex, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-24T15:54:09+01:00
---
```

Use the real concept type, path, owner, status, lifecycle stage, sensitivity, and verification status. Preserve unknown frontmatter fields when editing existing concepts.

## Section Templates

For requirements, include:

- `# Intent`
- `# Requirement`
- `# Acceptance Criteria`
- `# Dependencies`
- `# Risks`
- `# Verification`
- `# Citations`

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

Mark uncertain material as `verification_status: unverified`. Do not upgrade a concept to `reviewed`, `tested`, or `accepted` without evidence.

Store continuous-improvement concepts under `.okf/improvements/` and promote accepted improvements into templates, scripts, skills, adapters, or agent rules.

Never store secrets in OKF.
