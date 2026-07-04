"""OKF dispatch packet and role-result validation (stdlib only)."""
import re
from pathlib import Path

SCHEMA_VERSION = 1
ROLES = ("builder", "tester", "reviewer", "integrator")
RUNNERS = ("codex", "claude", "cursor", "xcode-claude")
MAX_RETRY_ATTEMPTS = 3

PACKET_REQUIRED = (
    "schema_version",
    "packet_id",
    "pipeline_id",
    "role",
    "runner",
    "status",
    "source",
    "prompt",
    "context",
    "depends_on",
    "created_at",
    "updated_at",
)

TEST_VERDICTS = ("PASS", "PARTIAL", "FAIL")
REVIEW_VERDICTS = ("approved", "approved with notes", "blocked")
TEST_ROW_RESULTS = ("PASS", "FAIL", "SKIP")

PLACEHOLDER_PROMPT_PATTERNS = [
    re.compile(r"\{\{[^}]+\}\}"),
    re.compile(r"\bTBD\.?\b"),
    re.compile(r"Task summary:\s*\nTask summary\s*$", re.MULTILINE),
]

FORGE_LINEAGE_KEYS = (
    "forge_server",
    "forge_artifact_id",
    "forge_artifact_type",
    "forge_promoted_at",
    "forge_promoted_by",
)

FORGE_APPROVAL_KEYS = (
    "forge_approval_receipt_id",
    "forge_approver_identity",
    "forge_approval_scope",
)

FORGE_BLOCKED_DECISION_STATES = frozenset({"superseded", "rejected"})


