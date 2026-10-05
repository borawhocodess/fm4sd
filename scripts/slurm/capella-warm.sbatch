#!/usr/bin/env bash
# build the DFS cache for one dataset on capella. cpu work; the partition only has gpu nodes.
#
#   sbatch scripts/slurm/capella-warm.sbatch rel-f1
#
#SBATCH --account=p_adv_fms
#SBATCH --partition=capella
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=24:00:00
#SBATCH --job-name=fm4sd-warm
#SBATCH --output=/data/horse/ws/saoe216i-tfmp/jobs/%x-%j.out
set -euo pipefail

WS=/data/horse/ws/saoe216i-tfmp
ROOT="${FM4SD_ROOT:-$WS/repos/fm4sd}"
export PATH="$HOME/.local/bin:$PATH"
export UV_CACHE_DIR="$WS/.uv-cache" UV_PYTHON_INSTALL_DIR="$WS/.uv-python"
export FM4SD_RUNS="$WS/jobs/fm4sd-runs"
export XDG_CACHE_HOME="$WS/.cache"
export OMP_NUM_THREADS="$SLURM_CPUS_PER_TASK"

mkdir -p "$FM4SD_RUNS/cache"
hostname
time "$ROOT/scripts/warm.sh" "$@"
du -sh "$FM4SD_RUNS/cache"
