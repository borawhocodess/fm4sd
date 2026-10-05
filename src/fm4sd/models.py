"""relarena methods of this repo.

`fm4sd-dfs-lightgbm`: gradient-boosted trees on the same DFS features that rdblearn and
tabpfn-rel use. relarena lists this baseline as missing (relarena-alpha paper, open issues,
"missing baselines"). it separates two questions: how much does the flattening give, and
how much does the tabular foundation model give on top.

`DFSTabularModel` is the base for any model that predicts from the flat DFS table. a new
method only has to give `fit_flat` and `predict_flat`. this is where a pfn of our own
plugs in.
"""

from __future__ import annotations

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
        self.fit_flat(df, cat_cols, train_table.df[task.target_col], task.task_type, seed=seed)

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

    def _encode(self, df: pd.DataFrame) -> pd.DataFrame:
        # DFS column names hold quotes and brackets, which lightgbm rejects: use positions.
        x = df.reindex(columns=self._cols).copy(deep=False)
        for c, dtype in self._cat_dtypes.items():
            x[c] = x[c].astype(dtype)
        x.columns = [f"f{i}" for i in range(len(self._cols))]
        return x

    def predict_flat(self, df: pd.DataFrame) -> np.ndarray:
        return self._booster.predict(self._encode(df))
