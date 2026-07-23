"""Readiness composition helpers — project Education OS outputs to view models.

Composition only. No mastery estimation, recommendation generation,
mission generation, scheduling, persistence, forecasting, or AI.
"""

from __future__ import annotations

from datetime import date

from application.education.mission_execution.enums import ExecutionStatus
from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)
from application.education.revision_planner.enums import SessionStatus
from application.education.revision_planner.models.study_schedule import StudySchedule
from application.student_experience.readiness.enums import (
    ActionPlanItemKind,
    AssessmentConfidenceCategory,
    ConsistencyBand,
    EvidenceQualityBand,
    EvidenceQuantityBand,
    ReadinessCategory,
    ReadinessDirection,
    ReadinessMilestoneKind,
    RiskKind,
    StrengthKind,
)
from application.student_experience.readiness.ids import (
    ReadinessId,
    ReadinessSnapshotId,
)
from application.student_experience.readiness.models.action_plan_card import (
    ActionPlanCard,
    ActionPlanItem,
)
from application.student_experience.readiness.models.confidence_card import (
    ConfidenceCard,
)
from application.student_experience.readiness.models.evidence_quality_card import (
    EvidenceQualityCard,
)
from application.student_experience.readiness.models.exam_readiness_view_model import (
    ExamReadinessViewModel,
)
from application.student_experience.readiness.models.readiness_card import (
    ReadinessCard,
)
from application.student_experience.readiness.models.readiness_snapshot import (
    ReadinessSnapshot,
)
from application.student_experience.readiness.models.readiness_trend_card import (
    ReadinessTrendCard,
)
from application.student_experience.readiness.models.risk_card import RiskCard, RiskItem
from application.student_experience.readiness.models.strength_card import (
    StrengthCard,
    StrengthItem,
)
from application.student_experience.readiness.models.upcoming_milestone_card import (
    ReadinessMilestone,
    UpcomingMilestoneCard,
)
from application.student_experience.readiness.presentation import (
    assessment_confidence_from_level,
    assessment_confidence_from_magnitude,
    assessment_confidence_label,
    assessment_confidence_message,
    consistency_from_stability,
    consistency_label,
    evidence_quality_from_confidence,
    evidence_quality_label,
    evidence_quantity_from_count,
    evidence_quantity_label,
    humanise_identifier,
    readiness_category_from_percent,
    readiness_category_label,
    readiness_direction_from_stability,
    readiness_direction_message,
    recommendation_guidance,
)
from application.student_experience.readiness.readiness_inputs import ReadinessInputs
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.mastery_estimation.enums import KnowledgeGapKind, MasteryBand
from domain.education.recommendation_engine.enums import RecommendationCategory

_COMPLETED = ExecutionStatus.COMPLETED
_ABANDONED = ExecutionStatus.ABANDONED
_INACTIVE_SESSION = frozenset(
    {
        SessionStatus.CANCELLED,
        SessionStatus.RESCHEDULED,
        SessionStatus.COMPLETED,
    }
)
_OVERDUE_STATUSES = frozenset({SessionStatus.PLANNED, SessionStatus.IN_PROGRESS})
_ACTION_KIND_BY_CATEGORY: dict[RecommendationCategory, ActionPlanItemKind] = {
    RecommendationCategory.FOCUS_COMPETENCY: ActionPlanItemKind.COMPLETE_NEXT_MISSION,
    RecommendationCategory.CONTINUE_CURRENT_MISSION: (
        ActionPlanItemKind.COMPLETE_NEXT_MISSION
    ),
    RecommendationCategory.CONSOLIDATE_KNOWLEDGE: (
        ActionPlanItemKind.FINISH_REVISION_CYCLE
    ),
    RecommendationCategory.INCREASE_REVISION_FREQUENCY: (
        ActionPlanItemKind.FINISH_REVISION_CYCLE
    ),
    RecommendationCategory.ATTEMPT_CHECKPOINT: (
        ActionPlanItemKind.REVIEW_BEFORE_CHECKPOINT
    ),
    RecommendationCategory.PREPARE_ASSESSMENT: (
        ActionPlanItemKind.REVIEW_BEFORE_CHECKPOINT
    ),
    RecommendationCategory.STUDY_PREREQUISITE: ActionPlanItemKind.ADDRESS_PREREQUISITE,
    RecommendationCategory.REVISIT_FOUNDATION: ActionPlanItemKind.ADDRESS_PREREQUISITE,
}


