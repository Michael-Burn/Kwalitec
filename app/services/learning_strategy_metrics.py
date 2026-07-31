"""Learning Strategy metrics for Founder observability (KWP-007).

Aggregates deterministic strategy advice over persisted Evidence Packages.
Does not change Evidence Authority, Twin, Progress, or Session runtime.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from app.application.learning_strategy.dto import (
    ConfidenceCalibration,
    SpacingDecision,
    StrategyAction,
)
from app.application.learning_strategy.engine import LearningStrategyEngine


@dataclass(frozen=True)
class LearningStrategyMetricsSnapshot:
    """Founder-facing strategy distribution and calibration summary."""

    sittings_evaluated: int = 0
    strategy_counts: dict[str, int] = field(default_factory=dict)
    spacing_counts: dict[str, int] = field(default_factory=dict)
    momentum_counts: dict[str, int] = field(default_factory=dict)
    calibration_counts: dict[str, int] = field(default_factory=dict)
    recovery_rate: float = 0.0
    reinforcement_rate: float = 0.0
    advance_rate: float = 0.0
    revision_rate: float = 0.0
    over_confident_rate: float = 0.0
    under_confident_rate: float = 0.0
    immediate_spacing_rate: float = 0.0
    recommendation_frequency: float = 0.0

    def to_opaque(self) -> dict[str, Any]:
        return {
            "sittings_evaluated": self.sittings_evaluated,
            "strategy_counts": dict(self.strategy_counts),
            "spacing_counts": dict(self.spacing_counts),
            "momentum_counts": dict(self.momentum_counts),
            "calibration_counts": dict(self.calibration_counts),
            "recovery_rate": round(self.recovery_rate, 4),
            "reinforcement_rate": round(self.reinforcement_rate, 4),
            "advance_rate": round(self.advance_rate, 4),
            "revision_rate": round(self.revision_rate, 4),
            "over_confident_rate": round(self.over_confident_rate, 4),
            "under_confident_rate": round(self.under_confident_rate, 4),
            "immediate_spacing_rate": round(self.immediate_spacing_rate, 4),
            "recommendation_frequency": round(self.recommendation_frequency, 4),
        }


class LearningStrategyMetrics:
    """Compute strategy distribution from persisted sitting packages."""

    _RECOVERY = frozenset(
        {
            StrategyAction.RECOVER_PRIOR_KNOWLEDGE.value,
        }
    )
    _REINFORCEMENT = frozenset(
        {
            StrategyAction.IMMEDIATE_REINFORCEMENT.value,
            StrategyAction.CONSOLIDATE_UNDERSTANDING.value,
            StrategyAction.REPEAT_PRACTICE.value,
            StrategyAction.PRACTICE_FOR_CERTAINTY.value,
        }
    )
    _ADVANCE = frozenset(
        {
            StrategyAction.ADVANCE_TOPIC.value,
            StrategyAction.INCREASE_CHALLENGE.value,
        }
    )
    _REVISION = frozenset(
        {
            StrategyAction.SCHEDULED_REVISION.value,
        }
    )

    @staticmethod
    def from_packages(
        packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
        *,
        engine: LearningStrategyEngine | None = None,
    ) -> LearningStrategyMetricsSnapshot:
        strategy_engine = engine or LearningStrategyEngine()
        strategy_counts: Counter[str] = Counter()
        spacing_counts: Counter[str] = Counter()
        momentum_counts: Counter[str] = Counter()
        calibration_counts: Counter[str] = Counter()
        evaluated = 0

        for raw in packages:
            if not isinstance(raw, dict):
                continue
            advice = strategy_engine.evaluate_opaque(raw)
            evaluated += 1
            strategy_counts[advice.action.value] += 1
            spacing_counts[advice.spacing.value] += 1
            momentum_counts[advice.momentum.value] += 1
            calibration_counts[advice.calibration.value] += 1

        if evaluated == 0:
            return LearningStrategyMetricsSnapshot()

        def _rate(keys: frozenset[str]) -> float:
            return sum(strategy_counts[k] for k in keys) / evaluated

        return LearningStrategyMetricsSnapshot(
            sittings_evaluated=evaluated,
            strategy_counts=dict(strategy_counts),
            spacing_counts=dict(spacing_counts),
            momentum_counts=dict(momentum_counts),
            calibration_counts=dict(calibration_counts),
            recovery_rate=_rate(LearningStrategyMetrics._RECOVERY),
            reinforcement_rate=_rate(LearningStrategyMetrics._REINFORCEMENT),
            advance_rate=_rate(LearningStrategyMetrics._ADVANCE),
            revision_rate=_rate(LearningStrategyMetrics._REVISION),
            over_confident_rate=(
                calibration_counts.get(
                    ConfidenceCalibration.OVER_CONFIDENT.value, 0
                )
                / evaluated
            ),
            under_confident_rate=(
                calibration_counts.get(
                    ConfidenceCalibration.UNDER_CONFIDENT.value, 0
                )
                / evaluated
            ),
            immediate_spacing_rate=(
                spacing_counts.get(SpacingDecision.IMMEDIATE.value, 0)
                / evaluated
            ),
            recommendation_frequency=1.0,
        )

    @classmethod
    def from_store(cls, store: Any) -> LearningStrategyMetricsSnapshot:
        packages: list[dict[str, Any]] = []
        list_fn = getattr(store, "list_evidence_packages", None)
        if callable(list_fn):
            raw_list = list_fn()
            if isinstance(raw_list, list | tuple):
                packages = [p for p in raw_list if isinstance(p, dict)]
        elif hasattr(store, "evidence_packages"):
            raw_list = store.evidence_packages
            if isinstance(raw_list, list | tuple):
                packages = [p for p in raw_list if isinstance(p, dict)]
        return cls.from_packages(packages)
