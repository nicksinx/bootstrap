---
type: Release
title: Initial OKF Bootstrap Kit
description: Initial Project-1 release containing OKF bundle, adapters, scripts, templates, and skills.
status: active
lifecycle_stage: release
owner: project
source_of_truth: true
resource: .okf/releases/2026-06-24-initial-bootstrap.md
tags: [okf, release, bootstrap]
applies_to: [codex, claude, cursor, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# Summary

Initial reusable OKF bootstrap kit.

# Included

- Primary `.okf` bundle.
- Codex, Claude, and Cursor adapters.
- Local OKF scripts.
- Nine Codex-installable skills.
- Template OKF and adapter files.
- Continuous-improvement repository under `.okf/improvements/`.

# Known Issues

- Skills are provided for manual installation, not installed automatically.
- Scripts are intentionally lightweight and may need project-specific hardening later.

# Validation

Run `.okf/tests/okf-validation-plan.md`.
