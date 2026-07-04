# Perplexity Project Files and Skills

Guide for attaching **Files** and **Skills** in Perplexity Desktop Pro / Spaces for OKF-enabled projects.

Configuration overview: `docs/configure-perplexity-okf.md`

Research evidence: `.okf/references/perplexity-spaces-dev-workflow.md`, `.okf/references/perplexity-file-limits.md`

## Terminology note

Perplexity help center documents **Spaces** (custom instructions, files, threads) and **Computer skills** (`SKILL.md` with YAML frontmatter). OKF treats **Spaces / Desktop project settings** as the verified research surface. Computer skills are adjacent but distinct from classic research threads.

## Attachment budget

| Guideline | Value |
|-----------|--------|
| Target file count | ~8–14 curated files |
| Avoid | Whole repo, dispatch JSON, secrets, long log history |
| Per Space (Pro) | Up to 50 files documented; prefer fewer high-signal files |
| Size | Help pages report differing limits (≈40–50 MB per file); keep Markdown packs small |
| Thread uploads | May count toward weekly allowances — prefer Space-level attachments for stable context |

When in doubt, attach **core OKF identity + active task** only; paste overflow or research detail via context pack in-thread.

## Tier 1 — always attach

| File | Why |
|------|-----|
| `.okf/project.md` | Identity and scope |
| `.okf/index.md` | Navigation |
| `PERPLEXITY.md` | Dual-mode adapter |
| `docs/okf-ways-of-working-brief.md` | **Canonical operator summary** (attach once only — do not duplicate in Tier 2–4) |

**Budget rule:** Count the operator brief as **one** file. Use remaining slots for handoffs and active specs, not duplicate setup docs.

## Tier 2 — mode contracts

| File | Why |
|------|-----|
| `.okf/prompts/perplexity-deep-research-setup.md` | MODE A |
| `.okf/prompts/perplexity-overflow-failover.md` | MODE B |
| `.okf/workflows/perplexity-research-cycle.md` | Research checklist |
| `.okf/workflows/perplexity-overflow-failover.md` | Overflow checklist |

## Tier 3 — agent rules

| File | Why |
|------|-----|
| `.okf/agents/perplexity.md` | Service 5 |
| `.okf/agents/perplexity-overflow.md` | Overflow |

## Tier 4 — refresh often

| File | Why |
|------|-----|
| Latest `.okf/handoffs/*.md` | Continuity |
| Active requirement or spec | Current task |

## Tier 5 — session-only

Decisions, architecture, reference index — add when relevant; remove when stale.

## Tier 6 — optional (avoid re-recommending closed work)

| File | Why |
|------|-----|
| `.okf/improvements/2026-06-27-perplexity-research-lessons.md` | Accepted lessons; closed P0/P1 backlog |
| `.okf/references/multi-agent-risks.md` | Risk context for research sessions |

Remove Tier 6 files when no longer relevant to avoid stale guidance.

## Project Skills (attach four)

| Skill | Source |
|-------|--------|
| Perplexity OKF Reader | `skills/perplexity-okf-reader/SKILL.md` |
| Perplexity OKF Citation Steward | `skills/perplexity-okf-citation-steward/SKILL.md` |
| Perplexity OKF Handoff Writer | `skills/perplexity-okf-handoff-writer/SKILL.md` |
| Perplexity OKF Concept Writer | `skills/perplexity-okf-concept-writer/SKILL.md` |

Upload `.md` or paste skill body below frontmatter. Minimum frontmatter for Perplexity: `name`, `description`. OKF extends with `applies_to`, `okf_mode`, `canonical_skill` — see `docs/skill-frontmatter-compatibility.md`.

## MODE emphasis

| Mode | Files | Skills |
|------|-------|--------|
| MODE A — Research | Tiers 1–3 + active spec | Citation Steward, Concept Writer, Handoff Writer |
| MODE B — Overflow | Tier 1 + latest handoff + overflow prompt | Reader, Handoff Writer, Concept Writer |

## Maintenance

- Replace latest handoff and active spec each sprint or task
- Re-sync skills when `skills/perplexity-okf-*/SKILL.md` changes
- After ingest, save references to `.okf/references/` via Cursor/Codex — do not treat Space chat as durable OKF
- When `docs/okf-ways-of-working-brief.md` changes in the repo, re-upload it to Project Files
- Do not attach the brief twice (Tier 1 only)

## Post-curation smoke test

After first Space setup or major file refresh, run `.okf/prompts/perplexity-post-curation-smoke-test.md` in the Space. Expect **PASS** before relying on Perplexity for MODE A research.

## Do not attach

- `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/` (other tools)
- `.okf/dispatch/` queues
- Secrets, credentials, customer data
- Full codebase