def compose_readiness(
    inputs: ReadinessInputs,
    *,
    readiness_id: ReadinessId,
) -> ExamReadinessViewModel:
    """Compose a full ExamReadinessViewModel from Education OS outputs."""
    readiness = compose_readiness_card(inputs)
    trend = compose_trend(inputs, readiness=readiness)
    confidence = compose_confidence(inputs)
    strengths = summarise_strengths(inputs)
    risks = summarise_risks(inputs)
    action_plan = compose_action_plan(inputs)
    milestones = compose_upcoming_milestones(inputs, readiness=readiness)
    evidence = compose_evidence_quality(inputs, confidence=confidence)
    return ExamReadinessViewModel(
        readiness_id=readiness_id,
        student_id=inputs.student_id,
        composed_at=inputs.as_of,
        readiness=readiness,
        trend=trend,
        confidence=confidence,
        strengths=strengths,
        risks=risks,
        action_plan=action_plan,
        upcoming_milestones=milestones,
        evidence_quality=evidence,
    )


def compose_snapshot(
    readiness: ExamReadinessViewModel,
    *,
    snapshot_id: ReadinessSnapshotId,
    home_focus_headline: str | None = None,
    journey_trajectory_message: str | None = None,
) -> ReadinessSnapshot:
    """Project an ExamReadinessViewModel into a compact ReadinessSnapshot."""
    return ReadinessSnapshot(
        snapshot_id=snapshot_id,
        student_id=readiness.student_id,
        captured_at=readiness.composed_at,
        readiness_available=readiness.readiness.available,
        readiness_percent=readiness.readiness.readiness_percent,
        readiness_category=readiness.readiness.readiness_category,
        readiness_label=readiness.readiness.readiness_label,
        direction=readiness.readiness.direction,
        direction_message=readiness.readiness.direction_message,
        assessment_confidence=readiness.confidence.assessment_confidence,
        assessment_confidence_label=readiness.confidence.assessment_confidence_label,
        strength_count=len(readiness.strengths.items),
        risk_count=len(readiness.risks.items),
        action_count=len(readiness.action_plan.items),
        milestone_count=len(readiness.upcoming_milestones.milestones),
        days_remaining=readiness.readiness.days_remaining,
        target_exam_label=readiness.readiness.target_exam_label,
        home_focus_headline=home_focus_headline,
        journey_trajectory_message=journey_trajectory_message,
    )


def compose_readiness_card(inputs: ReadinessInputs) -> ReadinessCard:
    """Compose current readiness, category, direction, target exam, days remaining."""
    exam = inputs.exam_target
    percent, direction = _readiness_signals(inputs)

    if exam is None and percent is None:
        return ReadinessCard(
            available=False,
            readiness_percent=None,
            readiness_category=ReadinessCategory.UNAVAILABLE,
            readiness_label=readiness_category_label(ReadinessCategory.UNAVAILABLE),
            direction=ReadinessDirection.UNKNOWN,
            direction_message=readiness_direction_message(ReadinessDirection.UNKNOWN),
            target_exam_label=None,
            exam_date=None,
            days_remaining=None,
        )

    category = readiness_category_from_percent(percent)
    days_remaining = None
    exam_date = None
    target_label = None
    if exam is not None:
        exam_date = exam.exam_date
        days_remaining = (exam.exam_date - inputs.as_of.date()).days
        target_label = humanise_identifier(exam.examination_id)

    # Prefer home snapshot direction message context when available without
    # inventing new scores — home already projected readiness language.
    if (
        direction is ReadinessDirection.UNKNOWN
        and inputs.home_snapshot is not None
        and inputs.home_snapshot.exam_readiness_label
    ):
        # Keep unknown direction; availability still follows exam/assessment.
        pass

    return ReadinessCard(
        available=exam is not None or percent is not None,
        readiness_percent=percent,
        readiness_category=category,
        readiness_label=readiness_category_label(category),
        direction=direction,
        direction_message=readiness_direction_message(direction),
        target_exam_label=target_label,
        exam_date=exam_date,
        days_remaining=days_remaining,
    )


