#!/bin/sh
set -eu

url=${1:-http://127.0.0.1:8876}
out=${2:?output directory required}
exec "$(dirname "$0")/capture_reference.sh" prc-c0 "$url" "$out"
