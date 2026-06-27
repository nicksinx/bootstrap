#!/usr/bin/env python3
import argparse
import datetime as dt
import re
import stat
import sys
import textwrap
from pathlib import Path

OKF_DIRS = [
    "requirements",
    "features",
    "architecture",
    "decisions",
    "components",
    "data",
    "apis",
    "workflows",
    "agents",
    "prompts",
    "risks",
    "tests",
    "releases",
    "handoffs",
    "context-packs",
    "references",
    "improvements",
    "dispatch/ready",
    "dispatch/running",
    "dispatch/done",
    "dispatch/failed",
    "dispatch/pipelines",
]


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "project"


def yaml_list(values):
    return "[" + ", ".join(values) + "]"


def frontmatter(
    concept_type,
    title,
    description,
    resource,
    *,
    status="draft",
    lifecycle_stage="planning",
    owner="project",
    tags=None,
    applies_to=None,
    sensitivity="internal",
    verification_status="unverified",
    timestamp=None,
):
    tags = tags or ["okf"]
    applies_to = applies_to or ["cursor", "claude", "codex", "xcode-claude", "perplexity", "local-agent"]
    timestamp = timestamp or dt.datetime.now().astimezone().isoformat(timespec="seconds")
    return textwrap.dedent(
        f"""\
        ---
        type: {concept_type}
        title: {title}
        description: {description}
        status: {status}
        lifecycle_stage: {lifecycle_stage}
        owner: {owner}
        source_of_truth: true
        resource: {resource}
        tags: {yaml_list(tags)}
        applies_to: {yaml_list(applies_to)}
        sensitivity: {sensitivity}
        verification_status: {verification_status}
        timestamp: {timestamp}
        ---
        """
    )


def write_file(root, relative_path, content, *, overwrite=False, executable=False):
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return "skipped", path
    path.write_text(content, encoding="utf-8")
    if executable:
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return "created" if not path.exists() else "written", path


def adapter_agents():
    return """# Codex OKF Adapter

This repository uses `.okf` as the durable project context layer for Cursor, Codex, Claude Code, Xcode-connected Claude Agent, and Perplexity Desktop Pro.

Canonical OKF skill definitions live in `skills/*/SKILL.md`. For OKF-related delivery, read and follow the relevant canonical skill instead of improvising workflows.

Before substantive project changes, read `.okf/index.md`, `.okf/project.md`, relevant concepts, and recent handoffs.

Keep material changes traceable to OKF requirements, features, decisions, risks, runbooks, improvements, or handoffs.

After substantive changes, update affected OKF concepts, append to `.okf/log.md`, add test evidence when applicable, and create a handoff when work pauses or transfers.

Capture reusable lessons learned under `.okf/improvements/`.

Perplexity Desktop Pro is service 5 for cited research and an ad hoc overflow substitute when a primary runner is blocked. Perplexity never writes the repository directly; Cursor or Codex ingests output and validates OKF.

Do not store secrets in OKF.

Run `scripts/okf-sync-skills` after adding or updating canonical skills to refresh this adapter with a generated skill index.
"""


def adapter_claude():
    return """# Claude OKF Adapter

Use `.okf` as the shared project context layer across Cursor, Codex, Claude Code, Xcode-connected Claude Agent, and Perplexity Desktop Pro.

Canonical OKF skill definitions live in `skills/*/SKILL.md`. For OKF-related delivery, read and follow the relevant canonical skill instead of improvising workflows.

Read `.okf/index.md`, `.okf/project.md`, relevant concepts, and recent handoffs before project changes.

Prefer reviewed, tested, and accepted OKF concepts over draft or unverified material.

Preserve citations, update OKF after substantive changes, and capture lessons learned under `.okf/improvements/`.

Perplexity Desktop Pro is service 5 for cited research and may be used in MODE B overflow when a primary runner is blocked. Cursor or Codex must apply Perplexity output and run validation.

Run `scripts/okf-sync-skills` after adding or updating canonical skills to refresh this adapter with a generated skill index.
"""


def adapter_cursor():
    return """---
description: Use OKF as the shared project context layer alongside existing Cursor skills
alwaysApply: true
---

# OKF Shared Context (project-local overlay)

This rule is a thin project-local overlay. It does **not** replace Cursor's existing global skills, rules, or workflows. Those remain valid and should still be used when they fit the task.

## Shared project context

- `.okf` is the durable shared project context layer for Cursor, Codex, Claude Code, Xcode-connected Claude Agent, and Perplexity Desktop Pro.
- Decisions, requirements, risks, handoffs, lessons learned, and test evidence belong in `.okf`, not only in chat.
- Read `.okf/index.md` and `.okf/project.md` before substantive project changes.
- Check recent `.okf/handoffs/` when continuing or transferring work.
- Perplexity is service 5 for cited research and an overflow substitute only when Cursor/Codex/Claude/Xcode is blocked; it does not write the repo directly.

## Canonical OKF skills

For OKF-related project delivery, follow the canonical skill definitions in `skills/*/SKILL.md` instead of duplicating their workflows in this rule.

Run `scripts/okf-sync-skills` after adding or updating skills to refresh this file with a generated skill index.

## During and after work

- Link material changes to OKF requirements, features, decisions, risks, runbooks, or handoffs.
- Prefer reviewed, tested, and accepted concepts over draft or unverified material.
- Update affected OKF concepts and append a short entry to `.okf/log.md` after substantive changes.
- Create a handoff under `.okf/handoffs/` before pausing unfinished work another agent may continue.
- Do not store secrets, credentials, private keys, or sensitive personal data in OKF.
"""


def adapter_perplexity():
    return """# Perplexity OKF Adapter

Perplexity Desktop Pro participates in this OKF project in two modes:

| Mode | Purpose |
|------|---------|
| **MODE A - RESEARCH** | Service 5 deep research that drafts cited OKF `Reference` concepts |
| **MODE B - OVERFLOW** | Ad hoc substitute for blocked Cursor, Codex, Claude Code, or Xcode runners |

## Configure Perplexity Desktop

1. Open **Perplexity Desktop -> Settings -> Custom instructions**.
2. Paste `.okf/prompts/perplexity-custom-instructions.md`.
3. Attach a curated project-file pack, not the whole repo: `.okf/project.md`, `.okf/index.md`, this file, relevant workflow/prompt docs, the latest handoff, and the active requirement or spec.
4. Attach the four Perplexity project skills from `skills/perplexity-okf-*/SKILL.md`.

Perplexity never writes this repository directly, executes hooks, or advances dispatch queues. Cursor or Codex ingests outputs, updates OKF, and runs `scripts/okf-validate`.

## MODE A - RESEARCH

- Use after Cursor, Codex, Claude Code, and Xcode setup.
- Follow `docs/create-new-okf-project-in-perplexity.md`.
- Draft references under `.okf/references/` with `verification_status: unverified` and `source_of_truth: false`.

## MODE B - OVERFLOW

- Use only when a primary runner is blocked by usage limits, outage, policy, or explicit user choice.
- Follow `.okf/workflows/perplexity-overflow-failover.md` and `.okf/prompts/perplexity-overflow-failover.md`.
- Complete the same OKF role contract (builder, tester, reviewer, or integrator), then hand output back for Cursor/Codex integration.

## Related OKF Material

- Research agent: `.okf/agents/perplexity.md`
- Overflow agent: `.okf/agents/perplexity-overflow.md`
- Configuration guide: `docs/configure-perplexity-okf.md`
"""


