# Create New OKF Project in Xcode

Use this document when configuring **Xcode-connected Claude Agent as the fourth service** in a new OKF-enabled project. Cursor must complete step 1, Codex step 2, and Claude Code step 3 first, including scaffold, adapters, validation, and the Claude Code to Xcode handoff.

This document is intended to be passed as context to Xcode-connected Claude Agent, Cursor, Codex, Claude Code, or Perplexity so every new project follows the same service setup order.

## Canonical service setup order

Configure services in this order for every new OKF project:

| Step | Service | Primary adapter / entry point | When it runs |
|------|---------|------------------------------|--------------|
| **1** | Cursor | `.cursor/rules/okf.mdc` | First — scaffold the project and OKF bundle |
| **2** | Codex | `AGENTS.md`, `.codex/hooks.json` | After Cursor handoff — install skills and Codex hooks |
| **3** | Claude Code | `CLAUDE.md`, `.claude/commands/` | After Codex handoff — wire Claude adapter and slash commands |
| **4** | **Xcode-connected Claude Agent** | `.okf/agents/xcode-claude.md` | After Claude Code handoff — Apple-platform build/test/dispatch consumer |
| **5** | Perplexity Desktop Pro | `PERPLEXITY.md`, `.okf/agents/perplexity.md` | Last — cited deep research into `.okf/references/`; overflow failover |

Each step produces a handoff under `.okf/handoffs/` before the next service is configured. Do not skip ahead; later services assume earlier steps completed and validated.

Companion documents:

- Step 1: `docs/create-new-okf-project-in-cursor.md`
- Step 2: `docs/create-new-okf-project-in-codex.md`
- Step 3: `docs/create-new-okf-project-in-claude.md`
- Step 4: `docs/create-new-okf-project-in-xcode.md` ← this document
- Step 5: `docs/create-new-okf-project-in-perplexity.md`, `docs/configure-perplexity-okf.md`

---

## What Xcode does in step 4

Xcode-connected Claude Agent confirms that Apple-platform build and test work can participate in the OKF dispatch model without storing local secrets in `.okf`.

Xcode must:

1. Read the Claude Code handoff and confirm steps 1–3 are complete enough to continue.
2. Verify or update `.okf/agents/xcode-claude.md` when project-specific Apple constraints are known.
3. Confirm whether dispatch is enabled and which role(s) use the `xcode-claude` runner.
4. Record build, simulator, package, signing, or platform limitations as OKF risks, tests, or handoffs.
5. Run dry verification (see `.okf/prompts/xcode-step4-verification-checklist.md`) before claiming live setup complete.
6. Run `scripts/okf-validate` and `scripts/okf-check-adapters`.
7. Write a handoff for Perplexity service 5.

Xcode does **not** configure Cursor global skills, Codex hooks, Claude Code slash commands, or Perplexity Spaces in step 4. It must not modify `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/okf.mdc`, or `.codex/hooks.json` except via documented sync scripts when repairing broken adapters.

Xcode-connected Claude Agent has **no automatic hook** equivalent to Codex's Stop hook. Dispatch packet consumption is **manual** — read packets from `.okf/dispatch/ready/` when invoked for the assigned runner.

---

## Prerequisites

Before Xcode step 4 starts, the project should already contain:

```text
.okf/
.cursor/rules/okf.mdc
AGENTS.md
CLAUDE.md
PERPLEXITY.md
.okf/agents/xcode-claude.md          ← draft until live Xcode verification
scripts/okf-validate
scripts/okf-sync-skills
scripts/okf-check-adapters
scripts/okf-context-pack
scripts/okf-handoff
docs/okf-ways-of-working-brief.md
docs/create-new-okf-project-in-claude.md
```

If multi-agent delivery is planned, the project should also contain:

```text
scripts/okf-dispatch
.okf/dispatch/
  ready/
  running/
  done/
  failed/
  pipelines/
docs/okf-dispatch-orchestration.md
.okf/workflows/multi-agent-delivery-pipeline.md
```

If these files are missing, record the gap in `.okf/log.md` and either repair the scaffold from the OKF bootstrap kit or stop with a handoff explaining what Claude Code needs to complete first.

---

## Step-by-step: configure Xcode (service 4)

### 1. Open the project in Xcode-connected Claude Agent

Open the Apple-platform project in Xcode with Claude Agent enabled, or open the repo root if the agent can read OKF context from the workspace.

For a quick initial read before any edits:

```bash
cat .okf/index.md
cat .okf/project.md
cat .okf/agents/xcode-claude.md
```

