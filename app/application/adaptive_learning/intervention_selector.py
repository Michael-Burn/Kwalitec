"""Intervention selector — pick the highest educational-value intervention."""

from __future__ import annotations

from app.application.adaptive_learning.policies.intervention_policy import (
    InterventionPolicy,
)
from app.application.adaptive_learning.policies.priority_policy import PriorityPolicy
from app.domain.adaptive_learning.decision_explanation import DecisionExplanation
from app.domain.adaptive_learning.intervention import Intervention
from app.domain.adaptive_learning.intervention_type import InterventionType
from app.domain.adaptive_learning.revision_candidate import RevisionCandidate
from app.domain.adaptive_learning.revision_plan import RevisionPlan
from app.domain.adaptive_learning.revision_window import RevisionWindow


class InterventionSelector:
    """Select Phase-1 REVISION interventions from ranked candidates.

    Future phases may select CONTINUE / REPEAT / ASSESS / BREAK / SKIP
    without redesigning this architecture.
    """

    @staticmethod
    def select_revision(
        candidates: list[RevisionCandidate] | tuple[RevisionCandidate, ...],
        *,
        windows: list[RevisionWindow] | tuple[RevisionWindow, ...] | None = None,
        plan_id: str = "plan-1",
        id_prefix: str = "rev",
    ) -> tuple[Intervention | None, RevisionPlan]:
        """Select top revision interventions and build a RevisionPlan."""
        InterventionPolicy.assert_supported(InterventionType.REVISION)
        ordered = sorted(candidates, key=lambda c: c.ranking_key)
        if not InterventionPolicy.should_recommend_revision(
            candidate_count=len(ordered),
            top_priority=ordered[0].priority.score if ordered else 0.0,
            min_priority=PriorityPolicy.MIN_REVISION_PRIORITY,
        ):
            return None, RevisionPlan.empty(plan_id)

        selected_candidates = ordered[: InterventionPolicy.max_interventions()]
        interventions: list[Intervention] = []
        for index, candidate in enumerate(selected_candidates):
            explanation = DecisionExplanation.create(
                evidence_considered=candidate.evidence_ids,
                rationale=candidate.rationale or "revision_selected",
                priority=candidate.priority,
                expected_educational_benefit=_benefit_phrase(candidate),
                confidence=candidate.confidence,
                detail_lines=(
                    f"retention_score={candidate.retention_score:.3f}",
                    f"mastery_score={candidate.mastery_score:.3f}",
                    f"roi_benefit={candidate.roi.educational_benefit:.3f}",
                ),
            )
            interventions.append(
                Intervention.create(
                    f"{id_prefix}-{index}-{candidate.topic_id}",
                    InterventionType.REVISION,
                    topic_id=candidate.topic_id,
                    priority=candidate.priority,
                    roi=candidate.roi,
                    explanation=explanation,
                    estimated_study_minutes=candidate.roi.estimated_study_minutes,
                    confidence=candidate.confidence,
                )
            )

        plan = RevisionPlan.create(
            plan_id,
            interventions=interventions,
            candidates=ordered,
            windows=windows or (),
            primary_topic_id=interventions[0].topic_id if interventions else None,
        )
        return interventions[0], plan

    @staticmethod
    def select(
        candidates: list[RevisionCandidate] | tuple[RevisionCandidate, ...],
        *,
        preferred_type: InterventionType | str = InterventionType.REVISION,
        windows: list[RevisionWindow] | tuple[RevisionWindow, ...] | None = None,
        plan_id: str = "plan-1",
    ) -> tuple[Intervention | None, RevisionPlan]:
        """Select an intervention of the preferred type (Phase 1: REVISION)."""
        InterventionPolicy.assert_supported(preferred_type)
        return InterventionSelector.select_revision(
            candidates,
            windows=windows,
            plan_id=plan_id,
        )


def _benefit_phrase(candidate: RevisionCandidate) -> str:
    if candidate.retention_risk >= 0.55:
        return "improve_long_term_retention"
    if candidate.mastery_gap >= 0.55:
        return "raise_demonstrated_mastery"
    if candidate.struggle_score >= 0.55:
        return "reduce_historical_struggle"
    return "consolidate_topic_readiness"