def compose_trend(
    inputs: ReadinessInputs,
    *,
    readiness: ReadinessCard | None = None,
) -> ReadinessTrendCard:
    """Compose readiness trend from existing stability / journey signals."""
    card = readiness or compose_readiness_card(inputs)
    direction = card.direction
    has_data = direction is not ReadinessDirection.UNKNOWN

    if inputs.journey_snapshot is not None:
        journey = inputs.journey_snapshot
        summary = journey.trajectory_message
        if journey.mastery_trend.value == "improving":
            direction = ReadinessDirection.IMPROVING
            has_data = True
        elif journey.mastery_trend.value == "declining":
            direction = ReadinessDirection.DECLINING
            has_data = True
        elif journey.mastery_trend.value == "steady":
            direction = ReadinessDirection.STABLE
            has_data = True
    elif has_data:
        summary = (
            f"{card.direction_message} "
            f"Current category: {card.readiness_label}."
        )
    else:
        summary = "A readiness trend will appear as study history builds."

    return ReadinessTrendCard(
        direction=direction,
        direction_message=readiness_direction_message(direction),
        summary=summary,
        has_trend_data=has_data,
    )


def compose_confidence(inputs: ReadinessInputs) -> ConfidenceCard:
    """Compose assessment confidence — not student confidence."""
    magnitude: float | None = None
    evidence_count = 0
    consistency_band = ConsistencyBand.UNKNOWN

    if inputs.assessment is not None:
        confidence = inputs.assessment.overall_confidence
        magnitude = float(confidence.score.magnitude)
        evidence_count = int(confidence.evidence_count)
        if evidence_count == 0:
            evidence_count = int(inputs.assessment.overall_mastery.evidence_count)
        consistency_band = consistency_from_stability(
            inputs.assessment.overall_stability.band
        )
        category = assessment_confidence_from_level(confidence.score.band)
    elif inputs.evaluation is not None and inputs.evaluation.summary is not None:
        summary = inputs.evaluation.summary
        magnitude = float(summary.confidence_magnitude)
        evidence_count = int(summary.evidence_count)
        consistency_band = consistency_from_stability(summary.stability_band)
        category = assessment_confidence_from_magnitude(magnitude)
    else:
        category = AssessmentConfidenceCategory.UNKNOWN

    quality = evidence_quality_from_confidence(category)
    quantity = evidence_quantity_from_count(evidence_count if evidence_count else None)
    available = category is not AssessmentConfidenceCategory.UNKNOWN

    return ConfidenceCard(
        available=available,
        evidence_quality=quality,
        evidence_quality_label=evidence_quality_label(quality),
        evidence_quantity=quantity,
        evidence_quantity_label=evidence_quantity_label(quantity),
        evidence_count=evidence_count,
        consistency=consistency_band,
        consistency_label=consistency_label(consistency_band),
        assessment_confidence=category,
        assessment_confidence_label=assessment_confidence_label(category),
        message=assessment_confidence_message(category),
    )


