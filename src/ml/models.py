"""Wrapper functions for Random Forest and XGBoost classifiers."""

from __future__ import annotations

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from src.ml.vectorizer import VectorizerConfig

DEFAULT_RF_CONFIG = {
    "n_estimators": 200,
    "max_depth": 12,
    "min_samples_leaf": 4,
    "class_weight": "balanced",
    "n_jobs": -1,
    "random_state": 42,
}

DEFAULT_XGB_CONFIG = {
    "n_estimators": 1000,
    "max_depth": 6,
    "learning_rate": 0.1,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_lambda": 1.0,
    "reg_alpha": 0.0,
    "min_child_weight": 3,
    "eval_metric": "mlogloss",
    "random_state": 42,
    "verbosity": 1,
    "n_jobs": -1,
    "tree_method": "hist",
    "device": "cuda",
}


class LabelEncodedModel:
    """Wraps a classifier with LabelEncoder for string label support."""

    def __init__(self, model_fn, config: dict):
        self._learner = model_fn(**config)
        self._encoder = LabelEncoder()
        self._config = config

    def fit(self, X, y: list[str], **fit_kwargs):
        y_enc = self._encoder.fit_transform(y)
        self._learner.fit(X, y_enc, **fit_kwargs)
        return self

    def predict(self, X):
        y_enc = self._learner.predict(X)
        return self._encoder.inverse_transform(y_enc)

    def predict_proba(self, X):
        return self._learner.predict_proba(X)

    @property
    def feature_importances_(self):
        return self._learner.feature_importances_

    @property
    def classes_(self):
        return self._encoder.classes_

    @property
    def learner(self):
        return self._learner


def train_rf(
    X,
    y: list[str],
    config: dict | None = None,
) -> LabelEncodedModel:
    """Train a Random Forest classifier."""
    merged = {**DEFAULT_RF_CONFIG, **(config or {})}
    model = LabelEncodedModel(RandomForestClassifier, merged)
    model.fit(X, y)
    return model


def train_xgb(
    X,
    y: list[str],
    config: dict | None = None,
    eval_set: tuple | None = None,
) -> LabelEncodedModel:
    """Train an XGBoost classifier with optional early stopping."""
    import xgboost as xgb

    merged = {**DEFAULT_XGB_CONFIG, **(config or {}), "early_stopping_rounds": 20}
    model = LabelEncodedModel(xgb.XGBClassifier, merged)
    y_enc = model._encoder.fit_transform(y)
    fit_kwargs = {}
    if eval_set:
        X_eval, y_eval = eval_set
        y_eval_enc = model._encoder.transform(y_eval)
        fit_kwargs["eval_set"] = [(X_eval, y_eval_enc)]
        fit_kwargs["verbose"] = False
    model._learner.fit(X, y_enc, **fit_kwargs)
    return model


def train_and_save(
    model_fn,
    X_train,
    y_train: list[str],
    vectorizer: VectorizerConfig,
    config: dict,
    save_path: str,
) -> object:
    """Train a model with a vectorizer and save artefact with joblib."""
    model = model_fn(X_train, y_train, config)
    joblib.dump({"vectorizer": vectorizer, "model": model, "config": config}, save_path)
    return model
