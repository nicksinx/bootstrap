# Codex Skill Install

This project includes OKF skills under `skills/`. Install them into Codex by copying the skill folders into Codex's skill directory.

From this project folder:

```bash
cd /Users/dv/Projects/testrunner/Project-1
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/create-new-okf-project skills/okf-* "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Validate the local skill folders before or after copying:

```bash
for skill in skills/create-new-okf-project skills/okf-*; do
  PYTHONPATH=/Users/dv/.cache/uv/archive-v0/Vq3DxWaKCfNRUmWt python3 /Users/dv/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill"
done
```

Start a new Codex thread, or reload Codex if needed, then invoke the skills by name:

```text
Use $okf-reader to load project context before this task.
Use $okf-concept-writer to add a new OKF requirement.
Use $okf-handoff-writer to create a handoff before stopping.
Use $okf-conformance-validator to check the OKF bundle.
Use $create-new-okf-project to scaffold a new OKF-enabled project.
```

To update an installed skill after editing this project, repeat the `cp -R` command above.
