---
name: create-new-okf-project
description: Create or bootstrap an OKF v0.2 software or agentic project from the canonical Project Bootstrap launcher, with a standalone fallback. Use when an agent needs .okf context, migration and strict validation, five-service adapters, dispatch, Forge-ready scaffolding, Perplexity research/overflow, skills, handoffs, or continuous-improvement storage.
---

# Create New OKF Project

Use this skill to start a new project that treats OKF as the durable context layer for LLM ops, software development, and cross-agent work.

## Workflow

1. Identify the target project path and project name. If the user gives a folder, use it.
2. Inspect the target path before writing. Do not overwrite existing files unless the user explicitly allows it.
3. Prefer the canonical Project Bootstrap launcher; use the embedded fallback only when the bootstrap repository is unavailable or omission flags are required.
4. Include `.okf/improvements/` as the continuous-improvement repository from the beginning.
5. Include the canonical five-service setup order: Cursor, Codex, Claude Code, Xcode-connected Claude Agent, and Perplexity Desktop Pro.
6. Include Perplexity MODE A research and MODE B overflow prompts, workflows, adapter material, and project skills.
7. Run `scripts/okf-migrate --check` and `scripts/okf-validate --strict`.
8. Tell the user which files were created and how to install or invoke any OKF skills.

## Preferred Script

Use the bundled script for a new local project:

```bash
python3 /path/to/create-new-okf-project/scripts/create_okf_project.py /path/to/new-project --name "Project Name"
```

Useful options:

```bash
--owner "team-or-person"
--profile default
--bootstrap-root /path/to/bootstrap
--overwrite
--embedded-fallback
--no-adapters
--no-scripts
--no-skills
```

Use `--overwrite` only when the user explicitly allows replacing existing scaffold files.

## Bootstrap Kit Path

When the Project Bootstrap repository is discoverable, the skill script delegates to `scripts/launch_project.sh`. That launcher is the canonical template source and preserves the display name and OKF owner while deriving a safe project id. Use `--bootstrap-root` when auto-discovery is ambiguous.

The canonical launcher renders `templates/new-project/`, copies schemas/profiles/skills/runtime libraries, generates all service adapters, initializes Git, and runs launch validation.

**Fallback augmentation set (when fallback is selected inside the bootstrap repository):**

| Category | Paths |
|----------|-------|
| Scripts | `scripts/okf-dispatch`, `scripts/okf-check-adapters`, `scripts/okf-migrate` |
| Operator docs | `docs/okf-ways-of-working-brief.md`, `docs/okf-dispatch-orchestration.md`, `docs/configure-perplexity-okf.md`, `docs/perplexity-project-files-and-skills.md`, `docs/skill-frontmatter-compatibility.md`, `docs/okf-v02-conformance.md` |
| Setup guides | `docs/create-new-okf-project-in-{cursor,codex,claude,xcode,perplexity}.md` |
| Handoffs / context | `.okf/handoffs/README.md`, `TEMPLATE.md`, `TEMPLATE-tester.md`, `TEMPLATE-reviewer.md`, `TEMPLATE-xcode-step4.md`, `.okf/context-packs/INDEX.md` |
| Perplexity prompt | `.okf/prompts/perplexity-post-curation-smoke-test.md` |
| Xcode step 4 | `.okf/prompts/xcode-step4-verification-checklist.md`, `.okf/handoffs/TEMPLATE-xcode-step4.md`, `.okf/risks/xcode-live-verification-pending.md` |
| Codex | `.codex/hooks.json`, `CODEX-SKILL-INSTALL.md` |

The embedded fallback is intentionally smaller. It carries the same v0.2 validator/migrator runtime and five-service core, but it does not promise every Forge or operator artifact from the canonical launcher.

If the script runs from an installed skill without the bootstrap repository, it announces the fallback on stderr. Use `--embedded-fallback` to select that behavior explicitly when the repository is present.

After scaffold, instruct the user to run:

```bash
scripts/okf-sync-skills
scripts/okf-migrate --check
scripts/okf-validate --strict
scripts/okf-check-adapters
```

**Expected file count (canonical default scaffold):** approximately 260 files, including the self-contained template source and 17 project-local skills. Treat the exact count as informational; validate required paths and strict checks instead.

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
- `scripts/okf-validate --strict`
- `scripts/okf-migrate`
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
