---
type: Test Evidence
title: Shared OKF Skills Validation Evidence
description: Validation evidence for the shared OKF skills operating model added on 2026-06-27.
status: active
lifecycle_stage: test
owner: project
source_of_truth: true
resource: .okf/tests/2026-06-27-shared-skills-validation.md
tags: [okf, validation, evidence, shared-skills]
applies_to: [cursor, claude, codex, local-agent]
sensitivity: internal
verification_status: tested
timestamp: 2026-06-27T12:00:00+01:00
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

## Sync Script — List Skills

Command:

```bash
scripts/okf-sync-skills --list-skills
```

Result:

```text
create-new-okf-project    skills/create-new-okf-project/SKILL.md    Create or bootstrap...
okf-citation-steward      skills/okf-citation-steward/SKILL.md      Preserve, verify...
okf-concept-writer        skills/okf-concept-writer/SKILL.md        Create or update...
okf-conformance-validator skills/okf-conformance-validator/SKILL.md Validate an Open...
okf-context-pack-builder  skills/okf-context-pack-builder/SKILL.md  Build compact...
okf-handoff-writer        skills/okf-handoff-writer/SKILL.md        Write concise...
okf-reader                skills/okf-reader/SKILL.md                Load and triage...
okf-requirements-auditor  skills/okf-requirements-auditor/SKILL.md  Audit Open...
okf-risk-scanner          skills/okf-risk-scanner/SKILL.md          Scan software...
```

9 canonical skills detected.

## Sync Script — Dry Run (All Targets)

Command:

```bash
scripts/okf-sync-skills --dry-run
```

Result:

```text
DRY-RUN: would write AGENTS.md (5081 bytes)
DRY-RUN: would write CLAUDE.md (4486 bytes)
DRY-RUN: would write .cursor/rules/okf.mdc (2065 bytes)
DRY-RUN: would write .okf/agents/future-service.md (4271 bytes)
OKF adapter dry-run complete for /Users/dv/Projects/testrunner/Project-1 (9 skill(s), target=all)
```

All four adapter targets resolved without errors.

## Sync Script — Single Target

Command:

```bash
scripts/okf-sync-skills --target cursor --dry-run
```

Result:

```text
DRY-RUN: would write .cursor/rules/okf.mdc (2065 bytes)
OKF adapter dry-run complete for /Users/dv/Projects/testrunner/Project-1 (9 skill(s), target=cursor)
```

## Adapter Files Present

All four adapter files exist after sync:

- `AGENTS.md` — Codex adapter
- `CLAUDE.md` — Claude Code adapter
- `.cursor/rules/okf.mdc` — Cursor project rule overlay
- `.okf/agents/future-service.md` — future-service template

## Related Concepts

- `.okf/features/shared-okf-skills.md`
- `docs/shared-okf-skills.md`
- `.okf/tests/okf-validation-plan.md`
