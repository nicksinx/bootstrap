---
name: okf-context-pack-builder
description: Build compact task-specific context packs from Open Knowledge Format bundles and related project files. Use when an agent needs to assemble relevant OKF concepts, source snippets, tests, handoffs, and task instructions for large tasks, cross-agent handoff, local model workflows, or tools with smaller context windows.
---

# OKF Context Pack Builder

Use this skill for larger tasks or handoffs where the full project is too broad.

## Workflow

1. Read `.okf/index.md` and `.okf/project.md`.
2. Select only concepts relevant to the active task.
3. Include the latest relevant handoff.
4. Include applicable lessons learned from `.okf/improvements/`.
5. Include source and test snippets only when they materially affect the task.
6. Preserve status, lifecycle stage, sensitivity, and verification status.
7. State that the context pack is generated task context, not durable source-of-context.

Use `scripts/okf-context-pack` when the project provides it.

## Pack Shape

A useful pack usually contains:

- Task instruction.
- Active OKF concepts.
- Relevant handoff excerpts.
- Applicable improvements or lessons learned.
- Source or test snippets.
- Known risks.
- Required output format or validation commands.

## Guardrails

Keep the pack small enough for the target tool.

Do not include secrets.

Do not let generated context packs replace OKF concepts. Convert durable discoveries back into `.okf`.
