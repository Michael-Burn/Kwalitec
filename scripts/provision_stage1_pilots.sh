#!/usr/bin/env bash
# Provision Stage 1 early-access users from ops/STAGE1_PILOT_MAP.local.md
# Usage:
#   1. Fill email + display name in ops/STAGE1_PILOT_MAP.local.md
#   2. export STAGE1_TEMP_PASSWORD='…'   # min 8 chars; shared temp OK if rotated
#   3. ./scripts/provision_stage1_pilots.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
MAP="$ROOT/ops/STAGE1_PILOT_MAP.local.md"
CRED="$ROOT/ops/STAGE1_CREDENTIALS.local.txt"

if [[ ! -f "$MAP" ]]; then
  echo "Missing $MAP — copy from STAGE1_PILOT_MAP.example.md" >&2
  exit 1
fi
if [[ -z "${STAGE1_TEMP_PASSWORD:-}" ]]; then
  echo "Set STAGE1_TEMP_PASSWORD (min 8 chars) before running." >&2
  exit 1
fi
if [[ ${#STAGE1_TEMP_PASSWORD} -lt 8 ]]; then
  echo "STAGE1_TEMP_PASSWORD must be at least 8 characters." >&2
  exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate
set -a
# shellcheck disable=SC1091
source .env
set +a

: > "$CRED"
echo "# Stage 1 temp credentials — LOCAL — do not commit" >> "$CRED"
echo "# Generated $(date -u +%Y-%m-%dT%H:%MZ)" >> "$CRED"
echo >> "$CRED"

provision_one() {
  local pilot_id="$1" name="$2" email="$3"
  if [[ -z "$email" || "$email" == *"@"* && "$email" == *" "|* ]]; then
    :
  fi
  if [[ -z "$name" || -z "$email" || "$email" != *"@"* ]]; then
    echo "Skip $pilot_id — missing name or email in local map" >&2
    return 0
  fi
  echo "Provisioning $pilot_id <$email>…"
  out="$(flask create-test-user --name "$name" --email "$email" --password "$STAGE1_TEMP_PASSWORD" 2>&1)" || {
    echo "$out" >&2
    if echo "$out" | grep -qi "already exists"; then
      echo "  (exists — resolve user id manually)"
      echo "$pilot_id	$email	EXISTING	(see DB)" >> "$CRED"
      return 0
    fi
    return 1
  }
  echo "$out" | tail -5
  uid="$(echo "$out" | sed -n 's/.*(id=\([0-9]*\)).*/\1/p' | tail -1)"
  echo "$pilot_id	$email	id=${uid:-?}	temp_password_set" >> "$CRED"
}

# Parse markdown table rows for BETA-PIL-001..003 (columns: Pilot ID | Display name | Email | ...)
while IFS= read -r line; do
  [[ "$line" == \|[[:space:]]*BETA-PIL-00[123]* ]] || continue
  # strip leading/trailing pipes and split
  row="${line#|}"
  row="${row%|}"
  IFS='|' read -r pilot name email _rest <<< "$row"
  pilot="$(echo "$pilot" | xargs)"
  name="$(echo "$name" | xargs)"
  email="$(echo "$email" | xargs)"
  provision_one "$pilot" "$name" "$email"
done < "$MAP"

echo
echo "Wrote $CRED (gitignored). Update BETA_COHORT.md onboarding after invites are sent."
echo "Send knowledge/product/private_beta/STAGE1_INVITE_PACK.md to each student."
