---
type: Reference
title: Forge Signing Keys Operator Runbook (OQ-2)
description: Where Forge envelope and approval-receipt keys live relative to OKF git; env layout, rotation, and per-server docs.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/references/forge-signing-keys-operator-runbook.md
tags: [okf, forge, signing, keys, security, oq-2, runbook]
applies_to: [cursor, codex, claude, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-07-04T02:30:00+01:00
---

# Summary

Forge signing and approver keys **never** belong in OKF git or committed Forge workspace artifacts. Operators store keys on the host (or secret manager) and point MCP launchers via environment variables.

# Layout

| Asset | Location | Git |
|-------|----------|-----|
| Ed25519 **private** signing keys | Operator path, e.g. `~/.forge/keys/<server>/<key-id>.pem` | **Never** |
| Trusted **public** keys JSON | Operator path, e.g. `~/.forge/trusted-public-keys.json` | **Never** (may ship example templates only) |
| Trusted **approver** public keys JSON | Operator path, e.g. `~/.forge/trusted-approvers.json` | **Never** |
| Forge workspace (`FORGE_WORKSPACE`) | Temp or per-product dir outside repo | **Gitignored** when under `.okf/forge/` |
| OKF promoted concepts | `.okf/requirements/`, `.okf/decisions/`, etc. | Committed after human review |

Sibling Forge repos (typical harness layout):

```text
../ForgeLifecycleContracts
../ConceptForge … ../SunsetForge
```

Project-1 MCP launchers: `scripts/*-mcp.sh` — set env before `node dist/index.js`.

# Environment variables

## Consumers (import signed envelopes)

| Variable | Purpose |
|----------|---------|
| `FORGE_REQUIRE_SIGNED_ENVELOPES` | `true` in production — reject unsigned imports |
| `FORGE_TRUSTED_KEYS_PATH` | JSON map: `{ "<signer>": { "<keyId>": "<PEM public>" } }` |

## Emitters (outbound packets)

| Variable | Purpose |
|----------|---------|
| `FORGE_SIGNING_KEY_ID` | Key id recorded on envelope authenticity |
| `FORGE_SIGNING_PRIVATE_KEY_PATH` | Ed25519 private PEM for `sourceServer` |

## Human approval receipts

| Variable | Purpose |
|----------|---------|
| `FORGE_TRUSTED_APPROVER_KEYS_PATH` | Approver public keys for receipt verification |

Separate from envelope signing — see decision 0004.

# Trusted keys file (example shape)

```json
{
  "conceptforge": { "conceptforge-prod-1": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n" },
  "sunsetforge": { "sunsetforge-prod-1": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n" }
}
```

Each consumer adds **only** upstream producers it accepts. Smokes generate ephemeral keys under `/tmp` — do not reuse smoke keys in production.

# Rotation

1. Generate new key pair; add new public key to all downstream `FORGE_TRUSTED_KEYS_PATH` files **before** switching emitters.
2. Update emitter `FORGE_SIGNING_KEY_ID` + private path.
3. Retire old public key after no in-flight packets reference old `keyId`.
4. Approval receipt keys rotate independently via `FORGE_TRUSTED_APPROVER_KEYS_PATH`.

# Promotion gate (LCF-2)

Before promoting Forge-sourced OKF Decisions to `verification_status: accepted`:

```bash
scripts/okf-check-forge-receipts --receipt path/to/receipt.json
```

Or invoke `forge-verify-receipt` from `@forge-lifecycle/contracts` when Node and trusted approver keys are available. `scripts/okf-validate` checks presence only (decision 0004).

# Per-server docs

| Server | Doc |
|--------|-----|
| ConceptForge | `ConceptForge/docs/signing-keys.md` |
| BuildForge | `BuildForge/docs/signing-keys.md` |
| LaunchForge | `LaunchForge/docs/signing-keys.md` |
| GovernanceForge | `GovernanceForge/docs/signing-keys.md` |
| OperateForge | `OperateForge/docs/signing-keys.md` |
| CustomerForge | `CustomerForge/docs/signing-keys.md` |
| GrowthForge | `GrowthForge/docs/signing-keys.md` |
| RevenueForge | `RevenueForge/docs/signing-keys.md` |
| InsightForge | `InsightForge/docs/signing-keys.md` |
| SunsetForge | `SunsetForge/docs/signing-keys.md` |

# Related

- `.okf/workflows/okf-forge-lifecycle-bridge.md` § Secrets and PII
- `.okf/decisions/0004-approval-receipt-verification.md`
- `docs/okf-forge-integration-spec.md` §9.2
