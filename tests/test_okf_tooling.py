"""Deterministic OKF index, graph, and freshness tests."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

from okf_tooling import (  # noqa: E402
    INDEX_BEGIN,
    ToolingError,
    apply_indexes,
    freshness_report,
    graph_html,
    graph_report,
    plan_indexes,
)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def concept(kind: str, title: str, stale_after: str | None = None, body: str = "") -> str:
    deadline = f"stale_after: {stale_after}\n" if stale_after else ""
    return f"""---
type: {kind}
title: {title}
description: Description for {title}.
status: stable
verification_status: reviewed
{deadline}generated: {{ by: process:test, at: 2026-08-16T10:00:00Z }}
---
# {title}

{body}
"""


def bundle(root: Path) -> None:
    write(
        root / ".okf" / "index.md",
        '---\nokf_version: "0.2"\n---\n\n# Authored Index\n\nKeep this operator note.\n',
    )
    write(root / ".okf" / "log.md", "# Log\n\n## 2026-08-16\n\n- Test.\n")
    write(
        root / ".okf" / "features" / "alpha.md",
        concept("Feature", "Alpha", "2026-08-15", "See [Zeta](../requirements/zeta.md)."),
    )
    write(
        root / ".okf" / "features" / "beta.md",
        concept("Feature", "Beta", "2026-08-16"),
    )
    write(
        root / ".okf" / "requirements" / "zeta.md",
        concept("Requirement", "Zeta"),
    )


def test_indexes_are_idempotent_and_preserve_authored_content() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-index-") as td:
        root = Path(td)
        bundle(root)
        first = plan_indexes(root)
        if first.errors or len(first.changes) != 3:
            raise AssertionError(first)
        apply_indexes(first)
        root_index = (root / ".okf" / "index.md").read_text()
        if "Keep this operator note." not in root_index or root_index.count(INDEX_BEGIN) != 1:
            raise AssertionError(root_index)
        nested = (root / ".okf" / "features" / "index.md").read_text()
        if nested.startswith("---") or nested.index("alpha.md") > nested.index("beta.md"):
            raise AssertionError(nested)
        second = plan_indexes(root)
        if second.errors or second.changes:
            raise AssertionError(second)


def test_malformed_marker_prevents_all_writes() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-index-invalid-") as td:
        root = Path(td)
        bundle(root)
        path = root / ".okf" / "index.md"
        path.write_text(path.read_text() + "\n" + INDEX_BEGIN + "\n")
        before = path.read_text()
        plan = plan_indexes(root)
        if not plan.errors:
            raise AssertionError(plan)
        try:
            apply_indexes(plan)
        except ToolingError:
            pass
        else:
            raise AssertionError("expected write refusal")
        if path.read_text() != before:
            raise AssertionError("index changed after failed plan")


def test_case_variant_index_is_a_compatibility_landing_page() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-index-case-") as td:
        root = Path(td)
        write(
            root / ".okf" / "index.md",
            '---\nokf_version: "0.2"\n---\n# Root\n',
        )
        write(root / ".okf" / "log.md", "# Log\n")
        landing = root / ".okf" / "context-packs" / "INDEX.md"
        write(landing, concept("Reference", "Legacy Landing"))
        before = landing.read_text()
        plan = plan_indexes(root)
        if plan.errors or plan.expected != 1 or len(plan.changes) != 1:
            raise AssertionError(plan)
        apply_indexes(plan)
        root_index = (root / ".okf" / "index.md").read_text()
        if "context-packs/INDEX.md" not in root_index:
            raise AssertionError(root_index)
        if landing.read_text() != before:
            raise AssertionError("case-variant landing page was modified")
        if (root / ".okf" / "context-packs" / "index.md").exists() and not landing.samefile(
            root / ".okf" / "context-packs" / "index.md"
        ):
            raise AssertionError("lowercase collision was created")
        if plan_indexes(root).changes:
            raise AssertionError("case-variant plan did not converge")


def test_graph_and_freshness_are_deterministic() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-graph-") as td:
        root = Path(td)
        bundle(root)
        as_of = dt.date(2026, 8, 16)
        graph = graph_report(root, as_of)
        if graph["summary"] != {"nodes": 3, "edges": 1}:
            raise AssertionError(graph["summary"])
        edge = graph["edges"][0]
        if edge["source"] != ".okf/features/alpha.md" or edge["target"] != ".okf/requirements/zeta.md":
            raise AssertionError(edge)
        report = freshness_report(root, as_of)
        if report["summary"] != {
            "total": 3,
            "tracked": 2,
            "current": 1,
            "stale": 1,
            "untracked": 1,
            "deprecated": 0,
        }:
            raise AssertionError(report["summary"])
        if graph_report(root, as_of) != graph:
            raise AssertionError("graph output is not deterministic")
        page = graph_html(graph)
        if "https://" in page or "const DATA=" not in page or "OKF concept graph" not in page:
            raise AssertionError("HTML export is not self-contained")
        if "[n.title+'\\n'+n.id" not in page:
            raise AssertionError("HTML export contains an invalid JavaScript newline escape")


def test_freshness_cli_check_exit_codes() -> None:
    with tempfile.TemporaryDirectory(prefix="okf-freshness-") as td:
        root = Path(td)
        bundle(root)
        command = subprocess.run(
            [
                str(ROOT / "scripts" / "okf-freshness"),
                "--root",
                str(root),
                "--as-of",
                "2026-08-16",
                "--check",
                "--format",
                "json",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        payload = json.loads(command.stdout)
        if command.returncode != 1 or payload["summary"]["stale"] != 1:
            raise AssertionError((command.returncode, payload, command.stderr))


def test_repository_indexes_have_no_drift() -> None:
    plan = plan_indexes(ROOT)
    if plan.errors or plan.changes:
        raise AssertionError(plan)


def main() -> int:
    tests = [
        test_indexes_are_idempotent_and_preserve_authored_content,
        test_malformed_marker_prevents_all_writes,
        test_case_variant_index_is_a_compatibility_landing_page,
        test_graph_and_freshness_are_deterministic,
        test_freshness_cli_check_exit_codes,
        test_repository_indexes_have_no_drift,
    ]
    for test in tests:
        test()
    print(f"OKF tooling tests passed ({len(tests)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
