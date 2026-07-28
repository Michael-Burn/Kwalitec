"""Explanation version constants for the application layer (AP-002D6)."""

from __future__ import annotations

from app.domain.intelligent_tutor.explainability.version import EXPLANATION_VERSION
from app.domain.mission.planning.version import PLANNING_VERSION
from app.domain.reasoning.decisions.version import DECISION_VERSION

SUPPORTED_EXPLANATION_VERSIONS: frozenset[str] = frozenset({EXPLANATION_VERSION})

# Decisions that may lawfully feed Tutor explanations (AP-002D3 contract).
SUPPORTED_DECISION_VERSIONS_FOR_EXPLANATION: frozenset[str] = frozenset(
    {DECISION_VERSION}
)

# Mission plans that may lawfully be narrated (AP-002D5 contract).
SUPPORTED_PLANNING_VERSIONS_FOR_EXPLANATION: frozenset[str] = frozenset(
    {PLANNING_VERSION}
)

EXPLANATION_PROVENANCE_PREFIX = "intelligent_tutor:explanation:educational_provenance"

__all__ = [
    "EXPLANATION_PROVENANCE_PREFIX",
    "EXPLANATION_VERSION",
    "SUPPORTED_DECISION_VERSIONS_FOR_EXPLANATION",
    "SUPPORTED_EXPLANATION_VERSIONS",
    "SUPPORTED_PLANNING_VERSIONS_FOR_EXPLANATION",
]
