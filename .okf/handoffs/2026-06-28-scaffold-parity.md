---
type: Handoff
title: Scaffold Parity — Wave 1 Complete
description: Cursor closed Wave 1 scaffold parity; Claude to verify test evidence and confirm full-kit vs sparse behavior.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/handoffs/2026-06-28-scaffold-parity.md
tags: [okf, handoff, scaffold, bootstrap, wave-1]
applies_to: [claude, cursor, codex]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-28T15:00:00+02:00
---

# Current State

Wave 1 (scaffold parity) implemented in Project-1. Full-kit scaffold now copies canonical five-service docs and replaces embedded stubs. Test evidence recorded.

# Completed Work

1. **Audit** — `copy_optional_bootstrap_files` was missing operator brief, full xcode/perplexity/configure-perplexity guides, and smoke-test prompt; embedded stubs were not replaced because copy ran after embed with `overwrite=False`.

2. **Fix** — Introduced `BOOTSTRAP_COPY_PATHS` in `create_okf_project.py`:
   - Added: `docs/okf-ways-of-working-brief.md`, `docs/create-new-okf-project-in-xcode.md`, `docs/create-new-okf-project-in-perplexity.md`, `docs/configure-perplexity-okf.md`, `.okf/prompts/perplexity-post-curation-smoke-test.md`
   - Bootstrap copies now use `overwrite=True` to replace embedded stubs

3. **Test evidence** — `.okf/tests/2026-06-28-scaffold-parity.md` (full: 77 written / 74 on disk; sparse: 35 files)

4. **Docs** — Updated `skills/create-new-okf-project/SKILL.md` (copy table, file count expectation) and `docs/okf-ways-of-working-brief.md` bootstrap section

# Decisions Made

- Keep embedded stubs in `service_operating_files` as sparse-path fallback; bootstrap kit copies win when sources exist
- Do not copy `.okf/prompts/perplexity-procurelex-research.md` into default scaffold (application-specific; deferred)

# Files Changed

- `skills/create-new-okf-project/scripts/create_okf_project.py`
- `skills/create-new-okf-project/SKILL.md`
- `docs/okf-ways-of-working-brief.md`
- `.okf/tests/2026-06-28-scaffold-parity.md` (new)
- `.okf/handoffs/2026-06-28-scaffold-parity.md` (this file)
- `.okf/log.md`

# Known Issues

- Sparse path copies no bundled skills when only the Python script is present (no sibling `skills/*/SKILL.md` trees) — expected; document for operators
- Pre-sync adapter drift warnings on fresh scaffold until `scripts/okf-sync-skills` runs — expected

# Next Recommended Actions (Claude — verify)

1. Read `.okf/tests/2026-06-28-scaffold-parity.md`
2. Optionally re-run full-kit smoke from Project-1 and confirm key file sizes
3. Run `scripts/okf-validate` and `scripts/okf-check-adapters` on Project-1
4. Append log line confirming verification
5. Proceed to **Wave 2: dispatch ergonomics** if operator approves

# Validation Needed

```bash
cd /Users/dv/Projects/testrunner/Project-1
scripts/okf-validate
scripts/okf-check-adapters
python3 -m py_compile skills/create-new-okf-project/scripts/create_okf_project.py
```

Project-1 baseline: validate and adapter-check should pass.

# Context Pack

- Prior handoff: `.okf/handoffs/2026-06-28-bootstrap-refinement-handoff.md`
- Refinement backlog Wave 2: dispatch ergonomics (tester/reviewer templates)
