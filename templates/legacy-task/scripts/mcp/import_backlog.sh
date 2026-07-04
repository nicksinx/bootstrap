#!/usr/bin/env bash
# Import or validate this project's backlog into the MCP server.
set -Eeuo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
exec python3 -m ai_task_orchestrator.cli backlog-import \
  --project-root "${PROJECT_ROOT}" "$@"
