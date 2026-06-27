# Perplexity OKF Adapter

Perplexity Desktop Pro participates in this OKF project in two modes:

| Mode | Purpose |
|------|---------|
| **MODE A - RESEARCH** | Service 5 deep research that drafts cited OKF `Reference` concepts |
| **MODE B - OVERFLOW** | Ad hoc substitute for blocked Cursor, Codex, Claude Code, or Xcode runners |

## Configure Perplexity Desktop

1. Open **Perplexity Desktop -> Settings -> Custom instructions**.
2. Paste `.okf/prompts/perplexity-custom-instructions.md`.
3. Attach a curated project-file pack, not the whole repo.
4. Attach the four Perplexity project skills from `skills/perplexity-okf-*/SKILL.md`.

Perplexity never writes this repository directly, executes hooks, or advances dispatch queues. Cursor or Codex ingests outputs, updates OKF, and runs `scripts/okf-validate`.

## MODE A - RESEARCH

- Use after Cursor, Codex, Claude Code, and Xcode setup.
- Follow `docs/create-new-okf-project-in-perplexity.md`.
- Draft references under `.okf/references/` with `verification_status: unverified` and `source_of_truth: false`.

## MODE B - OVERFLOW

- Use only when a primary runner is blocked by usage limits, outage, policy, or explicit user choice.
- Follow `.okf/workflows/perplexity-overflow-failover.md` and `.okf/prompts/perplexity-overflow-failover.md`.
- Complete the same OKF role contract, then hand output back for Cursor/Codex integration.
