---
type: Decision
title: Curated OKF Integration Boundary
description: External generators and query services must remain outside the curated OKF write path unless an integrator explicitly promotes reviewed output.
status: stable
lifecycle_stage: build
owner: project
source_of_truth: true
resource: .okf/decisions/0003-curated-okf-integration-boundary.md
tags: [okf, decision, openwiki, mcp, attestation, boundary]
applies_to: [cursor, claude, codex, local-agent, mcp]
sensitivity: internal
verification_status: reviewed
stale_after: 2026-11-14
generated: { by: process:codex, at: "2026-08-16T00:00:00Z" }
---

# Context

Generated wikis, agent query servers, and computation receipts add useful navigation and verification surfaces. Allowing those integrations to write curated `.okf` concepts directly would bypass provenance, review, strict validation, and the existing integrator role.

# Decision

- OpenWiki is opt-in and runs against an isolated staging copy. Only `openwiki/` and complete OpenWiki-owned blocks in shared adapter files may be imported. Any staged `.okf` mutation or generated symlink fails closed.
- The first-party OKF MCP pilot exposes deterministic query tools only. It rejects paths and symlinks outside the recognized `.okf` concept set and has no write, network, shell, or secret-access method.
- Attestation receipts and verdicts are runtime artifacts under `.okf-runtime/`, never concepts under `.okf`. The receipt ABI is explicitly experimental.
- Cursor, Codex, or another authorized integrator remains responsible for reviewing and promoting useful external output into OKF, followed by strict validation.

# Consequences

- Curated project truth retains one controlled write path.
- Optional integrations can be removed without migrating core OKF concepts.
- Sidecar and protocol tooling requires focused boundary tests in addition to normal happy-path tests.
- Generated wiki content and passing local receipts are evidence aids, not accepted requirements or cryptographic identity claims.

# Alternatives Considered

- Direct OpenWiki output into `.okf`: rejected because the documented upstream mode and local curated profile have different ownership and version contracts.
- Read/write MCP concept tools: deferred until authorization, concurrency, audit, and review semantics are specified.
- Receipts stored beside concepts: rejected because generated runtime churn would contaminate durable project memory.

# Related Concepts

- [Integration pilots](../features/okf-integration-pilots.md)
- [Protocol reference](../references/integration-protocol-boundaries.md)
- [Bootstrap requirement](../requirements/okf-bootstrap-kit.md)
