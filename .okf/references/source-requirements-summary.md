---
type: Reference
title: Source Requirements Summary
description: Summary of the draft OKF Companion Requirements used to create Project-1.
status: active
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/source-requirements-summary.md
tags: [okf, requirements, source]
applies_to: [cursor, claude, codex, chatgpt, ollama, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# Summary

The source requirements define OKF as a shared, Git-native, human-readable context layer for software development and agentic workflows.

# Key Requirements Represented

- Keep one primary OKF bundle per project.
- Use tool adapters that point back to OKF.
- Include local profile frontmatter on concept documents.
- Maintain controlled but extensible concept types.
- Require pre-task context loading, implementation traceability, post-task updates, and handoffs.
- Provide reusable skills for OKF reading, writing, handoffs, audits, citations, risks, context packs, and validation.
- Include validator, context pack, and handoff scripts.
- Add a continuous-improvement repository for lessons learned, retrospectives, and reusable process improvements.

# Local Interpretation

Project-1 implements the first milestone as a local bootstrap kit with `.okf`, `templates/`, `scripts/`, and `skills/`.
