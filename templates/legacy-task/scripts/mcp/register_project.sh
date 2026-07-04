#!/usr/bin/env bash
# Register this project with the MCP server.
set -Eeuo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
exec python3 -m ai_task_orchestrator.cli project-register \
  --project-root "${PROJECT_ROOT}" "$@"
