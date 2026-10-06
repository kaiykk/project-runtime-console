#!/bin/sh
set -eu

name=${1:?reference name required}
url=${2:?url required}
out=${3:?output directory required}
codex_home=${CODEX_HOME:-$HOME/.codex}
pwcli=${PWCLI:-$codex_home/skills/playwright/scripts/playwright_cli.sh}

mkdir -p "$out"
"$pwcli" open "$url" --headed >"$out/open.txt" 2>&1
"$pwcli" snapshot >"$out/snapshot.txt" 2>&1
"$pwcli" screenshot --filename "$out/overview.png" >"$out/screenshot.txt" 2>&1
"$pwcli" tracing-start >"$out/tracing-start.txt" 2>&1
"$pwcli" snapshot >"$out/trace-snapshot.txt" 2>&1
"$pwcli" tracing-stop >"$out/tracing-stop.txt" 2>&1 || true
printf 'name=%s\nurl=%s\n' "$name" "$url" >"$out/metadata.txt"
