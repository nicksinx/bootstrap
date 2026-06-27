---
type: Handoff
title: Bootstrap Refinement — Session Handoff (2026-06-28)
description: Session context for Claude Code continuing bootstrap kit and OKF ways-of-working refinement after Perplexity Space curation was completed.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/handoffs/2026-06-28-bootstrap-refinement-handoff.md
tags: [okf, handoff, bootstrap, claude, session-context]
applies_to: [claude, codex, cursor]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-28T00:00:00+01:00
---

# Bootstrap Refinement — Session Handoff (2026-06-28)

## Context

**Repo:** Project-1 OKF Bootstrap Kit (`/Users/dv/Projects/testrunner/Project-1`)

**Purpose:** Reusable OKF scaffold — `.okf` bundle, thin tool adapters, helper scripts, canonical skills, five-service LLM ops model, Perplexity research/overflow layer, continuous-improvement repo.

**Operator intent:** Continue refining bootstrap kit and OKF ways of working. **ProcureLex application research is deferred** (prompt exists at `.okf/prompts/perplexity-procurelex-research.md` but not actioned).

---

## Your role (Claude Code — service 3)

| Item | Detail |
|------|--------|
| Setup order | 1 Cursor → 2 Codex → **3 Claude Code** → 4 Xcode → 5 Perplexity |
| Adapter | `CLAUDE.md`, `.claude/commands/` (incl. `okf-sync.md`) |
| Dispatch | Default **`tester`** role in pipeline `builder → tester → reviewer → integrator` |
| Dispatch consumption | **Manual** — read packets from `.okf/dispatch/ready/` when invoked; no auto-hook like Codex Stop hook |
| Perplexity | Service 5 + MODE B overflow — you do **not** configure Perplexity; you **apply** its output via Cursor/Codex and run validation |

Read before changing files: `.okf/index.md` → `.okf/project.md` → `docs/okf-ways-of-working-brief.md` → relevant handoffs/concepts → matching `skills/*/SKILL.md`.

---

## What was done before this session

### Five-service model (complete in docs + scaffold)

- **Perplexity Desktop Pro** = service 5 (MODE A cited research → draft `.okf/references/`)
- **Overflow (MODE B)** = ad hoc substitute when a primary runner is blocked — not a sixth setup step
- Perplexity never writes the repo or advances dispatch; Cursor/Codex applies output

### Operator brief (canonical procedure)

- **`docs/okf-ways-of-working-brief.md`** — operator-facing "what to do now"; maintained after every material log entry
- **`.okf/references/*.md`** — citation/evidence layer (draft, `unverified`, `source_of_truth: false`)
- Both coexist; references are not obsolete when the brief exists

### Perplexity integration (complete)

- `docs/configure-perplexity-okf.md`, `docs/perplexity-project-files-and-skills.md`
- `.okf/agents/perplexity.md`, `.okf/agents/perplexity-overflow.md`
- Workflows + prompts under `.okf/workflows/` and `.okf/prompts/`
- Four canonical skills: `skills/perplexity-okf-{reader,citation-steward,handoff-writer,concept-writer}/`
- `PERPLEXITY.md` thin adapter via `scripts/okf-sync-skills --target perplexity`
- 11 draft references from shared-services research pack (`.okf/references/`)
- `.okf/improvements/2026-06-27-perplexity-research-lessons.md` (all P0/P1 closed)
- Perplexity Space curated and smoke-tested **PASS** (2026-06-28)

### Tooling (current state)

| Script | Purpose |
|--------|---------|
| `scripts/okf-sync-skills` | Regenerate thin adapters (`--target codex\|claude\|cursor\|perplexity`) |
| `scripts/okf-check-adapters` | Warn on canonical skill index drift in generated adapters |
| `scripts/okf-dispatch` | File-queue pipeline; `overflow --packet-id …` for MODE B metadata + handoff stub |
| `scripts/okf-validate` | Bundle validation; enforces draft Reference rules |

### Scaffold (`create-new-okf-project`)

- Five-service output when run from bootstrap kit path (full optional file copy)
- Smoke-tested: 66 files, validate 0 warnings

### Batch 1 soft-spot closure (2026-06-28)

- Brief: references vs docs, maintenance checklist, bootstrap path note
- Perplexity files guide: brief-once, Tier 6 optional
- Deferred: `.okf/prompts/perplexity-procurelex-research.md` (application Space — not started)

---

## Current handoffs (prior)

- Latest: `.okf/handoffs/2026-06-27-perplexity-research-implementation.md`
- Prior: `.okf/handoffs/2026-06-27-perplexity-okf-configuration.md`

---

## Key paths

1. `docs/okf-ways-of-working-brief.md`
2. `.okf/index.md`
3. `docs/shared-okf-skills.md`
4. `docs/okf-dispatch-orchestration.md`
5. `.okf/log.md` (tail — 2026-06-27/28 entries)
6. `.okf/improvements/2026-06-27-perplexity-research-lessons.md`

Setup guides: `docs/create-new-okf-project-in-{cursor,codex,claude,xcode,perplexity}.md`

---

## Operating rules (non-negotiable)

- Canonical skills in `skills/*/SKILL.md`; adapters stay thin — run `scripts/okf-sync-skills` after skill edits
- Draft research stays `verification_status: unverified`, `source_of_truth: false` until human/build-agent review
- No secrets in OKF; no fake citations
- Perplexity chat is not durable state — ingest to `.okf/` via Cursor/Codex
- After material changes: append `.okf/log.md`, run `scripts/okf-validate` (and `scripts/okf-check-adapters` if adapters touched)
- Write handoff under `.okf/handoffs/` before stopping if another agent continues

---

## Suggested focus — bootstrap and ways-of-working refinement

User priority: improve Project-1 bootstrap kit and OKF operating model before application work.

Candidate areas:

1. **Claude Code step-3 guide** — align `docs/create-new-okf-project-in-claude.md` with five-service + Perplexity + overflow reality (written before Perplexity integration existed)
2. **Scaffold parity** — ensure `create_okf_project.py` copies all optional bootstrap files reliably; document/test sparse-clone behavior
3. **Xcode step-4** — flesh out verification path for `xcode-claude` dispatch consumer
4. **Dispatch ergonomics** — tester/reviewer handoff templates, evidence in `.okf/tests/`
5. **Brief + index hygiene** — keep operator brief and `.okf/index.md` in sync after each refinement
6. **Improvements repo** — capture lessons from Perplexity smoke test and multi-agent ops

---

## Out of scope (for now)

- **ProcureLex** application Perplexity Space / feeds-corpus research
- Promoting `.okf/agents/xcode-claude.md` from `draft` (needs real Xcode verification)
- Optional research: Perplexity file limits, Computer skills vs Project Skills (#10 in improvements)

---

## Validation baseline

Last known: `scripts/okf-validate` passed (0 warnings) after 2026-06-28 changes.

Re-run after any edits.

---

## When you finish

1. Run `scripts/okf-validate` (+ `okf-check-adapters` if adapters changed)
2. Append `.okf/log.md`
3. Write `.okf/handoffs/YYYY-MM-DD-<task>.md` with changed files, decisions, next actions
4. Do not push unless user asks