def compose_evidence_quality(
    inputs: ReadinessInputs,
    *,
    confidence: ConfidenceCard | None = None,
) -> EvidenceQualityCard:
    """Compose evidence quality card from assessment confidence projection."""
    card = confidence or compose_confidence(inputs)
    if not card.available:
        return EvidenceQualityCard(
            available=False,
            quality=EvidenceQualityBand.UNKNOWN,
            quality_label=evidence_quality_label(EvidenceQualityBand.UNKNOWN),
            quantity=EvidenceQuantityBand.UNKNOWN,
            quantity_label=evidence_quantity_label(EvidenceQuantityBand.UNKNOWN),
            evidence_count=0,
            message="Evidence quality will appear once assessments are available.",
        )
    message = (
        f"Evidence quality is {card.evidence_quality_label.lower()} with "
        f"{card.evidence_quantity_label.lower()} quantity "
        f"({card.evidence_count} evidence points)."
    )
    return EvidenceQualityCard(
        available=True,
        quality=card.evidence_quality,
        quality_label=card.evidence_quality_label,
        quantity=card.evidence_quantity,
        quantity_label=card.evidence_quantity_label,
        evidence_count=card.evidence_count,
        message=message,
    )


def summarise_strengths(inputs: ReadinessInputs) -> StrengthCard:
    """Summarise strongest subjects, competencies, improvements, completion quality."""
    items: list[StrengthItem] = []

    strongest_subject = _strongest_subject(inputs.assessment)
    if strongest_subject is not None:
        items.append(strongest_subject)

    strongest_competency = _strongest_competency(inputs.assessment)
    if strongest_competency is not None:
        items.append(strongest_competency)

    improvement = _recent_improvement(inputs)
    if improvement is not None:
        items.append(improvement)

    quality = _mission_completion_quality(inputs.execution_history)
    if quality is not None:
        items.append(quality)

    if not items:
        return StrengthCard(
            items=(),
            summary="Strengths will appear as your assessment develops.",
            has_strengths=False,
        )

    summary = items[0].message
    if len(items) > 1:
        summary = f"{items[0].message} Also: {items[1].title.lower()}."
    return StrengthCard(items=tuple(items), summary=summary, has_strengths=True)


def summarise_risks(inputs: ReadinessInputs) -> RiskCard:
    """Summarise weakest competencies, prerequisites, gaps, overdue, pressure."""
    items: list[RiskItem] = []

    weakest = _weakest_competency(inputs.assessment)
    if weakest is not None:
        items.append(weakest)

    prerequisite = _incomplete_prerequisite(inputs)
    if prerequisite is not None:
        items.append(prerequisite)

    revision_gap = _revision_gap(inputs)
    if revision_gap is not None:
        items.append(revision_gap)

    overdue = _overdue_missions(inputs)
    if overdue is not None:
        items.append(overdue)

    pressure = _schedule_pressure(inputs)
    if pressure is not None:
        items.append(pressure)

    if not items:
        return RiskCard(
            items=(),
            summary="No readiness risks stand out from current signals.",
            has_risks=False,
        )

    summary = items[0].message
    if len(items) > 1:
        summary = f"{items[0].message} Also watch: {items[1].title.lower()}."
    return RiskCard(items=tuple(items), summary=summary, has_risks=True)


