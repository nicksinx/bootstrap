# OKF Index, Graph, and Freshness Tooling

Project Bootstrap provides deterministic, local tooling for navigating an OKF v0.2 bundle. All three commands are read-only by default except the explicit index `--write` mode.

## Deterministic indexes

```bash
scripts/okf-index --check
scripts/okf-index --write
scripts/okf-index --check --format json
```

The command creates or refreshes an `index.md` in each OKF directory that contains concepts. It owns only the content between `<!-- OKF-INDEX:BEGIN -->` and `<!-- OKF-INDEX:END -->`; operator-authored prose outside those markers is preserved. Root `index.md` retains its v0.2 frontmatter, while nested indexes have no frontmatter.

Index generation parses every concept before the first write, writes atomically, sorts by repository path, and is idempotent. A malformed concept or one-sided marker prevents all writes.

If a directory already has a case-variant landing page such as the legacy `INDEX.md`, the generator links to that file and does not create or modify lowercase `index.md`. This keeps behavior identical on case-sensitive and case-insensitive filesystems and avoids self-links.

## Concept graph

```bash
scripts/okf-visualize --format json --output /tmp/okf-graph.json
scripts/okf-visualize --format html --output /tmp/okf-graph.html
```

The graph contains concept nodes and resolvable internal Markdown-link edges. Nodes expose lifecycle status, verification state, `stale_after`, and calculated freshness. JSON is intended for automation; HTML is a self-contained, read-only operator view with no CDN or network dependency.

Use `--as-of YYYY-MM-DD` for reproducible freshness calculations in tests and audits.

## Freshness inventory

```bash
scripts/okf-freshness
scripts/okf-freshness --check
scripts/okf-freshness --verbose
scripts/okf-freshness --check --require-deadlines --format json
```

`--check` exits nonzero when a non-deprecated concept is past `stale_after`. Missing deadlines are summarized as `untracked`; use `--verbose` to list them. They fail only when `--require-deadlines` is selected. Deprecated concepts are reported separately and never count as stale.

Freshness is a review signal, not an automatic trust promotion or content deletion rule. Review and update the concept through the normal OKF workflow.
