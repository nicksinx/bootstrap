# Create New OKF Project in Perplexity

Use this document when configuring **Perplexity Desktop Pro** as the fifth service in the canonical OKF new-project setup sequence. Perplexity is the **project deep research layer**: it gathers cited external evidence and produces OKF `Reference` concepts for human or agent review before they influence requirements, architecture, or decisions.

For custom instructions, model routing, and overflow failover, see **`docs/configure-perplexity-okf.md`** first.

## Canonical service setup order

| Step | Service | Role |
|------|---------|------|
| 1 | Cursor | Scaffold OKF bundle and project identity |
| 2 | Codex | Wire Codex adapter, skills, and hooks |
| 3 | Claude Code | Wire Claude adapter and slash commands |
| 4 | Xcode | Wire Xcode-connected Claude Agent as dispatch consumer |
| **5** | **Perplexity** | **Deep research — populate `.okf/references/` with cited, unverified source material** |

Perplexity runs **after** steps 1–4 so research targets a stable project brief (`.okf/project.md`, requirements, and handoffs) rather than a blank scaffold.

---

## What Perplexity does in step 5

Perplexity must **not** invent project requirements or overwrite accepted OKF concepts. It:

1. Reads the project brief and open research questions from OKF context you provide.
2. Performs deep, citation-backed research on domain, technology, compliance, vendors, and risks.
3. Outputs OKF-compatible `Reference` concept drafts under `.okf/references/`.
4. Marks all outputs `verification_status: unverified` until reviewed by Cursor, Codex, or a human.
5. Produces a handoff summary listing research gaps and recommended follow-up searches.

Perplexity does not call other services directly. An agent in Cursor or Codex copies research outputs into the repository and runs `scripts/okf-validate`.

---

## Before you start: Perplexity custom instructions

1. Open **Perplexity Desktop → Settings → Custom instructions**.
2. Paste the block from `.okf/prompts/perplexity-custom-instructions.md` (or `docs/configure-perplexity-okf.md` Step 1).
3. This enables **MODE A — RESEARCH** (service 5) and **MODE B — OVERFLOW** (ad hoc failover) in the same Perplexity account.

---

## Copy-paste prompt for Perplexity

Replace every `{{PLACEHOLDER}}` before sending. Attach or paste `.okf/project.md` and the primary requirement concept if Perplexity supports file context.

```markdown
MODE A — RESEARCH

You are configuring **Perplexity as service 5 (deep research layer)** for a new OKF-enabled software project.
Model: Best (or Sonar 2 for citation-heavy sessions only).

## Setup context

- **Canonical service order:** (1) Cursor → (2) Codex → (3) Claude Code → (4) Xcode → (5) Perplexity
- **Your role:** Deep research only. Do not scaffold code, rewrite requirements, or claim findings are accepted project truth until reviewed.
- **OKF citation skill:** Follow the `okf-citation-steward` contract — prefer primary sources, include URLs and retrieval dates, summarize instead of copying long copyrighted text, and never invent citations.

## Project identity

- **Project name:** {{PROJECT_NAME}}
- **Project path:** {{PROJECT_PATH}}
- **Owner:** {{OWNER}}
- **Purpose (one paragraph):** {{PROJECT_PURPOSE}}
- **Primary requirement summary:** {{PRIMARY_REQUIREMENT_SUMMARY}}
- **In scope:** {{IN_SCOPE}}
- **Out of scope:** {{OUT_OF_SCOPE}}

## Research mandate

Perform deep research and produce **draft OKF Reference concepts** (Markdown with YAML frontmatter) for each topic below. Every concept must use `verification_status: unverified` and `status: draft` until a human or build agent reviews it.

### Required research topics

1. **Domain and problem landscape** — how similar products or workflows solve this problem today.
2. **Technology and architecture options** — viable stacks, integration patterns, and tradeoffs relevant to {{PRIMARY_TECH_DOMAIN}}.
3. **Standards, compliance, and policy** — regulations, security baselines, or industry standards that may constrain design (only where applicable to this project).
4. **Vendor and API landscape** — credible third-party services, APIs, or platforms worth evaluating, with licensing or lock-in notes where known.
5. **Risks and unknowns** — factual risks supported by sources; clearly separate evidence from inference.

### Optional research topics (if relevant)

- {{OPTIONAL_TOPIC_1}}
- {{OPTIONAL_TOPIC_2}}

## Output format (strict)

For **each** research topic, output one complete OKF Reference concept using this template:

---
type: Reference
title: {{Short descriptive title}}
description: One-sentence summary of what this reference covers.
status: draft
lifecycle_stage: planning
owner: project
source_of_truth: false
resource: .okf/references/{{slug-from-title}}.md
tags: [okf, reference, perplexity, deep-research]
applies_to: [cursor, claude, codex, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: {{ISO-8601 timestamp}}
---

# Source

- **Title:**
- **URL:**
- **Retrieval date:**
- **Source type:** (primary | secondary | vendor docs | academic | news | other)

# Summary

(Concise summary in your own words.)

# Relevant claims

(Bullet list of claims this project might rely on, each tied to the source above.)

# Limitations and uncertainty

(What the source does not cover, conflicts with other sources, or may have outdated.)

# Suggested OKF links

- Requirement(s):
- Architecture / decision concepts this may inform:
- Risks to open or update:

---

## Deliverables

1. **Reference concepts** — one Markdown file per topic listed above, ready to save under `.okf/references/`.
2. **Research index** — a short table listing each reference filename, topic, and top takeaway.
3. **Gap analysis** — what could not be verified, what needs primary-source follow-up, and suggested next Perplexity searches.
4. **Handoff block** for Cursor/Codex:

### Handoff: Perplexity step 5 complete

- References produced: (list filenames)
- Highest-confidence findings: (3–5 bullets)
- Findings that must not become requirements without review: (bullets)
- Recommended next actions for Cursor/Codex: copy references into repo, run `scripts/okf-validate`, link references from requirements/architecture, update `.okf/log.md`

## Rules

- Cite every factual claim with a reachable URL or named primary document.
- Do not store secrets, credentials, or confidential third-party material.
- Do not set `verification_status` to `reviewed`, `tested`, or `accepted`.
- Do not modify or contradict `.okf/project.md` scope without labeling disagreements as open questions.
- Prefer recent sources; note publication dates when material.

Begin with the domain and problem landscape, then proceed through the required topics in order.
Include a Routing note at the end (search-heavy vs reasoning-heavy subtasks).
```

