"""Projection version constants for the application layer (AP-002D4)."""

from __future__ import annotations

from app.domain.learning_graph.projections.version import PROJECTION_VERSION
from app.domain.reasoning.decisions.version import DECISION_VERSION

SUPPORTED_PROJECTION_VERSIONS: frozenset[str] = frozenset({PROJECTION_VERSION})

# Decisions that may lawfully feed Graph projection (AP-002D3 contract).
SUPPORTED_DECISION_VERSIONS_FOR_PROJECTION: frozenset[str] = frozenset(
    {DECISION_VERSION}
)

PROJECTION_PROVENANCE_PREFIX = "learning_graph:projection:twin_decision"

__all__ = [
    "PROJECTION_PROVENANCE_PREFIX",
    "PROJECTION_VERSION",
    "SUPPORTED_DECISION_VERSIONS_FOR_PROJECTION",
    "SUPPORTED_PROJECTION_VERSIONS",
]