### 2. Read required context

Read these files before editing:

1. `docs/okf-ways-of-working-brief.md`
2. `.okf/index.md`
3. `.okf/project.md`
4. Latest Claude Code to Xcode handoff under `.okf/handoffs/`
5. Prior handoffs from Cursor and Codex when still relevant
6. `docs/create-new-okf-project-in-claude.md`
7. `docs/okf-dispatch-orchestration.md` when dispatch is enabled
8. `.okf/workflows/multi-agent-delivery-pipeline.md`
9. `.okf/prompts/xcode-step4-verification-checklist.md` (dry verification)
10. Relevant `skills/okf-*/SKILL.md` files for active tasks

Confirm the canonical service order:

```text
Cursor first, Codex second, Claude Code third, Xcode fourth, Perplexity fifth.
```

### 3. Confirm steps 1–3 complete

Before configuring Xcode, verify:

- `.cursor/rules/okf.mdc`, `AGENTS.md`, and `CLAUDE.md` exist and were configured in order.
- A Claude Code to Xcode handoff exists under `.okf/handoffs/`.
- `PERPLEXITY.md` exists (step 5 stub; do not fully configure Perplexity in step 4).
- `.okf/agents/xcode-claude.md` exists (typically `status: draft` until live verification).
- Claude Code dispatch manual-advance constraint is documented in the step 3 handoff when dispatch is enabled.

Do not modify step 1–3 adapters unless sync scripts must repair broken generated files.

### 4. Verify or update the Xcode agent rule

Review `.okf/agents/xcode-claude.md`. Update project-specific sections when Apple constraints are known:

- Target platform (macOS, iOS, etc.)
- Build system (Xcode project, Swift Package, etc.)
- Test strategy (unit, UI, simulator)
- Signing approach (without storing secrets in OKF)

**Keep `status: draft` and `verification_status: unverified` until live build/test evidence exists.** See `.okf/risks/xcode-live-verification-pending.md`.

Do not promote to `active` / `reviewed` based on dry verification alone.

### 5. Configure Xcode for dispatch

If the project uses the OKF dispatch queue, assign `xcode-claude` to one or more roles. Common patterns:

| Pattern | Role map example | When to use |
|---------|------------------|-------------|
| Default (no Xcode in pipeline) | builder:codex, tester:claude, reviewer:cursor, integrator:codex | Non-Apple or OKF-only projects |
| Xcode as builder | builder:xcode-claude, tester:claude, reviewer:cursor, integrator:codex | Apple implementation-heavy work |
| Xcode as tester | builder:codex, tester:xcode-claude, reviewer:cursor, integrator:codex | Build/test evidence from Xcode |

Initialize a pipeline (dry-run example):

```bash
scripts/okf-dispatch init-pipeline "Task summary" \
  --pipeline-id my-pipeline \
  --runners builder:xcode-claude,tester:claude,reviewer:cursor,integrator:codex \
  --okf .okf/agents/xcode-claude.md docs/create-new-okf-project-in-xcode.md
```

Consume the next packet for Xcode:

```bash
scripts/okf-dispatch consume --runner xcode-claude --json
```

Complete work and advance:

```bash
scripts/okf-dispatch complete --packet-id <id> --from xcode-claude
```

Xcode must not invoke Codex, Claude Code, or Cursor directly. It updates OKF, writes evidence, and advances dispatch via `scripts/okf-dispatch`.

### 6. Dry verification (no live Xcode required)

Run the checklist in `.okf/prompts/xcode-step4-verification-checklist.md` before live verification. This confirms repo layout, dispatch runner support, and validation — not simulator or signing behavior.

Record results in `.okf/tests/2026-06-28-xcode-step4-dry-verification.md` or append to that file for your project.

### 7. Live verification (requires Xcode)

When a real Apple target exists:

1. Build the project in Xcode (or `xcodebuild` from terminal).
2. Run tests; capture pass/fail summary in `.okf/tests/` or the active handoff.
3. Record simulator, signing, SPM/CocoaPods constraints as OKF risks if they block delivery.
4. Confirm Xcode-connected Claude Agent can read a dispatch packet and act on it in practice.
5. Only then promote `.okf/agents/xcode-claude.md` to `status: active` and `verification_status: reviewed`.

If live verification is deferred, document deferral in the step 4 handoff and keep the agent rule at `draft`.

### 8. Validate

Run:

```bash
scripts/okf-validate
scripts/okf-check-adapters
```

Record validation results in `.okf/log.md`. If validation fails, fix blocking issues or document them in the handoff for Perplexity step 5.

