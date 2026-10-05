"""compare run results with relarena's published results. prints an html table for log.html.

    python3 scripts/compare.py workdir/runs/capella > workdir/runs/compare.html
"""

import csv
import glob
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLISHED = ROOT / "workdir/repos/relarena/baseline_results/results.csv"
ORDER = [l.split() for l in (ROOT / "scripts/slurm/tasks.txt").read_text().splitlines() if l and not l.startswith("#")]
MINE = ["fm4sd-dfs-lightgbm", "tabpfn-rel-local-2026-08-15"]
PUB = ["lightgbm", "rdblearn", "tabpfn-rel-local-2026-08-15", "tabpfn-rel-local-2026-09-28", "rt-plurel"]


def selected(path):
    out = {}
    for r in csv.DictReader(open(path)):
        if r.get("selected") in ("True", "true", "1") and r.get("test_score"):
            out[(r["model"], r["dataset"], r["task"])] = (float(r["test_score"]), r["metric"])
    return out


def main(run_dir):
    pub = selected(PUBLISHED)
    mine = {}
    for f in glob.glob(f"{run_dir}/*.csv"):
        mine.update(selected(f))
    head = ["task", "metric"] + [f"mine: {m}" for m in MINE] + [f"published: {m}" for m in PUB]
    print('<div class="tw"><table>')
    print("<tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr>")
    for dataset, task in ORDER:
        metric = next((v[1] for k, v in list(pub.items()) + list(mine.items()) if k[1:] == (dataset, task)), "")
        cells = [f"{dataset}/{task}", "AUC ↑" if metric == "roc_auc" else "MAE ↓"]
        for src, names in ((mine, MINE), (pub, PUB)):
            for m in names:
                v = src.get((m, dataset, task))
                cells.append("" if v is None else f"{v[0]:.4f}" if v[0] < 10 else f"{v[0]:.2f}")
        print("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    print("</table></div>")
    print(f"<!-- runs found: {len(mine)} -->")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "workdir/runs/capella"))
