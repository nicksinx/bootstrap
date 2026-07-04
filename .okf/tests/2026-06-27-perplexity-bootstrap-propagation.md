---
type: Test Evidence
title: Perplexity Bootstrap Propagation Validation
description: Validation evidence for propagating Perplexity and Xcode operating model material into the OKF bootstrap scaffold.
status: active
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/tests/2026-06-27-perplexity-bootstrap-propagation.md
tags: [okf, test-evidence, scaffold, perplexity, xcode]
applies_to: [cursor, claude, codex, xcode-claude, perplexity, local-agent]
sensitivity: internal
verification_status: tested
timestamp: 2026-06-27T22:45:00+01:00
---

# Test Objective

Confirm that Project-1 and newly generated OKF scaffolds include Perplexity service 5, Perplexity overflow, Xcode service 4, and the Perplexity adapter target.

# Commands Run

```bash
PYTHONPYCACHEPREFIX=/private/tmp/okf-pycache python3 -m py_compile skills/create-new-okf-project/scripts/create_okf_project.py scripts/okf-sync-skills
python3 skills/create-new-okf-project/scripts/create_okf_project.py /private/tmp/okf-scaffold-smoke-20260627-final --name "Smoke OKF Project" --owner smoke-test
scripts/okf-validate
scripts/okf-sync-skills
scripts/okf-sync-skills --target perplexity --dry-run
```

# Results

- Python compile passed after redirecting bytecode cache to `/private/tmp/okf-pycache`.
- Smoke scaffold wrote 66 files.
- Smoke scaffold validation passed with 0 warnings.
- Smoke scaffold `okf-sync-skills --target perplexity --dry-run` reported 13 skills and would write `PERPLEXITY.md`.
- Smoke scaffold generated `scripts/okf-sync-skills` with five-service wording and Perplexity Project Files/Project Skills instructions.
- Project-1 `scripts/okf-validate` passed with 0 warnings.
- Project-1 `scripts/okf-sync-skills` refreshed all adapter targets from 13 skills.
- Project-1 `scripts/okf-sync-skills --target perplexity --dry-run` reported 13 skills and would write `PERPLEXITY.md`.

# Evidence Files Checked

- `PERPLEXITY.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.cursor/rules/okf.mdc`
- `.okf/agents/future-service.md`
- `docs/configure-perplexity-okf.md`
- `docs/create-new-okf-project-in-perplexity.md`
- `docs/create-new-okf-project-in-xcode.md`
- `docs/create-new-okf-project-in-cursor.md`
- `docs/create-new-okf-project-in-codex.md`
- `docs/create-new-okf-project-in-claude.md`
- `docs/okf-dispatch-orchestration.md`
- `scripts/okf-dispatch`
- `.codex/hooks.json`
- `.okf/agents/xcode-claude.md`
- `.okf/agents/perplexity.md`
- `.okf/agents/perplexity-overflow.md`
- `.okf/prompts/perplexity-custom-instructions.md`
- `.okf/workflows/perplexity-research-cycle.md`
- `.okf/workflows/perplexity-overflow-failover.md`
- `skills/perplexity-okf-*/SKILL.md`

# Notes

`Project-1` is not a git repository in this workspace, so no branch commit/status validation was possible.
