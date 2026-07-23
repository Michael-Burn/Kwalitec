"""Coach composition helpers — project Education OS / XP outputs to coaching VMs.

Composition only. No mastery estimation, recommendation generation,
mission generation, scheduling, persistence, or LLM calls.
"""

from __future__ import annotations

from datetime import date

from application.education.mission_execution.enums import ExecutionStatus
from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)
from application.education.mission_generation.enums import MissionType
from application.education.mission_generation.models.mission import Mission
from application.education.mission_generation.models.mission_plan import MissionPlan
from application.education.orchestration.dto.educational_evaluation import (
    EducationalEvaluation,
)
from application.education.revision_planner.enums import SessionStatus
from application.education.revision_planner.models.study_schedule import StudySchedule
from application.student_experience.coach.coach_inputs import CoachInputs
from application.student_experience.coach.enums import (
    CelebrationKind,
    ExplanationCardKind,
    ReflectionPromptKind,
    SuggestedQuestionKind,
)
from application.student_experience.coach.ids import (
    CoachId,
    CoachSnapshotId,
    ConversationId,
)
from application.student_experience.coach.models.celebration_moments import (
    CelebrationMoment,
    CelebrationMoments,
)
from application.student_experience.coach.models.coach_context import (
    CoachContext,
    FocusContext,
    ImprovementItem,
    JourneyContext,
    MilestoneItem,
    MissionContext,
    ReadinessContext,
    RiskItem,
)
from application.student_experience.coach.models.coach_snapshot import CoachSnapshot
from application.student_experience.coach.models.conversation_context import (
    ConversationContext,
)
from application.student_experience.coach.models.explanation_cards import (
    ExplanationCard,
    ExplanationCards,
)
from application.student_experience.coach.models.reflection_prompts import (
    ReflectionPrompt,
    ReflectionPrompts,
)
from application.student_experience.coach.models.suggested_questions import (
    SuggestedQuestion,
    SuggestedQuestions,
)
from application.student_experience.coach.presentation import (
    humanise_identifier,
    is_revision_mission,
    mission_purpose,
    mission_title,
    study_objective_label,
)
from application.student_experience.progress.enums import TrendDirection

_REVISION_TYPES = frozenset(
    {
        MissionType.REVISION_SESSION,
        MissionType.REVISE_PREREQUISITE,
        MissionType.MAINTENANCE_REVIEW,
        MissionType.CONSOLIDATE_KNOWLEDGE,
    }
)

_ACTIVE_EXECUTION = frozenset(
    {
        ExecutionStatus.STARTED,
        ExecutionStatus.RESUMED,
        ExecutionStatus.PAUSED,
    }
)


def compose_context(inputs: CoachInputs, *, coach_id: CoachId) -> CoachContext:
    """Compose a full CoachContext from Student Experience + Education OS inputs."""
    return CoachContext(
        coach_id=coach_id,
        student_id=inputs.student_id,
        composed_at=inputs.as_of,
        current_focus=compose_focus(inputs),
        learning_journey=compose_journey(inputs),
        readiness=compose_readiness(inputs),
        current_mission=compose_mission(inputs),
        recent_improvements=compose_improvements(inputs),
        current_risks=compose_risks(inputs),
        upcoming_milestones=compose_milestones(inputs),
        explanation_cards=compose_explanation_cards(inputs),
        celebration_moments=compose_celebrations(inputs),
    )


def compose_conversation(
    inputs: CoachInputs,
    *,
    conversation_id: ConversationId,
    context: CoachContext | None = None,
) -> ConversationContext:
    """Compose ConversationContext with deterministic suggested questions."""
    context = context or compose_context(
        inputs, coach_id=CoachId(f"coach:{inputs.student_id}:tmp")
    )
    questions = compose_suggested_questions(inputs, context=context)
    focus = context.current_focus
    opening = _opening_message(focus)
    digest = _context_digest(context)
    return ConversationContext(
        conversation_id=conversation_id,
        student_id=inputs.student_id,
        composed_at=inputs.as_of,
        opening_message=opening,
        focus_summary=focus.headline,
        suggested_questions=questions,
        context_digest=digest,
    )


