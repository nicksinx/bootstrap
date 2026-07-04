---
type: Handoff
title: {{Task Title}} — Xcode Step 4
description: {{One-sentence summary for service 4 handoff to Perplexity step 5}}
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/handoffs/YYYY-MM-DD-xcode-step4-task-slug.md
tags: [okf, handoff, xcode, step-4]
applies_to: [xcode-claude, cursor, claude, codex, perplexity]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-28T12:00:00+00:00
---

Copy to `.okf/handoffs/YYYY-MM-DD-xcode-step4-<task-slug>.md`. Use after Xcode step 4 (dry or live verification).

# Current State

- Steps 1–3: {{complete / partial — cite handoffs}}
- Step 4 verification level: **dry** | **live** | **deferred**
- `.okf/agents/xcode-claude.md` status: {{draft / active}}

# Completed Work

- Dry verification: {{PASS / PARTIAL / not run}} — see `.okf/tests/…`
- Dispatch role map: {{e.g. builder:xcode-claude, …}}
- Agent rule updates: {{none / summary}}
- Live build/test: {{not applicable / summary with evidence path}}

# Decisions Made

- `xcode-claude` runner assigned to role(s): {{roles}}
- Live verification: {{deferred / complete}}

# Files Changed

# Known Issues

- {{e.g. live verification pending — `.okf/risks/xcode-live-verification-pending.md`}}
- {{signing / simulator / SPM constraints}}

# Next Recommended Actions (Perplexity step 5)

1. Read this handoff and `docs/create-new-okf-project-in-perplexity.md`
2. Configure Perplexity MODE A research only (unless overflow requested)
3. Attach curated Project Files per `docs/perplexity-project-files-and-skills.md`
4. Do not re-run bootstrap meta-research unless asked

# Validation Needed

```bash
scripts/okf-validate
scripts/okf-check-adapters
```

# Context Pack

- `.okf/project.md`
- Active requirement paths: {{paths}}
- Apple constraints for Perplexity research: {{list}}

## Verification level

| Level | Evidence |
|-------|----------|
| Dry | `.okf/prompts/xcode-step4-verification-checklist.md` + test doc |
| Live | `.okf/tests/` build/test output + promoted agent rule |
