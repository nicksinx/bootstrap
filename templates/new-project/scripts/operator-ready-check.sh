#!/usr/bin/env bash
# Post-standup verification: Cursor rules, operator skills, and OKF validation.
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

errors=0

check_file() {
  local rel="$1"
  if [[ -f "${rel}" ]]; then
    printf 'OK   %s\n' "${rel}"
  else
    printf 'MISS %s\n' "${rel}"
    errors=$((errors + 1))
  fi
}

echo "operator-ready-check: ${PROJECT_ROOT}"
echo ""

echo "## Cursor rules"
for f in \
  .cursor/rules/okf.mdc \
  .cursor/rules/okf-ecosystem-routing.mdc \
  .cursor/rules/okf-forge-operator.mdc \
  .cursor/rules/okf-dispatch.mdc \
  .cursor/rules/okf-forge-promotion.mdc \
  .cursor/rules/okf-legacy-aitask.mdc
do
  check_file "${f}"
done

echo ""
echo "## Operator skills"
for f in \
  skills/okf-reader/SKILL.md \
  skills/codex-okf-operator/SKILL.md \
  skills/claude-okf-operator/SKILL.md \
  skills/cursor-okf-operator/SKILL.md \
  skills/xcode-okf-operator/SKILL.md \
  docs/okf-service-operator-skills.md
do
  check_file "${f}"
done

echo ""
if [[ -f .cursor/mcp.json ]]; then
  printf 'OK   .cursor/mcp.json\n'
else
  printf 'WARN .cursor/mcp.json (copy from .cursor/mcp-forge-lifecycle.json.example after MCP setup)\n'
fi

echo ""
if [[ -x scripts/validate_launch.sh ]]; then
  echo "## validate_launch.sh"
  if scripts/validate_launch.sh; then
    :
  else
    errors=$((errors + 1))
  fi
fi

if [[ -x scripts/okf-validate ]]; then
  echo ""
  echo "## okf-validate"
  if scripts/okf-validate; then
    :
  else
    errors=$((errors + 1))
  fi
fi

echo ""
if [[ "${errors}" -eq 0 ]]; then
  echo "operator-ready-check: PASS"
  exit 0
fi

echo "operator-ready-check: FAIL (${errors} missing or failed check(s))"
exit 9
