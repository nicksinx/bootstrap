#!/usr/bin/env bash
# Cursor MCP launcher for SunsetForge.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SUNSETFORGE_ROOT="${SUNSETFORGE_ROOT:-$PROJECT_ROOT/../SunsetForge}"
ENTRY="$SUNSETFORGE_ROOT/dist/index.js"
REQUIRED_VERSION="${SUNSETFORGE_MIN_VERSION:-0.1.0}"

export FORGE_WORKSPACE="${FORGE_WORKSPACE:-$PROJECT_ROOT/.okf/forge/sunset}"
mkdir -p "$FORGE_WORKSPACE"

if [[ ! -f "$ENTRY" ]]; then
  echo "[sunsetforge-mcp] missing $ENTRY — run: cd $SUNSETFORGE_ROOT && npm ci && npm run build" >&2
  exit 1
fi

PKG_VERSION="$(node -p "require('$SUNSETFORGE_ROOT/package.json').version" 2>/dev/null || echo '')"
if [[ "$PKG_VERSION" != "$REQUIRED_VERSION" ]]; then
  echo "[sunsetforge-mcp] SunsetForge version $PKG_VERSION != required v$REQUIRED_VERSION" >&2
  exit 1
fi

if [[ -f "$SUNSETFORGE_ROOT/scripts/assert-contracts-version.mjs" ]]; then
  node "$SUNSETFORGE_ROOT/scripts/assert-contracts-version.mjs" || exit 1
fi

exec node "$ENTRY"
