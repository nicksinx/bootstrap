# Configure Perplexity for OKF Projects

Use this guide to configure **Perplexity Desktop Pro** (not Perplexity Computer) for OKF-enabled projects. Perplexity participates in two modes:

| Mode | Service layer | Purpose |
|------|---------------|---------|
| **Research** | Service 5 (planned) | Deep cited research into `.okf/references/` |
| **Overflow** | Ad hoc sixth layer | Substitute for blocked primary runners when usage limits or outages stop delivery |

Perplexity does not replace Cursor, Codex, Claude Code, or Xcode in the canonical setup order. It does not execute repo hooks or advance dispatch queues directly.

---

## Prerequisites

- Steps 1–4 complete (Cursor, Codex, Claude Code, Xcode) for new projects, or an existing OKF bundle with `.okf/project.md`.
- Perplexity Desktop Pro installed on macOS.
- Project context ready: `.okf/project.md`, relevant requirements, and the latest handoff from `.okf/handoffs/`.

---

## Step 1: Set Perplexity custom instructions

Open **Perplexity Desktop → Settings → Custom instructions** and paste the block from `.okf/prompts/perplexity-custom-instructions.md` (or below).

These instructions apply to every thread unless you override mode in the first message.

```text
OKF project assistant (Perplexity Desktop Pro)

When the user provides OKF project context (.okf/project.md, requirements, handoffs, context packs, or dispatch packet summaries):

You support TWO modes. The user will say which mode applies:

MODE A — RESEARCH (service 5, default for setup)
- Deep cited research only. Do not scaffold code or accept findings as project truth.
- Output draft OKF Reference concepts for .okf/references/ with verification_status: unverified and source_of_truth: false.
- Follow okf-citation-steward: reachable URLs, retrieval dates, limitations, no invented citations.
- End with: Research index, Gap analysis, Handoff block for Cursor/Codex ingest.

MODE B — OVERFLOW (ad hoc substitute runner)
- Continue the SAME OKF role contract when a primary runner (Codex, Claude, Cursor, Xcode) is blocked by usage limits, outage, or policy.
- Read the overflow handoff or packet summary: role (builder|tester|reviewer|integrator), acceptance criteria, context paths.
- Produce the role deliverable (draft code, review notes, test plan, OKF update drafts, handoff) for a human or Cursor/Codex to apply.
- Do NOT claim work was applied to the repo. Do NOT advance dispatch state.
- End with: Overflow completion block (role, primary_runner blocked, overflow_model used, files to apply, validation needed).

Model routing:
- Use Best when the user does not specify a model.
- Research: Sonar 2 for fast cited landscape; Gemini 3.1 Pro for deep analysis; Best for mixed packs.
- Overflow reviewer: Claude Sonnet 4.6 or Best; overflow builder drafts: GPT-5.4 or Best; evidence checks: Sonar 2.
- Include a short Routing note (search-heavy vs reasoning-heavy subtasks).

Never store secrets. Never set verification_status to reviewed, tested, or accepted without human or build-agent review.
Durable project state belongs in .okf, not only in this chat.
```

---

## Step 2: Configure service 5 (deep research)

1. Build a context pack or paste:
   - `.okf/project.md`
   - Primary requirement concept
   - Latest handoff from step 4 (Xcode)
2. Open a new Perplexity thread. Select **Best** or **Sonar 2** for citation-heavy work.
3. Paste the research prompt from `docs/create-new-okf-project-in-perplexity.md` or `.okf/prompts/perplexity-deep-research-setup.md`.
4. Save outputs via **Cursor or Codex** into `.okf/references/`.
5. Update `.okf/index.md`, append `.okf/log.md`, run `scripts/okf-validate`.

Workflow detail: `.okf/workflows/perplexity-research-cycle.md`

Project Files and Skills: `docs/perplexity-project-files-and-skills.md`

---

## Step 3: Configure overflow (ad hoc substitute)

Use overflow only when a primary runner cannot continue and the pipeline must not stall.

**Trigger conditions**

- Usage limit or quota exhausted on Codex, Claude, or another primary runner
- Service outage or policy block
- User explicitly requests failover to Perplexity

**Procedure**

1. Pause the active dispatch packet (or note the stalled role in a handoff).
2. Run `scripts/okf-handoff perplexity-overflow --summary "Failover from <runner> for <role>."` or use `.okf/prompts/perplexity-overflow-failover.md`.
3. Build an overflow context pack: packet summary, acceptance criteria, relevant OKF paths, changed files summary.
4. Start a Perplexity thread with **MODE B — OVERFLOW** in the first message. Paste the overflow prompt.
5. **Cursor or Codex** applies deliverables, runs tests/validation, updates OKF, resumes primary runner when available.

Workflow detail: `.okf/workflows/perplexity-overflow-failover.md`

**Roles Perplexity overflow handles well**

| Role | Fit | Notes |
|------|-----|-------|
| Reviewer | Strong | Compare work vs OKF requirements and risks |
| Integrator | Good | Draft OKF updates, log entries, handoffs |
| Builder | Partial | Draft code/specs; human applies patches |
| Tester | Low | Propose tests; paste results for interpretation |

---

## Step 4: Model selection cheat sheet

| Task | Suggested model |
|------|-----------------|
| Fast cited web research | Sonar 2 or Best |
| General drafting / overflow builder | GPT-5.4 or Best |
| Deep analysis / long context | Gemini 3.1 Pro or Best |
| Agentic-style overflow review | Claude Sonnet 4.6 or Best |
| Alternative phrasing / comparison | Kimi K2.6 |
| Technical reasoning comparison | Nemotron 3 Super |

Record `overflow_model_used` and Perplexity's Routing note in the handoff when using overflow.

---

## Step 5: Activate OKF agent concepts

After the first successful research cycle:

1. Set `.okf/agents/perplexity.md` to `status: active`.
2. Keep `.okf/agents/perplexity-overflow.md` as reference for overflow (no Perplexity app install step).
3. Append to `.okf/log.md` that Perplexity service 5 is configured.

After the first overflow event:

1. Append failover details to `.okf/log.md`.
2. Link the overflow handoff from the stalled pipeline or packet notes.

---

## Completion checklist

- [ ] Perplexity custom instructions pasted (Step 1)
- [ ] Service 5 research prompt tested; references saved under `.okf/references/`
- [ ] `.okf/agents/perplexity.md` active after first research cycle
- [ ] Overflow prompt and workflow reviewed by integrator (Cursor/Codex)
- [ ] `scripts/okf-validate` passes

---

## Related material

- Step 5 setup: `docs/create-new-okf-project-in-perplexity.md`
- Thin adapter: `PERPLEXITY.md`
- Agent rules: `.okf/agents/perplexity.md`, `.okf/agents/perplexity-overflow.md`
- Prompts: `.okf/prompts/perplexity-custom-instructions.md`, `.okf/prompts/perplexity-deep-research-setup.md`, `.okf/prompts/perplexity-overflow-failover.md`
- Workflows: `.okf/workflows/perplexity-research-cycle.md`, `.okf/workflows/perplexity-overflow-failover.md`
- Citation skill: `skills/okf-citation-steward/SKILL.md`
