#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: bash tools/run_godot_check.sh GODOT_BIN CHECK_NAME [GODOT_ARGS...]" >&2
  exit 2
fi

godot_bin="$1"
check_name="$2"
shift 2
log_file="${RUNNER_TEMP:-/tmp}/ai-arena-godot-${check_name}.log"

set +e
set -o pipefail
timeout 90s "$godot_bin" "$@" 2>&1 | tee "$log_file"
command_status=$?
set -e

if grep -Eq 'SCRIPT ERROR:|Parse Error:' "$log_file"; then
  echo "::error::Godot emitted a script or parse error during ${check_name}"
  exit 1
fi

exit "$command_status"
