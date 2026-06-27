---
type: Reference
title: Codex Prompt — Update GitHub OKF Bootstrap Repo
description: Copy-paste prompt for Codex to commit and push the current branch of the OKF Project Bootstrap GitHub repository with all 2026-06-28 refinement changes.
status: active
lifecycle_stage: operate
owner: project
source_of_truth: true
resource: .okf/prompts/codex-update-github-bootstrap-repo.md
tags: [okf, prompt, codex, github, bootstrap, publish]
applies_to: [codex, cursor, local-agent]
sensitivity: internal
verification_status: reviewed
timestamp: 2026-06-28T23:30:00+02:00
---

# Purpose

Use when the **OKF Project Bootstrap** GitHub repository is open locally and Codex should **publish the current branch** with all bootstrap refinement work (Perplexity integration, Waves 1–3, dispatch ergonomics).

If the GitHub clone is stale, sync from the canonical working tree first (see below).

# Prompt (copy below)

```markdown
You are working in the **OKF Project Bootstrap** GitHub repository (Project-1 / OKF bootstrap kit).

**Goal:** Update the GitHub remote with **all latest changes on the current branch** — commit, push, and report status. Do not rewrite history or force-push.

## 0. Locate repo and branch

1. Confirm you are in the git repository root (`git rev-parse --show-toplevel`).
2. Record:
   - `git branch --show-current`
   - `git remote -v`
   - `git status`
3. If the user provided a canonical source tree, sync missing files before commit:
   - **Canonical source (if needed):** `/Users/dv/Projects/testrunner/Project-1`
   - Compare with `rsync -avn` or diff key paths; copy only if the GitHub clone is behind.
4. Do **not** push to `main`/`master` without explicit user confirmation unless the user said the current branch **is** the release branch.

## 1. Read first (operating context)

1. `.okf/index.md`
2. `.okf/log.md` — all entries from **2026-06-27** and **2026-06-28**
3. `docs/okf-ways-of-working-brief.md`
4. Latest handoff: `.okf/handoffs/2026-06-28-dispatch-ergonomics.md`

## 2. Pre-push artifact checklist

Confirm these exist (add if missing from canonical source):

### Core operating model
- [ ] `docs/okf-ways-of-working-brief.md`
- [ ] `docs/shared-okf-skills.md`
- [ ] `docs/okf-dispatch-orchestration.md` (§ Role handoff expectations)
- [ ] Five setup guides: `docs/create-new-okf-project-in-{cursor,codex,claude,xcode,perplexity}.md`
- [ ] `docs/configure-perplexity-okf.md`, `docs/perplexity-project-files-and-skills.md`

### Perplexity (service 5 + overflow)
- [ ] `PERPLEXITY.md`, four `skills/perplexity-okf-*/SKILL.md`
- [ ] `.okf/agents/perplexity.md`, `.okf/agents/perplexity-overflow.md`
- [ ] `.okf/prompts/perplexity-{custom-instructions,deep-research-setup,overflow-failover,post-curation-smoke-test}.md`
- [ ] `.okf/prompts/perplexity-procurelex-research.md` (application prompt — include but not required for bootstrap operators)

### Xcode step 4 (dry — live verification still pending)
- [ ] `docs/create-new-okf-project-in-xcode.md` (expanded)
- [ ] `.okf/prompts/xcode-step4-verification-checklist.md`
- [ ] `.okf/agents/xcode-claude.md` (`status: draft`, `verification_status: unverified`)
- [ ] `.okf/risks/xcode-live-verification-pending.md`
- [ ] `.okf/tests/2026-06-28-xcode-step4-dry-verification.md`

### Scaffold (Wave 1)
- [ ] `skills/create-new-okf-project/scripts/create_okf_project.py` — `BOOTSTRAP_COPY_PATHS`, `overwrite=True` on bootstrap copies
- [ ] `.okf/tests/2026-06-28-scaffold-parity.md`

### Dispatch ergonomics (Wave 2)
- [ ] `.okf/handoffs/TEMPLATE-tester.md`, `TEMPLATE-reviewer.md`, `TEMPLATE-xcode-step4.md`
- [ ] `.okf/handoffs/README.md` (template selection table)
- [ ] `.okf/tests/2026-06-28-dispatch-dry-run.md`
- [ ] `.okf/improvements/2026-06-28-dispatch-ergonomics-lessons.md`

### Scripts
- [ ] `scripts/okf-validate`, `okf-sync-skills`, `okf-handoff`, `okf-context-pack`
- [ ] `scripts/okf-dispatch`, `scripts/okf-check-adapters`

### Claude step 3 alignment
- [ ] `docs/create-new-okf-project-in-claude.md` (five-service model)

## 3. Validate before commit

Run from repo root:

```bash
python3 -m py_compile skills/create-new-okf-project/scripts/create_okf_project.py
scripts/okf-validate
scripts/okf-check-adapters
scripts/okf-sync-skills --dry-run
```

Optional scaffold smoke (if time permits):

```bash
python3 skills/create-new-okf-project/scripts/create_okf_project.py /tmp/okf-github-push-smoke --name "GitHub Push Smoke" --owner codex
cd /tmp/okf-github-push-smoke && scripts/okf-validate && scripts/okf-check-adapters
```

Fix blocking validation failures before commit. Record results in commit body or a short note to append `.okf/log.md`.

## 4. Commit

Stage all intentional changes. **Do not commit:** secrets, `.env`, credentials, `/tmp/` smoke artifacts, dispatch test queue junk.

Draft commit message (adjust to match actual diff):

```
Publish OKF bootstrap refinement: Perplexity, Waves 1–3, dispatch ergonomics

