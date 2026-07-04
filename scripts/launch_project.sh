#!/usr/bin/env bash
# Project Launch Automation entry point.
# Bootstraps a deterministic project scaffold and (optionally) GitHub and MCP.

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOTSTRAP_LIB_DIR="${SCRIPT_DIR}/lib"
BOOTSTRAP_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
export BOOTSTRAP_LIB_DIR BOOTSTRAP_ROOT

# shellcheck source=lib/log.sh
source "${BOOTSTRAP_LIB_DIR}/log.sh"
# shellcheck source=lib/error.sh
source "${BOOTSTRAP_LIB_DIR}/error.sh"
# shellcheck source=lib/util.sh
source "${BOOTSTRAP_LIB_DIR}/util.sh"
# shellcheck source=lib/secret.sh
source "${BOOTSTRAP_LIB_DIR}/secret.sh"
# shellcheck source=lib/scaffold.sh
source "${BOOTSTRAP_LIB_DIR}/scaffold.sh"

readonly TEMPLATE_VERSION="2.0.0"

usage() {
  cat <<USAGE
launch_project.sh - Project Launch Automation

Common:
  --name <project-name>            Project id (lowercase, dashes)
  --profile <name>                 Profile name (default: default)
  --target-dir <path>              Where to create the project
  --dry-run                        Print actions, do not write
  --non-interactive                Never prompt
  --force                          Overwrite non-protected content
  --verbose                        Verbose logs

GitHub:
  --with-github
  --github-owner <owner>
  --github-visibility private|public
  --github-default-branch <branch>
  --github-create-labels
  --github-create-templates

Legacy MCP (profile legacy-task only):
  --with-mcp
  --with-mcp-config
  --mcp-server-name <name>
  --mcp-transport stdio|http
  --mcp-command <command>
  --mcp-url <url>
  --mcp-data-dir <path>
  --mcp-project-id <id>
  --mcp-register-only
  --mcp-seed-schedules
  --mcp-auth-profile none|local-token|mtls|oauth
  --mcp-token-source env|keychain

Compatibility:
  --profile-version <semver>
  --compat-mode strict|warn|legacy
USAGE
}

# Defaults; overlaid by profile, then overridden by CLI flags.
PROJECT_NAME=""
PROFILE_NAME="default"
TARGET_DIR=""
DRY_RUN=0
NON_INTERACTIVE=0
FORCE=0
VERBOSE=0

WITH_GITHUB=0
GITHUB_OWNER=""
GITHUB_VISIBILITY="private"
GITHUB_DEFAULT_BRANCH="main"
GITHUB_CREATE_LABELS=0
GITHUB_CREATE_TEMPLATES=0

WITH_MCP=0
WITH_MCP_CONFIG=0
MCP_SERVER_NAME="ai-task-orchestrator"
MCP_TRANSPORT="stdio"
MCP_COMMAND="python3 -m ai_task_orchestrator"
MCP_URL=""
MCP_DATA_DIR=".cursor/mcp-data"
MCP_PROJECT_ID=""
MCP_REGISTER_ONLY=0
MCP_SEED_SCHEDULES=0
MCP_AUTH_PROFILE="local-token"
MCP_TOKEN_SOURCE="env"

