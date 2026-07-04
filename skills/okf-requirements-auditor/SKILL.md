---
name: okf-requirements-auditor
description: Audit Open Knowledge Format requirements and feature concepts for implementation readiness. Use when an agent needs to review .okf/requirements or .okf/features for clarity, acceptance criteria, dependencies, risks, verification status, traceability, contradictions, or missing test expectations.
---

# OKF Requirements Auditor

Use this skill before implementation planning, release review, or requirements cleanup.

## Audit Checklist

For each relevant requirement or feature, check:

- Clear intent or user value.
- Specific requirement or behaviour.
- Testable acceptance criteria.
- Explicit dependencies.
- Known risks and mitigations.
- Verification plan or evidence.
- Citations for external claims.
- Links to related decisions, architecture, tests, and handoffs.
- Status, lifecycle stage, sensitivity, and verification status.

## Readiness Labels

Use these labels in the audit result:

- `Ready`: clear, traceable, and testable.
- `Needs clarification`: missing detail blocks implementation.
- `Needs verification`: plausible but unsupported by review, citation, or tests.
- `Conflicts`: contradicts another active concept.
- `Unsafe`: deprecated, superseded, archived, or sensitive in a way that blocks use.

## Output

Lead with blocking issues. Include file paths and the exact sections that need work.

When possible, propose a short OKF patch plan rather than rewriting requirements wholesale.

Do not silently promote draft or unverified requirements to accepted status.
