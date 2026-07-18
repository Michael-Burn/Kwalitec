"""Adaptive decision — top-level recommendation from the decision engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.adaptive_learning.decision_explanation import DecisionExplanation
from app.domain.adaptive_learning.educational_roi import EducationalROI
from app.domain.adaptive_learning.intervention import Intervention
from app.domain.adaptive_learning.intervention_type import InterventionType
from app.domain.adaptive_learning.revision_plan import RevisionPlan
from app.domain.student_twin.confidence_band import ConfidenceBand


@dataclass(frozen=True)
class AdaptiveDecision:
    """Highest educational-value intervention recommended for a learner.

    Phase 1 always selects REVISION when revision candidates exist; otherwise
    produces an empty revision plan with an explainable no-op rationale.
    """

    decision_id: str
    learner_id: str
    decided_at: datetime
    selected_intervention: Intervention | None
    intervention_type: InterventionType
    revision_plan: RevisionPlan
    priority_score: float
    roi: EducationalROI
    explanation: DecisionExplanation
    estimated_study_minutes: float
    confidence: ConfidenceBand
    twin_version_label: str = ""
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    alternative_topic_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        decision_id: str,
        learner_id: str,
        decided_at: datetime,
        *,
        selected_intervention: Intervention | None,
        revision_plan: RevisionPlan | None = None,
        explanation: DecisionExplanation,
        twin_version_label: str = "",
        evidence_ids: list[str] | tuple[str, ...] | None = None,
        alternative_topic_ids: list[str] | tuple[str, ...] | None = None,
    ) -> AdaptiveDecision:
        """Construct an AdaptiveDecision."""
        did = _require_non_empty(decision_id, "decision_id")
        lid = _require_non_empty(learner_id, "learner_id")
        if not isinstance(decided_at, datetime):
            raise ValueError("decided_at must be a datetime")
        when = decided_at if decided_at.tzinfo else decided_at.replace(tzinfo=UTC)
        plan = revision_plan if revision_plan is not None else RevisionPlan.empty()
        if selected_intervention is not None:
            itype = selected_intervention.intervention_type
            priority = selected_intervention.priority_score
            roi = selected_intervention.roi
            minutes = selected_intervention.estimated_study_minutes
            conf = selected_intervention.confidence
        else:
            itype = InterventionType.REVISION
            priority = 0.0
            roi = EducationalROI.zero()
            minutes = 0.0
            conf = explanation.confidence
        return cls(
            decision_id=did,
            learner_id=lid,
            decided_at=when,
            selected_intervention=selected_intervention,
            intervention_type=itype,
            revision_plan=plan,
            priority_score=priority,
            roi=roi,
            explanation=explanation,
            estimated_study_minutes=minutes,
            confidence=conf,
            twin_version_label=(twin_version_label or "").strip(),
            evidence_ids=tuple(evidence_ids or ()),
            alternative_topic_ids=tuple(alternative_topic_ids or ()),
        )

    @property
    def has_intervention(self) -> bool:
        """True when a concrete intervention was selected."""
        return self.selected_intervention is not None

    @property
    def primary_topic_id(self) -> str | None:
        """Primary topic from the selected intervention or revision plan."""
        if self.selected_intervention is not None:
            return self.selected_intervention.topic_id
        return self.revision_plan.primary_topic_id

    @property
    def is_revision_decision(self) -> bool:
        """True when the decision type is REVISION."""
        return self.intervention_type is InterventionType.REVISION


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
