---
type: Reference
title: OKF Handoffs Guide
description: Operating guide for handoff files, precedence, and when to use handoffs versus context packs.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/handoffs/README.md
tags: [okf, handoffs, guide]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T20:00:00+02:00
---

# OKF Handoffs

Handoffs are **active continuity notes** for paused, transferred, or overflow work. They are not durable requirements and not a substitute for `.okf/requirements/`.

## When to write a handoff

- Work pauses before completion
- Another agent or service may continue (Cursor, Codex, Claude, Xcode, Perplexity overflow)
- Primary runner blocked by usage limits, outage, or policy
- Perplexity research cycle complete and Cursor/Codex must ingest references

## File naming

```text
.okf/handoffs/YYYY-MM-DD-short-task-name.md
```

Use `scripts/okf-handoff <task-slug> --summary "..."` when available.

## Required sections

Every handoff must include:

- `# Current State`
- `# Completed Work`
- `# Decisions Made`
- `# Files Changed`
- `# Known Issues`
- `# Next Recommended Actions`
- `# Validation Needed`
- `# Context Pack`

For overflow failovers, also include: `primary_runner`, `overflow_runner`, `failover_reason`, `role`, `overflow_model_used`.

## Handoff vs other OKF locations

| Location | Purpose |
|----------|---------|
| `.okf/handoffs/` | Active work transfer; may go stale after resume |
| `.okf/context-packs/` | Ephemeral task snapshots for paste into agents (not source of truth) |
| `.okf/references/` | Cited external evidence (`verification_status: unverified` until reviewed) |
| `.okf/requirements/` | Accepted project requirements (after review) |
| `.okf/log.md` | Chronological project log (append-only summary) |
| `.okf/improvements/` | Durable lessons learned and process changes |

## Instruction precedence (repo-scoped)

When multiple instruction files apply:

1. Nearest repo-scoped adapter or rule wins for **tool behavior** (AGENTS.md, CLAUDE.md, `.cursor/rules/`, `PERPLEXITY.md` guidance).
2. **OKF concepts** remain authoritative for project truth (`verification_status`, `source_of_truth`).
3. **Canonical skills** (`skills/*/SKILL.md`) define workflows; adapters must not duplicate full skill bodies.
4. Chat transcripts are never authoritative.

See `.okf/references/shared-agent-memory-handoffs.md` for external evidence on nearest-file patterns.

## Template

Copy `TEMPLATE.md` in this directory or use `skills/okf-handoff-writer/SKILL.md`.

### Template selection

| Template | When to use |
|----------|-------------|
| `TEMPLATE.md` | General work transfer (any role or service) |
| `TEMPLATE-tester.md` | Tester role handing off to reviewer — structured test evidence table, issues for reviewer attention, pre-filled reviewer next steps |
| `TEMPLATE-reviewer.md` | Reviewer role handing off to integrator — requirements-checked table, findings with severity, reviewer verdict, pre-filled integrator next steps |
| `TEMPLATE-xcode-step4.md` | Xcode service 4 → Perplexity step 5 (record dry vs live verification level) |

Role-specific templates extend the standard required sections — they do not replace them. Include all eight required sections even when using a role template.

## After writing a handoff

1. Append a short entry to `.okf/log.md`
2. Run `scripts/okf-validate` if OKF concepts changed
3. Link the handoff from `.okf/index.md` when it is the current continuity note
