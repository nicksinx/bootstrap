---
name: okf-reader
description: Load and triage an Open Knowledge Format bundle for software development or agentic project work. Use when an agent needs to read .okf/index.md, .okf/project.md, relevant concepts, recent handoffs, tool adapters, or decide what OKF context is safe to implement from.
---

# OKF Reader

Use this skill before substantive work in an OKF-enabled project.

## Workflow

1. Locate the nearest `.okf` directory from the working directory upward.
2. Read `.okf/index.md`.
3. Read `.okf/project.md`.
4. Read relevant requirement, feature, architecture, decision, workflow, risk, test, release, reference, improvement, and agent-rule concepts for the task.
5. Check `.okf/handoffs/` for the most recent continuity note.
6. Check `.okf/improvements/` for applicable lessons learned.
7. Note any relevant concepts with `status: draft`, `deprecated`, `superseded`, or `archived`.
8. Prefer concepts with `verification_status: reviewed`, `tested`, or `accepted`.

## Context Triage

Report only the task-relevant facts:

- Active requirements and acceptance criteria.
- Current decisions and architecture constraints.
- Relevant risks and safety limits.
- Applicable lessons learned or process improvements.
- Recent handoff notes.
- Missing or unverified concepts that affect implementation.

## Safety Rules

Do not treat deprecated, superseded, or archived concepts as current guidance unless the user asks for historical analysis.

Do not copy secrets, credentials, private keys, or sensitive personal data into summaries or generated concepts.

If a task cannot be traced to an OKF requirement, feature, decision, runbook, or handoff, create or request an OKF concept before implementation.
