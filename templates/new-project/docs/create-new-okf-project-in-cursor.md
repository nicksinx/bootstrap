# Create New OKF Project in Cursor

Use this document when bootstrapping a **new** OKF-enabled project with Cursor as the first configured service. The same five-step service order applies to every new project so Codex, Claude Code, Xcode, and Perplexity can follow a consistent handoff pattern.

## Canonical service setup order

Configure services in this order for every new OKF project:

| Step | Service | Primary adapter / entry point | When it runs |
|------|---------|------------------------------|--------------|
| **1** | **Cursor** | `.cursor/rules/okf.mdc` | First — scaffold the project and OKF bundle |
| **2** | Codex | `AGENTS.md`, `.codex/hooks.json` | After Cursor handoff — install skills and Codex hooks |
| **3** | Claude Code | `CLAUDE.md`, `.claude/commands/` | After Codex handoff — wire Claude adapter and slash commands |
| **4** | Xcode | `.okf/agents/xcode-claude.md` (or project equivalent) | After Claude handoff — connect Xcode-connected Claude Agent as a dispatch consumer |
| **5** | Perplexity | `.okf/agents/perplexity.md`, `docs/create-new-okf-project-in-perplexity.md` | Last — deep research layer; populate `.okf/references/` with cited, unverified material |

Each step produces a handoff under `.okf/handoffs/` before the next service is configured. Do not skip ahead; later services assume earlier steps completed and validated.

Companion documents (create separately, same order):

- Step 2: *Create New OKF Project in Codex*
- Step 3: *Create New OKF Project in Claude*
- Step 4: *Create New OKF Project in Xcode*
- Step 5: *Create New OKF Project in Perplexity*
- Perplexity configuration: `docs/configure-perplexity-okf.md`

---

## What Cursor does in step 1

Cursor is responsible for **creating the project skeleton** and making `.okf` the durable context layer before any other agent tool is wired in.

Cursor must:

1. Create or open the target project directory.
2. Scaffold the OKF bundle, helper scripts, and thin adapters (Cursor rule included; other adapters as stubs).
3. Record project identity, scope, and initial requirements in OKF concepts.
4. Initialize dispatch queue directories when multi-agent delivery is expected.
5. Validate the bundle and write a handoff for Codex (step 2).

Cursor does **not** need Codex, Claude, or Xcode installed to complete step 1. Cursor must not modify user-global tool configuration outside the project repository.

---

## Prerequisites

- Cursor opened on the parent folder where the new project will live (or on the empty project folder itself).
- Access to the OKF bootstrap kit (Project-1 or an equivalent template repository).
- Python 3 available locally for scaffold and validation scripts.
- Project name, owner, and a one-paragraph purpose statement ready before you start.

---

## Step-by-step: configure Cursor (service 1)

### 1. Choose the project path and inspect it

Decide the absolute path for the new project, for example:

```text
/path/to/my-new-project/
```

Before writing files:

- Confirm the directory is empty, or that overwriting existing scaffold files is explicitly allowed.
- Do not overwrite application source, secrets, or unrelated project files.

### 2. Scaffold the OKF project

Preferred method — run the bundled scaffold script from the OKF bootstrap kit:

```bash
python3 /path/to/Project-1/skills/create-new-okf-project/scripts/create_okf_project.py \
  /path/to/my-new-project \
  --name "My New Project" \
  --owner "team-or-person"
```

Use `--overwrite` only when replacing an existing OKF scaffold is intentional.

The scaffold must include at minimum:

```text
my-new-project/
  .okf/
    index.md
    project.md
    log.md
    requirements/
    features/
    architecture/
    decisions/
    workflows/
    agents/
    prompts/
    handoffs/
    improvements/
    risks/
    tests/
    releases/
    references/
    dispatch/
      ready/
      running/
      done/
      failed/
      pipelines/
  .cursor/rules/okf.mdc
  AGENTS.md                  ← stub for Codex (step 2)
  CLAUDE.md                  ← stub for Claude (step 3)
  PERPLEXITY.md              ← stub for Perplexity (step 5)
  scripts/
    okf-validate
    okf-context-pack
    okf-handoff
    okf-sync-skills
  .claude/commands/okf-sync.md
  docs/
    shared-okf-skills.md
    configure-perplexity-okf.md
    create-new-okf-project-in-xcode.md
    create-new-okf-project-in-perplexity.md
  skills/
    okf-*/
    perplexity-okf-*/
```

