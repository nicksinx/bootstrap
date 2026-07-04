#!/usr/bin/env bash
# Cursor MCP launcher for LaunchForge (mcp-server/ layout). Resolves paths without ${env:LAUNCHFORGE_ROOT} in mcp.json.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LAUNCHFORGE_ROOT="${LAUNCHFORGE_ROOT:-$PROJECT_ROOT/../LaunchForge}"
ENTRY="$LAUNCHFORGE_ROOT/mcp-server/dist/index.js"
REQUIRED_VERSION="${LAUNCHFORGE_MIN_VERSION:-0.1.0}"

export FORGE_WORKSPACE="${FORGE_WORKSPACE:-$PROJECT_ROOT/.okf/forge/launch}"
mkdir -p "$FORGE_WORKSPACE"

if [[ ! -f "$ENTRY" ]]; then
  echo "[launchforge-mcp] missing $ENTRY — run: cd $LAUNCHFORGE_ROOT && npm ci && npm run build" >&2
  exit 1
fi

if [[ ! -f "$LAUNCHFORGE_ROOT/package.json" ]]; then
  echo "[launchforge-mcp] missing $LAUNCHFORGE_ROOT/package.json" >&2
  exit 1
fi

PKG_VERSION="$(node -p "require('$LAUNCHFORGE_ROOT/package.json').version" 2>/dev/null || echo '')"
if [[ -z "$PKG_VERSION" ]]; then
  echo "[launchforge-mcp] cannot read package version" >&2
  exit 1
fi

if [[ "$PKG_VERSION" != "$REQUIRED_VERSION" ]]; then
  echo "[launchforge-mcp] LaunchForge version $PKG_VERSION != required v$REQUIRED_VERSION" >&2
  exit 1
fi

if [[ -f "$LAUNCHFORGE_ROOT/scripts/assert-contracts-version.mjs" ]]; then
  node "$LAUNCHFORGE_ROOT/scripts/assert-contracts-version.mjs" || exit 1
fi

exec node "$ENTRY"
