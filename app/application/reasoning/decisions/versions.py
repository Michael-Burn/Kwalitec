"""Decision version constants for the application layer (AP-002D3)."""

from __future__ import annotations

from app.domain.reasoning.decisions.version import DECISION_VERSION

SUPPORTED_DECISION_VERSIONS: frozenset[str] = frozenset({DECISION_VERSION})

DECISION_PROVENANCE_PREFIX = "reasoning:decision:observation_set"

# Approved mastery parameters (MasteryUpdateRule — no new heuristics).
APPROVED_MASTERY_LEARNING_RATE = 0.28
APPROVED_MASTERY_PRIOR = 0.35
APPROVED_MASTERY_CONFIDENCE_BASE = 0.35
APPROVED_MASTERY_CONFIDENCE_STEP = 0.12
APPROVED_MASTERY_CONFIDENCE_CAP = 0.95

__all__ = [
    "APPROVED_MASTERY_CONFIDENCE_BASE",
    "APPROVED_MASTERY_CONFIDENCE_CAP",
    "APPROVED_MASTERY_CONFIDENCE_STEP",
    "APPROVED_MASTERY_LEARNING_RATE",
    "APPROVED_MASTERY_PRIOR",
    "DECISION_PROVENANCE_PREFIX",
    "DECISION_VERSION",
    "SUPPORTED_DECISION_VERSIONS",
]
