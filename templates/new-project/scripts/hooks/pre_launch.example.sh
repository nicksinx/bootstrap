#!/usr/bin/env bash
# Example pre-launch hook. Rename to pre_launch.sh to enable.
set -Eeuo pipefail
echo "[hook] pre_launch executed for ${PROJECT_ID:-<unknown>}"
