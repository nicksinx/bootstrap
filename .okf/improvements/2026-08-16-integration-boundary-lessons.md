---
type: Improvement
title: Optional Integration Boundary Lessons
description: Reusable lessons from adding generated documentation, read-only agent queries, and deterministic receipts without weakening curated OKF ownership.
status: stable
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/improvements/2026-08-16-integration-boundary-lessons.md
tags: [okf, improvement, openwiki, mcp, attestation, security]
applies_to: [cursor, claude, codex, local-agent, mcp]
sensitivity: internal
verification_status: reviewed
stale_after: 2026-11-14
generated: { by: process:codex, at: "2026-08-16T18:22:10+01:00" }
---

# Observation

Optional integrations create asymmetric risk: a useful generator can overwrite curated context, a nominally read-only server can still leak through path resolution, and a deterministic receipt can be mistaken for stronger attestation than it provides.

# Context

Work package 4 added an OpenWiki sidecar, a local MCP query pilot, and one OKF v0.2 `Attested Computation` after the core conformance, scaffold, and navigation packages were already stable.

# Impact

Without explicit ownership and adversarial gates, optional tooling can silently become a second source of truth. Positive smoke tests alone do not establish containment, atomicity, or the meaning of evidence.

# Recommendation

- Run third-party generators in a disposable working-tree copy and selectively import only documented outputs.
- Treat shared-file marker blocks as a two-owner merge contract; validate every selected adapter before writing any of them.
- Reject generated and source symlinks at trust boundaries so containment checks do not follow external targets.
- Enforce read-only behavior through the concrete method catalog and filesystem resolution, not MCP annotations alone.
- Support protocol eras deliberately when a current specification changed handshakes recently; test both current and deployed-client flows.
- Omit clocks from deterministic receipts, hash a complete sorted manifest, and store output outside the input knowledge tree.
- Label local receipt schemas as experiments unless an official interoperability contract exists.
- Put negative cases into launch and CI gates so scaffold propagation cannot drop the boundary silently.

# Action Items

- Run a disposable live smoke with the official OpenWiki CLI before promoting that integration beyond optional status.
- Exercise the MCP pilot with the target hosts or official Inspector and record host/version evidence.
- Re-review `.okf/references/integration-protocol-boundaries.md` by its short freshness deadline.
- Keep read/write MCP and production attestation out of scope until authorization, concurrency, audit, identity, and standard receipt semantics are decided.

# Related Concepts

- [Boundary decision](../decisions/0003-curated-okf-integration-boundary.md)
- [Integration feature](../features/okf-integration-pilots.md)
- [Validation evidence](../tests/2026-08-16-okf-integrations-attestation.md)

# Review Cadence

Review after any upstream OpenWiki or MCP protocol upgrade, before adding a new write-capable integration, and no later than `stale_after`.
