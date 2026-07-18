"""Decision snapshot — immutable point-in-time adaptive decision projection."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.adaptive_learning.adaptive_decision import AdaptiveDecision
from app.domain.adaptive_learning.intervention_type import InterventionType
from app.domain.adaptive_learning.revision_plan import RevisionPlan
from app.domain.student_twin.confidence_band import ConfidenceBand


@dataclass(frozen=True)
class DecisionSnapshot:
    """Immutable projection of an AdaptiveDecision for consumers / tests.

    Snapshots are never mutated. New decisions produce new snapshots.
    """

    decision_id: str
    learner_id: str
    captured_at: datetime
    intervention_type: InterventionType
    topic_id: str | None
    priority_score: float
    educational_benefit: float
    estimated_study_minutes: float
    confidence: ConfidenceBand
    rationale: str
    expected_benefit: str
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    twin_version_label: str = ""
    revision_plan_id: str = ""
    alternative_topic_ids: tuple[str, ...] = field(default_factory=tuple)
    cost_benefit_ratio: float = 0.0
    return_on_study_time: float = 0.0

    @classmethod
    def from_decision(cls, decision: AdaptiveDecision) -> DecisionSnapshot:
        """Project an AdaptiveDecision into an immutable snapshot."""
        return cls.create(
            decision_id=decision.decision_id,
            learner_id=decision.learner_id,
            captured_at=decision.decided_at,
            intervention_type=decision.intervention_type,
            topic_id=decision.primary_topic_id,
            priority_score=decision.priority_score,
            educational_benefit=decision.roi.educational_benefit,
            estimated_study_minutes=decision.estimated_study_minutes,
            confidence=decision.confidence,
            rationale=decision.explanation.rationale,
            expected_benefit=decision.explanation.expected_educational_benefit,
            evidence_ids=(
                decision.evidence_ids or decision.explanation.evidence_considered
            ),
            twin_version_label=decision.twin_version_label,
            revision_plan_id=decision.revision_plan.plan_id,
            alternative_topic_ids=decision.alternative_topic_ids,
            cost_benefit_ratio=decision.roi.cost_benefit_ratio,
            return_on_study_time=decision.roi.return_on_study_time,
        )

    @classmethod
    def create(
        cls,
        *,
        decision_id: str,
        learner_id: str,
        captured_at: datetime,
        intervention_type: InterventionType | str = InterventionType.REVISION,
        topic_id: str | None = None,
        priority_score: float = 0.0,
        educational_benefit: float = 0.0,
        estimated_study_minutes: float = 0.0,
        confidence: ConfidenceBand | str = ConfidenceBand.VERY_LOW,
        rationale: str = "",
        expected_benefit: str = "",
        evidence_ids: list[str] | tuple[str, ...] | None = None,
        twin_version_label: str = "",
        revision_plan_id: str = "",
        alternative_topic_ids: list[str] | tuple[str, ...] | None = None,
        cost_benefit_ratio: float = 0.0,
        return_on_study_time: float = 0.0,
    ) -> DecisionSnapshot:
        """Construct a DecisionSnapshot."""
        did = _require_non_empty(decision_id, "decision_id")
        lid = _require_non_empty(learner_id, "learner_id")
        if not isinstance(captured_at, datetime):
            raise ValueError("captured_at must be a datetime")
        when = captured_at if captured_at.tzinfo else captured_at.replace(tzinfo=UTC)
        itype = (
            intervention_type
            if isinstance(intervention_type, InterventionType)
            else InterventionType(str(intervention_type).strip().lower())
        )
        band = (
            confidence
            if isinstance(confidence, ConfidenceBand)
            else ConfidenceBand(str(confidence).strip().lower())
        )
        return cls(
            decision_id=did,
            learner_id=lid,
            captured_at=when,
            intervention_type=itype,
            topic_id=topic_id.strip() if topic_id else None,
            priority_score=_unit_interval(priority_score, "priority_score"),
            educational_benefit=_unit_interval(
                educational_benefit, "educational_benefit"
            ),
            estimated_study_minutes=_non_negative(
                estimated_study_minutes, "estimated_study_minutes"
            ),
            confidence=band,
            rationale=(rationale or "").strip(),
            expected_benefit=(expected_benefit or "").strip(),
            evidence_ids=tuple(evidence_ids or ()),
            twin_version_label=(twin_version_label or "").strip(),
            revision_plan_id=(revision_plan_id or "").strip(),
            alternative_topic_ids=tuple(alternative_topic_ids or ()),
            cost_benefit_ratio=_non_negative(
                cost_benefit_ratio, "cost_benefit_ratio"
            ),
            return_on_study_time=_non_negative(
                return_on_study_time, "return_on_study_time"
            ),
        )

    @property
    def has_revision_plan(self) -> bool:
        """True when a revision plan id is present."""
        return bool(self.revision_plan_id)

    @property
    def is_actionable(self) -> bool:
        """True when a topic and positive priority are present."""
        return self.topic_id is not None and self.priority_score > 0.0


# Re-export RevisionPlan for snapshot consumers that need plan attachment.
__all__ = ["DecisionSnapshot", "RevisionPlan"]


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _unit_interval(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a number in [0, 1]")
    numeric = float(value)
    if numeric < 0.0 or numeric > 1.0:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric


def _non_negative(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a non-negative number")
    numeric = float(value)
    if numeric < 0.0:
        raise ValueError(f"{field_name} must be a non-negative number")
    return numeric
