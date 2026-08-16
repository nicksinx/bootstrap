# OKF Project Log

## 2026-08-16

### OKF v0.2 conformance and strict validation

- Migrated the live OKF bundle and primary scaffold templates from v0.1 `timestamp`/legacy status values to v0.2 `generated` metadata and lifecycle values.
- Replaced line-splitting frontmatter parsing with a shared PyYAML validator that enforces reserved files, provenance/trust/lifecycle families, actor syntax, duplicate-key rejection, and Attested Computation structure.
- Added strict and JSON validator modes, a v0.2 JSON Schema, focused conformance tests, generated-project strict validation, and GitHub Actions CI.
- Removed unsupported `setup-python` pip caching from the dependency-file-free workflow after the initial hosted run failed before tests; PR #2 then passed `bootstrap-ci / validate` on Ubuntu with Python 3.11.
- Preserved Project Bootstrap profile extensions and generated-project Forge validation hooks while accepting unknown concept types and extension keys.
- Validation evidence: [PR 1 conformance tests](tests/2026-08-16-okf-v02-conformance.md).

### OKF v0.2 migration, scaffold consolidation, and skills

- Added atomic, idempotent `scripts/okf-migrate` check/apply behavior with parse-before-write rollback safety and strict post-apply validation.
- Consolidated normal project generation onto `scripts/launch_project.sh` and `templates/new-project/`; the installed `create-new-okf-project` skill now delegates when the bootstrap checkout is available and retains a strict v0.2 standalone fallback.
- Bundled byte-identical validator and migration runtimes in the portable skill, synchronized generated adapters after project creation, and made adapter drift a failing gate by default.
- Updated Codex-compatible skills to minimal frontmatter and current v0.2 examples while preserving the four Perplexity adapters' documented extended metadata contract.
- Added migration, scaffold-parity, and skill-contract regression suites; full validation evidence is recorded in [the work package 2 test record](tests/2026-08-16-okf-v02-migration-scaffold.md).

### Deterministic indexes, graph exports, and freshness review

- Added `scripts/okf-index` with atomic check/write modes, marked generated blocks, authored-prose preservation, parse-before-write safety, and per-directory indexes.
- Added `scripts/okf-visualize` for deterministic JSON and self-contained HTML concept graphs derived from resolvable internal Markdown links.
- Added `scripts/okf-freshness` with explicit audit dates, overdue checks, optional deadline coverage enforcement, and no automatic trust or lifecycle mutation.
- Added 90-day freshness deadlines to canonical and standalone project scaffolds and propagated all tooling through launch validation, Make targets, skills, and operator docs.
- Closed a canonical launcher parity gap by adding the documented Perplexity/Xcode agents and prompts, handoff templates, context-pack guide, Xcode risk, Perplexity file guide, and Codex skill-install instructions to `templates/new-project/`.
- Added cross-platform handling for legacy case-variant `INDEX.md` landing pages so index generation is identical on case-sensitive and case-insensitive filesystems.
- Added focused idempotence, rollback, graph, HTML, freshness, and scaffold tests; evidence is recorded in [the work package 3 test record](tests/2026-08-16-okf-index-graph-freshness.md).

### Bounded integrations and attested computation

- Added an opt-in OpenWiki sidecar overlay and staged runner that imports only `openwiki/` plus complete OpenWiki-owned adapter blocks; `.okf` mutation, malformed markers, and symlink outputs fail closed.
- Updated adapter synchronization to preserve valid OpenWiki blocks in `AGENTS.md` and `CLAUDE.md` and to preflight all selected adapters before the first write.
- Added a local, path-contained, read-only OKF MCP pilot with six deterministic query tools, modern `2026-07-28` discovery, legacy initialization compatibility, and traversal/symlink rejection.
- Added one deterministic OKF v0.2 `Attested Computation`, an executor and attester, ignored `.okf-runtime/` receipts, and explicit limits on the experimental receipt/verdict ABI.
- Added the curated integration boundary decision, optional-integration review workflow, reviewed upstream protocol reference, operator guides, project configuration, canonical scaffold propagation, and strict launch/CI probes.
- Focused adversarial suites and the combined `make check` gate passed; evidence is recorded in [the work package 4 test record](tests/2026-08-16-okf-integrations-attestation.md).
- Published the four logical work packages as draft GitHub PRs #2-#5; after correcting dependency-free Python setup at the conformance layer and merging it forward without rewriting history, every stacked `bootstrap-ci / validate` check passed.

## 2026-07-04

### Forge lifecycle profile — Project-1 harness promotion

