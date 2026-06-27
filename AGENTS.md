# Codex OKF Adapter

This repository uses `.okf` as the durable shared project context layer for Cursor, Codex, Claude Code, Xcode-connected Claude Agent, and Perplexity Desktop Pro.

Canonical OKF skill definitions live in `skills/*/SKILL.md`. For OKF-related delivery, read and follow the relevant canonical skill instead of improvising workflows.

Before substantive project changes:

1. Read `.okf/index.md`.
2. Read `.okf/project.md`.
3. Read relevant requirement, feature, architecture, decision, risk, test, and handoff concepts.
4. Check for recent files in `.okf/handoffs/`.
5. Treat `deprecated`, `superseded`, and `archived` concepts as unsafe for direct implementation unless the user explicitly asks for historical work.
6. Use `skills/okf-reader/SKILL.md` when triage is needed.

During implementation:

1. Link material work to an OKF requirement, feature, decision, runbook, or handoff.
2. Prefer `reviewed`, `tested`, and `accepted` concepts over `draft` or `unverified` concepts.
3. Do not invent durable requirements that are not represented in OKF.
4. Keep secrets, credentials, private keys, and sensitive personal data out of OKF.
5. Update tests in line with OKF acceptance criteria.
6. Follow the matching canonical skill under `skills/` for concept writing, handoffs, audits, risks, citations, context packs, and validation.

After substantive changes:

1. Update affected OKF concepts.
2. Append to `.okf/log.md`.
3. Add test evidence when validation was performed.
4. Create a handoff in `.okf/handoffs/` when work is paused, transferred, or context is likely to be lost.

Perplexity Desktop Pro is service 5 for cited research and an ad hoc overflow substitute when a primary runner is blocked. Perplexity never writes the repository directly; Cursor or Codex ingests output and validates OKF.

## Canonical OKF Skills

Canonical skill definitions live under `skills/*/SKILL.md`. Tool adapters stay thin and point here instead of duplicating skill bodies.


- `create-new-okf-project` — Create or bootstrap a new OKF-enabled software or agentic project. Use when an agent needs to scaffold a project folder with .okf, thin tool adapters, local OKF scripts, initial concepts, a continuous-improvement repository for lessons learned, five-service agent setup, Perplexity research/overflow material, and validation-ready OKF conventions. (`skills/create-new-okf-project/SKILL.md`)
- `okf-citation-steward` — Preserve, verify, and organize citations and external references in Open Knowledge Format bundles. Use when an agent needs to handle cited claims, vendor research, API references, market scans, legal or compliance notes, reference concepts, or external material that should not become accepted project knowledge without review. (`skills/okf-citation-steward/SKILL.md`)
- `okf-concept-writer` — Create or update Open Knowledge Format concept documents for software and agentic projects. Use when an agent needs to add requirements, features, architecture notes, decisions, workflows, risks, tests, releases, handoffs, references, agent rules, or tool adapters inside an .okf bundle. (`skills/okf-concept-writer/SKILL.md`)
- `okf-conformance-validator` — Validate an Open Knowledge Format bundle against the local software development OKF profile. Use when an agent needs to check .okf documents for frontmatter, required type fields, ISO timestamps, sensitivity, verification status, reserved files, likely secrets, broken internal links, and soft warnings versus blocking failures. (`skills/okf-conformance-validator/SKILL.md`)
- `okf-context-pack-builder` — Build compact task-specific context packs from Open Knowledge Format bundles and related project files. Use when an agent needs to assemble relevant OKF concepts, source snippets, tests, handoffs, and task instructions for large tasks, cross-agent handoff, local model workflows, or tools with smaller context windows. (`skills/okf-context-pack-builder/SKILL.md`)
- `okf-handoff-writer` — Write concise Open Knowledge Format handoff documents for paused, interrupted, context-limited, or transferred software and agentic project work. Use when an agent needs to create .okf/handoffs/YYYY-MM-DD-task.md with current state, completed work, decisions, changed files, known issues, next actions, and validation needs. (`skills/okf-handoff-writer/SKILL.md`)
- `okf-reader` — Load and triage an Open Knowledge Format bundle for software development or agentic project work. Use when an agent needs to read .okf/index.md, .okf/project.md, relevant concepts, recent handoffs, tool adapters, or decide what OKF context is safe to implement from. (`skills/okf-reader/SKILL.md`)
- `okf-requirements-auditor` — Audit Open Knowledge Format requirements and feature concepts for implementation readiness. Use when an agent needs to review .okf/requirements or .okf/features for clarity, acceptance criteria, dependencies, risks, verification status, traceability, contradictions, or missing test expectations. (`skills/okf-requirements-auditor/SKILL.md`)
- `okf-risk-scanner` — Scan software, architecture, agent workflows, OKF concepts, and handoffs for project risks. Use when an agent needs to identify security, privacy, reliability, delivery, context drift, tool-adapter drift, unverified-claim, secret-storage, compliance, release, or cross-agent handoff risks and record them in .okf/risks. (`skills/okf-risk-scanner/SKILL.md`)
- `perplexity-okf-citation-steward` — Produce cited external research for OKF Reference concepts in Perplexity Desktop Pro. Use when Perplexity runs MODE A deep research, vendor scans, compliance checks, or any task where web-backed claims must become draft .okf/references/ material with verification_status unverified. (`skills/perplexity-okf-citation-steward/SKILL.md`)
- `perplexity-okf-concept-writer` — Draft OKF concept documents from Perplexity Desktop Pro for Cursor or Codex to save. Use when Perplexity produces Reference concepts in MODE A research, OKF update drafts in MODE B integrator overflow, or structured concept output that must follow OKF frontmatter without becoming accepted truth until reviewed. (`skills/perplexity-okf-concept-writer/SKILL.md`)
- `perplexity-okf-handoff-writer` — Write OKF handoff and ingest blocks from Perplexity Desktop Pro when research or overflow work pauses or transfers to Cursor or Codex. Use when Perplexity completes MODE A research, MODE B overflow deliverables, or the user ends a session before repo changes are applied. (`skills/perplexity-okf-handoff-writer/SKILL.md`)
- `perplexity-okf-reader` — Load and triage OKF project context in Perplexity Desktop Pro before research or overflow work. Use when Perplexity needs to read attached project files, .okf/index.md, .okf/project.md, handoffs, and decide what context is safe to use for MODE A research or MODE B overflow. (`skills/perplexity-okf-reader/SKILL.md`)
Generated by `scripts/okf-sync-skills` for Project-1.
