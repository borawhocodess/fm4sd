"""turn stats/<dataset>.json (from relbench_stats.py) into html tables for log.html.

    python3 scripts/stats_summary.py > workdir/runs/stats-summary.html
"""

import json
from pathlib import Path

STATS = Path(__file__).resolve().parent.parent / "stats"


def n(x):
    if x is None:
        return ""
    if isinstance(x, float) and x != int(x):
        return f"{x:,.3g}" if abs(x) < 1000 else f"{x:,.0f}"
    return f"{int(x):,}"


def table(head, rows):
    out = ['<div class="tw"><table>', "<tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr>"]
    out += ["<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows]
    return "\n".join(out + ["</table></div>"])


def main():
    data = [json.loads(p.read_text()) for p in sorted(STATS.glob("rel-*.json"))]

    rows = []
    for d in data:
        kinds = {}
        fks = time_tables = 0
        for t in d["tables"].values():
            for k, v in t["feature_kinds"].items():
                kinds[k] = kinds.get(k, 0) + v
            fks += len(t["fkeys"])
            time_tables += t["time_col"] is not None
        rows.append([
            d["dataset"], d["num_tables"], time_tables, fks, n(d["total_rows"]),
            kinds.get("numeric", 0), kinds.get("categorical", 0), kinds.get("text", 0),
            kinds.get("datetime", 0), kinds.get("bool", 0),
            d["db_time_min"][:10], d["val_timestamp"][:10], d["test_timestamp"][:10],
        ])
    print("<!-- databases -->")
    print(table(["database", "tables", "with time col", "key links", "rows", "numeric", "categorical", "text", "datetime", "bool", "first row", "val cutoff", "test cutoff"], rows))

    rows = []
    for d in data:
        for name, t in d["tables"].items():
            kinds = ", ".join(f"{v} {k}" for k, v in sorted(t["feature_kinds"].items()))
            rows.append([d["dataset"], name, n(t["rows"]), t["columns"], kinds, t["time_col"] or "-", ", ".join(f"{c} → {p}" for c, p in t["fkeys"].items()) or "-", t["null_fraction"]])
    print("<!-- tables -->")
    print(table(["database", "table", "rows", "cols", "feature columns", "time col", "foreign keys", "null fraction"], rows))

    rows = []
    for d in data:
        for name, t in d["tables"].items():
            for col, l in t["links"].items():
                c = l["children_per_parent"]
                rows.append([d["dataset"], f"{name}.{col} → {l['parent']}", n(l["parent_rows"]), l["parents_without_children_fraction"], n(c.get("mean")), n(c.get("median")), n(c.get("p99")), n(c.get("max")), l["null_fraction"]])
    print("<!-- links -->")
    print(table(["database", "link (child.fk → parent)", "parent rows", "parents with no child", "children per parent: mean", "median", "p99", "max", "fk null fraction"], rows))

    rows = []
    for d in data:
        for name, t in d["tasks"].items():
            tr, va, te = (t["splits"][s] for s in ("train", "val", "test"))
            if t["type"] == "BINARY_CLASSIFICATION":
                label = f"positive rate {tr['positive_rate']} / {va['positive_rate']} / {te['positive_rate']}"
            else:
                label = f"mean {n(tr['target']['mean'])}, median {n(tr['target']['median'])}, p99 {n(tr['target']['p99'])}, zero {tr['target_zero_fraction']}"
            rows.append([
                d["dataset"], name, "cls" if "CLASS" in t["type"] else "reg", t["entity_table"], t["timedelta"].replace(" 00:00:00", ""),
                f"{n(tr['rows'])} / {n(va['rows'])} / {n(te['rows'])}", n(tr["unique_entities"]),
                f"{tr['seed_times']} / {va['seed_times']} / {te['seed_times']}", n(tr["rows_per_entity"]["median"]), label,
            ])
    print("<!-- tasks -->")
    print(table(["database", "task", "type", "entity table", "window", "rows train / val / test", "train entities", "seed times train / val / test", "median rows per entity (train)", "label (train / val / test, or train)"], rows))


if __name__ == "__main__":
    main()
