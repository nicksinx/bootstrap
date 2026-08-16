---
name: okf-conformance-validator
description: Validate an Open Knowledge Format v0.2 bundle and the local software-development profile. Use when an agent needs to check YAML frontmatter, reserved index/log files, provenance, trust, lifecycle, stale dates, Attested Computation contracts, profile extensions, likely secrets, links, or strict release readiness.
---

# OKF Conformance Validator

Use this skill before commits, releases, handoffs, or large OKF refactors.

## Validation Steps

1. Locate `.okf`.
2. Run `scripts/okf-validate --strict` when available.
3. Parse frontmatter with a real YAML parser and reject duplicate keys.
4. Check every concept has a non-empty `type`.
5. Check root/nested `index.md` and `log.md` reserved-file rules.
6. Check `status`, `generated`, `verified`, `sources`, and `stale_after` when present.
7. Check Project Bootstrap profile fields such as `sensitivity` and `verification_status` without confusing them with standard trust metadata.
8. Check Attested Computation executor and deterministic attester contracts.
9. Scan for likely secrets; report broken links as tolerated warnings.
10. Preserve unknown types and fields instead of rejecting them.

Treat `Improvement`, `Lesson Learned`, and `Retrospective` as project-critical concept types because they can change future agent behavior.

## Result Categories

Use:

- `Failure`: blocks commit or release.
- `Warning`: should be reviewed, but does not normally block.
- `Info`: quality suggestion.

Secret detection failures should block unless the user explicitly confirms an approved exception.

## Follow-up

After fixing validation issues, rerun `scripts/okf-migrate --check` and `scripts/okf-validate --strict`, then record the result in `.okf/log.md` or a `Test Evidence` concept.
