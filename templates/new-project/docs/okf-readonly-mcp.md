# Read-Only OKF MCP Pilot

`scripts/okf-mcp-server` exposes curated `.okf` concepts through a local stdio MCP server. It is an optional query surface, not an OKF writer and not a replacement for Forge lifecycle MCPs.

## Tools

| Tool | Result |
|------|--------|
| `okf_bundle_summary` | Concept, type, status, and verification counts |
| `okf_search_concepts` | Text search with optional type/tag filters |
| `okf_read_concept` | One path-contained `.okf/*.md` concept |
| `okf_get_neighbors` | Incoming and outgoing concept links |
| `okf_list_types` | Deterministically ordered concept-type counts |
| `okf_list_tags` | Deterministically ordered tag counts |

Every tool is read-only, idempotent, local-only, and closed to paths outside `.okf`. The server exposes no write, mutation, shell, network, or secret-reading method.

## Protocol Boundary

The pilot supports the modern MCP `2026-07-28` stdio contract (`server/discover`, per-request `_meta`, deterministic complete results) and the legacy 2025 `initialize` flow for deployed clients. Stdout is reserved for newline-delimited JSON-RPC; diagnostics go to stderr.

The implementation is deliberately dependency-light and should remain a pilot until it has been exercised with the target MCP hosts. Do not advertise HTTP transport or authorization support.

The reviewed upstream boundary and links are recorded in `.okf/references/integration-protocol-boundaries.md`.
Follow `.okf/workflows/optional-integration-review.md` for enablement and evidence gates.

## Configure

Merge the `okf-readonly` entry from `.cursor/mcp-okf-readonly.json.example` into the host's MCP configuration. Do not replace the existing Forge entries.

Direct launch:

```bash
scripts/okf-mcp-server
```

Run the contract suite before enabling it in a generated project:

```bash
python3 tests/test_okf_mcp.py
scripts/okf-validate --strict
```

## Safety Contract

- Resolve all requested files against the repository root and require containment under `.okf`.
- Return only recognized concepts loaded by the shared OKF parser.
- Never write receipts, caches, indexes, logs, or generated files.
- Keep secret-bearing files, `.env`, and unrelated repository paths inaccessible.
- Treat MCP tool annotations as descriptive only; the server implementation enforces the boundary.
