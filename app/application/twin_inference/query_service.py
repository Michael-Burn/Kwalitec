"""Read-side queries for Twin beliefs and explanations (EI-006)."""

from __future__ import annotations

from app.application.twin_inference.dto import BeliefView, KnowledgeStateView
from app.application.twin_inference.exceptions import (
    BeliefNotFoundError,
    InstanceNotFoundError,
)
from app.application.twin_inference.inference_service import BeliefInferenceService
from app.domain.twin_inference.knowledge_state import aggregate_knowledge_state
from app.models.student_curriculum_binding import SciStudentCurriculumInstance
from app.models.twin_inference import TieNodeBelief


class BeliefQueryService:
    """Retrieve explainable Twin belief summaries without re-inference."""

    def get_node_belief(
        self,
        instance_id: str,
        node_stable_id: str,
    ) -> BeliefView:
        """Return persisted belief + explanation for one node."""
        self._require_instance(instance_id)
        row = TieNodeBelief.query.filter_by(
            instance_id=instance_id,
            node_stable_id=node_stable_id,
        ).first()
        if row is None:
            raise BeliefNotFoundError(
                f"No belief for node {node_stable_id} in instance {instance_id}"
            )
        return BeliefInferenceService._row_to_view(row)

    def list_beliefs(self, instance_id: str) -> tuple[BeliefView, ...]:
        """All beliefs for an SCI, ordered by node stable id."""
        self._require_instance(instance_id)
        rows = (
            TieNodeBelief.query.filter_by(instance_id=instance_id)
            .order_by(TieNodeBelief.node_stable_id.asc())
            .all()
        )
        return tuple(BeliefInferenceService._row_to_view(row) for row in rows)

    def get_explainable_summary(
        self,
        instance_id: str,
        node_stable_id: str,
    ) -> dict:
        """Compact explainable summary for one node belief."""
        view = self.get_node_belief(instance_id, node_stable_id)
        return {
            "node_stable_id": view.belief.node_stable_id,
            "mastery_level": view.belief.mastery_level,
            "confidence_score": view.belief.confidence_score,
            "learning_state": view.belief.learning_state,
            "rationale_summary": view.belief.rationale_summary,
            "supporting_evidence_ids": list(view.belief.supporting_evidence_ids),
            "contributing_rule_ids": sorted(
                {r.rule_id for r in view.explanation.contributing_rules}
            ),
            "confidence_calculation": view.explanation.confidence_calculation.to_dict(),
            "inference_version": view.belief.inference_version,
            "inference_timestamp": view.belief.inference_timestamp.isoformat(),
            "learning_state_reason": view.explanation.learning_state_reason,
        }

    def get_knowledge_state(self, instance_id: str) -> KnowledgeStateView:
        """Subject knowledge state from persisted beliefs (no rebuild)."""
        instance = self._require_instance(instance_id)
        rows = (
            TieNodeBelief.query.filter_by(instance_id=instance_id)
            .order_by(TieNodeBelief.node_stable_id.asc())
            .all()
        )
        views = tuple(BeliefInferenceService._row_to_view(row) for row in rows)
        inferred_at = (
            max(v.belief.inference_timestamp for v in views)
            if views
            else instance.updated_at
        )
        version = views[0].belief.inference_version if views else "tie.v1"
        state = aggregate_knowledge_state(
            instance_id=instance_id,
            subject_code=instance.subject_code,
            beliefs=[v.belief for v in views],
            inferred_at=inferred_at,
            inference_version=version,
        )
        return KnowledgeStateView(state=state, node_summaries=views)

    @staticmethod
    def _require_instance(instance_id: str) -> SciStudentCurriculumInstance:
        instance = SciStudentCurriculumInstance.query.filter_by(
            instance_id=instance_id
        ).first()
        if instance is None:
            raise InstanceNotFoundError(f"Instance not found: {instance_id}")
        return instance
