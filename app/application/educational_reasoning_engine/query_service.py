"""Read-side queries for educational decisions and explanations (EI-007)."""

from __future__ import annotations

from app.application.educational_reasoning_engine.dto import DecisionView
from app.application.educational_reasoning_engine.exceptions import (
    DecisionNotFoundError,
    InstanceNotFoundError,
)
from app.application.educational_reasoning_engine.reasoning_service import (
    DecisionReasoningService,
)
from app.models.educational_reasoning_engine import EreEducationalDecision
from app.models.student_curriculum_binding import SciStudentCurriculumInstance


class DecisionQueryService:
    """Retrieve explainable educational decision summaries without re-reasoning."""

    def get_decision(self, decision_id: str) -> DecisionView:
        """Return persisted decision + explanation by id."""
        row = EreEducationalDecision.query.filter_by(decision_id=decision_id).first()
        if row is None:
            raise DecisionNotFoundError(f"Decision not found: {decision_id}")
        return DecisionReasoningService._row_to_view(row)

    def list_decisions(self, instance_id: str) -> tuple[DecisionView, ...]:
        """All decisions for an SCI, ordered by rank position."""
        self._require_instance(instance_id)
        rows = (
            EreEducationalDecision.query.filter_by(instance_id=instance_id)
            .order_by(
                EreEducationalDecision.rank_position.asc(),
                EreEducationalDecision.curriculum_target.asc(),
            )
            .all()
        )
        return tuple(DecisionReasoningService._row_to_view(row) for row in rows)

    def get_explainable_summary(self, decision_id: str) -> dict:
        """Compact explainable summary for one educational decision."""
        view = self.get_decision(decision_id)
        return {
            "decision_id": view.decision.decision_id,
            "decision_type": view.decision.decision_type,
            "curriculum_target": view.decision.curriculum_target,
            "priority": view.decision.priority,
            "rank_position": view.decision.rank_position,
            "rationale_summary": view.decision.rationale_summary,
            "prerequisite_chain": list(view.decision.prerequisite_chain),
            "estimated_effort_minutes": view.decision.estimated_effort_minutes,
            "expected_educational_outcome": (
                view.decision.expected_educational_outcome
            ),
            "contributing_beliefs": list(view.explanation.contributing_beliefs),
            "curriculum_dependencies": list(
                view.explanation.curriculum_dependencies
            ),
            "educational_rules_applied": list(
                view.explanation.educational_rules_applied
            ),
            "evidence_references": list(view.explanation.evidence_references),
            "priority_calculation": view.explanation.priority_calculation.to_dict(),
            "reasoning_version": view.decision.reasoning_version,
            "reasoned_at": view.decision.reasoned_at.isoformat(),
        }

    def highest_value_actions(
        self, instance_id: str, *, limit: int = 5
    ) -> tuple[DecisionView, ...]:
        """Top-N ranked educational decisions for an SCI."""
        decisions = self.list_decisions(instance_id)
        if limit < 1:
            return ()
        return decisions[:limit]

    @staticmethod
    def _require_instance(instance_id: str) -> SciStudentCurriculumInstance:
        instance = SciStudentCurriculumInstance.query.filter_by(
            instance_id=instance_id
        ).first()
        if instance is None:
            raise InstanceNotFoundError(f"Instance not found: {instance_id}")
        return instance
