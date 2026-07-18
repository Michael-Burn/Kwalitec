"""Revision planner — build revision candidates and plans from Twin state."""

from __future__ import annotations

from app.application.adaptive_learning.policies.intervention_policy import (
    InterventionPolicy,
)
from app.application.adaptive_learning.policies.priority_policy import PriorityPolicy
from app.application.adaptive_learning.priority_calculator import PriorityCalculator
from app.application.adaptive_learning.roi_estimator import ROIEstimator
from app.domain.adaptive_learning.revision_candidate import RevisionCandidate
from app.domain.adaptive_learning.revision_plan import RevisionPlan
from app.domain.student_twin.confidence_band import ConfidenceBand
from app.domain.student_twin.confidence_state import ConfidenceState
from app.domain.student_twin.knowledge_state import KnowledgeState
from app.domain.student_twin.learning_velocity import LearningVelocity
from app.domain.student_twin.mastery_state import MasteryState
from app.domain.student_twin.retention_state import RetentionState
from app.domain.student_twin.weakness_profile import WeaknessProfile


class RevisionPlanner:
    """Enumerate and rank revision candidates from Twin educational state."""

    @staticmethod
    def build_candidates(
        *,
        knowledge: KnowledgeState,
        mastery: MasteryState,
        retention: RetentionState,
        confidence: ConfidenceState,
        weaknesses: WeaknessProfile,
        velocity: LearningVelocity,
        topic_importance: dict[str, float] | None = None,
        prerequisite_criticality: dict[str, float] | None = None,
        historical_struggle: dict[str, float] | None = None,
        exam_proximity: float = 0.0,
        current_topic_id: str | None = None,
    ) -> tuple[RevisionCandidate, ...]:
        """Build ranked revision candidates from Twin component states."""
        importance = topic_importance or {}
        prereq = prerequisite_criticality or {}
        struggle_map = historical_struggle or {}

        topic_ids = _collect_topic_ids(
            knowledge, mastery, retention, confidence, weaknesses, current_topic_id
        )
        mastery_by = {r.topic_id: r for r in mastery.topic_records}
        retention_by = {r.topic_id: r for r in retention.topic_records}
        knowledge_by = {r.topic_id: r for r in knowledge.topic_records}
        confidence_by = {r.topic_id: r for r in confidence.topic_records}
        weakness_severity = _weakness_severity(weaknesses)

        candidates: list[RevisionCandidate] = []
        for topic_id in topic_ids[: InterventionPolicy.MAX_CANDIDATES_EVALUATED]:
            m = mastery_by.get(topic_id)
            r = retention_by.get(topic_id)
            k = knowledge_by.get(topic_id)
            c = confidence_by.get(topic_id)
            mastery_score = m.mastery_score if m else 0.0
            retention_score = r.retention_score if r else 0.0
            knowledge_score = k.knowledge_score if k else 0.0
            conf_band = c.confidence_band if c else ConfidenceBand.VERY_LOW
            struggle = max(
                struggle_map.get(topic_id, 0.0),
                weakness_severity.get(topic_id, 0.0),
            )
            # Slight boost when this is the current journey topic with risk.
            topic_prereq = prereq.get(topic_id, 0.0)
            if current_topic_id and topic_id == current_topic_id:
                topic_prereq = max(topic_prereq, 0.35)

            priority = PriorityCalculator.calculate(
                retention_score=retention_score,
                mastery_score=mastery_score,
                confidence=c.confidence_score if c else conf_band,
                curriculum_importance=importance.get(topic_id, 0.5),
                prerequisite_criticality=topic_prereq,
                historical_struggle=struggle,
                events_per_day=velocity.events_per_day,
                mastery_delta=velocity.mastery_delta,
                exam_proximity=exam_proximity,
            )
            if not PriorityPolicy.meets_revision_threshold(priority.score):
                continue

            roi = ROIEstimator.estimate(
                priority=priority,
                retention_risk=priority.retention_risk,
                mastery_gap=priority.mastery_gap,
                curriculum_importance=importance.get(topic_id, 0.5),
            )
            evidence = tuple(
                dict.fromkeys(
                    (
                        *(m.evidence_ids if m else ()),
                        *(r.evidence_ids if r else ()),
                        *(k.evidence_ids if k else ()),
                        *(c.evidence_ids if c else ()),
                    )
                )
            )
            rationale = _candidate_rationale(
                retention_score=retention_score,
                mastery_score=mastery_score,
                struggle=struggle,
            )
            candidates.append(
                RevisionCandidate.create(
                    topic_id,
                    priority=priority,
                    roi=roi,
                    retention_score=retention_score,
                    mastery_score=mastery_score,
                    knowledge_score=knowledge_score,
                    confidence=conf_band,
                    evidence_ids=evidence,
                    struggle_score=struggle,
                    curriculum_importance=importance.get(topic_id, 0.5),
                    prerequisite_criticality=topic_prereq,
                    rationale=rationale,
                )
            )

        candidates.sort(key=lambda c: c.ranking_key)
        return tuple(candidates)

    @staticmethod
    def empty_plan(plan_id: str = "plan-empty") -> RevisionPlan:
        """Return an empty revision plan."""
        return RevisionPlan.empty(plan_id)


def _collect_topic_ids(
    knowledge: KnowledgeState,
    mastery: MasteryState,
    retention: RetentionState,
    confidence: ConfidenceState,
    weaknesses: WeaknessProfile,
    current_topic_id: str | None,
) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()

    def _add(tid: str | None) -> None:
        if not tid or tid in seen:
            return
        seen.add(tid)
        ordered.append(tid)

    for item in weaknesses.items:
        _add(item.topic_id)
    for record in retention.topic_records:
        _add(record.topic_id)
    for record in mastery.topic_records:
        _add(record.topic_id)
    for record in knowledge.topic_records:
        _add(record.topic_id)
    for record in confidence.topic_records:
        _add(record.topic_id)
    _add(current_topic_id)
    return ordered


def _weakness_severity(weaknesses: WeaknessProfile) -> dict[str, float]:
    result: dict[str, float] = {}
    for item in weaknesses.items:
        result[item.topic_id] = max(result.get(item.topic_id, 0.0), item.severity)
    return result


def _candidate_rationale(
    *,
    retention_score: float,
    mastery_score: float,
    struggle: float,
) -> str:
    if retention_score < 0.45:
        return "low_retention_revision_needed"
    if mastery_score < 0.40:
        return "low_mastery_revision_needed"
    if struggle >= 0.55:
        return "historical_struggle_revision_needed"
    return "priority_threshold_met"
