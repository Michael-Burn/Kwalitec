"""Adaptive Decision Engine diagnostics — integrity inspection without mutation."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.adaptive_learning.policies.intervention_policy import (
    InterventionPolicy,
)
from app.application.adaptive_learning.policies.priority_policy import PriorityPolicy
from app.domain.adaptive_learning.adaptive_decision import AdaptiveDecision
from app.domain.adaptive_learning.intervention_type import InterventionType


@dataclass(frozen=True)
class AdaptiveDiagnosticsReport:
    """Immutable diagnostics over an adaptive decision."""

    decision_id: str
    learner_id: str
    intervention_type: str
    has_intervention: bool
    priority_score: float
    estimated_study_minutes: float
    revision_intervention_count: int
    explanation_complete: bool
    phase1_compliant: bool
    issues: tuple[str, ...] = field(default_factory=tuple)
    engine_id: str = "adaptive_decision"
    engine_version: str = "1.0.0"


class AdaptiveDiagnostics:
    """Framework-independent adaptive decision health / integrity diagnostics."""

    @staticmethod
    def inspect(decision: AdaptiveDecision) -> AdaptiveDiagnosticsReport:
        """Inspect decision integrity without mutating state."""
        issues: list[str] = []
        explanation = decision.explanation
        explanation_complete = bool(
            explanation.rationale and explanation.expected_educational_benefit
        )
        if not explanation_complete:
            issues.append("explanation_incomplete")
        if decision.has_intervention and not explanation.evidence_considered:
            issues.append("missing_evidence_considered")
        if decision.intervention_type is not InterventionType.REVISION:
            issues.append("non_revision_phase1_violation")
        if (
            decision.selected_intervention is not None
            and not InterventionPolicy.is_supported(
                decision.selected_intervention.intervention_type
            )
        ):
            issues.append("unsupported_intervention_type")
        if (
            decision.has_intervention
            and decision.priority_score < PriorityPolicy.MIN_REVISION_PRIORITY
        ):
            issues.append("priority_below_revision_threshold")
        for intervention in decision.revision_plan.interventions:
            if not intervention.explanation.rationale:
                issues.append(
                    f"intervention_missing_rationale:{intervention.intervention_id}"
                )
        return AdaptiveDiagnosticsReport(
            decision_id=decision.decision_id,
            learner_id=decision.learner_id,
            intervention_type=decision.intervention_type.value,
            has_intervention=decision.has_intervention,
            priority_score=decision.priority_score,
            estimated_study_minutes=decision.estimated_study_minutes,
            revision_intervention_count=decision.revision_plan.intervention_count,
            explanation_complete=explanation_complete,
            phase1_compliant="non_revision_phase1_violation" not in issues,
            issues=tuple(issues),
        )
