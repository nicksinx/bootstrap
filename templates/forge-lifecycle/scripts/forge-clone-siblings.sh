#!/usr/bin/env bash
# Clone Forge portfolio repos as siblings next to this project (optional operator helper).
# Does not vendor Forge code into the product repo.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PARENT="$(cd "$PROJECT_ROOT/.." && pwd)"
ORG="${FORGE_GITHUB_ORG:-nicksinx}"

REPOS=(
  ForgeLifecycleContracts
  ForgeRelay
  ConceptForge
  GovernanceForge
  BuildForge
  LaunchForge
  OperateForge
  CustomerForge
  GrowthForge
  RevenueForge
  InsightForge
  SunsetForge
)

usage() {
  cat <<USAGE
forge-clone-siblings.sh — clone Forge repos as peers of this project

  Parent directory: $PARENT
  Project root:     $PROJECT_ROOT

Options:
  --dry-run    Print clone commands only
  --org <org>  GitHub org/user (default: $ORG)
USAGE
}

DRY_RUN=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift;;
    --org) ORG="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "unknown flag: $1" >&2; usage; exit 1;;
  esac
done

for repo in "${REPOS[@]}"; do
  dest="$PARENT/$repo"
  url="https://github.com/${ORG}/${repo}.git"
  if [[ -d "$dest/.git" ]]; then
    echo "[skip] $dest already exists"
    continue
  fi
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "git clone $url $dest"
  else
    git clone "$url" "$dest"
  fi
done

echo "Done. Build each Forge repo: cd <repo> && npm ci && npm run build"