def compose_reflection(inputs: CoachInputs) -> ReflectionPrompts:
    """Compose post-study reflection prompts."""
    execution = inputs.mission_execution
    has_study = (
        execution is not None
        and execution.status
        in (
            ExecutionStatus.COMPLETED,
            ExecutionStatus.STARTED,
            ExecutionStatus.RESUMED,
            ExecutionStatus.PAUSED,
        )
    ) or (
        inputs.workspace_snapshot is not None
        and inputs.workspace_snapshot.session_available
    )
    if not has_study:
        return ReflectionPrompts(
            available=False,
            prompts=(),
            summary="Reflection prompts will appear after you study.",
        )

    mission_label = None
    if execution is not None:
        mission_label = mission_title(execution.mission)
    elif inputs.workspace_snapshot is not None:
        mission_label = inputs.workspace_snapshot.mission_title

    scope = f" in {mission_label}" if mission_label else ""
    prompts = (
        ReflectionPrompt(
            kind=ReflectionPromptKind.MOST_DIFFICULT,
            prompt="What was most difficult today?",
            detail=f"Name the hardest moment{scope}.",
        ),
        ReflectionPrompt(
            kind=ReflectionPromptKind.BECAME_CLEARER,
            prompt="What became clearer?",
            detail="Capture one idea that clicked during this session.",
        ),
        ReflectionPrompt(
            kind=ReflectionPromptKind.STILL_UNCERTAIN,
            prompt="What still feels uncertain?",
            detail="Note anything you want to revisit next time.",
        ),
        ReflectionPrompt(
            kind=ReflectionPromptKind.CONFIDENCE,
            prompt="How confident do you feel about today's work?",
            detail="A quick confidence check helps track how study feels.",
        ),
    )
    return ReflectionPrompts(
        available=True,
        prompts=prompts,
        summary="Take a moment to reflect on today's study.",
    )


def compose_snapshot(
    context: CoachContext,
    *,
    snapshot_id: CoachSnapshotId,
    suggested_question_count: int = 0,
    reflection_prompt_count: int = 0,
) -> CoachSnapshot:
    """Project a CoachContext into a compact CoachSnapshot."""
    return CoachSnapshot(
        snapshot_id=snapshot_id,
        student_id=context.student_id,
        captured_at=context.composed_at,
        focus_headline=context.current_focus.headline,
        mission_title=context.current_mission.mission_title
        or context.current_focus.mission_title,
        readiness_label=context.readiness.readiness_label,
        journey_message=context.learning_journey.trajectory_message,
        explanation_card_count=len(context.explanation_cards.cards),
        suggested_question_count=suggested_question_count,
        reflection_prompt_count=reflection_prompt_count,
        celebration_count=len(context.celebration_moments.moments),
        improvement_count=len(context.recent_improvements),
        risk_count=len(context.current_risks),
        milestone_count=len(context.upcoming_milestones),
    )


def compose_focus(inputs: CoachInputs) -> FocusContext:
    home = inputs.home_snapshot
    workspace = inputs.workspace_snapshot
    execution = inputs.mission_execution

    if home is not None and home.focus_headline:
        return FocusContext(
            headline=home.focus_headline,
            reason=_focus_reason_from_home(home),
            mission_title=home.focus_mission_title,
            action_label=home.focus_action_label,
            has_focus=bool(home.focus_mission_title),
        )

    if workspace is not None and workspace.session_available:
        title = workspace.mission_title
        headline = (
            f"Today's focus is {title}."
            if title
            else workspace.primary_focus_prompt
        )
        return FocusContext(
            headline=headline,
            reason=workspace.primary_focus_prompt,
            mission_title=title,
            action_label="Continue current session",
            has_focus=True,
        )

    if execution is not None and execution.status in _ACTIVE_EXECUTION:
        title = mission_title(execution.mission)
        return FocusContext(
            headline=f"Today's focus is {title}.",
            reason="You're mid-mission — pick up where you left off.",
            mission_title=title,
            action_label="Continue current mission",
            has_focus=True,
        )

    pending = _next_pending_mission(inputs.mission_plan)
    if pending is not None:
        title = mission_title(pending)
        return FocusContext(
            headline=f"Your next mission is {title}.",
            reason="This is the next planned mission in your study plan.",
            mission_title=title,
            action_label="Start next mission",
            has_focus=True,
        )

    return FocusContext(
        headline="Nothing is queued for coaching right now.",
        reason="Your coach will update as study work and decisions appear.",
        mission_title=None,
        action_label=None,
        has_focus=False,
    )


