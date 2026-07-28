"""Consistency checks for learner Educational Intelligence state (LP-001).

Detects incomplete derived state so recovery can re-invoke EI services.
Does not invent educational values.
"""

from __future__ import annotations

from app.application.learner_lifecycle.dto import ConsistencyReport
from app.models.educational_reasoning_engine import EreEducationalDecision
from app.models.student_curriculum_binding import (
    SciCurriculumNodeState,
    SciStudentCurriculumInstance,
)
from app.models.twin_inference import TieNodeBelief


class LifecycleConsistencyService:
    """Report whether an SCI has complete pipeline-derived state."""

    def inspect(self, instance_id: str) -> ConsistencyReport:
        instance = SciStudentCurriculumInstance.query.filter_by(
            instance_id=instance_id
        ).first()
        if instance is None:
            return ConsistencyReport(
                instance_id=instance_id,
                has_instance=False,
                node_state_count=0,
                belief_count=0,
                decision_count=0,
                is_complete=False,
                missing=("instance",),
            )

        node_count = SciCurriculumNodeState.query.filter_by(
            instance_id=instance_id
        ).count()
        belief_count = TieNodeBelief.query.filter_by(instance_id=instance_id).count()
        decision_count = EreEducationalDecision.query.filter_by(
            instance_id=instance_id
        ).count()

        missing: list[str] = []
        if node_count < 1:
            missing.append("node_states")
        if belief_count < 1:
            missing.append("twin_beliefs")
        if decision_count < 1:
            missing.append("educational_decisions")

        return ConsistencyReport(
            instance_id=instance_id,
            has_instance=True,
            node_state_count=node_count,
            belief_count=belief_count,
            decision_count=decision_count,
            is_complete=not missing,
            missing=tuple(missing),
        )
