"""statistics of the relbench v1 databases and entity tasks, as input for a prior design.

run with the relarena environment, because relarena pins the relbench version:

    cd workdir/repos/relarena
    uv run --all-packages --group cpu python ../../../scripts/relbench_stats.py rel-f1

writes one json per dataset to stats/<dataset>.json in this repo.
column kinds are heuristics on pandas dtypes, not the relbench / pytorch-frame stypes.
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from relbench.datasets import get_dataset
from relbench.tasks import get_task

DATASETS = ["rel-f1", "rel-avito", "rel-trial", "rel-stack", "rel-hm", "rel-amazon", "rel-event"]

ENTITY_TASKS = {
    "rel-amazon": ["user-churn", "item-churn", "user-ltv", "item-ltv"],
    "rel-avito": ["user-visits", "user-clicks", "ad-ctr"],
    "rel-event": ["user-attendance", "user-repeat", "user-ignore"],
    "rel-f1": ["driver-dnf", "driver-top3", "driver-position"],
    "rel-hm": ["user-churn", "item-sales"],
    "rel-stack": ["user-engagement", "user-badge", "post-votes"],
    "rel-trial": ["study-outcome", "study-adverse", "site-success"],
}

OUT = Path(__file__).resolve().parent.parent / "stats"


def kind(s: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(s):
        return "bool"
    if pd.api.types.is_datetime64_any_dtype(s):
        return "datetime"
    if pd.api.types.is_numeric_dtype(s):
        return "numeric"
    sample = s.dropna()
    if len(sample) == 0:
        return "empty"
    sample = sample.sample(min(len(sample), 20000), random_state=0)
    try:
        nunique = sample.astype(str).nunique()
    except Exception:
        return "other"
    mean_len = sample.astype(str).str.len().mean()
    if mean_len > 30 or nunique > 0.5 * len(sample):
        return "text"
    return "categorical"


def quantiles(x) -> dict:
    x = np.asarray(x, dtype="float64")
    if len(x) == 0:
        return {}
    q = np.quantile(x, [0.5, 0.9, 0.99])
    return {
        "mean": round(float(x.mean()), 4),
        "median": float(q[0]),
        "p90": float(q[1]),
        "p99": float(q[2]),
        "max": float(x.max()),
    }


def table_stats(name, table, db) -> dict:
    df = table.df
    fkeys = dict(table.fkey_col_to_pkey_table)
    special = set(fkeys) | {table.pkey_col, table.time_col}
    kinds = {}
    for c in df.columns:
        if c in special:
            continue
        k = kind(df[c])
        kinds[k] = kinds.get(k, 0) + 1
    out = {
        "rows": int(len(df)),
        "columns": int(df.shape[1]),
        "pkey": table.pkey_col,
        "time_col": table.time_col,
        "fkeys": fkeys,
        "feature_kinds": kinds,
        "null_fraction": round(float(df.isna().mean().mean()), 4),
    }
    if table.time_col is not None:
        t = pd.to_datetime(df[table.time_col])
        out["time_min"] = str(t.min())
        out["time_max"] = str(t.max())
    links = {}
    for col, parent in fkeys.items():
        counts = df[col].dropna().value_counts()
        n_parent = len(db.table_dict[parent].df)
        links[col] = {
            "parent": parent,
            "null_fraction": round(float(df[col].isna().mean()), 4),
            "parents_with_children": int(len(counts)),
            "parent_rows": int(n_parent),
            "parents_without_children_fraction": round(1 - len(counts) / max(n_parent, 1), 4),
            "children_per_parent": quantiles(counts.to_numpy()),
        }
    out["links"] = links
    return out


def task_stats(dataset, name) -> dict:
    task = get_task(dataset.name if hasattr(dataset, "name") else dataset, name, download=True)
    out = {
        "type": str(task.task_type).split(".")[-1],
        "entity_table": task.entity_table,
        "entity_col": task.entity_col,
        "time_col": task.time_col,
        "target_col": task.target_col,
        "timedelta": str(task.timedelta),
        "num_eval_timestamps": int(getattr(task, "num_eval_timestamps", 1)),
        "splits": {},
    }
    for split in ["train", "val", "test"]:
        df = task.get_table(split, mask_input_cols=False).df
        y = df[task.target_col]
        s = {
            "rows": int(len(df)),
            "unique_entities": int(df[task.entity_col].nunique()),
            "seed_times": int(df[task.time_col].nunique()),
            "seed_time_min": str(df[task.time_col].min()),
            "seed_time_max": str(df[task.time_col].max()),
            "rows_per_entity": quantiles(df[task.entity_col].value_counts().to_numpy()),
        }
        if out["type"] == "BINARY_CLASSIFICATION":
            s["positive_rate"] = round(float(y.mean()), 4)
        else:
            s["target"] = quantiles(y.to_numpy())
            s["target_std"] = round(float(y.std()), 4)
            s["target_zero_fraction"] = round(float((y == 0).mean()), 4)
        out["splits"][split] = s
    return out


def main(names):
    OUT.mkdir(exist_ok=True)
    for name in names:
        dataset = get_dataset(name, download=True)
        db = dataset.get_db()
        tables = {t: table_stats(t, table, db) for t, table in db.table_dict.items()}
        stats = {
            "dataset": name,
            "val_timestamp": str(dataset.val_timestamp),
            "test_timestamp": str(dataset.test_timestamp),
            "db_time_min": str(db.min_timestamp),
            "db_time_max": str(db.max_timestamp),
            "num_tables": len(tables),
            "total_rows": sum(t["rows"] for t in tables.values()),
            "total_columns": sum(t["columns"] for t in tables.values()),
            "tables": tables,
            "tasks": {},
        }
        for task_name in ENTITY_TASKS[name]:
            stats["tasks"][task_name] = task_stats(name, task_name)
        (OUT / f"{name}.json").write_text(json.dumps(stats, indent=1))
        print(name, "tables", len(tables), "rows", stats["total_rows"], flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or DATASETS)
