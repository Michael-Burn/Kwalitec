"""Learning-state derivation — composed from Educational Reasoning rules."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from app.domain.educational_reasoning.confidence_update import ConfidenceAdjustmentRule
from app.domain.educational_reasoning.consistency_rule import ConsistencyRule
from app.domain.educational_reasoning.momentum_rule import LearningMomentumRule
from app.domain.educational_reasoning.readiness_rule import ReadinessContributionRule
from app.domain.educational_reasoning.reasoning_context import (
    CurriculumEvidenceBundle,
    ReasoningContext,
)
from app.domain.student_digital_twin.learning_state import LearningState
from app.domain.student_digital_twin.mastery import MasteryMap
from app.domain.student_digital_twin.observation import Observation


class LearningStateService:
    """Compute multi-dimensional learning state via SDT-002 rules."""

    def compute(
        self,
        *,
        observations: tuple[Observation, ...],
        mastery: MasteryMap,
        snapshot_id: str | None = None,
        computed_at: datetime | None = None,
    ) -> LearningState:
        when = computed_at or datetime.now(UTC).replace(tzinfo=None)
        n = len(observations)
        if n == 0:
            return LearningState.empty(
                snapshot_id=snapshot_id or f"lss-{uuid.uuid4().hex[:12]}",
                computed_at=when,
            )

        scores = [r.mastery_score for r in mastery.records]
        knowledge = round(sum(scores) / len(scores), 4) if scores else 0.0

        context = ReasoningContext(
            twin_id="learning-state",
            student_id="learning-state",
            workspace_id="",
            subject_code="",
            observations=observations,
            observation_ids=tuple(o.observation_id for o in observations),
            prior_mastery=mastery,
            curriculum_evidence=CurriculumEvidenceBundle.empty(),
            triggered_by="learning_state_service",
            computed_at=when,
            mastery=mastery,
            knowledge=knowledge,
        )

        conf_ex = ConfidenceAdjustmentRule().apply(context)
        context = context.with_updates(
            confidence=conf_ex.confidence,
        )
        mom_ex = LearningMomentumRule().apply(context)
        context = context.with_updates(momentum=mom_ex.momentum)
        con_ex = ConsistencyRule().apply(context)
        context = context.with_updates(consistency=con_ex.consistency)
        rdy_ex = ReadinessContributionRule().apply(context)

        sid = snapshot_id or str(
            rdy_ex.outputs.get("snapshot_id") or f"lss-{uuid.uuid4().hex[:12]}"
        )
        return LearningState(
            knowledge=knowledge,
            confidence=conf_ex.confidence.score if conf_ex.confidence else 0.0,
            retention=rdy_ex.retention if rdy_ex.retention is not None else 0.0,
            consistency=con_ex.consistency if con_ex.consistency is not None else 0.0,
            momentum=mom_ex.momentum if mom_ex.momentum is not None else 0.0,
            exam_readiness=(
                rdy_ex.exam_readiness if rdy_ex.exam_readiness is not None else 0.0
            ),
            snapshot_id=sid,
            computed_at=when,
            evidence_count=n,
            reason="educational_reasoning_engine_v1",
        )
