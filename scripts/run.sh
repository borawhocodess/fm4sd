#!/usr/bin/env bash
# run relarena with this repo's methods and one shared cache. all arguments go to `relarena`.
#
#   scripts/run.sh --list
#   scripts/run.sh --model lightgbm --datasets rel-f1 --n-trials 30
#   scripts/run.sh --model fm4sd-dfs-lightgbm --datasets rel-f1 --tasks driver-top3 --n-trials 30
#   scripts/run.sh --model tabpfn-rel-local-2026-08-15 --datasets rel-f1 --n-trials 3   # needs TABPFN_TOKEN
#
# results go to workdir/runs/<model>-<datasets>-<tasks>.csv unless --output is given.
# DFS methods need a warm cache first: scripts/warm.sh rel-f1
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RELARENA="$ROOT/workdir/repos/relarena"
RUNS="${FM4SD_RUNS:-$ROOT/workdir/runs}"
export RELARENA_CACHE_DIR="${RELARENA_CACHE_DIR:-$RUNS/cache}"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"

# macos: lightgbm needs libomp. use the copy that scikit-learn ships in the venv.
if [ "$(uname)" = "Darwin" ]; then
    export DYLD_FALLBACK_LIBRARY_PATH="$RELARENA/.venv/lib/python3.11/site-packages/sklearn/.dylibs"
fi

model=run; datasets=all; tasks=all; has_output=0; has_cache=0; prev=""
for a in "$@"; do
    case "$prev" in
        --model) model="$a" ;;
        --datasets) datasets="$a" ;;
        --tasks) tasks="$a" ;;
    esac
    [ "$a" = "--output" ] && has_output=1
    [ "$a" = "--cache-dir" ] && has_cache=1
    prev="$a"
done

extra=()
[ "$has_cache" = 0 ] && extra+=(--cache-dir "$RELARENA_CACHE_DIR")
case " $* " in *" --list "*) ;; *) [ "$has_output" = 0 ] && extra+=(--output "$RUNS/$model-$datasets-$tasks.csv") ;; esac

cd "$RELARENA"
exec .venv/bin/relarena "$@" "${extra[@]}"
