"""Contract tests for schemas, profile, and error catalog.

Run via `make test-contracts` or `python3 tests/test_contracts.py`.
Exits non-zero on any contract failure.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"


def load_schema(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text())


def assert_valid(schema: dict, instance: dict, label: str) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    if errors:
        for err in errors:
            print(f"  FAIL [{label}]: {list(err.path)} -> {err.message}", file=sys.stderr)
        raise SystemExit(1)
    print(f"  OK   [{label}]")


def sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_profile_forge_lifecycle() -> None:
    schema = load_schema("profile.schema.json")
    profile = yaml.safe_load((ROOT / "profiles" / "forge-lifecycle.yaml").read_text())
    assert_valid(schema, profile, "profile/forge-lifecycle.yaml")


def test_profile_default() -> None:
    schema = load_schema("profile.schema.json")
    profile = yaml.safe_load((ROOT / "profiles" / "default.yaml").read_text())
    assert_valid(schema, profile, "profile/default.yaml")


def test_profile_legacy_task() -> None:
    schema = load_schema("profile.schema.json")
    profile = yaml.safe_load((ROOT / "profiles" / "legacy-task.yaml").read_text())
    assert_valid(schema, profile, "profile/legacy-task.yaml")


def test_project_example() -> None:
    schema = load_schema("project.schema.json")
    project = {
        "schema_version": 1,
        "project_id": "example-project",
        "name": "example-project",
        "template_version": "2.0.0",
        "profile": "default",
        "profile_version": "2.0.0",
        "default_branch": "main",
        "generated_by": "launch_project",
        "generated_at": "2026-04-28T22:00:00Z",
        "github": {
            "owner": "acme",
            "visibility": "private",
            "create_labels": True,
            "create_templates": True,
        },
        "mcp": {
            "enabled": True,
            "server_name": "forge-lifecycle",
            "transport": "stdio",
            "command": "bash",
            "data_dir": ".okf/forge",
            "auth_profile": "none",
            "token_source": "env",
        },
        "okf": {
            "enabled": True,
            "bundle_path": ".okf",
            "profile": "software-development",
            "continuous_improvement_path": ".okf/improvements",
        },
        "compat_mode": "strict",
    }
    assert_valid(schema, project, "project/example")


def test_task_example() -> None:
    schema = load_schema("task.schema.json")
    task = {
        "schema_version": 1,
        "task_id": "TASK-0001",
        "mcp_task_id": None,
        "title": "Validate launch scaffold idempotency",
        "status": "ready",
        "priority": "P0",
        "risk": "medium",
        "sdlc_stage": "verification",
        "agent_hint": "Verification & Security Agent",
        "required_skills": ["test-strategy-composer"],
        "depends_on": [],
        "context_paths": ["scripts/launch_project.sh"],
        "okf_concepts": [".okf/requirements/bootstrap-operational-readiness.md"],
        "expected_artifacts": ["test_plan", "validation_report"],
        "approval_required": False,
        "verification_type": "automated",
        "created_by": "launch_project",
        "created_at": None,
        "updated_at": None,
    }
    assert_valid(schema, task, "task/example")


def test_okf_concept_example() -> None:
    schema = load_schema("okf-concept.schema.json")
    concept = {
        "type": "Improvement",
        "title": "Continuous Improvement Repository",
        "description": "Captures lessons learned and reusable process improvements.",
        "status": "active",
        "lifecycle_stage": "operate",
        "owner": "project",
        "source_of_truth": True,
        "resource": ".okf/improvements/continuous-improvement-repository.md",
        "tags": ["okf", "continuous-improvement"],
        "applies_to": ["cursor", "claude", "codex", "mcp", "local-agent"],
        "sensitivity": "internal",
        "verification_status": "reviewed",
        "timestamp": "2026-04-28T22:00:00Z",
    }
    assert_valid(schema, concept, "okf-concept/example")


def test_queue_example() -> None:
    schema = load_schema("queue.schema.json")
    queue = {
        "schema_version": 1,
        "project_id": "example-project",
        "queue": [
            {
                "task_id": "TASK-0001",
                "status": "ready",
                "priority": "P0",
                "risk": "medium",
                "depends_on": [],
            },
            {
                "task_id": "TASK-0002",
                "status": "blocked",
                "priority": "P1",
                "risk": "low",
                "depends_on": ["TASK-0001"],
            },
        ],
    }
    assert_valid(schema, queue, "queue/example")


def test_handoff_example() -> None:
    schema = load_schema("handoff.schema.json")
    handoff = {
        "schema_version": 1,
        "input": {
            "task": {"task_id": "TASK-0001"},
            "context": ["scripts/launch_project.sh"],
        },
        "output": {
            "summary": "Validated launcher idempotency.",
            "proposed_changes": [
                {"path": "scripts/launch_project.sh", "kind": "update", "diff": ""},
            ],
            "verification": {
                "checklist": [
                    {"item": "rerun produces zero diff", "passed": True}
                ]
            },
            "blockers": [],
        },
    }
    assert_valid(schema, handoff, "handoff/example")


def test_evidence_example() -> None:
    schema = load_schema("evidence-pack.schema.json")
    evidence = {
        "schema_version": 1,
        "task_id": "TASK-0001",
        "project_id": "example-project",
        "inputs_hash": sha256("inputs"),
        "model_id": "claude-4.5-sonnet",
        "prompt_digest": sha256("prompt"),
        "tool_calls": [],
        "artifacts": [],
        "policy_decisions": [
            {"action": "task.approve", "decision": "allow", "reason_code": "OK"}
        ],
        "verifier_results": [
            {"name": "test_idempotency", "passed": True}
        ],
        "timestamps": {
            "created_at": "2026-04-28T22:00:00Z",
            "started_at": "2026-04-28T22:00:00Z",
            "ended_at": "2026-04-28T22:01:00Z"
        },
        "sealed": False,
    }
    assert_valid(schema, evidence, "evidence/example")


def test_audit_event_example() -> None:
    schema = load_schema("audit-event.schema.json")
    event = {
        "schema_version": 1,
        "event_id": "evt_000001",
        "project_id": "example-project",
        "actor": {"kind": "system", "id": "mcp-server"},
        "action": "task.approve",
        "decision": "allow",
        "reason_code": "OK",
        "before": None,
        "after": None,
        "timestamp": "2026-04-28T22:00:00Z",
    }
    assert_valid(schema, event, "audit-event/example")


def test_error_example() -> None:
    schema = load_schema("error.schema.json")
    error = {
        "code": "E0009",
        "exit_code": 9,
        "message": "Validation failure",
        "hint": "Run scripts/validate_launch.sh",
        "doc_url": "docs/errors.md",
        "correlation_id": "00000000-0000-0000-0000-000000000001",
        "context": {"step": "schema-validation"},
    }
    assert_valid(schema, error, "error/example")


def test_schedule_example() -> None:
    schema = load_schema("schedule.schema.json")
    schedule = {
        "schema_version": 1,
        "project_id": "example-project",
        "max_concurrent_runs": 1,
        "retry_budget": 3,
        "backoff_jitter_seconds": 30,
        "blackout_windows": [
            {"start": "22:00", "end": "06:00", "timezone": "Europe/London"}
        ],
        "kill_switch": False,
        "schedules": [
            {
                "id": "SCH-0001",
                "task_id": "TASK-0001",
                "cron": "0 9 * * *",
                "timezone": "Europe/London",
                "enabled": True,
                "allow_repo_mutation": False,
            }
        ],
    }
    assert_valid(schema, schedule, "schedule/example")


def test_worker_manifest_example() -> None:
    schema = load_schema("worker-manifest.schema.json")
    manifest = {
        "schema_version": 1,
        "run_id": "run_abcd1234",
        "task_id": "TASK-0001",
        "project_id": "example-project",
        "agent": "codex",
        "phase": "completed",
        "pid": None,
        "started_at": "2026-04-28T22:00:00Z",
        "ended_at": "2026-04-28T22:01:00Z",
        "task_file": "backlog/tasks/TASK-0001.md",
        "output_dir": "runs/codex/run_abcd1234",
        "command": ["/usr/local/bin/codex", "backlog/tasks/TASK-0001.md"],
        "exit_code": 0,
        "timeout_seconds": 3600,
        "allow_git_mutation": False,
        "retry_attempt": 0,
        "correlation_id": "00000000-0000-0000-0000-000000000001",
        "error_message": None,
        "manifest_path": "runs/codex/run_abcd1234/manifest.json",
        "stdout_log": "runs/codex/run_abcd1234/stdout.log",
        "stderr_log": "runs/codex/run_abcd1234/stderr.log",
    }
    assert_valid(schema, manifest, "worker-manifest/example")


def test_error_catalog_shape() -> None:
    catalog = json.loads((ROOT / "error_catalog.json").read_text())
    assert catalog["schema_version"] >= 1
    assert "E0009" in catalog["errors"]
    print("  OK   [error_catalog/shape]")


def main() -> int:
    print("Contract tests:")
    test_profile_default()
    test_profile_forge_lifecycle()
    test_profile_legacy_task()
    test_project_example()
    test_task_example()
    test_okf_concept_example()
    test_queue_example()
    test_handoff_example()
    test_evidence_example()
    test_audit_event_example()
    test_error_example()
    test_schedule_example()
    test_worker_manifest_example()
    test_error_catalog_shape()
    print("All contract tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