- Five-service operating model with operator brief and Perplexity Space docs
- Scaffold parity (BOOTSTRAP_COPY_PATHS, full-kit vs sparse evidence)
- Xcode step 4 dry verification (agent rule remains draft until live Xcode)
- Dispatch role templates (tester/reviewer) and live pipeline dry-run evidence
- Claude step-3 guide aligned to five-service model

Validation: okf-validate 0 warnings; okf-check-adapters pass (13 skills).
```

Use one commit or logical split commits if the diff is very large — prefer **one cohesive commit** on the current feature branch unless the user asked for split history.

## 5. Push to GitHub

```bash
git push -u origin HEAD
```

If the branch has no upstream, set `-u`. **Never** `git push --force` to shared branches.

If push is rejected (non-fast-forward), pull/rebase from remote on the **same branch** and resolve conflicts — do not force-push unless the user explicitly requests it.

## 6. Pull request (if not pushing directly to default branch)

If the current branch is not `main`/`master`:

```bash
gh pr create --title "OKF bootstrap refinement — Perplexity, Waves 1–3, dispatch ergonomics" --body "$(cat <<'EOF'
## Summary
- Five-service OKF operating model (Cursor → Codex → Claude → Xcode → Perplexity + overflow)
- Operator brief, Perplexity integration, scaffold parity, Xcode step 4 dry verification
- Dispatch role handoff templates and live dry-run evidence

## Validation
- [ ] `scripts/okf-validate` — 0 warnings
- [ ] `scripts/okf-check-adapters` — pass
- [ ] Optional: full-kit scaffold smoke

## Not in this PR
- Live Xcode verification (agent rule still draft)
- ProcureLex application Perplexity Space

## Test plan
- [ ] Clone fresh from branch; run `scripts/okf-validate`
- [ ] Run scaffold from kit path; confirm ~74 files full / ~35 sparse
- [ ] Review `docs/okf-ways-of-working-brief.md`

EOF
)"
```

If `gh` is unavailable, report that a PR must be opened manually and provide the compare URL.

## 7. Report back

Return:

1. Branch name and remote URL
2. Commit SHA(s)
3. Push result (success / blocked)
4. PR URL if created
5. Validation command output summary
6. Any files that were synced from canonical source vs already in clone
7. Explicit note: `.okf/agents/xcode-claude.md` remains **draft** until live Xcode verification

## Rules

- Do not modify global Cursor skills or user-global Codex settings.
- Do not invent functionality outside the OKF bundle.
- Do not store secrets in OKF or commit them.
- Append one line to `.okf/log.md` noting GitHub publish date and branch — include in the same commit if log changed.
- Do not push unless this prompt explicitly authorizes publish (it does).
```

# After Codex completes

- Verify the remote branch on GitHub matches local validation baseline.
- Re-clone or pull downstream project repos that depend on the bootstrap kit.
