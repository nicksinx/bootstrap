---
type: Reference
title: Perplexity ProcureLex Research Prompt
description: MODE A research prompt for ProcureLex application work — not bootstrap kit meta-configuration.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/prompts/perplexity-procurelex-research.md
tags: [okf, prompt, perplexity, procurelex, research]
applies_to: [perplexity, cursor, codex, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-28T12:00:00+02:00
---

# Purpose

Use when Perplexity research targets **ProcureLex application delivery**, not Project-1 bootstrap configuration.

**Use a separate Perplexity Space or thread** from the OKF bootstrap kit Space. Attach application specs and project brief — not `docs/okf-ways-of-working-brief.md` as the primary context unless comparing OKF process.

# Prompt (copy below)

```markdown
MODE A — RESEARCH (ProcureLex application)

This thread is for **ProcureLex product research**, not OKF bootstrap meta-configuration.

## Context

- **Project:** ProcureLex (macOS procurement document analysis app)
- **OKF rule:** Output draft Reference concepts only (`verification_status: unverified`, `source_of_truth: false`)
- **Ingest:** Cursor saves to the ProcureLex repo `.okf/references/` when OKF is bootstrapped there

## Attach or paste

- Active spec (e.g. `spec-04-feeds-corpus-integration.md`)
- Project brief / problem statement
- Any open risks or architecture constraints from the user

## Research mandate (adjust per task)

Example for feeds/corpus integration:

1. RSS/Atom ingestion patterns for local-first macOS apps
2. HTML article → searchable corpus pipelines (FTS, chunking, embeddings)
3. Licensing and ToS for common feed providers and article storage
4. Failure modes: duplicate ingestion, partial parse, offline behavior
5. Comparable approaches in document/corpus tools (cite sources)

## Output format

One OKF Reference concept per topic (YAML frontmatter + Source, Summary, Relevant claims, Limitations, Suggested OKF links).

End with: Research index, Gap analysis, Handoff block for Cursor ingest.

## Rules

- Do not modify bootstrap kit docs or Project-1 OKF operating model
- Do not promote findings to accepted requirements
- Cite reachable sources; no invented citations
- Include Routing note

Do not re-run the Project-1 six-topic shared-services research pack unless explicitly asked.
```

# After Perplexity responds

Cursor or Codex saves references to the **ProcureLex** repo, runs validation if `.okf` exists, and links from specs/requirements without promoting unverified claims.
