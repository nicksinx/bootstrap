---
type: Agent Rule
title: Perplexity Overflow OKF Agent Rule
description: Perplexity Desktop Pro rules for ad hoc overflow substitution when primary OKF runners are blocked.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/agents/perplexity-overflow.md
tags: [okf, perplexity, overflow, agent-rule, failover]
applies_to: [perplexity]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T21:00:00+01:00
---

# Purpose

Allow Perplexity to **substitute for a blocked primary runner** (Codex, Claude Code, Cursor, Xcode) while preserving the same OKF **role contract** (builder, tester, reviewer, integrator). This is an ad hoc sixth layer—not a change to the canonical five-service setup order.

Planned deep research remains service 5; see `.okf/agents/perplexity.md`.

# Applies To

Perplexity Desktop Pro threads opened with **MODE B — OVERFLOW** when usage limits, outages, policy blocks, or user choice prevent the assigned primary runner from continuing.

# Required Behaviour

- Use custom instructions that include MODE B from `.okf/prompts/perplexity-custom-instructions.md`.
- Read the overflow handoff and packet summary before acting.
- Complete the **same role deliverable** the blocked runner would have produced.
- Record `primary_runner`, `failover_reason`, `role`, and `overflow_model_used` in the closing Overflow completion block.
- Leave application of repo changes and dispatch advancement to **Cursor or Codex** (integrator).

# Prohibited Behaviour

- Do not advance dispatch queues or execute repo hooks from Perplexity.
- Do not claim deliverables were applied without integrator confirmation.
- Do not replace Xcode for Apple-specific build/sign when Xcode is available unless explicitly blocked.
- Do not promote overflow output to accepted OKF truth without review and validation.
- Do not fail over silently—every event must appear in `.okf/log.md` and a handoff.

# Role suitability

| Role | Fit |
|------|-----|
| Reviewer | Strong |
| Integrator | Good |
| Builder | Partial (drafts only) |
| Tester | Low (plans and interpretation only) |

# Pre-Task Checklist

- Confirm primary runner is blocked and role is identified.
- Write or read overflow handoff under `.okf/handoffs/`.
- Build overflow context pack from OKF paths and acceptance criteria.

# Post-Task Checklist

- Integrator applies deliverables and runs validation.
- Append failover entry to `.okf/log.md`.
- Resume primary runner when available; link overflow handoff in next continuity note.

# Escalation Conditions

Escalate when overflow cannot meet acceptance criteria, conflicts with accepted OKF scope, or requires secrets or live repo access Perplexity cannot safely handle.

# Related Material

- Configuration: `docs/configure-perplexity-okf.md`
- Workflow: `.okf/workflows/perplexity-overflow-failover.md`
- Prompt: `.okf/prompts/perplexity-overflow-failover.md`
- Research service 5: `.okf/agents/perplexity.md`
- Dispatch: `.okf/workflows/multi-agent-delivery-pipeline.md`
