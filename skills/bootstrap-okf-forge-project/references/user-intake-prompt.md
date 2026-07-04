# User prompt — collect OKF + Forge project setup

Copy the **short variant** below into Cursor Agent chat, or the full prompt when you need explicit phase control.

Canonical operator guide: `docs/new-okf-forge-project-standup.md`  
Skill: `bootstrap-okf-forge-project`  
Script: `scripts/project-intake`

---

## Short variant (recommended)

```markdown
Use bootstrap-okf-forge-project skill. Collect identity (id, name, purpose, owner), paths (target_dir), and GitHub (create repo? owner, visibility). Apply v2 defaults for profile, services, Forge, and dispatch unless I opt out. Write intake/<id>.yaml, validate, render plan, wait for my "approve standup" before apply --execute.
```

---

## Full prompt (copy below)

```markdown
BOOTSTRAP OKF + FORGE PROJECT SETUP — guided intake

Use the **bootstrap-okf-forge-project** skill (`skills/bootstrap-okf-forge-project/SKILL.md`).

Collect required setup information, write `intake/<project-id>.yaml`, validate with `scripts/project-intake`, show the rendered launch plan, and only run `scripts/project-intake apply … --execute` after I explicitly approve.

## Rules

- Ask questions **one phase at a time** (do not dump all questions at once).
- Use **AskQuestion** when choices are finite; use open questions for purpose/scope text.
- **project.id** must be lowercase-dashes (3–64 chars) and must equal the basename of **paths.target_dir**.
- Default profile: **default** (v2 OKF + Forge + dispatch). Mention `legacy-task` only if I ask for ai-task MCP.
- **Apply v2 defaults** for OKF services, Forge, and dispatch — only ask about phases C/E/F/G if I want non-defaults.
- `okf.services` booleans are advisory (which setup guides to follow); they do not change the scaffold.
- Do not run `--execute` until I reply **approve standup** (or equivalent explicit yes).
- After apply, point me to `.okf/handoffs/*-operator-standup.md` and `scripts/operator-ready-check.sh`.

## Required phases

### Phase A — Identity
Collect: project id, display name, purpose (one paragraph), owner.

### Phase B — Paths
Collect: absolute target directory. `forge_siblings_parent` defaults to parent of target.

### Phase D — GitHub
Collect: create repo with `gh`? owner, visibility (private/public), default branch.
Prefill owner from `gh api user` when available.

## Optional phases (only if I deviate from defaults)

### Phase C — Profile
`default` | `legacy-task` (deprecated). `forge-lifecycle` is an alias of `default`.

### Phase E — OKF services
Defaults: cursor, codex, claude, perplexity on; xcode off.

### Phase F — Forge
Defaults: enabled, clone siblings yes, build siblings no, org `nicksinx`.

### Phase G — Dispatch
Defaults: builder→codex, tester→claude, reviewer→cursor, integrator→codex.

## Deliverables

1. `intake/<project-id>.yaml` filled and validated
2. Output of `scripts/project-intake render intake/<project-id>.yaml`
3. After approval: `scripts/project-intake apply intake/<project-id>.yaml --execute`
4. Summary: operator handoff path and post-standup checklist

Start with Phase A. If I have not given a project id yet, ask for it first.
```

---

## After standup

- [ ] Open the new project folder as the Cursor workspace root
- [ ] Reload Cursor window (MCP + project rules)
- [ ] Run `scripts/operator-ready-check.sh`
- [ ] Read `.okf/handoffs/*-operator-standup.md` and `docs/okf-service-operator-skills.md`
- [ ] `docs/create-new-okf-project-in-*.md` for enabled services you will configure first
- [ ] Forge siblings — skip if `apply --execute` already cloned

**Troubleshooting:** missing rules on pre-v2 scaffolds only — bootstrap `docs/install-cursor-rules.md` section B.
