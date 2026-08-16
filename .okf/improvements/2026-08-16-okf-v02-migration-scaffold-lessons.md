---
type: Improvement
title: OKF v0.2 Migration and Scaffold Lessons
description: Reusable lessons from consolidating two project generators while preserving a portable installed-skill fallback.
status: stable
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/improvements/2026-08-16-okf-v02-migration-scaffold-lessons.md
tags: [okf, v0.2, migration, scaffold, skills, continuous-improvement]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: reviewed
generated: { by: process:okf-v02-migration-scaffold, at: 2026-08-16T17:25:01+01:00 }
---

# Observation

The bootstrap launcher and installed project-creation skill had evolved into separate scaffold implementations. Fixes to one path could therefore leave the other path stale, while platform-specific skill metadata made a single universal frontmatter validator misleading.

# Impact

Multiple template authorities create silent parity drift. Migration that writes before validating every source file can also leave a repository partially converted.

# Recommendation

- Keep `templates/new-project/` and `scripts/launch_project.sh` as the canonical scaffold authority.
- Make the installed skill discover and delegate to that launcher when possible, while retaining a self-contained fallback for portability.
- Keep shared validator and migration runtimes byte-identical in the standalone skill bundle and test that invariant.
- Parse every migration candidate before the first write, write atomically, and test the second apply as a no-op.
- Validate Codex-compatible skills and Perplexity service adapters against their distinct documented contracts.
- Treat generated-adapter drift as a failing release gate by default.
