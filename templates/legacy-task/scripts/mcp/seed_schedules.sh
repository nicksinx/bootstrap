#!/usr/bin/env bash
# Seed scheduled tasks for this project from a local schedule definition.
set -Eeuo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
exec python3 -m ai_task_orchestrator.cli seed-schedules \
  --project-root "${PROJECT_ROOT}" "$@"