def adapter_claude_command_okf_sync():
    return """Refresh all OKF tool adapters from canonical skill definitions.

Run this after editing any `skills/*/SKILL.md` file to propagate changes to `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/okf.mdc`, `PERPLEXITY.md`, and `.okf/agents/future-service.md`.

Steps:
1. Run `scripts/okf-sync-skills` from the project root.
2. Run `scripts/okf-validate` to confirm the bundle passes.
3. Append a short note to `.okf/log.md` describing what changed.

If you only want to preview changes without writing files, run `scripts/okf-sync-skills --dry-run`.
To refresh a single adapter, run `scripts/okf-sync-skills --target <codex|claude|cursor|perplexity|future>`.
"""


OKF_SYNC_SKILLS = r'''#!/usr/bin/env python3
"""Refresh thin tool adapters from canonical OKF skills under skills/*/SKILL.md."""

import argparse
import datetime as dt
import sys
from pathlib import Path

CANONICAL_SKILLS_DIR = "skills"
ADAPTER_TARGETS = {
    "codex": "AGENTS.md",
    "claude": "CLAUDE.md",
    "cursor": ".cursor/rules/okf.mdc",
    "perplexity": "PERPLEXITY.md",
    "future": ".okf/agents/future-service.md",
}

SKILL_INDEX_HEADER = """\
## Canonical OKF Skills

Canonical skill definitions live under `skills/*/SKILL.md`. Tool adapters stay thin and point here instead of duplicating skill bodies.

"""


def find_root():
    current = Path.cwd().resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".okf").is_dir() and (candidate / CANONICAL_SKILLS_DIR).is_dir():
            return candidate
    return current


def list_skills(root):
    skills_root = root / CANONICAL_SKILLS_DIR
    skills = []
    if not skills_root.is_dir():
        return skills
    for skill_md in sorted(skills_root.glob("*/SKILL.md")):
        name = skill_md.relative_to(skills_root).parts[0]
        description = ""
        text = skill_md.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            end = text.find("\n---", 4)
            if end != -1:
                for line in text[4:end].splitlines():
                    if line.startswith("description:"):
                        description = line.split(":", 1)[1].strip().strip('"').strip("'")
                        break
        skills.append({"name": name, "path": skill_md.relative_to(root).as_posix(), "description": description})
    return skills


def skill_index_markdown(skills):
    lines = [SKILL_INDEX_HEADER]
    for skill in skills:
        desc = skill["description"] or "See SKILL.md"
        lines.append(f"- `{skill['name']}` — {desc} (`{skill['path']}`)")
    lines.append("")
    return "\n".join(lines)


def adapter_codex(skills, root):
    index = skill_index_markdown(skills)
    return f"""# Codex OKF Adapter

This repository uses `.okf` as the durable shared project context layer for Cursor, Codex, Claude Code, Xcode-connected Claude Agent, and Perplexity Desktop Pro.

Canonical OKF skill definitions live in `skills/*/SKILL.md`. For OKF-related delivery, read and follow the relevant canonical skill instead of improvising workflows.

Before substantive project changes:

1. Read `.okf/index.md`.
2. Read `.okf/project.md`.
3. Read relevant requirement, feature, architecture, decision, risk, test, and handoff concepts.
4. Check for recent files in `.okf/handoffs/`.
5. Treat `deprecated`, `superseded`, and `archived` concepts as unsafe for direct implementation unless the user explicitly asks for historical work.
6. Use `skills/okf-reader/SKILL.md` when triage is needed.

During implementation:

1. Link material work to an OKF requirement, feature, decision, runbook, or handoff.
2. Prefer `reviewed`, `tested`, and `accepted` concepts over `draft` or `unverified` concepts.
3. Do not invent durable requirements that are not represented in OKF.
4. Keep secrets, credentials, private keys, and sensitive personal data out of OKF.
5. Update tests in line with OKF acceptance criteria.
6. Follow the matching canonical skill under `skills/` for concept writing, handoffs, audits, risks, citations, context packs, and validation.

After substantive changes:

1. Update affected OKF concepts.
2. Append to `.okf/log.md`.
3. Add test evidence when validation was performed.
4. Create a handoff in `.okf/handoffs/` when work is paused, transferred, or context is likely to be lost.

Perplexity Desktop Pro is service 5 for cited research and an ad hoc overflow substitute when a primary runner is blocked. Perplexity never writes the repository directly; Cursor or Codex ingests output and validates OKF.

{index}Generated by `scripts/okf-sync-skills` for {root.name}.
"""


def adapter_claude(skills, root):
    index = skill_index_markdown(skills)
    return f"""# Claude OKF Adapter

Use `.okf` as the shared source of curated project context across Cursor, Codex, Claude Code, Xcode-connected Claude Agent, and Perplexity Desktop Pro.

Canonical OKF skill definitions live in `skills/*/SKILL.md`. For OKF-related delivery, read and follow the relevant canonical skill instead of improvising workflows.

Read in this order before changing project files:

1. `.okf/index.md`
2. `.okf/project.md`
3. Relevant concepts linked from the task
4. Recent `.okf/handoffs/` notes
5. Tool adapter concepts under `.okf/agents/` when the task involves agent behavior
6. The matching canonical skill under `skills/` when the task matches an OKF skill contract

Prefer reviewed, tested, and accepted OKF concepts over draft or unverified material. Preserve citations and external references when updating concepts. If project state changes, update OKF and append a concise entry to `.okf/log.md`.

Create a handoff note before stopping if another agent may need to continue the work.

Perplexity Desktop Pro is service 5 for cited research and may be used in MODE B overflow when a primary runner is blocked. Cursor or Codex must apply Perplexity output and run validation.

{index}Generated by `scripts/okf-sync-skills` for {root.name}.
"""


def adapter_cursor(skills, root):
    skill_lines = "\n".join(f"- `{s['name']}` (`{s['path']}`)" for s in skills)
    return f"""---
description: Use OKF as the shared project context layer alongside existing Cursor skills
alwaysApply: true
---

# OKF Shared Context (project-local overlay)

This rule is a thin project-local overlay. It does **not** replace Cursor's existing global skills, rules, or workflows. Those remain valid and should still be used when they fit the task.

## Shared project context

- `.okf` is the durable shared project context layer for Cursor, Codex, Claude Code, Xcode-connected Claude Agent, and Perplexity Desktop Pro.
- Decisions, requirements, risks, handoffs, lessons learned, and test evidence belong in `.okf`, not only in chat.
- Read `.okf/index.md` and `.okf/project.md` before substantive project changes.
- Check recent `.okf/handoffs/` when continuing or transferring work.
- Perplexity is service 5 for cited research and an overflow substitute only when Cursor/Codex/Claude/Xcode is blocked; it does not write the repo directly.

## Canonical OKF skills

For OKF-related project delivery, follow the canonical skill definitions in `skills/*/SKILL.md` instead of duplicating their workflows in this rule:

{skill_lines}

## During and after work

- Link material changes to OKF requirements, features, decisions, risks, runbooks, or handoffs.
- Prefer reviewed, tested, and accepted concepts over draft or unverified material.
- Update affected OKF concepts and append a short entry to `.okf/log.md` after substantive changes.
- Create a handoff under `.okf/handoffs/` before pausing unfinished work another agent may continue.
- Do not store secrets, credentials, private keys, or sensitive personal data in OKF.

Generated by `scripts/okf-sync-skills` for {root.name}.
"""


def adapter_perplexity(skills, root):
    index = skill_index_markdown(skills)
    return f"""# Perplexity OKF Adapter

Perplexity Desktop Pro participates in this OKF project in two modes:

| Mode | Purpose |
|------|---------|
| **Research (service 5)** | Deep cited research into `.okf/references/` |
| **Overflow (ad hoc)** | Substitute for blocked primary runners (Codex, Claude, Cursor, Xcode) |

## Configure Perplexity Desktop

1. Open **Perplexity Desktop -> Settings -> Custom instructions**.
2. Paste the block from `.okf/prompts/perplexity-custom-instructions.md`.
3. Attach a curated Project Files pack, not the whole repo.
4. Attach the four Perplexity Project Skills from `skills/perplexity-okf-*/SKILL.md`.
5. Follow `docs/configure-perplexity-okf.md` for research and overflow workflows.

Perplexity does not execute repo hooks or advance dispatch queues. Cursor or Codex ingests outputs and runs `scripts/okf-validate`.

## Before research (MODE A)

1. Read `.okf/index.md`, `.okf/project.md`, and recent `.okf/handoffs/`.
2. Use `docs/create-new-okf-project-in-perplexity.md` or `.okf/prompts/perplexity-deep-research-setup.md`.
3. Save Reference drafts to `.okf/references/` via Cursor/Codex with `verification_status: unverified`.

## Before overflow (MODE B)

1. Write an overflow handoff when a primary runner is blocked.
2. Use `.okf/prompts/perplexity-overflow-failover.md`.
3. Integrator applies deliverables; append `.okf/log.md`; resume primary runner when available.

Agent rules: `.okf/agents/perplexity.md`, `.okf/agents/perplexity-overflow.md`

{index}Generated by `scripts/okf-sync-skills` for {root.name}.
"""


def adapter_future(skills, root):
    timestamp = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    return f"""---
type: Agent Rule
title: Future Service OKF Adapter
description: Thin adapter template for services that participate in the shared OKF operating model.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: false
resource: .okf/agents/future-service.md
tags: [okf, adapter, future-service]
applies_to: [local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: {timestamp}
---

# Future Service OKF Adapter

Use `.okf` as the shared project context layer.

Canonical OKF skill definitions live in `skills/*/SKILL.md`. Read the relevant skill before OKF-related delivery.

{skill_index_markdown(skills)}Install or mirror this file for the target service, then run `scripts/okf-sync-skills --target all` after canonical skill changes.
"""


ADAPTER_BUILDERS = {
    "codex": adapter_codex,
    "claude": adapter_claude,
    "cursor": adapter_cursor,
    "perplexity": adapter_perplexity,
    "future": adapter_future,
}


def write_adapter(root, target, content, dry_run):
    rel_path = ADAPTER_TARGETS[target]
    path = root / rel_path
    if dry_run:
        print(f"DRY-RUN: would write {rel_path} ({len(content.encode('utf-8'))} bytes)")
        return "dry-run"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"wrote {rel_path}")
    return "written"


def main():
    parser = argparse.ArgumentParser(description="Sync thin OKF tool adapters from canonical skills.")
    parser.add_argument(
        "--target",
        choices=["codex", "claude", "cursor", "perplexity", "future", "all"],
        default="all",
        help="Which adapter(s) to refresh (default: all)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show actions without writing files")
    parser.add_argument("--list-skills", action="store_true", help="List canonical skills and exit")
    args = parser.parse_args()

    root = find_root()
    skills = list_skills(root)

    if args.list_skills:
        if not skills:
            print("No canonical skills found under skills/*/SKILL.md")
            return 1
        for skill in skills:
            print(f"{skill['name']}\t{skill['path']}\t{skill['description']}")
        return 0

    if not (root / ".okf").is_dir():
        print("FAIL: .okf directory not found")
        return 1
    if not skills:
        print("WARN: no canonical skills found under skills/*/SKILL.md")

    selected = list(ADAPTER_BUILDERS.keys()) if args.target == "all" else [args.target]
    for target in selected:
        builder = ADAPTER_BUILDERS[target]
        content = builder(skills, root)
        write_adapter(root, target, content, args.dry_run)

    mode = "dry-run" if args.dry_run else "sync"
    print(f"OKF adapter {mode} complete for {root} ({len(skills)} skill(s), target={args.target})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


OKF_VALIDATE = r'''#!/usr/bin/env python3
import datetime as dt
import re
import sys
from pathlib import Path

