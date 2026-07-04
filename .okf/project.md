---
type: Project
title: Project-1 OKF Bootstrap Kit
description: Reusable OKF project scaffold with adapters, scripts, shared skills, and five-service LLM ops setup.
status: active
lifecycle_stage: build
owner: project
source_of_truth: true
resource: .okf/project.md
tags: [okf, software-development, agentic-workflows, shared-skills, perplexity]
applies_to: [cursor, claude, codex, chatgpt, xcode-claude, perplexity, ollama, mcp, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# Project-1 OKF Bootstrap Kit

## Purpose

Project-1 turns the draft OKF companion requirements into a reusable local project kit.

The kit provides:

- A primary `.okf` bundle for curated project context.
- Thin tool adapters for Codex, Claude Code, Cursor, and Perplexity.
- Helper scripts for validation, handoffs, and context packs.
- Bundled OKF skills for project-local use and Codex installation.
- Four Perplexity-specific project skills for Desktop Pro research and overflow.
- Xcode-connected Claude Agent setup material for Apple-platform dispatch work.
- Template OKF files for future projects.
- A continuous-improvement repository for lessons learned over the life of a project.

## Scope

In scope:

- Human-readable Markdown OKF concepts with local profile frontmatter.
- Agent operating rules for reading, updating, validating, and handing off OKF context.
- Installable Codex skills under `skills/`.
- Local scripts under `scripts/`.
- Perplexity custom-instruction, project-file, and project-skill setup docs.
- Five-service setup order: Cursor, Codex, Claude Code, Xcode, Perplexity.
- Manual Perplexity overflow behavior when a primary runner is blocked.
- Lessons learned, retrospectives, and improvement actions under `.okf/improvements/`.

Out of scope:

- Replacing source code, tests, issue trackers, OpenAPI documents, formal contracts, or secrets management.
- Proprietary knowledge platforms.
- Live MCP server implementation.

## Operating Model

OKF is the source of curated context. It references executable or authoritative artifacts rather than replacing them.

Tool adapters remain thin and point agents back to `.okf`.

Durable project knowledge should not live only in chat.

Perplexity Desktop Pro is service 5 for cited deep research into `.okf/references/` and a manual overflow substitute when Cursor, Codex, Claude Code, or Xcode is blocked. It never writes the repository directly; Cursor or Codex ingests Perplexity output and validates.
