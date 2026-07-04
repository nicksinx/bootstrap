---
type: Handoff
title: Perplexity Bootstrap Propagation
description: Handoff for propagating Perplexity integration and five-service setup lessons into the OKF bootstrap kit.
status: active
lifecycle_stage: build
owner: project
source_of_truth: true
resource: .okf/handoffs/2026-06-27-perplexity-bootstrap-propagation.md
tags: [okf, handoff, perplexity, scaffold, xcode]
applies_to: [cursor, claude, codex, xcode-claude, perplexity, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T22:45:00+01:00
---

# Current State

The bootstrap kit now propagates Perplexity service 5, Perplexity overflow behavior, Xcode service 4 setup material, and bundled OKF skills into newly generated OKF projects.

# Completed Work

- Updated `skills/create-new-okf-project/scripts/create_okf_project.py` to generate five-service scaffold content.
- Added default dispatch queue directories to the generated `.okf` structure.
- Added optional copying for bootstrap dispatcher/setup files such as `scripts/okf-dispatch`, `.codex/hooks.json`, and step 1-3 setup guides.
- Added `PERPLEXITY.md` generation and embedded `okf-sync-skills --target perplexity` support.
- Added bundled `skills/` copying by default, with `--no-skills` as an opt-out.
- Added Xcode setup guide and agent concept.
- Updated stale tool-adapter templates and shared-skills/Cursor setup documentation.
- Ran `scripts/okf-sync-skills` to refresh live adapters after the `create-new-okf-project` skill changed.
- Added validation evidence in `.okf/tests/2026-06-27-perplexity-bootstrap-propagation.md`.

# Decisions Made

- Perplexity remains service 5 for planned research and manual MODE B overflow for blocked primary runners.
- Perplexity Desktop Pro does not write the repository, run hooks, or advance dispatch queues.
- New scaffolds copy bundled skills when available instead of embedding stale skill bodies in the generator.
- Xcode service 4 is represented by `.okf/agents/xcode-claude.md` and `docs/create-new-okf-project-in-xcode.md`.

# Files Changed

- `.okf/agents/xcode-claude.md`
- `.okf/agents/future-service.md`
- `.okf/features/shared-okf-skills.md`
- `.okf/handoffs/2026-06-27-perplexity-bootstrap-propagation.md`
- `.okf/index.md`
- `.okf/log.md`
- `.okf/project.md`
- `.okf/tests/2026-06-27-perplexity-bootstrap-propagation.md`
- `.okf/workflows/multi-agent-delivery-pipeline.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.cursor/rules/okf.mdc`
- `PERPLEXITY.md`
- `docs/create-new-okf-project-in-cursor.md`
- `docs/create-new-okf-project-in-xcode.md`
- `docs/shared-okf-skills.md`
- `scripts/okf-sync-skills`
- `skills/create-new-okf-project/SKILL.md`
- `skills/create-new-okf-project/scripts/create_okf_project.py`
- `templates/tool-adapters/AGENTS.md`
- `templates/tool-adapters/CLAUDE.md`
- `templates/tool-adapters/.cursor/rules/okf.mdc`
- `templates/tool-adapters/PERPLEXITY.md`

# Known Issues

- `Project-1` is not a git repository in this workspace, so changes could not be committed to a branch.
- Optional bootstrap-owned files are copied only when the scaffold script is run from a full bootstrap checkout that contains those files.

# Next Recommended Actions

1. Review whether `.okf/agents/xcode-claude.md` should move from `status: draft` to `active` after real Xcode configuration.
2. If this folder is later placed in git, commit the current file changes on the intended branch.

# Validation Needed

No blocking validation remains. Future validation should rerun `scripts/okf-validate` after any additional dispatch script changes.

# Context Pack

Relevant context is in `.okf/tests/2026-06-27-perplexity-bootstrap-propagation.md`, `.okf/features/shared-okf-skills.md`, and `skills/create-new-okf-project/scripts/create_okf_project.py`.
