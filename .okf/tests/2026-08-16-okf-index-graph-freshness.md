---
type: Test Evidence
title: OKF Index, Graph, and Freshness Validation
description: Strict validation evidence for work package 3 covering deterministic indexes, graph exports, freshness checks, and scaffold propagation.
status: stable
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/tests/2026-08-16-okf-index-graph-freshness.md
tags: [okf, v0.2, index, graph, freshness, validation, pr-3]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: tested
stale_after: 2026-11-16
generated: { by: process:okf-index-graph-freshness, at: 2026-08-16T17:39:00+01:00 }
---

# Scope

Validate work package 3 against [the bootstrap requirement](../requirements/okf-bootstrap-kit.md), [the architecture](../architecture/okf-bootstrap-layout.md), and [the freshness workflow](../workflows/okf-index-graph-freshness-review.md).

# Test Matrix

| Command | Result | Coverage |
|---------|--------|----------|
| `python3 tests/test_okf_tooling.py` | PASS | Index idempotence/prose preservation/rollback, graph edges/HTML, freshness semantics and exits |
| `python3 tests/test_scaffold_consolidation.py` | PASS | Canonical and standalone tooling parity, generated index and freshness gates |
| `python3 tests/test_launch_smoke.py` | PASS | Fresh project emits and validates all navigation tools and nested indexes |
| `scripts/okf-index --write` followed by `--check --format json` | PASS | Live indexes converge with zero drift |
| `scripts/okf-visualize --as-of 2026-08-16 --format json` | PASS | Deterministic read-only concept graph export |
| Offline HTML structure and embedded JavaScript syntax check | PASS | Required DOM surfaces, executable script syntax, no external script/stylesheet dependency |
| `scripts/okf-freshness --as-of 2026-08-16 --check --format json` | PASS | No tracked concept is overdue; legacy untracked inventory remains visible |
| `make check` | PASS | Full repository suite plus strict index and freshness gates |
| Package-wide `compileall` and `git diff --check` | PASS | Python syntax and patch whitespace |

# Result

PASS. Generated index content is deterministic and author-safe, graph output is local and read-only, and freshness checks are explicit review signals. The live export contains 83 nodes and 20 internal edges. A fresh 330-file canonical scaffold contains 39 concepts, each with a current review deadline, the complete five-service operating material, and all three tooling commands.
