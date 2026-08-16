---
type: Handoff
title: Work Package 4 - Optional Integrations and Attestation
description: Completed the bounded OpenWiki sidecar, read-only OKF MCP pilot, deterministic attestation experiment, scaffold propagation, and strict release gates.
status: stable
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/handoffs/2026-08-16-okf-integrations-attestation.md
tags: [okf, handoff, openwiki, mcp, attestation, pr-4]
applies_to: [cursor, claude, codex, local-agent, mcp]
sensitivity: internal
verification_status: tested
stale_after: 2026-11-14
generated: { by: process:codex, at: "2026-08-16T18:22:10+01:00" }
---

# Current State

Work package 4 is implementation-complete on `agent/okf-v02-04-integrations-attestation`, stacked on work package 3. The focused suites and combined `make check` release gate pass. This is the final implementation branch in the four-package stack.

# Completed Work

- Added `--with-openwiki`, integration configuration, an operator instructions overlay, and an isolated staging/import wrapper.
- Made OKF adapter generation preserve one valid OpenWiki-owned block and fail before any write on malformed ownership markers.
- Added a six-tool, path-contained, read-only stdio MCP server supporting modern `2026-07-28` discovery and deployed legacy initialization flows.
- Added a spec-valid deterministic `Attested Computation`, executor, attester, convenience wrapper, ignored runtime path, and experimental receipt/verdict contract.
- Added reviewed primary-source boundaries, a durable integration decision, feature acceptance criteria, and a fixed review workflow.
- Propagated scripts, docs, configuration, concepts, schemas, Make targets, launch validation, and tests through canonical scaffolds and the creation skill.

# Decisions Made

- Curated `.okf` has one integrator-controlled write path; generated sidecars, query services, and runtime receipts do not write it directly.
- OpenWiki is optional and external. Its current documented OKF v0.1 behavior does not redefine the curated v0.2 bundle.
- The MCP pilot remains local stdio and read-only; HTTP, authentication, remote deployment, and mutations are out of scope.
- The attested concept shape follows OKF v0.2, while its receipt/verdict ABI is explicitly a Project Bootstrap experiment.

# Files Changed

Primary changes are in `scripts/openwiki-sidecar`, `mcp_server/okf_readonly_server.py`, `scripts/okf-mcp-server`, `scripts/lib/okf_attestation.py`, `scripts/attest/`, `scripts/okf-attest-experiment`, `scripts/launch_project.sh`, `scripts/validate_launch.sh`, `templates/`, `schemas/project.schema.json`, `tests/`, operator docs, and linked `.okf/` concepts.

# Known Issues

- The official OpenWiki CLI was not installed or invoked in the deterministic suite; a contract-faithful fake exercised output and failure boundaries.
- The MCP wire contract is unit-tested but has not yet been recorded against every target host or the official Inspector.
- Receipt/verdict JSON is not signed, remotely attested, replay-protected, or standardized.
- External protocol claims have a short review deadline because upstream projects are active.

# Next Recommended Actions

1. Merge the stacked work packages in order after CI and review: conformance, migration/scaffold, navigation/freshness, then integrations/attestation.
2. Run the documented disposable OpenWiki live smoke with no secrets in the repository.
3. Exercise `.cursor/mcp-okf-readonly.json.example` with target MCP hosts and record host/version evidence.
4. Keep integration pilots disabled or opt-in until their live smoke evidence is accepted.

# Validation Needed

Completed: focused positive/adversarial suites, canonical and OpenWiki-enabled scaffold validation, full `make check`, strict OKF validation, migration/index/freshness/adapter checks, compilation, shell syntax, and whitespace gates. Re-run after conflict resolution, rebases, or upstream protocol changes.

# Context Pack

- [Requirement](../requirements/okf-bootstrap-kit.md)
- [Architecture](../architecture/okf-bootstrap-layout.md)
- [Feature](../features/okf-integration-pilots.md)
- [Decision](../decisions/0003-curated-okf-integration-boundary.md)
- [Workflow](../workflows/optional-integration-review.md)
- [Validation evidence](../tests/2026-08-16-okf-integrations-attestation.md)
- [Lessons learned](../improvements/2026-08-16-integration-boundary-lessons.md)
