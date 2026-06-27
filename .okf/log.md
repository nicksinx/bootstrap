---
type: Reference
title: OKF Project Log
description: Chronological record of material OKF and project changes.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/log.md
tags: [okf, log]
applies_to: [cursor, claude, codex, xcode-claude, perplexity, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# OKF Project Log

## 2026-06-24

- Created Project-1 as a reusable OKF bootstrap kit.
- Added primary `.okf` bundle with project, requirement, feature, architecture, decision, risk, workflow, test, release, reference, and handoff concepts.
- Added thin adapters for Codex, Claude, and Cursor.
- Added helper script plan for validation, context packs, and handoffs.
- Added eight Codex-installable OKF skill folders.
- Validated the OKF bundle with `scripts/okf-validate`.
- Validated the original eight skill folders with the Codex skill quick validator using a local cached PyYAML package.
- Smoke-tested `scripts/okf-context-pack` and `scripts/okf-handoff`; removed generated smoke artifacts afterward.
- Added `.okf/improvements/` as the continuous-improvement repository for lessons learned, retrospectives, and reusable process improvements.
- Added the `create-new-okf-project` Codex skill with a bundled scaffold script.
- Smoke-tested `create-new-okf-project/scripts/create_okf_project.py` against a temporary project; generated OKF validation passed with zero warnings.
- Updated existing OKF skills so readers, concept writers, context packs, and validators recognize `.okf/improvements/`.
- Validated all nine skill folders with the Codex skill quick validator.

## 2026-06-27

- Added shared OKF skills operating model with canonical skills in `skills/*/SKILL.md` and thin adapters for Codex, Claude Code, Cursor, and future services.
- Added `scripts/okf-sync-skills` with `--dry-run`, `--list-skills`, and `--target` options.
- Added `docs/shared-okf-skills.md` and `.okf/features/shared-okf-skills.md`.
- Updated `.cursor/rules/okf.mdc` as a project-local overlay that preserves Cursor global skills.
- Marked `.okf/features/codex-okf-skills.md` as superseded by the shared skills feature.

## 2026-06-27 (shared-skills follow-up)

- Broadened all 9 canonical skill `description:` values from "Use when Codex needs" to "Use when an agent needs"; resynced all adapters.
- Updated `create-new-okf-project` scaffold to generate `scripts/okf-sync-skills` and `.claude/commands/okf-sync.md` for new projects; smoke-tested (19 files written, validate passed, `.claude/commands/okf-sync.md` present).
- Fixed hardcoded timestamp in `scripts/okf-sync-skills` `adapter_future` builder; now uses runtime timestamp.
- Updated `templates/tool-adapters/` to reference the sync script and use the richer Cursor overlay format.
- Added shared-skills test evidence at `.okf/tests/2026-06-27-shared-skills-validation.md`.
- Updated `.okf/architecture/okf-bootstrap-layout.md` to document the generated-adapter model and `.claude/commands/` layer.

## 2026-06-27 (dispatch)

- Added OKF file-queue dispatch under `.okf/dispatch/{ready,running,done,failed}/`.
- Added `scripts/okf-dispatch` with roles `builder`, `tester`, `reviewer`, and `integrator`.
- Added typed JSON work packets for runners `codex`, `claude`, `cursor`, and `xcode-claude`.
- Added Codex `Stop` hook in `.codex/hooks.json` calling `scripts/okf-dispatch advance --from codex`.
- Added `docs/okf-dispatch-orchestration.md` and `.okf/workflows/multi-agent-delivery-pipeline.md`.
- Validated the OKF bundle with `scripts/okf-validate`.

## 2026-06-27 (new-project setup guides)

- Added `docs/create-new-okf-project-in-codex.md` as the step 2 setup guide for configuring Codex after Cursor and before Claude Code and Xcode.
- Added `docs/create-new-okf-project-in-claude.md` as the step 3 setup guide for configuring Claude Code after Cursor and Codex and before Xcode.
- Updated `.okf/index.md` with the canonical new-project setup guide sequence: Cursor, Codex, Claude Code, Xcode.

## 2026-06-27 (Perplexity service 5 + overflow)

- Added `docs/configure-perplexity-okf.md` with custom instructions, model routing, and setup checklist.
- Added Perplexity agent rules: `.okf/agents/perplexity.md` (research, active), `.okf/agents/perplexity-overflow.md` (failover).
- Added workflows: `.okf/workflows/perplexity-research-cycle.md`, `.okf/workflows/perplexity-overflow-failover.md`.
- Added prompts: `.okf/prompts/perplexity-custom-instructions.md`, `.okf/prompts/perplexity-overflow-failover.md`; updated deep-research setup prompt.
- Updated `docs/create-new-okf-project-in-perplexity.md`, `docs/shared-okf-skills.md`, `.okf/features/shared-okf-skills.md`, `.okf/index.md`, multi-agent dispatch workflow.
- Added `perplexity` target to `scripts/okf-sync-skills` generating `PERPLEXITY.md` thin adapter.

## 2026-06-27 (Perplexity OKF skills)

- Added four Perplexity-specific canonical skills under `skills/perplexity-okf-*/SKILL.md` (reader, citation-steward, handoff-writer, concept-writer) for Perplexity Desktop Project skills attachment.
- Resynced tool adapters; validation passed.

## 2026-06-27 (Perplexity research implementation)

- Ingested Perplexity research pack: 11 Reference concepts under `.okf/references/`.
- Added `.okf/handoffs/README.md`, `TEMPLATE.md`; `.okf/context-packs/INDEX.md`.
- Added `docs/perplexity-project-files-and-skills.md`, `docs/skill-frontmatter-compatibility.md`.
- Added `.okf/improvements/2026-06-27-perplexity-research-lessons.md`.
- Extended `scripts/okf-validate` to enforce draft Reference rules (`unverified`, `source_of_truth: false`).
- Implemented P0/P1 backlog items; deferred scaffold generator and dispatch overflow automation.

## 2026-06-27 (Perplexity bootstrap propagation)

- Updated `create-new-okf-project` scaffold script and skill contract so new projects inherit `PERPLEXITY.md`, Perplexity prompts, Perplexity/Xcode agent rules, Perplexity workflows, dispatch directories, optional dispatcher files, and bundled OKF skills.
- Added `docs/create-new-okf-project-in-xcode.md` and `.okf/agents/xcode-claude.md` to complete the five-service setup sequence.
- Refreshed stale `templates/tool-adapters/` with the five-service model and added `templates/tool-adapters/PERPLEXITY.md`.
- Updated shared-skill and Cursor setup docs to describe Perplexity Project Skills, `--target perplexity`, and generated scaffold expectations.
- Ran `scripts/okf-sync-skills` after updating `skills/create-new-okf-project/SKILL.md`, refreshing `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/okf.mdc`, `PERPLEXITY.md`, and `.okf/agents/future-service.md`.
- Validation: `scripts/okf-validate` passed; `scripts/okf-sync-skills --target perplexity --dry-run` found 13 skills; final smoke scaffold under `/private/tmp/okf-scaffold-smoke-20260627-final` wrote 66 files and validated with 0 warnings.

## 2026-06-27 (OKF gap closure)

- Added `scripts/okf-check-adapters` to detect canonical skill index drift in generated adapters.
- Added `scripts/okf-dispatch overflow` for packet overflow metadata and automatic handoff stub.
- Extended `create-new-okf-project` bootstrap copy list: handoff README/TEMPLATE, context-pack index, Perplexity docs, check-adapters.
- Updated dispatch orchestration and overflow workflow docs.
- Added `.okf/prompts/codex-share-okf-ways-of-working-updates.md`.

## 2026-06-27 (operator brief)

- Added `docs/okf-ways-of-working-brief.md` — portable operator guide (five services, dispatch, Perplexity modes, research references, scaffold expectations).
- Linked brief from `.okf/index.md` required reading order and Shared Skills section.

## 2026-06-28 (soft-spot closure batch 1)

- Updated operator brief: references vs docs dual role, brief maintenance checklist, bootstrap kit path note.
- Updated `.okf/prompts/perplexity-custom-instructions.md` — read brief before re-deriving policy.
- Updated `docs/perplexity-project-files-and-skills.md` — brief once rule, Tier 6 optional improvements.
- Updated `skills/create-new-okf-project/SKILL.md` — bootstrap kit path guidance.
- Added `.okf/prompts/perplexity-procurelex-research.md` for application research (ProcureLex).

## 2026-06-28 (Batch 2 — Perplexity Space curation)

- Operator curated Project Files and Skills per `docs/perplexity-project-files-and-skills.md` (brief once, Tier 1–4, four perplexity-okf-* skills).
- Added `.okf/prompts/perplexity-post-curation-smoke-test.md` for configuration verification.
- Post-curation smoke test: **PASS** (2026-06-28) — five-service order, brief-once, references vs docs, MODE A/B, four skills, explicit negatives confirmed.
- Post-smoke follow-up: Tier 2 prompt/workflow files attached; four `perplexity-okf-*` skills uploaded as Project Skills. Perplexity Space curation complete.

## 2026-06-28 (Wave 1 — scaffold parity)

- Added `BOOTSTRAP_COPY_PATHS` to `create_okf_project.py`; extended copy list with operator brief, full xcode/perplexity/configure-perplexity guides, post-curation smoke-test prompt.
- Bootstrap copies now use `overwrite=True` to replace embedded stubs when run from kit path.
- Added `.okf/tests/2026-06-28-scaffold-parity.md` (full kit ~74 files vs sparse ~35).
- Updated `skills/create-new-okf-project/SKILL.md` and brief bootstrap section.
- Handoff: `.okf/handoffs/2026-06-28-scaffold-parity.md` for Claude verification.

## 2026-06-28 (Wave 3 — Xcode step 4 dry verification)

- Expanded `docs/create-new-okf-project-in-xcode.md` to full step-4 guide (prerequisites, dispatch, dry vs live verification).
- Added `.okf/prompts/xcode-step4-verification-checklist.md`, `.okf/handoffs/TEMPLATE-xcode-step4.md`, `.okf/risks/xcode-live-verification-pending.md`.
- Deepened `.okf/agents/xcode-claude.md` (remains `draft` / `unverified` until live Xcode).
- Added `.okf/tests/2026-06-28-xcode-step4-dry-verification.md` — dry verification **PASS** (dispatch `xcode-claude` runner exercised).
- Added `.okf/improvements/2026-06-28-xcode-step4-dry-lessons.md`.
- Extended `BOOTSTRAP_COPY_PATHS` with xcode checklist, step-4 handoff template, live-verification risk.
- Handoff: `.okf/handoffs/2026-06-28-xcode-step4-dry-verification.md`.

## 2026-06-28 (Claude Code step-3 guide — five-service alignment)

- Saved session handoff at `.okf/handoffs/2026-06-28-bootstrap-refinement-handoff.md`.
- Updated `docs/create-new-okf-project-in-claude.md` to reflect five-service model: added Perplexity (step 5) to service table and companion docs list; added `docs/okf-ways-of-working-brief.md` to required read order; updated service-order confirmation text to include "Perplexity fifth"; added `PERPLEXITY.md` stub check in step 3; added `scripts/okf-check-adapters` to step 8 validate block; updated handoff payload item 10 to point to step 5; added two checklist items (`PERPLEXITY.md` present, `okf-check-adapters` clean); added Perplexity configuration docs to related material.
- Updated `.okf/index.md` current handoff pointer to 2026-06-28 session handoff.
- `scripts/okf-validate` and `scripts/okf-check-adapters` both pass (0 warnings, 13 skills).

## 2026-06-28 (Wave 2 — dispatch ergonomics)

- Added `.okf/handoffs/TEMPLATE-tester.md` — role-specific template with test evidence table, issues-for-reviewer section, and pre-filled reviewer next steps.
- Added `.okf/handoffs/TEMPLATE-reviewer.md` — role-specific template with requirements-checked table, findings table with severity, reviewer verdict, and pre-filled integrator next steps.
- Updated `.okf/handoffs/README.md` with template selection table (general / tester / reviewer / xcode / general).
- Added `.okf/tests/2026-06-28-dispatch-dry-run.md` — live dry run of full pipeline cycle: init-pipeline, builder advance, tester overflow metadata stub, reviewer and integrator completion; all checks PASS.
- Extended `docs/okf-dispatch-orchestration.md` with "Role handoff expectations" section covering tester and reviewer deliverables, overflow trigger sequence, and a template quick-reference table.
- `scripts/okf-validate` 0 warnings; `scripts/okf-check-adapters` pass (13 skills).

## 2026-06-28 (Wave 2 follow-up — Cursor)

- Extended `BOOTSTRAP_COPY_PATHS` with all handoff templates (`TEMPLATE-tester`, `TEMPLATE-reviewer`, `TEMPLATE-xcode-step4`).
- Added `.okf/improvements/2026-06-28-dispatch-ergonomics-lessons.md`.
- Updated brief (dispatch templates, dry-run evidence), README (removed stale Wave 2 pending note), test doc pending line closed.
