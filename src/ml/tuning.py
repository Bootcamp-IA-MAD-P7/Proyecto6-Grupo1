"""Optuna-based hyperparameter tuning."""

from __future__ import annotations

import optuna
import numpy as np
from sklearn.metrics import f1_score, precision_recall_fscore_support
from sklearn.model_selection import StratifiedGroupKFold
from time import perf_counter


def _fold_metrics(y_train, train_predictions, y_validation, validation_predictions) -> dict:
    """Return aggregate fold metrics without retaining feature inputs."""
    train_macro_f1 = float(f1_score(y_train, train_predictions, average="macro"))
    validation_macro_f1 = float(
        f1_score(y_validation, validation_predictions, average="macro")
    )
    labels = sorted(set(y_validation))
    precision, recall, per_class_f1, support = precision_recall_fscore_support(
        y_validation,
        validation_predictions,
        labels=labels,
        zero_division=0,
    )
    return {
        "train_macro_f1": train_macro_f1,
        "validation_macro_f1": validation_macro_f1,
        "class_limitations": [
            label for label, score in zip(labels, per_class_f1) if float(score) == 0.0
        ],
        "per_class_metrics": {
            str(label): {
                "precision": float(precision[index]),
                "recall": float(recall[index]),
                "f1": float(per_class_f1[index]),
                "support": int(support[index]),
            }
            for index, label in enumerate(labels)
        },
    }


def _aggregate_per_class_metrics(fold_metrics: list[dict]) -> dict:
    """Aggregate validation metrics by canonical class across held-out folds."""
    totals: dict[str, dict[str, float | int]] = {}
    for metrics in fold_metrics:
        for label, values in metrics["per_class_metrics"].items():
            aggregate = totals.setdefault(
                label,
                {"precision": 0.0, "recall": 0.0, "f1": 0.0, "support": 0, "folds": 0},
            )
            aggregate["precision"] += values["precision"]
            aggregate["recall"] += values["recall"]
            aggregate["f1"] += values["f1"]
            aggregate["support"] += values["support"]
            aggregate["folds"] += 1
    return {
        label: {
            "precision": values["precision"] / values["folds"],
            "recall": values["recall"] / values["folds"],
            "f1": values["f1"] / values["folds"],
            "support": values["support"],
        }
        for label, values in sorted(totals.items())
    }


def _objective_rf(trial, X_train, y_train, X_val, y_val, return_metrics=False):
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
    validation_predictions = model.predict(X_val)
    if not return_metrics:
        return f1_score(y_val, validation_predictions, average="macro")
    return _fold_metrics(
        y_train,
        model.predict(X_train),
        y_val,
        validation_predictions,
    )


def _objective_xgb(trial, X_train, y_train, X_val, y_val, return_metrics=False):
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
    validation_predictions = encoder.inverse_transform(model.predict(X_val))
    if not return_metrics:
        return f1_score(y_val, validation_predictions, average="macro")
    return _fold_metrics(
        y_train,
        encoder.inverse_transform(model.predict(X_train)),
        y_val,
        validation_predictions,
    )


