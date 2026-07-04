# Install bootstrap-okf-forge-project Cursor skill

The skill guides operators (and Cursor agents) through standardized **project intake** for new OKF + Forge products.

Canonical location: `skills/bootstrap-okf-forge-project/SKILL.md`

Heavy lifting: `scripts/project-intake`

---

## Option A — Use from bootstrap repo (recommended)

1. Clone/open the bootstrap repository in Cursor.
2. Ensure the skill is visible:
   - **Project skill:** it lives at `skills/bootstrap-okf-forge-project/` (Cursor discovers `skills/*/SKILL.md` when indexed from the repo).
   - If your Cursor version only loads `.cursor/skills/`, symlink or copy:

```bash
cd /path/to/bootstrap
mkdir -p .cursor/skills
ln -sf ../../skills/bootstrap-okf-forge-project .cursor/skills/bootstrap-okf-forge-project
```

3. In Agent chat, invoke explicitly — or paste the prompt from `skills/bootstrap-okf-forge-project/references/user-intake-prompt.md`:

```text
Use the bootstrap-okf-forge-project skill to stand up a new OKF + Forge project.
```

4. Follow the skill phases (intake → validate → render → user approval → apply).

---

## Option B — Personal skill (all workspaces)

Copy into your user skills directory:

```bash
mkdir -p ~/.cursor/skills
cp -R /path/to/bootstrap/skills/bootstrap-okf-forge-project ~/.cursor/skills/
```

Edit `SKILL.md` if needed so `paths.bootstrap_root` in generated intake points at your bootstrap clone.

---

## CLI without Cursor

```bash
cd /path/to/bootstrap
chmod +x scripts/project-intake

scripts/project-intake init \
  --project-id my-product \
  --target-dir "$HOME/projects/my-product" \
  -o intake/my-product.yaml

# Edit intake/my-product.yaml (purpose, GitHub, services, forge flags)

scripts/project-intake validate intake/my-product.yaml
scripts/project-intake render intake/my-product.yaml
scripts/project-intake apply intake/my-product.yaml          # launch dry-run
scripts/project-intake apply intake/my-product.yaml --execute  # full standup
```

---

## What gets standardized

| Artifact | Purpose |
|----------|---------|
| `intake/<id>.yaml` | Operator/agent intake record (bootstrap repo) |
| `.okf/project-intake.yaml` | Copy in launched product (audit trail) |
| `.okf/project.md` | Purpose / scope patched from intake |
| `.okf/handoffs/*-operator-standup.md` | First operator handoff |

Schema: `schemas/project-intake.schema.json`

---

## Related

- [install-cursor-rules.md](install-cursor-rules.md) — after launch, install Cursor rules in the product
- [migration-from-legacy-bootstrap.md](migration-from-legacy-bootstrap.md)
- `skills/bootstrap-okf-forge-project/references/intake-example.yaml`