- Added `profiles/forge-lifecycle.yaml` and `templates/forge-lifecycle/` overlay (11 MCP launchers, clone helper, Cursor config, OKF decision/refs).
- `launch_project.sh`: render overlay when profile is `forge-lifecycle`; auto-write `.cursor/mcp.json` from forge example.
- Default `.gitignore.tmpl` now ignores `.okf/forge/*/` workspaces.
- Lessons: `.okf/improvements/forge-lifecycle-bootstrap-lessons.md`.
- Smoke: `test_forge_lifecycle_launch_and_validate` in `tests/test_launch_smoke.py`.


### Cursor rules pack — adversarial review + install

- Added OKF + Forge Cursor rules under `templates/tool-adapters/.cursor/rules/` (routing, forge operator, dispatch, promotion, legacy).
- Adversarial review: `docs/cursor-rules-adversarial-review.md`; install guide: `docs/install-cursor-rules.md`.
- Wired into `profiles/default.yaml` v2 and `validate_launch.sh`.


### Bootstrap-okf-forge-project skill

- Added `skills/bootstrap-okf-forge-project/` Cursor skill for standardized project intake.
- Added `scripts/project-intake` CLI, `schemas/project-intake.schema.json`, `docs/install-bootstrap-okf-forge-skill.md`.

- Merged Forge + OKF dispatch into `profiles/default.yaml` v2.0.0; deprecated `legacy-task` and `forge-lifecycle` alias profiles.
- Updated `launch_project.sh`, `validate_launch.sh`, templates, tests, README, CHANGELOG, migration doc.
- Removed ai-task MCP and workers from default scaffold; `templates/legacy-task/` overlay for deprecated path.


### Standup guide + express intake

- Added `docs/new-okf-forge-project-standup.md` — consolidated operator cheat sheet.
- Added `scripts/project-intake quick` with `gh` owner prefill; updated handoff and render checklists.
- Added `scripts/operator-ready-check.sh` to v2 scaffold and `validate_launch.sh`.
- Compressed guided intake phases in skill and `user-intake-prompt.md`; fixed install doc stale rules step.
- Added `docs/operator-guides.md` and `docs/new-okf-forge-project-standup-offline.md` for notes-app continuity export.

## 2026-06-28

### Soft-spot closure batch 1

- Updated operator brief: references vs docs dual role, brief maintenance checklist, bootstrap kit path note.
- Updated `.okf/prompts/perplexity-custom-instructions.md` — read brief before re-deriving policy.
- Updated `docs/perplexity-project-files-and-skills.md` — brief once rule, Tier 6 optional improvements.
- Updated `skills/create-new-okf-project/SKILL.md` — bootstrap kit path guidance.
- Added `.okf/prompts/perplexity-procurelex-research.md` for application research (ProcureLex).


### Batch 2 — Perplexity Space curation

- Operator curated Project Files and Skills per `docs/perplexity-project-files-and-skills.md` (brief once, Tier 1–4, four perplexity-okf-* skills).
- Added `.okf/prompts/perplexity-post-curation-smoke-test.md` for configuration verification.
- Post-curation smoke test: **PASS** (2026-06-28) — five-service order, brief-once, references vs docs, MODE A/B, four skills, explicit negatives confirmed.
- Post-smoke follow-up: Tier 2 prompt/workflow files attached; four `perplexity-okf-*` skills uploaded as Project Skills. Perplexity Space curation complete.


### Wave 1 — scaffold parity

- Added `BOOTSTRAP_COPY_PATHS` to `create_okf_project.py`; extended copy list with operator brief, full xcode/perplexity/configure-perplexity guides, post-curation smoke-test prompt.
- Bootstrap copies now use `overwrite=True` to replace embedded stubs when run from kit path.
- Added `.okf/tests/2026-06-28-scaffold-parity.md` (full kit ~74 files vs sparse ~35).
- Updated `skills/create-new-okf-project/SKILL.md` and brief bootstrap section.
- Handoff: `.okf/handoffs/2026-06-28-scaffold-parity.md` for Claude verification.


### Wave 3 — Xcode step 4 dry verification

- Expanded `docs/create-new-okf-project-in-xcode.md` to full step-4 guide (prerequisites, dispatch, dry vs live verification).
- Added `.okf/prompts/xcode-step4-verification-checklist.md`, `.okf/handoffs/TEMPLATE-xcode-step4.md`, `.okf/risks/xcode-live-verification-pending.md`.
- Deepened `.okf/agents/xcode-claude.md` (remains `draft` / `unverified` until live Xcode).
- Added `.okf/tests/2026-06-28-xcode-step4-dry-verification.md` — dry verification **PASS** (dispatch `xcode-claude` runner exercised).
- Added `.okf/improvements/2026-06-28-xcode-step4-dry-lessons.md`.
- Extended `BOOTSTRAP_COPY_PATHS` with xcode checklist, step-4 handoff template, live-verification risk.
- Handoff: `.okf/handoffs/2026-06-28-xcode-step4-dry-verification.md`.


