#!/usr/bin/env bash
# set up relarena + this repo's methods. works on the mac and on a cluster login node.
#
#   scripts/setup.sh            # cpu torch (mac, login node)
#   scripts/setup.sh cuda       # cuda torch (gpu node)
#
# needs: git, uv. relarena is cloned into workdir/repos/relarena (gitignored).
# relarena pins relbench, because the relbench version is the data version.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GROUP="${1:-cpu}"
RELARENA="$ROOT/workdir/repos/relarena"

mkdir -p "$ROOT/workdir/repos" "$ROOT/workdir/runs/cache"
[ -d "$RELARENA" ] || git clone https://github.com/PriorLabs/relarena.git "$RELARENA"

cd "$RELARENA"
uv sync --all-packages --group "$GROUP" --extra tabpfn-rel-local
uv pip install -e "$ROOT"

"$ROOT/scripts/run.sh" --list | tail -3
echo "ok. this repo adds the method fm4sd-dfs-lightgbm."
