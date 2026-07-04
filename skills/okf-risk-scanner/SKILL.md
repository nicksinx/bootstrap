---
name: okf-risk-scanner
description: Scan software, architecture, agent workflows, OKF concepts, and handoffs for project risks. Use when an agent needs to identify security, privacy, reliability, delivery, context drift, tool-adapter drift, unverified-claim, secret-storage, compliance, release, or cross-agent handoff risks and record them in .okf/risks.
---

# OKF Risk Scanner

Use this skill during planning, implementation review, handoff, and release preparation.

## Risk Categories

Check for:

- Security and secret storage risks.
- Privacy and sensitive data risks.
- Reliability and failure mode risks.
- Requirements ambiguity.
- Missing tests or weak acceptance criteria.
- Unverified external claims.
- Deprecated or superseded concepts still being used.
- Tool adapter drift from `.okf`.
- Context loss during agent handoff.
- Release, deployment, signing, or operational risks.

## Output

For each material risk, include:

- Risk title.
- Impact.
- Likelihood.
- Mitigation.
- Monitoring signal.
- Related OKF concepts and source files.

## OKF Updates

Create or update `Risk` concepts under `.okf/risks/` for durable risks.

If a risk blocks implementation, say so clearly and link the blocking concept.

Do not bury severe risks inside a general summary.
