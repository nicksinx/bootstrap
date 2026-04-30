#!/usr/bin/env bash
# Migrate a project from one template/profile version to another.
# Dry-run by default; never writes unless --apply is provided.

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BOOTSTRAP_LIB_DIR="${SCRIPT_DIR}/lib"

# shellcheck source=lib/log.sh
source "${BOOTSTRAP_LIB_DIR}/log.sh"
# shellcheck source=lib/error.sh
source "${BOOTSTRAP_LIB_DIR}/error.sh"

FROM=""
TO=""
APPLY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from) FROM="$2"; shift 2;;
    --to) TO="$2"; shift 2;;
    --apply) APPLY=1; shift;;
    *) bs_die "E0002" "$BS_EXIT_INPUT" "unknown flag: $1";;
  esac
done

if [[ -z "$FROM" || -z "$TO" ]]; then
  bs_die "E0002" "$BS_EXIT_INPUT" "--from and --to are required"
fi

bs_log_info "migration plan ${FROM} -> ${TO} (apply=${APPLY})"

python3 - "${PROJECT_ROOT}" "${FROM}" "${TO}" "${APPLY}" <<'PY'
import json, sys
from pathlib import Path
import yaml

root, from_v, to_v, apply = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4] == "1"

cfg_path = root / "project.config.yaml"
cfg = yaml.safe_load(cfg_path.read_text()) if cfg_path.exists() else {}

current = cfg.get("template_version")
plan = {
    "from": from_v,
    "to": to_v,
    "current_template_version": current,
    "actions": [],
}

if current != from_v:
    plan["actions"].append({
        "kind": "version-mismatch",
        "detail": f"project.config.yaml has template_version={current}, expected {from_v}",
    })

plan["actions"].append({
    "kind": "bump-template-version",
    "detail": f"set template_version to {to_v}",
})

print(json.dumps(plan, indent=2))

if apply and current == from_v:
    cfg["template_version"] = to_v
    cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False))
    print("applied: template_version updated")
PY
