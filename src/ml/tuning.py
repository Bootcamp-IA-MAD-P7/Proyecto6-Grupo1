"""Optuna-based hyperparameter tuning."""

from __future__ import annotations

import optuna
import numpy as np
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedGroupKFold


def _objective_rf(trial, X_train, y_train, X_val, y_val):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 300, step=50),
        "max_depth": trial.suggest_int("max_depth", 4, 16),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 2, 8),
        "class_weight": "balanced",
        "n_jobs": -1,
        "random_state": 42,
    }
    from sklearn.ensemble import RandomForestClassifier

    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    return f1_score(y_val, preds, average="macro")


def _objective_xgb(trial, X_train, y_train, X_val, y_val):
    import xgboost as xgb
    from sklearn.preprocessing import LabelEncoder

    encoder = LabelEncoder()
    y_train_enc = encoder.fit_transform(y_train)
    y_val_enc = encoder.transform(y_val)

    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 300, step=50),
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        "reg_lambda": trial.suggest_float("reg_lambda", 1.0, 10.0, log=True),
        "reg_alpha": trial.suggest_float("reg_alpha", 0.0, 5.0),
        "min_child_weight": trial.suggest_int("min_child_weight", 3, 10),
        "eval_metric": "mlogloss",
        "random_state": 42,
        "verbosity": 0,
        "n_jobs": -1,
        "tree_method": "hist",
        "early_stopping_rounds": 15,
    }
    model = xgb.XGBClassifier(**params)
    model.fit(
        X_train, y_train_enc,
        eval_set=[(X_val, y_val_enc)],
        verbose=False,
    )
    preds_enc = model.predict(X_val)
    return f1_score(y_val_enc, preds_enc, average="macro")


def _objective_lgbm(trial, X_train, y_train, X_val, y_val, runtime_config=None):
    import lightgbm as lgb
    from sklearn.preprocessing import LabelEncoder

    encoder = LabelEncoder()
    y_train_enc = encoder.fit_transform(y_train)
    y_val_enc = encoder.transform(y_val)

    params = {
        "num_leaves": trial.suggest_int("num_leaves", 15, 31),
        "max_depth": trial.suggest_int("max_depth", 3, 6),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "bagging_fraction": trial.suggest_float("bagging_fraction", 0.6, 1.0),
        "bagging_freq": 5,
        "feature_fraction": trial.suggest_float("feature_fraction", 0.6, 1.0),
        "reg_lambda": trial.suggest_float("reg_lambda", 0.0, 3.0),
        "reg_alpha": trial.suggest_float("reg_alpha", 0.0, 5.0),
        "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 5, 50),
        "n_estimators": trial.suggest_int("n_estimators", 100, 500, step=50),
        "objective": "multiclass",
        "metric": "multi_logloss",
        "device": "cpu",
        "num_threads": 12,
        "random_state": 42,
        "verbosity": -1,
    }
    params.update(runtime_config or {})
    model = lgb.LGBMClassifier(**params)
    model.fit(
        X_train, y_train_enc,
        eval_X=X_val,
        eval_y=y_val_enc,
        callbacks=[lgb.early_stopping(15)],
    )
    preds_enc = model.predict(X_val)
    return f1_score(y_val_enc, preds_enc, average="macro")


def tune_hyperparams(
    model_type: str,
    X_train,
    y_train: list[str],
    X_val,
    y_val: list[str],
    n_trials: int = 30,
    direction: str = "maximize",
    runtime_config: dict | None = None,
) -> dict:
    """Run Optuna tuning; runtime_config is used only by LightGBM."""
    _objectives = {"rf": _objective_rf, "xgb": _objective_xgb, "lgbm": _objective_lgbm}
    objective = _objectives.get(model_type, _objective_xgb)
    sampler = optuna.samplers.TPESampler(seed=42)
    study = optuna.create_study(direction=direction, sampler=sampler)
    if model_type == "lgbm":
        run_trial = lambda trial: objective(
            trial, X_train, y_train, X_val, y_val, runtime_config
        )
    else:
        run_trial = lambda trial: objective(trial, X_train, y_train, X_val, y_val)
    study.optimize(
        run_trial,
        n_trials=n_trials,
    )
    return {
        "best_params": study.best_params,
        "best_value": study.best_value,
        "n_trials": n_trials,
    }


def tune_hyperparams_cv(
    model_type: str,
    X,
    y: list[str],
    groups: list[str],
    *,
    n_splits: int,
    n_trials: int,
    random_state: int,
    runtime_config: dict | None = None,
) -> dict:
    """Tune one candidate only within grouped, stratified training folds."""
    if len(y) != len(groups):
        raise ValueError("Labels and leakage-control groups must have the same length.")

    objectives = {"rf": _objective_rf, "xgb": _objective_xgb, "lgbm": _objective_lgbm}
    objective = objectives.get(model_type)
    if objective is None:
        raise ValueError(f"Unsupported model candidate: {model_type}.")

    labels = np.asarray(y)
    group_values = np.asarray(groups)
    splitter = StratifiedGroupKFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state,
    )
    sampler = optuna.samplers.TPESampler(seed=random_state)
    study = optuna.create_study(direction="maximize", sampler=sampler)

    def run_trial(trial):
        fold_scores = []
        for train_index, fold_index in splitter.split(X, labels, group_values):
            if model_type == "lgbm":
                score = objective(
                    trial,
                    X[train_index],
                    labels[train_index],
                    X[fold_index],
                    labels[fold_index],
                    runtime_config,
                )
            else:
                score = objective(
                    trial,
                    X[train_index],
                    labels[train_index],
                    X[fold_index],
                    labels[fold_index],
                )
            fold_scores.append(float(score))
        trial.set_user_attr("fold_macro_f1", fold_scores)
        return float(np.mean(fold_scores))

    study.optimize(run_trial, n_trials=n_trials)
    best_trial = study.best_trial
    fold_scores = best_trial.user_attrs["fold_macro_f1"]
    return {
        "best_params": best_trial.params,
        "macro_f1_mean": best_trial.value,
        "macro_f1_std": float(np.std(fold_scores)),
        "fold_macro_f1": fold_scores,
        "n_trials": n_trials,
        "n_splits": n_splits,
        "random_state": random_state,
    }
