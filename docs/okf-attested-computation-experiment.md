# OKF Attested Computation Experiment

Project Bootstrap includes one deterministic `Attested Computation` at `.okf/computations/bootstrap-integrity.md`. It demonstrates the OKF v0.2 concept shape while keeping the receipt/verdict transport explicitly experimental.

Follow `.okf/workflows/optional-integration-review.md` for enablement and evidence gates.

## Run

```bash
scripts/okf-attest-experiment run
scripts/okf-attest-experiment verify
```

The default receipt is `.okf-runtime/attestations/okf-bundle-receipt.json`. Runtime output is ignored by Git and must never be placed under `.okf`.

Direct executor and attester calls are also available:

```bash
scripts/attest/okf_bundle_digest.py --output /tmp/okf-receipt.json
scripts/attest/verify_okf_bundle_digest.py /tmp/okf-receipt.json
```

## Deterministic Scope

The executor uses the shared strict OKF parser to enumerate concepts. For each concept it records the repo-relative path and SHA-256 of the exact file bytes, path-sorts the manifest, and hashes canonical JSON for the bundle digest. Reserved generated `index.md` files and `.okf/log.md` are outside the concept set.

The attester requires an exact manifest match against the current bundle. It rejects missing, additional, reordered, duplicate, changed, or symlinked concepts, as well as altered receipt metadata or digest values.

## What This Does Not Prove

- The experimental receipt is not a signature and establishes no actor identity.
- It does not provide remote attestation, trusted hardware, transparency logging, or replay protection.
- The receipt/verdict JSON is not asserted to be an official OKF transport ABI.
- A passing verdict proves only that the receipt matches the local curated concept set at verification time.

Production interoperability should wait for a reviewed ecosystem convention or official extension. Until then, keep this feature disabled in `project.config.yaml` and use it only for local evaluation.
