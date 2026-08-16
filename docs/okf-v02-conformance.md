# OKF v0.2 Conformance

Project Bootstrap emits and validates [Open Knowledge Format v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). The bootstrap profile adds operational fields such as `sensitivity`, `verification_status`, and `lifecycle_stage`; consumers must preserve unknown extension fields.

## Reserved files

- Root `.okf/index.md` may contain only `okf_version: "0.2"` in frontmatter.
- Nested `index.md` files have no frontmatter.
- Any `log.md` has no frontmatter and uses `## YYYY-MM-DD` headings, newest first.
- Every other Markdown file in `.okf/` is a concept and requires a non-empty `type`.

## Standard metadata

Use the v0.2 families for new or changed concepts:

```yaml
---
type: Requirement
title: Example requirement
status: stable
generated: { by: process:requirements-import, at: 2026-08-16T10:00:00Z }
verified:
  - { by: human:reviewer-id, at: 2026-08-16T12:00:00Z }
stale_after: 2026-11-16
sources:
  - id: source-spec
    resource: https://example.com/spec
---
```

- `status` is `draft`, `stable`, or `deprecated`; omission means stable.
- `generated.by` and `verified[].by` follow the OKF actor convention.
- `timestamp` is legacy v0.1 metadata. The normal validator warns; strict validation fails on the warning.
- Missing `verified` means unverified. Do not manufacture verification events during migration.
- Unknown `type` values and extension keys are accepted.

## Validation gates

```bash
scripts/okf-validate
scripts/okf-validate --strict
scripts/okf-validate --strict --format json
make check
```

The default command fails on structural and safety errors. `--strict` also fails on warnings and is the CI/release gate. PyYAML is required so nested maps, lists, quoted values, duplicate keys, and malformed YAML are handled by a real parser rather than line splitting.

Fresh projects run the same engine from `scripts/lib/okf_validation.py`. `scripts/validate_launch.sh` invokes strict OKF validation, so scaffold smoke tests cover the emitted bundle as well as the bootstrap repository.
