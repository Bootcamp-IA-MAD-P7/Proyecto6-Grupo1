"""Optuna-based hyperparameter tuning."""

from __future__ import annotations

import optuna
from sklearn.metrics import f1_score


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


def _objective_lgbm(trial, X_train, y_train, X_val, y_val):
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
        "device": "gpu",
        "gpu_platform_id": 0,
        "gpu_device_id": 0,
        "num_threads": 12,
        "random_state": 42,
        "verbosity": -1,
    }
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
) -> dict:
    """Run Optuna tuning for rf, xgb, or lgbm and return best params."""
    _objectives = {"rf": _objective_rf, "xgb": _objective_xgb, "lgbm": _objective_lgbm}
    objective = _objectives.get(model_type, _objective_xgb)
    sampler = optuna.samplers.TPESampler(seed=42)
    study = optuna.create_study(direction=direction, sampler=sampler)
    study.optimize(
        lambda trial: objective(trial, X_train, y_train, X_val, y_val),
        n_trials=n_trials,
    )
    return {
        "best_params": study.best_params,
        "best_value": study.best_value,
        "n_trials": n_trials,
    }
