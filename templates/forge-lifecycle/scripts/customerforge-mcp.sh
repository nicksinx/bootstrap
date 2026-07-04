#!/usr/bin/env bash
# Cursor MCP launcher for CustomerForge.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CUSTOMERFORGE_ROOT="${CUSTOMERFORGE_ROOT:-$PROJECT_ROOT/../CustomerForge}"
ENTRY="$CUSTOMERFORGE_ROOT/dist/index.js"
REQUIRED_VERSION="${CUSTOMERFORGE_MIN_VERSION:-0.1.0}"

export FORGE_WORKSPACE="${FORGE_WORKSPACE:-$PROJECT_ROOT/.okf/forge/customer}"
mkdir -p "$FORGE_WORKSPACE"

if [[ ! -f "$ENTRY" ]]; then
  echo "[customerforge-mcp] missing $ENTRY — run: cd $CUSTOMERFORGE_ROOT && npm ci && npm run build" >&2
  exit 1
fi

PKG_VERSION="$(node -p "require('$CUSTOMERFORGE_ROOT/package.json').version" 2>/dev/null || echo '')"
if [[ "$PKG_VERSION" != "$REQUIRED_VERSION" ]]; then
  echo "[customerforge-mcp] CustomerForge version $PKG_VERSION != required v$REQUIRED_VERSION" >&2
  exit 1
fi

if [[ -f "$CUSTOMERFORGE_ROOT/scripts/assert-contracts-version.mjs" ]]; then
  node "$CUSTOMERFORGE_ROOT/scripts/assert-contracts-version.mjs" || exit 1
fi

exec node "$ENTRY"
