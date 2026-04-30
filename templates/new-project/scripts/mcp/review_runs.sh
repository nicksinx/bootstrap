#!/usr/bin/env bash
# Summarize recent task runs and surface review-ready items.
set -Eeuo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
exec python3 -m ai_task_orchestrator.cli review-runs \
  --project-root "${PROJECT_ROOT}" "$@"
