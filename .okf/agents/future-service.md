---
type: Agent Rule
title: Future Service OKF Adapter
description: Thin adapter template for services that participate in the shared OKF operating model.
status: stable
lifecycle_stage: operate
owner: project
source_of_truth: false
resource: .okf/agents/future-service.md
tags: [okf, adapter, future-service]
applies_to: [local-agent]
sensitivity: internal
verification_status: reviewed
stale_after: 2026-11-14
generated: { by: process:okf-sync-skills, at: "2026-08-16T18:18:56+01:00" }
---

# Future Service OKF Adapter

Use `.okf` as the shared project context layer.

Canonical OKF skill definitions live in `skills/*/SKILL.md`. Read the relevant skill before OKF-related delivery.

## Canonical OKF Skills

Canonical skill definitions live under `skills/*/SKILL.md`. Tool adapters stay thin and point here instead of duplicating skill bodies.


- `bootstrap-okf-forge-project` — >- (`skills/bootstrap-okf-forge-project/SKILL.md`)
- `claude-okf-operator` — Operate as Claude Code in OKF + Forge v2 projects — tester dispatch role and validation evidence. Use when Claude runs tests, reviews dispatch packets as tester, or completes tester-phase work. Does not wire Forge lifecycle MCPs (Cursor hosts Forge). (`skills/claude-okf-operator/SKILL.md`)
- `codex-okf-operator` — Operate as Codex in OKF + Forge v2 projects — builder/integrator dispatch, hooks, and OKF promotion. Use when Codex implements or integrates work, runs okf-dispatch, advances pipelines from Stop hooks, or ingests handoffs. Does not wire Forge lifecycle MCPs (Cursor hosts Forge). (`skills/codex-okf-operator/SKILL.md`)
- `create-new-okf-project` — Create or bootstrap an OKF v0.2 software or agentic project from the canonical Project Bootstrap launcher, with a standalone fallback. Use when an agent needs .okf context, migration and strict validation, five-service adapters, dispatch, Forge-ready scaffolding, Perplexity research/overflow, skills, handoffs, or continuous-improvement storage. (`skills/create-new-okf-project/SKILL.md`)
- `cursor-okf-operator` — Operate as Cursor in OKF + Forge v2 projects — reviewer dispatch role, Forge MCP lifecycle host, and OKF promotion integrator. Use when Cursor reviews work, runs Forge stage tools, promotes Forge artifacts to OKF, or consumes reviewer dispatch packets. (`skills/cursor-okf-operator/SKILL.md`)
- `okf-citation-steward` — Preserve, verify, and organize citations and external references in Open Knowledge Format bundles. Use when an agent needs to handle cited claims, vendor research, API references, market scans, legal or compliance notes, reference concepts, or external material that should not become accepted project knowledge without review. (`skills/okf-citation-steward/SKILL.md`)
- `okf-concept-writer` — Create or update Open Knowledge Format concept documents for software and agentic projects. Use when an agent needs to add requirements, features, architecture notes, decisions, workflows, risks, tests, releases, handoffs, references, agent rules, or tool adapters inside an .okf bundle. (`skills/okf-concept-writer/SKILL.md`)
- `okf-conformance-validator` — Validate an Open Knowledge Format v0.2 bundle and the local software-development profile. Use when an agent needs to check YAML frontmatter, reserved index/log files, provenance, trust, lifecycle, stale dates, Attested Computation contracts, profile extensions, likely secrets, links, or strict release readiness. (`skills/okf-conformance-validator/SKILL.md`)
- `okf-context-pack-builder` — Build compact task-specific context packs from Open Knowledge Format bundles and related project files. Use when an agent needs to assemble relevant OKF concepts, source snippets, tests, handoffs, and task instructions for large tasks, cross-agent handoff, local model workflows, or tools with smaller context windows. (`skills/okf-context-pack-builder/SKILL.md`)
- `okf-handoff-writer` — Write concise Open Knowledge Format handoff documents for paused, interrupted, context-limited, or transferred software and agentic project work. Use when an agent needs to create .okf/handoffs/YYYY-MM-DD-task.md with current state, completed work, decisions, changed files, known issues, next actions, and validation needs. (`skills/okf-handoff-writer/SKILL.md`)
- `okf-reader` — Load and triage an Open Knowledge Format bundle for software development or agentic project work. Use when an agent needs to read .okf/index.md, .okf/project.md, relevant concepts, recent handoffs, tool adapters, or decide what OKF context is safe to implement from. (`skills/okf-reader/SKILL.md`)
- `okf-requirements-auditor` — Audit Open Knowledge Format requirements and feature concepts for implementation readiness. Use when an agent needs to review .okf/requirements or .okf/features for clarity, acceptance criteria, dependencies, risks, verification status, traceability, contradictions, or missing test expectations. (`skills/okf-requirements-auditor/SKILL.md`)
- `okf-risk-scanner` — Scan software, architecture, agent workflows, OKF concepts, and handoffs for project risks. Use when an agent needs to identify security, privacy, reliability, delivery, context drift, tool-adapter drift, unverified-claim, secret-storage, compliance, release, or cross-agent handoff risks and record them in .okf/risks. (`skills/okf-risk-scanner/SKILL.md`)
- `perplexity-okf-citation-steward` — Produce cited external research for OKF Reference concepts in Perplexity Desktop Pro. Use when Perplexity runs MODE A deep research, vendor scans, compliance checks, or any task where web-backed claims must become draft .okf/references/ material with verification_status unverified. (`skills/perplexity-okf-citation-steward/SKILL.md`)
- `perplexity-okf-concept-writer` — Draft OKF concept documents from Perplexity Desktop Pro for Cursor or Codex to save. Use when Perplexity produces Reference concepts in MODE A research, OKF update drafts in MODE B integrator overflow, or structured concept output that must follow OKF frontmatter without becoming accepted truth until reviewed. (`skills/perplexity-okf-concept-writer/SKILL.md`)
- `perplexity-okf-handoff-writer` — Write OKF handoff and ingest blocks from Perplexity Desktop Pro when research or overflow work pauses or transfers to Cursor or Codex. Use when Perplexity completes MODE A research, MODE B overflow deliverables, or the user ends a session before repo changes are applied. (`skills/perplexity-okf-handoff-writer/SKILL.md`)
- `perplexity-okf-reader` — Load and triage OKF project context in Perplexity Desktop Pro before research or overflow work. Use when Perplexity needs to read attached project files, .okf/index.md, .okf/project.md, handoffs, and decide what context is safe to use for MODE A research or MODE B overflow. (`skills/perplexity-okf-reader/SKILL.md`)
- `xcode-okf-operator` — Operate as Xcode-connected Claude Agent in OKF + Forge v2 projects — Apple-platform dispatch consumer and integrator. Use when Xcode builds, tests, or completes platform-specific dispatch work. Does not wire Forge lifecycle MCPs (Cursor hosts Forge). (`skills/xcode-okf-operator/SKILL.md`)
Install or mirror this file for the target service, then run `scripts/okf-sync-skills --target all` after canonical skill changes.