CRITICAL_TYPES = {
    "Project", "Requirement", "Feature", "Architecture", "Decision", "Workflow",
    "Runbook", "Agent Rule", "Agent Skill", "Tool Adapter", "Risk", "Test Case",
    "Test Evidence", "Release", "Handoff", "Improvement", "Lesson Learned",
    "Retrospective",
}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bghp_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"(?i)\b(password|api[_-]?key|token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}"),
]


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    return text[4:end]


def parse_simple_yaml(frontmatter):
    data = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def valid_iso8601(value):
    try:
        dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def main():
    root = Path.cwd()
    okf = root / ".okf"
    failures = []
    warnings = []
    if not okf.is_dir():
        print("FAIL: .okf directory not found")
        return 1

    for path in sorted(okf.rglob("*.md")):
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            failures.append(f"{rel}: likely secret detected")
        frontmatter = split_frontmatter(text)
        if frontmatter is None:
            failures.append(f"{rel}: missing YAML frontmatter")
            continue
        data = parse_simple_yaml(frontmatter)
        concept_type = data.get("type", "")
        if not concept_type:
            failures.append(f"{rel}: missing non-empty type")
        timestamp = data.get("timestamp")
        if timestamp and not valid_iso8601(timestamp):
            failures.append(f"{rel}: timestamp is not ISO 8601")
        if concept_type in CRITICAL_TYPES:
            for field in ("status", "lifecycle_stage", "sensitivity", "verification_status"):
                if not data.get(field):
                    warnings.append(f"{rel}: missing {field}")

    for warning in warnings:
        print(f"WARN: {warning}")
    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        print(f"OKF validation failed: {len(failures)} failure(s), {len(warnings)} warning(s)")
        return 1
    print(f"OKF validation passed: {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


OKF_CONTEXT_PACK = r'''#!/usr/bin/env python3
import argparse
import datetime as dt
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Build a small Markdown context pack from OKF files.")
    parser.add_argument("paths", nargs="*", help="Files or directories to include.")
    parser.add_argument("-o", "--output", default="tmp/okf-context-pack.md")
    args = parser.parse_args()

    root = Path.cwd()
    selected = args.paths or [".okf/index.md", ".okf/project.md", ".okf/log.md"]
    files = []
    for item in selected:
        path = root / item
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.is_file():
            files.append(path)

    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    chunks = [
        "# OKF Context Pack",
        "",
        f"Generated: {dt.datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "Generated task context, not durable source-of-context.",
        "",
    ]
    for path in files:
        chunks.extend([f"## {path.relative_to(root)}", "", path.read_text(encoding="utf-8"), ""])
    output.write_text("\n".join(chunks), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
'''


OKF_HANDOFF = r'''#!/usr/bin/env python3
import argparse
import datetime as dt
import re
from pathlib import Path


def slugify(value):
    value = re.sub(r"[^a-z0-9]+", "-", value.lower().strip())
    return value.strip("-") or "handoff"


def main():
    parser = argparse.ArgumentParser(description="Create an OKF handoff document.")
    parser.add_argument("task", nargs="?", default="handoff")
    args = parser.parse_args()
    root = Path.cwd()
    now = dt.datetime.now().astimezone()
    slug = slugify(args.task)
    path = root / ".okf" / "handoffs" / f"{now.date().isoformat()}-{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    title = " ".join(part.capitalize() for part in slug.split("-"))
    path.write_text(f"""---
type: Handoff
title: {title}
description: Continuity note for paused or transferred work.
status: active
lifecycle_stage: build
owner: project
source_of_truth: true
resource: .okf/handoffs/{path.name}
tags: [okf, handoff]
applies_to: [cursor, claude, codex, xcode-claude, perplexity, local-agent]
sensitivity: internal
verification_status: unverified
timestamp: {now.isoformat(timespec='seconds')}
---

# Current State

TBD.

# Completed Work

TBD.

# Decisions Made

TBD.

# Files Changed

TBD.

# Known Issues

TBD.

# Next Recommended Actions

TBD.

# Validation Needed

TBD.

# Context Pack

TBD.
""", encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
'''


def copy_bundled_skills(root, overwrite):
    """Copy project-local skill folders that ship with this bootstrap kit."""
    try:
        source_skills = Path(__file__).resolve().parents[2]
    except IndexError:
        return []
    if not (source_skills / "create-new-okf-project" / "SKILL.md").is_file():
        return []

    results = []
    for source in sorted(source_skills.rglob("*")):
        if not source.is_file():
            continue
        if "__pycache__" in source.parts or source.suffix in {".pyc", ".pyo"}:
            continue
        relative = source.relative_to(source_skills)
        destination = root / "skills" / relative
        if destination.exists() and destination.resolve() == source.resolve():
            continue
        executable = bool(source.stat().st_mode & stat.S_IXUSR)
        content = source.read_text(encoding="utf-8")
        results.append(write_file(root, Path("skills") / relative, content, overwrite=overwrite, executable=executable))
    return results


BOOTSTRAP_COPY_PATHS = [
    "scripts/okf-dispatch",
    "scripts/okf-check-adapters",
    "docs/okf-dispatch-orchestration.md",
    "docs/okf-ways-of-working-brief.md",
    "docs/create-new-okf-project-in-cursor.md",
    "docs/create-new-okf-project-in-codex.md",
    "docs/create-new-okf-project-in-claude.md",
    "docs/create-new-okf-project-in-xcode.md",
    "docs/create-new-okf-project-in-perplexity.md",
    "docs/configure-perplexity-okf.md",
    "docs/perplexity-project-files-and-skills.md",
    "docs/skill-frontmatter-compatibility.md",
    ".okf/handoffs/README.md",
    ".okf/handoffs/TEMPLATE.md",
    ".okf/handoffs/TEMPLATE-tester.md",
    ".okf/handoffs/TEMPLATE-reviewer.md",
    ".okf/handoffs/TEMPLATE-xcode-step4.md",
    ".okf/context-packs/INDEX.md",
    ".okf/prompts/perplexity-post-curation-smoke-test.md",
    ".okf/prompts/xcode-step4-verification-checklist.md",
    ".okf/handoffs/TEMPLATE-xcode-step4.md",
    ".okf/risks/xcode-live-verification-pending.md",
    ".codex/hooks.json",
    "CODEX-SKILL-INSTALL.md",
]


def copy_optional_bootstrap_files(root, overwrite):
    """Copy optional helper files from the bootstrap repository when available.

    When the script runs inside the OKF bootstrap kit (Project-1 layout),
    ``source_root`` resolves to the kit root and canonical docs replace any
    embedded scaffold stubs (always overwrite on copy).

    When run from a sparse/minimal tree without bootstrap siblings, missing
    sources are skipped and embedded stubs from ``service_operating_files``
    remain the fallback.
    """
    try:
        source_root = Path(__file__).resolve().parents[3]
    except IndexError:
        return []

    results = []
    for relative_path in BOOTSTRAP_COPY_PATHS:
        source = source_root / relative_path
        if not source.is_file():
            continue
        destination = root / relative_path
        if destination.exists() and destination.resolve() == source.resolve():
            continue
        executable = bool(source.stat().st_mode & stat.S_IXUSR)
        content = source.read_text(encoding="utf-8")
        results.append(
            write_file(
                root,
                relative_path,
                content,
                overwrite=True,
                executable=executable,
            )
        )
    return results


def service_operating_files(project_name, owner, timestamp):
    files = {}
    files["docs/shared-okf-skills.md"] = f"""# Shared OKF Skills Operating Model

{project_name} uses `.okf` as a durable context layer shared by Cursor, Codex, Claude Code, Xcode-connected Claude Agent, and Perplexity Desktop Pro.

Canonical skill definitions live under `skills/*/SKILL.md`. Tool adapters stay thin and point back to those skills.

## Service Roles

| Service | Adapter | Role |
|---------|---------|------|
| Cursor | `.cursor/rules/okf.mdc` | Service 1: scaffold and project-local rule overlay |
| Codex | `AGENTS.md` | Service 2: coding agent, skill install target, hooks |
| Claude Code | `CLAUDE.md` | Service 3: delivery agent and slash-command consumer |
| Xcode | `.okf/agents/xcode-claude.md` | Service 4: Apple-platform dispatch consumer |
| Perplexity Desktop Pro | `PERPLEXITY.md` | Service 5: cited deep research into `.okf/references/` |

Perplexity may also run in MODE B overflow when a primary runner is blocked. It completes the same OKF role contract but does not write the repo or advance dispatch.

## Propagation

After editing any skill, run:

```bash
scripts/okf-sync-skills
scripts/okf-validate
```
"""
    files["docs/configure-perplexity-okf.md"] = """# Configure Perplexity for OKF

Perplexity Desktop Pro participates in OKF through three layers:

1. **Custom instructions**: paste `.okf/prompts/perplexity-custom-instructions.md` into Perplexity Desktop settings.
2. **Project Files**: attach a curated pack, not the whole repo. Start with `.okf/project.md`, `.okf/index.md`, `PERPLEXITY.md`, relevant workflows/prompts, the latest handoff, and the active requirement or spec.
3. **Project Skills**: attach the four Perplexity-specific skills from `skills/perplexity-okf-*/SKILL.md`.

## MODE A - RESEARCH

Use Perplexity as service 5 after Cursor, Codex, Claude Code, and Xcode are configured. It drafts cited `Reference` concepts under `.okf/references/` with `verification_status: unverified` and `source_of_truth: false`.

## MODE B - OVERFLOW

Use overflow only when Codex, Claude Code, Cursor, or Xcode is blocked by usage limits, outage, policy, or explicit user choice. Perplexity completes the same OKF role contract and returns output for Cursor or Codex to apply.

Perplexity Computer is out of scope unless explicitly added later.
"""
    files["docs/create-new-okf-project-in-perplexity.md"] = """# Create New OKF Project in Perplexity

Perplexity Desktop Pro is service 5 in the canonical setup order:

1. Cursor
2. Codex
3. Claude Code
4. Xcode-connected Claude Agent
5. Perplexity Desktop Pro

Perplexity performs deep research only. It does not scaffold code, mutate repository files, or promote research to accepted project truth.

## Research Prompt Shape

Start the thread with `MODE A - RESEARCH`, attach the curated OKF project-file pack, and ask Perplexity to produce OKF `Reference` concept drafts for domain, architecture, compliance, vendor/API, and risk research.

Every reference must include citations, retrieval dates, limitations, `status: draft`, `source_of_truth: false`, and `verification_status: unverified`.

Cursor or Codex saves the references, updates `.okf/index.md` and `.okf/log.md`, and runs `scripts/okf-validate`.
"""
    files["docs/create-new-okf-project-in-xcode.md"] = """# Create New OKF Project in Xcode

Use this guide for service 4 in the canonical OKF setup order. Xcode-connected Claude Agent participates as a local dispatch consumer for Apple-platform build, test, and integration work.

## Role

- Read `.okf/index.md`, `.okf/project.md`, and the latest handoff before acting.
- Consume dispatch packets assigned to `xcode-claude` when dispatch is enabled.
- Keep Apple build, signing, simulator, and package-manager details in OKF handoffs or test evidence.
- Do not replace Perplexity research or overflow roles.

## Completion

After Xcode setup, write a handoff for Perplexity service 5 and run `scripts/okf-validate`.
"""
    files[".okf/features/shared-okf-skills.md"] = frontmatter(
        "Feature",
        "Shared OKF Skills",
        "Shared OKF skill and adapter model for the five-service operating pattern.",
        ".okf/features/shared-okf-skills.md",
        status="active",
        lifecycle_stage="build",
        owner=owner,
        tags=["okf", "skills", "shared-operating-model", "perplexity"],
        applies_to=["cursor", "claude", "codex", "xcode-claude", "perplexity", "local-agent"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + """# User Value

Agents can share OKF project context, skill contracts, handoff format, and validation flow across Cursor, Codex, Claude Code, Xcode, and Perplexity.

# Scope

The scaffold includes canonical OKF skills under `skills/` and Perplexity adapter skills under `skills/perplexity-okf-*/`.

# Out of Scope

- Replacing user-global tool settings.
- Using Perplexity Computer as an automated runner.
- Storing secrets in OKF.

# Behaviour

`scripts/okf-sync-skills` refreshes thin adapters, including `PERPLEXITY.md`. Perplexity service 5 writes cited research drafts only through Cursor/Codex ingestion; overflow is manual and logged.

# UX Notes

Start with `docs/shared-okf-skills.md`, then use the service-specific setup guide for the active tool.

# Data / API Impact

No external API is required by the scaffold itself.

# Test Expectations

- `scripts/okf-validate` passes.
- `scripts/okf-sync-skills --target perplexity --dry-run` reports `PERPLEXITY.md`.

# Related Concepts

- `.okf/workflows/multi-agent-delivery-pipeline.md`
- `.okf/workflows/perplexity-research-cycle.md`
- `.okf/workflows/perplexity-overflow-failover.md`
"""
    files[".okf/agents/xcode-claude.md"] = frontmatter(
        "Agent Rule",
        "Xcode Claude OKF Agent Rule",
        "Rules for an Xcode-connected Claude Agent acting as service 4.",
        ".okf/agents/xcode-claude.md",
        status="draft",
        lifecycle_stage="operate",
        owner=owner,
        tags=["okf", "xcode", "claude", "agent-rule"],
        applies_to=["xcode-claude"],
        timestamp=timestamp,
    ) + """# Purpose

Define the Xcode-connected Claude Agent role for Apple-platform implementation, build, and test work.

# Required Behaviour

- Read `.okf/index.md`, `.okf/project.md`, relevant requirements, and recent handoffs.
- Consume dispatch packets for `xcode-claude` when dispatch is enabled.
- Capture build/test evidence under `.okf/tests/` or handoffs.
- Handoff to Perplexity service 5 when research setup is next.

# Prohibited Behaviour

- Do not store signing secrets, private keys, or credentials in OKF.
- Do not advance Perplexity research or overflow automatically.
"""
    files[".okf/agents/perplexity.md"] = frontmatter(
        "Agent Rule",
        "Perplexity OKF Agent Rule",
        "Rules for Perplexity Desktop Pro as service 5 research layer.",
        ".okf/agents/perplexity.md",
        status="active",
        lifecycle_stage="operate",
        owner=owner,
        tags=["okf", "perplexity", "agent-rule", "deep-research"],
        applies_to=["perplexity"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + """# Purpose

Use Perplexity Desktop Pro as service 5 for cited deep research that drafts OKF `Reference` concepts.

# Required Behaviour

- Run in MODE A - RESEARCH for planned research.
- Use `.okf/prompts/perplexity-custom-instructions.md`.
- Draft references in `.okf/references/` with `verification_status: unverified`.
- Include URLs, retrieval dates, limitations, and suggested OKF links.

# Prohibited Behaviour

- Do not write the repository directly.
- Do not promote research to accepted requirements or decisions.
- Do not use Perplexity Computer unless explicitly added later.
"""
    files[".okf/agents/perplexity-overflow.md"] = frontmatter(
        "Agent Rule",
        "Perplexity Overflow OKF Agent Rule",
        "Rules for Perplexity Desktop Pro as an ad hoc overflow substitute.",
        ".okf/agents/perplexity-overflow.md",
        status="active",
        lifecycle_stage="operate",
        owner=owner,
        tags=["okf", "perplexity", "overflow", "agent-rule"],
        applies_to=["perplexity"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + """# Purpose

Allow Perplexity to substitute for a blocked Cursor, Codex, Claude Code, or Xcode runner while preserving the same OKF role contract.

# Required Behaviour

- Run in MODE B - OVERFLOW.
- Read the overflow handoff and active acceptance criteria.
- Complete the assigned builder, tester, reviewer, or integrator deliverable.
- Return output for Cursor/Codex to apply and validate.

# Prohibited Behaviour

- Do not advance dispatch queues.
- Do not claim repo changes were applied.
- Do not fail over silently; record every event in `.okf/log.md` and a handoff.
"""
    files[".okf/workflows/multi-agent-delivery-pipeline.md"] = frontmatter(
        "Workflow",
        "Multi-Agent Delivery Pipeline",
        "File-queue dispatch workflow for OKF roles across the five-service model.",
        ".okf/workflows/multi-agent-delivery-pipeline.md",
        status="active",
        lifecycle_stage="build",
        owner=owner,
        tags=["okf", "workflow", "dispatch", "multi-agent"],
        applies_to=["cursor", "claude", "codex", "xcode-claude", "perplexity", "local-agent"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + """# Purpose

Coordinate builder, tester, reviewer, and integrator work through `.okf/dispatch/` rather than direct service-to-service calls.

# Roles

Role order is `builder` -> `tester` -> `reviewer` -> `integrator`.

# Runners

- `cursor`: project-local packet consumer.
- `codex`: Codex runner and hook participant.
- `claude`: Claude Code runner.
- `xcode-claude`: local Xcode-connected consumer.
- `perplexity-overflow`: manual overflow only; does not consume dispatch JSON directly.

# Required Behaviour

Update OKF concepts, append `.okf/log.md`, and run `scripts/okf-validate` after substantive work.
"""
    files[".okf/workflows/perplexity-research-cycle.md"] = frontmatter(
        "Workflow",
        "Perplexity Research Cycle",
        "Workflow for Perplexity service 5 research into OKF references.",
        ".okf/workflows/perplexity-research-cycle.md",
        status="active",
        lifecycle_stage="operate",
        owner=owner,
        tags=["okf", "workflow", "perplexity", "research"],
        applies_to=["perplexity", "cursor", "codex"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + """# Purpose

Use Perplexity Desktop Pro for cited research and keep outputs as unverified OKF references until reviewed.

# Flow

1. Cursor/Codex builds a curated context pack.
2. Perplexity runs MODE A - RESEARCH.
3. Perplexity drafts `Reference` concepts.
4. Cursor/Codex saves references, updates index/log, links affected concepts, and validates.
"""
    files[".okf/workflows/perplexity-overflow-failover.md"] = frontmatter(
        "Workflow",
        "Perplexity Overflow Failover",
        "Manual overflow workflow for blocked primary OKF runners.",
        ".okf/workflows/perplexity-overflow-failover.md",
        status="active",
        lifecycle_stage="operate",
        owner=owner,
        tags=["okf", "workflow", "perplexity", "overflow"],
        applies_to=["perplexity", "cursor", "codex", "claude", "xcode-claude"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + """# Purpose

Use Perplexity in MODE B - OVERFLOW when a primary runner is blocked.

# Required Handoff Fields

- `execution_mode: overflow`
- `primary_runner`
- `overflow_runner: perplexity-overflow`
- `failover_reason`
- `role`
- `acceptance_criteria`

# Flow

1. Record the block in a handoff.
2. Send the curated context pack to Perplexity.
3. Perplexity completes the same OKF role deliverable.
4. Cursor/Codex applies output, validates, logs the failover, and resumes primary delivery.
"""
    files[".okf/prompts/perplexity-custom-instructions.md"] = frontmatter(
        "Reference",
        "Perplexity Custom Instructions",
        "Custom instructions to paste into Perplexity Desktop for OKF work.",
        ".okf/prompts/perplexity-custom-instructions.md",
        status="active",
        lifecycle_stage="operate",
        owner=owner,
        tags=["okf", "perplexity", "prompt"],
        applies_to=["perplexity"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + """# Custom Instructions

You participate in OKF projects in two modes.

MODE A - RESEARCH: act as service 5. Produce cited draft OKF `Reference` concepts only. Use `verification_status: unverified`; do not write repository files or promote requirements.

MODE B - OVERFLOW: substitute for a blocked Cursor, Codex, Claude Code, or Xcode runner. Complete the same role contract and return output for Cursor/Codex integration. Do not advance dispatch queues.
"""
    files[".okf/prompts/perplexity-deep-research-setup.md"] = frontmatter(
        "Reference",
        "Perplexity Deep Research Setup",
        "Reusable MODE A research prompt starter.",
        ".okf/prompts/perplexity-deep-research-setup.md",
        status="active",
        lifecycle_stage="operate",
        owner=owner,
        tags=["okf", "perplexity", "prompt", "research"],
        applies_to=["perplexity"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + """# Prompt

MODE A - RESEARCH

Use the attached OKF project files to produce cited draft `Reference` concepts for the requested research topics. Mark every output `status: draft`, `source_of_truth: false`, and `verification_status: unverified`. Include URLs, retrieval dates, limitations, and suggested OKF links.
"""
    files[".okf/prompts/perplexity-overflow-failover.md"] = frontmatter(
        "Reference",
        "Perplexity Overflow Failover Prompt",
        "Reusable MODE B overflow prompt starter.",
        ".okf/prompts/perplexity-overflow-failover.md",
        status="active",
        lifecycle_stage="operate",
        owner=owner,
        tags=["okf", "perplexity", "prompt", "overflow"],
        applies_to=["perplexity"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + """# Prompt

MODE B - OVERFLOW

Primary runner: {{primary_runner}}
Failover reason: {{failover_reason}}
Role: {{builder|tester|reviewer|integrator}}

Complete the same OKF role contract using the attached context. Return patch-ready instructions, validation notes, and an Overflow completion block. Do not claim repo writes or dispatch advancement.
"""
    files[".okf/tests/perplexity-operating-model-validation.md"] = frontmatter(
        "Test Case",
        "Perplexity Operating Model Validation",
        "Checks that the Perplexity research and overflow model is present in a new scaffold.",
        ".okf/tests/perplexity-operating-model-validation.md",
        status="active",
        lifecycle_stage="test",
        owner=owner,
        tags=["okf", "perplexity", "validation"],
        applies_to=["cursor", "codex", "perplexity"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + """# Test Objective

Confirm new scaffolds include Perplexity service 5 and overflow material.

# Test Cases

1. Confirm `PERPLEXITY.md` exists when adapters are enabled.
2. Confirm `scripts/okf-sync-skills --target perplexity --dry-run` succeeds.
3. Confirm the four `skills/perplexity-okf-*/SKILL.md` files exist after bundled skills are copied.
4. Confirm `.okf/prompts/perplexity-custom-instructions.md` exists.

# Expected Result

The project has a complete Perplexity configuration path without requiring repo-wide file attachment in Perplexity Desktop.
"""
    return files


def initial_files(project_name, owner, timestamp):
    slug = slugify(project_name)
    today = timestamp.split("T", 1)[0]
    files = {}
    files[".gitignore"] = ".DS_Store\ntmp/\n"
    files[".okf/index.md"] = frontmatter(
        "Reference",
        "OKF Bundle Index",
        f"Navigation index for {project_name}.",
        ".okf/index.md",
        status="active",
        lifecycle_stage="build",
        owner=owner,
        tags=["okf", "index"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + f"""# OKF Bundle Index

## Required Reading Order

1. Read `.okf/index.md`.
2. Read `.okf/project.md`.
3. Read relevant concepts for the active task.
4. Check recent handoffs.
5. Check `.okf/improvements/` for applicable lessons learned.

## Canonical Service Setup Order

1. Cursor
2. Codex
3. Claude Code
4. Xcode-connected Claude Agent
5. Perplexity Desktop Pro

Perplexity overflow is an ad hoc failover mode, not a sixth setup step.

## Core Areas

- Project: `.okf/project.md`
- Log: `.okf/log.md`
- Shared skills: `.okf/features/shared-okf-skills.md`
- Requirements: `.okf/requirements/`
- Architecture: `.okf/architecture/`
- Decisions: `.okf/decisions/`
- Workflows: `.okf/workflows/`
- Agent rules: `.okf/agents/`
- Prompts: `.okf/prompts/`
- Risks: `.okf/risks/`
- Tests: `.okf/tests/`
- Handoffs: `.okf/handoffs/`
- References: `.okf/references/`
- Continuous improvement: `.okf/improvements/`

## Tool Adapters

- Cursor: `.cursor/rules/okf.mdc`
- Codex: `AGENTS.md`
- Claude Code: `CLAUDE.md`
- Handoffs guide: `.okf/handoffs/README.md`
- Context packs: `.okf/context-packs/INDEX.md`
- Perplexity: `PERPLEXITY.md`
- Perplexity Files/Skills: `docs/perplexity-project-files-and-skills.md`
"""
    files[".okf/project.md"] = frontmatter(
        "Project",
        project_name,
        f"Project overview for {project_name}.",
        ".okf/project.md",
        status="active",
        lifecycle_stage="planning",
        owner=owner,
        tags=["okf", "project", slug],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + f"""# {project_name}

## Purpose

TBD.

## Scope

TBD.

## Out of Scope

TBD.

## Operating Model

Use `.okf` as source-of-context. Keep durable project knowledge in OKF and keep tool adapters thin.

Five-service setup order:

1. Cursor scaffolds project context.
2. Codex wires skills, hooks, and repository work.
3. Claude Code consumes the shared OKF context and commands.
4. Xcode-connected Claude Agent handles Apple-platform local work when applicable.
5. Perplexity Desktop Pro performs cited deep research into `.okf/references/`.

Perplexity overflow is allowed only when a primary runner is blocked. Cursor or Codex applies overflow output and runs validation.
"""
    files[".okf/log.md"] = frontmatter(
        "Reference",
        "OKF Project Log",
        "Chronological record of material project knowledge changes.",
        ".okf/log.md",
        status="active",
        lifecycle_stage="operate",
        owner=owner,
        tags=["okf", "log"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + f"""# OKF Project Log

## {today}

- Created initial OKF project scaffold for {project_name}.
- Initialized five-service OKF operating model: Cursor, Codex, Claude Code, Xcode, and Perplexity.
- Added Perplexity MODE A research and MODE B overflow docs, prompts, workflows, and agent rules.
"""
    files[".okf/requirements/example.md"] = frontmatter(
        "Requirement",
        "Example Requirement",
        "One-sentence requirement summary.",
        ".okf/requirements/example.md",
        owner=owner,
        tags=["okf", "requirement"],
        timestamp=timestamp,
    ) + """# Intent

TBD.

# Requirement

TBD.

# Acceptance Criteria

1. TBD.

# Dependencies

TBD.

# Risks

TBD.

# Verification

TBD.

# Citations

TBD.
"""
    files[".okf/architecture/example.md"] = frontmatter(
        "Architecture",
        "Example Architecture",
        "One-sentence architecture summary.",
        ".okf/architecture/example.md",
        owner=owner,
        tags=["okf", "architecture"],
        timestamp=timestamp,
    ) + """# Context

TBD.

# Current Design

TBD.

# Constraints

TBD.

# Interfaces

TBD.

# Dependencies

TBD.

# Failure Modes

TBD.

# Open Questions

TBD.

# Related Decisions

TBD.
"""
    files[".okf/decisions/0001-use-okf-as-context-layer.md"] = frontmatter(
        "Decision",
        "Use OKF as the Shared Context Layer",
        "Keep durable project context in OKF and use tool adapters as thin entrypoints.",
        ".okf/decisions/0001-use-okf-as-context-layer.md",
        status="active",
        lifecycle_stage="planning",
        owner=owner,
        tags=["okf", "decision", "context"],
        verification_status="accepted",
        timestamp=timestamp,
    ) + """# Decision

Use `.okf` as the durable project context layer.

# Context

LLM-assisted projects need portable, inspectable, version-controlled context.

# Options Considered

1. Store durable context in each tool adapter.
2. Store durable context in `.okf` and keep adapters thin.

# Rationale

The OKF bundle reduces duplication and keeps project knowledge reviewable.

# Consequences

Agents must read OKF before substantive work and update OKF after material changes.

# Reversal Conditions

Revisit if another reviewed text-first source becomes the durable project context layer.

# Related Concepts

- `.okf/project.md`
"""
    files[".okf/risks/example.md"] = frontmatter(
        "Risk",
        "Example Risk",
        "One-sentence risk summary.",
        ".okf/risks/example.md",
        owner=owner,
        tags=["okf", "risk"],
        timestamp=timestamp,
    ) + """# Risk

TBD.

# Impact

TBD.

# Likelihood

TBD.

# Mitigations

TBD.

# Monitoring

TBD.
"""
    files[".okf/handoffs/example.md"] = frontmatter(
        "Handoff",
        "Example Handoff",
        "Continuity note for paused or transferred work.",
        ".okf/handoffs/example.md",
        owner=owner,
        tags=["okf", "handoff"],
        timestamp=timestamp,
    ) + """# Current State

TBD.

# Completed Work

TBD.

# Decisions Made

TBD.

# Files Changed

TBD.

# Known Issues

TBD.

# Next Recommended Actions

TBD.

# Validation Needed

TBD.

# Context Pack

TBD.
"""
    files[".okf/improvements/continuous-improvement-repository.md"] = frontmatter(
        "Improvement",
        "Continuous Improvement Repository",
        "Defines where lessons learned, retrospectives, and process improvements are captured.",
        ".okf/improvements/continuous-improvement-repository.md",
        status="active",
        lifecycle_stage="operate",
        owner=owner,
        tags=["okf", "continuous-improvement", "lessons-learned"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + """# Observation

Projects improve faster when lessons learned are captured as durable knowledge.

# Context

Agent workflows, validation results, tool limitations, release issues, and handoffs often produce reusable lessons.

# Impact

If lessons stay only in chat or handoffs, future agents repeat avoidable mistakes.

# Recommendation

Capture reusable lessons under `.okf/improvements/` and promote accepted improvements into templates, scripts, skills, adapters, or agent rules.

# Action Items

1. Add lesson learned, improvement, or retrospective concepts when project workflow changes.
2. Review improvement concepts at milestones, releases, incidents, and major handoffs.

# Related Concepts

- `.okf/project.md`
- `.okf/log.md`

# Review Cadence

Review before release, after incidents, after substantial handoffs, and during retrospectives.
"""
    files[".okf/tests/okf-validation-plan.md"] = frontmatter(
        "Test Case",
        "OKF Validation Plan",
        "Validation checks for this OKF-enabled project.",
        ".okf/tests/okf-validation-plan.md",
        status="active",
        lifecycle_stage="test",
        owner=owner,
        tags=["okf", "validation", "tests"],
        verification_status="reviewed",
        timestamp=timestamp,
    ) + """# Test Objective

Confirm that the OKF bundle is readable, structured, and safe to use.

# Test Cases

1. Run `scripts/okf-validate`.
2. Confirm required adapters exist (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules/okf.mdc`, `PERPLEXITY.md`).
3. Confirm `.okf/improvements/`, `.okf/references/`, and Perplexity prompts exist.
4. Run `scripts/okf-sync-skills --target perplexity --dry-run` to confirm the sync script detects Perplexity project skills.
5. Run `scripts/okf-check-adapters` after adapter sync to detect index drift.

# Expected Result

Validation passes with no failures. Sync script reports expected adapter targets, including `perplexity`.

# Evidence

Record command output summaries in `.okf/log.md` or a `Test Evidence` concept.
"""
    files.update(service_operating_files(project_name, owner, timestamp))
    return files


def create_project(target, project_name, owner, overwrite, include_adapters, include_scripts, include_skills):
    root = target.resolve()
    root.mkdir(parents=True, exist_ok=True)
    okf = root / ".okf"
    okf.mkdir(exist_ok=True)
    for directory in OKF_DIRS:
        (okf / directory).mkdir(parents=True, exist_ok=True)

    timestamp = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    results = []
    for relative_path, content in initial_files(project_name, owner, timestamp).items():
        results.append(write_file(root, relative_path, content, overwrite=overwrite))

    if include_adapters:
        results.append(write_file(root, "AGENTS.md", adapter_agents(), overwrite=overwrite))
        results.append(write_file(root, "CLAUDE.md", adapter_claude(), overwrite=overwrite))
        results.append(write_file(root, ".cursor/rules/okf.mdc", adapter_cursor(), overwrite=overwrite))
        results.append(write_file(root, "PERPLEXITY.md", adapter_perplexity(), overwrite=overwrite))

    if include_skills:
        results.extend(copy_bundled_skills(root, overwrite))

    if include_scripts:
        results.append(write_file(root, "scripts/okf-validate", OKF_VALIDATE, overwrite=overwrite, executable=True))
        results.append(write_file(root, "scripts/okf-context-pack", OKF_CONTEXT_PACK, overwrite=overwrite, executable=True))
        results.append(write_file(root, "scripts/okf-handoff", OKF_HANDOFF, overwrite=overwrite, executable=True))
        results.append(write_file(root, "scripts/okf-sync-skills", OKF_SYNC_SKILLS, overwrite=overwrite, executable=True))
        results.extend(copy_optional_bootstrap_files(root, overwrite))

    if include_adapters:
        results.append(write_file(root, ".claude/commands/okf-sync.md", adapter_claude_command_okf_sync(), overwrite=overwrite))

    return root, results


def main():
    parser = argparse.ArgumentParser(description="Create a new OKF-enabled project scaffold.")
    parser.add_argument("target", help="Target project directory.")
    parser.add_argument("--name", help="Project display name. Defaults to target folder name.")
    parser.add_argument("--owner", default="project", help="Owner value for OKF frontmatter.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing scaffold files.")
    parser.add_argument("--no-adapters", action="store_true", help="Do not create AGENTS.md, CLAUDE.md, Cursor rules, or PERPLEXITY.md.")
    parser.add_argument("--no-scripts", action="store_true", help="Do not create helper scripts.")
    parser.add_argument("--no-skills", action="store_true", help="Do not copy bundled OKF skills into the new project.")
    args = parser.parse_args()

    target = Path(args.target)
    project_name = args.name or target.name
    root, results = create_project(
        target,
        project_name,
        args.owner,
        args.overwrite,
        not args.no_adapters,
        not args.no_scripts,
        not args.no_skills,
    )

    created = [path for status, path in results if status in {"created", "written"}]
    skipped = [path for status, path in results if status == "skipped"]
    print(f"OKF project scaffold ready: {root}")
    print(f"Files written: {len(created)}")
    if skipped:
        print(f"Files skipped because they already existed: {len(skipped)}")
        print("Use --overwrite only when replacing existing scaffold files is intended.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
