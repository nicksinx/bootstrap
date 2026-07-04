#!/usr/bin/env bash
# Cursor MCP launcher for GovernanceForge. Resolves paths without ${env:GOVERNANCEFORGE_ROOT} in mcp.json.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GOVERNANCEFORGE_ROOT="${GOVERNANCEFORGE_ROOT:-$PROJECT_ROOT/../GovernanceForge}"
ENTRY="$GOVERNANCEFORGE_ROOT/dist/index.js"
REQUIRED_VERSION="${GOVERNANCEFORGE_MIN_VERSION:-0.1.0}"

export FORGE_WORKSPACE="${FORGE_WORKSPACE:-$PROJECT_ROOT/.okf/forge/governance}"
mkdir -p "$FORGE_WORKSPACE"

if [[ ! -f "$ENTRY" ]]; then
  echo "[governanceforge-mcp] missing $ENTRY — run: cd $GOVERNANCEFORGE_ROOT && npm ci && npm run build" >&2
  exit 1
fi

if [[ ! -f "$GOVERNANCEFORGE_ROOT/package.json" ]]; then
  echo "[governanceforge-mcp] missing $GOVERNANCEFORGE_ROOT/package.json" >&2
  exit 1
fi

PKG_VERSION="$(node -p "require('$GOVERNANCEFORGE_ROOT/package.json').version" 2>/dev/null || echo '')"
if [[ -z "$PKG_VERSION" ]]; then
  echo "[governanceforge-mcp] cannot read package version" >&2
  exit 1
fi

if [[ "$PKG_VERSION" != "$REQUIRED_VERSION" ]]; then
  echo "[governanceforge-mcp] GovernanceForge version $PKG_VERSION != required v$REQUIRED_VERSION" >&2
  exit 1
fi

if [[ -f "$GOVERNANCEFORGE_ROOT/scripts/assert-contracts-version.mjs" ]]; then
  node "$GOVERNANCEFORGE_ROOT/scripts/assert-contracts-version.mjs" || exit 1
fi

exec node "$ENTRY"
