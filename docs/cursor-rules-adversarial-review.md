# Adversarial review: OKF + Forge Cursor rules pack

**Reviewer stance:** Attack the proposed rule pack as if deploying to dozens of product repos with mixed maturity (v1 ai-task, v2 Forge, harness-only).

**Verdict:** **ACCEPT WITH CONDITIONS** — ship a reduced pack; reject several scope choices from the initial recommendation.

---

## 1. Scope confirmation

| Proposed rule | Original intent |
|---------------|-----------------|
| Expanded `okf.mdc` + routing | Layer selection (OKF / Forge / dispatch / relay) |
| `no-legacy-aitask.mdc` | Block ai-task MCP on v2 scaffolds |
| `forge-mcp-operator.mdc` | Launcher + workspace boundaries |
| `okf-dispatch.mdc` | File-queue delivery semantics |
| `forge-promotion.mdc` | Option C promotion + receipts |
| `forgerelay-coexistence.mdc` | Decision 0003 boundary |
| `bootstrap-toolkit.mdc` | Bootstrap repo only |
| `integration-harness.mdc` | Project-1 only |

---

## 2. Boundary attacks

### Attack A — Context bloat from multiple `alwaysApply` rules

**Finding:** Three or more always-on rules duplicate OKF reading order, Perplexity notes, and routing tables. Cursor injects all of them every turn → token waste and contradictory emphasis.

**Severity:** Medium  
**Mitigation:** At most **two** always-on rules: `okf.mdc` (context + skills, sync-managed) and `okf-ecosystem-routing.mdc` (short routing table only). Everything else uses `globs`.

### Attack B — `no-legacy-aitask` as alwaysApply

**Finding:** Fires on harness repos, migration branches, and `legacy-task` profile products where ai-task is intentional. Agents may refuse valid work.

**Severity:** High  
**Mitigation:** **REJECT alwaysApply.** Use globs `scripts/mcp/**`, `scripts/workers/**` so the rule activates only when touching legacy paths. Wording: "if present, deprecated — prefer dispatch."

### Attack C — `forge-promotion` globs on `.okf/decisions/**`

**Finding:** Every decision edit triggers promotion/receipt guidance, including non-Forge decisions (0001 OKF substrate).

**Severity:** Medium  
**Mitigation:** Narrow to `.okf/workflows/forge-*.md` and `.okf/decisions/0002*.md`, `0004*.md` only.

### Attack D — `okf-sync-skills` overwrites `okf.mdc`

**Finding:** Embedding routing tables inside sync-generated `okf.mdc` causes drift or loss on every `okf-sync-skills` run.

**Severity:** High  
**Mitigation:** Keep routing in **static** `.mdc` files. `okf-sync-skills` may add a pointer paragraph only (implemented in adapter template).

### Attack E — Rules do not enforce behavior

**Finding:** Agents can ignore rules; MCP calls are not gated by `.mdc` files.

**Severity:** Accepted limitation  
**Mitigation:** Pair rules with `scripts/validate_launch.sh`, `scripts/okf-validate`, `scripts/okf-check-forge-receipts`. Rules are **fast guardrails**, not policy enforcement.

### Attack F — Glob rules inactive during “drive-by” tasks

**Finding:** Agent edits `src/foo.ts` without open Forge files → scoped rules never load → layer confusion persists.

**Severity:** Medium  
**Mitigation:** `okf-ecosystem-routing.mdc` alwaysApply carries the trigger table. Scoped rules add operator detail when relevant files are touched.

### Attack G — Shipping harness/bootstrap rules into products

**Finding:** `bootstrap-toolkit.mdc` in a product repo tells agents not to implement features.

**Severity:** High  
**Mitigation:** **Exclude** from `profiles/default.yaml`. Install manually in bootstrap and Project-1 only.

### Attack H — Duplicate ForgeRelay rule

**Finding:** `forgerelay-coexistence.mdc` overlaps routing table and decision 0003 already in bridge workflow.

**Severity:** Low  
**Mitigation:** **MERGE** relay boundary into `okf-ecosystem-routing.mdc`; drop standalone relay rule.

---

## 3. Wording attacks

| Phrase risk | Issue | Fix |
|-------------|-------|-----|
| "Never use Forge for implementation" | Too absolute; Forge may emit build tasks | "Lifecycle **planning** stages use Forge; **code delivery** uses dispatch" |
| "Auto-promote forbidden" | Unclear what "auto" means | "Do not set `verification_status: accepted` without integrator review and receipt checks per 0004" |
| "cursor-ai-task-mcp-server" by name | Repo may rename server | "legacy ai-task MCP wrappers under `scripts/mcp/`" |

---

## 4. Final accepted pack

| Rule | alwaysApply | globs | Ships in default profile |
|------|-------------|-------|--------------------------|
| `okf.mdc` | yes | — | yes (sync-managed) |
| `okf-ecosystem-routing.mdc` | yes | — | yes |
| `okf-legacy-aitask.mdc` | no | `scripts/mcp/**`, `scripts/workers/**` | yes |
| `okf-forge-operator.mdc` | no | `scripts/*forge*.sh`, `.okf/forge/**`, `.cursor/mcp*.json` | yes |
| `okf-dispatch.mdc` | no | `.okf/dispatch/**`, `scripts/okf-dispatch*` | yes |
| `okf-forge-promotion.mdc` | no | `.okf/workflows/forge-*.md`, `.okf/decisions/0002*.md`, `.okf/decisions/0004*.md` | yes |
| `bootstrap-toolkit.mdc` | yes | — | **no** (bootstrap repo only) |
| `integration-harness.mdc` | yes | — | **no** (Project-1 only) |

Forge server repos: defer minimal rules to a separate follow-up.

---

## 5. Conditions of acceptance

1. Document install path in `docs/install-cursor-rules.md`.
2. Add rule paths to `profiles/default.yaml` and `validate_launch.sh`.
3. Copy canonical rules to `templates/tool-adapters` and `templates/new-project`.
4. Install in Project-1 and bootstrap repo roots.
5. Do not regenerate static rules from `okf-sync-skills`.

---

## Related

- Initial recommendation (chat, 2026-07-04)
- `.okf/decisions/0002-okf-forge-integration.md` (Project-1)
- `.okf/decisions/0003-forgerelay-dispatch-coexistence.md` (Project-1)
- `.okf/decisions/0004-approval-receipt-verification.md` (Project-1)
