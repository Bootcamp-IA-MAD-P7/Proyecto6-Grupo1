"""Privacy-safe contract checks for locally stored CFPB model artefacts."""

from __future__ import annotations

from collections.abc import Collection, Mapping, Sequence
from pathlib import Path
from typing import Any

import joblib
import numpy as np


class ModelQualityGateError(RuntimeError):
    """Raised when a local model artefact does not satisfy its contract."""


def _controlled_artifact_path(artifact_path: Path, allowed_root: Path) -> Path:
    """Resolve an artefact path and keep it under the configured local root."""
    resolved_root = allowed_root.resolve()
    resolved_artifact = artifact_path.resolve()
    try:
        resolved_artifact.relative_to(resolved_root)
    except ValueError as error:
        raise ModelQualityGateError("Model artifact is outside the controlled root.") from error

    if not resolved_artifact.is_file():
        raise ModelQualityGateError("Model artifact is unavailable.")
    return resolved_artifact


def validate_model_artifact(
    artifact_path: Path,
    *,
    allowed_root: Path,
    feature_columns: Collection[str],
    allowed_feature_columns: Collection[str],
    canonical_labels: Collection[str],
    synthetic_inputs: Sequence[str],
) -> dict[str, Any]:
    """Validate a trusted local artefact using only synthetic inference inputs.

    The caller owns the input values. This gate deliberately returns aggregate
    contract facts only and never logs or includes those inputs in an error.
    """
    expected_features = set(allowed_feature_columns)
    if set(feature_columns) != expected_features:
        raise ModelQualityGateError("Model feature contract is not permitted.")
    if not synthetic_inputs:
        raise ModelQualityGateError("Synthetic inference input is required.")

    resolved_artifact = _controlled_artifact_path(artifact_path, allowed_root)
    try:
        artifact = joblib.load(resolved_artifact)
    except Exception as error:  # pragma: no cover - loader implementation detail
        raise ModelQualityGateError("Model artifact could not be loaded.") from error

    if not isinstance(artifact, Mapping):
        raise ModelQualityGateError("Model artifact has an unsupported structure.")
    vectorizer = artifact.get("vectorizer")
    model = artifact.get("model")
    if not callable(getattr(vectorizer, "transform", None)):
        raise ModelQualityGateError("Model artifact has no compatible vectorizer.")
    if not callable(getattr(model, "predict_proba", None)):
        raise ModelQualityGateError("Model artifact has no probability output.")

    classes = getattr(model, "classes_", None)
    expected_labels = set(canonical_labels)
    if classes is None or set(classes) != expected_labels:
        raise ModelQualityGateError("Model classes do not match the canonical contract.")

    try:
        probabilities = np.asarray(model.predict_proba(vectorizer.transform(synthetic_inputs)))
    except Exception as error:  # pragma: no cover - estimator implementation detail
        raise ModelQualityGateError("Synthetic model inference failed.") from error

    expected_shape = (len(synthetic_inputs), len(expected_labels))
    if probabilities.shape != expected_shape:
        raise ModelQualityGateError("Model probability output has an invalid shape.")
    if not np.isfinite(probabilities).all() or (probabilities < 0).any():
        raise ModelQualityGateError("Model probability output is invalid.")
    if not np.allclose(probabilities.sum(axis=1), 1.0):
        raise ModelQualityGateError("Model probabilities do not form distributions.")

    return {
        "artifact_within_controlled_root": True,
        "feature_contract_valid": True,
        "canonical_class_count": len(expected_labels),
        "probability_shape": list(probabilities.shape),
        "synthetic_inference_valid": True,
    }
