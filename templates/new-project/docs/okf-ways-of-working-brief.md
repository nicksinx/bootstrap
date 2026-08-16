---
type: Reference
title: OKF Ways of Working Brief
description: Operator-facing brief for the Project-1 five-service OKF operating model, dispatch, Perplexity, and validation workflow.
status: stable
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: docs/okf-ways-of-working-brief.md
tags: [okf, operating-model, operator-guide, brief]
applies_to: [cursor, claude, codex, xcode-claude, perplexity, local-agent]
sensitivity: internal
verification_status: reviewed
stale_after: 2026-11-16
generated: { by: process:okf-index-graph-freshness, at: 2026-08-16T17:25:01+01:00 }
---

# Project-1 OKF Ways of Working Brief

Operator guide for the OKF bootstrap kit. All paths below are **repo-relative**.

## Executive Summary

Project-1 standardizes OKF work around a **five-service setup order**: Cursor, Codex, Claude Code, Xcode, then Perplexity Desktop Pro. Cursor is a **project-local OKF overlay** and does not replace global Cursor skills. Canonical workflows live in `skills/*/SKILL.md`; tool adapters stay thin and are regenerated from those skills via `scripts/okf-sync-skills`.

Perplexity is the **cited research layer** for draft `.okf/references/` material. It never writes the repository directly. **MODE B overflow** substitutes for a blocked primary runner when usage limits, outages, or policy block delivery — it is **not** a sixth setup step.

**Handoffs** (`.okf/handoffs/`) are for active work transfer. **Context packs** (`.okf/context-packs/`) are ephemeral paste bundles, not source of truth.

Operators should run `scripts/okf-validate --strict`, check deterministic index and adapter drift, review freshness, and keep secrets out of OKF. Use `scripts/okf-visualize` when a graph is more useful than another context dump.

---

## What Changed

### Services

| Step | Service | Role |
|------|---------|------|
| 1 | Cursor | Scaffold; project-local OKF overlay |
| 2 | Codex | Skills, hooks, builder/dispatch runner |
| 3 | Claude Code | Delivery agent, slash commands |
| 4 | Xcode | Apple-platform dispatch consumer |
| 5 | Perplexity Desktop Pro | Cited deep research into `.okf/references/` |

**Overflow (ad hoc):** Perplexity MODE B can substitute for a blocked runner. Cursor or Codex applies the output.

### Perplexity (three layers)

1. **Custom instructions** — `.okf/prompts/perplexity-custom-instructions.md`
2. **Project Files** — curated ~8–14 files per `docs/perplexity-project-files-and-skills.md`
3. **Project Skills** — `skills/perplexity-okf-*/SKILL.md`

See `docs/configure-perplexity-okf.md`.

### Skills and adapters

- Canonical skills: `skills/*/SKILL.md`
- Perplexity adapter skills: extended frontmatter (`applies_to`, `okf_mode`, `canonical_skill`) — see `docs/skill-frontmatter-compatibility.md`
- Regenerate adapters: `scripts/okf-sync-skills`
- Check drift: `scripts/okf-check-adapters`

### Dispatch and overflow

- Pipeline: `scripts/okf-dispatch` — see `docs/okf-dispatch-orchestration.md` (§ Role handoff expectations)
- Role handoff templates: `.okf/handoffs/TEMPLATE-tester.md`, `TEMPLATE-reviewer.md` — see README selection table
- Dry-run evidence: `.okf/tests/2026-06-28-dispatch-dry-run.md`
- Overflow metadata:

```bash
scripts/okf-dispatch overflow --packet-id <id> --reason usage_limit --primary-runner codex
```

### Validation

Run `scripts/okf-validate --strict`, `scripts/okf-index --check`, `scripts/okf-freshness --check`, and `scripts/okf-check-adapters`. Draft References must remain `verification_status: unverified` and `source_of_truth: false`.

Directory `index.md` files contain a marked generated block maintained by `scripts/okf-index`; prose outside that block remains operator-owned. `stale_after` is a review deadline, not an automatic trust promotion, lifecycle change, or deletion instruction.

### Optional integration surfaces

