#!/usr/bin/env bash
# Idempotent file scaffolding with template substitution and protected sections.

# shellcheck shell=bash

if [[ -n "${BOOTSTRAP_LIB_SCAFFOLD_LOADED:-}" ]]; then
  return 0
fi
BOOTSTRAP_LIB_SCAFFOLD_LOADED=1

# Write a templated file at <dest> from <src>, replacing __VAR__ placeholders.
# Idempotent semantics:
#   - If <dest> does not exist: write rendered content.
#   - If <dest> exists and contains protected markers, preserve protected blocks.
#   - If <dest> exists and FORCE=1, overwrite while still preserving protected blocks.
#   - Otherwise leave <dest> untouched.
#
# Usage: bs_render_file <src> <dest>
bs_render_file() {
  local src="$1"
  local dest="$2"
  local force="${BOOTSTRAP_FORCE:-0}"
  local dry_run="${BOOTSTRAP_DRY_RUN:-0}"

  if [[ ! -f "$src" ]]; then
    return 1
  fi

  mkdir -p "$(dirname "$dest")"

  local rendered
  rendered=$(BOOTSTRAP_TEMPLATE_INPUT="$src" python3 "${BOOTSTRAP_LIB_DIR}/render_template.py")

  if [[ "$dry_run" == "1" ]]; then
    printf '[dry-run] would write %s\n' "$dest" >&2
    return 0
  fi

  if [[ -e "$dest" ]] && [[ "$force" != "1" ]]; then
    if [[ "$(cat "$dest")" == "$rendered" ]]; then
      return 0
    fi
    if grep -q 'BOOTSTRAP-PROTECTED-BEGIN' "$dest" 2>/dev/null; then
      rendered=$(BOOTSTRAP_EXISTING="$dest" BOOTSTRAP_RENDERED_CONTENT="$rendered" \
        python3 "${BOOTSTRAP_LIB_DIR}/preserve_protected.py")
      printf '%s\n' "$rendered" > "$dest"
      return 0
    fi
    return 0
  fi

  if [[ -e "$dest" ]] && [[ "$force" == "1" ]] && grep -q 'BOOTSTRAP-PROTECTED-BEGIN' "$dest" 2>/dev/null; then
    rendered=$(BOOTSTRAP_EXISTING="$dest" BOOTSTRAP_RENDERED_CONTENT="$rendered" \
      python3 "${BOOTSTRAP_LIB_DIR}/preserve_protected.py")
  fi

  printf '%s\n' "$rendered" > "$dest"
}

# Acquire a launch lock to prevent concurrent runs in the same project.
# Usage: bs_lock_acquire <path>
bs_lock_acquire() {
  local lock_file="$1"
  if [[ -e "$lock_file" ]]; then
    local pid
    pid=$(cat "$lock_file" 2>/dev/null || echo "")
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      return 1
    fi
  fi
  printf '%s\n' "$$" > "$lock_file"
}

bs_lock_release() {
  local lock_file="$1"
  if [[ -e "$lock_file" ]]; then
    rm -f "$lock_file"
  fi
}
