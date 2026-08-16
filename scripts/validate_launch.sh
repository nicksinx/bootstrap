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
import json, os, subprocess, sys, tempfile
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

root = Path(sys.argv[1])
release_gate = sys.argv[2] == "1"

common_files = [
    "README.md", "Makefile", ".gitignore", "project.config.yaml", "CODEX-SKILL-INSTALL.md",
    "AGENTS.md", "CLAUDE.md", "PERPLEXITY.md", ".cursor/rules/okf.mdc",
    "backlog/queue.yaml", "backlog/tasks/TASK-0001.md",
    "schemas/project.schema.json", "schemas/queue.schema.json",
    "schemas/task.schema.json", "schemas/error.schema.json",
    "schemas/okf-concept.schema.json",
    "profiles/default.yaml",
    "docs/agent-workflow.md", "docs/runbook.md", "docs/security.md",
    "docs/okf-integration.md",
    ".okf/index.md", ".okf/project.md", ".okf/log.md",
    ".okf/requirements/bootstrap-operational-readiness.md",
    ".okf/requirements/index.md",
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
    "docs/okf-v02-conformance.md",
    "docs/migrate-okf-v02.md",
    "docs/okf-index-graph-freshness.md",
    "docs/okf-readonly-mcp.md",
    "docs/openwiki-okf-sidecar.md",
    "docs/okf-attested-computation-experiment.md",
    "docs/perplexity-project-files-and-skills.md",
    "docs/skill-frontmatter-compatibility.md",
    ".cursor/mcp-forge-lifecycle.json.example",
    ".cursor/mcp-okf-readonly.json.example",
    "scripts/forgerelay-mcp.sh",
    "scripts/conceptforge-mcp.sh",
    "scripts/forge-clone-siblings.sh",
    "scripts/okf-dispatch",
    "scripts/okf_dispatch_schema.py",
    "scripts/okf-check-adapters",
    "scripts/okf-migrate",
    "scripts/okf-index",
    "scripts/okf-freshness",
    "scripts/okf-visualize",
    "scripts/okf-mcp-server",
    "scripts/openwiki-sidecar",
    "scripts/okf-attest-experiment",
    "scripts/attest/okf_bundle_digest.py",
    "scripts/attest/verify_okf_bundle_digest.py",
    "scripts/lib/okf_attestation.py",
    "scripts/okf-check-forge-receipts",
    "scripts/okf-sync-skills",
    "scripts/operator-ready-check.sh",
    ".okf/decisions/0002-okf-forge-integration.md",
    ".okf/decisions/0003-curated-okf-integration-boundary.md",
    ".okf/features/okf-integration-pilots.md",
    ".okf/agents/perplexity.md",
    ".okf/agents/perplexity-overflow.md",
    ".okf/agents/xcode-claude.md",
    ".okf/prompts/perplexity-custom-instructions.md",
    ".okf/prompts/perplexity-deep-research-setup.md",
    ".okf/prompts/perplexity-overflow-failover.md",
    ".okf/prompts/perplexity-post-curation-smoke-test.md",
    ".okf/prompts/xcode-step4-verification-checklist.md",
    ".okf/handoffs/README.md",
    ".okf/handoffs/TEMPLATE.md",
    ".okf/handoffs/TEMPLATE-tester.md",
    ".okf/handoffs/TEMPLATE-reviewer.md",
    ".okf/handoffs/TEMPLATE-xcode-step4.md",
    ".okf/context-packs/INDEX.md",
    ".okf/risks/xcode-live-verification-pending.md",
    ".okf/workflows/okf-forge-lifecycle-bridge.md",
    ".okf/workflows/multi-agent-delivery-pipeline.md",
    ".okf/workflows/optional-integration-review.md",
    ".okf/references/forge-sibling-layout.md",
    ".okf/references/forge-packet-type-registry.md",
    ".okf/references/integration-protocol-boundaries.md",
    ".okf/improvements/forge-lifecycle-operator-notes.md",
    "docs/okf-service-operator-skills.md",
    "skills/okf-reader/SKILL.md",
    "skills/codex-okf-operator/SKILL.md",
    "skills/claude-okf-operator/SKILL.md",
    "skills/cursor-okf-operator/SKILL.md",
    "mcp_server/okf_readonly_server.py",
    ".okf/computations/bootstrap-integrity.md",
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

integrations = (proj or {}).get("integrations") or {}
openwiki = integrations.get("openwiki") or {}
if openwiki.get("enabled") and not (root / "openwiki" / "INSTRUCTIONS.md").is_file():
    errors.append(("openwiki-sidecar", "enabled integration is missing openwiki/INSTRUCTIONS.md"))

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
        [str(okf_validate), "--strict"],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if okf.returncode != 0:
        errors.append(("okf-validation", (okf.stderr + okf.stdout).strip()))

okf_migrate = root / "scripts" / "okf-migrate"
if okf_migrate.exists():
    migrate = subprocess.run(
        [str(okf_migrate), "--check"],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if migrate.returncode != 0:
        errors.append(("okf-migration-drift", (migrate.stderr + migrate.stdout).strip()))

okf_index = root / "scripts" / "okf-index"
if okf_index.exists():
    index = subprocess.run(
        [str(okf_index), "--check"],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if index.returncode != 0:
        errors.append(("okf-index-drift", (index.stderr + index.stdout).strip()))

okf_freshness = root / "scripts" / "okf-freshness"
if okf_freshness.exists():
    freshness = subprocess.run(
        [str(okf_freshness), "--check"],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if freshness.returncode != 0:
        errors.append(("okf-freshness", (freshness.stderr + freshness.stdout).strip()))

adapter_check = root / "scripts" / "okf-check-adapters"
if adapter_check.exists():
    adapters = subprocess.run(
        [str(adapter_check)],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if adapters.returncode != 0:
        errors.append(("okf-adapter-drift", (adapters.stderr + adapters.stdout).strip()))

# Exercise the local read-only MCP protocol without enabling it in a host.
okf_mcp = root / "scripts" / "okf-mcp-server"
if okf_mcp.exists():
    probe = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "server/discover",
        "params": {
            "_meta": {
                "io.modelcontextprotocol/protocolVersion": "2026-07-28",
                "io.modelcontextprotocol/clientInfo": {"name": "validate-launch", "version": "1.0.0"},
                "io.modelcontextprotocol/clientCapabilities": {},
            }
        },
    }
    try:
        mcp = subprocess.run(
            [str(okf_mcp)],
            cwd=str(root),
            input=json.dumps(probe) + "\n",
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        errors.append(("okf-readonly-mcp", str(exc)))
    else:
        try:
            mcp_payload = json.loads(mcp.stdout)
            mcp_tools = mcp_payload["result"]["capabilities"]["tools"]
        except (json.JSONDecodeError, KeyError, TypeError):
            mcp_tools = None
        if mcp.returncode != 0 or mcp_tools is None:
            errors.append(("okf-readonly-mcp", (mcp.stderr + mcp.stdout).strip()))

# Generate and verify the experimental receipt outside the curated bundle.
okf_attest = root / "scripts" / "okf-attest-experiment"
if okf_attest.exists():
    with tempfile.TemporaryDirectory(prefix="okf-attest-launch-") as temporary:
        receipt = Path(temporary) / "receipt.json"
        try:
            attest = subprocess.run(
                [str(okf_attest), "run", "--root", str(root), "--receipt", str(receipt)],
                cwd=str(root),
                capture_output=True,
                text=True,
                timeout=30,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            errors.append(("okf-attestation", str(exc)))
        else:
            if attest.returncode != 0:
                errors.append(("okf-attestation", (attest.stderr + attest.stdout).strip()))

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
