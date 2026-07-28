"""Builders for deterministic educational observations and decisions."""

from __future__ import annotations

__all__ = ["DecisionBuilder", "ObservationBuilder"]


def __getattr__(name: str):
    if name == "ObservationBuilder":
        from app.application.reasoning.builders.observation_builder import (
            ObservationBuilder,
        )

        return ObservationBuilder
    if name == "DecisionBuilder":
        from app.application.reasoning.builders.decision_builder import DecisionBuilder

        return DecisionBuilder
    raise AttributeError(name)
