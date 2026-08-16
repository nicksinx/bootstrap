# OKF Project Profile

Use this profile when creating a new OKF-enabled software or agentic project.

## Directory Layout

```text
project-root/
  .okf/
    index.md
    log.md
    project.md
    requirements/
    features/
    architecture/
    decisions/
    components/
    data/
    apis/
    workflows/
    agents/
    prompts/
    risks/
    tests/
    releases/
    handoffs/
    references/
    improvements/
  AGENTS.md
  CLAUDE.md
  .cursor/rules/okf.mdc
  scripts/
    okf-validate
    okf-migrate
    okf-context-pack
    okf-handoff
```

## Reserved files

- Root `index.md` may carry only `okf_version: "0.2"` in frontmatter.
- Nested `index.md` files have no frontmatter.
- `log.md` has no frontmatter and uses newest-first `## YYYY-MM-DD` headings.

## Concept frontmatter

Every concept should include:

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
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: unverified
generated: { by: process:project-scaffold, at: 2026-08-16T10:00:00Z }
---
```

Use only `draft`, `stable`, or `deprecated` for standard lifecycle status. Preserve unknown extension fields. Omit `verified` until an actor actually verifies the concept.

## Continuous Improvement

`.okf/improvements/` is required. It captures lessons learned over the project lifecycle and prevents operational knowledge from staying only in chat or handoff files.

Recommended concept types:

- `Lesson Learned`
- `Improvement`
- `Retrospective`

Required sections:

- `# Observation`
- `# Context`
- `# Impact`
- `# Recommendation`
- `# Action Items`
- `# Related Concepts`
- `# Review Cadence`

Agents should add or update improvement concepts after recurring failures, workflow discoveries, tool limitations, successful process changes, major releases, incidents, and substantial cross-agent handoffs.

Accepted improvements should be promoted into templates, scripts, skills, adapters, or agent rules.

## Operating Rules

- Treat `.okf` as source-of-context, not a replacement for source code, tests, API specs, schemas, issue trackers, or contracts.
- Keep tool adapters thin and point them back to `.okf`.
- Do not store secrets, credentials, private keys, sensitive personal data, or confidential third-party material in OKF.
- Prefer non-stale stable concepts with appropriate v0.2 verification events over draft or unverified concepts.
- Create a handoff before stopping unfinished work.
- Append to `.okf/log.md` after substantive changes.
