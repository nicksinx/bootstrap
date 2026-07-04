# Create New OKF Project in Codex

Use this document when configuring **Codex as the second service** in a new OKF-enabled project. Cursor must complete step 1 first, including the OKF scaffold, Cursor project rule, validation attempt, and Cursor to Codex handoff.

This document is intended to be passed as context to Codex, Claude Code, Cursor, Xcode-connected Claude Agent, or a future service so every new project follows the same service setup order.

## Canonical service setup order

Configure services in this order for every new OKF project:

| Step | Service | Primary adapter / entry point | When it runs |
|------|---------|------------------------------|--------------|
| **1** | Cursor | `.cursor/rules/okf.mdc` | First - scaffold the project and OKF bundle |
| **2** | **Codex** | `AGENTS.md`, `.codex/hooks.json` | After Cursor handoff - install skills and Codex hooks |
| **3** | Claude Code | `CLAUDE.md`, `.claude/commands/` | After Codex handoff - wire Claude adapter and slash commands |
| **4** | Xcode | `.okf/agents/xcode-claude.md` or project equivalent | Last - connect Xcode-connected Claude Agent as a dispatch consumer |

Each step produces a handoff under `.okf/handoffs/` before the next service is configured. Do not skip ahead; later services assume earlier steps completed and validated.

Companion documents:

- Step 1: `docs/create-new-okf-project-in-cursor.md`
- Step 2: `docs/create-new-okf-project-in-codex.md`
- Step 3: *Create New OKF Project in Claude* (create separately)
- Step 4: *Create New OKF Project in Xcode* (create separately)

---

## What Codex does in step 2

Codex is responsible for making the project usable from Codex while preserving the OKF operating model created by Cursor.

Codex must:

1. Read the Cursor handoff and confirm step 1 is complete enough to continue.
2. Configure the Codex project adapter in `AGENTS.md`.
3. Install or document native Codex skill availability from canonical `skills/*/SKILL.md`.
4. Create or verify project-local Codex hooks under `.codex/hooks.json` when dispatch is enabled.
5. Verify multi-agent dispatch does not call other services directly.
6. Update the Codex OKF agent concept and project log.
7. Validate the OKF bundle.
8. Write a Codex to Claude Code handoff for step 3.

Codex does **not** fully configure Claude Code, Cursor, or Xcode in step 2. It may refresh thin generated stubs, but step 3 owns Claude Code and step 4 owns Xcode.

---

## Prerequisites

Before Codex starts step 2, the project should already contain:

```text
.okf/
.cursor/rules/okf.mdc
AGENTS.md
CLAUDE.md
scripts/okf-validate
scripts/okf-context-pack
scripts/okf-handoff
scripts/okf-sync-skills
skills/
docs/create-new-okf-project-in-cursor.md
```

If multi-agent delivery is planned, the project should also contain:

```text
scripts/okf-dispatch
.okf/dispatch/
docs/okf-dispatch-orchestration.md
.okf/workflows/multi-agent-delivery-pipeline.md
```

If these files are missing, Codex should record the gap in `.okf/log.md` and either repair the scaffold from the OKF bootstrap kit or stop with a handoff explaining what Cursor needs to complete.

---

## Step-by-step: configure Codex (service 2)

### 1. Open the project root in Codex

Start Codex from the new project root:

```bash
cd /path/to/my-new-project
codex
```

For a non-interactive check, use:

```bash
codex exec --sandbox workspace-write "Read .okf/index.md and summarize the Codex setup state."
```

If the project is not yet a Git repository, initialize Git before serious work unless the project owner explicitly chooses another version-control path.

### 2. Read required context

Codex must read these files before editing:

1. `.okf/index.md`
2. `.okf/project.md`
3. Latest Cursor to Codex handoff under `.okf/handoffs/`
4. `docs/create-new-okf-project-in-cursor.md`
5. `docs/shared-okf-skills.md` when present
6. `docs/okf-dispatch-orchestration.md` when dispatch is enabled
7. `skills/create-new-okf-project/SKILL.md`
8. Relevant `skills/okf-*/SKILL.md` files

Codex should confirm the canonical service order in its working notes:

```text
Cursor first, Codex second, Claude Code third, Xcode fourth.
```

### 3. Confirm Cursor step 1 completion

Before configuring Codex, verify:

- `.cursor/rules/okf.mdc` exists and remains a thin project-local overlay.
- `.okf/index.md`, `.okf/project.md`, and `.okf/log.md` identify the new project.
- At least one requirement concept exists under `.okf/requirements/`.
- A Cursor to Codex handoff exists under `.okf/handoffs/`.
- `scripts/okf-validate` can be run.
- Cursor has not fully configured Codex, Claude Code, or Xcode out of order.

If Cursor changed Codex-specific files beyond stubs, preserve useful work but re-align it to this document and the shared OKF model.

### 4. Refresh the Codex adapter

Run:

```bash
scripts/okf-sync-skills --target codex
```

This should refresh `AGENTS.md` from canonical skills without copying full skill bodies into the adapter.

Check that `AGENTS.md`:

- Points to `.okf/index.md` and `.okf/project.md`.
- References canonical `skills/*/SKILL.md`.
- Requires OKF log updates and handoffs after substantive work.
- Keeps secrets out of OKF.
- Does not duplicate large skill bodies.

Do not edit `.cursor/rules/okf.mdc` during step 2 unless the sync script must repair a broken generated adapter. Cursor remains service 1 and its global skills must stay untouched.

### 5. Install Codex-native OKF skills when needed

The canonical skill source remains the project-local `skills/` directory. Native Codex installation is a convenience layer so Codex can trigger the same skills by name.

