#!/usr/bin/env bash
# Cursor MCP launcher for OperateForge.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OPERATEFORGE_ROOT="${OPERATEFORGE_ROOT:-$PROJECT_ROOT/../OperateForge}"
ENTRY="$OPERATEFORGE_ROOT/dist/index.js"
REQUIRED_VERSION="${OPERATEFORGE_MIN_VERSION:-0.1.0}"

export FORGE_WORKSPACE="${FORGE_WORKSPACE:-$PROJECT_ROOT/.okf/forge/operate}"
mkdir -p "$FORGE_WORKSPACE"

if [[ ! -f "$ENTRY" ]]; then
  echo "[operateforge-mcp] missing $ENTRY — run: cd $OPERATEFORGE_ROOT && npm ci && npm run build" >&2
  exit 1
fi

PKG_VERSION="$(node -p "require('$OPERATEFORGE_ROOT/package.json').version" 2>/dev/null || echo '')"
if [[ "$PKG_VERSION" != "$REQUIRED_VERSION" ]]; then
  echo "[operateforge-mcp] OperateForge version $PKG_VERSION != required v$REQUIRED_VERSION" >&2
  exit 1
fi

if [[ -f "$OPERATEFORGE_ROOT/scripts/assert-contracts-version.mjs" ]]; then
  node "$OPERATEFORGE_ROOT/scripts/assert-contracts-version.mjs" || exit 1
fi

exec node "$ENTRY"
