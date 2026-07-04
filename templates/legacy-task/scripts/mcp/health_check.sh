#!/usr/bin/env bash
# Probe MCP server health for this project.
set -Eeuo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
exec python3 -m ai_task_orchestrator.cli health \
  --project-root "${PROJECT_ROOT}" "$@"