PROFILE_VERSION=""
COMPAT_MODE="strict"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) PROJECT_NAME="$2"; shift 2;;
    --profile) PROFILE_NAME="$2"; shift 2;;
    --target-dir) TARGET_DIR="$2"; shift 2;;
    --dry-run) DRY_RUN=1; shift;;
    --non-interactive) NON_INTERACTIVE=1; shift;;
    --force) FORCE=1; shift;;
    --verbose) VERBOSE=1; shift;;
    --with-github) WITH_GITHUB=1; shift;;
    --github-owner) GITHUB_OWNER="$2"; shift 2;;
    --github-visibility) GITHUB_VISIBILITY="$2"; shift 2;;
    --github-default-branch) GITHUB_DEFAULT_BRANCH="$2"; shift 2;;
    --github-create-labels) GITHUB_CREATE_LABELS=1; shift;;
    --github-create-templates) GITHUB_CREATE_TEMPLATES=1; shift;;
    --with-mcp) WITH_MCP=1; shift;;
    --with-mcp-config) WITH_MCP_CONFIG=1; shift;;
    --mcp-server-name) MCP_SERVER_NAME="$2"; shift 2;;
    --mcp-transport) MCP_TRANSPORT="$2"; shift 2;;
    --mcp-command) MCP_COMMAND="$2"; shift 2;;
    --mcp-url) MCP_URL="$2"; shift 2;;
    --mcp-data-dir) MCP_DATA_DIR="$2"; shift 2;;
    --mcp-project-id) MCP_PROJECT_ID="$2"; shift 2;;
    --mcp-register-only) MCP_REGISTER_ONLY=1; shift;;
    --mcp-seed-schedules) MCP_SEED_SCHEDULES=1; shift;;
    --mcp-auth-profile) MCP_AUTH_PROFILE="$2"; shift 2;;
    --mcp-token-source) MCP_TOKEN_SOURCE="$2"; shift 2;;
    --profile-version) PROFILE_VERSION="$2"; shift 2;;
    --compat-mode) COMPAT_MODE="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) bs_die "E0002" "$BS_EXIT_INPUT" "unknown flag: $1" "Run with --help" "docs/errors.md";;
  esac
done

export BOOTSTRAP_VERBOSE="$VERBOSE"
export BOOTSTRAP_FORCE="$FORCE"
export BOOTSTRAP_DRY_RUN="$DRY_RUN"
export BOOTSTRAP_CORRELATION_ID="${BOOTSTRAP_CORRELATION_ID:-$(bs_correlation_id)}"

if [[ -z "$PROJECT_NAME" ]]; then
  bs_die "E0002" "$BS_EXIT_INPUT" "--name is required" "" "docs/errors.md"
fi

if ! bs_validate_project_id "$PROJECT_NAME"; then
  bs_die "E0002" "$BS_EXIT_INPUT" \
    "invalid --name '$PROJECT_NAME'" \
    "Use lowercase letters, digits, and dashes (3-64 chars)" \
    "docs/errors.md"
fi

if [[ -z "$TARGET_DIR" ]]; then
  TARGET_DIR="${PWD}/${PROJECT_NAME}"
fi

for cmd in python3 git; do
  if ! bs_require_command "$cmd"; then
    bs_die "E0003" "$BS_EXIT_DEPENDENCY" "missing dependency: $cmd"
  fi
done
if [[ "$WITH_GITHUB" == "1" ]] && ! bs_require_command gh; then
  bs_die "E0003" "$BS_EXIT_DEPENDENCY" "missing dependency: gh" \
    "Install GitHub CLI or rerun without --with-github"
fi

PROFILE_FILE="${BOOTSTRAP_ROOT}/profiles/${PROFILE_NAME}.yaml"
if [[ ! -f "$PROFILE_FILE" ]]; then
  bs_die "E0002" "$BS_EXIT_INPUT" "unknown profile: $PROFILE_NAME"
fi

# Validate the profile file against schemas/profile.schema.json.
if ! python3 - "$PROFILE_FILE" "${BOOTSTRAP_ROOT}/schemas/profile.schema.json" <<'PY'
import json, sys, yaml
from jsonschema import Draft202012Validator
profile_path, schema_path = sys.argv[1], sys.argv[2]
schema = json.load(open(schema_path))
profile = yaml.safe_load(open(profile_path))
errors = sorted(Draft202012Validator(schema).iter_errors(profile), key=lambda e: e.path)
if errors:
    for e in errors:
        print(f"  profile invalid: {list(e.path)} -> {e.message}", file=sys.stderr)
    sys.exit(1)
PY
then
  bs_die "E1001" "$BS_EXIT_VALIDATION" "profile failed schema validation"
fi

if [[ -z "$PROFILE_VERSION" ]]; then
  PROFILE_VERSION=$(python3 -c "import yaml,sys;print(yaml.safe_load(open('${PROFILE_FILE}')).get('profile_version',''))")
fi

mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

LOCK_FILE="${TARGET_DIR}/.launch.lock"
if ! bs_lock_acquire "$LOCK_FILE"; then
  bs_die "E0010" "$BS_EXIT_UNSAFE" "another launch is in progress at $TARGET_DIR"
fi
trap 'bs_lock_release "$LOCK_FILE"' EXIT

