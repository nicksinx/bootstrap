# Bootstrap Launcher Toolkit

Deterministic scaffolding for software projects that use **AI agents as first-class operators**. This repository is the reusable launcher: it generates a product repo with OKF project context, optional GitHub setup, MCP integration hooks, backlog contracts, and—when you need it—the **Forge lifecycle MCP portfolio** layered on top.

Validated patterns come from real integration work in the [Project-1 harness](https://github.com/nicksinx/Project-1) and are promoted here so every new product does not reinvent wiring, launchers, or operator docs.

---

## What you get

| Capability | Description |
|------------|-------------|
| **Deterministic scaffold** | Versioned templates, JSON schemas, and profile contracts—same inputs produce the same tree |
| **OKF bundle** | `.okf/` curated memory: requirements, decisions, workflows, handoffs, risks, improvements |
| **Forge lifecycle MCP** | Eleven Forge launchers, sibling-clone helper, auto-written `.cursor/mcp.json` |
| **OKF dispatch** | `scripts/okf-dispatch` multi-role delivery pipeline (Project-1 aligned) |
| **Agent adapters** | Thin `AGENTS.md`, `CLAUDE.md`, Cursor rules—pointing at OKF, not duplicating it |
| **Legacy ai-task path** | Deprecated `legacy-task` profile only—see [migration doc](docs/migration-from-legacy-bootstrap.md) |

Bootstrap **generates** product repositories. It does not run your application, vend Forge server code, or replace OKF as the source of curated project truth.

---

## How it works

```mermaid
flowchart TB
  subgraph bootstrap [Bootstrap repo]
    LP[launch_project.sh]
    PROF[profiles/*.yaml]
    TPL[templates/new-project]
    LEG[templates/legacy-task overlay]
  end

  subgraph product [Generated product repo]
    OKF[.okf/ curated memory]
    SCR[scripts/ okf-dispatch forge launchers]
    MCP[.cursor/mcp.json Forge]
    BL[backlog/ schemas/]
  end

  subgraph optional [Optional siblings — not vendored]
    FC[ConceptForge … SunsetForge]
    FLC[ForgeLifecycleContracts]
  end

  LP --> PROF
  PROF --> TPL
  PROF -->|legacy-task only| LEG
  TPL --> product
  LEG --> product
  MCP -->|stdio launchers| FC
  FC --> FLC
  OKF -->|one-way promotion| OKF
```

1. **Choose a profile** (`default` v2.0.0 recommended; `legacy-task` deprecated) — see [`profiles/`](profiles/).
2. **Run** [`scripts/launch_project.sh`](scripts/launch_project.sh) with `--name`, `--target-dir`, and flags.
3. **Render** templates from [`templates/new-project/`](templates/new-project/) (plus `legacy-task` overlay when applicable).
4. **Validate** with `make check` in bootstrap, then `scripts/validate_launch.sh` and `scripts/okf-validate` in the new project.
5. **Clone and build** Forge siblings, then reload Cursor MCP.

---

## Profiles (v2.0.0)

| Profile | Use when |
|---------|----------|
| **`default`** | New OKF + Forge + dispatch products (recommended) |
| **`forge-lifecycle`** | Deprecated alias for `default` v2 |
| **`legacy-task`** | Deprecated ai-task MCP + workers only—see [migration](docs/migration-from-legacy-bootstrap.md) |

---

## Legacy ai-task track (deprecated)

[v1.x](CHANGELOG.md) shipped optional [cursor-ai-task-mcp-server-updated](https://github.com/nicksinx/cursor-ai-task-mcp-server-updated) via `--with-mcp`. **v2 default does not.** Use profile `legacy-task` if you must keep that path temporarily. Project-1 and Forge integration never used ai-task.

---

## Prerequisites

- `bash`
- `python3` with `pyyaml` and `jsonschema`
- `git`
- **Optional:** `gh` for `--with-github`
- **Forge profile:** `node` ≥ 20 and built sibling Forge repos (see below)

---

## Quick start — default (OKF + Forge + dispatch)

```bash
git clone https://github.com/nicksinx/bootstrap.git
cd bootstrap
make check

./scripts/launch_project.sh \
  --name my-product \
  --profile default \
  --target-dir ./out/my-product \
  --non-interactive

cd ./out/my-product
scripts/forge-clone-siblings.sh   # optional — clone Forge peers
scripts/okf-validate
scripts/okf-dispatch status
```

Forge `.cursor/mcp.json` is written automatically. Build sibling Forge repos and reload Cursor MCP before calling Forge tools.

Sync OKF skills from the bootstrap kit when needed: `scripts/okf-sync-skills --dry-run` then `scripts/okf-sync-skills`.

---

## Quick start — legacy ai-task (deprecated)

```bash
./scripts/launch_project.sh \
  --name my-legacy \
  --profile legacy-task \
  --target-dir ./out/my-legacy \
  --with-mcp --with-mcp-config \
  --non-interactive
```

See [docs/migration-from-legacy-bootstrap.md](docs/migration-from-legacy-bootstrap.md).

---

## OKF augmentation

**Open Knowledge Format (OKF)** is the Git-native curated memory layer every scaffolded project shares.

| Concern | Where it lives |
|---------|----------------|
| Navigation | `.okf/index.md`, `.okf/project.md` |
| Requirements & features | `.okf/requirements/`, `.okf/features/` |
| Decisions & risks | `.okf/decisions/`, `.okf/risks/` |
| Agent continuity | `.okf/handoffs/` |
| Lessons learned | `.okf/improvements/` |
| Validation | `scripts/okf-validate`, `scripts/okf-handoff`, `scripts/okf-context-pack` |

**Reading order for any agent:** index → project → task-relevant concepts → recent handoffs → improvements.

OKF explains and links to code, tests, and backlog—it does not replace them. Material changes should append to `.okf/log.md` and trace to a requirement, decision, or handoff.

To extend OKF on a generated project:

1. Add concepts under `.okf/` using your agent’s OKF skill or `scripts/okf-handoff`.
2. Run `scripts/okf-validate` before and after substantive edits.
3. Promote lessons from `.okf/improvements/` back into **bootstrap templates** when they apply to *all* future projects (see [Continuous improvement](#continuous-improvement)).

---

## Forge MCP augmentation

The **Forge portfolio** (`nicksinx/*Forge`) provides one MCP server per lifecycle stage. Shared contracts live in [ForgeLifecycleContracts](https://github.com/nicksinx/ForgeLifecycleContracts). [ForgeRelay](https://github.com/nicksinx/ForgeRelay) handles cross-tool session continuity—orthogonal to OKF dispatch.

### Option C integration (default policy)

Scaffolded `forge-lifecycle` projects inherit **Option C**:

| Layer | Role |
|-------|------|
| **OKF** | Curated memory substrate—requirements, decisions, handoffs |
| **Forge MCP** | Lifecycle planning engine—typed workspaces, signed envelopes, stage gates |
| **Promotion** | One-way, integrator-reviewed: Forge workspace → `.okf/` concepts |
| **OKF dispatch** | Implementation delivery pipeline (when installed on the product) |
| **ForgeRelay** | Tool-switch / session resume—not a replacement for dispatch or governance |

Forge is **not** a sixth OKF bootstrap service. Enable it **after** the five-service OKF setup.

Decision record (generated): `.okf/decisions/0002-okf-forge-integration.md`.

### Sibling layout (no vendoring)

Forge repos clone as **peers** of the product project:

```text
parent/
├── my-product/          ← generated repo (this toolkit)
├── ConceptForge/
├── BuildForge/
├── LaunchForge/
├── …
└── ForgeLifecycleContracts/
```

Launchers in `scripts/*-mcp.sh` resolve `../<Repo>`, pin versions, set `FORGE_WORKSPACE` under `.okf/forge/<stage>/` (gitignored), and assert contracts alignment.

### Lifecycle spine (conceptual)

```text
ConceptForge → BuildForge → LaunchForge → OperateForge
                    ↓              ↓
              GovernanceForge   Customer / Growth / Revenue (parallel)
                    ↓
              InsightForge (learning, iteration)
                    ↓
              SunsetForge → GovernanceForge + InsightForge (retirement closure)
```

Packet routing and OKF ingest targets: `.okf/references/forge-packet-type-registry.md`.

### What bootstrap includes vs the full harness

| In bootstrap (`default` v2) | In [Project-1 harness](https://github.com/nicksinx/Project-1) |
|----------------------------------|------------------------------------------------------------------|
| MCP launchers, clone helper, slim integration doc | Full integration spec (`docs/okf-forge-integration-spec.md`) |
| Decision 0002, sibling layout, packet registry | Per-server agent guides (`.okf/agents/*forge*.md`) |
| Operator notes, promotion checklist **stub** | Full promotion checklists (`.okf/workflows/forge-*-checklist.md`) |
| Profile + smoke test | Vertical-slice evidence (`.okf/tests/*-evidence.md`) |

When you need promotion checklists, adversarial prompts, or E2E proof paths, link to or copy from Project-1—then promote stable patterns back into bootstrap templates.

Durable lessons from harness → bootstrap promotion: [`.okf/improvements/forge-lifecycle-bootstrap-lessons.md`](.okf/improvements/forge-lifecycle-bootstrap-lessons.md).

---

## Launch script reference

```bash
./scripts/launch_project.sh \
  --name <project-id> \
  --profile default|legacy-task|forge-lifecycle \
  --target-dir <path> \
  [--non-interactive] \
  [--dry-run] \
  [--force] \
  [--with-github]
```

Legacy profile only: `--with-mcp`, `--with-mcp-config`, and related ai-task flags.

| Flag | Purpose |
|------|---------|
| `--dry-run` | Print actions without writing |
| `--with-github` | Create remote via `gh` (optional) |
| `--with-mcp` | **legacy-task only** — register with ai-task MCP |
| `--with-mcp-config` | **legacy-task only** — write ai-task `.cursor/mcp.json` |

Full flag list: `./scripts/launch_project.sh --help`.

---

## Repository layout

| Path | Purpose |
|------|---------|
| [`scripts/`](scripts/) | `launch_project.sh`, validation, GitHub helpers |
| [`templates/new-project/`](templates/new-project/) | v2 scaffold (`.tmpl` Go templates) |
| [`templates/legacy-task/`](templates/legacy-task/) | Deprecated ai-task overlay |
| [`profiles/`](profiles/) | `default.yaml` v2, `legacy-task.yaml`, `forge-lifecycle.yaml` (alias) |
| [`schemas/`](schemas/) | JSON Schema contracts for backlog, handoffs, OKF concepts |
| [`skills/`](skills/) | Canonical OKF skill definitions (synced to generated projects) |
| [`tests/`](tests/) | Contract tests and launch smoke (including forge-lifecycle) |
| [`.okf/improvements/`](.okf/improvements/) | Bootstrap’s own lessons—source for template promotion |

---

## Development

```bash
make test-contracts    # JSON schema + profile contracts
make test-launch-smoke # End-to-end launch into temp dir
make test-intake       # project-intake CLI smoke
make check             # All of the above
```

### Cursor skill: bootstrap-okf-forge-project

Standardized operator intake for new OKF + Forge products:

```text
skills/bootstrap-okf-forge-project/SKILL.md
scripts/project-intake
```

In Cursor, invoke the skill when standing up a new product; it collects `project-intake.yaml`, validates, and runs launch + post-steps. See `skills/bootstrap-okf-forge-project/SKILL.md`.

Forge-lifecycle smoke: `tests/test_launch_smoke.py` validates profile render + `okf-validate` on output.

---

## Continuous improvement

1. **Product project** discovers a repeatable pattern → record in `.okf/improvements/`.
2. **Integration harness** (Project-1) proves it with tests and operator checklists.
3. **Bootstrap** absorbs stable, generic parts into `templates/` or `profiles/`.
4. **Forge repos** ship MCP behavior and contracts independently.

Do not copy harness-only material (full spec, adversarial dossiers, vertical-slice evidence) into bootstrap until it applies to every new product.

---

## Security notes

- Never commit Forge **signing keys**, approval receipts, or workspace PII.
- Forge runtime state belongs under `.okf/forge/` (gitignored).
- OKF promoted concepts are reviewed Markdown—not a secrets store.

Signing key layout: see Project-1 `.okf/references/forge-signing-keys-operator-runbook.md` when operating Forge in production.

---

## Related repositories

| Repository | Role |
|------------|------|
| [nicksinx/bootstrap](https://github.com/nicksinx/bootstrap) | This toolkit |
| [nicksinx/Project-1](https://github.com/nicksinx/Project-1) | OKF + Forge integration harness (full policy & evidence) |
| [nicksinx/ForgeLifecycleContracts](https://github.com/nicksinx/ForgeLifecycleContracts) | Shared envelopes, signing, compatibility boundaries |
| [nicksinx/ForgeRelay](https://github.com/nicksinx/ForgeRelay) | Cross-tool agent continuity (INT-001) |
| [nicksinx/ConceptForge](https://github.com/nicksinx/ConceptForge) … [SunsetForge](https://github.com/nicksinx/SunsetForge) | Lifecycle stage MCP servers (`forge-lifecycle` profile) |
| [cursor-ai-task-mcp-server-updated](https://github.com/nicksinx/cursor-ai-task-mcp-server-updated) | **Optional** task/backlog MCP for `default` profile only—not used by Project-1 or Forge |

---

## License & support

Bootstrap is an operator toolkit maintained for the `nicksinx` Forge + OKF ecosystem. For integration policy and phase status, treat [Project-1](https://github.com/nicksinx/Project-1) `docs/okf-forge-integration-spec.md` as the authoritative harness spec; treat this README as the entry point for **starting a new product** with the right profile and augmentation path.