### Claude Code step-3 guide — five-service alignment

- Saved session handoff at `.okf/handoffs/2026-06-28-bootstrap-refinement-handoff.md`.
- Updated `docs/create-new-okf-project-in-claude.md` to reflect five-service model: added Perplexity (step 5) to service table and companion docs list; added `docs/okf-ways-of-working-brief.md` to required read order; updated service-order confirmation text to include "Perplexity fifth"; added `PERPLEXITY.md` stub check in step 3; added `scripts/okf-check-adapters` to step 8 validate block; updated handoff payload item 10 to point to step 5; added two checklist items (`PERPLEXITY.md` present, `okf-check-adapters` clean); added Perplexity configuration docs to related material.
- Updated `.okf/index.md` current handoff pointer to 2026-06-28 session handoff.
- `scripts/okf-validate` and `scripts/okf-check-adapters` both pass (0 warnings, 13 skills).


### Wave 2 — dispatch ergonomics

- Added `.okf/handoffs/TEMPLATE-tester.md` — role-specific template with test evidence table, issues-for-reviewer section, and pre-filled reviewer next steps.
- Added `.okf/handoffs/TEMPLATE-reviewer.md` — role-specific template with requirements-checked table, findings table with severity, reviewer verdict, and pre-filled integrator next steps.
- Updated `.okf/handoffs/README.md` with template selection table (general / tester / reviewer / xcode / general).
- Added `.okf/tests/2026-06-28-dispatch-dry-run.md` — live dry run of full pipeline cycle: init-pipeline, builder advance, tester overflow metadata stub, reviewer and integrator completion; all checks PASS.
- Extended `docs/okf-dispatch-orchestration.md` with "Role handoff expectations" section covering tester and reviewer deliverables, overflow trigger sequence, and a template quick-reference table.
- `scripts/okf-validate` 0 warnings; `scripts/okf-check-adapters` pass (13 skills).


### Wave 2 follow-up — Cursor

- Extended `BOOTSTRAP_COPY_PATHS` with all handoff templates (`TEMPLATE-tester`, `TEMPLATE-reviewer`, `TEMPLATE-xcode-step4`).
- Added `.okf/improvements/2026-06-28-dispatch-ergonomics-lessons.md`.
- Updated brief (dispatch templates, dry-run evidence), README (removed stale Wave 2 pending note), test doc pending line closed.

## 2026-06-27

- Added shared OKF skills operating model with canonical skills in `skills/*/SKILL.md` and thin adapters for Codex, Claude Code, Cursor, and future services.
- Added `scripts/okf-sync-skills` with `--dry-run`, `--list-skills`, and `--target` options.
- Added `docs/shared-okf-skills.md` and `.okf/features/shared-okf-skills.md`.
- Updated `.cursor/rules/okf.mdc` as a project-local overlay that preserves Cursor global skills.
- Marked `.okf/features/codex-okf-skills.md` as superseded by the shared skills feature.


### Shared-skills follow-up

- Broadened all 9 canonical skill `description:` values from "Use when Codex needs" to "Use when an agent needs"; resynced all adapters.
- Updated `create-new-okf-project` scaffold to generate `scripts/okf-sync-skills` and `.claude/commands/okf-sync.md` for new projects; smoke-tested (19 files written, validate passed, `.claude/commands/okf-sync.md` present).
- Fixed hardcoded timestamp in `scripts/okf-sync-skills` `adapter_future` builder; now uses runtime timestamp.
- Updated `templates/tool-adapters/` to reference the sync script and use the richer Cursor overlay format.
- Added shared-skills test evidence at `.okf/tests/2026-06-27-shared-skills-validation.md`.
- Updated `.okf/architecture/okf-bootstrap-layout.md` to document the generated-adapter model and `.claude/commands/` layer.


### Dispatch

- Added OKF file-queue dispatch under `.okf/dispatch/{ready,running,done,failed}/`.
- Added `scripts/okf-dispatch` with roles `builder`, `tester`, `reviewer`, and `integrator`.
- Added typed JSON work packets for runners `codex`, `claude`, `cursor`, and `xcode-claude`.
- Added Codex `Stop` hook in `.codex/hooks.json` calling `scripts/okf-dispatch advance --from codex`.
- Added `docs/okf-dispatch-orchestration.md` and `.okf/workflows/multi-agent-delivery-pipeline.md`.
- Validated the OKF bundle with `scripts/okf-validate`.


### New-project setup guides

