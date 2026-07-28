"""Learning Graph application DTOs."""

from __future__ import annotations

__all__ = [
    "ProjectionEventDTO",
    "ProjectionResultDTO",
    "RelationshipProjectionDTO",
]


def __getattr__(name: str):
    if name in {
        "ProjectionEventDTO",
        "ProjectionResultDTO",
        "RelationshipProjectionDTO",
    }:
        from app.application.learning_graph.dto import projection_dto as mod

        return getattr(mod, name)
    raise AttributeError(name)