bs_log_info "launching ${PROJECT_NAME} at ${TARGET_DIR}"

GENERATED_AT="$(bs_iso_timestamp)"
TEMPLATE_DIR="${BOOTSTRAP_ROOT}/templates/new-project"

# Export __VAR__ values used by render_template.py
export BOOTSTRAP_VAR_PROJECT_ID="$PROJECT_NAME"
export BOOTSTRAP_VAR_PROJECT_NAME="$PROJECT_NAME"
export BOOTSTRAP_VAR_TEMPLATE_VERSION="$TEMPLATE_VERSION"
export BOOTSTRAP_VAR_PROFILE_NAME="$PROFILE_NAME"
export BOOTSTRAP_VAR_PROFILE_VERSION="$PROFILE_VERSION"
export BOOTSTRAP_VAR_DEFAULT_BRANCH="$GITHUB_DEFAULT_BRANCH"
export BOOTSTRAP_VAR_GENERATED_AT="$GENERATED_AT"
export BOOTSTRAP_VAR_GITHUB_OWNER="$GITHUB_OWNER"
export BOOTSTRAP_VAR_GITHUB_VISIBILITY="$GITHUB_VISIBILITY"
export BOOTSTRAP_VAR_GITHUB_CREATE_LABELS=$([[ "$GITHUB_CREATE_LABELS" == "1" ]] && echo true || echo false)
export BOOTSTRAP_VAR_GITHUB_CREATE_TEMPLATES=$([[ "$GITHUB_CREATE_TEMPLATES" == "1" ]] && echo true || echo false)
if [[ "$PROFILE_NAME" == "legacy-task" ]]; then
  export BOOTSTRAP_VAR_MCP_ENABLED=$([[ "$WITH_MCP" == "1" ]] && echo true || echo false)
else
  export BOOTSTRAP_VAR_MCP_ENABLED=true
fi
export BOOTSTRAP_VAR_MCP_SERVER_NAME="$MCP_SERVER_NAME"
export BOOTSTRAP_VAR_MCP_TRANSPORT="$MCP_TRANSPORT"
export BOOTSTRAP_VAR_MCP_COMMAND="$MCP_COMMAND"
export BOOTSTRAP_VAR_MCP_URL="$MCP_URL"
export BOOTSTRAP_VAR_MCP_DATA_DIR="$MCP_DATA_DIR"
export BOOTSTRAP_VAR_MCP_AUTH_PROFILE="$MCP_AUTH_PROFILE"
export BOOTSTRAP_VAR_MCP_TOKEN_SOURCE="$MCP_TOKEN_SOURCE"
export BOOTSTRAP_VAR_COMPAT_MODE="$COMPAT_MODE"
export BOOTSTRAP_VAR_OKF_ENABLED=true
export BOOTSTRAP_VAR_OKF_BUNDLE_PATH=".okf"
export BOOTSTRAP_VAR_OKF_PROFILE="software-development"
export BOOTSTRAP_VAR_OKF_CONTINUOUS_IMPROVEMENT_PATH=".okf/improvements"

# Render every templated file from the new-project template tree.
render_tree() {
  local src_root="$1"
  while IFS= read -r -d '' src; do
    local rel="${src#"$src_root"/}"
    local dest_rel="${rel%.tmpl}"
    if ! bs_safe_relpath "$dest_rel" >/dev/null; then
      bs_die "E0010" "$BS_EXIT_UNSAFE" "unsafe template path: $dest_rel"
    fi
    local dest="${TARGET_DIR}/${dest_rel}"
    if [[ "$rel" == *.tmpl ]]; then
      bs_render_file "$src" "$dest"
    else
      mkdir -p "$(dirname "$dest")"
      if [[ "$DRY_RUN" == "1" ]]; then
        printf '[dry-run] would copy %s\n' "$dest" >&2
      else
        cp "$src" "$dest"
      fi
    fi
  done < <(find "$src_root" -type f -print0)
}

render_tree "$TEMPLATE_DIR"

LEGACY_OVERLAY_DIR="${BOOTSTRAP_ROOT}/templates/legacy-task"
if [[ "$PROFILE_NAME" == "legacy-task" ]] && [[ -d "$LEGACY_OVERLAY_DIR" ]]; then
  render_tree "$LEGACY_OVERLAY_DIR"
