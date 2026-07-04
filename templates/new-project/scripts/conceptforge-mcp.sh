#!/usr/bin/env bash
# Cursor MCP launcher for ConceptForge. Resolves paths without ${env:CONCEPTFORGE_ROOT} in mcp.json.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONCEPTFORGE_ROOT="${CONCEPTFORGE_ROOT:-$PROJECT_ROOT/../ConceptForge}"
ENTRY="$CONCEPTFORGE_ROOT/dist/index.js"
REQUIRED_VERSION="${CONCEPTFORGE_MIN_VERSION:-0.1.0}"

export CONCEPTFORGE_WORKSPACE="${CONCEPTFORGE_WORKSPACE:-$PROJECT_ROOT/.okf/forge/concept}"
mkdir -p "$CONCEPTFORGE_WORKSPACE"

if [[ ! -f "$ENTRY" ]]; then
  echo "[conceptforge-mcp] missing $ENTRY — run: cd $CONCEPTFORGE_ROOT && npm ci && npm run build" >&2
  exit 1
fi

if [[ ! -f "$CONCEPTFORGE_ROOT/package.json" ]]; then
  echo "[conceptforge-mcp] missing $CONCEPTFORGE_ROOT/package.json" >&2
  exit 1
fi

PKG_VERSION="$(node -p "require('$CONCEPTFORGE_ROOT/package.json').version" 2>/dev/null || echo '')"
if [[ -z "$PKG_VERSION" ]]; then
  echo "[conceptforge-mcp] cannot read package version" >&2
  exit 1
fi

if [[ "$PKG_VERSION" != "$REQUIRED_VERSION" ]]; then
  echo "[conceptforge-mcp] ConceptForge version $PKG_VERSION != required v$REQUIRED_VERSION" >&2
  exit 1
fi

if [[ -f "$CONCEPTFORGE_ROOT/scripts/assert-contracts-version.mjs" ]]; then
  node "$CONCEPTFORGE_ROOT/scripts/assert-contracts-version.mjs" || exit 1
fi

exec node "$ENTRY"