def compose_action_plan(inputs: ReadinessInputs) -> ActionPlanCard:
    """Compose deterministic guidance from existing recommendations — never invent."""
    items: list[ActionPlanItem] = []

    if inputs.recommendation_set is not None:
        recommendations = sorted(
            inputs.recommendation_set.recommendations,
            key=lambda item: (item.ordering.rank, item.recommendation_id.value),
        )
        for recommendation in recommendations[:5]:
            scope = _recommendation_scope(recommendation)
            guidance = recommendation_guidance(recommendation.category, scope=scope)
            kind = _ACTION_KIND_BY_CATEGORY.get(
                recommendation.category, ActionPlanItemKind.FOLLOW_RECOMMENDATION
            )
            title = humanise_identifier(recommendation.category.value) or "Next step"
            items.append(
                ActionPlanItem(
                    kind=kind,
                    title=title,
                    guidance=guidance,
                    scope_label=scope,
                )
            )

    if inputs.evaluation is not None and inputs.evaluation.decisions and not items:
        for decision in sorted(
            inputs.evaluation.decisions, key=lambda item: item.rank
        )[:5]:
            scope = humanise_identifier(decision.competency_id) or humanise_identifier(
                decision.subject_id
            )
            category = decision.category
            try:
                rec_category = RecommendationCategory(category)
                guidance = recommendation_guidance(rec_category, scope=scope or None)
                kind = _ACTION_KIND_BY_CATEGORY.get(
                    rec_category, ActionPlanItemKind.FOLLOW_RECOMMENDATION
                )
            except ValueError:
                guidance = recommendation_guidance(category, scope=scope or None)
                kind = ActionPlanItemKind.FOLLOW_RECOMMENDATION
            title = humanise_identifier(category) or "Next step"
            items.append(
                ActionPlanItem(
                    kind=kind,
                    title=title,
                    guidance=guidance,
                    scope_label=scope or None,
                )
            )

    if not items and inputs.schedule is not None:
        items.append(
            ActionPlanItem(
                kind=ActionPlanItemKind.VIEW_SCHEDULE,
                title="View schedule",
                guidance="Check your study schedule for the next planned session.",
            )
        )

    if not items:
        return ActionPlanCard(
            items=(),
            summary="An action plan will appear when recommendations are available.",
            has_actions=False,
        )

    summary = items[0].guidance
    return ActionPlanCard(items=tuple(items), summary=summary, has_actions=True)


def compose_upcoming_milestones(
    inputs: ReadinessInputs,
    *,
    readiness: ReadinessCard | None = None,
) -> UpcomingMilestoneCard:
    """Compose upcoming milestones from schedule, exam target, and recommendations."""
    card = readiness or compose_readiness_card(inputs)
    today = inputs.as_of.date()
    milestones: list[ReadinessMilestone] = []

    revision = _next_revision_from_recommendations(inputs)
    if revision is not None:
        milestones.append(revision)

    if (
        card.readiness_category
        not in (ReadinessCategory.EXAM_READY, ReadinessCategory.UNAVAILABLE)
        and card.available
    ):
        milestones.append(
            ReadinessMilestone(
                kind=ReadinessMilestoneKind.READINESS_TARGET,
                title="Reach readiness target",
                detail=(
                    f"Continue toward exam readiness — currently "
                    f"{card.readiness_label.lower()}."
                ),
                milestone_date=card.exam_date,
                days_until=card.days_remaining,
            )
        )

    checkpoint = _next_checkpoint_from_recommendations(inputs)
    if checkpoint is not None:
        milestones.append(checkpoint)

    if inputs.exam_target is not None:
        exam = inputs.exam_target
        days = (exam.exam_date - today).days
        milestones.append(
            ReadinessMilestone(
                kind=ReadinessMilestoneKind.EXAM,
                title=f"Exam: {humanise_identifier(exam.examination_id)}",
                detail=(
                    f"Exam date is {exam.exam_date.isoformat()} "
                    f"({days} day{'s' if days != 1 else ''} remaining)."
                ),
                milestone_date=exam.exam_date,
                days_until=days,
            )
        )

    next_session = _next_future_session(inputs.schedule, today)
    if next_session is not None and not any(
        item.kind is ReadinessMilestoneKind.STUDY_SESSION for item in milestones
    ):
        days = (next_session.session_date - today).days
        milestones.append(
            ReadinessMilestone(
                kind=ReadinessMilestoneKind.STUDY_SESSION,
                title="Next study session",
                detail=(
                    f"Next session is on {next_session.session_date.isoformat()}."
                ),
                milestone_date=next_session.session_date,
                days_until=days,
            )
        )

    if not milestones:
        return UpcomingMilestoneCard(
            milestones=(),
            primary=None,
            has_milestones=False,
            summary="Milestones will appear as your plan develops.",
        )

    primary = milestones[0]
    return UpcomingMilestoneCard(
        milestones=tuple(milestones),
        primary=primary,
        has_milestones=True,
        summary=primary.detail,
    )


