# User prompt — collect OKF + Forge project setup

Copy everything inside the fenced block below into Cursor Agent chat **from the bootstrap repository** to start standardized project intake.

Skill: `bootstrap-okf-forge-project`  
Script: `scripts/project-intake`

---

## Prompt (copy below)

```markdown
BOOTSTRAP OKF + FORGE PROJECT SETUP — guided intake

Use the **bootstrap-okf-forge-project** skill (`skills/bootstrap-okf-forge-project/SKILL.md`).

Your job is to collect all required project setup information from me, write a valid `intake/<project-id>.yaml`, validate it with `scripts/project-intake`, show me the rendered launch plan, and only run `scripts/project-intake apply … --execute` after I explicitly approve.

## Rules

- Ask questions **one phase at a time** (do not dump all questions at once).
- Use **AskQuestion** when choices are finite; use open questions for purpose/scope text.
- **project.id** must be lowercase-dashes (3–64 chars) and must equal the basename of **paths.target_dir**.
- Default profile: **default** (v2 OKF + Forge + dispatch). Mention `legacy-task` only if I ask for ai-task MCP.
- Do not run `--execute` until I reply **approve standup** (or equivalent explicit yes).
- After apply, give me the post-launch checklist (MCP reload, five-service setup guides, Forge siblings).

## Phases to complete

### Phase A — Identity
Collect: project id, display name, purpose (one paragraph), scope summary, out of scope, owner.

### Phase B — Paths
Collect: absolute target directory, forge siblings parent directory (default: parent of target).

### Phase C — Profile
Confirm: `default` | `forge-lifecycle` (alias) | `legacy-task` (deprecated).

### Phase D — GitHub
Collect: create repo with gh? owner, visibility (private/public), default branch.

### Phase E — OKF services
Confirm which I will configure: cursor, codex, claude, xcode, perplexity (booleans).

### Phase F — Forge
Collect: enable Forge MCP, clone siblings after launch, build siblings now (slow), GitHub org for Forge repos (default nicksinx).

### Phase G — Dispatch
Confirm runners or accept defaults: builder→codex, tester→claude, reviewer→cursor, integrator→codex.

## Deliverables

1. `intake/<project-id>.yaml` filled and validated
2. Output of `scripts/project-intake render intake/<project-id>.yaml`
3. After approval: `scripts/project-intake apply intake/<project-id>.yaml --execute`
4. Summary of what was created and my next operator steps

Start with Phase A. If I have not given a project id yet, ask for it first.
```

---

## Short variant

```markdown
Use bootstrap-okf-forge-project skill. Interview me phase-by-phase (identity, paths, GitHub, OKF services, Forge, dispatch). Write intake/<id>.yaml, validate, render plan, wait for my "approve standup" before apply --execute.
```

---

## After standup

- [ ] Open the new project folder as the Cursor workspace root
- [ ] Reload MCP (`.cursor/mcp.json` should exist)
- [ ] `docs/install-cursor-rules.md` if rules missing
- [ ] `docs/create-new-okf-project-in-*.md` per enabled service
- [ ] `scripts/forge-clone-siblings.sh` if not run during apply
