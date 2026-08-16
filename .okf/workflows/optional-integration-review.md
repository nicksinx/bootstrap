---
type: Workflow
title: Optional Integration Review
description: Staged enablement and validation gates for OpenWiki, read-only OKF MCP, and experimental attested computation.
status: stable
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/workflows/optional-integration-review.md
tags: [okf, workflow, openwiki, mcp, attestation, validation]
applies_to: [cursor, claude, codex, local-agent, mcp]
sensitivity: internal
verification_status: tested
stale_after: 2026-11-14
generated: { by: process:codex, at: "2026-08-16T18:22:10+01:00" }
---

# Trigger

Use this workflow when enabling, upgrading, or reviewing any optional integration shipped by Project Bootstrap.

# Fixed Gates

1. **Select:** identify one integration and read its operator guide plus [the boundary decision](../decisions/0003-curated-okf-integration-boundary.md).
2. **Preflight:** confirm no secret will enter OKF, generated output, receipts, arguments, or committed configuration.
3. **Isolate:** keep generated writes in the documented sidecar or runtime path; query-only processes receive no mutation method.
4. **Exercise:** run the integration's focused positive and adversarial tests.
5. **Inspect:** review generated output or structured results; do not auto-promote them to requirements or decisions.
6. **Integrate:** Cursor, Codex, or the designated integrator applies any accepted durable change.
7. **Validate:** run `make check` in bootstrap or the generated project's launch/strict OKF gates.
8. **Record:** update the affected concept, `.okf/log.md`, test evidence, and handoff.

# Integration Checks

| Integration | Enablement | Required focused evidence | Promotion rule |
|-------------|------------|---------------------------|----------------|
| OpenWiki | Scaffold with `--with-openwiki`; install CLI outside repo | Staged `.okf` mutation, malformed marker, and symlink rejection | Generated wiki remains a sidecar; integrator promotes selected facts |
| Read-only MCP | Merge host config example manually | Modern/legacy protocol, exact tool list, traversal and symlink rejection, no `.okf` byte changes | Tool output is read context only |
| Attestation | Keep config disabled except during evaluation | Repeated receipt identity, tamper/live-change failure, forbidden `.okf` output | Verdict is local evidence, not identity or accepted project truth |

# Stop Conditions

- A tool requests or writes secrets.
- OpenWiki attempts to alter staged `.okf`.
- MCP exposes a write-like method or accesses an unrecognized path.
- A receipt is proposed for storage under `.okf`.
- Upstream protocol behavior no longer matches the reviewed reference.

On any stop condition, fail closed, preserve current curated state, record the issue, and require explicit review before retrying.
