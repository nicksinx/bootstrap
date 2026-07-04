---
type: Decision
title: Use OKF as the Shared Context Substrate
description: Project-1 keeps durable project context in OKF and uses tool adapters as thin entrypoints.
status: active
lifecycle_stage: build
owner: project
source_of_truth: true
resource: .okf/decisions/0001-okf-as-context-substrate.md
tags: [okf, decision, context]
applies_to: [cursor, claude, codex, chatgpt, ollama, local-agent]
sensitivity: internal
verification_status: accepted
timestamp: 2026-06-24T15:54:09+01:00
---

# Decision

Project-1 shall use `.okf` as the shared curated context substrate and keep tool-specific files as thin adapters.

# Context

The requirements call for one shared OKF bundle that is portable, inspectable, version-controlled, and usable by humans and AI tools.

# Options Considered

1. Store all durable context in each tool adapter.
2. Store durable context in `.okf` and use adapters only as entrypoints.
3. Store durable context in an external knowledge platform.

# Rationale

Option 2 minimizes duplication, keeps context Git-native, and remains readable without proprietary tooling.

# Consequences

- Agents must read OKF before substantive work.
- Adapters need maintenance when OKF operating rules change.
- OKF updates should accompany material project changes.

# Reversal Conditions

Revisit this decision if an external system becomes the authoritative project context source and can export stable, reviewable, text-first artifacts.

# Related Concepts

- `.okf/requirements/okf-bootstrap-kit.md`
- `.okf/architecture/okf-bootstrap-layout.md`