- `scripts/okf-mcp-server` is a disabled-by-default, path-contained read-only query pilot. It is separate from Forge lifecycle MCPs and exposes no mutation tools.
- `.okf/computations/bootstrap-integrity.md` is a spec-valid `Attested Computation`; its receipt/verdict JSON remains a local experiment under `.okf-runtime/`.
- OpenWiki is an opt-in generated sidecar enabled with `--with-openwiki`. `scripts/openwiki-sidecar` stages execution and imports only `openwiki/` plus complete OpenWiki marker blocks.

---

## Dispatch Pipeline

Roles run in **fixed order**:

```text
builder → tester → reviewer → integrator
```

| Role | Typical responsibility | Default runner |
|------|------------------------|----------------|
| `builder` | Implement or change project artifacts | `codex` |
| `tester` | Run tests and capture evidence | `claude` |
| `reviewer` | Review changes against OKF requirements | `cursor` |
| `integrator` | Merge outcomes, update OKF, finalize handoff | `codex` |

Override at pipeline start:

```bash
scripts/okf-dispatch init-pipeline "Task summary" \
  --runners builder:codex,tester:claude,reviewer:cursor,integrator:claude
```

**Perplexity is not a dispatch runner.** It does not consume JSON from `.okf/dispatch/`. On quota failure, use `scripts/okf-dispatch overflow` plus Perplexity MODE B; Cursor or Codex integrates output and completes or fails the packet manually.

Supported dispatch runners: `codex`, `claude`, `cursor`, `xcode-claude`.

---

## Perplexity Modes and Terminology

### Spaces vs Projects

OKF documents **Perplexity Spaces** (custom instructions, attached files, threads, collaboration) as the verified research surface per Perplexity help-center docs. There is no separate formal “Desktop Pro Projects” API documented beyond Spaces and file-upload behavior.

**Perplexity Computer skills** (uploadable `SKILL.md`) are adjacent but **out of scope** for automated OKF dispatch runners unless explicitly added later.

### MODE A vs MODE B

| Mode | When to use | Output | Who applies |
|------|-------------|--------|-------------|
| **MODE A — RESEARCH** | After steps 1–4; planned external evidence; domain/vendor/compliance/risk research | Draft `Reference` concepts | Cursor/Codex → `.okf/references/` |
| **MODE B — OVERFLOW** | Primary runner blocked (`usage_limit`, `outage`, `policy`, `user_choice`) | Same OKF role deliverable as blocked runner | Cursor/Codex applies; resume primary when available |

**Do not use MODE A** for mid-pipeline implementation when a dispatch runner is available.

**Do not use MODE B** for planned research or when the primary runner can continue.

Workflows: `.okf/workflows/perplexity-research-cycle.md`, `.okf/workflows/perplexity-overflow-failover.md`.

---

## Skills: Platform Consumption Model

| Platform | How skills are consumed | Location |
|----------|-------------------------|----------|
| **Codex** | Install/copy skill folders from `skills/` per `CODEX-SKILL-INSTALL.md`; progressive disclosure from `name` + `description` | Codex home / project |
| **Claude Code** | Reads `CLAUDE.md`; follows canonical skills via adapter pointers and slash commands | Repo |
| **Cursor** | Global skills unchanged; project overlay `.cursor/rules/okf.mdc` references canonical skills | Repo |
| **Perplexity** | Attach `skills/perplexity-okf-*/SKILL.md` in Project Skills settings (minimum `name`, `description`) | Perplexity Space |
| **Xcode** | Agent rule `.okf/agents/xcode-claude.md`; dispatch packet consumer | Repo |

Do not assume all platforms parse OKF extended frontmatter (`okf_mode`, `canonical_skill`) natively — those keys document OKF contracts.

---

## Day-to-Day Workflow Per Service

### Cursor

Use `.cursor/rules/okf.mdc` as the local OKF overlay. Keep global Cursor skills active. Read `.okf/index.md`, `.okf/project.md`, and recent handoffs before substantive work.

### Codex

Use `AGENTS.md`. Install OKF skills as needed, run builder tasks, maintain hooks, update OKF, validate before handoff.

### Claude Code

