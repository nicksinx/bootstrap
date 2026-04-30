#!/usr/bin/env bash
# Logging helpers. Source-only; do not execute directly.

# shellcheck shell=bash

if [[ -n "${BOOTSTRAP_LIB_LOG_LOADED:-}" ]]; then
  return 0
fi
BOOTSTRAP_LIB_LOG_LOADED=1

: "${BOOTSTRAP_VERBOSE:=0}"
: "${BOOTSTRAP_QUIET:=0}"
: "${BOOTSTRAP_LOG_FORMAT:=plain}"

bs_log_emit() {
  local level="$1"
  shift
  local message="$*"
  if [[ "${BOOTSTRAP_LOG_FORMAT}" == "jsonl" ]]; then
    python3 - "$level" "$message" "${BOOTSTRAP_CORRELATION_ID:-}" <<'PY' >&2
import json, sys, datetime
level, message, cid = sys.argv[1:4]
out = {
  "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
  "level": level,
  "message": message,
}
if cid:
  out["correlation_id"] = cid
print(json.dumps(out, sort_keys=True))
PY
  else
    printf '[%s] %s\n' "$level" "$message" >&2
  fi
}

bs_log_info() {
  if [[ "${BOOTSTRAP_QUIET}" == "1" ]]; then
    return 0
  fi
  bs_log_emit info "$*"
}

bs_log_warn() {
  bs_log_emit warn "$*"
}

bs_log_error() {
  bs_log_emit error "$*"
}

bs_log_debug() {
  if [[ "${BOOTSTRAP_VERBOSE}" == "1" ]]; then
    bs_log_emit debug "$*"
  fi
}

bs_redact() {
  # Redact obvious secret-shaped tokens (~16+ char base64-ish runs and bearer tokens).
  sed -E \
    -e 's/(Bearer )[A-Za-z0-9._-]{8,}/\1[REDACTED]/g' \
    -e 's/(token|key|secret|password)([= :])([^[:space:]]+)/\1\2[REDACTED]/Ig' \
    -e 's/(ghp_|gho_|github_pat_)[A-Za-z0-9_]{16,}/[REDACTED-GH-PAT]/g'
}
