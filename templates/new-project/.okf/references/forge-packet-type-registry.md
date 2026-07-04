---
type: Reference
title: Forge and OKF Packet Type Registry
description: Producer → consumer → OKF ingest target for lifecycle envelopes, relay, dispatch, and overflow.
status: active
lifecycle_stage: build
owner: project
source_of_truth: true
resource: .okf/references/forge-packet-type-registry.md
tags: [okf, forge, contracts, registry, phase-1, dispatch, relay]
applies_to: [cursor, codex, claude, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-07-04T00:10:00+01:00
---

# Summary

Registry of packet and artifact types across Forge portfolio, ForgeRelay, and OKF layers. Schema authority: lifecycle → `ForgeLifecycleContracts/SPEC.md` §5; relay → §6; OKF dispatch → `scripts/okf_dispatch_schema.py`.

# Lifecycle envelope packets (signed JSON)

From `compatibilityBoundaries` — transport: signed envelope between Forge MCP servers.

| packetType | Producer | Consumer | OKF ingest target | Status |
|------------|----------|----------|-------------------|--------|
| `concept_build_decision` | ConceptForge | BuildForge | `.okf/requirements/` draft | **server E2E** (see `.okf/tests/2026-07-04-concept-build-vertical-slice-evidence.md`) + compatibility fixtures |
| `build_launch_candidate` | BuildForge | LaunchForge | `.okf/releases/`, test evidence | **server E2E** — `smoke:build-to-launch` |
| `concept_launch_handoff` | ConceptForge | LaunchForge | `.okf/handoffs/` note | legacy |
| `launch_operations_handoff` | LaunchForge | OperateForge | `.okf/handoffs/` + operate runbooks | **server E2E** — `smoke:launch-to-operate` |
| `launch_customer_handoff` | LaunchForge | CustomerForge | `.okf/features/` draft | **server E2E** — `smoke:launch-to-customer` |
| `launch_growth_handoff` | LaunchForge | GrowthForge | `.okf/references/` | **server E2E** — `smoke:launch-to-growth` |
| `launch_revenue_handoff` | LaunchForge | RevenueForge | `.okf/references/` | **server E2E** — `smoke:launch-to-revenue` |
| `lifecycle_evidence_bundle` | any Forge | InsightForge | `.okf/improvements/` | **server E2E** — `smoke:customer-to-insight` |
| `governance_evidence_bundle` | any Forge | GovernanceForge | `.okf/decisions/`, `.okf/risks/` | import + policy-bundle smoke 2026-07-04 |
| `governance_policy_bundle` | GovernanceForge | BuildForge | `.okf/decisions/` | **server E2E** — `smoke:governance-to-build` |
| `iteration_recommendation` | InsightForge | ConceptForge / BuildForge | `.okf/improvements/` | contract_only |
| `sunset_candidate` | any Forge | SunsetForge | `.okf/handoffs/` | **server E2E** — `smoke:operate-to-sunset` |
| `retirement_evidence_bundle` | SunsetForge | GovernanceForge / InsightForge | `.okf/handoffs/` archive | contract_only — see Phase 6.3 cross-check |

# Relay packets (INT-001A — NOT lifecycle envelopes)

Transport: local JSON in `.okf/forge/relay/` via ForgeRelay MCP.

| packetType | Producer | Consumer | OKF cross-link | Canonical truth |
|------------|----------|----------|---------------|-----------------|
| `implementation` | ForgeRelay | Target coding tool | `relay_session_id` in handoff | `.okf/handoffs/` |
| `research` | ForgeRelay | Research tool | same | `.okf/handoffs/` + citations |
| `review` | ForgeRelay | Review tool | same | `.okf/handoffs/` |
| `session` | ForgeRelay | Same/different tool | same | `.okf/handoffs/` |
| `blocked` | ForgeRelay | Operator / next tool | same + `blockedReason` | `.okf/handoffs/` |

# OKF dispatch packets (NOT Forge contracts)

Transport: `.okf/dispatch/{ready,running,done}/` JSON files.

| Role | Producer | Consumer | OKF artifact | Advance mechanism |
|------|----------|----------|--------------|-----------------|
| `builder` | `okf-dispatch init` / `complete` | Configured runner | Handoff in `complete --result-json` | `complete` only |
| `tester` | dispatch on builder `complete` | Configured runner | same | `complete` only |
| `reviewer` | dispatch | Configured runner | same | `complete` only |
| `integrator` | dispatch | Configured runner | same | `complete` only |

# Perplexity overflow (NOT Forge contracts)

Transport: overflow command metadata + MODE B output.

| Trigger | Producer | Consumer | OKF cross-link fields |
|---------|----------|----------|----------------------|
| Usage limit, substitute deliverable | `okf-dispatch overflow` | Perplexity | `overflow_packet_id`, `primary_runner`, `failover_reason` |

# Operator rule

Choose layer by **trigger** (see `docs/okf-dispatch-orchestration.md` § Trigger-keyed decision matrix), not by tool name.

# Related

- `.okf/references/forge-envelope-okf-frontmatter-map.md`
- `.okf/decisions/0003-forgerelay-dispatch-coexistence.md`
- `ForgeLifecycleContracts/SPEC.md` §2, §5, §6
