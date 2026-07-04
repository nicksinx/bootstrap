---
type: Agent Rule
title: Xcode Claude OKF Agent Rule
description: Rules for Xcode-connected Claude Agent as service 4 in the OKF setup sequence.
status: draft
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/agents/xcode-claude.md
tags: [okf, xcode, claude, agent-rule, dispatch]
applies_to: [xcode-claude]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-28T16:00:00+02:00
---

# Purpose

Define the Xcode-connected Claude Agent role for Apple-platform delivery in the five-service OKF setup order (service 4, before Perplexity service 5).

**This rule remains `draft` / `unverified` until live build and test evidence exists.** Dry repo verification alone is insufficient — see `.okf/prompts/xcode-step4-verification-checklist.md` and `.okf/risks/xcode-live-verification-pending.md`.

# Applies To

- Service 4 setup in new OKF projects
- Local Xcode work where build, test, simulator, signing, package, or platform integration context matters
- Dispatch packets assigned to runner `xcode-claude`

# Required Behaviour

## Before acting

1. Read `.okf/index.md`, `.okf/project.md`, and the latest handoff (especially Claude Code → Xcode).
2. Read `docs/okf-ways-of-working-brief.md` and `docs/create-new-okf-project-in-xcode.md`.
3. Read active requirements and relevant `.okf/tests/` evidence when continuing prior work.

## Dispatch consumption

When multi-agent delivery is enabled:

1. List ready work: `scripts/okf-dispatch status --verbose`
2. Consume next packet: `scripts/okf-dispatch consume --runner xcode-claude --json`
3. Read `context.okf_paths` and the packet `prompt` before implementing.
4. Execute the assigned **role** (builder, tester, reviewer, or integrator) — do not substitute another service's role.
5. Capture build/test evidence under `.okf/tests/` or the active handoff (command summaries, pass/fail, simulator notes — no secrets).
6. Complete: `scripts/okf-dispatch complete --packet-id <id> --from xcode-claude`

There is **no automatic hook**. Dispatch advancement is explicit during the session.

## Evidence and handoffs

- Record validation command output when OKF concepts change.
- Append material changes to `.okf/log.md`.
- Write a step 4 → step 5 handoff when Xcode setup pauses or completes (use `.okf/handoffs/TEMPLATE-xcode-step4.md`).
- Hand off to Perplexity service 5 for cited research — do not perform MODE A research inline unless overflow is explicitly invoked.

## Secrets

- Keep signing identities, provisioning profiles, API keys, and machine credentials **out of OKF**.
- Reference secret **locations** (e.g. Keychain, Xcode signing settings) without values.

# Prohibited Behaviour

- Do not promote this agent rule to `active` / `reviewed` without live Xcode build/test evidence.
- Do not replace Perplexity research (MODE A) or overflow (MODE B) roles.
- Do not advance Perplexity work or configure Perplexity Spaces during step 4.
- Do not modify `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/okf.mdc`, or `.codex/hooks.json` out of service order.
- Do not invoke Codex, Claude Code, or Cursor directly — use dispatch and OKF handoffs.
- Do not store secrets or local-only credentials in OKF concepts.

# Default dispatch patterns

| Pattern | Typical role for `xcode-claude` |
|---------|--------------------------------|
| Apple implementation-heavy | `builder` |
| Build/test evidence from Xcode | `tester` |
| OKF-only / non-Apple bootstrap | Not in default pipeline |

Override at pipeline init via `--runners`. Document the chosen map in the step 4 handoff.

# Related Material

- Setup guide: `docs/create-new-okf-project-in-xcode.md`
- Dry verification: `.okf/prompts/xcode-step4-verification-checklist.md`
- Dispatch workflow: `.okf/workflows/multi-agent-delivery-pipeline.md`
- Orchestration: `docs/okf-dispatch-orchestration.md`
- Perplexity step 5: `docs/create-new-okf-project-in-perplexity.md`
- Live verification risk: `.okf/risks/xcode-live-verification-pending.md`
