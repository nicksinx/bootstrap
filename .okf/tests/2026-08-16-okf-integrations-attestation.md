---
type: Test Evidence
title: OKF Optional Integrations and Attestation Validation
description: Strict validation evidence for work package 4 covering the OpenWiki sidecar, read-only MCP pilot, attested computation, and scaffold propagation.
status: stable
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/tests/2026-08-16-okf-integrations-attestation.md
tags: [okf, validation, openwiki, mcp, attested-computation, pr-4]
applies_to: [cursor, claude, codex, local-agent, mcp]
sensitivity: internal
verification_status: tested
stale_after: 2026-11-14
generated: { by: process:codex, at: "2026-08-16T18:22:10+01:00" }
---

# Scope

Validate [the integration feature](../features/okf-integration-pilots.md), [curated-boundary decision](../decisions/0003-curated-okf-integration-boundary.md), and [review workflow](../workflows/optional-integration-review.md) across the bootstrap repository and generated projects.

# Stage Evidence

| Stage | Command / suite | Result | Strict coverage |
|-------|-----------------|--------|-----------------|
| MCP implementation | `python3 tests/test_okf_mcp.py` | PASS, 6 cases | Modern discovery/version/metadata validation, legacy initialize, deterministic six-tool catalog, queries, traversal rejection, symlink rejection before read, no repository byte changes |
| OpenWiki implementation | `python3 tests/test_openwiki_sidecar.py` | PASS, 5 cases | Default-off config, opt-in overlay, dry-run, staging import, adapter block preservation, atomic malformed-marker failure, `.okf` mutation rejection, generated-symlink rejection, concurrent-run lock |
| Attestation implementation | `python3 tests/test_attested_computation.py` | PASS, 4 cases | Byte-identical repeat receipts, valid verdict, altered digest failure, live concept-change failure, forbidden `.okf` output, symlink rejection, strict concept validation |
| Contract and syntax gate | `tests/test_contracts.py`, package `compileall`, `bash -n` | PASS | Project integration schema, Python and shell syntax |
| Canonical scaffolds | `tests/test_launch_smoke.py`, `tests/test_scaffold_consolidation.py` | PASS | Default and `--with-openwiki` projects validate themselves; root/template/runtime parity |
| Full release gate | `make check` | PASS | Entire historical and package 4 suite plus strict validator/migration/index/freshness/adapter checks |
| Published stack | GitHub Actions `bootstrap-ci / validate` on PRs #2-#5 | PASS | Each stacked merge ref executed its package-specific `make check` gate on Ubuntu with Python 3.11 |
| Whitespace and deterministic drift | `git diff --check`, `okf-index --check`, `okf-sync-skills --dry-run` | PASS | Patch hygiene, generated indexes, adapter preflight |

# Generated Project Smoke

The final OpenWiki-enabled canonical smoke project completed launch with:

- 367 files;
- 44 OKF concepts and 14 generated directory indexes;
- 17 copied project-local skills;
- successful modern MCP `server/discover` probe in `validate_launch.sh`;
- successful temporary deterministic attestation receipt outside `.okf`;
- `validate_launch: OK`.

The exact file and concept counts are informational because the launcher includes its own template source. Required artifact assertions and strict gates are the contract.

# Result

PASS. Each work-package slice passed focused negative tests before integration, the combined repository passed the complete release gate, and GitHub Actions passed across the four-PR stack. No live external OpenWiki CLI or third-party MCP host was required for this deterministic package gate; those remain explicit follow-up smokes.
