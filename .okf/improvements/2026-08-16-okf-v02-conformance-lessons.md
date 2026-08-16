---
type: Improvement
title: OKF v0.2 Conformance Lessons
description: Reusable lessons from replacing permissive v0.1 validation with strict, generated-project-aware v0.2 checks.
status: stable
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/improvements/2026-08-16-okf-v02-conformance-lessons.md
tags: [okf, v0.2, validation, yaml, continuous-improvement]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: reviewed
generated: { by: process:okf-v02-conformance, at: 2026-08-16T17:02:47+01:00 }
---

# Observation

The prior line parser treated nested YAML as strings and let malformed template placeholders pass until an independent validator inspected them.

# Impact

A repository-only validator can report success while emitted projects or full YAML consumers fail. Reserved files and generated templates need the same gate as live concepts.

# Recommendation

- Keep one validation engine and copy it into generated projects.
- Exercise malformed YAML, duplicate keys, reserved files, and machine-readable output directly.
- Run strict validation inside scaffold smoke tests, not only against the bootstrap repository.
- Isolate Python bytecode with `PYTHONPYCACHEPREFIX` on managed macOS environments.
- Treat local profile fields as extensions and preserve unknown keys/types during round trips.
