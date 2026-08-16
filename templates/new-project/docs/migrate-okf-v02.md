# Migrate an OKF Bundle to v0.2

Use the migration command before enabling strict validation on an existing bundle.

```bash
scripts/okf-migrate --check
scripts/okf-migrate --apply --strict
scripts/okf-migrate --check
scripts/okf-validate --strict
```

`--check` is read-only and exits `1` when migration is needed. `--apply` plans every file first, refuses all writes if any concept cannot be parsed, writes changed files atomically, and validates the result. A second check must report no changes.

## Automatic changes

- Root `index.md` frontmatter becomes only `okf_version: "0.2"`.
- Nested `index.md` frontmatter is removed.
- `log.md` frontmatter is removed; dated headings are normalized and sorted newest first.
- `timestamp` becomes `generated` with the `--actor` value.
- `active` becomes `stable`.
- `superseded` and `archived` become `deprecated`, with the old value preserved in `project_bootstrap.legacy_status`.
- Existing unknown types, extension fields, nested YAML, and Markdown bodies are preserved.

## Deliberately manual

Migration does not invent `verified` events, convert a body citations section into `sources`, choose `stale_after`, or infer an Attested Computation contract. Review those semantics after the mechanical migration.

Use `--format json` for CI or inventory tooling. Use `--actor process:<id>` or another valid OKF actor when the default `process:okf-migrate` is not specific enough.
