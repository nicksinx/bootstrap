#!/usr/bin/env bash
# Common utilities used by the launcher and supporting scripts.

# shellcheck shell=bash

if [[ -n "${BOOTSTRAP_LIB_UTIL_LOADED:-}" ]]; then
  return 0
fi
BOOTSTRAP_LIB_UTIL_LOADED=1

bs_iso_timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

bs_sha256_file() {
  local path="$1"
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$path" | awk '{print $1}'
  else
    sha256sum "$path" | awk '{print $1}'
  fi
}

# Validate that a project_id matches schemas/project.schema.json pattern.
bs_validate_project_id() {
  local id="$1"
  if [[ ! "$id" =~ ^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$ ]]; then
    return 1
  fi
  return 0
}

# Validate semver "X.Y.Z".
bs_validate_semver() {
  local v="$1"
  if [[ ! "$v" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    return 1
  fi
  return 0
}

bs_require_command() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    return 1
  fi
}

# Stable PATH sanitiser: rejects path traversal and absolute paths.
bs_safe_relpath() {
  local p="$1"
  if [[ "$p" == /* ]]; then
    return 1
  fi
  if [[ "$p" == *".."* ]]; then
    return 1
  fi
  printf '%s' "$p"
}
