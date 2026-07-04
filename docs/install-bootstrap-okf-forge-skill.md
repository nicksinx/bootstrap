# Install bootstrap-okf-forge-project Cursor skill

The skill guides operators (and Cursor agents) through standardized **project intake** for new OKF + Forge products.

**Operator cheat sheet (start here):** [new-okf-forge-project-standup.md](new-okf-forge-project-standup.md) · [offline export](new-okf-forge-project-standup-offline.md) · [operator-guides.md](operator-guides.md)

Canonical skill: `skills/bootstrap-okf-forge-project/SKILL.md`  
Heavy lifting: `scripts/project-intake`

---

## Option A — Personal skill (repeat operators, recommended)

```bash
mkdir -p ~/.cursor/skills
cp -R /path/to/bootstrap/skills/bootstrap-okf-forge-project ~/.cursor/skills/
```

Works from any workspace. Edit `SKILL.md` only if your bootstrap clone path is non-standard.

---

## Option B — Bootstrap repo only

1. Open the bootstrap repository in Cursor.
2. Most builds discover `skills/*/SKILL.md` automatically.
3. If not indexed:

```bash
cd /path/to/bootstrap
mkdir -p .cursor/skills
ln -sf ../../skills/bootstrap-okf-forge-project .cursor/skills/bootstrap-okf-forge-project
```

4. In Agent chat:

```text
Use the bootstrap-okf-forge-project skill to stand up a new OKF + Forge project.
```

Or paste from `skills/bootstrap-okf-forge-project/references/user-intake-prompt.md`.

---

## Express CLI (no agent)

```bash
cd /path/to/bootstrap
scripts/project-intake quick \
  --project-id my-product \
  --target-dir "$HOME/projects/my-product" \
  --purpose "Why this product exists." \
  --owner platform-team

scripts/project-intake validate intake/my-product.yaml
scripts/project-intake render intake/my-product.yaml
scripts/project-intake apply intake/my-product.yaml --execute
```

`quick` prefills `github.owner` from `gh api user` when logged in. See [new-okf-forge-project-standup.md](new-okf-forge-project-standup.md) for full flow.

---

## What gets standardized

| Artifact | Purpose |
|----------|---------|
| `intake/<id>.yaml` | Operator/agent intake record (bootstrap repo) |
| `.okf/project-intake.yaml` | Copy in launched product (audit trail) |
| `.okf/project.md` | Purpose / scope patched from intake |
| `.okf/handoffs/*-operator-standup.md` | First operator handoff with post-standup checklist |

Schema: `schemas/project-intake.schema.json`

---

## Related

- [new-okf-forge-project-standup.md](new-okf-forge-project-standup.md) — full operator guide
- [install-cursor-rules.md](install-cursor-rules.md) — troubleshooting for pre-v2 products only
- [migration-from-legacy-bootstrap.md](migration-from-legacy-bootstrap.md)
- `skills/bootstrap-okf-forge-project/references/intake-example.yaml`
