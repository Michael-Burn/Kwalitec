"""Learning Strategy Engine — Educational Intelligence Phase 1 (KWP-007).

Deterministic educational reasoning over existing sitting / Progress / Twin
signals. Produces recommendations with WHY — never scores, never AI.

MUST NOT redesign LearningSessionRuntime, EducationalEvidenceAuthority,
StudentTwinEngine, ProgressEngine, Mission Runtime, Commercial Loop, or
Session FSM. Consumes their outputs only.
"""

from __future__ import annotations

import logging
from typing import Any

from app.application.learning_strategy.calibration import guidance_for
from app.application.learning_strategy.dto import (
    LearningStrategyAdvice,
    StrategyEvidenceInput,
)
from app.application.learning_strategy.explainability import (
    explanation_for,
    recommendation_body,
    title_for,
)
from app.application.learning_strategy.momentum import derive_momentum
from app.application.learning_strategy.rules import select_strategy
from app.application.learning_strategy.spacing import decide_spacing

logger = logging.getLogger(__name__)


class LearningStrategyEngine:
    """Compose educational strategy from existing evidence outputs."""

    AUTHORITY_ID = "learning_strategy_engine"

    def evaluate(
        self,
        evidence: StrategyEvidenceInput | dict[str, Any] | None = None,
        *,
        opaque: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        twin_signals: dict[str, Any] | None = None,
        cadence: dict[str, Any] | None = None,
    ) -> LearningStrategyAdvice:
        """Return a deterministic LearningStrategyAdvice.

        Args:
            evidence: Pre-built StrategyEvidenceInput, or omit to build from
                opaque sitting facts.
            opaque: Sitting / completion opaque summary.
            metadata: Completion metadata pairs / dict.
            twin_signals: Optional Twin-derived enrichments (read-only).
            cadence: Optional streak / session-count enrichments.

        Returns:
            LearningStrategyAdvice with student-safe recommendation + WHY.
        """
        if isinstance(evidence, StrategyEvidenceInput):
            inputs = evidence
        else:
            merged_opaque = dict(opaque or {})
            if isinstance(evidence, dict):
                merged_opaque = {**merged_opaque, **evidence}
            inputs = StrategyEvidenceInput.from_opaque(
                merged_opaque,
                metadata=metadata,
                twin_signals=twin_signals,
                cadence=cadence,
            )

        decision = select_strategy(inputs)
        spacing, spacing_guidance = decide_spacing(
            inputs, action=decision.action
        )
        momentum, momentum_guidance = derive_momentum(inputs)
        title = title_for(decision.action)
        body = recommendation_body(decision, inputs)
        why = explanation_for(decision, inputs)
        confidence_guidance = guidance_for(
            decision.calibration, topic=inputs.topic_title or "this topic"
        )

        advice = LearningStrategyAdvice(
            action=decision.action,
            recommendation_title=title,
            recommendation_body=body,
            explanation=why,
            spacing=spacing,
            spacing_guidance=spacing_guidance,
            momentum=momentum,
            momentum_guidance=momentum_guidance,
            confidence_guidance=confidence_guidance,
            rule_id=decision.rule_id,
            reason_codes=decision.reason_codes,
            calibration=decision.calibration,
            topic_title=inputs.topic_title,
            metadata=(
                ("authority", self.AUTHORITY_ID),
                ("rule_id", decision.rule_id),
                ("action", decision.action.value),
                ("spacing", spacing.value),
                ("momentum", momentum.value),
            ),
        )
        logger.debug(
            "learning_strategy rule=%s action=%s topic=%r",
            decision.rule_id,
            decision.action.value,
            inputs.topic_title,
        )
        return advice

    def evaluate_opaque(
        self,
        opaque_summary: dict[str, Any] | None,
        *,
        metadata: dict[str, Any] | None = None,
        twin_signals: dict[str, Any] | None = None,
        cadence: dict[str, Any] | None = None,
        next_recommendation: str = "",
    ) -> LearningStrategyAdvice:
        """Convenience wrapper for Sitting Report / Home projectors."""
        opaque = dict(opaque_summary or {})
        if next_recommendation and not opaque.get("next_recommendation"):
            opaque["next_recommendation"] = next_recommendation
        return self.evaluate(
            opaque=opaque,
            metadata=metadata,
            twin_signals=twin_signals,
            cadence=cadence,
        )


_DEFAULT_ENGINE: LearningStrategyEngine | None = None


def get_learning_strategy_engine() -> LearningStrategyEngine:
    """Process-scoped default engine instance."""
    global _DEFAULT_ENGINE
    if _DEFAULT_ENGINE is None:
        _DEFAULT_ENGINE = LearningStrategyEngine()
    return _DEFAULT_ENGINE
