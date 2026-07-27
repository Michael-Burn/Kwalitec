"""Prediction scaffolding — framework only for SDT-001."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime

from app.domain.student_digital_twin.learning_state import LearningState
from app.domain.student_digital_twin.mastery import MasteryMap
from app.domain.student_digital_twin.prediction import Prediction, PredictionKind


class PredictionService:
    """Persist prediction scaffolds with deterministic placeholder values.

    Full prediction algorithms are deferred to later milestones.
    """

    def scaffold(
        self,
        *,
        twin_id: str,
        learning_state: LearningState,
        mastery: MasteryMap,
        observation_ids: tuple[str, ...] = (),
    ) -> tuple[Prediction, ...]:
        now = datetime.now(UTC).replace(tzinfo=None)
        evidence = tuple(observation_ids[:8])
        avg_mastery = (
            sum(r.mastery_score for r in mastery.records) / len(mastery.records)
            if mastery.records
            else 0.0
        )
        readiness = learning_state.exam_readiness
        growth = min(1.0, max(0.0, (1.0 - avg_mastery) * learning_state.momentum))
        goal_likelihood = min(1.0, 0.5 * readiness + 0.5 * learning_state.consistency)

        kinds = (
            (
                PredictionKind.ESTIMATED_READINESS,
                readiness,
                "exam_readiness_dimension",
                30,
            ),
            (
                PredictionKind.LIKELIHOOD_OF_GOAL_COMPLETION,
                goal_likelihood,
                "readiness_consistency_blend",
                60,
            ),
            (
                PredictionKind.EXPECTED_MASTERY_GROWTH,
                growth,
                "residual_mastery_times_momentum",
                14,
            ),
        )
        predictions: list[Prediction] = []
        for kind, value, reason, horizon in kinds:
            predictions.append(
                Prediction(
                    prediction_id=self._pred_id(twin_id, kind.value),
                    twin_id=twin_id,
                    kind=kind,
                    value=round(value, 4),
                    confidence=round(
                        min(0.7, 0.25 + 0.05 * learning_state.evidence_count), 4
                    ),
                    horizon_days=horizon,
                    supporting_evidence=evidence,
                    reason=f"framework_scaffold:{reason}",
                    created_at=now,
                    algorithm_version="sdt001.scaffold_v1",
                )
            )
        return tuple(predictions)

    @staticmethod
    def _pred_id(twin_id: str, kind: str) -> str:
        digest = hashlib.sha256(f"pred:{twin_id}:{kind}".encode()).hexdigest()[:16]
        return f"pred-{digest}"
