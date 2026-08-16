---
type: Attested Computation
title: Bootstrap OKF Bundle Integrity Experiment
description: Deterministically hashes curated OKF concept bytes and verifies an experimental receipt against the live bundle.
status: draft
lifecycle_stage: test
owner: project
source_of_truth: false
resource: .okf/computations/bootstrap-integrity.md
tags: [okf, attested-computation, integrity, experiment]
applies_to: [cursor, claude, codex, local-agent, mcp]
sensitivity: internal
verification_status: tested
stale_after: 2026-11-14
generated: { by: process:project-bootstrap, at: "2026-08-16T00:00:00Z" }
runtime: python3
parameters:
  - name: root
    type: path
    required: false
  - name: output
    type: path
    required: false
computation: scripts/attest/okf_bundle_digest.py
executor:
  resource: scripts/attest/okf_bundle_digest.py
  receipt: [experiment_version, okf_version, computation, algorithm, manifest, bundle_digest]
attester:
  resource: scripts/attest/verify_okf_bundle_digest.py
  receipt: [experiment_version, verdict, checks]
---

# Purpose

Exercise the OKF v0.2 `Attested Computation` structure with a deterministic, local computation. The computation covers every curated concept recognized by the shared OKF parser and excludes reserved generated indexes and `log.md`.

# Execution

```bash
scripts/okf-attest-experiment run
scripts/okf-attest-experiment verify
```

Receipts are written to `.okf-runtime/attestations/`, outside the curated bundle and ignored by Git.

# Experimental Boundary

The concept shape, runtime, computation, executor, and attester fields follow OKF v0.2. The receipt and verdict JSON fields are a Project Bootstrap experiment, not a claimed OKF standard or interoperability ABI.

# Acceptance

- Repeated runs over identical concept bytes produce byte-identical receipts.
- Any omitted, added, reordered, or changed concept causes verification to fail.
- Symlink concepts and receipt paths under `.okf` are rejected.
- No secrets, signatures, remote services, or claims of cryptographic identity are involved.
