#!/usr/bin/env bash
# Optional GitHub repository bootstrap. Safe-by-default: never force-pushes,
# never overwrites an existing remote, and emits structured errors.

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOTSTRAP_LIB_DIR="${SCRIPT_DIR}/lib"

# shellcheck source=lib/log.sh
source "${BOOTSTRAP_LIB_DIR}/log.sh"
# shellcheck source=lib/error.sh
source "${BOOTSTRAP_LIB_DIR}/error.sh"
# shellcheck source=lib/util.sh
source "${BOOTSTRAP_LIB_DIR}/util.sh"

PROJECT_ID=""
OWNER=""
VISIBILITY="private"
DEFAULT_BRANCH="main"
TARGET_DIR=""
CREATE_LABELS=0
CREATE_TEMPLATES=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-id) PROJECT_ID="$2"; shift 2;;
    --owner) OWNER="$2"; shift 2;;
    --visibility) VISIBILITY="$2"; shift 2;;
    --default-branch) DEFAULT_BRANCH="$2"; shift 2;;
    --target-dir) TARGET_DIR="$2"; shift 2;;
    --create-labels) CREATE_LABELS=1; shift;;
    --create-templates) CREATE_TEMPLATES=1; shift;;
    *) bs_die "E0002" "$BS_EXIT_INPUT" "unknown flag: $1";;
  esac
done

if ! bs_require_command gh; then
  bs_die "E0003" "$BS_EXIT_DEPENDENCY" "missing dependency: gh"
fi
if ! gh auth status >/dev/null 2>&1; then
  bs_die "E0004" "$BS_EXIT_GITHUB" "gh is not authenticated" "Run: gh auth login"
fi

if [[ -z "$PROJECT_ID" ]]; then
  bs_die "E0002" "$BS_EXIT_INPUT" "--project-id is required"
fi
if [[ -z "$TARGET_DIR" ]]; then
  bs_die "E0002" "$BS_EXIT_INPUT" "--target-dir is required"
fi
if [[ ! -d "$TARGET_DIR/.git" ]]; then
  bs_die "E0004" "$BS_EXIT_GITHUB" "target dir is not a git repo: $TARGET_DIR"
fi

cd "$TARGET_DIR"

# Refuse to overwrite an existing remote.
if git remote get-url origin >/dev/null 2>&1; then
  bs_log_warn "remote 'origin' already configured; skipping repo creation"
else
  REPO_NAME="${OWNER:+$OWNER/}${PROJECT_ID}"
  bs_log_info "creating repo $REPO_NAME ($VISIBILITY)"
  gh repo create "$REPO_NAME" --"${VISIBILITY}" --source=. --remote=origin --push >/dev/null 2>&1 \
    || bs_die "E0004" "$BS_EXIT_GITHUB" "gh repo create failed"
fi

if [[ "$CREATE_LABELS" == "1" ]]; then
  bs_log_info "creating standard labels (idempotent)"
  for label in "type:bug" "type:feat" "type:docs" "risk:high" "risk:medium" "risk:low" "agent:review-needed"; do
    gh label create "$label" --force >/dev/null 2>&1 || true
  done
fi

if [[ "$CREATE_TEMPLATES" == "1" ]]; then
  mkdir -p .github/ISSUE_TEMPLATE
  if [[ ! -f .github/ISSUE_TEMPLATE/bug.yml ]]; then
    cat > .github/ISSUE_TEMPLATE/bug.yml <<'TPL'
name: Bug
description: File a bug report
labels: [type:bug]
body:
  - type: textarea
    id: what
    attributes:
      label: What happened?
      placeholder: Describe the bug
    validations:
      required: true
TPL
  fi
fi

bs_log_info "github bootstrap complete"
