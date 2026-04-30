#!/usr/bin/env bash
# Sync MCP-owned task fields back into local backlog metadata.
set -Eeuo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
exec python3 -m ai_task_orchestrator.cli backlog-sync \
  --project-root "${PROJECT_ROOT}" "$@"
