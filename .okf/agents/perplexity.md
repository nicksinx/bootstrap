---
type: Agent Rule
title: Perplexity OKF Agent Rule
description: Perplexity Desktop Pro rules for OKF service 5 deep research and cited reference production.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/agents/perplexity.md
tags: [okf, perplexity, agent-rule, deep-research, references]
applies_to: [perplexity]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T21:00:00+01:00
---

# Purpose

Make Perplexity the fifth configured service and the **deep research layer** for OKF projects, producing cited reference material without becoming accepted project truth until reviewed.

For **overflow substitution** when primary runners are blocked, see `.okf/agents/perplexity-overflow.md`.

# Applies To

Perplexity Desktop Pro research sessions (MODE A — RESEARCH). Runs after Cursor, Codex, Claude Code, and Xcode setup (steps 1–4) for new projects, or on demand during delivery. Outputs land in `.okf/references/` via copy-in from Cursor or Codex.

# Required Behaviour

- Configure custom instructions from `.okf/prompts/perplexity-custom-instructions.md`.
- Read `.okf/project.md`, primary requirements, and the step 4 handoff before researching.
- Follow `skills/okf-citation-steward/SKILL.md` for all external claims.
- Produce `Reference` concepts with URLs, retrieval dates, summaries, and limitations.
- Set `verification_status: unverified` on all Perplexity-sourced concepts.
- Set `source_of_truth: false` on reference concepts until promoted through review.
- Deliver a gap analysis and handoff block after each research cycle.
- Prefer **Best** for mixed research packs; use **Sonar 2** when citation retrieval dominates.

# Prohibited Behaviour

- Do not invent citations or treat search snippets as verified fact.
- Do not overwrite accepted OKF requirements, decisions, or architecture directly.
- Do not store secrets, credentials, or confidential third-party material in OKF.
- Do not set `verification_status` to `reviewed`, `tested`, or `accepted` without human or build-agent review.
- Do not use Perplexity overflow mode for planned research (use overflow agent rule instead).

# Pre-Task Checklist

- Confirm steps 1–4 are complete for new-project setup.
- Custom instructions pasted in Perplexity Desktop.
- Paste project brief and research topics using `docs/create-new-okf-project-in-perplexity.md` or `docs/configure-perplexity-okf.md`.
- Identify which requirements or risks the research should inform.

# Post-Task Checklist

- Save references under `.okf/references/` (via Cursor/Codex).
- Update `.okf/index.md` and append to `.okf/log.md`.
- Run `scripts/okf-validate`.
- Link references from draft requirements or risks without promoting unverified claims.

# Escalation Conditions

Escalate when sources conflict materially, compliance claims cannot be verified, or research contradicts accepted OKF scope.

# Related Material

- Configuration: `docs/configure-perplexity-okf.md`
- Setup guide: `docs/create-new-okf-project-in-perplexity.md`
- Workflow: `.okf/workflows/perplexity-research-cycle.md`
- Prompts: `.okf/prompts/perplexity-deep-research-setup.md`, `.okf/prompts/perplexity-custom-instructions.md`
- Thin adapter: `PERPLEXITY.md`
- Overflow: `.okf/agents/perplexity-overflow.md`
- Citation skill: `skills/okf-citation-steward/SKILL.md`
