---
name: okf-handoff-writer
description: Write concise Open Knowledge Format handoff documents for paused, interrupted, context-limited, or transferred software and agentic project work. Use when an agent needs to create .okf/handoffs/YYYY-MM-DD-task.md with current state, completed work, decisions, changed files, known issues, next actions, and validation needs.
---

# OKF Handoff Writer

Use this skill before work is paused, transferred, or likely to lose context.

## File Location

Create handoffs under:

```text
.okf/handoffs/YYYY-MM-DD-short-task-name.md
```

Use `scripts/okf-handoff` when the project provides it.

## Required Sections

Include these sections:

- `# Current State`
- `# Completed Work`
- `# Decisions Made`
- `# Files Changed`
- `# Known Issues`
- `# Next Recommended Actions`
- `# Validation Needed`
- `# Context Pack`

## Content Rules

Write for the next agent, not for the transcript. Include enough detail to continue without rereading the whole conversation.

Prefer concrete paths, commands, test results, and remaining decisions. Keep speculation clearly marked.

Do not include secrets or private credentials. If a sensitive external dependency exists, describe where the approved secret store or owner is, not the secret value.

Append a short entry to `.okf/log.md` after creating a handoff.
