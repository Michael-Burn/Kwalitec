"""Shared helpers for Adaptive Decision Engine domain tests."""

from __future__ import annotations

from datetime import UTC, datetime

from app.domain.adaptive_learning.decision_explanation import DecisionExplanation
from app.domain.adaptive_learning.educational_roi import EducationalROI
from app.domain.adaptive_learning.intervention import Intervention
from app.domain.adaptive_learning.intervention_priority import InterventionPriority
from app.domain.adaptive_learning.intervention_type import InterventionType
from app.domain.adaptive_learning.revision_candidate import RevisionCandidate
from app.domain.adaptive_learning.revision_plan import RevisionPlan
from app.domain.adaptive_learning.revision_window import RevisionWindow
from app.domain.student_twin.confidence_band import ConfidenceBand


def make_explanation(
    *,
    rationale: str = "test_rationale",
    priority: float = 0.5,
    benefit: str = "improve_long_term_retention",
    confidence: str = "medium",
    evidence: list[str] | None = None,
) -> DecisionExplanation:
    return DecisionExplanation.create(
        evidence_considered=evidence or ("e1",),
        rationale=rationale,
        priority=priority,
        expected_educational_benefit=benefit,
        confidence=confidence,
    )


def make_priority(score: float = 0.5, **kwargs) -> InterventionPriority:
    return InterventionPriority.create(score, **kwargs)


def make_roi(
    *,
    improvement: float = 0.2,
    minutes: float = 30.0,
    benefit: float = 0.5,
) -> EducationalROI:
    return EducationalROI.create(
        expected_readiness_improvement=improvement,
        estimated_study_minutes=minutes,
        educational_benefit=benefit,
    )


def make_intervention(
    intervention_id: str = "int-1",
    *,
    topic_id: str = "topic-1",
    priority: float = 0.6,
    intervention_type: InterventionType = InterventionType.REVISION,
) -> Intervention:
    prio = make_priority(priority)
    roi = make_roi(minutes=25.0, benefit=priority)
    return Intervention.create(
        intervention_id,
        intervention_type,
        topic_id=topic_id,
        priority=prio,
        roi=roi,
        explanation=make_explanation(priority=priority),
        confidence=ConfidenceBand.MEDIUM,
    )


def make_candidate(
    topic_id: str = "topic-1",
    *,
    retention: float = 0.3,
    mastery: float = 0.4,
    priority: float = 0.6,
) -> RevisionCandidate:
    return RevisionCandidate.create(
        topic_id,
        priority=make_priority(priority),
        roi=make_roi(benefit=priority),
        retention_score=retention,
        mastery_score=mastery,
        knowledge_score=max(retention, mastery),
        confidence=ConfidenceBand.MEDIUM,
        evidence_ids=("e1",),
        rationale="test_candidate",
    )


def make_window(
    topic_id: str = "topic-1",
    *,
    urgency: str = "today",
    minutes: float = 30.0,
    priority: float = 0.6,
) -> RevisionWindow:
    start = datetime(2026, 7, 18, 12, 0, tzinfo=UTC)
    return RevisionWindow.create(
        topic_id,
        urgency=urgency,
        suggested_start=start,
        allocated_minutes=minutes,
        priority_score=priority,
    )


def make_plan(
    plan_id: str = "plan-1",
    *,
    topics: list[str] | None = None,
) -> RevisionPlan:
    topics = topics or ["topic-1"]
    interventions = [
        make_intervention(f"int-{i}", topic_id=tid, priority=0.7 - i * 0.05)
        for i, tid in enumerate(topics)
    ]
    return RevisionPlan.create(plan_id, interventions=interventions)