def compose_journey(inputs: CoachInputs) -> JourneyContext:
    journey = inputs.journey_snapshot
    if journey is None:
        return JourneyContext(
            available=False,
            trajectory_message="Your learning journey will appear as you study.",
            consistency_message="Consistency signals will build with more sessions.",
            habits_message="Study habits will appear once you have a history.",
        )
    return JourneyContext(
        available=True,
        trajectory_message=journey.trajectory_message,
        consistency_message=journey.consistency_message,
        habits_message=journey.habits_message,
        weekly_missions_completed=journey.weekly_missions_completed,
        current_streak_days=journey.current_streak_days,
    )


def compose_readiness(inputs: CoachInputs) -> ReadinessContext:
    readiness = inputs.readiness_snapshot
    if readiness is None or not readiness.readiness_available:
        return ReadinessContext(
            available=False,
            readiness_label="Readiness not available yet",
            direction_message=(
                "Readiness will appear once an exam target and assessment exist."
            ),
            assessment_confidence_label="Not assessed",
        )
    return ReadinessContext(
        available=True,
        readiness_label=readiness.readiness_label,
        direction_message=readiness.direction_message,
        assessment_confidence_label=readiness.assessment_confidence_label,
        risk_count=readiness.risk_count,
        strength_count=readiness.strength_count,
        days_remaining=readiness.days_remaining,
        readiness_percent=readiness.readiness_percent,
    )


def compose_mission(inputs: CoachInputs) -> MissionContext:
    workspace = inputs.workspace_snapshot
    execution = inputs.mission_execution
    if workspace is not None and workspace.mission_title:
        completion = workspace.completion_percent
        progress = (
            f"{completion:.0f}% complete"
            if completion is not None
            else workspace.primary_focus_prompt
        )
        purpose = (
            f"Stay with {workspace.mission_title} — "
            f"{workspace.current_objective_label or 'continue the current objective'}."
        )
        return MissionContext(
            available=True,
            purpose=purpose,
            progress_summary=progress,
            mission_title=workspace.mission_title,
            completion_percent=completion,
            objective_label=workspace.current_objective_label,
        )

    if execution is not None:
        mission = execution.mission
        title = mission_title(mission)
        progress = _execution_progress_summary(execution)
        return MissionContext(
            available=True,
            purpose=mission_purpose(mission),
            progress_summary=progress,
            mission_title=title,
            completion_percent=_execution_completion_percent(execution),
            objective_label=study_objective_label(mission),
        )

    pending = _next_pending_mission(inputs.mission_plan)
    if pending is not None:
        return MissionContext(
            available=True,
            purpose=mission_purpose(pending),
            progress_summary="Not started yet",
            mission_title=mission_title(pending),
            completion_percent=0.0,
            objective_label=study_objective_label(pending),
        )

    return MissionContext(
        available=False,
        purpose="No current mission to explain.",
        progress_summary="Mission details will appear when a session is active.",
    )


def compose_improvements(inputs: CoachInputs) -> tuple[ImprovementItem, ...]:
    items: list[ImprovementItem] = []
    journey = inputs.journey_snapshot
    home = inputs.home_snapshot
    evaluation = inputs.evaluation

    if journey is not None and journey.mastery_trend is TrendDirection.IMPROVING:
        items.append(
            ImprovementItem(
                title="Mastery trend improving",
                message=journey.trajectory_message,
            )
        )
    if journey is not None and journey.weekly_missions_completed > 0:
        count = journey.weekly_missions_completed
        items.append(
            ImprovementItem(
                title="Weekly mission progress",
                message=(
                    f"You completed {count} mission"
                    f"{'s' if count != 1 else ''} this week."
                ),
            )
        )
    if home is not None and home.completed_missions > 0:
        items.append(
            ImprovementItem(
                title="Missions completed",
                message=home.progress_message,
            )
        )
    if evaluation is not None and evaluation.success and evaluation.summary is not None:
        summary = evaluation.summary
        if summary.knowledge_gap_count == 0:
            items.append(
                ImprovementItem(
                    title="No open knowledge gaps",
                    message="Your latest evaluation shows no open knowledge gaps.",
                )
            )
        elif summary.top_decision_category:
            category = humanise_identifier(summary.top_decision_category)
            items.append(
                ImprovementItem(
                    title="Top learning opportunity identified",
                    message=f"Your latest evaluation highlights {category}.",
                )
            )

    # Deduplicate by title while preserving order.
    seen: set[str] = set()
    unique: list[ImprovementItem] = []
    for item in items:
        if item.title in seen:
            continue
        seen.add(item.title)
        unique.append(item)
    return tuple(unique[:5])


