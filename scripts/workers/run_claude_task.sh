#!/usr/bin/env bash
# Start a Claude worker run for a task markdown file (non-blocking by default).
set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
exec python3 "${ROOT}/scripts/lib/worker_runner.py" start --agent claude "$@"
