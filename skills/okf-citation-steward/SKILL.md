---
name: okf-citation-steward
description: Preserve, verify, and organize citations and external references in Open Knowledge Format bundles. Use when an agent needs to handle cited claims, vendor research, API references, market scans, legal or compliance notes, reference concepts, or external material that should not become accepted project knowledge without review.
---

# OKF Citation Steward

Use this skill when external claims influence project requirements, architecture, risks, decisions, or releases.

## Workflow

1. Identify claims that depend on external sources.
2. Prefer primary sources for technical, legal, security, financial, or policy claims.
3. Record provenance in `sources` frontmatter; each entry requires `resource` and should have a stable `id`.
4. Attribute individual claims with Markdown footnotes keyed to `sources[].id`.
5. Store durable source summaries as `Reference` concepts under `.okf/references/` when useful.
6. Omit `verified` for unreviewed research; only add actual verification events.
7. Preserve objective credibility signals such as author, usage count/window, and last modified date without inventing a score.

## Reference Concepts

Reference concepts should include:

- Source title.
- `sources` entries with URL or file path and stable ids.
- Retrieval or review date when known.
- Short summary.
- Relevant claims.
- Limitations or uncertainty.

## Guardrails

Do not invent citations. Do not treat search snippets as accepted source material.

Do not paste long copyrighted source text into OKF. Summarize and link instead.

Do not place confidential third-party material in OKF unless the project explicitly permits it.