# --- internal helpers -----------------------------------------------------


def _readiness_signals(
    inputs: ReadinessInputs,
) -> tuple[float | None, ReadinessDirection]:
    if inputs.assessment is not None:
        percent = round(float(inputs.assessment.overall_mastery.magnitude) * 100.0, 2)
        direction = readiness_direction_from_stability(
            inputs.assessment.overall_stability.band
        )
        return percent, direction
    if inputs.evaluation is not None and inputs.evaluation.summary is not None:
        summary = inputs.evaluation.summary
        percent = round(float(summary.mastery_magnitude) * 100.0, 2)
        direction = readiness_direction_from_stability(summary.stability_band)
        return percent, direction
    if inputs.home_snapshot is not None and inputs.home_snapshot.exam_available:
        # Home already projected a readiness label — no percent without assessment.
        return None, ReadinessDirection.UNKNOWN
    return None, ReadinessDirection.UNKNOWN


def _strongest_subject(assessment: MasteryAssessment | None) -> StrengthItem | None:
    if assessment is None or not assessment.subject_assessments:
        return None
    ranked = sorted(
        assessment.subject_assessments,
        key=lambda subject: (
            -subject.mastery.magnitude,
            subject.subject_id.value,
        ),
    )
    top = ranked[0]
    if not top.mastery.has_evidence():
        return None
    label = humanise_identifier(top.subject_id.value)
    return StrengthItem(
        kind=StrengthKind.STRONGEST_SUBJECT,
        title="Strongest subject",
        message=f"{label} is your strongest assessed subject right now.",
        scope_label=label,
    )


def _strongest_competency(
    assessment: MasteryAssessment | None,
) -> StrengthItem | None:
    if assessment is None:
        return None
    competencies = [
        competency
        for subject in assessment.subject_assessments
        for competency in subject.competency_assessments
        if competency.mastery.has_evidence()
        and competency.mastery.band
        in (MasteryBand.SECURE, MasteryBand.MASTERED, MasteryBand.DEVELOPING)
    ]
    if not competencies:
        return None
    strongest = sorted(
        competencies,
        key=lambda item: (-item.mastery.magnitude, item.competency_id.value),
    )[0]
    label = humanise_identifier(strongest.competency_id.value)
    return StrengthItem(
        kind=StrengthKind.STRONGEST_COMPETENCY,
        title="Strongest competency",
        message=f"{label} is your strongest assessed competency.",
        scope_label=label,
    )


def _recent_improvement(inputs: ReadinessInputs) -> StrengthItem | None:
    if inputs.journey_snapshot is not None:
        journey = inputs.journey_snapshot
        if journey.mastery_trend.value == "improving":
            return StrengthItem(
                kind=StrengthKind.RECENT_IMPROVEMENT,
                title="Recent improvement",
                message=journey.trajectory_message,
            )
        if journey.weekly_missions_completed > 0:
            count = journey.weekly_missions_completed
            return StrengthItem(
                kind=StrengthKind.RECENT_IMPROVEMENT,
                title="Recent improvement",
                message=(
                    f"You completed {count} mission"
                    f"{'s' if count != 1 else ''} this week."
                ),
            )
    if inputs.evaluation is not None and inputs.evaluation.summary is not None:
        if inputs.evaluation.summary.stability_band == "stable":
            return StrengthItem(
                kind=StrengthKind.RECENT_IMPROVEMENT,
                title="Recent improvement",
                message="Your latest evaluation shows a stable learning signal.",
            )
    return None


