---
type: Reference
title: Perplexity Overflow Failover Prompt
description: Copy-paste prompt for Perplexity when substituting for a blocked primary OKF dispatch runner.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/prompts/perplexity-overflow-failover.md
tags: [okf, prompt, perplexity, overflow, failover]
applies_to: [perplexity, cursor, codex, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T21:00:00+01:00
---

# Purpose

Use when a primary runner (Codex, Claude Code, Cursor, Xcode) cannot continue and Perplexity must complete the **same OKF role contract** in overflow mode.

Workflow: `.okf/workflows/perplexity-overflow-failover.md`

# Prompt template

Replace `{{PLACEHOLDERS}}` before sending. Attach or paste the overflow handoff and context pack.

```markdown
MODE B — OVERFLOW

You are substituting for a blocked OKF primary runner. You are NOT service 5 research mode unless the role is explicitly research.

## Failover context

- **Project name:** {{PROJECT_NAME}}
- **Primary runner blocked:** {{PRIMARY_RUNNER}} (codex | claude | cursor | xcode-claude)
- **Failover reason:** {{FAILOVER_REASON}} (usage_limit | outage | policy | user_choice)
- **OKF role to complete:** {{ROLE}} (builder | tester | reviewer | integrator)
- **Pipeline / packet ID (if any):** {{PIPELINE_ID}} / {{PACKET_ID}}
- **Preferred model:** {{MODEL}} (best | sonar-2 | gpt-5.4 | gemini-3.1-pro | claude-sonnet-4.6 | kimi-k2.6 | nemotron-3-super)

## OKF context paths (read these)

{{OKF_CONTEXT_PATHS}}

## Acceptance criteria

{{ACCEPTANCE_CRITERIA}}

## Work completed so far

{{COMPLETED_WORK_SUMMARY}}

## Your deliverable

Produce the output the blocked {{PRIMARY_RUNNER}} {{ROLE}} would have produced:

- **builder:** implementation plan, file-level changes, draft patches or code blocks, OKF concept update drafts
- **tester:** test plan, commands to run, expected results; interpret pasted test output if provided
- **reviewer:** structured review vs OKF requirements/risks, blocking issues, suggested fixes
- **integrator:** OKF update drafts, `.okf/log.md` entry draft, handoff for next runner

Rules:
- Do not claim changes were applied to the repository.
- Do not advance dispatch queues.
- Do not promote unverified research to accepted requirements.
- Link work to OKF concepts by path.
- No secrets.

## Required closing sections

### Routing note

(Which subtasks were search-heavy vs reasoning-heavy; which model behavior you used.)

### Overflow completion block

- Role completed:
- Primary runner blocked:
- Overflow model used:
- Files / concepts to update:
- Commands for integrator (Cursor/Codex):
- Validation needed:
- Resume primary runner when:
```

# Minimal invocation

```text
MODE B — OVERFLOW. Primary runner {{PRIMARY_RUNNER}} blocked ({{FAILOVER_REASON}}). Complete {{ROLE}} role per attached handoff and acceptance criteria. Output deliverable for Cursor/Codex to apply; do not claim repo changes.
```
