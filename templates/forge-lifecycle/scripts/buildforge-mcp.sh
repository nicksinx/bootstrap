#!/usr/bin/env bash
# Cursor MCP launcher for BuildForge. Resolves paths without ${env:BUILDFORGE_ROOT} in mcp.json.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILDFORGE_ROOT="${BUILDFORGE_ROOT:-$PROJECT_ROOT/../BuildForge}"
ENTRY="$BUILDFORGE_ROOT/dist/index.js"
REQUIRED_VERSION="${BUILDFORGE_MIN_VERSION:-0.1.0}"

export FORGE_WORKSPACE="${FORGE_WORKSPACE:-$PROJECT_ROOT/.okf/forge/build}"
mkdir -p "$FORGE_WORKSPACE"

if [[ ! -f "$ENTRY" ]]; then
  echo "[buildforge-mcp] missing $ENTRY — run: cd $BUILDFORGE_ROOT && npm ci && npm run build" >&2
  exit 1
fi

if [[ ! -f "$BUILDFORGE_ROOT/package.json" ]]; then
  echo "[buildforge-mcp] missing $BUILDFORGE_ROOT/package.json" >&2
  exit 1
fi

PKG_VERSION="$(node -p "require('$BUILDFORGE_ROOT/package.json').version" 2>/dev/null || echo '')"
if [[ -z "$PKG_VERSION" ]]; then
  echo "[buildforge-mcp] cannot read package version" >&2
  exit 1
fi

if [[ "$PKG_VERSION" != "$REQUIRED_VERSION" ]]; then
  echo "[buildforge-mcp] BuildForge version $PKG_VERSION != required v$REQUIRED_VERSION" >&2
  exit 1
fi

if [[ -f "$BUILDFORGE_ROOT/scripts/assert-contracts-version.mjs" ]]; then
  node "$BUILDFORGE_ROOT/scripts/assert-contracts-version.mjs" || exit 1
fi

exec node "$ENTRY"
