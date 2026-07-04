#!/usr/bin/env bash
# Cursor MCP launcher for ForgeRelay. Resolves paths without ${env:FORGERELAY_ROOT} in mcp.json.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FORGERELAY_ROOT="${FORGERELAY_ROOT:-$PROJECT_ROOT/../ForgeRelay}"
ENTRY="$FORGERELAY_ROOT/dist/index.js"
REQUIRED_VERSION="${FORGERELAY_MIN_VERSION:-0.1.2}"

export FORGERELAY_WORKSPACE="${FORGERELAY_WORKSPACE:-$PROJECT_ROOT/.okf/forge/relay}"
export FORGERELAY_PROJECT_ROOT="${FORGERELAY_PROJECT_ROOT:-$PROJECT_ROOT}"
mkdir -p "$FORGERELAY_WORKSPACE"

if [[ ! -f "$ENTRY" ]]; then
  echo "[forgerelay-mcp] missing $ENTRY — run: cd $FORGERELAY_ROOT && git checkout v$REQUIRED_VERSION && npm ci && npm run build" >&2
  exit 1
fi

if [[ ! -f "$FORGERELAY_ROOT/package.json" ]]; then
  echo "[forgerelay-mcp] missing $FORGERELAY_ROOT/package.json" >&2
  exit 1
fi

PKG_VERSION="$(node -p "require('$FORGERELAY_ROOT/package.json').version" 2>/dev/null || echo '')"
if [[ -z "$PKG_VERSION" ]]; then
  echo "[forgerelay-mcp] cannot read package version from $FORGERELAY_ROOT/package.json" >&2
  exit 1
fi

if [[ "$PKG_VERSION" != "$REQUIRED_VERSION" ]]; then
  echo "[forgerelay-mcp] ForgeRelay version $PKG_VERSION != required v$REQUIRED_VERSION" >&2
  echo "[forgerelay-mcp] fix: cd $FORGERELAY_ROOT && git fetch --tags && git checkout v$REQUIRED_VERSION && npm ci && npm run build" >&2
  exit 1
fi

if git -C "$FORGERELAY_ROOT" rev-parse --is-inside-work-tree &>/dev/null; then
  TAG_AT_HEAD="$(git -C "$FORGERELAY_ROOT" describe --tags --exact-match 2>/dev/null || true)"
  if [[ -n "$TAG_AT_HEAD" && "$TAG_AT_HEAD" != "v$REQUIRED_VERSION" ]]; then
    echo "[forgerelay-mcp] checkout at $TAG_AT_HEAD but required v$REQUIRED_VERSION" >&2
    exit 1
  fi
fi

if [[ ! -f "$FORGERELAY_ROOT/scripts/assert-contracts-version.mjs" ]]; then
  echo "[forgerelay-mcp] missing contracts pin script at $FORGERELAY_ROOT/scripts/assert-contracts-version.mjs" >&2
  exit 1
fi

node "$FORGERELAY_ROOT/scripts/assert-contracts-version.mjs" || exit 1

exec node "$ENTRY"