From the project root:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/create-new-okf-project skills/okf-* "${CODEX_HOME:-$HOME/.codex}/skills/"
```

If the project includes `CODEX-SKILL-INSTALL.md`, follow it for validation commands.

Rules for installed skills:

- Do not edit installed copies as the source of truth.
- Make canonical changes in project `skills/*/SKILL.md`.
- Re-run the copy command after canonical skill updates.
- Use `scripts/okf-sync-skills` to refresh adapters after canonical skill changes.

### 6. Configure Codex hooks for dispatch

If the project uses the OKF dispatch queue, create or verify:

```text
.codex/hooks.json
```

The Codex hook should enqueue or advance dispatch state; it should not directly invoke Claude Code, Cursor, or Xcode.

Expected shape:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/scripts/okf-dispatch\" advance --from codex",
            "timeout": 30,
            "statusMessage": "Advancing OKF dispatch"
          }
        ]
      }
    ]
  }
}
```

After adding or changing hooks, start a fresh Codex session and review/trust project hooks if Codex asks. In the Codex CLI, use:

```text
/hooks
```

Do not bypass hook trust for ordinary local development.

### 7. Verify dispatch runner mapping

If dispatch is enabled, confirm `docs/okf-dispatch-orchestration.md` and the dispatch script agree on runner mapping.

Default role mapping should remain:

| Role | Default runner |
|------|----------------|
| `builder` | `codex` |
| `tester` | `claude` |
| `reviewer` | `cursor` |
| `integrator` | `codex` |

Codex may create builder or integrator packets, but it must not call Claude Code, Cursor, or Xcode directly. It should write typed packets under `.okf/dispatch/ready/` and let the assigned service consume them.

### 8. Update Codex OKF concepts

Review and update:

```text
.okf/agents/codex.md
```

The Codex agent concept should state:

- Codex is service 2 in the new-project setup order.
- Codex reads OKF before substantive edits.
- Codex uses `AGENTS.md` and canonical `skills/*/SKILL.md`.
- Codex hooks may advance dispatch state but must not directly drive other services.
- Codex records validation evidence and handoffs.

If the concept was a draft placeholder, move it to `status: active` only after `AGENTS.md`, native skill installation guidance, and hooks are verified.

### 9. Validate

Run:

```bash
scripts/okf-validate
```

If available, also run a safe adapter check:

```bash
scripts/okf-sync-skills --target codex --dry-run
```

Record validation results in `.okf/log.md`. If validation fails, fix blocking issues or document them in the Codex to Claude handoff.

### 10. Write the Codex to Claude Code handoff

Create a handoff for step 3:

```bash
scripts/okf-handoff claude-service-setup --summary "Codex step 2 complete; configure Claude Code as service 3."
```

Fill in the handoff with:

- **Current state** - Cursor step 1 complete, Codex adapter configured, validation result.
- **Completed work** - `AGENTS.md`, Codex skill installation status, `.codex/hooks.json`, dispatch verification.
- **Decisions made** - service order confirmed, canonical skills remain in `skills/`, hooks enqueue rather than directly call services.
- **Files changed** - list Codex-related files.
- **Known issues** - any validation warnings, hook trust steps, missing dispatch pieces.
- **Next recommended actions** - explicit Claude Code step 3 checklist.
- **Validation needed** - any Claude-specific checks still pending.

---

## Handoff payload for step 3 (Claude Code)

Include this checklist in the handoff so Claude Code receives consistent instructions across projects:

1. Read `.okf/index.md`, `.okf/project.md`, the Cursor handoff, and the Codex handoff.
2. Read `docs/create-new-okf-project-in-cursor.md` and `docs/create-new-okf-project-in-codex.md` for the canonical service order.
3. Confirm Cursor is step 1, Codex is step 2, Claude Code is step 3, and Xcode is step 4.
4. Run or verify `scripts/okf-sync-skills --target claude`.
5. Finalize `CLAUDE.md` and `.claude/commands/` as thin project-local adapters.
6. Do not modify Cursor global skills or Codex installed skill copies.
7. Preserve canonical skill definitions in `skills/*/SKILL.md`.
8. Run `scripts/okf-validate`.
9. Append to `.okf/log.md`.
10. Write a handoff for Xcode-connected Claude Agent (step 4).

---

## Codex step 2 completion checklist

Use this checklist before declaring step 2 done:

- [ ] Cursor to Codex handoff was read.
- [ ] Canonical service order was confirmed: Cursor, Codex, Claude Code, Xcode.
- [ ] `AGENTS.md` was refreshed or verified via `scripts/okf-sync-skills --target codex`.
- [ ] Codex-native OKF skill installation was completed or clearly documented as pending.
- [ ] `.codex/hooks.json` exists when dispatch is enabled.
- [ ] Codex hooks enqueue or advance dispatch only; they do not directly call Claude Code, Cursor, or Xcode.
- [ ] `.okf/agents/codex.md` reflects Codex as service 2.
- [ ] `scripts/okf-validate` was run and the result recorded.
- [ ] `.okf/log.md` records Codex as the configured second service.
- [ ] A Codex to Claude Code handoff exists under `.okf/handoffs/`.
- [ ] Claude Code and Xcode remain unconfigured except for thin stubs and handoff instructions.

---

## Operating rules during step 2

- Treat `.okf` as the source of curated project context.
- Treat `skills/*/SKILL.md` as the canonical OKF skill definitions.
- Keep `AGENTS.md` thin and generated where possible.
- Do not store secrets, API keys, tokens, private keys, signing credentials, or personal data in OKF.
- Do not let installed Codex skill copies become the source of truth.
- Do not modify Cursor global skills.
- Do not fully configure Claude Code or Xcode during the Codex step.
- Use dispatch packets for cross-service handoff; do not drive other services directly from Codex hooks.
