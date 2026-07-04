#!/usr/bin/env bash
# Deterministic validation for a launched project.
# Validates schemas, queue invariants, scaffold completeness, and (optionally)
# emits a release-gate decision.

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BOOTSTRAP_LIB_DIR="${SCRIPT_DIR}/lib"

# shellcheck source=lib/log.sh
source "${BOOTSTRAP_LIB_DIR}/log.sh"
# shellcheck source=lib/error.sh
source "${BOOTSTRAP_LIB_DIR}/error.sh"

RELEASE_GATE=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --release-gate) RELEASE_GATE=1; shift;;
    *) bs_die "E0002" "$BS_EXIT_INPUT" "unknown flag: $1";;
  esac
done

PYTHONPATH= python3 - "${PROJECT_ROOT}" "${RELEASE_GATE}" <<'PY' || exit 9
import json, os, subprocess, sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

root = Path(sys.argv[1])
release_gate = sys.argv[2] == "1"

common_files = [
    "README.md", "Makefile", ".gitignore", "project.config.yaml",
    "AGENTS.md", "CLAUDE.md", ".cursor/rules/okf.mdc",
    "backlog/queue.yaml", "backlog/tasks/TASK-0001.md",
    "schemas/project.schema.json", "schemas/queue.schema.json",
    "schemas/task.schema.json", "schemas/error.schema.json",
    "schemas/okf-concept.schema.json",
    "profiles/default.yaml",
    "docs/agent-workflow.md", "docs/runbook.md", "docs/security.md",
    "docs/okf-integration.md",
    ".okf/index.md", ".okf/project.md", ".okf/log.md",
    ".okf/requirements/bootstrap-operational-readiness.md",
    ".okf/architecture/bootstrap-lifecycle-framework.md",
    ".okf/decisions/0001-okf-as-context-layer.md",
    ".okf/workflows/agent-okf-lifecycle.md",
    ".okf/risks/secret-storage-and-memory-drift.md",
    ".okf/tests/okf-validation-plan.md",
    ".okf/handoffs/initial-bootstrap.md",
    ".okf/improvements/continuous-improvement-repository.md",
    "scripts/okf-validate", "scripts/okf-context-pack", "scripts/okf-handoff",
    ".cursor/rules/okf-ecosystem-routing.mdc",
    ".cursor/rules/okf-forge-operator.mdc",
    ".cursor/rules/okf-dispatch.mdc",
    ".cursor/rules/okf-forge-promotion.mdc",
]

v2_files = [
    "docs/forge-lifecycle-integration.md",
    "docs/okf-dispatch-orchestration.md",
    "docs/okf-ways-of-working-brief.md",
    ".cursor/mcp-forge-lifecycle.json.example",
    "scripts/forgerelay-mcp.sh",
    "scripts/conceptforge-mcp.sh",
    "scripts/forge-clone-siblings.sh",
    "scripts/okf-dispatch",
    "scripts/okf_dispatch_schema.py",
    "scripts/okf-check-adapters",
    "scripts/okf-check-forge-receipts",
    "scripts/okf-sync-skills",
    ".okf/decisions/0002-okf-forge-integration.md",
    ".okf/workflows/okf-forge-lifecycle-bridge.md",
    ".okf/workflows/multi-agent-delivery-pipeline.md",
    ".okf/references/forge-sibling-layout.md",
    ".okf/references/forge-packet-type-registry.md",
    ".okf/improvements/forge-lifecycle-operator-notes.md",
    "docs/okf-service-operator-skills.md",
    "skills/okf-reader/SKILL.md",
    "skills/codex-okf-operator/SKILL.md",
    "skills/claude-okf-operator/SKILL.md",
    "skills/cursor-okf-operator/SKILL.md",
]

legacy_files = [
    "docs/mcp-integration.md",
    ".cursor/mcp.json.example",
    "scripts/mcp/register_project.sh",
    "scripts/mcp/health_check.sh",
    "scripts/workers/run_codex_task.sh",
    "scripts/workers/run_claude_task.sh",
    "scripts/workers/dispatch_task.sh",
    "scripts/lib/worker_runner.py",
    "schemas/worker-manifest.schema.json",
]

errors = []

class _NoTsLoader(yaml.SafeLoader):
    pass