def _objective_lgbm(
    trial, X_train, y_train, X_val, y_val, runtime_config=None, return_metrics=False
):
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
    validation_predictions = encoder.inverse_transform(model.predict(X_val))
    if not return_metrics:
        return f1_score(y_val, validation_predictions, average="macro")
    return _fold_metrics(
        y_train,
        encoder.inverse_transform(model.predict(X_train)),
        y_val,
        validation_predictions,
    )


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
        started_at = perf_counter()
        fold_metrics = []
        for train_index, fold_index in splitter.split(X, labels, group_values):
            if model_type == "lgbm":
                metrics = objective(
                    trial,
                    X[train_index],
                    labels[train_index],
                    X[fold_index],
                    labels[fold_index],
                    runtime_config,
                    return_metrics=True,
                )
            else:
                metrics = objective(
                    trial,
                    X[train_index],
                    labels[train_index],
                    X[fold_index],
                    labels[fold_index],
                    return_metrics=True,
                )
            fold_metrics.append(metrics)
        validation_scores = [metrics["validation_macro_f1"] for metrics in fold_metrics]
        train_scores = [metrics["train_macro_f1"] for metrics in fold_metrics]
        class_limitations = sorted(
            {label for metrics in fold_metrics for label in metrics["class_limitations"]}
        )
        trial.set_user_attr("fold_metrics", fold_metrics)
        trial.set_user_attr("train_macro_f1_mean", float(np.mean(train_scores)))
        trial.set_user_attr("train_macro_f1_std", float(np.std(train_scores)))
        trial.set_user_attr("validation_macro_f1_mean", float(np.mean(validation_scores)))
        trial.set_user_attr("validation_macro_f1_std", float(np.std(validation_scores)))
        trial.set_user_attr("execution_cost_seconds", perf_counter() - started_at)
        trial.set_user_attr("class_limitations", class_limitations)
        trial.set_user_attr("per_class_metrics", _aggregate_per_class_metrics(fold_metrics))
        return float(np.mean(validation_scores))

    study.optimize(run_trial, n_trials=n_trials)
    best_trial = study.best_trial
    best_metrics = best_trial.user_attrs["fold_metrics"]
    trial_results = [
        {
            "params": trial.params,
            "train_macro_f1_mean": trial.user_attrs["train_macro_f1_mean"],
            "train_macro_f1_std": trial.user_attrs["train_macro_f1_std"],
            "validation_macro_f1_mean": trial.user_attrs["validation_macro_f1_mean"],
            "validation_macro_f1_std": trial.user_attrs["validation_macro_f1_std"],
            "fold_metrics": trial.user_attrs["fold_metrics"],
            "execution_cost_seconds": trial.user_attrs["execution_cost_seconds"],
            "class_limitations": trial.user_attrs["class_limitations"],
            "per_class_metrics": trial.user_attrs["per_class_metrics"],
        }
        for trial in study.trials
    ]
    return {
        "best_params": best_trial.params,
        "macro_f1_mean": best_trial.value,
        "macro_f1_std": best_trial.user_attrs["validation_macro_f1_std"],
        "fold_macro_f1": [metrics["validation_macro_f1"] for metrics in best_metrics],
        "fold_metrics": best_metrics,
        "train_macro_f1_mean": best_trial.user_attrs["train_macro_f1_mean"],
        "train_macro_f1_std": best_trial.user_attrs["train_macro_f1_std"],
        "execution_cost_seconds": best_trial.user_attrs["execution_cost_seconds"],
        "class_limitations": best_trial.user_attrs["class_limitations"],
        "per_class_metrics": best_trial.user_attrs["per_class_metrics"],
        "trials": trial_results,
        "n_trials": n_trials,
        "n_splits": n_splits,
        "random_state": random_state,
    }


def recommend_candidate(
    candidates: list[dict],
    *,
    maximum_gap: float,
    macro_f1_tie_tolerance: float,
) -> dict:
    """Apply the versioned PG-11 selection rule without consulting test data."""
    eligible = [
        candidate
        for candidate in candidates
        if candidate["train_validation_gap"] < maximum_gap
    ]
    if not eligible:
        return {
            "status": "no_selection_approved",
            "candidate": None,
            "rationale": ["No candidate satisfies the approved train-validation gap."],
        }

    best_macro_f1 = max(candidate["macro_f1_mean"] for candidate in eligible)
    tied = [
        candidate
        for candidate in eligible
        if best_macro_f1 - candidate["macro_f1_mean"] <= macro_f1_tie_tolerance
    ]
    selected = min(
        tied,
        key=lambda candidate: (
            candidate["macro_f1_std"],
            candidate["execution_cost"]["seconds"],
            len(candidate["class_limitations"]),
            candidate["name"],
        ),
    )
    return {
        "status": "recommended_for_validation",
        "candidate": selected["name"],
        "rationale": [
            "Macro F1 is within the approved selection tolerance.",
            "Tie-breakers applied: fold variability, execution cost, and class limitations.",
        ],
    }
