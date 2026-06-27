---
type: Reference
title: OKF Bundle Index
description: Navigation index for the Project-1 OKF bootstrap kit.
status: active
lifecycle_stage: build
owner: project
source_of_truth: true
resource: .okf/index.md
tags: [okf, index, bootstrap]
applies_to: [cursor, claude, codex, chatgpt, xcode-claude, perplexity, ollama, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# OKF Bundle Index

Project-1 is a reusable OKF bootstrap kit for software development and agentic projects.

## Required Reading Order

1. Read this file.
2. Read `.okf/project.md`.
3. Read `docs/okf-ways-of-working-brief.md` for the operator summary.
4. Read relevant concepts for the active task.
5. Check `.okf/handoffs/` for recent continuity notes.
6. Prefer reviewed, tested, and accepted concepts over draft or unverified concepts.

## Core Concepts

- Project overview: `.okf/project.md`
- Primary requirement: `.okf/requirements/okf-bootstrap-kit.md`
- Shared skills feature: `.okf/features/shared-okf-skills.md`
- Legacy alias: `.okf/features/codex-okf-skills.md`
- Architecture: `.okf/architecture/okf-bootstrap-layout.md`
- Decision: `.okf/decisions/0001-okf-as-context-substrate.md`
- Workflow: `.okf/workflows/agent-okf-lifecycle.md`
- Multi-agent dispatch: `.okf/workflows/multi-agent-delivery-pipeline.md`
- Perplexity research: `.okf/workflows/perplexity-research-cycle.md`
- Perplexity overflow: `.okf/workflows/perplexity-overflow-failover.md`
- Xcode agent rule: `.okf/agents/xcode-claude.md`
- Risk: `.okf/risks/secret-storage-and-memory-drift.md`
- Continuous improvement: `.okf/improvements/continuous-improvement-repository.md`
- Validation plan: `.okf/tests/okf-validation-plan.md`
- Initial release: `.okf/releases/2026-06-24-initial-bootstrap.md`
- Current handoff: `.okf/handoffs/2026-06-28-dispatch-ergonomics.md`
- Prior handoff: `.okf/handoffs/2026-06-28-xcode-step4-dry-verification.md`
- Prior handoff: `.okf/handoffs/2026-06-28-scaffold-parity.md`

## Tool Adapters

- Codex adapter: `AGENTS.md`
- Claude adapter: `CLAUDE.md`
- Cursor adapter: `.cursor/rules/okf.mdc`
- Perplexity adapter: `PERPLEXITY.md`
- Xcode agent rule: `.okf/agents/xcode-claude.md`
- Perplexity agent rules: `.okf/agents/perplexity.md`, `.okf/agents/perplexity-overflow.md`
- OKF agent rules: `.okf/agents/`
- Lessons learned and improvements: `.okf/improvements/`

## Shared Skills

- **Operator brief:** `docs/okf-ways-of-working-brief.md`
- Operating model: `docs/shared-okf-skills.md`
- Perplexity configuration: `docs/configure-perplexity-okf.md`
- Perplexity Files and Skills: `docs/perplexity-project-files-and-skills.md`
- Skill frontmatter: `docs/skill-frontmatter-compatibility.md`
- Handoffs guide: `.okf/handoffs/README.md`
- Dispatch test evidence: `.okf/tests/2026-06-28-dispatch-dry-run.md`
- Context packs: `.okf/context-packs/INDEX.md`
- Research references: `.okf/references/` (2026-06-27 Perplexity research pack)
- Sync adapters: `scripts/okf-sync-skills`

## New Project Setup Guides

- Step 1, Cursor: `docs/create-new-okf-project-in-cursor.md`
- Step 2, Codex: `docs/create-new-okf-project-in-codex.md`
- Step 3, Claude Code: `docs/create-new-okf-project-in-claude.md`
- Step 4, Xcode: `docs/create-new-okf-project-in-xcode.md`, `.okf/prompts/xcode-step4-verification-checklist.md`
- Step 5, Perplexity: `docs/create-new-okf-project-in-perplexity.md`, `docs/configure-perplexity-okf.md`
- Codex bootstrap update prompt: `.okf/prompts/codex-update-okf-bootstrap-perplexity-integration.md`
- Codex GitHub publish prompt: `.okf/prompts/codex-update-github-bootstrap-repo.md`
- Codex share ways of working: `.okf/prompts/codex-share-okf-ways-of-working-updates.md`
- ProcureLex research (application): `.okf/prompts/perplexity-procurelex-research.md`
- Post-curation smoke test: `.okf/prompts/perplexity-post-curation-smoke-test.md`
- Xcode step 4 dry verification: `.okf/prompts/xcode-step4-verification-checklist.md`

## Local Commands

- Validate OKF: `scripts/okf-validate`
- Build context pack: `scripts/okf-context-pack`
- Create handoff: `scripts/okf-handoff`
- Sync tool adapters from canonical skills: `scripts/okf-sync-skills`
- Dispatch multi-agent work: `scripts/okf-dispatch`
- Check adapter drift: `scripts/okf-check-adapters`

## Dispatch

- Orchestration guide: `docs/okf-dispatch-orchestration.md`
- Queue root: `.okf/dispatch/{ready,running,done,failed}/`
- Codex Stop hook: `.codex/hooks.json`
