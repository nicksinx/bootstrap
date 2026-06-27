---
type: Handoff
title: {{Task Title}} — Tester Handoff
description: {{One-sentence summary of what was tested and the verdict}}
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/handoffs/YYYY-MM-DD-tester-task-slug.md
tags: [okf, handoff, tester]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-28T12:00:00+00:00
---

Copy to `.okf/handoffs/YYYY-MM-DD-tester-<task-slug>.md`. Use when the `tester` role (default runner: `claude`) completes test work and hands off to the `reviewer` (default runner: `cursor`).

Replace `timestamp` and frontmatter placeholders before saving.

# Current State

- Pipeline: `{{pipeline_id}}` | Packet: `{{packet_id}}`
- Tester role complete: **yes** | **partial**
- Reviewer ready: **yes** | **blocked — see Known Issues**

# Completed Work

## Tests run

| Command | Result |
|---------|--------|
| `scripts/okf-validate` | PASS / FAIL / SKIP |
| `scripts/okf-check-adapters` | PASS / FAIL / SKIP |
| `{{other command}}` | PASS / FAIL / SKIP |

## Evidence captured

- Test evidence doc: `{{.okf/tests/YYYY-MM-DD-<slug>.md}}` or N/A
- Key finding: {{one-line verdict — e.g. "all checks pass", "2 failures in X"}}

# Decisions Made

- Test scope: {{what was in scope and what was explicitly not tested}}
- Evidence format: {{doc path or inline}}

# Files Changed

# Known Issues

- {{Failing tests, coverage gaps, or skipped areas requiring reviewer attention}}

# Next Recommended Actions (reviewer — cursor)

1. Read this handoff and `docs/okf-dispatch-orchestration.md`
2. Consume reviewer packet: `scripts/okf-dispatch consume --runner cursor`
3. Open packet JSON and follow the packet prompt
4. Review test evidence at `{{evidence path}}`
5. Check changes against `.okf/requirements/` and relevant `skills/*/SKILL.md`
6. Run `scripts/okf-validate` after any OKF updates
7. Complete packet: `scripts/okf-dispatch complete --packet-id {{packet_id}} --from cursor`
8. Write a reviewer handoff using `TEMPLATE-reviewer.md` before handing off to integrator

# Validation Needed

```bash
scripts/okf-validate
scripts/okf-check-adapters
```

# Context Pack

- `.okf/project.md`
- Active requirement: `{{path}}`
- Test evidence: `{{path}}`
- Packet context paths: `{{from packet context.okf_paths}}`

## Overflow fields (when applicable — tester blocked by usage limit or outage)

- **primary_runner:** claude
- **overflow_runner:** perplexity-overflow
- **failover_reason:** {{usage_limit | outage | policy | user_choice}}
- **role:** tester
- **overflow_model_used:** {{best | sonar | gemini}}