def compose_risks(inputs: CoachInputs) -> tuple[RiskItem, ...]:
    items: list[RiskItem] = []
    readiness = inputs.readiness_snapshot
    evaluation = inputs.evaluation
    home = inputs.home_snapshot

    if readiness is not None and readiness.risk_count > 0:
        count = readiness.risk_count
        items.append(
            RiskItem(
                title="Readiness risks",
                message=(
                    f"{count} readiness risk{'s' if count != 1 else ''} "
                    f"need attention — {readiness.direction_message}"
                ),
            )
        )
    if evaluation is not None and evaluation.success and evaluation.summary is not None:
        gaps = evaluation.summary.knowledge_gap_count
        if gaps > 0:
            items.append(
                RiskItem(
                    title="Knowledge gaps",
                    message=(
                        f"{gaps} knowledge gap{'s' if gaps != 1 else ''} "
                        "remain in your latest evaluation."
                    ),
                )
            )
    if home is not None and home.current_streak_days == 0:
        items.append(
            RiskItem(
                title="Study streak reset",
                message=(
                    "Your study streak is at zero — a session today "
                    "rebuilds momentum."
                ),
            )
        )
    if (
        readiness is not None
        and readiness.days_remaining is not None
        and readiness.days_remaining <= 14
        and readiness.readiness_available
    ):
        items.append(
            RiskItem(
                title="Exam approaching",
                message=(
                    f"{readiness.days_remaining} day"
                    f"{'s' if readiness.days_remaining != 1 else ''} remain"
                    f"{'ing' if readiness.days_remaining != 1 else ''} until the exam."
                ),
            )
        )
    return tuple(items[:5])


def compose_milestones(inputs: CoachInputs) -> tuple[MilestoneItem, ...]:
    items: list[MilestoneItem] = []
    readiness = inputs.readiness_snapshot
    home = inputs.home_snapshot
    schedule = inputs.schedule
    today = inputs.as_of.date()

    if readiness is not None and readiness.days_remaining is not None:
        label = readiness.target_exam_label or "Exam"
        items.append(
            MilestoneItem(
                title=f"Exam: {label}",
                detail=f"{readiness.days_remaining} days remaining",
                days_until=readiness.days_remaining,
            )
        )
    elif (
        home is not None
        and home.exam_available
        and home.exam_days_remaining is not None
    ):
        items.append(
            MilestoneItem(
                title="Upcoming exam",
                detail=f"{home.exam_days_remaining} days remaining",
                days_until=home.exam_days_remaining,
            )
        )

    next_session = _next_future_session(schedule, today)
    if next_session is not None:
        days = (next_session.session_date - today).days
        items.append(
            MilestoneItem(
                title="Next study session",
                detail=f"{next_session.estimated_duration_minutes} minutes planned",
                days_until=days,
            )
        )

    checkpoint = _next_checkpoint_mission(inputs.mission_plan)
    if checkpoint is not None:
        items.append(
            MilestoneItem(
                title=mission_title(checkpoint),
                detail=study_objective_label(checkpoint),
                days_until=None,
            )
        )

    return tuple(items[:4])


def compose_explanation_cards(inputs: CoachInputs) -> ExplanationCards:
    cards: list[ExplanationCard] = []

    mission_card = _mission_purpose_card(inputs)
    if mission_card is not None:
        cards.append(mission_card)

    recommendation = _recommendation_rationale_card(inputs)
    if recommendation is not None:
        cards.append(recommendation)

    progress = _progress_summary_card(inputs)
    if progress is not None:
        cards.append(progress)

    readiness = _readiness_reasoning_card(inputs)
    if readiness is not None:
        cards.append(readiness)

    journey = _journey_highlights_card(inputs)
    if journey is not None:
        cards.append(journey)

    return ExplanationCards(cards=tuple(cards))