- Added `docs/create-new-okf-project-in-codex.md` as the step 2 setup guide for configuring Codex after Cursor and before Claude Code and Xcode.
- Added `docs/create-new-okf-project-in-claude.md` as the step 3 setup guide for configuring Claude Code after Cursor and Codex and before Xcode.
- Updated `.okf/index.md` with the canonical new-project setup guide sequence: Cursor, Codex, Claude Code, Xcode.


### Perplexity service 5 + overflow

- Added `docs/configure-perplexity-okf.md` with custom instructions, model routing, and setup checklist.
- Added Perplexity agent rules: `.okf/agents/perplexity.md` (research, active), `.okf/agents/perplexity-overflow.md` (failover).
- Added workflows: `.okf/workflows/perplexity-research-cycle.md`, `.okf/workflows/perplexity-overflow-failover.md`.
- Added prompts: `.okf/prompts/perplexity-custom-instructions.md`, `.okf/prompts/perplexity-overflow-failover.md`; updated deep-research setup prompt.
- Updated `docs/create-new-okf-project-in-perplexity.md`, `docs/shared-okf-skills.md`, `.okf/features/shared-okf-skills.md`, `.okf/index.md`, multi-agent dispatch workflow.
- Added `perplexity` target to `scripts/okf-sync-skills` generating `PERPLEXITY.md` thin adapter.


### Perplexity OKF skills

- Added four Perplexity-specific canonical skills under `skills/perplexity-okf-*/SKILL.md` (reader, citation-steward, handoff-writer, concept-writer) for Perplexity Desktop Project skills attachment.
- Resynced tool adapters; validation passed.


### Perplexity research implementation

- Ingested Perplexity research pack: 11 Reference concepts under `.okf/references/`.
- Added `.okf/handoffs/README.md`, `TEMPLATE.md`; `.okf/context-packs/INDEX.md`.
- Added `docs/perplexity-project-files-and-skills.md`, `docs/skill-frontmatter-compatibility.md`.
- Added `.okf/improvements/2026-06-27-perplexity-research-lessons.md`.
- Extended `scripts/okf-validate` to enforce draft Reference rules (`unverified`, `source_of_truth: false`).
- Implemented P0/P1 backlog items; deferred scaffold generator and dispatch overflow automation.


### Perplexity bootstrap propagation

- Updated `create-new-okf-project` scaffold script and skill contract so new projects inherit `PERPLEXITY.md`, Perplexity prompts, Perplexity/Xcode agent rules, Perplexity workflows, dispatch directories, optional dispatcher files, and bundled OKF skills.
- Added `docs/create-new-okf-project-in-xcode.md` and `.okf/agents/xcode-claude.md` to complete the five-service setup sequence.
- Refreshed stale `templates/tool-adapters/` with the five-service model and added `templates/tool-adapters/PERPLEXITY.md`.
- Updated shared-skill and Cursor setup docs to describe Perplexity Project Skills, `--target perplexity`, and generated scaffold expectations.
- Ran `scripts/okf-sync-skills` after updating `skills/create-new-okf-project/SKILL.md`, refreshing `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/okf.mdc`, `PERPLEXITY.md`, and `.okf/agents/future-service.md`.
- Validation: `scripts/okf-validate` passed; `scripts/okf-sync-skills --target perplexity --dry-run` found 13 skills; final smoke scaffold under `/private/tmp/okf-scaffold-smoke-20260627-final` wrote 66 files and validated with 0 warnings.


### OKF gap closure

- Added `scripts/okf-check-adapters` to detect canonical skill index drift in generated adapters.
- Added `scripts/okf-dispatch overflow` for packet overflow metadata and automatic handoff stub.
- Extended `create-new-okf-project` bootstrap copy list: handoff README/TEMPLATE, context-pack index, Perplexity docs, check-adapters.
- Updated dispatch orchestration and overflow workflow docs.
- Added `.okf/prompts/codex-share-okf-ways-of-working-updates.md`.


### Operator brief

- Added `docs/okf-ways-of-working-brief.md` — portable operator guide (five services, dispatch, Perplexity modes, research references, scaffold expectations).
- Linked brief from `.okf/index.md` required reading order and Shared Skills section.


### GitHub publish attempt

- Synced GitHub clone at `/Users/dv/Projects/testrunner/bootstrap` from canonical source `/Users/dv/Projects/testrunner/Project-1`.
- Committed latest OKF bootstrap kit changes on branch `okf-project-bootstrap-framework` with commit `8a2666f`.
- Validation before commit passed: Python compile, `scripts/okf-validate`, `scripts/okf-check-adapters`, and `scripts/okf-sync-skills --dry-run`.
- Push to `origin` was attempted without force; network escalation reached GitHub, but HTTPS authentication was unavailable (`could not read Username for 'https://github.com'`).

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
