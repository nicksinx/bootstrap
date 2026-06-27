---
type: Reference
title: Multi-agent configuration risks
description: The main risks are context drift, duplicated instructions, stale adapters, and oversized attachments.
status: draft
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/multi-agent-risks.md
tags: [okf, reference, perplexity, deep-research, shared-services]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-27T19:42:00+02:00
---

# Source

- **Title:** Perplexity Spaces; Agent Skills – Codex; AGENTS.md
- **URL:** https://www.perplexity.ai/help-center/en/articles/10352961-what-are-spaces.html ; https://developers.openai.com/codex/skills ; https://agents.md
- **Retrieval date:** 2026-06-27
- **Source type:** primary documentation synthesis

# Summary

Perplexity Spaces encourage file-backed context that can become over-attachment without curation. Codex and AGENTS.md favor compact local instructions. Primary risk: research drafts promoted to requirements without validation, plus adapter drift and secret leakage into shared files.

# Relevant claims

- Spaces keep files and threads together, which can encourage over-attachment if bundles are not curated.
- Codex skill selection relies on concise descriptions before loading full instructions.
- AGENTS.md encourages focused agent instructions rather than bloated README content.

# Limitations and uncertainty

Security cautions about secrets are project policy, not vendor claims from these sources.

# Suggested OKF links

- `.okf/references/`
- `scripts/okf-validate`
- `.okf/improvements/`
- `.okf/risks/secret-storage-and-memory-drift.md`
