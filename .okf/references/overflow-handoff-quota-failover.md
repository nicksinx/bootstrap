---
type: Reference
title: Overflow handoff and quota failover
description: When a primary agent hits limits, the safest pattern is a role-preserving file handoff with explicit state, next action, and validation.
status: draft
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/overflow-handoff-quota-failover.md
tags: [okf, reference, perplexity, deep-research, shared-services]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-27T19:42:00+02:00
---

# Source

- **Title:** What are Spaces?
- **URL:** https://www.perplexity.ai/help-center/en/articles/10352961-what-are-spaces.html
- **Retrieval date:** 2026-06-27
- **Source type:** primary product documentation

# Summary

Perplexity Spaces keep threads, files, and instructions together in a portable workspace. That supports failover designs where current pipeline state is handed off as a compact file bundle when a runner hits quota or availability limits.

# Relevant claims

- Spaces keep threads, files, and instructions together.
- Files and threads can be pinned and searched inside a Space.
- Contributors and viewers can share access to Space contents.

# Limitations and uncertainty

Sources do not describe quota failover directly. Failover via compact handoff packets is an OKF inference, not a Perplexity-native feature.

# Suggested OKF links

- `.okf/handoffs/`
- `.okf/workflows/perplexity-overflow-failover.md`
- `scripts/okf-dispatch`
