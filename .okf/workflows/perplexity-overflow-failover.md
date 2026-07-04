---
type: Workflow
title: Perplexity Overflow Failover
description: Ad hoc workflow when Perplexity substitutes for a blocked primary OKF dispatch runner.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/workflows/perplexity-overflow-failover.md
tags: [okf, workflow, perplexity, overflow, failover, dispatch]
applies_to: [perplexity, cursor, codex, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T21:00:00+01:00
---

# Purpose

Continue OKF delivery when a **primary runner** (Codex, Claude Code, Cursor, Xcode) is blocked, without changing the canonical five-service setup order. Perplexity acts as an **overflow executor** for the same role contract—not as a permanent replacement.

# Applies To

Mid-pipeline stalls caused by usage limits, outages, policy blocks, or explicit user failover. Not for planned service 5 research (use `.okf/workflows/perplexity-research-cycle.md` instead).

# Failover Triggers

- Usage limit or quota exhausted on primary runner
- Service outage or unavailability
- Policy block on primary runner
- User explicitly requests Perplexity overflow
- Context too large for primary runner (optional; prefer context pack trimming first)

# Required Behaviour

1. **Pause** the active packet or note the stalled role; do not silently switch runners in dispatch metadata without logging.
2. **Write overflow handoff** under `.okf/handoffs/` with:
   - `primary_runner`, `overflow_runner: perplexity-overflow`
   - `failover_reason`, `role`, `acceptance_criteria`
   - `context.okf_paths`, packet/pipeline IDs if applicable
3. **Build overflow context pack** for Perplexity (handoff + requirements + file summaries + test output if tester role).
4. **Perplexity thread:** first message `MODE B — OVERFLOW`; paste `.okf/prompts/perplexity-overflow-failover.md`.
5. **Integrator (Cursor or Codex):** apply deliverables, run validation/tests, update OKF, append `.okf/log.md`.
6. **Resume primary runner** when quota or service is restored; reference overflow handoff in next packet or handoff.

# Prohibited Behaviour

- Do not let Perplexity advance dispatch queues or run hooks directly.
- Do not treat overflow output as applied without integrator confirmation.
- Do not auto-promote overflow drafts to accepted OKF decisions.
- Do not fail over silently—every overflow event must appear in `.okf/log.md` and a handoff.

# Role suitability

| Role | Overflow fit | Integrator must |
|------|--------------|-----------------|
| Reviewer | Strong | Apply review findings or open follow-up packets |
| Integrator | Good | Apply OKF/log/handoff drafts |
| Builder | Partial | Apply patches, run build/tests |
| Tester | Low | Run tests locally; paste results to Perplexity only if needed |

# Packet metadata (recommended)

When documenting overflow in dispatch notes or handoffs, include:

```yaml
execution_mode: overflow
primary_runner: codex
overflow_runner: perplexity-overflow
failover_reason: usage_limit
role: reviewer
overflow_model_used: best
```

Automated dispatch fields may be added in a later iteration; handoffs are authoritative for MVP. Record overflow on a blocked packet with:

```bash
scripts/okf-dispatch overflow --packet-id <id> --reason usage_limit --primary-runner codex
```

# Pre-Task Checklist

- Confirm primary runner is actually blocked.
- Identify role and acceptance criteria from packet or handoff.
- Perplexity custom instructions include MODE B (see `.okf/prompts/perplexity-custom-instructions.md`).

# Post-Task Checklist

- Integrator applied deliverables and ran validation.
- `.okf/log.md` records failover event.
- Pipeline resumed or new handoff written for primary runner.
- `scripts/okf-validate` passes if OKF concepts changed.

# Related Material

- Setup: `docs/configure-perplexity-okf.md`
- Prompt: `.okf/prompts/perplexity-overflow-failover.md`
- Agent rule: `.okf/agents/perplexity-overflow.md`
- Dispatch workflow: `.okf/workflows/multi-agent-delivery-pipeline.md`
- Handoff skill: `skills/okf-handoff-writer/SKILL.md`
