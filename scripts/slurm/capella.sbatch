#!/usr/bin/env bash
# one relarena run per array element on capella (tu dresden).
#
#   sbatch --array=0-2 scripts/slurm/capella.sbatch fm4sd-dfs-lightgbm 30 rel-f1
#   sbatch --array=0-20 scripts/slurm/capella.sbatch tabpfn-rel-local-2026-08-15 3
#
# arguments: <model> <n_trials> [dataset]. the array index picks the task from scripts/slurm/tasks.txt
# (filtered by dataset if given). header values are the ones tested by bora's other session on 5 oct 2026.
#SBATCH --account=p_adv_fms
#SBATCH --partition=capella
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --job-name=fm4sd
#SBATCH --output=jobs/%x-%A_%a.out
set -euo pipefail

WS=/data/horse/ws/saoe216i-tfmp
ROOT="${FM4SD_ROOT:-$WS/repos/fm4sd}"
export PATH="$HOME/.local/bin:$PATH"
export UV_CACHE_DIR="$WS/.uv-cache" UV_PYTHON_INSTALL_DIR="$WS/.uv-python"
export FM4SD_RUNS="$WS/jobs/fm4sd-runs"
export OMP_NUM_THREADS="$SLURM_CPUS_PER_TASK"
# relbench downloads go here, not to $HOME
export XDG_CACHE_HOME="$WS/.cache"
# TABPFN_TOKEN must be in the environment for tabpfn methods. do not write the key into this file.

MODEL="$1"; TRIALS="$2"; DATASET="${3:-}"
LINE=$(grep -v '^#' "$ROOT/scripts/slurm/tasks.txt" | { [ -n "$DATASET" ] && grep "^$DATASET " || cat; } | sed -n "$((SLURM_ARRAY_TASK_ID + 1))p")
[ -n "$LINE" ] || { echo "no task for array index $SLURM_ARRAY_TASK_ID"; exit 1; }
set -- $LINE

mkdir -p "$FM4SD_RUNS"
"$ROOT/scripts/run.sh" --model "$MODEL" --datasets "$1" --tasks "$2" --n-trials "$TRIALS"
