#!/usr/bin/env bash
# build the DFS feature cache that every DFS method reads (rdblearn, tabpfn-rel, fm4sd-dfs-*).
# cpu only. do this once per dataset, before any run.
#
#   scripts/warm.sh rel-f1
#   scripts/warm.sh rel-f1 rel-avito
#
# rel-f1 (74k rows): 8.5 min on one mac cpu thread, 60 MB. large databases take hours.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RELARENA="$ROOT/workdir/repos/relarena"
export RELARENA_CACHE_DIR="${RELARENA_CACHE_DIR:-${FM4SD_RUNS:-$ROOT/workdir/runs}/cache}"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
if [ "$(uname)" = "Darwin" ]; then
    export DYLD_FALLBACK_LIBRARY_PATH="$RELARENA/.venv/lib/python3.11/site-packages/sklearn/.dylibs"
fi

cd "$RELARENA"
exec .venv/bin/python workflows/warm_feature_cache.py --datasets "$@"