---

## Overflow mode (ad hoc, not step 5)

Perplexity can also act as an **overflow substitute** when Codex, Claude, Cursor, or Xcode hit usage limits mid-delivery. This is not part of the new-project setup sequence.

- Workflow: `.okf/workflows/perplexity-overflow-failover.md`
- Prompt: `.okf/prompts/perplexity-overflow-failover.md`
- Agent rule: `.okf/agents/perplexity-overflow.md`

Use **MODE B — OVERFLOW** in the first message; Cursor or Codex applies deliverables and resumes the primary runner when available.

---

## After Perplexity responds

An agent in **Cursor** or **Codex** should:

1. Save each reference to `.okf/references/<slug>.md`.
2. Update `.okf/index.md` to link new references.
3. Link references from affected requirements, risks, or architecture drafts — without promoting unverified claims to accepted requirements.
4. Activate `.okf/agents/perplexity.md` (set `status: active` after first successful research cycle).
5. Append to `.okf/log.md` that Perplexity service 5 is configured.
6. Run `scripts/okf-validate`.
7. Write a handoff if further research rounds are needed.

---

## Perplexity step 5 completion checklist

- [ ] Steps 1–4 (Cursor, Codex, Claude, Xcode) completed and handoffs exist.
- [ ] Project brief and requirements pasted into the Perplexity prompt.
- [ ] At least one `Reference` concept per required research topic saved under `.okf/references/`.
- [ ] Every reference has `verification_status: unverified` and reachable citations.
- [ ] `.okf/agents/perplexity.md` exists and reflects the deep-research role.
- [ ] `.okf/log.md` records Perplexity as the configured fifth service.
- [ ] `scripts/okf-validate` passes after references are added.
- [ ] Gap analysis and open questions captured in a handoff or `.okf/references/` index note.

---

## Related material

- Configuration: `docs/configure-perplexity-okf.md`
- Cursor step 1 guide: `docs/create-new-okf-project-in-cursor.md`
- Perplexity step 5 guide: `docs/create-new-okf-project-in-perplexity.md`
- Citation skill: `skills/okf-citation-steward/SKILL.md`
- Custom instructions: `.okf/prompts/perplexity-custom-instructions.md`
- Reusable prompt in OKF: `.okf/prompts/perplexity-deep-research-setup.md`
- Perplexity agent rule: `.okf/agents/perplexity.md`
- Overflow agent rule: `.okf/agents/perplexity-overflow.md`
- Thin adapter: `PERPLEXITY.md`