def compose_suggested_questions(
    inputs: CoachInputs, *, context: CoachContext | None = None
) -> SuggestedQuestions:
    context = context or compose_context(
        inputs, coach_id=CoachId(f"coach:{inputs.student_id}:tmp")
    )
    questions = (
        SuggestedQuestion(
            kind=SuggestedQuestionKind.WHY_NEXT_MISSION,
            prompt="Why is this my next mission?",
            rationale=_why_next_mission_rationale(inputs, context),
            enabled=(
                context.current_mission.available or context.current_focus.has_focus
            ),
        ),
        SuggestedQuestion(
            kind=SuggestedQuestionKind.WHAT_IMPROVED,
            prompt="What improved this week?",
            rationale=_what_improved_rationale(context),
            enabled=True,
        ),
        SuggestedQuestion(
            kind=SuggestedQuestionKind.WHY_READINESS,
            prompt="Why isn't my readiness higher?",
            rationale=_why_readiness_rationale(context),
            enabled=context.readiness.available,
        ),
        SuggestedQuestion(
            kind=SuggestedQuestionKind.FOCUS_TODAY,
            prompt="What should I focus on today?",
            rationale=context.current_focus.reason,
            enabled=True,
        ),
        SuggestedQuestion(
            kind=SuggestedQuestionKind.MISS_SESSION,
            prompt="What happens if I miss today's session?",
            rationale=_miss_session_rationale(inputs, context),
            enabled=inputs.schedule is not None
            or (inputs.home_snapshot is not None),
        ),
    )
    return SuggestedQuestions(questions=questions)


def compose_celebrations(inputs: CoachInputs) -> CelebrationMoments:
    moments: list[CelebrationMoment] = []
    home = inputs.home_snapshot
    journey = inputs.journey_snapshot

    streak = 0
    if journey is not None:
        streak = journey.current_streak_days
    elif home is not None:
        streak = home.current_streak_days

    if streak >= 7:
        moments.append(
            CelebrationMoment(
                kind=CelebrationKind.STUDY_STREAK,
                title="Seven-day study streak",
                message=f"You've studied {streak} days in a row — keep the rhythm.",
            )
        )
    elif streak >= 3:
        moments.append(
            CelebrationMoment(
                kind=CelebrationKind.STUDY_STREAK,
                title=f"{streak}-day study streak",
                message=f"You're on a {streak}-day study streak.",
            )
        )

    if journey is not None and journey.mastery_trend is TrendDirection.IMPROVING:
        subject_hint = _subject_improvement_hint(inputs)
        moments.append(
            CelebrationMoment(
                kind=CelebrationKind.MASTERY_IMPROVED,
                title=subject_hint or "Mastery improved",
                message=journey.trajectory_message,
            )
        )

    if _has_completed_revision_cycle(inputs):
        moments.append(
            CelebrationMoment(
                kind=CelebrationKind.FIRST_REVISION_CYCLE,
                title="Completed first revision cycle",
                message=(
                    "You've completed revision work — a strong habit "
                    "for lasting recall."
                ),
            )
        )

    if journey is not None and journey.weekly_missions_completed >= 3:
        moments.append(
            CelebrationMoment(
                kind=CelebrationKind.MISSION_STREAK,
                title="Strong weekly mission finish",
                message=(
                    f"{journey.weekly_missions_completed} missions completed this week."
                ),
            )
        )

    if home is not None and "strong" in home.momentum_message.lower():
        moments.append(
            CelebrationMoment(
                kind=CelebrationKind.CONSISTENCY,
                title="Consistency building",
                message=home.momentum_message,
            )
        )

    if not moments:
        return CelebrationMoments(
            moments=(),
            summary="Celebrations will appear as you make progress.",
        )
    return CelebrationMoments(
        moments=tuple(moments[:5]),
        summary=(
            f"{len(moments[:5])} moment"
            f"{'s' if len(moments[:5]) != 1 else ''} worth celebrating."
        ),
    )


# --- internal helpers -----------------------------------------------------


def _focus_reason_from_home(home) -> str:
    if home.focus_mission_title:
        return f"Your home focus is {home.focus_mission_title}."
    return home.focus_action_label or home.focus_headline


def _opening_message(focus: FocusContext) -> str:
    if focus.has_focus and focus.mission_title:
        return f"Let's look at why {focus.mission_title} is your focus right now."
    return "I can help explain your current study decisions."


def _context_digest(context: CoachContext) -> str:
    parts = [
        f"Focus: {context.current_focus.headline}",
        f"Journey: {context.learning_journey.trajectory_message}",
        f"Readiness: {context.readiness.readiness_label}",
    ]
    if context.current_mission.mission_title:
        parts.append(f"Mission: {context.current_mission.mission_title}")
    if context.recent_improvements:
        parts.append(f"Improvements: {context.recent_improvements[0].title}")
    if context.current_risks:
        parts.append(f"Risks: {context.current_risks[0].title}")
    return " | ".join(parts)


