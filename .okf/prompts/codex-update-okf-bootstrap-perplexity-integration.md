---
type: Reference
title: Codex Prompt — Update OKF Bootstrap for Perplexity Integration
description: Copy-paste prompt for Codex to propagate Perplexity integration, Project Files/Skills guidance, and skill-format lessons into the OKF Project Bootstrap repository.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/prompts/codex-update-okf-bootstrap-perplexity-integration.md
tags: [okf, prompt, codex, perplexity, bootstrap]
applies_to: [codex, cursor, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T22:00:00+01:00
---

# Purpose

Use this prompt when the OKF Project Bootstrap repository is open (local clone or GitHub) and Codex should propagate Perplexity integration work and lessons learned into the bootstrap kit, scaffold, templates, and documentation.

# Prompt (copy below this line)

```markdown
You are working in the **OKF Project Bootstrap repository** (Project-1 / OKF bootstrap kit). Your job is to **propagate Perplexity integration and related lessons learned** into the bootstrap repo so new OKF projects inherit a complete five-service operating model (Cursor, Codex, Claude Code, Xcode, Perplexity) plus documented overflow behavior.

## Read first (do not skip)

1. `.okf/index.md`
2. `.okf/project.md`
3. `.okf/log.md` — entries from 2026-06-27 (shared skills, dispatch, Perplexity service 5 + overflow, Perplexity OKF skills)
4. `.okf/handoffs/2026-06-27-perplexity-okf-configuration.md`
5. `.okf/handoffs/2026-06-27-shared-okf-skills-mvp.md`
6. `docs/configure-perplexity-okf.md`
7. `docs/shared-okf-skills.md`
8. `docs/create-new-okf-project-in-perplexity.md`
9. `docs/create-new-okf-project-in-cursor.md` (canonical 5-step service order)
10. `.okf/features/shared-okf-skills.md`
11. `.okf/workflows/perplexity-research-cycle.md`
12. `.okf/workflows/perplexity-overflow-failover.md`
13. `.okf/workflows/multi-agent-delivery-pipeline.md`
14. `scripts/okf-sync-skills` (including `--target perplexity`)
15. `PERPLEXITY.md`
16. All four Perplexity skills:
    - `skills/perplexity-okf-reader/SKILL.md`
    - `skills/perplexity-okf-citation-steward/SKILL.md`
    - `skills/perplexity-okf-handoff-writer/SKILL.md`
    - `skills/perplexity-okf-concept-writer/SKILL.md`
17. `skills/create-new-okf-project/scripts/create_okf_project.py` (scaffold gaps)
18. `templates/tool-adapters/` (may be stale)

## Context — what was learned (treat as requirements for this update)

### Perplexity roles in OKF

- **Service 5 (planned):** Perplexity Desktop Pro deep research → draft `Reference` concepts in `.okf/references/` (`verification_status: unverified`). Cursor or Codex ingests; Perplexity never writes the repo directly.
- **Overflow (ad hoc sixth layer):** When Codex, Claude, Cursor, or Xcode is blocked (usage limits, outage, policy), Perplexity completes the **same OKF role contract** (builder/tester/reviewer/integrator) in **MODE B — OVERFLOW**. Integrator applies output; dispatch is not advanced from Perplexity automatically in MVP.
- **Not in scope:** Perplexity Computer as an automated runner unless explicitly added later.

### Perplexity configuration model (three layers)

1. **Custom instructions** — pasted in Perplexity Desktop Settings from `.okf/prompts/perplexity-custom-instructions.md` (MODE A research + MODE B overflow).
2. **Project Files** — curated OKF attachments (~8–14 files), not the whole repo. Tiered: core (project.md, index.md, PERPLEXITY.md), mode contracts (prompts/workflows), agent rules, latest handoff + active requirement/spec.
3. **Project Skills** — four Perplexity-specific skills (`perplexity-okf-*`) attached from `skills/perplexity-okf-*/SKILL.md`; they are **not** the same as Codex-installed `okf-*` skills.

### Skill formatting adjustments required

Canonical OKF skills remain under `skills/okf-*/SKILL.md` with minimal frontmatter (`name`, `description`).

**Service-specific adapter skills** for Perplexity use **extended frontmatter**:

```yaml
---
name: perplexity-okf-reader
description: ...
applies_to: [perplexity]
okf_mode: [research, overflow]
canonical_skill: skills/okf-reader/SKILL.md
---
```

Rules learned:

- Do **not** duplicate full `okf-*` skill bodies in Perplexity skills; point to `canonical_skill` and add Perplexity-only constraints (no repo access, Project Files, ingest via Cursor/Codex, MODE A/B).
- Keep `scripts/okf-sync-skills` listing **all** canonical skills in thin adapters; Perplexity adapter is `PERPLEXITY.md` via `--target perplexity`.
- Codex skills install from `skills/` into Codex home; Perplexity skills are **attached in Perplexity Project settings** — document both paths clearly.
- Cursor global skills remain untouched; OKF is a project-local overlay.

### Gaps in bootstrap repo (fix these)

1. **`create-new-okf-project` scaffold** likely does not yet emit:
   - Perplexity docs, prompts, workflows, agent rules
   - Four `skills/perplexity-okf-*/SKILL.md` files
   - `docs/configure-perplexity-okf.md`
   - `PERPLEXITY.md` (or generate via first `okf-sync-skills` run)
   - Stub `.okf/prompts/` and `.okf/agents/perplexity*.md` entries
2. **Embedded `scripts/okf-sync-skills` in `create_okf_project.py`** may lack `--target perplexity` and `adapter_perplexity`.
3. **`templates/tool-adapters/`** may still use pre-shared-skills or pre-Perplexity Cursor rules.
4. **`docs/`** lacks a dedicated **Perplexity Project Files and Skills** guide (create from lessons below).
5. **`.okf/improvements/`** should capture durable lessons so future agents do not repeat mistakes.
6. **Setup guides** for Codex/Claude may still say four services only — align to five (+ overflow footnote).
7. **`docs/create-new-okf-project-in-xcode.md`** may still be missing (note in handoff if out of scope).

## Task — implement bootstrap propagation

Implement the **smallest complete update** that makes new projects OKF-aligned with Perplexity:

### A. Documentation

1. Add `docs/perplexity-project-files-and-skills.md` documenting:
   - Tier 1–5 file attachment list for Perplexity Projects
   - Four recommended Perplexity skills and when to use each
   - MODE A vs MODE B file/skill emphasis
   - Maintenance rhythm (refresh handoff, active spec)
   - What not to attach (dispatch JSON, secrets, full codebase)
2. Link it from `docs/configure-perplexity-okf.md`, `docs/shared-okf-skills.md`, and `.okf/index.md`.
3. Add `.okf/improvements/` entry capturing lessons: dual-mode Perplexity, adapter skill frontmatter, ingest boundary, overflow manual integrator.

### B. Scaffold (`skills/create-new-okf-project`)

1. Update `create_okf_project.py` to scaffold Perplexity artifacts (copy from current bootstrap repo or generate stubs that match existing files).
2. Ensure embedded `OKF_SYNC_SKILLS` includes `perplexity` target and `adapter_perplexity` (keep in sync with root `scripts/okf-sync-skills`).
3. Scaffold all four `skills/perplexity-okf-*/SKILL.md` into new projects (or copy from bootstrap kit template).
4. Update scaffold validation checklist and post-scaffold instructions to mention:
   - Step 5 Perplexity configuration
   - Paste custom instructions
   - Attach Project Files and Skills per `docs/perplexity-project-files-and-skills.md`
5. Update `skills/create-new-okf-project/SKILL.md` if behavior changed.

### C. Templates

1. Refresh `templates/tool-adapters/` (Cursor rule, AGENTS.md, CLAUDE.md stubs) to reference shared skills + Perplexity where appropriate.
2. Add template stubs for Perplexity prompts/agents if the scaffold does not copy full files.

### D. OKF concepts

1. Update `.okf/features/shared-okf-skills.md` if Perplexity skills or file guidance is not fully reflected.
2. Update `.okf/architecture/okf-bootstrap-layout.md` if adapter/skill model changed.
3. Append concise entry to `.okf/log.md`.
4. Create handoff `.okf/handoffs/YYYY-MM-DD-bootstrap-perplexity-propagation.md` with any remaining follow-ups.

### E. Optional (only if small)

- Extend `scripts/okf-sync-skills --list-skills` output or docs to distinguish `okf-*` vs `perplexity-okf-*` skill families.
- Add `.okf/tests/` evidence note after validation.

## Constraints

- Do not modify global Cursor user skills or external tool config outside this repo.
- Do not introduce network dependencies or nonstandard packages.
- Keep adapters thin; do not duplicate long skill bodies in `AGENTS.md`, `CLAUDE.md`, `PERPLEXITY.md`, or `.cursor/rules/okf.mdc`.
- Do not store secrets in OKF.
- Prefer editing canonical skills once, then running sync — do not hand-edit generated adapter footers except via sync script.
- MVP scope: document overflow; do not require automating Perplexity in `scripts/okf-dispatch` unless trivial.

## Validation (required before finishing)

From repository root:

```bash
scripts/okf-sync-skills
scripts/okf-sync-skills --dry-run
scripts/okf-validate
```

If scaffold script changed, smoke-test:

```bash
python3 skills/create-new-okf-project/scripts/create_okf_project.py /tmp/okf-perplexity-scaffold-test --name "Scaffold Test" --owner test
scripts/okf-validate   # run from test dir if applicable
```

Report any blocking validation failures and fix them.

## Expected output

Reply with:

1. **Summary** of what changed and why (bootstrap propagation for Perplexity).
2. **Files changed** (grouped: docs, scaffold, templates, skills, OKF concepts, scripts).
3. **Skill formatting** — confirm `perplexity-okf-*` extended frontmatter and `canonical_skill` pointers are preserved in scaffold output.
4. **Perplexity Project setup** — pointer to `docs/perplexity-project-files-and-skills.md` for Files + Skills attachment.
5. **Validation results** (`okf-validate`, scaffold smoke test if run).
6. **Remaining follow-ups** (e.g. Xcode step-4 guide, dispatch overflow metadata).

## OKF discipline during this task

- Link work to `.okf/features/shared-okf-skills.md` and Perplexity handoff concepts.
- Update `.okf/log.md` after substantive changes.
- Write a handoff if anything remains incomplete.
- Follow `skills/okf-concept-writer/SKILL.md` and `skills/okf-handoff-writer/SKILL.md` for OKF edits.
```