def _mission_completion_quality(
    history: tuple[MissionExecution, ...],
) -> StrengthItem | None:
    completed = sum(1 for item in history if item.status is _COMPLETED)
    abandoned = sum(1 for item in history if item.status is _ABANDONED)
    total = completed + abandoned
    if total == 0:
        return None
    rate = round((completed / total) * 100.0)
    if rate < 50:
        return None
    return StrengthItem(
        kind=StrengthKind.MISSION_COMPLETION_QUALITY,
        title="Mission completion quality",
        message=f"You complete {rate}% of the missions you start.",
    )


def _weakest_competency(assessment: MasteryAssessment | None) -> RiskItem | None:
    if assessment is None:
        return None
    if assessment.knowledge_gaps:
        gap = sorted(
            assessment.knowledge_gaps,
            key=lambda item: (
                item.severity.value,
                item.mastery_score.magnitude,
                item.competency_id.value,
            ),
        )[0]
        label = humanise_identifier(gap.competency_id.value)
        return RiskItem(
            kind=RiskKind.WEAKEST_COMPETENCY,
            title="Weakest competency",
            message=f"{label} needs the most attention.",
            scope_label=label,
        )
    competencies = [
        competency
        for subject in assessment.subject_assessments
        for competency in subject.competency_assessments
        if competency.mastery.has_evidence()
    ]
    if not competencies:
        return None
    weakest = sorted(
        competencies,
        key=lambda item: (item.mastery.magnitude, item.competency_id.value),
    )[0]
    label = humanise_identifier(weakest.competency_id.value)
    return RiskItem(
        kind=RiskKind.WEAKEST_COMPETENCY,
        title="Weakest competency",
        message=f"{label} is your lowest assessed competency.",
        scope_label=label,
    )


def _incomplete_prerequisite(inputs: ReadinessInputs) -> RiskItem | None:
    assessment = inputs.assessment
    if assessment is not None:
        prereq_gaps = [
            gap
            for gap in assessment.knowledge_gaps
            if gap.kind is KnowledgeGapKind.WEAK_PREREQUISITE
        ]
        if prereq_gaps:
            gap = sorted(
                prereq_gaps,
                key=lambda item: (
                    item.severity.value,
                    item.competency_id.value,
                ),
            )[0]
            label = humanise_identifier(gap.competency_id.value)
            return RiskItem(
                kind=RiskKind.INCOMPLETE_PREREQUISITE,
                title="Incomplete prerequisite",
                message=f"A prerequisite for {label} still needs attention.",
                scope_label=label,
            )

    if inputs.recommendation_set is not None:
        for recommendation in sorted(
            inputs.recommendation_set.recommendations,
            key=lambda item: item.ordering.rank,
        ):
            if recommendation.category is RecommendationCategory.STUDY_PREREQUISITE:
                scope = _recommendation_scope(recommendation)
                return RiskItem(
                    kind=RiskKind.INCOMPLETE_PREREQUISITE,
                    title="Incomplete prerequisite",
                    message=(
                        f"Prerequisite work remains"
                        f"{f' for {scope}' if scope else ''}."
                    ),
                    scope_label=scope,
                )
    return None


def _revision_gap(inputs: ReadinessInputs) -> RiskItem | None:
    if inputs.recommendation_set is not None:
        for recommendation in sorted(
            inputs.recommendation_set.recommendations,
            key=lambda item: item.ordering.rank,
        ):
            if recommendation.category in (
                RecommendationCategory.INCREASE_REVISION_FREQUENCY,
                RecommendationCategory.CONSOLIDATE_KNOWLEDGE,
                RecommendationCategory.REVIEW_CONCEPT,
            ):
                scope = _recommendation_scope(recommendation)
                return RiskItem(
                    kind=RiskKind.REVISION_GAP,
                    title="Revision gap",
                    message=(
                        f"Revision still needed"
                        f"{f' for {scope}' if scope else ''}."
                    ),
                    scope_label=scope,
                )
    return None


