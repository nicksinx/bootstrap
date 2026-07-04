---
type: Reference
title: Codex Prompt — Share OKF Ways of Working Updates
description: Copy-paste prompt for Codex to communicate OKF operating model updates to stakeholders or downstream project repos.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/prompts/codex-share-okf-ways-of-working-updates.md
tags: [okf, prompt, codex, communication, operating-model]
applies_to: [codex, cursor, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T23:00:00+02:00
---

# Purpose

Use when Codex should **communicate** (not re-implement) the current OKF ways of working after bootstrap, Perplexity integration, research implementation, and gap-closure updates.

# Prompt (copy below)

```markdown
You are updating stakeholders and downstream OKF project operators on the **current OKF ways of working** for Project-1 (OKF Bootstrap Kit). Your output is a **clear communication document** — release note, team brief, or README section — not code changes unless explicitly asked.

## Read first

1. `.okf/index.md`
2. `.okf/project.md`
3. `.okf/log.md` — entries from 2026-06-27 (shared skills, dispatch, Perplexity, research, gap closure)
4. `.okf/improvements/2026-06-27-perplexity-research-lessons.md`
5. `docs/shared-okf-skills.md`
6. `docs/configure-perplexity-okf.md`
7. `docs/perplexity-project-files-and-skills.md`
8. `docs/skill-frontmatter-compatibility.md`
9. `docs/okf-dispatch-orchestration.md`
10. `.okf/handoffs/README.md`
11. `.okf/context-packs/INDEX.md`

## Communicate these core facts

### Five-service setup order (plus overflow)

| Step | Service | Role |
|------|---------|------|
| 1 | Cursor | Scaffold; project-local OKF overlay (does not replace global Cursor skills) |
| 2 | Codex | Skills, hooks, builder/dispatch runner |
| 3 | Claude Code | Delivery agent, slash commands |
| 4 | Xcode | Apple-platform dispatch consumer |
| 5 | Perplexity Desktop Pro | Cited deep research → `.okf/references/` |

**Overflow (ad hoc):** Perplexity MODE B substitutes for a blocked primary runner. Cursor/Codex applies output. Not a sixth setup step.

### Canonical skills and thin adapters

- Canonical definitions: `skills/*/SKILL.md`
- Perplexity adapters: `skills/perplexity-okf-*/SKILL.md` (extended frontmatter: `applies_to`, `okf_mode`, `canonical_skill`)
- Generated adapters: `scripts/okf-sync-skills` → `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/okf.mdc`, `PERPLEXITY.md`
- Drift check: `scripts/okf-check-adapters`

### Perplexity configuration (three layers)

1. **Custom instructions** — `.okf/prompts/perplexity-custom-instructions.md`
2. **Project Files** — curated ~8–14 files (`docs/perplexity-project-files-and-skills.md`)
3. **Project Skills** — four `perplexity-okf-*` skills

Perplexity never writes the repo. Cursor/Codex ingests research and runs `scripts/okf-validate`.

### Handoffs vs context packs

- **Handoffs** (`.okf/handoffs/`) — active work transfer; see README + TEMPLATE
- **Context packs** (`.okf/context-packs/`) — ephemeral paste bundles, not source of truth

### Dispatch and overflow

- File-queue dispatch: `scripts/okf-dispatch` (roles: builder → tester → reviewer → integrator)
- Overflow on quota failure: `scripts/okf-dispatch overflow --packet-id <id> --reason usage_limit`

### Validation and safety

- `scripts/okf-validate` — bundle checks; draft References must stay `unverified`
- Research in `.okf/references/` is never accepted truth until reviewed
- No secrets in OKF

### New projects

- Scaffold: `skills/create-new-okf-project/scripts/create_okf_project.py`
- Copies bootstrap docs, handoff guides, Perplexity material, and scripts when run from bootstrap kit

## Output format

Produce a **team-facing brief** with:

1. **Executive summary** (5–8 sentences)
2. **What changed** (bullet list grouped by: services, Perplexity, skills/adapters, dispatch/overflow, validation)
3. **How to work day-to-day** (numbered workflow for Cursor, Codex, Claude, Xcode, Perplexity)
4. **Commands cheat sheet** (sync, validate, check-adapters, dispatch, overflow, handoff, context-pack)
5. **What not to do** (anti-patterns from research: over-attach files, promote unverified research, duplicate skill bodies in adapters)
6. **Open follow-ups** (if any remain after gap closure)

## Tone and audience

- Audience: engineers and agent operators using OKF-enabled repos
- Tone: practical, concise, no hype
- Do not claim Perplexity features not verified in OKF references
- Link to repo paths, not external URLs unless citing research references

## Constraints

- Do not modify repository files unless the user explicitly asks for a commit or doc edit
- Do not store secrets
- Prefer OKF concepts over chat-only summaries
```
