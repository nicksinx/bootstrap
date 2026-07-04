---
type: Handoff
title: Overflow tester — tester-ece3c5a5
description: Overflow failover from claude to Perplexity for packet tester-ece3c5a5.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/handoffs/2026-06-27-overflow-tester-ece3c5a5.md
tags: [okf, handoff, overflow, perplexity]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-27T22:58:20+02:00
---

# Current State

Packet `tester-ece3c5a5` (tester) blocked on runner `claude`. Overflow to Perplexity MODE B recommended.

Pipeline: `pipe-cb8dc04e`

# Completed Work

See packet prompt and OKF context paths before failover.

# Decisions Made

- Failover reason: usage_limit
- Overflow runner: perplexity-overflow
- Overflow model: best

# Files Changed

- Dispatch packet updated with `context.overflow` metadata

# Known Issues

Primary runner unavailable: usage_limit

# Next Recommended Actions

1. Open Perplexity with MODE B — OVERFLOW and `.okf/prompts/perplexity-overflow-failover.md`
2. Complete the same `tester` role deliverable
3. Cursor or Codex applies output, updates OKF, appends `.okf/log.md`
4. Resume `claude` when available

# Validation Needed

- `scripts/okf-validate` after OKF updates
- Confirm packet completion or failure after integrator applies overflow output

# Context Pack

- Packet id: `tester-ece3c5a5`
- Queue: `ready`
- OKF paths: ['.okf/index.md', '.okf/project.md']

## Overflow metadata

```json
{
  "execution_mode": "overflow",
  "primary_runner": "claude",
  "overflow_runner": "perplexity-overflow",
  "failover_reason": "usage_limit",
  "role": "tester",
  "overflow_at": "2026-06-27T22:58:20+02:00",
  "overflow_model_used": "best"
}
```
