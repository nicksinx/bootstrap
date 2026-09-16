# Forge collection MCP (Cursor Desktop and Cloud Agents)

Bootstrap v2 products wire Cursor to **HTTP `forge-collection`** on Vercel. That host is a **map/gateway**, not a copy of the Forge stage servers.

**URL:** `https://forge-collection-mcp-server-nicksinxs-projects.vercel.app/api/mcp`

Do **not** vendor Forge server source into bootstrap or generated product repos. Bearer auth (`MCP_BEARER_TOKEN`) is **on hold** — templates must not require it.

## Desktop vs Cloud

| Client | Where to register | Sees `~/.cursor/mcp.json`? |
|--------|-------------------|----------------------------|
| Cursor Desktop | Settings → MCP (user) **and/or** project `.cursor/mcp.json` | Yes (user MCP) |
| Cursor Cloud Agents | Custom HTTP MCP on [cursor.com/agents](https://cursor.com/agents) | **No.** Cloud does not inherit Desktop MCP |

Vercel going live does not add the server to a shared Customization list. Desktop and Cloud do not share one MCP page. Do not use SSE / `mcp-remote` for this host.

Generated projects:

- Commit `.cursor/mcp-forge-lifecycle.json.example` (HTTP collection).
- Auto-write gitignored `.cursor/mcp.json` from that example.
- Keep `.cursor/mcp-forge-stdio-siblings.json.example` for the **Node-host** path only.

## What actually runs Forge

Sibling clones (`scripts/forge-clone-siblings.sh`) plus `npm ci && npm run build` on a **Node host** (Mac next to the product, a Cloud Agent environment snapshot, or an always-on runtime). Stdio launchers: `scripts/*-mcp.sh`.

| Need | Running |
|------|---------|
| Catalog / packet map | Vercel `/api/mcp` |
| Cloud emit/import | Vercel **and** reachable runtime (`FORGE_RUNTIME_URL`) |
| Desktop local stdio only | Sibling `dist/` + stdio example — Vercel optional |

Docker is optional packaging of a runtime, not a second required product.

## Related

- Generated operator guide: `docs/forge-lifecycle-integration.md`
- Sibling layout: `.okf/references/forge-sibling-layout.md`
- Host: [nicksinx/forge-collection-mcp-server](https://github.com/nicksinx/forge-collection-mcp-server)
