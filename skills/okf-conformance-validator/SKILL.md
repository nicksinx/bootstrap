---
name: okf-conformance-validator
description: Validate an Open Knowledge Format bundle against the local software development OKF profile. Use when an agent needs to check .okf documents for frontmatter, required type fields, ISO timestamps, sensitivity, verification status, reserved files, likely secrets, broken internal links, and soft warnings versus blocking failures.
---

# OKF Conformance Validator

Use this skill before commits, releases, handoffs, or large OKF refactors.

## Validation Steps

1. Locate `.okf`.
2. Run `scripts/okf-validate` when available.
3. Check every non-reserved Markdown concept has YAML frontmatter.
4. Check every concept has a non-empty `type`.
5. Check project-critical concepts include `status`, `lifecycle_stage`, `sensitivity`, and `verification_status`.
6. Check timestamps are ISO 8601 values.
7. Scan for likely secrets.
8. Report broken internal links as warnings unless project policy says otherwise.
9. Preserve unknown fields instead of rejecting them.

Treat `Improvement`, `Lesson Learned`, and `Retrospective` as project-critical concept types because they can change future agent behavior.

## Result Categories

Use:

- `Failure`: blocks commit or release.
- `Warning`: should be reviewed, but does not normally block.
- `Info`: quality suggestion.

Secret detection failures should block unless the user explicitly confirms an approved exception.

## Follow-up

After fixing validation issues, rerun the validator and record the result in `.okf/log.md` or a `Test Evidence` concept.
