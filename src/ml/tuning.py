"""Optuna-based hyperparameter tuning."""

from __future__ import annotations

import warnings

import optuna
import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import confusion_matrix, f1_score
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


def tune_logistic_regression_cv(
    X,
    y: list[str],
    groups: list[str],
    *,
    n_splits: int,
    n_trials: int,
    random_state: int,
) -> dict:
    """Tune only LogisticRegression within grouped, stratified train folds."""
    if len(y) != len(groups):
        raise ValueError("Labels and leakage-control groups must have the same length.")

    from sklearn.linear_model import LogisticRegression

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
        params = {
            "C": trial.suggest_float("C", 1e-3, 10.0, log=True),
            "class_weight": "balanced",
            "max_iter": 500,
            "random_state": random_state,
            "solver": "saga",
        }
        fold_scores = []
        validation_support = {label: 0 for label in sorted(set(labels))}
        for train_index, fold_index in splitter.split(X, labels, group_values):
            model = LogisticRegression(**params)
            model.fit(X[train_index], labels[train_index])
            predictions = model.predict(X[fold_index])
            fold_scores.append(
                float(f1_score(labels[fold_index], predictions, average="macro"))
            )
            for label in labels[fold_index]:
                validation_support[label] += 1
        trial.set_user_attr("fold_macro_f1", fold_scores)
        trial.set_user_attr("class_validation_support", validation_support)
        return float(np.mean(fold_scores))

    study.optimize(run_trial, n_trials=n_trials)
    best_trial = study.best_trial
    fold_scores = best_trial.user_attrs["fold_macro_f1"]
    class_support = best_trial.user_attrs["class_validation_support"]
    limitations = [
        {"class_name": label, "limitation_code": "not_observed"}
        for label, support in sorted(class_support.items())
        if support == 0
    ]
    return {
        "best_params": {
            "C": best_trial.params["C"],
            "class_weight": "balanced",
            "max_iter": 500,
            "random_state": random_state,
            "solver": "saga",
        },
        "macro_f1_mean": best_trial.value,
        "macro_f1_std": float(np.std(fold_scores)),
        "fold_macro_f1": fold_scores,
        "class_limitations": limitations,
        "n_trials": n_trials,
        "n_splits": n_splits,
        "random_state": random_state,
    }


class LinearModelConvergenceError(RuntimeError):
    """Raised when a frozen linear candidate fails to converge in a CV fold."""


def evaluate_frozen_logistic_regression_cv(
    X,
    y: list[str],
    groups: list[str],
    *,
    class_labels: list[str],
    frozen_parameters: dict,
    n_splits: int,
    random_state: int,
) -> dict:
    """Evaluate frozen LogisticRegression parameters without retuning.

    A convergence warning aborts immediately so no partial result can be used as
    delivery evidence or a model-promotion signal.
    """
    if len(y) != len(groups):
        raise ValueError("Labels and leakage-control groups must have the same length.")

    from sklearn.linear_model import LogisticRegression

    labels = np.asarray(y)
    group_values = np.asarray(groups)
    splitter = StratifiedGroupKFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state,
    )
    fold_metrics = []
    aggregate_confusion = np.zeros((len(class_labels), len(class_labels)), dtype=int)
    for fold, (train_index, validation_index) in enumerate(
        splitter.split(X, labels, group_values), start=1
    ):
        model = LogisticRegression(**frozen_parameters)
        with warnings.catch_warnings(record=True) as captured_warnings:
            warnings.simplefilter("always", ConvergenceWarning)
            model.fit(X[train_index], labels[train_index])
        if any(issubclass(warning.category, ConvergenceWarning) for warning in captured_warnings):
            raise LinearModelConvergenceError(
                "Frozen LogisticRegression did not converge; no delivery evidence was written."
            )
        train_predictions = model.predict(X[train_index])
        validation_predictions = model.predict(X[validation_index])
        fold_metrics.append(
            {
                "fold": fold,
                "train_macro_f1": float(
                    f1_score(labels[train_index], train_predictions, average="macro")
                ),
                "validation_macro_f1": float(
                    f1_score(labels[validation_index], validation_predictions, average="macro")
                ),
            }
        )
        aggregate_confusion += confusion_matrix(
            labels[validation_index], validation_predictions, labels=class_labels
        )

    true_positive = np.diag(aggregate_confusion).astype(float)
    predicted_total = aggregate_confusion.sum(axis=0).astype(float)
    actual_total = aggregate_confusion.sum(axis=1).astype(float)
    precision = np.divide(true_positive, predicted_total, out=np.zeros_like(true_positive), where=predicted_total != 0)
    recall = np.divide(true_positive, actual_total, out=np.zeros_like(true_positive), where=actual_total != 0)
    f1 = np.divide(2 * precision * recall, precision + recall, out=np.zeros_like(precision), where=(precision + recall) != 0)
    per_class_metrics = {
        label: {
            "precision": float(precision[index]),
            "recall": float(recall[index]),
            "f1": float(f1[index]),
        }
        for index, label in enumerate(class_labels)
    }
    train_scores = [fold["train_macro_f1"] for fold in fold_metrics]
    validation_scores = [fold["validation_macro_f1"] for fold in fold_metrics]
    return {
        "fold_metrics": fold_metrics,
        "macro_f1_mean": float(np.mean(validation_scores)),
        "macro_f1_std": float(np.std(validation_scores)),
        "train_fold_macro_f1_gap": float(abs(np.mean(train_scores) - np.mean(validation_scores))),
        "per_class_metrics": per_class_metrics,
        "convergence_warning_count": 0,
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
