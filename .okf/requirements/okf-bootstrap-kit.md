---
type: Requirement
title: OKF Bootstrap Kit
description: Project-1 shall provide a reusable OKF bootstrap kit for software and agentic projects.
status: active
lifecycle_stage: build
owner: project
source_of_truth: true
resource: .okf/requirements/okf-bootstrap-kit.md
tags: [okf, requirement, bootstrap]
applies_to: [cursor, claude, codex, chatgpt, ollama, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# Intent

Create a reusable starter kit that makes OKF practical for future software development and agentic workflows.

# Requirement

Project-1 shall contain an operational OKF bundle, thin tool adapters, helper scripts, and Codex-installable skills that implement the local Software Development OKF Profile.

# Acceptance Criteria

1. `.okf/index.md` exists.
2. `.okf/project.md` exists.
3. Tool adapters exist for Codex, Claude, and Cursor.
4. At least one requirement, architecture, decision, risk, handoff, and test concept exists.
5. A continuous-improvement repository exists under `.okf/improvements/`.
6. `scripts/okf-validate` exists.
7. Agents have a clear reading order.
8. Agents have rules for updating OKF.
9. Handoff documents are created at task boundaries.
10. Project-critical concepts include status, lifecycle stage, sensitivity, and verification status.
11. No durable project decision is stored only in chat.
12. External claims are represented through reference concepts or citations.

# Dependencies

- Local file system access to the project directory.
- Python 3 for helper scripts.
- Codex skill directory for installing reusable skills.

# Risks

- Tool adapters may drift from `.okf` if copied and edited manually.
- Generated context packs may become stale if retained as durable knowledge.
- Secrets may be accidentally added to OKF documents.

# Verification

Run `scripts/okf-validate` and validate each skill with the Codex skill validator.

# Citations

- Source requirements: `.okf/references/source-requirements-summary.md`
