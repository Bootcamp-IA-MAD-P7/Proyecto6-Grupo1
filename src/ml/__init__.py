"""Reusable ML modules for CFPB complaint classification."""

from src.ml.evaluation import EvaluationReport, evaluate
from src.ml.models import train_rf, train_xgb
from src.ml.tuning import tune_hyperparams
from src.ml.vectorizer import VectorizerConfig
from src.ml.visualization import (
    plot_confusion_matrix,
    plot_feature_importance,
    plot_model_comparison,
)

__all__ = [
    "EvaluationReport",
    "VectorizerConfig",
    "evaluate",
    "plot_confusion_matrix",
    "plot_feature_importance",
    "plot_model_comparison",
    "train_rf",
    "train_xgb",
    "tune_hyperparams",
]
