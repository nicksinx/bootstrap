#!/usr/bin/env bash
# Structured error emission and stable exit codes.

# shellcheck shell=bash

if [[ -n "${BOOTSTRAP_LIB_ERROR_LOADED:-}" ]]; then
  return 0
fi
BOOTSTRAP_LIB_ERROR_LOADED=1

# Stable exit codes (also documented in error_catalog.json).
readonly BS_EXIT_OK=0
readonly BS_EXIT_INPUT=2
readonly BS_EXIT_DEPENDENCY=3
readonly BS_EXIT_GITHUB=4
readonly BS_EXIT_SCAFFOLD=5
readonly BS_EXIT_MCP_REGISTER=6
readonly BS_EXIT_MCP_CONFIG=7
readonly BS_EXIT_MCP_SCHEDULE=8
readonly BS_EXIT_VALIDATION=9
readonly BS_EXIT_UNSAFE=10

bs_correlation_id() {
  if [[ -n "${BOOTSTRAP_CORRELATION_ID:-}" ]]; then
    printf '%s' "${BOOTSTRAP_CORRELATION_ID}"
    return 0
  fi
  if command -v uuidgen >/dev/null 2>&1; then
    uuidgen | tr '[:upper:]' '[:lower:]'
  else
    od -An -N16 -tx1 /dev/urandom | tr -d ' \n'
  fi
}

# Emit a single JSON line conforming to schemas/error.schema.json on stderr.
# Usage: bs_emit_error CODE EXIT_CODE MESSAGE [HINT] [DOC_URL]
bs_emit_error() {
  local code="$1"
  local exit_code="$2"
  local message="$3"
  local hint="${4:-}"
  local doc_url="${5:-}"
  local cid
  cid="${BOOTSTRAP_CORRELATION_ID:-$(bs_correlation_id)}"
  python3 - "$code" "$exit_code" "$message" "$hint" "$doc_url" "$cid" <<'PY' >&2
import json, sys
code, exit_code, message, hint, doc_url, cid = sys.argv[1:7]
out = {"code": code, "exit_code": int(exit_code), "message": message, "correlation_id": cid}
if hint:
    out["hint"] = hint
if doc_url:
    out["doc_url"] = doc_url
print(json.dumps(out, sort_keys=True))
PY
}

# Emit a structured error and exit with the matching exit code.
bs_die() {
  local code="$1"
  local exit_code="$2"
  local message="$3"
  local hint="${4:-}"
  local doc_url="${5:-docs/errors.md}"
  bs_emit_error "$code" "$exit_code" "$message" "$hint" "$doc_url"
  exit "$exit_code"
}
