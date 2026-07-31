"""Learning Strategy Engine — Educational Intelligence Phase 1 (KWP-007).

Deterministic educational strategy recommendations with explainability.
Consumes existing Evidence / Progress / Twin / cadence outputs only.
"""

from __future__ import annotations

from app.application.learning_strategy.dto import (
    STRATEGY_TITLES,
    ConfidenceCalibration,
    LearningStrategyAdvice,
    MomentumPosture,
    SpacingDecision,
    StrategyAction,
    StrategyEvidenceInput,
)
from app.application.learning_strategy.engine import (
    LearningStrategyEngine,
    get_learning_strategy_engine,
)

__all__ = [
    "STRATEGY_TITLES",
    "ConfidenceCalibration",
    "LearningStrategyAdvice",
    "LearningStrategyEngine",
    "MomentumPosture",
    "SpacingDecision",
    "StrategyAction",
    "StrategyEvidenceInput",
    "get_learning_strategy_engine",
]