def _overdue_missions(inputs: ReadinessInputs) -> RiskItem | None:
    schedule = inputs.schedule
    if schedule is None:
        return None
    today = inputs.as_of.date()
    overdue_sessions = [
        session
        for session in schedule.sessions
        if session.session_date < today and session.status in _OVERDUE_STATUSES
    ]
    if not overdue_sessions:
        return None
    count = len(overdue_sessions)
    return RiskItem(
        kind=RiskKind.OVERDUE_MISSION,
        title="Overdue missions",
        message=(
            f"{count} scheduled session{'s' if count != 1 else ''} "
            f"{'are' if count != 1 else 'is'} overdue."
        ),
    )


def _schedule_pressure(inputs: ReadinessInputs) -> RiskItem | None:
    exam = inputs.exam_target
    schedule = inputs.schedule
    if exam is None or schedule is None:
        return None
    today = inputs.as_of.date()
    days_remaining = (exam.exam_date - today).days
    if days_remaining < 0:
        return RiskItem(
            kind=RiskKind.SCHEDULE_PRESSURE,
            title="Schedule pressure",
            message="The exam date has passed while scheduled work remains.",
        )
    remaining = [
        session
        for session in schedule.sessions
        if session.session_date >= today and session.status not in _INACTIVE_SESSION
    ]
    if not remaining:
        return None
    # Pressure when remaining sessions exceed remaining days (simple projection).
    if days_remaining <= 14 and len(remaining) > max(days_remaining, 1):
        return RiskItem(
            kind=RiskKind.SCHEDULE_PRESSURE,
            title="Schedule pressure",
            message=(
                f"{len(remaining)} sessions remain with "
                f"{days_remaining} day{'s' if days_remaining != 1 else ''} "
                f"until the exam."
            ),
        )
    return None


def _recommendation_scope(recommendation) -> str | None:
    target = recommendation.target
    if target.competency_id is not None:
        return humanise_identifier(target.competency_id.value) or None
    if target.subject_id is not None:
        return humanise_identifier(target.subject_id.value) or None
    return None


def _next_revision_from_recommendations(
    inputs: ReadinessInputs,
) -> ReadinessMilestone | None:
    if inputs.recommendation_set is None:
        return None
    for recommendation in sorted(
        inputs.recommendation_set.recommendations,
        key=lambda item: item.ordering.rank,
    ):
        if recommendation.category in (
            RecommendationCategory.CONSOLIDATE_KNOWLEDGE,
            RecommendationCategory.INCREASE_REVISION_FREQUENCY,
            RecommendationCategory.MAINTAIN_MASTERY,
        ):
            scope = _recommendation_scope(recommendation)
            return ReadinessMilestone(
                kind=ReadinessMilestoneKind.REVISION_CYCLE,
                title="Complete current revision cycle",
                detail=(
                    f"Finish the revision cycle"
                    f"{f' for {scope}' if scope else ''}."
                ),
            )
    return None


def _next_checkpoint_from_recommendations(
    inputs: ReadinessInputs,
) -> ReadinessMilestone | None:
    if inputs.recommendation_set is None:
        return None
    for recommendation in sorted(
        inputs.recommendation_set.recommendations,
        key=lambda item: item.ordering.rank,
    ):
        if recommendation.category in (
            RecommendationCategory.ATTEMPT_CHECKPOINT,
            RecommendationCategory.PREPARE_ASSESSMENT,
        ):
            scope = _recommendation_scope(recommendation)
            return ReadinessMilestone(
                kind=ReadinessMilestoneKind.CHECKPOINT,
                title="Checkpoint due",
                detail=(
                    f"Checkpoint preparation"
                    f"{f' for {scope}' if scope else ''} is due."
                ),
            )
    return None


def _next_future_session(schedule: StudySchedule | None, today: date):
    if schedule is None:
        return None
    candidates = [
        session
        for session in schedule.sessions
        if session.session_date >= today and session.status not in _INACTIVE_SESSION
    ]
    if not candidates:
        return None
    return sorted(
        candidates, key=lambda session: (session.session_date, session.start_time)
    )[0]
