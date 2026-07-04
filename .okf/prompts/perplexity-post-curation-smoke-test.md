---
type: Reference
title: Perplexity Post-Curation Smoke Test Prompt
description: Copy-paste prompt to verify Perplexity Space Files, Skills, and custom instructions after Batch 2 curation.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/prompts/perplexity-post-curation-smoke-test.md
tags: [okf, prompt, perplexity, smoke-test, validation]
applies_to: [perplexity, cursor, codex, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-28T14:00:00+02:00
---

# Purpose

Run once after curating **Project Files**, **Project Skills**, and **Custom instructions** in a Perplexity Space for an OKF bootstrap kit project (Project-1).

This is a **configuration verification** — no deep research, no six-topic shared-services pack, no repo changes.

Guide: `docs/perplexity-project-files-and-skills.md`

# When to run

- After first Space setup
- After re-uploading `docs/okf-ways-of-working-brief.md`
- After adding or removing Tier 2–4 files or the four `perplexity-okf-*` skills

# Prompt (copy below)

```markdown
OKF POST-CURATION SMOKE TEST — configuration check only

Do NOT run deep research. Do NOT re-run the six-topic shared-services research pack. Do NOT scaffold code or claim you wrote to the repo.

Read the attached Project Files (especially docs/okf-ways-of-working-brief.md, PERPLEXITY.md, and .okf/index.md) and answer every section below. If a file is missing from context, say so explicitly — do not guess.

---

## 1. Project identity (from attached files)

- Project name and purpose (one sentence each)
- Canonical five-service order (list all five)
- What overflow is (one sentence) and whether it replaces service 5

## 2. References vs operator docs

- What role does docs/okf-ways-of-working-brief.md play?
- What role do .okf/references/*.md files play?
- Are references obsolete when the brief exists? (yes/no + one sentence why)

## 3. Policy source of truth

- Before researching OKF operating policy, what should you read first?
- Will you re-derive implemented rules from chat memory if they are already in the brief? (yes/no)
- Name one rule from the brief you can cite without opening external sources

## 4. MODE A vs MODE B

| Question | MODE A — Research | MODE B — Overflow |
|----------|-------------------|-------------------|
| Default for setup? | | |
| Primary output | | |
| May advance dispatch / claim repo applied? | | |
| Required closing sections | | |

## 5. Project Files curation

- Is docs/okf-ways-of-working-brief.md attached in this Space? (yes/no)
- How many times should the brief appear in Project Files? (number)
- Name two Tier 2 files you can see (or state "not in context")
- Name the latest handoff file if present (or state "none attached")

## 6. Project Skills

List the four perplexity-okf-* skills you have access to (or state which are missing):
- perplexity-okf-reader
- perplexity-okf-citation-steward
- perplexity-okf-handoff-writer
- perplexity-okf-concept-writer

## 7. Citation and Reference output rules

- Required frontmatter fields for draft Reference concepts
- verification_status for new research output
- source_of_truth for new research output
- One thing okf-citation-steward forbids

## 8. Explicit negatives (confirm each with one line)

- [ ] I will not treat Space chat as durable OKF state
- [ ] I will not set verification_status to reviewed/accepted without human review
- [ ] I will not re-run the Project-1 six-topic shared-services pack unless explicitly asked
- [ ] I will not attach or duplicate the operator brief twice in file recommendations

## 9. Mini handoff block (format check only)

Produce a **sample** Handoff block for Cursor ingest (no real research). Include:
- Mode: MODE A smoke test
- Files to apply: none (config check only)
- Validation needed: operator confirms Sections 1–8 pass
- Routing note: one line

---

End with:

**SMOKE TEST VERDICT:** PASS | PARTIAL | FAIL

**If PARTIAL or FAIL:** list missing files, skills, or instruction gaps and what the operator should attach or paste.
```

# Pass criteria (operator)

| Verdict | Meaning |
|---------|---------|
| **PASS** | Sections 1–8 accurate; brief attached once; four skills listed; negatives all confirmed |
| **PARTIAL** | Core policy correct but missing handoff, skill, or brief not in context |
| **FAIL** | Wrong service order, conflates references with brief, offers to re-run six-topic pack, or claims repo/dispatch actions |

After PASS: append one line to `.okf/log.md` noting smoke test date and verdict. No reference files to ingest.

# Fail remediation

| Gap | Fix |
|-----|-----|
| Brief not in context | Re-upload `docs/okf-ways-of-working-brief.md` (Tier 1 only) |
| Wrong service order | Re-read brief + `.okf/index.md`; refresh custom instructions |
| Skills missing | Attach four `skills/perplexity-okf-*/SKILL.md` in Project Skills |
| Re-runs six-topic pack | Add "read brief first" line from `.okf/prompts/perplexity-custom-instructions.md` to Settings |
