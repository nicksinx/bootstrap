---
type: Reference
title: Integration Protocol Boundaries
description: Reviewed primary-source boundaries for OpenWiki sidecar ownership and modern plus legacy MCP stdio interoperability.
status: stable
lifecycle_stage: build
owner: project
source_of_truth: false
resource: .okf/references/integration-protocol-boundaries.md
tags: [okf, reference, openwiki, mcp, interoperability]
applies_to: [cursor, claude, codex, local-agent, mcp]
sensitivity: internal
verification_status: reviewed
stale_after: 2026-09-15
generated: { by: process:codex, at: "2026-08-16T00:00:00Z" }
sources:
  - id: mcp-2026-07-28
    resource: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/basic/transports/index.mdx
    title: MCP 2026-07-28 transport specification
    author: modelcontextprotocol/modelcontextprotocol
    usage_count: 2
    last_modified: 2026-07-28
  - id: mcp-tools-2026-07-28
    resource: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/server/tools.mdx
    title: MCP 2026-07-28 tools specification
    author: modelcontextprotocol/modelcontextprotocol
    usage_count: 2
    last_modified: 2026-07-28
  - id: openwiki-readme
    resource: https://github.com/langchain-ai/openwiki/blob/main/README.md
    title: OpenWiki README
    author: langchain-ai/openwiki
    usage_count: 2
---

# Reviewed Claims

- Modern MCP `2026-07-28` uses newline-delimited JSON-RPC over stdio, per-request protocol metadata, and `server/discover`; older deployed revisions use `initialize`. A pilot intended for mixed local hosts should exercise both eras.
- MCP tool catalogs should be deterministic. Read-only intent annotations improve disclosure but do not replace implementation-level path and method controls.
- OpenWiki code mode generates an `openwiki/` documentation tree and maintains bounded marker blocks in shared agent files while preserving content outside those blocks.
- OpenWiki's documented OKF output remains v0.1 at the time of review, so it must stay separate from the curated Project Bootstrap OKF v0.2 bundle.

# Local Decisions

- Run OpenWiki only in an isolated staging copy and import its documented sidecar outputs after checking that staged `.okf` was not mutated.
- Expose OKF through a first-party local MCP server with query tools only, path containment under `.okf`, and no network or secret access.
- Recheck these claims after `stale_after` because both upstream projects are active.
