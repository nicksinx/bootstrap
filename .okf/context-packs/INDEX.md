---
type: Reference
title: OKF Context Packs Index
description: Index and naming guide for ephemeral task-specific context packs.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/context-packs/INDEX.md
tags: [okf, context-packs, guide]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T20:00:00+02:00
---

# OKF Context Packs

Context packs are **ephemeral, task-specific bundles** for paste into Cursor, Codex, Claude, Perplexity, or other agents. They are **not** durable source material — OKF concepts remain authoritative.

Generate packs with `scripts/okf-context-pack` or `skills/okf-context-pack-builder/SKILL.md`.

## Pack types

| Pack | When to use | Typical contents |
|------|-------------|------------------|
| **research** | Perplexity MODE A | `.okf/project.md`, active requirement/spec, open risks, research questions |
| **overflow** | Perplexity MODE B or runner failover | Handoff, packet summary, acceptance criteria, changed files summary |
| **implementation** | Builder handoff to Codex/Claude/Cursor | Requirements, decisions, architecture constraints, test expectations |
| **review** | Reviewer role | Diff summary, acceptance criteria, risks, requirements links |
| **validation** | Pre-commit / pre-release | Changed OKF paths, validation commands, test evidence pointers |

## Rules

- Do not store secrets in context packs.
- Prefer paths and summaries over full file dumps.
- After ingest, durable updates belong in `.okf/`, not in the pack file.
- For Perplexity, keep packs small — see `docs/perplexity-project-files-and-skills.md` attachment budget.

## Naming (recommended)

```text
.okf/context-packs/YYYY-MM-DD-{pack-type}-{task-slug}.md
```

Generated packs may also live outside the repo (clipboard, Perplexity thread). Only promote content to OKF after review.

## Related

- `.okf/handoffs/README.md`
- `docs/perplexity-project-files-and-skills.md`
- `.okf/references/perplexity-file-limits.md`