for ch, resolvers in list(_NoTsLoader.yaml_implicit_resolvers.items()):
    _NoTsLoader.yaml_implicit_resolvers[ch] = [
        (tag, rx) for tag, rx in resolvers if tag != "tag:yaml.org,2002:timestamp"
    ]

def load_yaml(path: Path):
    return yaml.load(path.read_text(), Loader=_NoTsLoader)

proj = load_yaml(root / "project.config.yaml")
profile_name = (proj or {}).get("profile", "default")
if profile_name == "legacy-task":
    required_files = common_files + legacy_files
else:
    required_files = common_files + v2_files

for rel in required_files:
    if not (root / rel).is_file():
        errors.append(("missing-file", rel))

# Validate project.config.yaml against schema.
schema_dir = root / "schemas"
proj_schema = json.loads((schema_dir / "project.schema.json").read_text())
for err in Draft202012Validator(proj_schema).iter_errors(proj):
    errors.append(("project-schema", f"{list(err.path)} -> {err.message}"))

# Validate queue.yaml against schema and check invariants.
queue_schema = json.loads((schema_dir / "queue.schema.json").read_text())
queue_doc = load_yaml(root / "backlog/queue.yaml")
for err in Draft202012Validator(queue_schema).iter_errors(queue_doc):
    errors.append(("queue-schema", f"{list(err.path)} -> {err.message}"))

# Queue invariants: unique task_ids, no cycles in depends_on.
queue = (queue_doc or {}).get("queue", [])
ids = [t["task_id"] for t in queue]
if len(set(ids)) != len(ids):
    errors.append(("queue-invariant", "duplicate task_id in queue"))
adj = {t["task_id"]: list(t.get("depends_on") or []) for t in queue}
visited, stack = set(), set()

def dfs(node: str) -> bool:
    if node in stack:
        return True
    if node in visited:
        return False
    stack.add(node)
    for n in adj.get(node, []):
        if dfs(n):
            return True
    stack.discard(node)
    visited.add(node)
    return False

for tid in ids:
    if dfs(tid):
        errors.append(("queue-invariant", f"dependency cycle including {tid}"))
        break

# Validate every TASK-XXXX.md frontmatter against task schema.
task_schema = json.loads((schema_dir / "task.schema.json").read_text())
for path in sorted((root / "backlog/tasks").glob("TASK-*.md")):
    raw = path.read_text()
    if not raw.startswith("---\n"):
        errors.append(("task-frontmatter", f"{path.name}: missing frontmatter"))
        continue
    _, fm, _ = raw.split("---\n", 2)
    fm_doc = yaml.load(fm, Loader=_NoTsLoader) or {}
    for err in Draft202012Validator(task_schema).iter_errors(fm_doc):
        errors.append(("task-schema", f"{path.name}: {list(err.path)} -> {err.message}"))
    for okf_path in fm_doc.get("okf_concepts") or []:
        if not (root / okf_path).exists():
            errors.append(("task-okf-traceability", f"{path.name}: missing OKF concept {okf_path}"))

# Validate OKF bundle through the generated helper.
okf_validate = root / "scripts" / "okf-validate"
if okf_validate.exists():
    okf = subprocess.run(
        [str(okf_validate)],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if okf.returncode != 0:
        errors.append(("okf-validation", (okf.stderr + okf.stdout).strip()))

# Deterministic rerun check: launcher dry-run should converge without error.
project_id = (proj or {}).get("project_id")
profile = (proj or {}).get("profile", "default")
if project_id and not (root / ".launch.lock").exists():
    dry = subprocess.run(
        [
            str(root / "scripts/launch_project.sh"),
            "--name", str(project_id),
            "--profile", str(profile),
            "--target-dir", str(root),
            "--dry-run",
            "--non-interactive",
        ],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if dry.returncode != 0:
        errors.append(("determinism", f"dry-run relaunch failed: {dry.stderr.strip()}"))

if errors:
    for kind, msg in errors:
        print(f"[{kind}] {msg}", file=sys.stderr)
    if release_gate:
        print(json.dumps({
            "decision": "fail",
            "errors": [{"kind": k, "message": m} for k, m in errors],
        }))
    sys.exit(9)

if release_gate:
    print(json.dumps({"decision": "pass", "errors": []}))
print("validate_launch: OK")
PY
