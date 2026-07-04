---
type: Workflow
title: Multi-Agent Delivery Pipeline
description: File-queue dispatch workflow for builder, tester, reviewer, and integrator roles across Codex, Claude Code, Cursor, Xcode-connected Claude Agent, and Perplexity overflow.
status: active
lifecycle_stage: build
owner: project
source_of_truth: true
resource: .okf/workflows/multi-agent-delivery-pipeline.md
tags: [okf, workflow, dispatch, multi-agent]
applies_to: [cursor, claude, codex, xcode-claude, perplexity, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T18:00:00+01:00
---

# Purpose

Coordinate multi-step delivery across agents using OKF dispatch queues instead of direct service-to-service calls.

# Applies To

Tasks that benefit from separated build, test, review, and integration roles across Codex, Claude Code, Cursor, or Xcode-connected Claude Agent, with Perplexity available only as manual overflow.

# Queue Contract

Work moves through `.okf/dispatch/`:

- `ready/` — typed JSON packets waiting for a runner
- `running/` — packets claimed by a runner
- `done/` — completed packets with optional result metadata
- `failed/` — failed packets with failure metadata
- `pipelines/` — pipeline manifests keyed by `pipeline_id`

Hooks enqueue work. Runners consume work. No agent invokes another agent directly.

# Roles

| Role | Responsibility |
|------|----------------|
| `builder` | Implement requested changes and link work to OKF concepts |
| `tester` | Execute tests, capture evidence, report failures |
| `reviewer` | Check implementation against requirements and risks |
| `integrator` | Finalize OKF updates, log entries, and handoffs |

Role order is fixed: `builder` → `tester` → `reviewer` → `integrator`.

# Runners

| Runner | Execution model |
|--------|-----------------|
| `codex` | `codex exec` via `scripts/okf-dispatch run --runner codex`; Codex `Stop` hook calls `scripts/okf-dispatch advance --from codex` |
| `claude` | `claude -p` via `scripts/okf-dispatch run --runner claude` |
| `cursor` | Project-local packet consumer; read packet JSON from the queue and complete manually |
| `xcode-claude` | Local packet consumer for Xcode-connected Claude Agent |

# Overflow runner (manual, not automated)

When a primary runner is blocked by usage limits, outage, or policy, **Perplexity Desktop Pro** may substitute for the same OKF role in overflow mode. Perplexity does not consume dispatch JSON directly.

| Overflow | Execution model |
|----------|-----------------|
| `perplexity-overflow` | Manual thread with MODE B; integrator (Cursor/Codex) applies deliverables and logs failover |

See `.okf/workflows/perplexity-overflow-failover.md` and `docs/configure-perplexity-okf.md`.

# Required Behaviour

1. Read `.okf/index.md`, `.okf/project.md`, and packet `context.okf_paths` before acting on a packet.
2. Claim work only through `scripts/okf-dispatch consume` or `scripts/okf-dispatch run`.
3. Mark completion with `scripts/okf-dispatch complete` or rely on hook-driven `advance` when appropriate.
4. Update affected OKF concepts and append to `.okf/log.md` after substantive changes.
5. Write a handoff when pausing before the pipeline completes.

# Prohibited Behaviour

- Do not call other agents or services directly to continue a pipeline step.
- Do not store secrets in dispatch packets or pipeline manifests.
- Do not treat queue files as durable source material; OKF concepts remain authoritative.

# Pre-Task Checklist

- Confirm queue state with `scripts/okf-dispatch status`.
- Identify the active `pipeline_id`, `packet_id`, and assigned role.
- Read the workflow doc at `docs/okf-dispatch-orchestration.md` when operating the dispatcher manually.

# Post-Task Checklist

- Move the packet to `done/` or `failed/` through dispatch commands.
- Update OKF concepts touched by the role.
- Append to `.okf/log.md`.
- Run `scripts/okf-validate` when OKF concepts changed.

# Escalation Conditions

Escalate to the user when a packet fails, a pipeline stalls in `running/`, or requested work conflicts with accepted OKF requirements.

# Related Material

- Orchestration guide: `docs/okf-dispatch-orchestration.md`
- Dispatcher script: `scripts/okf-dispatch`
- Codex hook: `.codex/hooks.json`
- Agent lifecycle: `.okf/workflows/agent-okf-lifecycle.md`
- Perplexity overflow: `.okf/workflows/perplexity-overflow-failover.md`
