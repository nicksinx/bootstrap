#!/usr/bin/env bash
# Orchestrate end-to-end project standup in a designated folder.
# Wraps launch_project.sh with strong validation, secure MCP preflight,
# optional GitHub bootstrap, and optional post-launch actions.

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOTSTRAP_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BOOTSTRAP_LIB_DIR="${SCRIPT_DIR}/lib"
export BOOTSTRAP_ROOT BOOTSTRAP_LIB_DIR

# shellcheck source=lib/log.sh
source "${BOOTSTRAP_LIB_DIR}/log.sh"
# shellcheck source=lib/error.sh
source "${BOOTSTRAP_LIB_DIR}/error.sh"
# shellcheck source=lib/util.sh
source "${BOOTSTRAP_LIB_DIR}/util.sh"

usage() {
  cat <<'USAGE'
standup_project.sh - Stand up a project in a designated folder.

Primary:
  --project-dir <abs-or-rel-path>    Designated project folder (basename must match project-id convention)
                                     Default: current working directory

Common:
  --profile <name>                   Launcher profile (default: default)
  --create-dir                       Create project dir if missing
  --non-interactive                  Never prompt (default)
  --interactive                      Allow interactive mode
  --force                            Allow scaffold overwrites where supported
  --dry-run                          Print actions only
  --verbose                          Verbose logs

GitHub:
  --with-github
  --github-owner <owner-or-org>
  --github-visibility private|public
  --github-default-branch <branch>
  --github-create-labels
  --github-create-templates

MCP:
  --with-mcp
  --with-mcp-config
  --allow-insecure-mcp               Bypass secure env preflight checks
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

Post-launch actions:
  --skip-post-validate               Skip extra validate-launch rerun
  --backlog-init                     Seed backlog after launch
  --worker-next                      Dispatch next ready task after launch
  --release-gate                     Run release-gate output

Examples:
  # Run from inside the target folder; project id auto-uses folder name.
  cd /Users/dv/projects/Codex/hummingbird-crypto-trading
  /Users/dv/projects/Codex/Bootstrap/scripts/standup_project.sh --with-github --with-mcp --with-mcp-config

  # Explicit project folder mode.
  ./scripts/standup_project.sh --project-dir "$HOME/projects/acme-signals" --with-github --github-owner my-org
USAGE
}

PROJECT_DIR=""
PROFILE_NAME="default"
CREATE_DIR=0
NON_INTERACTIVE=1
FORCE=0
DRY_RUN=0
VERBOSE=0

WITH_GITHUB=0
GITHUB_OWNER=""
GITHUB_VISIBILITY="private"
GITHUB_DEFAULT_BRANCH="main"
GITHUB_CREATE_LABELS=0
GITHUB_CREATE_TEMPLATES=0

WITH_MCP=0
WITH_MCP_CONFIG=0
ALLOW_INSECURE_MCP=0
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

POST_VALIDATE=1
POST_BACKLOG_INIT=0
POST_WORKER_NEXT=0
POST_RELEASE_GATE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-dir) PROJECT_DIR="$2"; shift 2;;
    --profile) PROFILE_NAME="$2"; shift 2;;
    --create-dir) CREATE_DIR=1; shift;;
    --non-interactive) NON_INTERACTIVE=1; shift;;
    --interactive) NON_INTERACTIVE=0; shift;;
    --force) FORCE=1; shift;;
    --dry-run) DRY_RUN=1; shift;;
    --verbose) VERBOSE=1; shift;;

    --with-github) WITH_GITHUB=1; shift;;
    --github-owner) GITHUB_OWNER="$2"; shift 2;;
    --github-visibility) GITHUB_VISIBILITY="$2"; shift 2;;
    --github-default-branch) GITHUB_DEFAULT_BRANCH="$2"; shift 2;;
    --github-create-labels) GITHUB_CREATE_LABELS=1; shift;;
    --github-create-templates) GITHUB_CREATE_TEMPLATES=1; shift;;

    --with-mcp) WITH_MCP=1; shift;;
    --with-mcp-config) WITH_MCP_CONFIG=1; shift;;
    --allow-insecure-mcp) ALLOW_INSECURE_MCP=1; shift;;
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

    --skip-post-validate) POST_VALIDATE=0; shift;;
    --backlog-init) POST_BACKLOG_INIT=1; shift;;
    --worker-next) POST_WORKER_NEXT=1; shift;;
    --release-gate) POST_RELEASE_GATE=1; shift;;

    -h|--help) usage; exit 0;;
    *) bs_die "E0002" "$BS_EXIT_INPUT" "unknown flag: $1" "Run with --help";;
  esac
