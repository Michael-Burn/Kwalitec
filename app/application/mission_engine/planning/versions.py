"""Planning version constants for the application layer (AP-002D5)."""

from __future__ import annotations

from app.domain.mission.planning.version import PLANNING_VERSION
from app.domain.reasoning.decisions.version import DECISION_VERSION

SUPPORTED_PLANNING_VERSIONS: frozenset[str] = frozenset({PLANNING_VERSION})

# Decisions that may lawfully feed Mission planning (AP-002D3 contract).
SUPPORTED_DECISION_VERSIONS_FOR_PLANNING: frozenset[str] = frozenset(
    {DECISION_VERSION}
)

PLANNING_PROVENANCE_PREFIX = "mission_engine:planning:twin_decision"

__all__ = [
    "PLANNING_PROVENANCE_PREFIX",
    "PLANNING_VERSION",
    "SUPPORTED_DECISION_VERSIONS_FOR_PLANNING",
    "SUPPORTED_PLANNING_VERSIONS",
]
