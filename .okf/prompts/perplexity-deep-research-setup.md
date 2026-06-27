---
type: Reference
title: Perplexity Deep Research Setup Prompt
description: Reusable Perplexity prompt for configuring service 5 deep research on new OKF projects.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/prompts/perplexity-deep-research-setup.md
tags: [okf, prompt, perplexity, deep-research, setup]
applies_to: [perplexity, cursor, codex, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-27T21:00:00+01:00
---

# Purpose

Copy-paste prompt for Perplexity when configuring the fifth service (deep research layer) in the canonical OKF new-project setup order.

Configuration guide: `docs/configure-perplexity-okf.md`

# Canonical service order

1. Cursor — scaffold
2. Codex — adapter and hooks
3. Claude Code — adapter and commands
4. Xcode — dispatch consumer
5. Perplexity — deep research into `.okf/references/`

Overflow (ad hoc): Perplexity may substitute for blocked primary runners — see `.okf/prompts/perplexity-overflow-failover.md`.

# First message (recommended)

```text
MODE A — RESEARCH

Configure Perplexity as OKF service 5 (deep research layer) for project "{{PROJECT_NAME}}".
Model: Best (or Sonar 2 if this session is citation-heavy only).

Read the project brief below. Research domain, technology, compliance, vendor, and risk topics with citations.
Output draft OKF Reference concepts (verification_status: unverified, source_of_truth: false) ready for .okf/references/.
Follow okf-citation-steward: cite sources, no invented claims, no secrets.

End with: Research index, Gap analysis, Handoff block for Cursor/Codex ingest.
Include a Routing note (search-heavy vs reasoning-heavy subtasks).
```

Attach or paste `.okf/project.md` and the primary requirement before sending.

# Full prompt

See the complete template with placeholders in `docs/create-new-okf-project-in-perplexity.md`.

# Post-research

Cursor or Codex copies outputs into `.okf/references/`, updates index and log, runs `scripts/okf-validate`, and activates `.okf/agents/perplexity.md` after the first successful cycle.

Workflow: `.okf/workflows/perplexity-research-cycle.md`
