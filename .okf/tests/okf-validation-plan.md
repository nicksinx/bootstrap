---
type: Test Case
title: OKF Validation Plan
description: Validation checks for Project-1 OKF files, scripts, and skills.
status: active
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/tests/okf-validation-plan.md
tags: [okf, tests, validation]
applies_to: [codex, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# Test Objective

Confirm that Project-1 is operationally ready as an OKF bootstrap kit.

# Test Cases

1. Run `scripts/okf-validate`.
2. Run the Codex skill quick validator for each folder under `skills/`.
3. Confirm required adapters exist.
4. Confirm required scripts exist.
5. Confirm `.okf/improvements/` exists with at least one continuous-improvement concept.
6. Confirm the install instructions include copy and validation commands.

# Expected Result

Validation should pass with no failures. Warnings should be reviewed and either addressed or accepted.

# Evidence

Record command output summaries in `.okf/log.md` after validation.
