---
type: Risk
title: Secret Storage and Project Memory Drift
description: OKF may become unsafe or unreliable if secrets are stored or adapters drift from the bundle.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/risks/secret-storage-and-memory-drift.md
tags: [okf, risk, security, agent-memory]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-24T15:54:09+01:00
---

# Risk

OKF can lose value if project facts diverge across tool adapters, chat history, generated context packs, and `.okf` concepts. It can become unsafe if secrets or credentials are committed.

# Impact

- Agents may implement stale requirements.
- Reviewers may miss durable decisions made only in chat.
- Credentials may be exposed through Git history.

# Likelihood

Medium for early projects unless adapter and validation habits are established.

# Mitigations

- Keep adapters thin and point back to `.okf`.
- Run `scripts/okf-validate` before commits.
- Mark unverified material clearly.
- Store secrets only in approved secret stores, never in OKF.

# Monitoring

- Review `.okf/log.md` for untracked material changes.
- Check generated context packs are not treated as source concepts.
- Review handoffs when tasks transfer between agents.
