#!/usr/bin/env bash
# Cursor MCP launcher for InsightForge.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INSIGHTFORGE_ROOT="${INSIGHTFORGE_ROOT:-$PROJECT_ROOT/../InsightForge}"
ENTRY="$INSIGHTFORGE_ROOT/dist/index.js"
REQUIRED_VERSION="${INSIGHTFORGE_MIN_VERSION:-0.1.0}"

export FORGE_WORKSPACE="${FORGE_WORKSPACE:-$PROJECT_ROOT/.okf/forge/insight}"
mkdir -p "$FORGE_WORKSPACE"

if [[ ! -f "$ENTRY" ]]; then
  echo "[insightforge-mcp] missing $ENTRY — run: cd $INSIGHTFORGE_ROOT && npm ci && npm run build" >&2
  exit 1
fi

PKG_VERSION="$(node -p "require('$INSIGHTFORGE_ROOT/package.json').version" 2>/dev/null || echo '')"
if [[ "$PKG_VERSION" != "$REQUIRED_VERSION" ]]; then
  echo "[insightforge-mcp] InsightForge version $PKG_VERSION != required v$REQUIRED_VERSION" >&2
  exit 1
fi

if [[ -f "$INSIGHTFORGE_ROOT/scripts/assert-contracts-version.mjs" ]]; then
  node "$INSIGHTFORGE_ROOT/scripts/assert-contracts-version.mjs" || exit 1
fi

exec node "$ENTRY"
