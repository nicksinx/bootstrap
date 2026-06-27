# Claude OKF Adapter

Use `.okf` as the shared source of curated project context across Cursor, Codex, Claude Code, Xcode-connected Claude Agent, and Perplexity Desktop Pro.

Canonical OKF skill definitions live in `skills/*/SKILL.md`. For OKF-related delivery, read and follow the relevant canonical skill instead of improvising workflows.

Read in this order before changing project files:

1. `.okf/index.md`
2. `.okf/project.md`
3. Relevant concepts linked from the task
4. Recent `.okf/handoffs/` notes
5. Tool adapter concepts under `.okf/agents/` when the task involves agent behavior
6. The matching canonical skill under `skills/` when the task matches an OKF skill contract

Prefer reviewed, tested, and accepted OKF concepts over draft or unverified material. Preserve citations and external references when updating concepts. If project state changes, update OKF and append a concise entry to `.okf/log.md`.

Create a handoff note before stopping if another agent may need to continue the work.

Perplexity Desktop Pro is service 5 for cited research and may be used in MODE B overflow when a primary runner is blocked. Cursor or Codex must apply Perplexity output and run validation.

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
