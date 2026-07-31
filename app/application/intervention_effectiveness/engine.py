"""Educational Intervention Effectiveness Engine — EI Phase 4 (KWP-010).

Determines whether previous educational recommendations improved learning
from subsequent evidence. Produces natural student feedback and founder
outcome labels — never scores as product, never AI.

MUST NOT redesign Learning Strategy, Learning Diagnostics, Learning
Difficulty, LearningSessionRuntime, EducationalEvidenceAuthority,
StudentTwinEngine, ProgressEngine, Mission Runtime, Commercial Loop, or
Session FSM. Consumes their outputs only.
"""

from __future__ import annotations

import logging
from typing import Any

from app.application.intervention_effectiveness.dto import (
    EffectivenessEvidenceInput,
    InterventionEffectivenessReport,
    InterventionKind,
    PriorIntervention,
    prior_from_sitting,
)
from app.application.intervention_effectiveness.guidance import (
    explanation_for,
    feedback_for,
    scrub,
)
from app.application.intervention_effectiveness.rules import evaluate_effectiveness
from app.application.learning_difficulty.dto import LoadRecommendation
from app.application.learning_strategy.dto import StrategyAction

logger = logging.getLogger(__name__)


class InterventionEffectivenessEngine:
    """Evaluate whether a prior recommendation improved subsequent outcomes."""

    AUTHORITY_ID = "intervention_effectiveness_engine"

    def evaluate(
        self,
        evidence: EffectivenessEvidenceInput | dict[str, Any] | None = None,
        *,
        opaque: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        twin_signals: dict[str, Any] | None = None,
        cadence: dict[str, Any] | None = None,
        prior: PriorIntervention | None = None,
    ) -> InterventionEffectivenessReport:
        """Return a deterministic InterventionEffectivenessReport.

        Args:
            evidence: Pre-built EffectivenessEvidenceInput, or omit to build
                from opaque sitting facts + optional prior enrichment.
            opaque: Subsequent sitting / completion opaque summary.
            metadata: Completion metadata pairs / dict.
            twin_signals: Optional Twin-derived enrichments (read-only).
            cadence: Optional streak / prior_intervention enrichments.
            prior: Explicit PriorIntervention when known.

        Returns:
            InterventionEffectivenessReport with student-safe feedback.
        """
        if isinstance(evidence, EffectivenessEvidenceInput):
            inputs = evidence
            if prior is not None and not inputs.prior.has_recommendation:
                inputs = EffectivenessEvidenceInput(
                    prior=prior,
                    topic_title=inputs.topic_title,
                    practice_correct=inputs.practice_correct,
                    practice_incorrect=inputs.practice_incorrect,
                    practice_attempted=inputs.practice_attempted,
                    finish_verdict=inputs.finish_verdict,
                    progress_advanced=inputs.progress_advanced,
                    mission_completed=inputs.mission_completed,
                    has_reflection=inputs.has_reflection,
                    abandoned=inputs.abandoned,
                    reported_confidence=inputs.reported_confidence,
                    retention_risk=inputs.retention_risk,
                    weak_topic=inputs.weak_topic,
                    session_duration_minutes=inputs.session_duration_minutes,
                    days_since_topic_practice=inputs.days_since_topic_practice,
                    recovered_after_misses=inputs.recovered_after_misses,
                    consecutive_strong_sittings=inputs.consecutive_strong_sittings,
                    consecutive_partial_finishes=inputs.consecutive_partial_finishes,
                )
        else:
            merged_opaque = dict(opaque or {})
            if isinstance(evidence, dict):
                merged_opaque = {**merged_opaque, **evidence}
            inputs = EffectivenessEvidenceInput.from_opaque(
                merged_opaque,
                metadata=metadata,
                twin_signals=twin_signals,
                cadence=cadence,
                prior=prior,
            )

        decision = evaluate_effectiveness(inputs)
        feedback = scrub(feedback_for(decision, inputs))
        explanation = scrub(explanation_for(decision, inputs))

        report = InterventionEffectivenessReport(
            verdict=decision.verdict,
            intervention_kind=decision.intervention_kind,
            feedback=feedback,
            explanation=explanation,
            rule_id=decision.rule_id,
            evidence_codes=decision.evidence_codes,
            topic_title=inputs.topic_title or inputs.prior.topic_title,
            strategy_action=inputs.prior.strategy_action,
            load_recommendation=inputs.prior.load_recommendation,
            metadata=(
                ("authority", self.AUTHORITY_ID),
                ("rule_id", decision.rule_id),
                ("verdict", decision.verdict.value),
                ("kind", decision.intervention_kind.value),
            ),
        )
        logger.debug(
            "intervention_effectiveness rule=%s verdict=%s kind=%s topic=%r",
            decision.rule_id,
            decision.verdict.value,
            decision.intervention_kind.value,
            report.topic_title,
        )
        return report

    def evaluate_opaque(
        self,
        opaque_summary: dict[str, Any] | None,
        *,
        metadata: dict[str, Any] | None = None,
        twin_signals: dict[str, Any] | None = None,
        cadence: dict[str, Any] | None = None,
        prior: PriorIntervention | None = None,
    ) -> InterventionEffectivenessReport:
        """Convenience wrapper for Sitting Report / founder projectors."""
        return self.evaluate(
            opaque=opaque_summary,
            metadata=metadata,
            twin_signals=twin_signals,
            cadence=cadence,
            prior=prior,
        )

    def evaluate_pair(
        self,
        prior_opaque: dict[str, Any] | None,
        subsequent_opaque: dict[str, Any] | None,
        *,
        strategy_action: StrategyAction | str = "",
        load_recommendation: LoadRecommendation | str = "",
    ) -> InterventionEffectivenessReport:
        """Evaluate effectiveness from a prior sitting + subsequent sitting.

        When strategy/load are omitted, callers should pass the actions that
        were recommended on the prior sitting (from Strategy / Difficulty
        engines). This helper only builds the PriorIntervention baseline.
        """
        prior_raw = dict(prior_opaque or {})
        action = strategy_action or str(
            prior_raw.get("strategy_action")
            or prior_raw.get("recommended_strategy_action")
            or ""
        )
        load = load_recommendation or str(
            prior_raw.get("load_recommendation")
            or prior_raw.get("recommended_load_recommendation")
            or ""
        )
        prior = prior_from_sitting(
            strategy_action=action,
            load_recommendation=load,
            topic_title=str(prior_raw.get("topic_title") or ""),
            practice_correct=int(prior_raw.get("practice_correct") or 0),
            practice_incorrect=int(prior_raw.get("practice_incorrect") or 0),
            practice_attempted=int(prior_raw.get("practice_attempted") or 0),
            session_duration_minutes=_optional_int(
                prior_raw.get("session_duration_minutes")
                or prior_raw.get("actual_duration_minutes")
            ),
            finish_verdict=str(
                (prior_raw.get("finish_review") or {}).get("verdict")
                if isinstance(prior_raw.get("finish_review"), dict)
                else prior_raw.get("finish_verdict")
                or ""
            ),
            progress_advanced=bool(prior_raw.get("progress_advanced")),
            source="pair",
        )
        if not prior.has_recommendation:
            # Lawful empty pair — insufficient evidence.
            return self.evaluate(
                opaque=subsequent_opaque,
                prior=PriorIntervention(kind=InterventionKind.OTHER),
            )
        return self.evaluate(opaque=subsequent_opaque, prior=prior)


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


_DEFAULT_ENGINE: InterventionEffectivenessEngine | None = None


def get_intervention_effectiveness_engine() -> InterventionEffectivenessEngine:
    """Process-scoped default engine instance."""
    global _DEFAULT_ENGINE
    if _DEFAULT_ENGINE is None:
        _DEFAULT_ENGINE = InterventionEffectivenessEngine()
    return _DEFAULT_ENGINE
