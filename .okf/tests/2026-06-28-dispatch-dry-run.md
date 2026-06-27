---
type: Test Evidence
title: Dispatch Dry Run — Wave 2 Ergonomics
description: Live dry run of init-pipeline, tester flow, overflow metadata stub, and full pipeline completion for dispatch ergonomics validation.
status: active
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/tests/2026-06-28-dispatch-dry-run.md
tags: [okf, test-evidence, dispatch, ergonomics, tester, overflow]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: tested
timestamp: 2026-06-28T22:58:00+02:00
---

# Test Objective

Validate the full dispatch ergonomics cycle live: `init-pipeline`, builder advance, tester packet shape and overflow metadata, reviewer and integrator completion, and final pipeline close. Confirm overflow JSON structure and auto-generated handoff stub match expected schema before documenting them in `TEMPLATE-tester.md`, `TEMPLATE-reviewer.md`, and `docs/okf-dispatch-orchestration.md`.

# Change Under Test

- New role-specific templates: `TEMPLATE-tester.md`, `TEMPLATE-reviewer.md`
- Updated `README.md` with template selection guidance
- Pending: ~~dispatch orchestration doc update with tester/reviewer handoff expectations~~ — done in Wave 2 (see `docs/okf-dispatch-orchestration.md` § Role handoff expectations)

# Commands Run

## 1. Init pipeline

```bash
python3 scripts/okf-dispatch init-pipeline \
  "Dispatch dry run — Wave 2 ergonomics test" \
  --runners builder:codex,tester:claude,reviewer:cursor,integrator:codex
```

Output:

```
.okf/dispatch/ready/2026-06-27T2257390200-builder-a30beb9c.json
pipeline_id=pipe-cb8dc04e packet_id=builder-a30beb9c role=builder runner=codex
```

## 2. Initial status

```bash
python3 scripts/okf-dispatch status --verbose
```

```
OKF dispatch queues:
  ready: 1  running: 0  done: 0  failed: 0

Pipelines:
  pipe-cb8dc04e status=active current_role=builder current_packet=builder-a30beb9c
  [ready] builder-a30beb9c role=builder runner=codex pipeline=pipe-cb8dc04e
```

## 3. Tester packet (after builder complete)

```bash
python3 scripts/okf-dispatch complete --packet-id builder-a30beb9c --from codex
python3 scripts/okf-dispatch show --packet-id tester-ece3c5a5
```

Tester packet (abbreviated):

```json
{
  "packet_id": "tester-ece3c5a5",
  "pipeline_id": "pipe-cb8dc04e",
  "role": "tester",
  "runner": "claude",
  "status": "ready",
  "source": "pipeline",
  "prompt": "You are the tester in an OKF multi-agent delivery pipeline.\nPipeline: pipe-cb8dc04e\n\nTask summary:\nDispatch dry run — Wave 2 ergonomics test\n\nRead these OKF concepts first:\n- .okf/index.md\n- .okf/project.md\n\nFollow the workflow in `.okf/workflows/multi-agent-delivery-pipeline.md`.\nDo not call other agents directly; update OKF and let dispatch enqueue the next role.\nWhen finished, run: scripts/okf-dispatch complete --packet-id <id> --from claude",
  "context": { "okf_paths": [".okf/index.md", ".okf/project.md"], "overflow": null },
  "depends_on": [],
  "result": null
}
```

Observation: `prompt` includes explicit `--from claude` completion instruction; `context.overflow` is `null` by default.

## 4. Overflow metadata stub (tester blocked)

```bash
python3 scripts/okf-dispatch overflow \
  --packet-id tester-ece3c5a5 \
  --reason usage_limit \
  --primary-runner claude
```

```json
{
  "packet_id": "tester-ece3c5a5",
  "queue": "ready",
  "path": ".okf/dispatch/ready/2026-06-27T2258040200-tester-ece3c5a5.json",
  "overflow": {
    "execution_mode": "overflow",
    "primary_runner": "claude",
    "overflow_runner": "perplexity-overflow",
    "failover_reason": "usage_limit",
    "role": "tester",
    "overflow_at": "2026-06-27T22:58:20+02:00",
    "overflow_model_used": "best"
  },
  "handoff": ".okf/handoffs/2026-06-27-overflow-tester-ece3c5a5.md",
  "next_steps": [
    "Start Perplexity MODE B — OVERFLOW",
    "Use .okf/prompts/perplexity-overflow-failover.md",
    "Integrator applies deliverable and runs scripts/okf-validate"
  ]
}
```

Auto-generated overflow handoff stub: `.okf/handoffs/2026-06-27-overflow-tester-ece3c5a5.md`

The stub includes: blocked packet ID and pipeline, failover reason, overflow runner assignment, next steps for Perplexity MODE B, and the raw overflow JSON block.

## 5. Tester complete → reviewer → integrator

```bash
python3 scripts/okf-dispatch complete --packet-id tester-ece3c5a5 --from claude
python3 scripts/okf-dispatch complete --packet-id reviewer-29990410 --from cursor
python3 scripts/okf-dispatch complete --packet-id integrator-a4a1fb4d --from codex
```

Final status:

```
OKF dispatch queues:
  ready: 0  running: 0  done: 4  failed: 0

Pipelines:
  pipe-cb8dc04e status=complete current_role=integrator current_packet=integrator-a4a1fb4d
```

# Results

| Check | Result |
|-------|--------|
| `init-pipeline` creates builder packet in ready queue | PASS |
| Builder → tester advance enqueues correct runner (`claude`) | PASS |
| Tester packet prompt includes `--from claude` completion instruction | PASS |
| `overflow` command writes `context.overflow` metadata to packet JSON | PASS |
| `overflow` command auto-generates handoff stub with correct fields | PASS |
| Overflow stub `next_steps` correctly names Perplexity MODE B | PASS |
| Tester complete → reviewer enqueued for `cursor` | PASS |
| Reviewer complete → integrator enqueued for `codex` | PASS |
| Integrator complete → pipeline `status=complete` | PASS |
| `scripts/okf-validate` after test run | 0 warnings |
| `scripts/okf-check-adapters` | 13 skills, pass |

# Expected Result

Full four-role pipeline cycle operates cleanly. Overflow metadata populates `context.overflow` in the live packet JSON and writes a usable handoff stub. The auto-generated stub is sufficient for Perplexity MODE B context without requiring manual handoff creation.

# Verdict

**PASS** — all dispatch ergonomics checks pass. Tester and reviewer packet prompts, overflow metadata schema, and stub handoff structure are confirmed and usable as reference for `TEMPLATE-tester.md`, `TEMPLATE-reviewer.md`, and the dispatch orchestration doc update.

# Follow-Up

- Dispatch orchestration doc: add tester/reviewer handoff expectations section (this session)
- Dispatch queue contains only `done/` state from this run — no cleanup required
- Overflow stub `.okf/handoffs/2026-06-27-overflow-tester-ece3c5a5.md` retained as reference for the overflow template pattern