def _next_pending_mission(plan: MissionPlan | None) -> Mission | None:
    if plan is None or plan.is_empty():
        return None
    return sorted(plan.missions, key=lambda item: item.ordering.rank)[0]


def _next_checkpoint_mission(plan: MissionPlan | None) -> Mission | None:
    if plan is None:
        return None
    for mission in sorted(plan.missions, key=lambda item: item.ordering.rank):
        if mission.mission_type is MissionType.CHECKPOINT_PREPARATION:
            return mission
    return None


def _next_future_session(schedule: StudySchedule | None, today: date):
    if schedule is None:
        return None
    candidates = [
        session
        for session in schedule.active_sessions()
        if session.session_date > today
    ]
    if not candidates:
        # Also allow today's planned/in-progress as a near-term milestone.
        today_sessions = [
            session
            for session in schedule.sessions_on(today)
            if session.status
            in (SessionStatus.PLANNED, SessionStatus.IN_PROGRESS)
        ]
        if today_sessions:
            return sorted(
                today_sessions,
                key=lambda session: (session.start_time, session.sequence_index),
            )[0]
        return None
    return sorted(
        candidates, key=lambda session: (session.session_date, session.start_time)
    )[0]


def _execution_completion_percent(execution: MissionExecution) -> float:
    total = len(execution.mission.steps)
    if total == 0:
        return 0.0
    done = len(execution.completed_step_ids)
    return round((done / total) * 100.0, 2)


def _execution_progress_summary(execution: MissionExecution) -> str:
    total = len(execution.mission.steps)
    done = len(execution.completed_step_ids)
    if total == 0:
        return humanise_identifier(execution.status.value)
    return f"{done} of {total} steps complete"


def _mission_purpose_card(inputs: CoachInputs) -> ExplanationCard | None:
    mission: Mission | None = None
    if inputs.mission_execution is not None:
        mission = inputs.mission_execution.mission
    else:
        mission = _next_pending_mission(inputs.mission_plan)
    if mission is None and inputs.workspace_snapshot is not None:
        title = inputs.workspace_snapshot.mission_title
        if title:
            return ExplanationCard(
                kind=ExplanationCardKind.MISSION_PURPOSE,
                title="Mission purpose",
                body=(
                    f"{title} is your current mission. "
                    f"{inputs.workspace_snapshot.primary_focus_prompt}"
                ),
            )
        return None
    if mission is None:
        return None
    return ExplanationCard(
        kind=ExplanationCardKind.MISSION_PURPOSE,
        title="Mission purpose",
        body=f"{mission_title(mission)} — {mission_purpose(mission)}",
    )


def _recommendation_rationale_card(inputs: CoachInputs) -> ExplanationCard | None:
    evaluation = inputs.evaluation
    if evaluation is None or not evaluation.success:
        return None
    if evaluation.decisions:
        decision = min(evaluation.decisions, key=lambda item: item.rank)
        scope = humanise_identifier(decision.competency_id) or humanise_identifier(
            decision.subject_id
        )
        category = humanise_identifier(decision.category)
        reason = (
            decision.reason_summary
            or f"{category} was selected as the top action."
        )
        detail = f"{category}" if not scope else f"{category} for {scope}"
        return ExplanationCard(
            kind=ExplanationCardKind.RECOMMENDATION_RATIONALE,
            title="Recommendation rationale",
            body=f"Your top recommendation is {detail}. {reason}",
        )
    if evaluation.summary is not None and evaluation.summary.top_decision_category:
        category = humanise_identifier(evaluation.summary.top_decision_category)
        return ExplanationCard(
            kind=ExplanationCardKind.RECOMMENDATION_RATIONALE,
            title="Recommendation rationale",
            body=f"Your latest evaluation highlights {category} as the top category.",
        )
    return None


def _progress_summary_card(inputs: CoachInputs) -> ExplanationCard | None:
    home = inputs.home_snapshot
    journey = inputs.journey_snapshot
    if home is not None:
        return ExplanationCard(
            kind=ExplanationCardKind.PROGRESS_SUMMARY,
            title="Progress summary",
            body=(
                f"{home.progress_message} "
                f"Completed missions: {home.completed_missions}. "
                f"{home.momentum_message}"
            ),
        )
    if journey is not None:
        return ExplanationCard(
            kind=ExplanationCardKind.PROGRESS_SUMMARY,
            title="Progress summary",
            body=(
                f"{journey.trajectory_message} "
                f"Weekly missions completed: {journey.weekly_missions_completed}."
            ),
        )
    return None


