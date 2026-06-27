---
type: Workflow
title: Perplexity Research Cycle
description: Standard workflow for Perplexity Desktop Pro as OKF service 5 deep research layer.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/workflows/perplexity-research-cycle.md
tags: [okf, workflow, perplexity, deep-research, references]
applies_to: [perplexity, cursor, codex, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T21:00:00+01:00
---

# Purpose

Run Perplexity Desktop Pro as the **planned deep research layer** (service 5), producing cited Reference material for `.okf/references/` without becoming accepted project truth until reviewed.

# Applies To

External evidence gathering after steps 1–4 (Cursor, Codex, Claude Code, Xcode) are complete, or ad hoc research rounds during delivery.

# Required Behaviour

1. Paste Perplexity custom instructions from `.okf/prompts/perplexity-custom-instructions.md` (once per Perplexity account or project).
2. Build context: `.okf/project.md`, relevant requirements, risks, and latest handoff.
3. Start thread with **MODE A — RESEARCH** or the step-5 prompt from `docs/create-new-okf-project-in-perplexity.md`.
4. Prefer **Best** for mixed research packs; use **Sonar 2** when citations and retrieval quality dominate.
5. Perplexity outputs draft Reference concepts with `verification_status: unverified`.
6. **Cursor or Codex** saves files under `.okf/references/`, updates index and log, runs `scripts/okf-validate`.
7. Link references from requirements, architecture, or risks without promoting unverified claims.

# Prohibited Behaviour

- Do not treat Perplexity chat as durable OKF state.
- Do not overwrite accepted OKF requirements or decisions from research alone.
- Do not store secrets in OKF or Perplexity threads.
- Do not use Perplexity Computer for this workflow unless a separate runner contract is added later.

# Pre-Task Checklist

- Confirm steps 1–4 complete for new-project setup, or identify the specific research question.
- Custom instructions configured in Perplexity Desktop.
- Context pack or key OKF paths prepared.

# Post-Task Checklist

- References saved under `.okf/references/`.
- `.okf/index.md` and `.okf/log.md` updated.
- Gap analysis captured in handoff or reference index.
- `scripts/okf-validate` passes.
- Activate `.okf/agents/perplexity.md` after first successful cycle.

# Model routing

| Research task | Suggested model |
|---------------|-----------------|
| Domain / vendor landscape | Sonar 2 or Best |
| Compliance / policy scan | Sonar 2 + primary-source follow-up |
| Deep multi-topic analysis | Gemini 3.1 Pro or Best |
| Mixed bootstrap pack (step 5) | Best |

Record Perplexity's Routing note in the handoff when useful for downstream agents.

# Related Material

- Setup: `docs/configure-perplexity-okf.md`
- Step 5 guide: `docs/create-new-okf-project-in-perplexity.md`
- Prompt: `.okf/prompts/perplexity-deep-research-setup.md`
- Agent rule: `.okf/agents/perplexity.md`
- Citation skill: `skills/okf-citation-steward/SKILL.md`
