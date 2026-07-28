"""Application decision pipeline — observation set → Twin belief (AP-002D3)."""

from __future__ import annotations

from app.application.reasoning.decisions.versions import (
    DECISION_VERSION,
    SUPPORTED_DECISION_VERSIONS,
)

__all__ = [
    "DECISION_VERSION",
    "SUPPORTED_DECISION_VERSIONS",
    "DecisionGenerator",
    "DecisionValidator",
    "TwinUpdater",
]


def __getattr__(name: str):
    if name == "DecisionGenerator":
        from app.application.reasoning.decisions.decision_generator import (
            DecisionGenerator,
        )

        return DecisionGenerator
    if name == "DecisionValidator":
        from app.application.reasoning.decisions.validator import DecisionValidator

        return DecisionValidator
    if name == "TwinUpdater":
        from app.application.reasoning.decisions.twin_updater import TwinUpdater

        return TwinUpdater
    raise AttributeError(name)
