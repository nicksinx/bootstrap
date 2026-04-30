#!/usr/bin/env bash
# Example post-launch hook. Rename to post_launch.sh to enable.
set -Eeuo pipefail
echo "[hook] post_launch executed for ${PROJECT_ID:-<unknown>}"