If the bootstrap kit includes dispatch support, also copy or reference:

```text
  scripts/okf-dispatch
  docs/okf-dispatch-orchestration.md
  .okf/workflows/multi-agent-delivery-pipeline.md
```

Open the new project in Cursor after scaffolding.

### 3. Configure the Cursor project rule

Confirm `.cursor/rules/okf.mdc` exists and has `alwaysApply: true` in its frontmatter so OKF context loads on every agent session without disabling Cursor global skills.

The rule must stay **thin**. It should:

- Point agents to `.okf/index.md` and `.okf/project.md`.
- List canonical skills under `skills/*/SKILL.md` (when present).
- Require log updates and handoffs after substantive work.
- Explicitly state that Cursor global skills remain valid alongside OKF.

If you copied skills from Project-1, refresh adapters after any canonical skill edit:

```bash
scripts/okf-sync-skills --target cursor
```

Do not duplicate full skill bodies into `.cursor/rules/`.

### 4. Set project identity in OKF

Edit these files before any implementation work:

**`.okf/project.md`** — purpose, scope, in/out of scope, operating model.

**`.okf/index.md`** — navigation index linking requirements, architecture, workflows, handoffs, and local commands.

**`.okf/requirements/`** — at least one primary requirement concept with acceptance criteria.

**`.okf/log.md`** — append an entry recording project creation, scaffold method, and Cursor as the configured first service.

Example log entry:

```markdown
## YYYY-MM-DD

- Bootstrapped OKF project scaffold from Project-1 bootstrap kit.
- Configured Cursor as service 1 (`.cursor/rules/okf.mdc`).
- Pending: Codex (step 2), Claude Code (step 3), Xcode (step 4), Perplexity (step 5).
```

### 5. Initialize multi-agent dispatch (recommended)

When the project will use Codex, Claude, Cursor, and Xcode in a delivery pipeline, create dispatch queue directories:

```bash
mkdir -p .okf/dispatch/{ready,running,done,failed,pipelines}
```

Ensure `scripts/okf-dispatch` is present and executable. Cursor acts as a **project-local packet consumer** for `reviewer` (and other cursor-assigned) roles — agents read typed JSON packets from `.okf/dispatch/ready/` rather than calling other services directly.

See `docs/okf-dispatch-orchestration.md` for queue contracts and runner mapping.

### 6. Leave stub adapters for later services

At the end of step 1, these files may exist as thin stubs generated by the scaffold script. **Do not fully configure them in Cursor** — that is the job of steps 2–5:

| File / path | Configured in step |
|-------------|-------------------|
| `AGENTS.md` | 2 — Codex |
| `.codex/hooks.json` | 2 — Codex |
| `CODEX-SKILL-INSTALL.md` (if present) | 2 — Codex |
| `CLAUDE.md` | 3 — Claude Code |
| `.claude/commands/okf-sync.md` | 3 — Claude Code |
| `.okf/agents/xcode-claude.md` | 4 — Xcode |
| `.okf/agents/perplexity.md`, `.okf/agents/perplexity-overflow.md`, `PERPLEXITY.md` | 5 — Perplexity |

Optionally add placeholder agent concepts under `.okf/agents/` for Codex, Claude, Xcode, and Perplexity with `status: draft` and `verification_status: unverified` so later steps have a clear target.

### 7. Validate the OKF bundle

From the project root:

```bash
scripts/okf-validate
```

Resolve any blocking failures before handoff. Warnings about missing sensitivity or verification fields on draft concepts are acceptable at this stage.

### 8. Write the Cursor → Codex handoff

Create a handoff for step 2:

```bash
scripts/okf-handoff codex-service-setup --summary "Cursor step 1 complete; configure Codex as service 2."
```

Fill in the handoff with:

