#!/usr/bin/env bash
# Cursor MCP launcher for RevenueForge.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REVENUEFORGE_ROOT="${REVENUEFORGE_ROOT:-$PROJECT_ROOT/../RevenueForge}"
ENTRY="$REVENUEFORGE_ROOT/dist/index.js"
REQUIRED_VERSION="${REVENUEFORGE_MIN_VERSION:-0.1.0}"

export FORGE_WORKSPACE="${FORGE_WORKSPACE:-$PROJECT_ROOT/.okf/forge/revenue}"
mkdir -p "$FORGE_WORKSPACE"

if [[ ! -f "$ENTRY" ]]; then
  echo "[revenueforge-mcp] missing $ENTRY — run: cd $REVENUEFORGE_ROOT && npm ci && npm run build" >&2
  exit 1
fi

PKG_VERSION="$(node -p "require('$REVENUEFORGE_ROOT/package.json').version" 2>/dev/null || echo '')"
if [[ "$PKG_VERSION" != "$REQUIRED_VERSION" ]]; then
  echo "[revenueforge-mcp] RevenueForge version $PKG_VERSION != required v$REQUIRED_VERSION" >&2
  exit 1
fi

if [[ -f "$REVENUEFORGE_ROOT/scripts/assert-contracts-version.mjs" ]]; then
  node "$REVENUEFORGE_ROOT/scripts/assert-contracts-version.mjs" || exit 1
fi

exec node "$ENTRY"
