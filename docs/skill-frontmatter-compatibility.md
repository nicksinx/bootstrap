# OKF Skill Frontmatter Compatibility

Canonical OKF skills live under `skills/*/SKILL.md`. Platform adapters and Perplexity project skills use overlapping but not identical frontmatter.

## Universal keys (all platforms)

| Key | Required | Purpose |
|-----|----------|---------|
| `name` | Yes | Skill identifier (Codex, Perplexity Computer skills) |
| `description` | Yes | Selection / invocation summary |

## OKF canonical keys (`skills/okf-*`, `skills/perplexity-okf-*`)

| Key | Required | Purpose |
|-----|----------|---------|
| `applies_to` | Recommended | e.g. `[perplexity]`, `[codex, local-agent]` |
| `okf_mode` | Perplexity adapters | `[research]`, `[overflow]`, or both |
| `canonical_skill` | Perplexity adapters | Path to shared OKF skill, e.g. `skills/okf-reader/SKILL.md` |

Generic `okf-*` skills use minimal frontmatter (`name`, `description` only).

## Platform consumption

| Platform | How skills are consumed |
|----------|-------------------------|
| **Codex** | Directory under `skills/`; progressive disclosure from `name` + `description`; optional `agents/openai.yaml` |
| **Claude Code** | Reads `CLAUDE.md` + repo; no native SKILL.md loader — follow via adapter pointer |
| **Cursor** | Global skills + project `.cursor/rules/okf.mdc` overlay; canonical skills referenced, not duplicated |
| **Perplexity** | Project Skills: upload `SKILL.md` with at least `name` + `description`; attach `perplexity-okf-*` files |

## Adapter generation

Run `scripts/okf-sync-skills` after editing canonical skills to refresh:

- `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/okf.mdc`, `PERPLEXITY.md`

Do not hand-edit generated adapter skill index footers.

## Authoring rules

1. Edit workflow once in `skills/okf-*/SKILL.md` or `skills/perplexity-okf-*/SKILL.md`.
2. Perplexity adapter skills add constraints only (no repo access, MODE A/B, ingest boundary).
3. Point to `canonical_skill` instead of copying full `okf-*` bodies into `perplexity-okf-*`.
4. Do not assume all platforms parse `applies_to` or `okf_mode` — they are OKF documentation and selection hints.

## Related

- `.okf/references/cross-platform-skill-adapters.md`
- `.okf/references/codex-skills-disclosure.md`
- `.okf/references/perplexity-skills-format.md`
- `docs/shared-okf-skills.md`