### 9. Write the Xcode to Perplexity handoff

Create a handoff for step 5:

```bash
scripts/okf-handoff perplexity-service-setup --summary "Xcode step 4 complete (dry or live); configure Perplexity as service 5."
```

Use `.okf/handoffs/TEMPLATE-xcode-step4.md` as a starting point.

Fill in:

- **Current state** — steps 1–4 status; dry vs live verification level
- **Completed work** — agent rule updates, dispatch role assignment, test evidence paths
- **Known issues** — live verification pending, signing/simulator constraints
- **Next recommended actions** — Perplexity step 5 via `docs/create-new-okf-project-in-perplexity.md`
- **Validation needed** — any Perplexity Space curation still pending

---

## Handoff payload for step 5 (Perplexity)

Include:

- Current state of Xcode setup (dry verified / live verified / deferred)
- Validation result (`okf-validate`, `okf-check-adapters`)
- Active project brief and requirement paths Perplexity should read
- Known Apple-platform constraints and open research questions
- Confirmation that Perplexity must run **MODE A research only** unless overflow is explicitly requested
- Explicit note if `.okf/agents/xcode-claude.md` remains `draft`

---

## Xcode step 4 completion checklist

Use before declaring step 4 done:

- [ ] Claude Code to Xcode handoff was read.
- [ ] Canonical service order confirmed: Cursor, Codex, Claude Code, Xcode, Perplexity.
- [ ] Steps 1–3 completion verified before editing.
- [ ] `.okf/agents/xcode-claude.md` exists and reflects project constraints (still `draft` unless live verified).
- [ ] Dry verification checklist run (`.okf/prompts/xcode-step4-verification-checklist.md`).
- [ ] Dispatch role map documented if dispatch is enabled (`xcode-claude` runner tested via dry-run when applicable).
- [ ] `scripts/okf-validate` run; result recorded.
- [ ] `scripts/okf-check-adapters` run when adapters touched.
- [ ] `.okf/log.md` records Xcode step 4 status (dry vs live).
- [ ] Xcode to Perplexity handoff exists under `.okf/handoffs/`.
- [ ] Perplexity step 5 not configured yet except stubs and handoff instructions.
- [ ] `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/okf.mdc`, `.codex/hooks.json` not modified out of order.

**Live verification add-ons (when Xcode available):**

- [ ] Build succeeded; evidence in `.okf/tests/` or handoff
- [ ] Tests run; results recorded
- [ ] Agent rule promoted to `active` / `reviewed` only after live evidence

---

## Operating rules during step 4

- Treat `.okf` as the source of curated project context.
- Keep signing secrets, API keys, provisioning profiles, and credentials **out of OKF**.
- Capture build/test evidence under `.okf/tests/` or handoffs — not only in chat.
- Do not replace Perplexity research or overflow roles.
- Do not configure Perplexity Spaces during the Xcode step.
- Advance dispatch manually; do not call other services directly.

---

## Quick reference commands (Xcode step 4)

```bash
# Dry verification checklist (read and execute)
cat .okf/prompts/xcode-step4-verification-checklist.md

# Validate OKF bundle
scripts/okf-validate
scripts/okf-check-adapters

# Dispatch dry-run with xcode-claude as builder
scripts/okf-dispatch init-pipeline "Task summary" \
  --runners builder:xcode-claude,tester:claude,reviewer:cursor,integrator:codex

# Consume packet as Xcode runner
scripts/okf-dispatch consume --runner xcode-claude --json

# Complete and advance
scripts/okf-dispatch complete --packet-id <id> --from xcode-claude

# Handoff for Perplexity
scripts/okf-handoff perplexity-service-setup --summary "Xcode step 4 complete."
```

---

## Related material

- **Operator brief:** `docs/okf-ways-of-working-brief.md`
- Dry verification: `.okf/prompts/xcode-step4-verification-checklist.md`
- Dry test evidence (bootstrap kit): `.okf/tests/2026-06-28-xcode-step4-dry-verification.md`
- Xcode agent rule: `.okf/agents/xcode-claude.md`
- Live verification risk: `.okf/risks/xcode-live-verification-pending.md`
- Dispatch orchestration: `docs/okf-dispatch-orchestration.md`
- Multi-agent pipeline: `.okf/workflows/multi-agent-delivery-pipeline.md`
- Perplexity step 5: `docs/create-new-okf-project-in-perplexity.md`, `docs/configure-perplexity-okf.md`
- Handoff template: `.okf/handoffs/TEMPLATE-xcode-step4.md`