Use `CLAUDE.md`. Follow canonical skills through adapter pointers. Use `.claude/commands/okf-sync.md` after skill changes.

### Xcode

Use `.okf/agents/xcode-claude.md` for Apple-platform dispatch, build/test evidence, signing/simulator constraints. Hand off to Perplexity service 5 when research is next.

**Step 4 dry verification (no Xcode required):** `.okf/prompts/xcode-step4-verification-checklist.md` — evidence template `.okf/tests/2026-06-28-xcode-step4-dry-verification.md`. Live verification pending: `.okf/risks/xcode-live-verification-pending.md`.

### Perplexity

Use `PERPLEXITY.md`. MODE A creates cited draft References. MODE B produces overflow deliverables for Cursor/Codex to apply.

---

## Commands Cheat Sheet

```bash
scripts/okf-validate --strict
scripts/okf-migrate --check
scripts/okf-index --check
scripts/okf-index --write
scripts/okf-freshness --check
scripts/okf-visualize --format html --output /tmp/okf-graph.html
scripts/okf-sync-skills
scripts/okf-check-adapters
scripts/okf-dispatch status --verbose
scripts/okf-dispatch init-pipeline "Task summary"
scripts/okf-dispatch overflow --packet-id <id> --reason usage_limit --primary-runner codex
scripts/okf-attest-experiment run
scripts/openwiki-sidecar status
scripts/okf-context-pack
scripts/okf-handoff <task-slug> --summary "..."
python3 skills/create-new-okf-project/scripts/create_okf_project.py /path/to/project \
  --name "My Project" --owner team
# Optional sidecar:
python3 skills/create-new-okf-project/scripts/create_okf_project.py /path/to/project \
  --name "My Project" --owner team --with-openwiki
```

Use `--overwrite` on the scaffold script only when replacing an existing OKF scaffold intentionally.

---

## Research References in This Repo

The 2026-06-27 **Perplexity shared-services research pack** is ingested under `.okf/references/` as **draft, unverified** material.

**Dual role (do not collapse):**

| Location | Role |
|----------|------|
| `docs/okf-ways-of-working-brief.md` | Operator summary — what to do now |
| `.okf/references/*.md` | Citation source — URLs, claims, limitations, external evidence |

References are **not obsolete** when docs exist; they remain the traceability layer until promoted or superseded. Do not treat references as accepted requirements.

| Reference | Topic |
|-----------|--------|
| `shared-agent-memory-handoffs.md` | AGENTS.md / file-based handoffs |
| `claude-project-instructions.md` | CLAUDE.md |
| `codex-skills-disclosure.md` | Codex progressive disclosure |
| `perplexity-spaces-dev-workflow.md` | Perplexity Spaces |
| `perplexity-file-limits.md` | Attachment limits |
| `perplexity-skills-format.md` | Computer skills format |
| `cross-platform-skill-adapters.md` | Adapter pattern |
| `claude-agents-layering.md` | Instruction layering |
| `overflow-handoff-quota-failover.md` | Overflow handoffs |
| `agent-ready-bootstrap-scaffolds.md` | Scaffold patterns |
| `multi-agent-risks.md` | Configuration risks |

Also present: `source-requirements-summary.md` (project-specific).

`integration-protocol-boundaries.md` is a separate **stable, reviewed** primary-source record for the MCP and OpenWiki contracts used by the optional pilots. Its short freshness deadline reflects active upstream protocols; review it rather than silently extending trust.

Lessons accepted from this research: `.okf/improvements/2026-06-27-perplexity-research-lessons.md`.

---

## New Project Scaffold

When run from the bootstrap kit, the scaffold script creates an OKF-enabled project with the five-service operating model:

```bash
python3 skills/create-new-okf-project/scripts/create_okf_project.py /path/to/project \
  --name "My Project" --owner team
```

**Expect approximately 367 files with the OpenWiki overlay enabled** in the canonical default scaffold, including the five-service OKF material, copied template source, generated directory indexes, integration pilots, and project-local skills. Validate required paths rather than treating the exact count as a contract.

