---
type: Test Evidence
title: Scaffold Parity Validation (Wave 1)
description: Full-kit vs sparse-path smoke evidence for create_okf_project.py BOOTSTRAP_COPY_PATHS and stub replacement.
status: active
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/tests/2026-06-28-scaffold-parity.md
tags: [okf, test-evidence, scaffold, bootstrap, parity]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: tested
timestamp: 2026-06-28T15:00:00+02:00
---

# Test Objective

Confirm that `create_okf_project.py` copies the full five-service bootstrap doc set when run from the Project-1 kit path, replaces embedded stubs with canonical files, and degrades predictably on a sparse/minimal script-only tree.

# Change Under Test

- Added `BOOTSTRAP_COPY_PATHS` constant in `create_okf_project.py`
- Extended copy list: operator brief, full xcode/perplexity/configure-perplexity guides, smoke-test prompt
- Bootstrap copies use `overwrite=True` so canonical kit docs replace embedded stubs

# Commands Run

```bash
cd /Users/dv/Projects/testrunner/Project-1
python3 -m py_compile skills/create-new-okf-project/scripts/create_okf_project.py

# Full kit path (script inside Project-1 layout)
python3 skills/create-new-okf-project/scripts/create_okf_project.py \
  /private/tmp/okf-scaffold-full-20260628 --name "Full Kit Smoke" --owner smoke-test

# Sparse path (script only, no bootstrap siblings)
mkdir -p /private/tmp/okf-sparse-kit-20260628/skills/create-new-okf-project/scripts
cp skills/create-new-okf-project/scripts/create_okf_project.py \
  /private/tmp/okf-sparse-kit-20260628/skills/create-new-okf-project/scripts/
python3 /private/tmp/okf-sparse-kit-20260628/skills/create-new-okf-project/scripts/create_okf_project.py \
  /private/tmp/okf-scaffold-sparse-20260628 --name "Sparse Smoke" --owner smoke-test

# Validation (full)
cd /private/tmp/okf-scaffold-full-20260628
scripts/okf-validate
scripts/okf-sync-skills
scripts/okf-check-adapters
scripts/okf-sync-skills --target perplexity --dry-run

# Validation (sparse)
cd /private/tmp/okf-scaffold-sparse-20260628
scripts/okf-validate
```

# Results

## File counts

| Path | Files written (script output) | Files on disk |
|------|------------------------------|---------------|
| Full kit | 77 | 74 |
| Sparse | 35 | 35 |

## Key path byte sizes (full vs sparse)

| Path | Full kit | Sparse |
|------|----------|--------|
| `docs/okf-ways-of-working-brief.md` | 12 748 | missing |
| `docs/configure-perplexity-okf.md` | 7 008 (canonical) | 1 094 (embedded stub) |
| `docs/create-new-okf-project-in-xcode.md` | 1 843 (canonical) | 660 (embedded stub) |
| `docs/create-new-okf-project-in-perplexity.md` | 9 280 (canonical) | 849 (embedded stub) |
| `docs/create-new-okf-project-in-claude.md` | 16 693 | missing |
| `scripts/okf-dispatch` | 24 692 | missing |
| `scripts/okf-check-adapters` | 2 866 | missing |
| `.okf/prompts/perplexity-post-curation-smoke-test.md` | 5 039 | missing |

Full-kit sizes match Project-1 bootstrap sources for the paths checked.

## Full-kit-only paths (39 files vs sparse)

Bootstrap copy set present only on full path includes:

- All bundled `skills/` trees (sparse has no sibling skill folders under `skills/`)
- `docs/okf-ways-of-working-brief.md`, all five setup guides (cursor/codex/claude), dispatch orchestration, Perplexity files guide, skill frontmatter doc
- `scripts/okf-dispatch`, `scripts/okf-check-adapters`
- `.okf/handoffs/README.md`, `TEMPLATE.md`, `.okf/context-packs/INDEX.md`
- `.okf/prompts/perplexity-post-curation-smoke-test.md`
- `.codex/hooks.json`, `CODEX-SKILL-INSTALL.md`, `.okf/agents/future-service.md`

## Validation

| Check | Full kit | Sparse |
|-------|----------|--------|
| `scripts/okf-validate` | 0 warnings | 0 warnings |
| `scripts/okf-check-adapters` (after sync) | pass, 13 skills | N/A (script not copied) |
| `scripts/okf-sync-skills --target perplexity --dry-run` | 13 skills | N/A |

Pre-sync adapter check on full kit correctly warned about missing skill index entries until `okf-sync-skills` ran.

# Expected Result

Full kit produces canonical five-service docs and operator brief; sparse produces embedded stubs and core scaffold only.

# Verdict

**PASS** — full-kit scaffold matches bootstrap repo for audited paths; sparse degradation is documented and predictable.

# Follow-Up

- Claude: verify evidence and close Wave 1 handoff
- Wave 2: dispatch ergonomics (independent)
