#!/usr/bin/env bash
# Regenerate the canonical backlog seed (TASK-0001 + queue.yaml) safely.
# Existing files are not overwritten unless --force is provided.

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BOOTSTRAP_LIB_DIR="${SCRIPT_DIR}/lib"

# shellcheck source=lib/log.sh
source "${BOOTSTRAP_LIB_DIR}/log.sh"
# shellcheck source=lib/error.sh
source "${BOOTSTRAP_LIB_DIR}/error.sh"
# shellcheck source=lib/util.sh
source "${BOOTSTRAP_LIB_DIR}/util.sh"

FORCE=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE=1; shift;;
    *) bs_die "E0002" "$BS_EXIT_INPUT" "unknown flag: $1";;
  esac
done

mkdir -p "${PROJECT_ROOT}/backlog/tasks" "${PROJECT_ROOT}/backlog/templates"

if [[ ! -f "${PROJECT_ROOT}/backlog/queue.yaml" ]] || [[ "$FORCE" == "1" ]]; then
  PROJECT_ID=$(python3 -c "
import yaml
data = yaml.safe_load(open('${PROJECT_ROOT}/project.config.yaml'))
print(data['project_id'])
")
  cat > "${PROJECT_ROOT}/backlog/queue.yaml" <<YAML
schema_version: 1
project_id: ${PROJECT_ID}
queue:
  - task_id: TASK-0001
    status: ready
    priority: P0
    risk: medium
    depends_on: []
YAML
  bs_log_info "wrote backlog/queue.yaml"
fi

bs_log_info "backlog seed complete"
