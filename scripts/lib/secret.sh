#!/usr/bin/env bash
# Secret-handling helpers. Centralised so the launcher never echoes raw tokens.

# shellcheck shell=bash

if [[ -n "${BOOTSTRAP_LIB_SECRET_LOADED:-}" ]]; then
  return 0
fi
BOOTSTRAP_LIB_SECRET_LOADED=1

# Retrieve a secret by logical name from one of the supported sources.
# Sources: env|keychain. Keychain is macOS-only (security CLI).
# Usage: bs_get_secret <name> <source>
bs_get_secret() {
  local name="$1"
  local source="${2:-env}"
  case "$source" in
    env)
      printf '%s' "${!name:-}"
      ;;
    keychain)
      if ! command -v security >/dev/null 2>&1; then
        return 1
      fi
      security find-generic-password -a "${USER}" -s "$name" -w 2>/dev/null
      ;;
    *)
      return 2
      ;;
  esac
}

# Indicate whether a secret is present without revealing it.
bs_secret_present() {
  local name="$1"
  local source="${2:-env}"
  local val
  val=$(bs_get_secret "$name" "$source" || true)
  if [[ -n "$val" ]]; then
    return 0
  fi
  return 1
}

# Reject any operation that would persist a secret to a generated file.
# Usage: bs_assert_no_secret_in_file <path>
bs_assert_no_secret_in_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    return 0
  fi
  if grep -E -q '(ghp_|gho_|github_pat_)[A-Za-z0-9_]{16,}' "$path"; then
    return 1
  fi
}
