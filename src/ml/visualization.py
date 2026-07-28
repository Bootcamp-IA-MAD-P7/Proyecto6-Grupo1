"""Visualization utilities: confusion matrix, feature importance, comparison."""

from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay

matplotlib.use("Agg")


def plot_confusion_matrix(
    y_true: list[str],
    y_pred: list[str],
    classes: list[str],
    save_path: str | Path,
    title: str = "Confusion Matrix",
) -> None:
    """Plot and save a normalized confusion matrix."""
    fig, ax = plt.subplots(figsize=(10, 9))
    ConfusionMatrixDisplay.from_predictions(
        y_true,
        y_pred,
        labels=classes,
        normalize="true",
        xticks_rotation=45,
        ax=ax,
        cmap="Blues",
        values_format=".2f",
    )
    ax.set_title(title, fontsize=14)
    fig.tight_layout()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def plot_feature_importance(
    importances: list[float],
    feature_names: list[str],
    save_path: str | Path,
    title: str = "Feature Importance",
    top_n: int = 20,
) -> None:
    """Plot top-N feature importance as horizontal bars."""
    indices = np.argsort(importances)[-top_n:]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(range(len(indices)), [importances[i] for i in indices], color="steelblue")
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels([feature_names[i] for i in indices], fontsize=8)
    ax.set_xlabel("Importance")
    ax.set_title(title)
    fig.tight_layout()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def plot_model_comparison(
    model_names: list[str],
    metrics: dict[str, list[float]],
    save_path: str | Path,
    title: str = "Model Comparison",
) -> None:
    """Plot grouped bar chart comparing multiple models."""
    x = np.arange(len(model_names))
    n_metrics = len(metrics)
    width = 0.8 / n_metrics

    fig, ax = plt.subplots(figsize=(8, 5))
    for i, (metric_name, values) in enumerate(metrics.items()):
        offset = (i - n_metrics / 2) * width + width / 2
        bars = ax.bar(x + offset, values, width, label=metric_name)
        for bar, val in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.005,
                f"{val:.3f}",
                ha="center",
                va="bottom",
                fontsize=7,
            )

    ax.set_xticks(x)
    ax.set_xticklabels(model_names)
    ax.set_ylabel("Score")
    ax.set_title(title)
    ax.legend(fontsize=8, loc="lower right")
    ax.set_ylim(0, 1.0)
    fig.tight_layout()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
