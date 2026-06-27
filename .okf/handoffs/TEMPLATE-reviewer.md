---
type: Handoff
title: {{Task Title}} — Reviewer Handoff
description: {{One-sentence summary of review verdict and any critical findings}}
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/handoffs/YYYY-MM-DD-reviewer-task-slug.md
tags: [okf, handoff, reviewer]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-28T12:00:00+00:00
---

Copy to `.okf/handoffs/YYYY-MM-DD-reviewer-<task-slug>.md`. Use when the `reviewer` role (default runner: `cursor`) completes review and hands off to the `integrator` (default runner: `codex`).

Replace `timestamp` and frontmatter placeholders before saving.

# Current State

- Pipeline: `{{pipeline_id}}` | Packet: `{{packet_id}}`
- Reviewer role complete: **yes** | **partial**
- Reviewer verdict: **approved** | **approved with notes** | **blocked**
- Integrator ready: **yes** | **blocked — see Known Issues**

# Completed Work

## Requirements checked

| Requirement | Conforms | Notes |
|-------------|----------|-------|
| `{{.okf/requirements/…}}` | yes / no / N/A | {{brief note}} |
| `{{skills/*/SKILL.md contract}}` | yes / no / N/A | {{brief note}} |

## Findings

| # | Finding | Severity | Disposition |
|---|---------|----------|-------------|
| 1 | {{description}} | low / medium / high | accepted / must-fix / deferred |

No findings: replace table with "None."

# Decisions Made

- Reviewer verdict: **approved** | **approved with notes** | **blocked**
- Must-fix items before integration: {{none | list}}
- Deferred items (for improvement backlog): {{none | list}}

# Files Changed

# Known Issues

- {{Unresolved concerns blocking integration or requiring integrator attention}}

# Next Recommended Actions (integrator — codex)

1. Read this handoff and the tester handoff
2. Consume integrator packet: `scripts/okf-dispatch run --runner codex`
3. Apply any must-fix items flagged by the reviewer before merging
4. Merge outcomes, update OKF concepts, append `.okf/log.md`
5. Run `scripts/okf-validate` and `scripts/okf-check-adapters`
6. Complete packet: `scripts/okf-dispatch complete --packet-id {{packet_id}} --from codex`
7. Write final integration handoff or update `.okf/index.md` current handoff pointer

# Validation Needed

```bash
scripts/okf-validate
scripts/okf-check-adapters
```

# Context Pack

- `.okf/project.md`
- Active requirement: `{{path}}`
- Tester handoff: `{{path}}`
- Tester evidence: `{{path}}`
- Packet context paths: `{{from packet context.okf_paths}}`

## Overflow fields (when applicable — reviewer blocked by usage limit or outage)

- **primary_runner:** cursor
- **overflow_runner:** perplexity-overflow
- **failover_reason:** {{usage_limit | outage | policy | user_choice}}
- **role:** reviewer
- **overflow_model_used:** {{best | sonar | gemini}}
