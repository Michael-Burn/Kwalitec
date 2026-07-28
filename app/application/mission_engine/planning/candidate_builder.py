"""CandidateBuilder — deterministic MissionCandidateProjection construction.

Maps Twin decisions onto mission candidates using existing Adaptive Mission
prioritisation scoring. Never invents missing learner state or new heuristics.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.application.mission_engine.planning.versions import (
    PLANNING_PROVENANCE_PREFIX,
    PLANNING_VERSION,
)
from app.domain.adaptive_mission.prioritisation import (
    _recovery_for,
    _score_candidate,
)
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.mission.planning.activity_type import PlanningActivityType
from app.domain.mission.planning.candidate import MissionCandidateProjection
from app.domain.mission.planning.context import PlanningContext
from app.domain.mission.planning.reference import PlanningReference
from app.domain.reasoning.decisions.category import DecisionCategory
from app.domain.reasoning.decisions.decision import EducationalDecision
from app.domain.student_digital_twin.knowledge_gap import KnowledgeGap
from app.domain.student_digital_twin.recommendation import Recommendation
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin


class CandidateBuilder:
    """Build immutable mission candidates without inventing educational facts."""

    def __init__(
        self,
        *,
        context: PlanningContext,
        twin: StudentDigitalTwin,
        learning_graph: LearningGraph | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self._context = context
        self._twin = twin
        self._learning_graph = learning_graph
        self._created_at = created_at or datetime.now(UTC).replace(tzinfo=None)
        self._seen_ids: set[str] = set()
        self._gaps_by_concept = {g.concept_id: g for g in twin.knowledge_gaps}
        self._recs_by_concept = {
            (r.curriculum_entity_id or "").strip(): r
            for r in twin.recommendations
            if (r.status or "active") == "active"
            and (r.curriculum_entity_id or "").strip()
        }

    @property
    def context(self) -> PlanningContext:
        return self._context

    @property
    def seen_ids(self) -> frozenset[str]:
        return frozenset(self._seen_ids)

    def build_from_decision(
        self,
        decision: EducationalDecision,
    ) -> tuple[MissionCandidateProjection, ...]:
        """Derive zero or one mission candidate from one Twin decision.

        Soft / non-planning decisions yield an empty tuple (caller may emit
        MissionPlanningSkipped). Never invents gaps, mastery, or recommendations.
        """
        category = decision.category
        if category is DecisionCategory.MASTERY_BELIEF_UPDATE:
            return self._from_mastery(decision)
        if category is DecisionCategory.CONFIDENCE_BELIEF_UPDATE:
            return self._from_confidence(decision)
        if category is DecisionCategory.UNCERTAINTY_PRESERVED:
            return ()
        if category is DecisionCategory.PROVENANCE_RECORDED:
            return ()
        return ()

    def _from_mastery(
        self, decision: EducationalDecision
    ) -> tuple[MissionCandidateProjection, ...]:
        concept = (decision.reference.concept_reference or "").strip()
        if not concept:
            concept = (decision.subject_ref or "").strip()
        if not concept:
            return ()

        gap = self._gaps_by_concept.get(concept)
        rec = self._recs_by_concept.get(concept)
        tags = _string_list((decision.payload or {}).get("misconception_tags"))
        if not tags:
            tags = _string_list(
                (decision.provenance or {}).get("misconception_tags")
            )
        activity = (
            PlanningActivityType.RECOVERY
            if gap is not None or tags
            else PlanningActivityType.PRACTICE
        )
        return (
            self._build_candidate(
                decision=decision,
                concept_id=concept,
                activity_type=activity,
                gap=gap,
                recommendation=rec,
            ),
        )

    def _from_confidence(
        self, decision: EducationalDecision
    ) -> tuple[MissionCandidateProjection, ...]:
        lo = (decision.reference.learning_objective_reference or "").strip()
        concept = (decision.reference.concept_reference or "").strip()
        if not concept:
            concept = (decision.subject_ref or "").strip()
        # Confidence practice requires both concept (mission targeting) and LO.
        # Never invent missing refs — soft-skip incomplete decisions.
        if not concept or not lo:
            return ()

        gap = self._gaps_by_concept.get(concept)
        rec = self._recs_by_concept.get(concept)
        return (
            self._build_candidate(
                decision=decision,
                concept_id=concept,
                activity_type=PlanningActivityType.CONFIDENCE_PRACTICE,
                gap=gap,
                recommendation=rec,
                learning_objective_id=lo,
            ),
        )

    def _build_candidate(
        self,
        *,
        decision: EducationalDecision,
        concept_id: str,
        activity_type: PlanningActivityType,
        gap: KnowledgeGap | None,
        recommendation: Recommendation | None,
        learning_objective_id: str = "",
    ) -> MissionCandidateProjection:
        candidate_id = (
            f"mc:{self._context.twin_id}:{decision.decision_id}:"
            f"{activity_type.value}:{concept_id}"
        )
        if candidate_id in self._seen_ids:
            from app.domain.mission.planning.errors import DuplicateMissionRequest

            raise DuplicateMissionRequest(f"duplicate candidate: {candidate_id!r}")
        self._seen_ids.add(candidate_id)

        recovery = _recovery_for(concept_id, self._learning_graph)
        score = _score_candidate(
            recommendation=recommendation,
            gap=gap,
            learning_state=self._twin.learning_state,
            recovery=recovery,
            recently_studied=False,
        )
        title = (
            (gap.concept_title if gap and gap.concept_title else "")
            or (recommendation.title if recommendation and recommendation.title else "")
            or concept_id
        )
        lo = (
            learning_objective_id
            or (decision.reference.learning_objective_reference or "").strip()
        )
        evidence = tuple(
            dict.fromkeys(
                list(recommendation.supporting_evidence if recommendation else ())
                + list(gap.supporting_evidence if gap else ())
                + list(decision.reference.educational_observation_ids)
            )
        )
        reference = PlanningReference(
            decision_id=decision.decision_id,
            decision_version=decision.decision_version,
            twin_version=self._context.twin_version,
            evidence_bundle_id=decision.reference.evidence_bundle_id,
            educational_observation_ids=(
                decision.reference.educational_observation_ids
            ),
            reasoning_request_id=decision.reference.reasoning_request_id,
            assessment_session_id=decision.reference.assessment_session_id,
            correlation_id=decision.reference.correlation_id,
            planning_version=PLANNING_VERSION,
            twin_id=self._context.twin_id,
            learning_objective_reference=lo,
            concept_reference=concept_id,
            candidate_id=candidate_id,
        )
        provenance = {
            "prefix": PLANNING_PROVENANCE_PREFIX,
            "decision_id": decision.decision_id,
            "decision_version": decision.decision_version,
            "twin_version": self._context.twin_version,
            "evidence_bundle_id": decision.reference.evidence_bundle_id,
            "educational_observation_ids": list(
                decision.reference.educational_observation_ids
            ),
            "reasoning_request_id": decision.reference.reasoning_request_id,
            "assessment_session_id": decision.reference.assessment_session_id,
            "correlation_id": decision.reference.correlation_id,
            "planning_version": PLANNING_VERSION,
            "twin_id": self._context.twin_id,
            "activity_type": activity_type.value,
            "concept_id": concept_id,
        }
        return MissionCandidateProjection(
            candidate_id=candidate_id,
            activity_type=activity_type,
            concept_id=concept_id,
            concept_title=title,
            twin_id=self._context.twin_id,
            reference=reference,
            planning_version=PLANNING_VERSION,
            created_at=self._created_at,
            decision_id=decision.decision_id,
            priority_score=score.score,
            priority_band=score.priority.value,
            learning_objective_id=lo,
            twin_decision_ref=decision.decision_id,
            recommendation_id=(
                recommendation.recommendation_id if recommendation else ""
            ),
            gap_id=gap.gap_id if gap else "",
            recovery_path_concept_ids=(
                tuple(recovery.concept_ids) if recovery is not None else ()
            ),
            evidence_ids=evidence,
            priority_explanation=score.explanation,
            provenance=provenance,
            payload={
                "twin_decision_ref": decision.decision_id,
                "decision_category": decision.category.value,
                "decision_value": (
                    float(decision.value)
                    if isinstance(decision.value, int | float)
                    else str(decision.value)
                ),
            },
        )


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, list | tuple):
        out: list[str] = []
        for item in value:
            text = str(item or "").strip()
            if text and text not in out:
                out.append(text)
        return out
    return []