done

export BOOTSTRAP_VERBOSE="$VERBOSE"
export BOOTSTRAP_CORRELATION_ID="${BOOTSTRAP_CORRELATION_ID:-$(bs_correlation_id)}"

if [[ -z "$PROJECT_DIR" ]]; then
  PROJECT_DIR="."
  bs_log_info "no --project-dir provided; using current directory"
fi

PROJECT_DIR_ABS="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$PROJECT_DIR")"
PROJECT_NAME="$(basename "$PROJECT_DIR_ABS")"

if ! bs_validate_project_id "$PROJECT_NAME"; then
  bs_die "E0002" "$BS_EXIT_INPUT" \
    "invalid project folder name '$PROJECT_NAME'" \
    "Use lowercase letters, digits, and dashes (3-64 chars)"
fi

if [[ ! -d "$PROJECT_DIR_ABS" ]]; then
  if [[ "$CREATE_DIR" == "1" ]]; then
    mkdir -p "$PROJECT_DIR_ABS"
  else
    bs_die "E0002" "$BS_EXIT_INPUT" \
      "project dir does not exist: $PROJECT_DIR_ABS" \
      "Create it first or rerun with --create-dir"
  fi
fi

for cmd in python3 git; do
  if ! bs_require_command "$cmd"; then
    bs_die "E0003" "$BS_EXIT_DEPENDENCY" "missing dependency: $cmd"
  fi
done

if [[ "$WITH_GITHUB" == "1" ]]; then
  if ! bs_require_command gh; then
    bs_die "E0003" "$BS_EXIT_DEPENDENCY" "missing dependency: gh"
  fi
  if [[ "$DRY_RUN" != "1" ]] && ! gh auth status >/dev/null 2>&1; then
    bs_die "E0004" "$BS_EXIT_GITHUB" "gh is not authenticated" "Run: gh auth login"
  fi
fi

if [[ "$WITH_MCP" == "1" ]] && [[ "$ALLOW_INSECURE_MCP" != "1" ]] && [[ "$DRY_RUN" != "1" ]]; then
  if [[ -z "${AITASK_MCP_API_KEY:-}" ]]; then
    bs_die "E0010" "$BS_EXIT_UNSAFE" \
      "secure MCP mode requires AITASK_MCP_API_KEY" \
      "Set env var or pass --allow-insecure-mcp for local-only usage"
  fi
  if [[ "$MCP_TRANSPORT" == "http" ]]; then
    if [[ -z "${AITASK_HTTP_API_KEY:-}" ]]; then
      bs_die "E0010" "$BS_EXIT_UNSAFE" \
        "secure HTTP mode requires AITASK_HTTP_API_KEY" \
        "Set env var or pass --allow-insecure-mcp for local-only usage"
    fi
    if [[ "${AITASK_HTTP_AUTH_MODE:-}" != "all_requests" ]]; then
      bs_die "E0010" "$BS_EXIT_UNSAFE" \
        "secure HTTP mode requires AITASK_HTTP_AUTH_MODE=all_requests" \
        "Set auth mode or pass --allow-insecure-mcp for local-only usage"
    fi
  fi
fi
if [[ "$WITH_MCP" == "1" ]] && [[ "$ALLOW_INSECURE_MCP" != "1" ]] && [[ "$DRY_RUN" == "1" ]]; then
  bs_log_warn "dry-run: skipping secure MCP env preflight checks"
fi

LAUNCH_ARGS=(
  --name "$PROJECT_NAME"
  --profile "$PROFILE_NAME"
  --target-dir "$PROJECT_DIR_ABS"
)