- `.okf/` bundle (requirements, workflows, agents, prompts, handoffs, references, improvements, dispatch queues)
- Handoffs guide: `.okf/handoffs/README.md`, `TEMPLATE.md`, `TEMPLATE-tester.md`, `TEMPLATE-reviewer.md`, `TEMPLATE-xcode-step4.md`
- Context packs index: `.okf/context-packs/INDEX.md`
- Thin adapters: `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/okf.mdc`, `PERPLEXITY.md`
- Docs: `docs/shared-okf-skills.md`, `docs/configure-perplexity-okf.md`, Perplexity/Xcode setup guides (when copied from bootstrap)
- Scripts: `okf-validate`, `okf-migrate`, `okf-index`, `okf-freshness`, `okf-visualize`, `okf-sync-skills`, `okf-handoff`, `okf-context-pack`, `okf-dispatch`, `okf-check-adapters`, `okf-mcp-server`, `okf-attest-experiment`, `openwiki-sidecar`
- Bundled skills under `skills/` including four `perplexity-okf-*` skills

After scaffold: run `scripts/okf-migrate --check`, `scripts/okf-index --check`, `scripts/okf-freshness --check`, `scripts/okf-validate --strict`, and `scripts/okf-check-adapters`.

### Bootstrap kit path (important)

The scaffold script delegates to the canonical `scripts/launch_project.sh` when the bootstrap repository is discoverable. Use `--bootstrap-root` to select it explicitly. The launcher renders the canonical template tree, copies runtime assets and skills, generates adapters, and validates the result.

**Canonical scaffold includes:** operator brief, all five setup guides, configure-perplexity, dispatch orchestration, Perplexity files/skills guide, dispatch and validation scripts, handoff templates, context-pack index, post-curation smoke-test prompt, Codex hooks, disabled read-only MCP/attestation pilots, and OpenWiki sidecar tooling. `--with-openwiki` controls only the generated sidecar content overlay.

If you run an installed skill without the bootstrap repository, it announces and uses a smaller embedded fallback. The fallback still carries v0.2 migration/validation and five-service core material. Use the canonical repository for full Forge, operator-guide, and template parity.

Current evidence: `.okf/tests/2026-08-16-okf-v02-migration-scaffold.md`.

---

## What Not To Do

- Do not store secrets, credentials, private keys, or customer data in OKF.
- Do not treat Perplexity research or `.okf/references/` drafts as accepted truth before review.
- Do not let Perplexity write repo files or advance dispatch queues.
- Do not attach the whole repo to Perplexity; use curated Project Files.
- Do not hand-edit generated adapter skill indexes (regenerate with `scripts/okf-sync-skills`).
- Do not hand-edit content inside OKF generated index markers (regenerate with `scripts/okf-index --write`).
- Do not interpret an overdue `stale_after` date as permission to delete or silently rewrite a concept.
- Do not confuse handoffs with context packs.

---

## Open Follow-Ups

- Review Perplexity product behavior as Spaces/skills documentation evolves.
- Promote `.okf/agents/xcode-claude.md` from `draft` when **live** Xcode build/test is verified (dry verification alone is insufficient).
- Use `.okf/handoffs/README.md` and `.okf/context-packs/INDEX.md` as operator training material.

## Brief Maintenance (operators and Cursor/Codex)

Refresh this brief when `.okf/log.md` records a **material operating-model change** (new service, dispatch behavior, Perplexity workflow, validation rule, or scaffold output).

**Checklist after such a log entry:**

1. Update affected sections in `docs/okf-ways-of-working-brief.md`.
2. Update `generated.at` in this file's frontmatter.
3. Append one line to `.okf/log.md` noting the brief refresh.
4. Re-attach the brief in Perplexity Project Files if you use a Space for this repo.
5. Run `scripts/okf-validate --strict`.

If Perplexity or another agent proposes policy that already appears here, **read the brief first** — do not re-derive implemented rules from chat memory.

---

## Related Material

- Index: `.okf/index.md`
- Shared operating model: `docs/shared-okf-skills.md`
- Dispatch: `docs/okf-dispatch-orchestration.md`
- Perplexity: `docs/configure-perplexity-okf.md`, `docs/perplexity-project-files-and-skills.md`
- Improvement log: `.okf/improvements/2026-06-27-perplexity-research-lessons.md`
