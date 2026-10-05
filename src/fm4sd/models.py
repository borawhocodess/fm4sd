"""relarena methods of this repo.

`fm4sd-dfs-lightgbm`: gradient-boosted trees on the same DFS features that rdblearn and
tabpfn-rel use. relarena lists this baseline as missing (relarena-alpha paper, open issues,
"missing baselines"). it separates two questions: how much does the flattening give, and
how much does the tabular foundation model give on top.

`fm4sd-rdbpfn`: the released rdb-pfn checkpoint (0.7M parameters, binary classification,
1024 context rows) on the same DFS features. it shows how a pfn plugs in, and it puts
rdb-pfn into the relarena protocol, where the paper does not report it.

`fm4sd-tabpfn-topk`: tabpfn v3 on the k DFS columns that correlate most with the label
(k = 30, 120, or all). a controlled test of feature dilution: same model, same rows, fewer
columns. it is not tabpfn-rel: no recency context, no lag or calendar features.

`DFSTabularModel` is the base for any model that predicts from the flat DFS table. a new
method only has to give `fit_flat` and `predict_flat`. this is where a pfn of our own
plugs in.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from ConfigSpace import Categorical, ConfigurationSpace, Constant, Float, Integer
from relarena_core.featurization.dfs import DFS_MAX_DEPTH, build_dfs_features
from relarena_core.model import RelArenaModel
from relarena_core.registry import register_model
from relarena_core.search_space import SearchSpace
from relbench.base import Database, EntityTask, Table, TaskType

MIN_DEPTH = 2


class DFSTabularModel(RelArenaModel):
    """flat-table model: DFS features in, predictions out.

    features are built exactly as in relarena's rdblearn method: depth from the config,
    past labels of the entity as a history table, anchor columns kept.
    """

    MAX_DEPTH = DFS_MAX_DEPTH

    def _features(self, task: EntityTask, db: Database, table: Table) -> tuple[pd.DataFrame, list[str]]:
        return build_dfs_features(
            task,
            db,
            table,
            depth=self._depth,
            max_depth=self.MAX_DEPTH,
            history_table=self._history_table,
            keep_anchor_columns=True,
            cache=self.cache,
            run_identity=self.run_identity,
        )

    def fit(
        self,
        task: EntityTask,
        db: Database,
        train_table: Table,
        val_table: Table | None,
        *,
        seed: int,
        time_limit: float | None = None,
    ) -> None:
        self._depth = int(self.config.get("max_depth", MIN_DEPTH))
        self._history_table = train_table if task.time_col else None
        df, cat_cols = self._features(task, db, train_table)
        if df.shape[1] == 0:
            raise ValueError(f"DFS produced no features at depth {self._depth}.")
        y = train_table.df[task.target_col]
        self.fit_flat(df, cat_cols, y, task.task_type, seed=seed)
        if os.environ.get("FM4SD_DUMP"):
            self._dump(df, cat_cols, y, task)

    def _dump(self, df: pd.DataFrame, cat_cols: list[str], y: pd.Series, task: EntityTask) -> None:
        """diagnostics: which DFS columns carry the signal. set FM4SD_DUMP to a directory."""
        import json

        num = df.select_dtypes(include=[np.number, bool]).astype("float64")
        corr = num.corrwith(pd.Series(y.to_numpy(dtype="float64"), index=num.index)).abs().fillna(0.0)
        out = {
            "model": self.name,
            "task": f"{task.entity_table}/{task.target_col}",
            "depth": self._depth,
            "rows": int(len(df)),
            "columns": int(df.shape[1]),
            "categorical_columns": list(cat_cols),
            "top_abs_corr": [(c, round(float(v), 4)) for c, v in corr.sort_values(ascending=False).head(40).items()],
            "extra": self._dump_extra(),
        }
        path = Path(os.environ["FM4SD_DUMP"])
        path.mkdir(parents=True, exist_ok=True)
        (path / f"{self.name}-{task.entity_table}-{task.target_col}-d{self._depth}-n{len(df)}.json").write_text(json.dumps(out, indent=1))

    def _dump_extra(self) -> dict:
        return {}

    def predict(self, task: EntityTask, db: Database, table: Table) -> np.ndarray:
        df, _ = self._features(task, db, table)
        return self.predict_flat(df)

    def fit_flat(self, df: pd.DataFrame, cat_cols: list[str], y: pd.Series, task_type: TaskType, *, seed: int) -> None:
        raise NotImplementedError

    def predict_flat(self, df: pd.DataFrame) -> np.ndarray:
        raise NotImplementedError


def _lightgbm_space() -> ConfigurationSpace:
    # same ranges as relarena's entity-only lightgbm (tabarena's space + n_estimators),
    # plus the DFS depth that rdblearn and tabpfn-rel tune.
    return ConfigurationSpace(
        space=[
            Categorical("max_depth", list(range(MIN_DEPTH, DFS_MAX_DEPTH + 1))),
            Integer("n_estimators", (50, 1000), log=True),
            Float("learning_rate", (5e-3, 1e-1), log=True),
            Float("feature_fraction", (0.4, 1.0)),
            Float("bagging_fraction", (0.7, 1.0)),
            Constant("bagging_freq", 1),
            Integer("num_leaves", (2, 200), log=True),
            Integer("min_data_in_leaf", (1, 64), log=True),
            Categorical("extra_trees", [False, True]),
            Integer("min_data_per_group", (2, 100), log=True),
            Float("cat_l2", (5e-3, 2.0), log=True),
            Float("cat_smooth", (1e-3, 100.0), log=True),
            Integer("max_cat_to_onehot", (8, 100), log=True),
            Float("lambda_l1", (1e-4, 1.0)),
            Float("lambda_l2", (1e-4, 2.0)),
        ],
    )


DFS_LIGHTGBM_SPACE = SearchSpace(space=_lightgbm_space(), default_overrides={"max_depth": MIN_DEPTH})

_OBJECTIVE = {TaskType.BINARY_CLASSIFICATION: "binary", TaskType.REGRESSION: "regression_l1"}


@register_model(search_space=DFS_LIGHTGBM_SPACE)
class DFSLightGBM(DFSTabularModel):
    """lightgbm on DFS features. regression uses the L1 objective, because the metric is MAE."""

    name = "fm4sd-dfs-lightgbm"

    def fit_flat(self, df: pd.DataFrame, cat_cols: list[str], y: pd.Series, task_type: TaskType, *, seed: int) -> None:
        import lightgbm as lgb

        params: dict[str, Any] = {k: v for k, v in self.config.items() if k != "max_depth"}
        rounds = int(params.pop("n_estimators", 100))
        params.update(objective=_OBJECTIVE[task_type], verbosity=-1, seed=seed)

        self._cat_dtypes = {c: pd.CategoricalDtype(df[c].astype("category").cat.categories) for c in cat_cols}
        self._cols = list(df.columns)
        x = self._encode(df)
        label = y.to_numpy(dtype=float) if task_type == TaskType.REGRESSION else y.to_numpy()
        cat = [f"f{self._cols.index(c)}" for c in cat_cols]
        self._booster = lgb.train(params, lgb.Dataset(x, label=label, categorical_feature=cat or "auto"), num_boost_round=rounds)

    def _dump_extra(self) -> dict:
        gain = self._booster.feature_importance(importance_type="gain")
        order = np.argsort(gain)[::-1][:40]
        total = float(gain.sum()) or 1.0
        return {"top_gain_share": [(self._cols[i], round(float(gain[i]) / total, 4)) for i in order]}

    def _encode(self, df: pd.DataFrame) -> pd.DataFrame:
        # DFS column names hold quotes and brackets, which lightgbm rejects: use positions.
        x = df.reindex(columns=self._cols).copy(deep=False)
        for c, dtype in self._cat_dtypes.items():
            x[c] = x[c].astype(dtype)
        x.columns = [f"f{i}" for i in range(len(self._cols))]
        return x

    def predict_flat(self, df: pd.DataFrame) -> np.ndarray:
        return self._booster.predict(self._encode(df))


RDBPFN_SPACE = SearchSpace(
    default_overrides={"max_depth": MIN_DEPTH, "n_features": 30},
    fixed_grid=[{"max_depth": MIN_DEPTH, "n_features": k} for k in (30, 60, 120)],
)


@register_model(search_space=RDBPFN_SPACE)
class RDBPFN(DFSTabularModel):
    """released rdb-pfn checkpoint on DFS features.

    needs a clone of https://github.com/MuLabPKU/RDBPFN. its path comes from the
    environment variable FM4SD_RDBPFN, default workdir/repos/RDBPFN in this repo.
    the predictor keeps at most 1024 context rows per forward pass and averages over
    several random contexts when there are more training rows (its own ensemble logic).
    search: the number of DFS columns kept (30, 60, 120), at DFS depth 2.
    """

    name = "fm4sd-rdbpfn"
    supported_task_types = frozenset({TaskType.BINARY_CLASSIFICATION})

    def fit_flat(self, df: pd.DataFrame, cat_cols: list[str], y: pd.Series, task_type: TaskType, *, seed: int) -> None:
        import torch

        root = Path(os.environ.get("FM4SD_RDBPFN", Path(__file__).resolve().parents[2] / "workdir/repos/RDBPFN")) / "inference"
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        cwd = os.getcwd()
        os.chdir(root)  # the predictor finds its checkpoint relative to inference/
        try:
            from src.predictor import RDBPFNClassifier

            np.random.seed(seed)
            torch.manual_seed(seed)
            self._cols = self._select(df, y, int(self.config.get("n_features", 30)))
            df = df[self._cols]
            self._clf = RDBPFNClassifier.from_pretrained("RDBPFN")
            self._clf.fit(df.reset_index(drop=True), y.to_numpy())
        finally:
            os.chdir(cwd)

    @staticmethod
    def _select(df: pd.DataFrame, y: pd.Series, k: int) -> list[str]:
        # rdb-pfn was pretrained on 30 feature columns; DFS gives hundreds or thousands, and its
        # feature attention is quadratic in the column count. keep the k numeric columns with the
        # largest absolute correlation with the label on the training rows. this is our choice,
        # not part of rdb-pfn.
        num = df.select_dtypes(include=[np.number, bool]).astype("float64")
        num = num.loc[:, num.nunique(dropna=True) > 1]
        corr = num.corrwith(pd.Series(y.to_numpy(dtype="float64"), index=num.index)).abs().fillna(0.0)
        return list(corr.sort_values(ascending=False).index[:k])

    def _dump_extra(self) -> dict:
        return {"selected_columns": list(self._cols)}

    def predict_flat(self, df: pd.DataFrame) -> np.ndarray:
        prob = self._clf.predict_proba(df.reindex(columns=self._cols).reset_index(drop=True), chunk_size=2000)
        return np.asarray(prob)[:, 1]


def top_columns(df: pd.DataFrame, y: pd.Series, k: int) -> list[str]:
    """the k numeric columns with the largest absolute correlation with y on the training rows."""
    num = df.select_dtypes(include=[np.number, bool]).astype("float64")
    num = num.loc[:, num.nunique(dropna=True) > 1]
    corr = num.corrwith(pd.Series(y.to_numpy(dtype="float64"), index=num.index)).abs().fillna(0.0)
    return list(corr.sort_values(ascending=False).index[:k])


TABPFN_TOPK_SPACE = SearchSpace(
    default_overrides={"max_depth": MIN_DEPTH, "n_features": 0},
    fixed_grid=[{"max_depth": MIN_DEPTH, "n_features": k} for k in (0, 30, 120)],
)


@register_model(search_space=TABPFN_TOPK_SPACE)
class TabPFNTopK(DFSTabularModel):
    """tabpfn v3 on all DFS columns (n_features 0) or on the top-k correlated numeric ones."""

    name = "fm4sd-tabpfn-topk"

    def fit_flat(self, df: pd.DataFrame, cat_cols: list[str], y: pd.Series, task_type: TaskType, *, seed: int) -> None:
        from relarena_core.tfm import fit_tfm
        from tabpfn_rel.tfm import TFM_REGISTRY

        k = int(self.config.get("n_features", 0))
        self._cols = list(df.columns) if k == 0 else top_columns(df, y, k)
        self._fitted = fit_tfm(df[self._cols], y, task_type, spec=TFM_REGISTRY["tabpfn-v3"], seed=seed)

    def _dump_extra(self) -> dict:
        return {"n_columns": len(self._cols)}

    def predict_flat(self, df: pd.DataFrame) -> np.ndarray:
        from relarena_core.tfm import predict_tfm

        return predict_tfm(self._fitted, df.reindex(columns=self._cols))
