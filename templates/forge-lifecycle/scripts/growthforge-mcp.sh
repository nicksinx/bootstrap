#!/usr/bin/env bash
# Cursor MCP launcher for GrowthForge.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GROWTHFORGE_ROOT="${GROWTHFORGE_ROOT:-$PROJECT_ROOT/../GrowthForge}"
ENTRY="$GROWTHFORGE_ROOT/dist/index.js"
REQUIRED_VERSION="${GROWTHFORGE_MIN_VERSION:-0.1.0}"

export FORGE_WORKSPACE="${FORGE_WORKSPACE:-$PROJECT_ROOT/.okf/forge/growth}"
mkdir -p "$FORGE_WORKSPACE"

if [[ ! -f "$ENTRY" ]]; then
  echo "[growthforge-mcp] missing $ENTRY — run: cd $GROWTHFORGE_ROOT && npm ci && npm run build" >&2
  exit 1
fi

PKG_VERSION="$(node -p "require('$GROWTHFORGE_ROOT/package.json').version" 2>/dev/null || echo '')"
if [[ "$PKG_VERSION" != "$REQUIRED_VERSION" ]]; then
  echo "[growthforge-mcp] GrowthForge version $PKG_VERSION != required v$REQUIRED_VERSION" >&2
  exit 1
fi

if [[ -f "$GROWTHFORGE_ROOT/scripts/assert-contracts-version.mjs" ]]; then
  node "$GROWTHFORGE_ROOT/scripts/assert-contracts-version.mjs" || exit 1
fi

exec node "$ENTRY"