def _require_dict(value, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _require_list(value, label):
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return value


def _require_non_empty_str(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    if value.strip().lower() in ("task summary", "tbd", "tbd."):
        raise ValueError(f"{label} contains placeholder text")
    return value.strip()


def _require_bool(value, label):
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be a boolean")
    return value


def prompt_has_placeholders(prompt):
    if not isinstance(prompt, str):
        return True
    for pattern in PLACEHOLDER_PROMPT_PATTERNS:
        if pattern.search(prompt):
            return True
    return False


def validate_packet_shape(packet, *, check_prompt_placeholders=True):
    errors = []
    if not isinstance(packet, dict):
        return ["packet must be a JSON object"]
    for key in PACKET_REQUIRED:
        if key not in packet:
            errors.append(f"missing required field: {key}")
    if packet.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    role = packet.get("role")
    if role not in ROLES:
        errors.append(f"invalid role: {role!r}")
    runner = packet.get("runner")
    if runner not in RUNNERS:
        errors.append(f"invalid runner: {runner!r}")
    if check_prompt_placeholders and prompt_has_placeholders(packet.get("prompt", "")):
        errors.append("prompt contains unfilled template placeholders")
    context = packet.get("context")
    if context is not None and not isinstance(context, dict):
        errors.append("context must be an object")
    depends_on = packet.get("depends_on")
    if depends_on is not None and not isinstance(depends_on, list):
        errors.append("depends_on must be an array")
    return errors


def validate_role_result(role, result):
    """Validate per-role result payload. Raises ValueError on failure."""
    validate_role(role)
    data = _require_dict(result, "result")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"result.schema_version must be {SCHEMA_VERSION}")
    _require_non_empty_str(data.get("completed_at", ""), "result.completed_at")
    _require_non_empty_str(data.get("completed_by", ""), "result.completed_by")

    if role == "builder":
        _require_non_empty_str(data.get("summary", ""), "result.summary")
        handoff = _require_non_empty_str(data.get("handoff_path", ""), "result.handoff_path")
        if not handoff.startswith(".okf/handoffs/"):
            raise ValueError("result.handoff_path must be under .okf/handoffs/")
        artifacts = _require_list(data.get("artifacts_changed"), "result.artifacts_changed")
        if not artifacts:
            raise ValueError("result.artifacts_changed must be a non-empty array")
        for item in artifacts:
            _require_non_empty_str(item, "result.artifacts_changed[]")
        concepts = _require_list(data.get("okf_concepts_updated"), "result.okf_concepts_updated")
        for item in concepts:
            _require_non_empty_str(item, "result.okf_concepts_updated[]")
        return data

    if role == "tester":
        verdict = _require_non_empty_str(data.get("verdict", ""), "result.verdict").upper()
        if verdict not in TEST_VERDICTS:
            raise ValueError(f"result.verdict must be one of {', '.join(TEST_VERDICTS)}")
        evidence = _require_non_empty_str(data.get("evidence_path", ""), "result.evidence_path")
        if not evidence.startswith(".okf/tests/"):
            raise ValueError("result.evidence_path must be under .okf/tests/")
        tests_run = _require_list(data.get("tests_run"), "result.tests_run")
        if not tests_run:
            raise ValueError("result.tests_run must be a non-empty array")
        for row in tests_run:
            row = _require_dict(row, "result.tests_run[]")
            _require_non_empty_str(row.get("command", ""), "result.tests_run[].command")
            outcome = _require_non_empty_str(row.get("result", ""), "result.tests_run[].result").upper()
            if outcome not in TEST_ROW_RESULTS:
                raise ValueError(
                    f"result.tests_run[].result must be one of {', '.join(TEST_ROW_RESULTS)}"
                )
        data["verdict"] = verdict
        data["evidence_path"] = evidence
        return data

    if role == "reviewer":
        handoff = _require_non_empty_str(data.get("handoff_path", ""), "result.handoff_path")
        if not handoff.startswith(".okf/handoffs/"):
            raise ValueError("result.handoff_path must be under .okf/handoffs/")
        verdict = _require_non_empty_str(data.get("verdict", ""), "result.verdict").lower()
        if verdict not in REVIEW_VERDICTS:
            raise ValueError(f"result.verdict must be one of {', '.join(REVIEW_VERDICTS)}")
        reqs = _require_list(data.get("requirements_checked"), "result.requirements_checked")
        if not reqs:
            raise ValueError("result.requirements_checked must be a non-empty array")
        for item in reqs:
            _require_non_empty_str(item, "result.requirements_checked[]")
        findings = _require_list(data.get("findings"), "result.findings")
        for item in findings:
            row = _require_dict(item, "result.findings[]")
            _require_non_empty_str(row.get("description", ""), "result.findings[].description")
            severity = _require_non_empty_str(row.get("severity", ""), "result.findings[].severity")
            if severity not in ("low", "medium", "high"):
                raise ValueError("result.findings[].severity must be low, medium, or high")
            disposition = _require_non_empty_str(row.get("disposition", ""), "result.findings[].disposition")
            if disposition not in ("accepted", "must-fix", "deferred"):
                raise ValueError("result.findings[].disposition must be accepted, must-fix, or deferred")
        data["verdict"] = verdict
        return data

    if role == "integrator":
        handoff = _require_non_empty_str(data.get("handoff_path", ""), "result.handoff_path")
        if not handoff.startswith(".okf/handoffs/"):
            raise ValueError("result.handoff_path must be under .okf/handoffs/")
        _require_non_empty_str(data.get("integration_summary", ""), "result.integration_summary")
        _require_bool(data.get("okf_log_updated"), "result.okf_log_updated")
        _require_bool(data.get("validation_passed"), "result.validation_passed")
        commands = _require_list(data.get("validation_commands"), "result.validation_commands")
        if not commands:
            raise ValueError("result.validation_commands must be a non-empty array")
        for item in commands:
            _require_non_empty_str(item, "result.validation_commands[]")
        return data

    raise ValueError(f"unsupported role for result validation: {role}")


def validate_role(role):
    if role not in ROLES:
        raise ValueError(f"invalid role {role!r}; expected one of {', '.join(ROLES)}")


def role_handoff_path(role, result):
    """Return required handoff/evidence path for role completion."""
    if role == "tester":
        return result.get("evidence_path")
    path = result.get("handoff_path")
    if path:
        return path
    return None


def role_requires_handoff_file(role):
    return role in ("builder", "reviewer", "integrator")


def verify_handoff_exists(root, role, result):
    """P0-2: verify role handoff/evidence file exists on disk."""
    path_str = role_handoff_path(role, result)
    if role == "tester":
        if not path_str:
            raise ValueError("tester result must include evidence_path")
        path = root / path_str
        if not path.is_file():
            raise ValueError(f"tester evidence file not found: {path_str}")
        return path_str

    if not role_requires_handoff_file(role):
        return path_str

    if not path_str:
        raise ValueError(f"{role} result must include handoff_path")
    path = root / path_str
    if not path.is_file():
        raise ValueError(f"{role} handoff file not found: {path_str}")
    text = path.read_text(encoding="utf-8")
    if "type: Handoff" not in text:
        raise ValueError(f"{role} handoff missing Handoff type in frontmatter: {path_str}")
    return path_str


def parse_forge_lineage(text, frontmatter_data):
    """Extract forge lineage keys from frontmatter and body."""
    lineage = {}
    for key in FORGE_LINEAGE_KEYS:
        if key in frontmatter_data:
            lineage[key] = frontmatter_data[key]
    body_match = re.search(
        r"# Forge lineage[^\n]*\n((?:forge_[a-z_]+:.*\n)+)",
        text,
        re.IGNORECASE,
    )
    if body_match:
        for line in body_match.group(1).splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key.startswith("forge_"):
                lineage[key] = value
    return lineage


def claims_forge_origin(text, frontmatter_data):
    lineage = parse_forge_lineage(text, frontmatter_data)
    if lineage.get("forge_server") and lineage.get("forge_artifact_id"):
        return True
    if frontmatter_data.get("forge_server") or frontmatter_data.get("forge_artifact_id"):
        return True
    patterns = [
        r"Promoted from Forge",
        r"Forge-derived",
        r"forge-promoted",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def claims_forge_approval(text, frontmatter_data):
    lineage = parse_forge_lineage(text, frontmatter_data)
    if any(key.startswith("forge_approval") for key in lineage):
        return True
    if frontmatter_data.get("forge_approval_receipt_id"):
        return True
    return False


def validate_forge_lineage_concept(rel_path, text, frontmatter_data, failures):
    if not claims_forge_origin(text, frontmatter_data):
        return
    lineage = parse_forge_lineage(text, frontmatter_data)
    missing = [key for key in FORGE_LINEAGE_KEYS if not lineage.get(key)]
    if missing:
        failures.append(
            f"{rel_path}: Forge-origin claim missing lineage fields: {', '.join(missing)}"
        )


def validate_forge_envelope_decision_state(rel_path, text, frontmatter_data, failures):
    lineage = parse_forge_lineage(text, frontmatter_data)
    state = (
        lineage.get("forge_envelope_decision_state")
        or frontmatter_data.get("forge_envelope_decision_state")
        or ""
    ).strip().lower()
    if state not in FORGE_BLOCKED_DECISION_STATES:
        return
    if frontmatter_data.get("superseded_by") or lineage.get("superseded_by"):
        return
    failures.append(
        f"{rel_path}: forge_envelope_decision_state {state!r} cannot promote as active OKF truth without superseded_by override"
    )


def validate_forge_approval_decision(rel_path, text, frontmatter_data, failures):
    if frontmatter_data.get("type") != "Decision":
        return
    if frontmatter_data.get("verification_status") != "accepted":
        return
    if not claims_forge_approval(text, frontmatter_data):
        return
    lineage = parse_forge_lineage(text, frontmatter_data)
    receipt = frontmatter_data.get("forge_approval_receipt_id") or lineage.get(
        "forge_approval_receipt_id"
    )
    if not receipt:
        failures.append(
            f"{rel_path}: accepted Decision claims Forge approval without forge_approval_receipt_id"
        )
    missing = [key for key in FORGE_APPROVAL_KEYS if not (
        frontmatter_data.get(key) or lineage.get(key)
    )]
    if receipt and missing:
        failures.append(
            f"{rel_path}: Forge approval receipt missing fields: {', '.join(missing)}"
        )
