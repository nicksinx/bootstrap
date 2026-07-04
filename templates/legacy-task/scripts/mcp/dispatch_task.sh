#!/usr/bin/env bash
# Dispatch a task through the MCP server for this project.
set -Eeuo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
exec python3 -m ai_task_orchestrator.cli task-dispatch \
  --project-root "${PROJECT_ROOT}" "$@"
