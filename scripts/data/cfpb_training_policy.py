"""Validate the versioned policy before local CFPB preparation begins."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY_PATH = ROOT / "config" / "cfpb_training_policy.json"


class TrainingPolicyError(RuntimeError):
    """Raised when local inputs do not match the approved training policy."""


def fingerprint_file(path: Path) -> str:
    """Return the SHA-256 fingerprint of a local input without reading its content."""

    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_policy(path: Path = DEFAULT_POLICY_PATH) -> dict[str, Any]:
    """Load a checked-in policy that contains no local data paths or narratives."""

    return json.loads(path.read_text(encoding="utf-8"))


def validate_reference_inputs(
    *,
    source_path: Path,
    contract_path: Path,
    policy_path: Path = DEFAULT_POLICY_PATH,
) -> dict[str, Any]:
    """Fail closed unless source and contract fingerprints match the policy."""

    if not source_path.is_file() or not contract_path.is_file():
        raise TrainingPolicyError("Approved local reference inputs are unavailable.")

    policy = load_policy(policy_path)
    reference = policy["reference"]
    if fingerprint_file(source_path) != reference["source_sha256"]:
        raise TrainingPolicyError("Local source does not match the approved training policy.")
    if fingerprint_file(contract_path) != reference["contract_sha256"]:
        raise TrainingPolicyError("Target contract does not match the approved training policy.")
    return policy
