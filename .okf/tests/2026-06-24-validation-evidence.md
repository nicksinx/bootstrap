---
type: Test Evidence
title: Initial Validation Evidence
description: Validation evidence for the initial Project-1 OKF bootstrap kit.
status: active
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/tests/2026-06-24-validation-evidence.md
tags: [okf, validation, evidence]
applies_to: [codex, local-agent]
sensitivity: internal
verification_status: tested
timestamp: 2026-06-24T15:54:09+01:00
---

# Validation Performed

## OKF Bundle

Command:

```bash
scripts/okf-validate
```

Result:

```text
OKF validation passed: 0 warning(s)
```

## Codex Skills

Command:

```bash
for skill in Project-1/skills/create-new-okf-project Project-1/skills/okf-*; do
  PYTHONPATH=/Users/dv/.cache/uv/archive-v0/Vq3DxWaKCfNRUmWt python3 /Users/dv/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill"
done
```

Result:

```text
Skill is valid!
Skill is valid!
Skill is valid!
Skill is valid!
Skill is valid!
Skill is valid!
Skill is valid!
Skill is valid!
Skill is valid!
```

## Script Smoke Tests

Commands:

```bash
scripts/okf-context-pack -o tmp/smoke-context-pack.md .okf/index.md .okf/project.md
scripts/okf-handoff smoke-test --summary "Smoke test generated handoff."
```

Result:

Both commands created expected output files. Generated smoke artifacts were removed after validation.

## Create New OKF Project Skill

Commands:

```bash
Project-1/skills/create-new-okf-project/scripts/create_okf_project.py /private/tmp/okf-skill-smoke --name "OKF Skill Smoke" --owner codex
scripts/okf-validate
scripts/okf-context-pack -o tmp/smoke-pack.md .okf/index.md .okf/improvements/continuous-improvement-repository.md
scripts/okf-handoff smoke-transfer
```

Result:

```text
OKF project scaffold ready: /private/tmp/okf-skill-smoke
OKF validation passed: 0 warning(s)
Skill is valid!
```

The generated temporary project included `.okf/improvements/continuous-improvement-repository.md`. Generated smoke artifacts were removed after validation.

## Scaffold Script Syntax

Command:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/okf-pycache python3 -m py_compile Project-1/skills/create-new-okf-project/scripts/create_okf_project.py
```

Result:

```text
Passed with no syntax errors.
```
