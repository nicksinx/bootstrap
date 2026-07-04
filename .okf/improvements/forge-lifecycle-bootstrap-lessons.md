---
type: Improvement
title: Forge Lifecycle Bootstrap Lessons
description: Durable lessons from Project-1 Forge+OKF integration harness, promoted to bootstrap toolkit.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/improvements/forge-lifecycle-bootstrap-lessons.md
tags: [okf, forge, bootstrap, lessons-learned, mcp, integration]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-07-04T01:40:00+01:00
---

# Context

Project-1 (`/Users/dv/Projects/testrunner/Project-1`) served as the **integration harness** wiring all `nicksinx/*Forge` MCP repos via OKF operator docs, Cursor launchers, promotion checklists, and vertical-slice smoke evidence. This document captures reusable scaffold lessons promoted into [nicksinx/bootstrap](https://github.com/nicksinx/bootstrap) as the `forge-lifecycle` profile.

# Three-layer model

| Layer | Repo | Role |
|-------|------|------|
| Forge MCP servers | `nicksinx/ConceptForge`, `LaunchForge`, … | One MCP per lifecycle stage; pushed independently |
| Integration harness | Project-1 | Proof, policy, promotion checklists, E2E evidence |
| New-project scaffold | `nicksinx/bootstrap` | `forge-lifecycle` profile — what product projects inherit |

# Lessons promoted to bootstrap

## 1. Sibling clone layout

Clone Forge repos as **peers** of the product project (`../ConceptForge`), not vendored submodules inside the product repo.

- Launchers default `*_ROOT` to `../<RepoName>`.
- Helper: `scripts/forge-clone-siblings.sh` in `forge-lifecycle` overlay.
- Documented in `.okf/references/forge-sibling-layout.md` (generated projects).

## 2. Bash MCP launchers in `scripts/`

Cursor `mcp.json` should reference bash wrappers, not raw `node` paths with env vars.

- Resolves sibling paths, version pins, workspace dirs, contracts assertion.
- LaunchForge exception: entry at `mcp-server/dist/index.js`.
- ForgeRelay: additional `FORGERELAY_WORKSPACE`, `FORGERELAY_PROJECT_ROOT`, stricter tag pinning.

## 3. Gitignored Forge workspaces

Runtime Forge state lives under `.okf/forge/<stage>/` — **not** OKF concepts until integrator promotion.

Added to default `.gitignore.tmpl` for all scaffolds (harmless when Forge unused).

## 4. Option C integration policy

OKF substrate + Forge lifecycle engine + **one-way** promotion after review. Forge is **not** a sixth bootstrap service.

- Decision concept: `.okf/decisions/0002-okf-forge-integration.md` (overlay).
- Operator guide: `docs/forge-lifecycle-integration.md` (slim; full spec remains in Project-1 harness).

## 5. Cursor MCP config template

`.cursor/mcp-forge-lifecycle.json.example` lists all eleven Forge servers. Auto-copied to gitignored `.cursor/mcp.json` when profile is `forge-lifecycle`.

## 6. Packet registry reference

`.okf/references/forge-packet-type-registry.md` — producer/consumer/OKF ingest routing. Copied from harness; update when new packet types ship.

# Validation evidence (harness)

Post-launch spine proven in Project-1 sibling smokes (2026-07-04):

| Handoff | Smoke |
|---------|-------|
| `launch_operations_handoff` → OperateForge | `smoke:launch-to-operate` |
| `launch_customer_handoff` → CustomerForge | `smoke:launch-to-customer` |
| `launch_growth_handoff` → GrowthForge | `smoke:launch-to-growth` |
| `launch_revenue_handoff` → RevenueForge | `smoke:launch-to-revenue` |
| `lifecycle_evidence_bundle` → InsightForge | `smoke:customer-to-insight` |
| `sunset_candidate` → SunsetForge | `smoke:operate-to-sunset` |

Bootstrap smoke: `tests/test_launch_smoke.py::test_forge_lifecycle_launch_and_validate`.

# What stays in Project-1 (not bootstrap)

- Full integration spec: `docs/okf-forge-integration-spec.md`
- Per-server agent guides: `.okf/agents/*forge*.md`
- Promotion checklists: `.okf/workflows/forge-*-promotion-checklist.md`
- Vertical-slice evidence: `.okf/tests/2026-07-04-*-vertical-slice-evidence.md`
- Adversarial review dossiers and prompts

Promote additional harness material into bootstrap **only after** it stabilizes and applies to every new product project.

# Open follow-ups

- `retirement_evidence_bundle` cross-MCP E2E (still `contract_only` in registry)
- Phase 4.3–4.4 contradiction handling and governance adversarial prompt (harness spec)
- Optional: fold slim promotion checklist stubs into bootstrap overlay

# Related

- Profile: `profiles/forge-lifecycle.yaml`
- Overlay templates: `templates/forge-lifecycle/`
- Harness: Project-1 `docs/okf-forge-integration-spec.md`
