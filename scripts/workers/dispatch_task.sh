#!/usr/bin/env bash
# Dispatch workers from backlog/queue.yaml and inspect run status.
set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PY="${ROOT}/scripts/lib/worker_runner.py"
sub="${1:-}"
if [[ $# -ge 1 ]]; then
  shift
fi
case "${sub}" in
  start)
    exec python3 "$PY" dispatch-start "$@"
    ;;
  start-next)
    exec python3 "$PY" dispatch-next "$@"
    ;;
  status)
    exec python3 "$PY" status "$@"
    ;;
  stop)
    exec python3 "$PY" stop "$@"
    ;;
  review)
    exec python3 "$PY" review "$@"
    ;;
  *)
    cat >&2 <<EOF
Usage: $0 <command> [args]

Commands:
  start --task-id TASK-XXXX [--run-id ID] [...]   Start worker for queued task
  start-next                                       First ready task in queue
  status [--run-id ID]                             JSON status rows
  stop --agent codex|claude --run-id ID           SIGTERM worker pid
  review [--limit N]                               Recent manifests JSON
EOF
    exit 2
    ;;
esac
