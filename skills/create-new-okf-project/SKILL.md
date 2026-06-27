---
name: create-new-okf-project
description: Create or bootstrap a new OKF-enabled software or agentic project. Use when an agent needs to scaffold a project folder with .okf, thin tool adapters, local OKF scripts, initial concepts, a continuous-improvement repository for lessons learned, five-service agent setup, Perplexity research/overflow material, and validation-ready OKF conventions.
---

# Create New OKF Project

Use this skill to start a new project that treats OKF as the durable context layer for LLM ops, software development, and cross-agent work.

## Workflow

1. Identify the target project path and project name. If the user gives a folder, use it.
2. Inspect the target path before writing. Do not overwrite existing files unless the user explicitly allows it.
3. Create the OKF scaffold with `.okf`, thin adapters, helper scripts, bundled skills, and starter concepts.
4. Include `.okf/improvements/` as the continuous-improvement repository from the beginning.
5. Include the canonical five-service setup order: Cursor, Codex, Claude Code, Xcode-connected Claude Agent, and Perplexity Desktop Pro.
6. Include Perplexity MODE A research and MODE B overflow prompts, workflows, adapter material, and project skills.
7. Run the generated validator when practical.
8. Tell the user which files were created and how to install or invoke any OKF skills.

## Preferred Script

Use the bundled script for a new local project:

```bash
python3 /path/to/create-new-okf-project/scripts/create_okf_project.py /path/to/new-project --name "Project Name"
```

Useful options:

```bash
--owner "team-or-person"
--overwrite
--no-adapters
--no-scripts
--no-skills
```

Use `--overwrite` only when the user explicitly allows replacing existing scaffold files.

## Bootstrap Kit Path

Run the scaffold script from the **OKF bootstrap kit repository** (Project-1 layout) when you need full five-service parity. The script copies optional files from the bootstrap tree via `copy_optional_bootstrap_files` (see `BOOTSTRAP_COPY_PATHS` in `create_okf_project.py`).

**Full-kit copy set (when bootstrap sources exist):**

| Category | Paths |
|----------|-------|
| Scripts | `scripts/okf-dispatch`, `scripts/okf-check-adapters` |
| Operator docs | `docs/okf-ways-of-working-brief.md`, `docs/okf-dispatch-orchestration.md`, `docs/configure-perplexity-okf.md`, `docs/perplexity-project-files-and-skills.md`, `docs/skill-frontmatter-compatibility.md` |
| Setup guides | `docs/create-new-okf-project-in-{cursor,codex,claude,xcode,perplexity}.md` |
| Handoffs / context | `.okf/handoffs/README.md`, `TEMPLATE.md`, `TEMPLATE-tester.md`, `TEMPLATE-reviewer.md`, `TEMPLATE-xcode-step4.md`, `.okf/context-packs/INDEX.md` |
| Perplexity prompt | `.okf/prompts/perplexity-post-curation-smoke-test.md` |
| Xcode step 4 | `.okf/prompts/xcode-step4-verification-checklist.md`, `.okf/handoffs/TEMPLATE-xcode-step4.md`, `.okf/risks/xcode-live-verification-pending.md` |
| Codex | `.codex/hooks.json`, `CODEX-SKILL-INSTALL.md` |

Bootstrap copies **replace embedded stubs** for the five-service setup guides and `docs/configure-perplexity-okf.md`.

If the script runs from a **minimal checkout** without those sibling paths, the embedded scaffold still creates core `.okf` concepts, adapters, scripts, bundled skills, and **short fallback stubs** for configure-perplexity and xcode/perplexity setup guides — but not the operator brief, dispatch scripts, or full setup guides. Point the user to the bootstrap kit for missing files.

After scaffold, instruct the user to run:

```bash
scripts/okf-sync-skills
scripts/okf-validate
scripts/okf-check-adapters
```

**Expected file count (full kit, default flags):** ~70 files (see `.okf/tests/2026-06-28-scaffold-parity.md`).

## Required Scaffold

Create:

- `.okf/index.md`
- `.okf/project.md`
- `.okf/log.md`
- `.okf/requirements/`
- `.okf/features/`
- `.okf/architecture/`
- `.okf/decisions/`
- `.okf/workflows/`
- `.okf/agents/`
- `.okf/prompts/`
- `.okf/risks/`
- `.okf/tests/`
- `.okf/releases/`
- `.okf/handoffs/`
- `.okf/references/`
- `.okf/improvements/`
- `AGENTS.md`
- `CLAUDE.md`
- `.cursor/rules/okf.mdc`
- `PERPLEXITY.md`
- `scripts/okf-validate`
- `scripts/okf-context-pack`
- `scripts/okf-handoff`
- `scripts/okf-sync-skills`
- `scripts/okf-dispatch` when available from the bootstrap kit
- `.claude/commands/okf-sync.md`
- `.codex/hooks.json` when available from the bootstrap kit
- `docs/shared-okf-skills.md`
- `docs/create-new-okf-project-in-cursor.md` when available from the bootstrap kit
- `docs/create-new-okf-project-in-codex.md` when available from the bootstrap kit
- `docs/create-new-okf-project-in-claude.md` when available from the bootstrap kit
- `docs/configure-perplexity-okf.md` (full version when bootstrap kit path; embedded stub otherwise)
- `docs/okf-dispatch-orchestration.md` when available from the bootstrap kit
- `docs/okf-ways-of-working-brief.md` when available from the bootstrap kit
- `docs/create-new-okf-project-in-perplexity.md` (full version when bootstrap kit path)
- `docs/create-new-okf-project-in-xcode.md` (full version when bootstrap kit path)
- `.okf/prompts/perplexity-post-curation-smoke-test.md` when available from the bootstrap kit
- `.okf/agents/xcode-claude.md`
- `.okf/agents/perplexity.md`
- `.okf/agents/perplexity-overflow.md`
- `.okf/prompts/perplexity-custom-instructions.md`
- `.okf/prompts/perplexity-deep-research-setup.md`
- `.okf/prompts/perplexity-overflow-failover.md`
- `.okf/workflows/multi-agent-delivery-pipeline.md`
- `.okf/workflows/perplexity-research-cycle.md`
- `.okf/workflows/perplexity-overflow-failover.md`
- `.okf/dispatch/ready/`
- `.okf/dispatch/running/`
- `.okf/dispatch/done/`
- `.okf/dispatch/failed/`
- `.okf/dispatch/pipelines/`
- `skills/` with bundled canonical OKF skills and Perplexity adapter skills when available

## Continuous Improvement

Every new OKF project must include `.okf/improvements/`.

Use it for:

- `Lesson Learned` concepts.
- `Improvement` concepts.
- `Retrospective` concepts.
- Reusable process changes that should later be promoted into templates, scripts, skills, adapters, or agent rules.

Improvement concepts should include:

- `# Observation`
- `# Context`
- `# Impact`
- `# Recommendation`
- `# Action Items`
- `# Related Concepts`
- `# Review Cadence`

## Perplexity Requirements

Every scaffold should make Perplexity usable without repository-wide file attachment:

- Custom instructions live at `.okf/prompts/perplexity-custom-instructions.md`.
- Project Files are curated OKF attachments, not the whole repo.
- Project Skills are the four `skills/perplexity-okf-*/SKILL.md` files.
- MODE A creates cited, unverified `Reference` concepts for `.okf/references/`.
- MODE B overflow completes the blocked runner's same OKF role contract and returns output for Cursor/Codex integration.
- Perplexity Computer is out of scope unless explicitly added later.

## Reference

Read `references/okf-project-profile.md` when the task requires explaining or manually recreating the scaffold.
