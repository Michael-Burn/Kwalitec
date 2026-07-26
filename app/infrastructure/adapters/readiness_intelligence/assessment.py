"""Assemble Readiness Intelligence assessment (EP-001.3).

Readiness-owned evaluation outputs. Uses Twin signals and Planner outputs —
never invents learner state or re-plans missions.
"""

from __future__ import annotations

from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
)
from app.infrastructure.adapters.readiness_intelligence.contracts import (
    CONFIDENCE_HIGH,
    CONFIDENCE_LOW,
    CONFIDENCE_MEDIUM,
    CONFIDENCE_VERY_LOW,
    READINESS_INTELLIGENCE_VERSION,
    ReadinessDriver,
    ReadinessIntelligenceAssessment,
    ReadinessIntelligenceInputs,
    RecommendedNextAction,
    TopicArea,
)

_LIGHT_BEHAVIOUR = frozenset(
    {
        "irregular",
        "inconsistent",
        "fragile",
        "low",
        "struggling",
        "interrupted",
        "sparse",
    }
)


def _confidence_level(inputs: ReadinessIntelligenceInputs) -> str:
    """Deterministic confidence from evidence density — not self-report."""
    attempts = int(inputs.evidence_attempt_count or 0)
    started = int(inputs.topics_started or 0)
    total = int(inputs.total_topics or 0)
    mission_events = int(inputs.mission_completed_count or 0) + int(
        inputs.mission_missed_count or 0
    )

    coverage_ok = total > 0 and started >= max(1, total // 4)
    evidence_ok = attempts >= 3
    mission_ok = mission_events >= 2

    score = 0
    if attempts >= 1:
        score += 1
    if evidence_ok:
        score += 1
    if started >= 1:
        score += 1
    if coverage_ok:
        score += 1
    if mission_ok:
        score += 1
    if inputs.avg_mastery is not None:
        score += 1

    if score <= 1:
        return CONFIDENCE_VERY_LOW
    if score <= 3:
        return CONFIDENCE_LOW
    if score <= 5:
        return CONFIDENCE_MEDIUM
    return CONFIDENCE_HIGH


def _split_areas(
    areas: tuple[TopicArea, ...],
    *,
    limit: int = 3,
) -> tuple[tuple[TopicArea, ...], tuple[TopicArea, ...]]:
    scored = [a for a in areas if a.mastery_score is not None]
    if not scored:
        return (), ()
    strongest = tuple(scored[:limit])
    weakest_sorted = sorted(
        scored,
        key=lambda a: (
            a.mastery_score if a.mastery_score is not None else 999.0,
            a.topic_id,
        ),
    )
    weakest = tuple(weakest_sorted[:limit])
    return strongest, weakest


def _influence_from_pct(value: float | None, *, supportive_at: float = 70.0) -> str:
    if value is None:
        return "unknown"
    if value >= supportive_at:
        return "supportive"
    if value >= 40.0:
        return "mixed"
    return "risk_elevating"


def _drivers(inputs: ReadinessIntelligenceInputs) -> tuple[ReadinessDriver, ...]:
    drivers: list[ReadinessDriver] = []

    drivers.append(
        ReadinessDriver(
            driver_id="curriculum_coverage",
            label="Curriculum coverage",
            influence=_influence_from_pct(inputs.coverage_pct),
            value=inputs.coverage_pct,
            source="canonical.study_state.readiness_overall|topic_progress",
            rationale=(
                f"Coverage {inputs.coverage_pct:.1f}% of syllabus leaves started."
                if inputs.coverage_pct is not None
                else "Coverage unavailable on Canonical Learner State."
            ),
        )
    )
    drivers.append(
        ReadinessDriver(
            driver_id="knowledge_strength",
            label="Knowledge strength",
            influence=_influence_from_pct(inputs.avg_mastery),
            value=inputs.avg_mastery,
            source="canonical.topic_mastery",
            rationale=(
                f"Average Estimated Knowledge {inputs.avg_mastery:.1f}."
                if inputs.avg_mastery is not None
                else "Average mastery unavailable on Canonical Learner State."
            ),
        )
    )
    drivers.append(
        ReadinessDriver(
            driver_id="mission_discipline",
            label="Mission / review discipline",
            influence=_influence_from_pct(inputs.review_discipline),
            value=inputs.review_discipline,
            source="canonical.mission_completion|readiness_overall",
            rationale=(
                f"Review discipline {inputs.review_discipline:.1f}% "
                f"({inputs.mission_completed_count} completed / "
                f"{inputs.mission_missed_count} missed)."
                if inputs.review_discipline is not None
                else "Mission discipline unavailable on Canonical Learner State."
            ),
        )
    )

    if inputs.consistency_label:
        label_l = inputs.consistency_label.strip().lower()
        influence = (
            "risk_elevating" if label_l in _LIGHT_BEHAVIOUR else "supportive"
        )
        drivers.append(
            ReadinessDriver(
                driver_id="study_consistency",
                label="Study consistency",
                influence=influence,
                value=inputs.consistency_label,
                source="canonical.study_consistency",
                rationale=f"Consistency facet: {inputs.consistency_label}.",
            )
        )

    for key, label in inputs.behaviour_labels.items():
        label_l = str(label).strip().lower()
        influence = (
            "risk_elevating" if label_l in _LIGHT_BEHAVIOUR else "supportive"
        )
        drivers.append(
            ReadinessDriver(
                driver_id=f"behaviour_{key}",
                label=f"Behaviour — {key.replace('_', ' ')}",
                influence=influence,
                value=label,
                source="canonical.study_behaviour",
                rationale=f"{key} facet: {label}.",
            )
        )

    if inputs.current_streak is not None:
        influence = (
            "supportive"
            if inputs.current_streak >= 3
            else ("mixed" if inputs.current_streak >= 1 else "risk_elevating")
        )
        drivers.append(
            ReadinessDriver(
                driver_id="streaks",
                label="Study streak",
                influence=influence,
                value=inputs.current_streak,
                source="canonical.streaks",
                rationale=(
                    f"Current streak {inputs.current_streak} days"
                    + (
                        f" (longest {inputs.longest_streak})."
                        if inputs.longest_streak is not None
                        else "."
                    )
                ),
            )
        )

    if inputs.practice_mean_accuracy_pct is not None:
        drivers.append(
            ReadinessDriver(
                driver_id="practice_performance",
                label="Practice performance",
                influence=_influence_from_pct(inputs.practice_mean_accuracy_pct),
                value=inputs.practice_mean_accuracy_pct,
                source="canonical.practice_performance",
                rationale=(
                    f"Mean practice accuracy "
                    f"{inputs.practice_mean_accuracy_pct:.1f}%."
                ),
            )
        )

    if inputs.exam_countdown_days is not None:
        days = inputs.exam_countdown_days
        if days <= 14:
            influence = "risk_elevating"
            rationale = f"Exam in {days} days — elevated time pressure."
        elif days <= 45:
            influence = "mixed"
            rationale = f"Exam in {days} days — moderate time pressure."
        else:
            influence = "supportive"
            rationale = f"Exam in {days} days — runway available."
        drivers.append(
            ReadinessDriver(
                driver_id="time_goal_pressure",
                label="Time / goal pressure",
                influence=influence,
                value=days,
                source="canonical.study_state",
                rationale=rationale,
            )
        )

    drivers.append(
        ReadinessDriver(
            driver_id="evidence_density",
            label="Evidence density",
            influence=(
                "supportive"
                if inputs.evidence_attempt_count >= 3
                else (
                    "mixed"
                    if inputs.evidence_attempt_count >= 1
                    else "risk_elevating"
                )
            ),
            value=inputs.evidence_attempt_count,
            source="canonical.learning_evidence",
            rationale=(
                f"{inputs.evidence_attempt_count} learning evidence attempts "
                "backing confidence."
            ),
        )
    )

    return tuple(drivers)


def _next_actions(
    inputs: ReadinessIntelligenceInputs,
) -> tuple[RecommendedNextAction, ...]:
    actions: list[RecommendedNextAction] = []
    for index, row in enumerate(inputs.planner_missions, start=1):
        slot = str(row.get("slot") or f"mission_{index}")
        topic_name = str(row.get("topic_name") or "Study focus")
        reason = str(row.get("reason") or "Planner mission slot")
        priority = str(row.get("priority") or "normal")
        topic_id = row.get("topic_id")
        actions.append(
            RecommendedNextAction(
                action_id=f"mission:{slot}",
                title=f"Today's mission — {topic_name}",
                reason=reason,
                priority=priority,
                topic_id=None if topic_id is None else str(topic_id),
                source="planner.today_missions",
            )
        )
    for row in inputs.planner_revision_priorities:
        rank = row.get("rank")
        topic_name = str(row.get("topic_name") or "Revision topic")
        reason = str(row.get("reason") or "Planner revision priority")
        topic_id = row.get("topic_id")
        actions.append(
            RecommendedNextAction(
                action_id=f"revision:{topic_id or rank}",
                title=f"Revise — {topic_name}",
                reason=reason,
                priority=f"rank_{rank}" if rank is not None else "revision",
                topic_id=None if topic_id is None else str(topic_id),
                source="planner.revision_priorities",
            )
        )
    # Cap for stable, concise assessment packaging.
    return tuple(actions[:6])


class ReadinessAssessmentAssembler:
    """Assemble ReadinessIntelligenceAssessment from projected inputs."""

    ASSEMBLER_ID = "readiness_assessment_assembler"
    ASSEMBLER_VERSION = READINESS_INTELLIGENCE_VERSION

    def assemble(
        self, inputs: ReadinessIntelligenceInputs
    ) -> ReadinessIntelligenceAssessment:
        if not isinstance(inputs, ReadinessIntelligenceInputs):
            raise TypeError("inputs must be a ReadinessIntelligenceInputs")

        if inputs.availability != AVAILABILITY_AVAILABLE:
            return ReadinessIntelligenceAssessment(
                student_id=inputs.student_id,
                as_of=inputs.as_of,
                consumer_version=READINESS_INTELLIGENCE_VERSION,
                foundation_version=inputs.foundation_version,
                twin_id=inputs.twin_id,
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=inputs.unavailable_reason,
                readiness_score=None,
                confidence_level=CONFIDENCE_VERY_LOW,
                strongest_areas=(),
                weakest_areas=(),
                readiness_drivers=(),
                recommended_next_actions=(),
                provenance_refs=inputs.provenance_refs,
                limitations_codes=inputs.limitations_codes,
                explainability={
                    "source": "canonical_learner_state",
                    "status": "unavailable",
                },
            )

        strongest, weakest = _split_areas(inputs.topic_areas)
        confidence = _confidence_level(inputs)
        drivers = _drivers(inputs)
        actions = _next_actions(inputs)

        return ReadinessIntelligenceAssessment(
            student_id=inputs.student_id,
            as_of=inputs.as_of,
            consumer_version=READINESS_INTELLIGENCE_VERSION,
            foundation_version=inputs.foundation_version,
            twin_id=inputs.twin_id,
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
            readiness_score=inputs.readiness_score,
            confidence_level=confidence,
            strongest_areas=strongest,
            weakest_areas=weakest,
            readiness_drivers=drivers,
            recommended_next_actions=actions,
            provenance_refs=inputs.provenance_refs,
            limitations_codes=inputs.limitations_codes,
            explainability={
                "source": "canonical_learner_state",
                "status": "available",
                "score_authority": "runtime_a_readiness_pass_through_or_50_30_20",
                "planner_available": inputs.planner_available,
                "lifecycle_stage": inputs.lifecycle_stage,
                "examination_label": inputs.examination_label,
            },
        )


def build_readiness_assessment_assembler() -> ReadinessAssessmentAssembler:
    return ReadinessAssessmentAssembler()


__all__ = [
    "ReadinessAssessmentAssembler",
    "build_readiness_assessment_assembler",
]