fi

if [[ "${BOOTSTRAP_ROOT}" != "${TARGET_DIR}" ]]; then
  # Copy schemas into the project so it is self-contained.
  mkdir -p "${TARGET_DIR}/schemas"
  for sch in "${BOOTSTRAP_ROOT}"/schemas/*.json; do
    cp "$sch" "${TARGET_DIR}/schemas/$(basename "$sch")"
  done

  # Copy profiles to support idempotent relaunches from generated projects.
  mkdir -p "${TARGET_DIR}/profiles"
  for pf in "${BOOTSTRAP_ROOT}"/profiles/*.yaml; do
    cp "$pf" "${TARGET_DIR}/profiles/$(basename "$pf")"
  done

  # Copy launcher template source so generated projects can dry-run/relaunch.
  TEMPLATE_SOURCE_DIR="${BOOTSTRAP_ROOT}/templates/new-project"
  TEMPLATE_TARGET_DIR="${TARGET_DIR}/templates/new-project"
  if [[ -d "${TEMPLATE_SOURCE_DIR}" ]] && [[ "${TEMPLATE_SOURCE_DIR}" != "${TEMPLATE_TARGET_DIR}" ]]; then
    mkdir -p "${TARGET_DIR}/templates"
    rm -rf "${TEMPLATE_TARGET_DIR}"
    cp -R "${TEMPLATE_SOURCE_DIR}" "${TEMPLATE_TARGET_DIR}"
  fi

  LEGACY_OVERLAY_SOURCE="${BOOTSTRAP_ROOT}/templates/legacy-task"
  LEGACY_OVERLAY_TARGET="${TARGET_DIR}/templates/legacy-task"
  if [[ -d "${LEGACY_OVERLAY_SOURCE}" ]] && [[ "${LEGACY_OVERLAY_SOURCE}" != "${LEGACY_OVERLAY_TARGET}" ]]; then
    rm -rf "${LEGACY_OVERLAY_TARGET}"
    cp -R "${LEGACY_OVERLAY_SOURCE}" "${LEGACY_OVERLAY_TARGET}"
  fi

  # Copy canonical OKF skills (exclude bootstrap-only intake skill).
  if [[ -d "${BOOTSTRAP_ROOT}/skills" ]]; then
    if [[ "$DRY_RUN" == "1" ]]; then
      python3 "${BOOTSTRAP_ROOT}/scripts/lib/copy_okf_skills.py" \
        "${BOOTSTRAP_ROOT}" "${TARGET_DIR}" --dry-run >&2 || true
    else
      python3 "${BOOTSTRAP_ROOT}/scripts/lib/copy_okf_skills.py" \
        "${BOOTSTRAP_ROOT}" "${TARGET_DIR}" \
        || bs_die "E0009" "$BS_EXIT_VALIDATION" "failed to copy OKF skills"
      bs_log_info "copied OKF skills into ${TARGET_DIR}/skills"
    fi
  fi

  # Copy launcher and validation scripts so the project can re-run itself.
  mkdir -p "${TARGET_DIR}/scripts/lib"
  cp "${BOOTSTRAP_ROOT}/scripts/launch_project.sh"      "${TARGET_DIR}/scripts/launch_project.sh"
  cp "${BOOTSTRAP_ROOT}/scripts/github_init.sh"          "${TARGET_DIR}/scripts/github_init.sh"
  cp "${BOOTSTRAP_ROOT}/scripts/backlog_seed.sh"         "${TARGET_DIR}/scripts/backlog_seed.sh"
  cp "${BOOTSTRAP_ROOT}/scripts/validate_launch.sh"      "${TARGET_DIR}/scripts/validate_launch.sh"
  cp "${BOOTSTRAP_ROOT}/scripts/migrate_project.sh"      "${TARGET_DIR}/scripts/migrate_project.sh"
  cp "${BOOTSTRAP_ROOT}"/scripts/lib/*.{sh,py}            "${TARGET_DIR}/scripts/lib/" 2>/dev/null || true
  if [[ "$PROFILE_NAME" == "legacy-task" ]]; then
    mkdir -p "${TARGET_DIR}/scripts/workers"
    for wf in "${BOOTSTRAP_ROOT}/scripts/workers/"*.sh; do
      [[ -f "$wf" ]] || continue
      cp "$wf" "${TARGET_DIR}/scripts/workers/"
    done
  fi
fi
chmod +x "${TARGET_DIR}"/scripts/*.sh "${TARGET_DIR}"/scripts/okf-* "${TARGET_DIR}"/scripts/hooks/*.sh "${TARGET_DIR}"/scripts/*forge*.sh "${TARGET_DIR}"/scripts/forgerelay-mcp.sh 2>/dev/null || true
chmod +x "${TARGET_DIR}"/scripts/mcp/*.sh 2>/dev/null || true
chmod +x "${TARGET_DIR}"/scripts/workers/*.sh 2>/dev/null || true

if [[ "$PROFILE_NAME" == "legacy-task" ]]; then
  if [[ "$WITH_MCP_CONFIG" == "1" ]]; then
    if [[ "$DRY_RUN" != "1" ]]; then
      cp "${TARGET_DIR}/.cursor/mcp.json.example" "${TARGET_DIR}/.cursor/mcp.json"
      bs_log_info "wrote .cursor/mcp.json (ai-task, gitignored)"
    fi
  fi
else
  if [[ "$DRY_RUN" != "1" ]]; then
    if [[ -f "${TARGET_DIR}/.cursor/mcp-forge-lifecycle.json.example" ]]; then
      cp "${TARGET_DIR}/.cursor/mcp-forge-lifecycle.json.example" "${TARGET_DIR}/.cursor/mcp.json"
      bs_log_info "wrote .cursor/mcp.json from forge-lifecycle example (gitignored)"
    else
      bs_die "E0007" "$BS_EXIT_MCP_REGISTER" "missing .cursor/mcp-forge-lifecycle.json.example"
    fi
  fi
fi

# Initialise git repo if one does not already exist.
if [[ ! -d "${TARGET_DIR}/.git" ]] && [[ "$DRY_RUN" != "1" ]]; then
  ( cd "$TARGET_DIR" && git init -q -b "$GITHUB_DEFAULT_BRANCH" )
  bs_log_info "initialised git repository"
fi

# Optional GitHub bootstrap.
if [[ "$WITH_GITHUB" == "1" ]] && [[ "$DRY_RUN" != "1" ]]; then
  "${BOOTSTRAP_ROOT}/scripts/github_init.sh" \
    --project-id "$PROJECT_NAME" \
    --owner "$GITHUB_OWNER" \
    --visibility "$GITHUB_VISIBILITY" \
    --default-branch "$GITHUB_DEFAULT_BRANCH" \
    --target-dir "$TARGET_DIR" \
    $([[ "$GITHUB_CREATE_LABELS" == "1" ]] && echo "--create-labels") \
    $([[ "$GITHUB_CREATE_TEMPLATES" == "1" ]] && echo "--create-templates") \
    || bs_die "E0004" "$BS_EXIT_GITHUB" "GitHub bootstrap failed"
fi

# Optional ai-task MCP registration (legacy-task profile only).
if [[ "$PROFILE_NAME" == "legacy-task" ]] && [[ "$WITH_MCP" == "1" ]] && [[ "$DRY_RUN" != "1" ]]; then
  "${TARGET_DIR}/scripts/mcp/register_project.sh" --json \
    || bs_die "E0006" "$BS_EXIT_MCP_REGISTER" "MCP registration failed"
fi

if [[ "$PROFILE_NAME" == "legacy-task" ]] && [[ "$MCP_SEED_SCHEDULES" == "1" ]] && [[ "$DRY_RUN" != "1" ]]; then
  "${TARGET_DIR}/scripts/mcp/seed_schedules.sh" \
    || bs_die "E0008" "$BS_EXIT_MCP_SCHEDULE" "MCP schedule seeding failed"
fi

# Run validation as a post-step.
if [[ "$DRY_RUN" != "1" ]]; then
  "${TARGET_DIR}/scripts/validate_launch.sh" \
    || bs_die "E0009" "$BS_EXIT_VALIDATION" "post-launch validation failed"
fi

bs_log_info "launch complete: ${PROJECT_NAME}"
