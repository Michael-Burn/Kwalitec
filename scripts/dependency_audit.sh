#!/usr/bin/env bash
# Reproducible dependency vulnerability audit (EI-001.2 / ER-RB-07).
# Hard-fails on any pip-audit finding not listed in
# docs/security/dependency_accepted_vulns.txt
#
# Usage:
#   ./scripts/dependency_audit.sh
#   ./scripts/dependency_audit.sh --output pip-audit.txt
#
# Requires: pip-audit on PATH (CI installs it; locally: pip install pip-audit)

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ACCEPTED_FILE="$ROOT/docs/security/dependency_accepted_vulns.txt"
REQUIREMENTS="$ROOT/requirements.txt"
OUTPUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output|-o)
      OUTPUT="${2:-}"
      if [[ -z "$OUTPUT" ]]; then
        echo "dependency_audit: --output requires a path" >&2
        exit 2
      fi
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [--output FILE]"
      exit 0
      ;;
    *)
      echo "dependency_audit: unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

if [[ ! -f "$ACCEPTED_FILE" ]]; then
  echo "dependency_audit: missing accepted vulns file: $ACCEPTED_FILE" >&2
  exit 2
fi

if [[ ! -f "$REQUIREMENTS" ]]; then
  echo "dependency_audit: missing requirements.txt" >&2
  exit 2
fi

resolve_pip_audit() {
  if command -v pip-audit >/dev/null 2>&1; then
    echo "pip-audit"
    return 0
  fi
  if [[ -x "$ROOT/.venv/bin/pip-audit" ]]; then
    echo "$ROOT/.venv/bin/pip-audit"
    return 0
  fi
  if command -v python >/dev/null 2>&1 && python -m pip_audit --help >/dev/null 2>&1; then
    echo "python -m pip_audit"
    return 0
  fi
  if [[ -x "$ROOT/.venv/bin/python" ]] \
    && "$ROOT/.venv/bin/python" -m pip_audit --help >/dev/null 2>&1; then
    echo "$ROOT/.venv/bin/python -m pip_audit"
    return 0
  fi
  return 1
}

if ! PIP_AUDIT_CMD="$(resolve_pip_audit)"; then
  echo "dependency_audit: pip-audit not found (PATH, .venv, or python -m pip_audit)" >&2
  exit 2
fi

# shellcheck disable=SC2206
PIP_AUDIT_ARR=($PIP_AUDIT_CMD)

ignore_args=()
while IFS= read -r line || [[ -n "$line" ]]; do
  # Trim whitespace
  line="${line#"${line%%[![:space:]]*}"}"
  line="${line%"${line##*[![:space:]]}"}"
  [[ -z "$line" || "$line" == \#* ]] && continue
  ignore_args+=(--ignore-vuln "$line")
done < "$ACCEPTED_FILE"

echo "dependency_audit: auditing $REQUIREMENTS via ${PIP_AUDIT_ARR[*]}"
if [[ ${#ignore_args[@]} -gt 0 ]]; then
  echo "dependency_audit: applying $((${#ignore_args[@]} / 2)) accepted ignore ID(s)"
fi

run_audit() {
  "${PIP_AUDIT_ARR[@]}" -r "$REQUIREMENTS" --progress-spinner=off "${ignore_args[@]}"
}

if [[ -n "$OUTPUT" ]]; then
  set +e
  run_audit | tee "$OUTPUT"
  status=${PIPESTATUS[0]}
  set -e
else
  set +e
  run_audit
  status=$?
  set -e
fi

if [[ "$status" -ne 0 ]]; then
  echo "dependency_audit: FAILED (exit $status)." >&2
  echo "Review docs/security/DEPENDENCY_ASSURANCE_POLICY.md and DEPENDENCY_ACCEPTED_FINDINGS.md." >&2
  exit "$status"
fi

echo "dependency_audit: clean (no unaccepted advisories)"
exit 0
