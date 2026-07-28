"""Learning Graph application mappers."""

from __future__ import annotations

__all__ = [
    "map_projection_result",
]


def __getattr__(name: str):
    if name == "map_projection_result":
        from app.application.learning_graph.mappers.projection_mapper import (
            map_projection_result,
        )

        return map_projection_result
    raise AttributeError(name)