[[ "$DRY_RUN" == "1" ]] && LAUNCH_ARGS+=(--dry-run)
[[ "$NON_INTERACTIVE" == "1" ]] && LAUNCH_ARGS+=(--non-interactive)
[[ "$FORCE" == "1" ]] && LAUNCH_ARGS+=(--force)
[[ "$VERBOSE" == "1" ]] && LAUNCH_ARGS+=(--verbose)

if [[ "$WITH_GITHUB" == "1" ]]; then
  LAUNCH_ARGS+=(--with-github --github-visibility "$GITHUB_VISIBILITY" --github-default-branch "$GITHUB_DEFAULT_BRANCH")
  [[ -n "$GITHUB_OWNER" ]] && LAUNCH_ARGS+=(--github-owner "$GITHUB_OWNER")
  [[ "$GITHUB_CREATE_LABELS" == "1" ]] && LAUNCH_ARGS+=(--github-create-labels)
  [[ "$GITHUB_CREATE_TEMPLATES" == "1" ]] && LAUNCH_ARGS+=(--github-create-templates)
fi

if [[ "$WITH_MCP" == "1" ]]; then
  if [[ -z "$MCP_PROJECT_ID" ]]; then
    MCP_PROJECT_ID="$PROJECT_NAME"
  fi
  LAUNCH_ARGS+=(
    --with-mcp
    --mcp-server-name "$MCP_SERVER_NAME"
    --mcp-transport "$MCP_TRANSPORT"
    --mcp-command "$MCP_COMMAND"
    --mcp-url "$MCP_URL"
    --mcp-data-dir "$MCP_DATA_DIR"
    --mcp-auth-profile "$MCP_AUTH_PROFILE"
    --mcp-token-source "$MCP_TOKEN_SOURCE"
  )
  [[ "$WITH_MCP_CONFIG" == "1" ]] && LAUNCH_ARGS+=(--with-mcp-config)
  LAUNCH_ARGS+=(--mcp-project-id "$MCP_PROJECT_ID")
  [[ "$MCP_REGISTER_ONLY" == "1" ]] && LAUNCH_ARGS+=(--mcp-register-only)
  [[ "$MCP_SEED_SCHEDULES" == "1" ]] && LAUNCH_ARGS+=(--mcp-seed-schedules)
fi

bs_log_info "standing up project '$PROJECT_NAME' at '$PROJECT_DIR_ABS'"
if [[ "$DRY_RUN" == "1" ]]; then
  printf '[dry-run] would run: %q' "${SCRIPT_DIR}/launch_project.sh" >&2
  if [[ "${#LAUNCH_ARGS[@]}" -gt 0 ]]; then
    printf ' ' >&2
    printf '%q ' "${LAUNCH_ARGS[@]}" >&2
  fi
  printf '\n' >&2
else
  "${SCRIPT_DIR}/launch_project.sh" "${LAUNCH_ARGS[@]}"
fi

run_post() {
  local title="$1"
  shift
  local cmd="$1"
  shift || true
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[dry-run] would run (%s): %q' "$title" "$cmd" >&2
    if [[ "$#" -gt 0 ]]; then
      printf ' ' >&2
      printf '%q ' "$@" >&2
    fi
    printf '\n' >&2
  else
    bs_log_info "$title"
    "$cmd" "$@"
  fi
}

if [[ "$POST_VALIDATE" == "1" ]]; then
  run_post "post-validate" "${PROJECT_DIR_ABS}/scripts/validate_launch.sh"
fi
if [[ "$POST_BACKLOG_INIT" == "1" ]]; then
  run_post "backlog-init" "${PROJECT_DIR_ABS}/scripts/backlog_seed.sh"
fi
if [[ "$POST_WORKER_NEXT" == "1" ]]; then
  run_post "worker-next" "${PROJECT_DIR_ABS}/scripts/workers/dispatch_task.sh" start-next
fi
if [[ "$POST_RELEASE_GATE" == "1" ]]; then
  run_post "release-gate" "${PROJECT_DIR_ABS}/scripts/validate_launch.sh" --release-gate
fi

bs_log_info "standup complete: $PROJECT_NAME"
