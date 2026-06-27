---
type: Reference
title: Perplexity file upload limits and supported types
description: Perplexity supports code, PDFs, images, audio, and video uploads, with size and per-space limits that should shape OKF attachment strategy.
status: draft
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/perplexity-file-limits.md
tags: [okf, reference, perplexity, deep-research, shared-services]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: 2026-06-27T19:42:00+02:00
---

# Source

- **Title:** File Uploads
- **URL:** https://www.perplexity.ai/help-center/en/articles/10354807-file-upload
- **Retrieval date:** 2026-06-27
- **Source type:** primary product documentation

# Summary

Perplexity supports file uploads from the prompt bar including text, code, PDFs, images, audio, and video. Help pages report differing size limits across surfaces (general upload page vs Spaces). OKF should keep Perplexity attachment bundles small and curated rather than assuming one fixed cap.

# Relevant claims

- Perplexity supports file uploads from the prompt bar and drag-and-drop.
- Supported content includes text, code, PDFs, images, audio, and video.
- Documented size limits differ between help articles; verify in-product before hard-coding.

# Limitations and uncertainty

Do not hard-code a single byte limit in OKF validation until verified in-product. Practical policy: target ~8–14 curated Markdown files, avoid whole-repo dumps.

# Suggested OKF links

- `.okf/references/`
- `.okf/context-packs/`
- `PERPLEXITY.md`
- `docs/perplexity-project-files-and-skills.md`