def _readiness_reasoning_card(inputs: CoachInputs) -> ExplanationCard | None:
    readiness = inputs.readiness_snapshot
    if readiness is None or not readiness.readiness_available:
        return None
    percent = (
        f" ({readiness.readiness_percent:.0f}%)"
        if readiness.readiness_percent is not None
        else ""
    )
    return ExplanationCard(
        kind=ExplanationCardKind.READINESS_REASONING,
        title="Readiness reasoning",
        body=(
            f"Readiness is {readiness.readiness_label}{percent}. "
            f"{readiness.direction_message} "
            f"Assessment confidence: {readiness.assessment_confidence_label}."
        ),
    )


def _journey_highlights_card(inputs: CoachInputs) -> ExplanationCard | None:
    journey = inputs.journey_snapshot
    if journey is None:
        return None
    return ExplanationCard(
        kind=ExplanationCardKind.JOURNEY_HIGHLIGHTS,
        title="Journey highlights",
        body=(
            f"{journey.trajectory_message} "
            f"{journey.consistency_message} "
            f"{journey.habits_message}"
        ),
    )


def _why_next_mission_rationale(inputs: CoachInputs, context: CoachContext) -> str:
    if inputs.mission_execution is not None:
        mission = inputs.mission_execution.mission
        return f"{mission_title(mission)} — {mission_purpose(mission)}"
    if context.current_mission.available and context.current_mission.purpose:
        title = context.current_mission.mission_title or "Your next mission"
        return f"{title} — {context.current_mission.purpose}"
    return "Your next mission comes from the current study plan and schedule."


def _what_improved_rationale(context: CoachContext) -> str:
    if context.recent_improvements:
        first = context.recent_improvements[0]
        return f"{first.title}: {first.message}"
    return "Weekly improvements will appear as you complete more study work."


def _why_readiness_rationale(context: CoachContext) -> str:
    if not context.readiness.available:
        return (
            "Readiness needs an exam target and assessment "
            "before it can be explained."
        )
    parts = [context.readiness.direction_message]
    if context.readiness.risk_count > 0:
        parts.append(
            f"{context.readiness.risk_count} readiness risk"
            f"{'s' if context.readiness.risk_count != 1 else ''} are in focus."
        )
    if context.current_risks:
        parts.append(context.current_risks[0].message)
    return " ".join(parts)


def _miss_session_rationale(inputs: CoachInputs, context: CoachContext) -> str:
    today = inputs.as_of.date()
    session = None
    if inputs.schedule is not None:
        sessions = [
            item
            for item in inputs.schedule.sessions_on(today)
            if item.status is not SessionStatus.CANCELLED
        ]
        if sessions:
            session = sorted(
                sessions, key=lambda item: (item.start_time, item.sequence_index)
            )[0]
    if session is not None:
        return (
            f"Missing today's {session.estimated_duration_minutes}-minute session "
            "pauses momentum and may delay scheduled missions."
        )
    if context.current_focus.has_focus:
        return (
            "Skipping today delays your current focus and weakens study consistency."
        )
    return (
        "Missing a planned session reduces consistency and can "
        "push milestones later."
    )


def _subject_improvement_hint(inputs: CoachInputs) -> str | None:
    evaluation: EducationalEvaluation | None = inputs.evaluation
    if evaluation is None or not evaluation.decisions:
        return None
    decision = min(evaluation.decisions, key=lambda item: item.rank)
    subject = humanise_identifier(decision.subject_id)
    if subject:
        return f"{subject} mastery improved"
    return None


def _has_completed_revision_cycle(inputs: CoachInputs) -> bool:
    execution = inputs.mission_execution
    if execution is not None and execution.status is ExecutionStatus.COMPLETED:
        if is_revision_mission(execution.mission):
            return True
    plan = inputs.mission_plan
    has_revision_in_plan = plan is not None and any(
        mission.mission_type in _REVISION_TYPES for mission in plan.missions
    )
    if not has_revision_in_plan:
        return False
    # Celebrate when revision work is in the plan and study progress exists.
    home = inputs.home_snapshot
    if home is not None and home.completed_missions >= 1:
        return True
    journey = inputs.journey_snapshot
    if journey is not None and journey.weekly_missions_completed >= 1:
        return True
    return False

