---
name: perplexity-okf-reader
description: Load and triage OKF project context in Perplexity Desktop Pro before research or overflow work. Use when Perplexity needs to read attached project files, .okf/index.md, .okf/project.md, handoffs, and decide what context is safe to use for MODE A research or MODE B overflow.
applies_to: [perplexity]
okf_mode: [research, overflow]
canonical_skill: skills/okf-reader/SKILL.md
---

# Perplexity OKF Reader

Use this skill at the start of every Perplexity thread on an OKF-enabled project.

## When to use

- User opens a Perplexity Project with OKF files attached.
- User says `MODE A — RESEARCH` or `MODE B — OVERFLOW`.
- User asks what is safe to implement, cite, or continue from current project state.

## Workflow

1. Read attached project files in this order when present:
   - `.okf/project.md`
   - `.okf/index.md`
   - Latest `.okf/handoffs/` note
   - Active requirement, spec, or overflow handoff for the task
2. Identify the active OKF mode (research vs overflow) from the user's first message or custom instructions.
3. Prefer concepts with `verification_status: reviewed`, `tested`, or `accepted`.
4. Treat `deprecated`, `superseded`, and `archived` concepts as unsafe unless the user asks for historical analysis.
5. Report only task-relevant facts:
   - Active requirements and acceptance criteria
   - Decisions and architecture constraints
   - Risks and safety limits
   - Recent handoff notes
   - Gaps or unverified concepts that affect the task

## Perplexity-specific rules

- Perplexity does not have direct repo access; rely on Project **Files** and pasted context packs.
- Do not invent project requirements not represented in attached OKF material.
- Do not store secrets or credentials in summaries.
- **Do not use Forge MCP** — lifecycle planning is Cursor-only; research stays MODE A → `.okf/references/`; overflow is MODE B substitute delivery only.
- For full OKF reader contract, see `skills/okf-reader/SKILL.md`.

## Output

End triage with a short **Context summary** listing:

- Mode (research or overflow)
- Safe-to-use concepts
- Concepts that must stay `unverified`
- Missing context the user should attach or paste