- **Current state** — scaffold complete, Cursor rule active, validation result.
- **Completed work** — files created, project identity recorded, dispatch initialized (if applicable).
- **Decisions made** — project name, owner, bootstrap kit source, service order commitment.
- **Files changed** — list scaffold paths.
- **Next recommended actions** — explicit instructions for Codex step 2 (see below).
- **Validation needed** — `scripts/okf-validate` pass/fail, any open warnings.

---

## Handoff payload for step 2 (Codex)

Include this checklist in the handoff so Codex receives consistent instructions across projects:

1. Read `.okf/index.md`, `.okf/project.md`, and this handoff.
2. Read `docs/create-new-okf-project-in-cursor.md` for the canonical five-service order.
3. Finalize `AGENTS.md` via `scripts/okf-sync-skills --target codex` (or follow `CODEX-SKILL-INSTALL.md`).
4. Install canonical OKF skills from `skills/` into Codex home when needed.
5. Create or verify `.codex/hooks.json` (for example a `Stop` hook calling `scripts/okf-dispatch advance --from codex` when dispatch is enabled).
6. Update `.okf/agents/codex.md` to `status: active` and record verification evidence.
7. Run `scripts/okf-validate` and append to `.okf/log.md`.
8. Write a handoff for Claude Code (step 3).

---

## Cursor step 1 completion checklist

Use this checklist before declaring step 1 done:

- [ ] Project directory exists and is opened in Cursor.
- [ ] `.okf/index.md`, `.okf/project.md`, and `.okf/log.md` reflect the new project.
- [ ] At least one requirement concept exists under `.okf/requirements/`.
- [ ] `.cursor/rules/okf.mdc` exists with `alwaysApply: true` and stays thin.
- [ ] Helper scripts exist: `okf-validate`, `okf-handoff`, `okf-context-pack`, `okf-sync-skills`.
- [ ] `PERPLEXITY.md`, Perplexity prompts, and four `skills/perplexity-okf-*/SKILL.md` files exist.
- [ ] Dispatch queues exist under `.okf/dispatch/` when multi-agent delivery is planned.
- [ ] `scripts/okf-validate` passes (or failures are documented in the handoff).
- [ ] Handoff for Codex (step 2) exists under `.okf/handoffs/`.
- [ ] `.okf/log.md` records Cursor as the configured first service.
- [ ] `AGENTS.md`, `CLAUDE.md`, Xcode, and Perplexity material are stubs only — not fully configured beyond setup scaffolding.

---

## Operating rules during step 1

- Treat `.okf` as the source of curated context; do not store secrets in OKF or dispatch packets.
- Prefer canonical skills in `skills/*/SKILL.md` over improvising workflows in chat.
- Keep Cursor global skills available; OKF is a project-local overlay.
- Do not install or configure Codex, Claude, Xcode, or Perplexity from Cursor step 1 except by writing stub files and handoff instructions inside the repository.
- Create a handoff before pausing if step 1 cannot finish in one session.

---

## Quick reference commands (Cursor step 1)

```bash
# Scaffold (from bootstrap kit)
python3 /path/to/Project-1/skills/create-new-okf-project/scripts/create_okf_project.py \
  /path/to/my-new-project --name "My New Project"

# Refresh Cursor adapter after skill changes
scripts/okf-sync-skills --target cursor

# Validate bundle
scripts/okf-validate

# Create handoff for Codex
scripts/okf-handoff codex-service-setup --summary "Cursor step 1 complete."

# Initialize dispatch directories (when using multi-agent pipeline)
mkdir -p .okf/dispatch/{ready,running,done,failed,pipelines}
```

---

## Related material

- Canonical skill: `skills/create-new-okf-project/SKILL.md`
- Shared skills model: `docs/shared-okf-skills.md`
- Dispatch orchestration: `docs/okf-dispatch-orchestration.md`
- Perplexity deep research (step 5): `docs/create-new-okf-project-in-perplexity.md`
- Agent lifecycle: `.okf/workflows/agent-okf-lifecycle.md`
- Cursor agent rule: `.okf/agents/cursor.md`
- OKF project profile: `skills/create-new-okf-project/references/okf-project-profile.md`
