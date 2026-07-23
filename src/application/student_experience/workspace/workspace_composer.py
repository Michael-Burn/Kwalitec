"""Workspace composition helpers — project Education OS outputs to view models.

Composition only. No mastery estimation, recommendation generation,
mission generation, scheduling, persistence, timers, or AI.
"""

from __future__ import annotations

from datetime import date

from application.education.mission_execution.enums import ConfidenceTrend
from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)
from application.education.mission_generation.enums import MissionType
from application.education.mission_generation.models.mission import Mission
from application.education.mission_generation.models.mission_plan import MissionPlan
from application.education.mission_generation.models.mission_step import MissionStep
from application.education.revision_planner.enums import SessionStatus
from application.education.revision_planner.models.study_schedule import StudySchedule
from application.student_experience.workspace.enums import (
    FocusPromptKind,
    ObjectiveStatus,
    PriorityLabel,
    QualityIndicatorKind,
    ResourceKind,
    SessionPresence,
    TimerDisplayState,
)
from application.student_experience.workspace.ids import (
    WorkspaceId,
    WorkspaceSnapshotId,
)
from application.student_experience.workspace.models.completion_card import (
    CompletionCard,
)
from application.student_experience.workspace.models.current_session_card import (
    CurrentSessionCard,
)
from application.student_experience.workspace.models.focus_card import (
    FocusCard,
    FocusPrompt,
)
from application.student_experience.workspace.models.mission_card import MissionCard
from application.student_experience.workspace.models.objectives_card import (
    ObjectiveItem,
    ObjectivesCard,
)
from application.student_experience.workspace.models.progress_card import (
    ProgressCard,
    QualityIndicator,
)
from application.student_experience.workspace.models.reflection_card import (
    ReflectionCard,
)
from application.student_experience.workspace.models.resources_card import (
    ResourceItem,
    ResourcesCard,
)
from application.student_experience.workspace.models.session_timer_card import (
    SessionTimerCard,
)
from application.student_experience.workspace.models.study_workspace_view_model import (
    StudyWorkspaceViewModel,
)
from application.student_experience.workspace.models.workspace_snapshot import (
    WorkspaceSnapshot,
)
from application.student_experience.workspace.ports.workspace_resource_provider import (
    WorkspaceResource,
)
from application.student_experience.workspace.presentation import (
    confidence_trend_label,
    format_minutes,
    format_seconds_as_minutes,
    humanise_identifier,
    is_checkpoint_mission,
    mission_purpose,
    mission_title,
    objective_code_label,
    priority_from_band,
    priority_label,
    step_action_label,
    study_objective_label,
    timer_state_from_execution,
    timer_state_from_session,
)
from application.student_experience.workspace.workspace_inputs import WorkspaceInputs

_PREREQUISITE_TYPES = frozenset(
    {
        MissionType.REVISE_PREREQUISITE,
        MissionType.STRENGTHEN_FOUNDATION,
    }
)

_INACTIVE_SESSION = frozenset(
    {
        SessionStatus.CANCELLED,
        SessionStatus.RESCHEDULED,
        SessionStatus.COMPLETED,
    }
)

_RESOURCE_KIND_MAP: dict[str, ResourceKind] = {
    "task": ResourceKind.TASK,
    "reference": ResourceKind.REFERENCE,
    "tip": ResourceKind.TIP,
    "checkpoint": ResourceKind.CHECKPOINT,
}


def compose_workspace(
    inputs: WorkspaceInputs,
    *,
    workspace_id: WorkspaceId,
    resources: tuple[WorkspaceResource, ...] = (),
) -> StudyWorkspaceViewModel:
    """Compose a full StudyWorkspaceViewModel from Education OS outputs."""
    mission = _resolve_mission(inputs)
    objectives = compose_objectives(inputs, mission=mission)
    return StudyWorkspaceViewModel(
        workspace_id=workspace_id,
        student_id=inputs.student_id,
        composed_at=inputs.as_of,
        current_session=compose_current_session(
            inputs, mission=mission, objectives=objectives
        ),
        mission=compose_mission(inputs, mission=mission),
        objectives=objectives,
        resources=compose_resources(resources),
        progress=compose_progress(inputs, mission=mission),
        focus=compose_focus(inputs, mission=mission, objectives=objectives),
        session_timer=compose_session_timer(inputs, mission=mission),
        reflection=compose_reflection(inputs),
        completion=compose_completion(inputs),
    )


def compose_snapshot(
    workspace: StudyWorkspaceViewModel,
    *,
    snapshot_id: WorkspaceSnapshotId,
) -> WorkspaceSnapshot:
    """Project a StudyWorkspaceViewModel into a compact WorkspaceSnapshot."""
    primary = workspace.focus.primary
    return WorkspaceSnapshot(
        snapshot_id=snapshot_id,
        student_id=workspace.student_id,
        captured_at=workspace.composed_at,
        session_available=workspace.current_session.available,
        session_presence=workspace.current_session.presence,
        mission_title=workspace.current_session.mission_title,
        completion_percent=workspace.progress.completion_percent,
        remaining_minutes=workspace.session_timer.remaining_minutes,
        current_objective_label=(
            workspace.objectives.current.label
            if workspace.objectives.current is not None
            else None
        ),
        primary_focus_kind=(
            primary.kind if primary is not None else FocusPromptKind.NONE
        ),
        primary_focus_prompt=(
            primary.prompt
            if primary is not None
            else "Open your study workspace when a session is ready."
        ),
        objective_count=len(workspace.objectives.items),
        completed_objective_count=len(workspace.objectives.completed),
        remaining_objective_count=len(workspace.objectives.remaining),
        resource_count=len(workspace.resources.items),
        next_session_preview=workspace.completion.next_session_preview,
        readiness_impact_summary=workspace.completion.readiness_impact_summary,
    )


def compose_current_session(
    inputs: WorkspaceInputs,
    *,
    mission: Mission | None = None,
    objectives: ObjectivesCard | None = None,
) -> CurrentSessionCard:
    """Compose current mission, remaining duration, objectives, estimated completion."""
    mission = mission if mission is not None else _resolve_mission(inputs)
    objectives = objectives or compose_objectives(inputs, mission=mission)
    session = inputs.current_session

    if session is None and mission is None:
        return CurrentSessionCard(
            available=False,
            presence=SessionPresence.UNAVAILABLE,
            session_id=None,
            mission_id=None,
            mission_title=None,
            remaining_duration_minutes=None,
            remaining_duration_label="—",
            objectives_preview=(),
            estimated_completion_label="No session is ready yet.",
            summary="A study session will appear when one is scheduled.",
        )

    title = mission_title(mission) if mission is not None else "Scheduled study session"
    remaining = _remaining_duration_minutes(inputs, mission=mission)
    preview = tuple(item.label for item in objectives.items[:3])
    if not preview and mission is not None:
        preview = (study_objective_label(mission),)
    estimated = (
        f"Estimated completion in {format_minutes(remaining)}."
        if remaining is not None
        else "Estimated completion will appear once timing is available."
    )
    return CurrentSessionCard(
        available=True,
        presence=SessionPresence.AVAILABLE,
        session_id=session.session_id.value if session is not None else None,
        mission_id=str(mission.mission_id) if mission is not None else None,
        mission_title=title,
        remaining_duration_minutes=remaining,
        remaining_duration_label=format_minutes(remaining),
        objectives_preview=preview,
        estimated_completion_label=estimated,
        summary=f"Current session focuses on {title}.",
    )


def compose_mission(
    inputs: WorkspaceInputs,
    *,
    mission: Mission | None = None,
) -> MissionCard:
    """Compose mission title, purpose, priority, and satisfied dependencies."""
    mission = mission if mission is not None else _resolve_mission(inputs)
    if mission is None:
        return MissionCard(
            available=False,
            mission_id=None,
            title="No mission available",
            purpose="A mission will appear when your study session begins.",
            priority=PriorityLabel.UNKNOWN,
            priority_label=priority_label(PriorityLabel.UNKNOWN),
            dependencies_satisfied=True,
            dependencies_summary="No mission dependencies to check yet.",
            dependency_labels=(),
        )

    priority = priority_from_band(mission.ordering.priority_band)
    deps = _dependency_labels(inputs.mission_plan, mission)
    satisfied = True
    if deps:
        summary = (
            "Dependencies already satisfied by plan order: "
            + "; ".join(deps)
            + "."
        )
    else:
        summary = "Dependencies already satisfied — no outstanding prerequisites."
    return MissionCard(
        available=True,
        mission_id=str(mission.mission_id),
        title=mission_title(mission),
        purpose=mission_purpose(mission),
        priority=priority,
        priority_label=priority_label(priority),
        dependencies_satisfied=satisfied,
        dependencies_summary=summary,
        dependency_labels=deps,
    )


def compose_objectives(
    inputs: WorkspaceInputs,
    *,
    mission: Mission | None = None,
) -> ObjectivesCard:
    """Compose ordered objectives with current / completed / remaining views."""
    mission = mission if mission is not None else _resolve_mission(inputs)
    execution = inputs.mission_execution
    session = inputs.current_session

    items: list[ObjectiveItem] = []
    if execution is not None and execution.mission.steps:
        completed_ids = set(execution.completed_step_ids)
        skipped_ids = set(execution.skipped_step_ids)
        current_id = execution.current_step_id
        for step in sorted(execution.mission.steps, key=lambda item: item.order):
            items.append(
                _objective_from_step(
                    step,
                    completed_ids=completed_ids,
                    skipped_ids=skipped_ids,
                    current_id=current_id,
                )
            )
    elif mission is not None and mission.steps:
        for step in sorted(mission.steps, key=lambda item: item.order):
            items.append(
                ObjectiveItem(
                    objective_id=str(step.step_id),
                    label=_step_label(step),
                    status=ObjectiveStatus.REMAINING,
                    order=step.order,
                    estimated_minutes=step.estimated_minutes,
                )
            )
    elif mission is not None:
        items.append(
            ObjectiveItem(
                objective_id=f"objective:{mission.mission_id.value}",
                label=study_objective_label(mission),
                status=ObjectiveStatus.CURRENT,
                order=1,
                estimated_minutes=mission.estimate.duration_minutes,
            )
        )
    elif session is not None and session.objectives:
        for index, code in enumerate(session.objectives, start=1):
            items.append(
                ObjectiveItem(
                    objective_id=f"session-objective:{index}:{code.value}",
                    label=objective_code_label(code),
                    status=(
                        ObjectiveStatus.CURRENT
                        if index == 1
                        else ObjectiveStatus.REMAINING
                    ),
                    order=index,
                )
            )

    if not items:
        return ObjectivesCard(
            items=(),
            current=None,
            completed=(),
            remaining=(),
            has_objectives=False,
            summary="Objectives will appear when a mission is ready.",
        )

    current = next(
        (item for item in items if item.status is ObjectiveStatus.CURRENT), None
    )
    completed = tuple(
        item for item in items if item.status is ObjectiveStatus.COMPLETED
    )
    remaining = tuple(
        item
        for item in items
        if item.status in (ObjectiveStatus.REMAINING, ObjectiveStatus.CURRENT)
    )
    if current is not None:
        summary = f"Current objective: {current.label}."
    elif completed and not remaining:
        summary = "All objectives for this session are complete."
    else:
        count = len(remaining)
        noun = "objective" if count == 1 else "objectives"
        summary = f"{count} {noun} remaining."
    return ObjectivesCard(
        items=tuple(items),
        current=current,
        completed=completed,
        remaining=remaining,
        has_objectives=True,
        summary=summary,
    )


def compose_resources(
    resources: tuple[WorkspaceResource, ...] = (),
) -> ResourcesCard:
    """Compose resources from the optional provider — never invent content."""
    if not resources:
        return ResourcesCard(
            items=(),
            has_resources=False,
            summary="Study resources will appear when available.",
        )
    items = tuple(
        ResourceItem(
            resource_id=resource.resource_id,
            title=resource.title,
            detail=resource.detail or resource.title,
            kind=_RESOURCE_KIND_MAP.get(
                (resource.kind or "other").strip().lower(), ResourceKind.OTHER
            ),
            estimated_minutes=resource.estimated_minutes,
        )
        for resource in resources
    )
    return ResourcesCard(
        items=items,
        has_resources=True,
        summary=f"{len(items)} study resource{'s' if len(items) != 1 else ''} ready.",
    )


def compose_progress(
    inputs: WorkspaceInputs,
    *,
    mission: Mission | None = None,
) -> ProgressCard:
    """Compose completion, time invested, remaining work, and quality indicators."""
    mission = mission if mission is not None else _resolve_mission(inputs)
    execution = inputs.mission_execution

    if execution is None and mission is None and inputs.current_session is None:
        return ProgressCard(
            available=False,
            completion_percent=None,
            completion_label="Progress not available yet",
            time_invested_minutes=None,
            time_invested_label="—",
            remaining_work_minutes=None,
            remaining_work_label="—",
            quality_indicators=(),
            summary="Progress will appear once you start the session.",
        )

    completion: float | None = None
    elapsed_minutes: int | None = None
    remaining_minutes = _remaining_duration_minutes(inputs, mission=mission)
    indicators: list[QualityIndicator] = []

    if execution is not None:
        progress = execution.progress
        metrics = execution.metrics
        completion = float(progress.completion_percentage)
        elapsed_minutes = int(round(execution.elapsed_study_time_seconds / 60.0))
        indicators.extend(_quality_from_metrics(metrics.confidence_trend, metrics))
    elif inputs.current_session is not None:
        session = inputs.current_session
        if session.status is SessionStatus.COMPLETED:
            completion = 100.0
            if session.completion_metrics is not None:
                elapsed_minutes = session.completion_metrics.actual_duration_minutes
            else:
                elapsed_minutes = session.estimated_duration_minutes
            remaining_minutes = 0
        else:
            completion = 0.0
            elapsed_minutes = 0
            remaining_minutes = session.estimated_duration_minutes

    completion_label = (
        f"{completion:.0f}% complete"
        if completion is not None
        else "Completion not available yet"
    )
    return ProgressCard(
        available=True,
        completion_percent=completion,
        completion_label=completion_label,
        time_invested_minutes=elapsed_minutes,
        time_invested_label=format_minutes(elapsed_minutes),
        remaining_work_minutes=remaining_minutes,
        remaining_work_label=format_minutes(remaining_minutes),
        quality_indicators=tuple(indicators),
        summary=(
            f"{completion_label}. "
            f"Time invested: {format_minutes(elapsed_minutes)}. "
            f"Remaining work: {format_minutes(remaining_minutes)}."
        ),
    )


def compose_focus(
    inputs: WorkspaceInputs,
    *,
    mission: Mission | None = None,
    objectives: ObjectivesCard | None = None,
) -> FocusCard:
    """Compose deterministic focus prompts — never generate recommendations."""
    mission = mission if mission is not None else _resolve_mission(inputs)
    objectives = objectives or compose_objectives(inputs, mission=mission)
    execution = inputs.mission_execution
    prompts: list[FocusPrompt] = []

    if objectives.current is not None:
        prompts.append(
            FocusPrompt(
                kind=FocusPromptKind.CONTINUE_CURRENT_OBJECTIVE,
                title="Continue current objective",
                prompt=f"Continue: {objectives.current.label}.",
            )
        )

    if execution is not None and execution.current_step is not None:
        step = execution.current_step
        prompts.append(
            FocusPrompt(
                kind=FocusPromptKind.FINISH_CURRENT_STEP,
                title="Finish current step",
                prompt=f"Finish this step: {_step_label(step)}.",
            )
        )

    if is_checkpoint_mission(mission):
        prompts.append(
            FocusPrompt(
                kind=FocusPromptKind.PREPARE_CHECKPOINT,
                title="Prepare checkpoint",
                prompt="Prepare for your checkpoint with the current mission work.",
            )
        )

    if _should_review_previous_mistake(execution):
        prompts.append(
            FocusPrompt(
                kind=FocusPromptKind.REVIEW_PREVIOUS_MISTAKE,
                title="Review previous mistake",
                prompt="Review the previous mistake before continuing.",
            )
        )

    # Deduplicate by kind while preserving insertion order.
    unique: list[FocusPrompt] = []
    seen: set[FocusPromptKind] = set()
    for prompt in prompts:
        if prompt.kind in seen:
            continue
        seen.add(prompt.kind)
        unique.append(prompt)

    if not unique:
        return FocusCard(
            prompts=(),
            primary=None,
            has_prompts=False,
            summary="Focus prompts will appear when a session is active.",
        )

    return FocusCard(
        prompts=tuple(unique),
        primary=unique[0],
        has_prompts=True,
        summary=unique[0].prompt,
    )


def compose_session_timer(
    inputs: WorkspaceInputs,
    *,
    mission: Mission | None = None,
) -> SessionTimerCard:
    """Compose display-only timing values — never implement a live timer."""
    mission = mission if mission is not None else _resolve_mission(inputs)
    execution = inputs.mission_execution
    session = inputs.current_session

    if execution is None and session is None and mission is None:
        return SessionTimerCard(
            available=False,
            display_state=TimerDisplayState.UNAVAILABLE,
            planned_minutes=None,
            planned_label="—",
            elapsed_minutes=None,
            elapsed_label="—",
            remaining_minutes=None,
            remaining_label="—",
            summary="Session timing will appear when a session is available.",
        )

    planned = None
    if session is not None:
        planned = session.estimated_duration_minutes
    elif mission is not None:
        planned = mission.estimate.duration_minutes

    elapsed = None
    if execution is not None:
        elapsed = int(round(execution.elapsed_study_time_seconds / 60.0))
        display_state = timer_state_from_execution(execution.status)
    elif session is not None:
        elapsed = 0
        display_state = timer_state_from_session(session.status)
    else:
        elapsed = 0
        display_state = TimerDisplayState.IDLE

    remaining = _remaining_duration_minutes(inputs, mission=mission)
    return SessionTimerCard(
        available=True,
        display_state=display_state,
        planned_minutes=planned,
        planned_label=format_minutes(planned),
        elapsed_minutes=elapsed,
        elapsed_label=format_minutes(elapsed),
        remaining_minutes=remaining,
        remaining_label=format_minutes(remaining),
        summary=(
            f"Planned {format_minutes(planned)}; "
            f"elapsed {format_minutes(elapsed)}; "
            f"remaining {format_minutes(remaining)}."
        ),
    )


def compose_reflection(inputs: WorkspaceInputs) -> ReflectionCard:
    """Compose reflection prompt, confidence reminder, and notes placeholder."""
    execution = inputs.mission_execution
    prior_count = (
        len(execution.reflection_history) if execution is not None else 0
    )
    confidence = None
    if execution is not None and execution.confidence is not None:
        confidence = execution.confidence.level.value.replace("_", " ")

    reflection_prompt = (
        "Take a moment to reflect on what felt clear and what still needs work."
    )
    if prior_count > 0:
        reflection_prompt = (
            "Add a closing reflection for this session — "
            "what progressed, and what will you revisit next?"
        )

    confidence_reminder = (
        f"Remember to note your confidence after this session "
        f"(last recorded: {confidence})."
        if confidence is not None
        else "Remember to note your confidence after this session."
    )
    return ReflectionCard(
        available=True,
        reflection_prompt=reflection_prompt,
        confidence_reminder=confidence_reminder,
        notes_placeholder="Session notes (optional)",
        prior_reflection_count=prior_count,
        summary=reflection_prompt,
    )


def compose_completion(inputs: WorkspaceInputs) -> CompletionCard:
    """Compose next session preview, upcoming milestone, readiness impact."""
    today = inputs.as_of.date()
    next_session, next_date = _next_session_preview(inputs.schedule, today)
    milestone = _upcoming_milestone(inputs)
    readiness = _readiness_impact_summary(inputs)
    return CompletionCard(
        available=True,
        next_session_preview=next_session,
        next_session_date=next_date,
        upcoming_milestone=milestone,
        readiness_impact_summary=readiness,
        summary=f"{next_session} {milestone}",
    )


# --- internal helpers -----------------------------------------------------


def _resolve_mission(inputs: WorkspaceInputs) -> Mission | None:
    execution = inputs.mission_execution
    if execution is not None:
        return execution.mission

    session = inputs.current_session
    plan = inputs.mission_plan
    if session is not None and plan is not None:
        for mission_id in session.scheduled_mission_ids:
            for mission in plan.missions:
                if mission.mission_id == mission_id:
                    return mission

    if plan is not None and plan.missions:
        return plan.missions[0]
    return None


def _remaining_duration_minutes(
    inputs: WorkspaceInputs,
    *,
    mission: Mission | None,
) -> int | None:
    execution = inputs.mission_execution
    if execution is not None:
        planned = mission.estimate.duration_minutes if mission is not None else None
        if planned is None:
            planned = int(
                round(execution.metrics.mission_duration_seconds / 60.0)
            )
        elapsed = int(round(execution.elapsed_study_time_seconds / 60.0))
        return max(0, planned - elapsed)

    session = inputs.current_session
    if session is not None:
        return session.estimated_duration_minutes
    if mission is not None:
        return mission.estimate.duration_minutes
    return None


def _objective_from_step(
    step: MissionStep,
    *,
    completed_ids: set,
    skipped_ids: set,
    current_id,
) -> ObjectiveItem:
    if step.step_id in completed_ids:
        status = ObjectiveStatus.COMPLETED
    elif step.step_id in skipped_ids:
        status = ObjectiveStatus.SKIPPED
    elif current_id is not None and step.step_id == current_id:
        status = ObjectiveStatus.CURRENT
    else:
        status = ObjectiveStatus.REMAINING
    return ObjectiveItem(
        objective_id=str(step.step_id),
        label=_step_label(step),
        status=status,
        order=step.order,
        estimated_minutes=step.estimated_minutes,
    )


def _step_label(step: MissionStep) -> str:
    base = step_action_label(step.action)
    scope = humanise_identifier(step.competency_id) or humanise_identifier(
        step.subject_id
    )
    detail = (step.action_detail or "").strip()
    if detail:
        return f"{base}: {detail}"
    if scope:
        return f"{base} — {scope}"
    return base


def _dependency_labels(
    plan: MissionPlan | None, mission: Mission
) -> tuple[str, ...]:
    if plan is None:
        return ()
    labels: list[str] = []
    for candidate in plan.missions:
        if candidate.mission_id == mission.mission_id:
            break
        is_prereq = (
            candidate.mission_type in _PREREQUISITE_TYPES
            or candidate.is_prerequisite()
        )
        same_subject_prereq = (
            candidate.subject_id == mission.subject_id
            and candidate.mission_type is MissionType.REVISE_PREREQUISITE
            and candidate.ordering.rank < mission.ordering.rank
        )
        if is_prereq or same_subject_prereq:
            labels.append(mission_title(candidate))
    # Also surface REQUIRE_PREREQUISITE_FIRST constraints as satisfied ordering.
    for constraint in mission.constraints:
        if constraint.requires_prerequisite_first():
            label = constraint.label or humanise_identifier(constraint.competency_id)
            if label and label not in labels:
                labels.append(label)
    return tuple(labels)


def _quality_from_metrics(trend: ConfidenceTrend, metrics) -> list[QualityIndicator]:
    indicators: list[QualityIndicator] = [
        QualityIndicator(
            kind=QualityIndicatorKind.COMPLETION_RATE,
            label="Completion rate",
            message=(
                f"Step completion rate is "
                f"{round(float(metrics.step_completion_rate) * 100.0):.0f}%."
            ),
        ),
        QualityIndicator(
            kind=QualityIndicatorKind.TIME_ON_TASK,
            label="Time on task",
            message=(
                f"Time invested so far: "
                f"{format_seconds_as_minutes(metrics.elapsed_study_time_seconds)}."
            ),
        ),
        QualityIndicator(
            kind=QualityIndicatorKind.CONFIDENCE_TREND,
            label="Confidence trend",
            message=f"{confidence_trend_label(trend)}.",
        ),
    ]
    if metrics.reflection_count > 0:
        count = metrics.reflection_count
        indicators.append(
            QualityIndicator(
                kind=QualityIndicatorKind.REFLECTION_ACTIVITY,
                label="Reflection activity",
                message=(
                    f"You have recorded {count} reflection"
                    f"{'s' if count != 1 else ''} in this session."
                ),
            )
        )
    return indicators


def _should_review_previous_mistake(execution: MissionExecution | None) -> bool:
    if execution is None:
        return False
    if execution.skipped_step_ids:
        return True
    if execution.metrics.confidence_trend is ConfidenceTrend.FALLING:
        return True
    return False


def _next_session_preview(
    schedule: StudySchedule | None, today: date
) -> tuple[str, date | None]:
    if schedule is None:
        return "Next session will appear when your schedule is ready.", None
    candidates = [
        session
        for session in schedule.sessions
        if session.session_date > today and session.status not in _INACTIVE_SESSION
    ]
    if not candidates:
        # Fall back to a later session today after the current one.
        later_today = [
            session
            for session in schedule.sessions
            if session.session_date == today
            and session.status not in _INACTIVE_SESSION
        ]
        if len(later_today) > 1:
            ordered = sorted(
                later_today,
                key=lambda session: (session.start_time, session.sequence_index),
            )
            nxt = ordered[1]
            return (
                f"Next session today at {nxt.start_time.strftime('%H:%M')}.",
                nxt.session_date,
            )
        return "No further sessions are scheduled yet.", None
    nxt = sorted(
        candidates, key=lambda session: (session.session_date, session.start_time)
    )[0]
    return (
        f"Next session on {nxt.session_date.isoformat()} "
        f"at {nxt.start_time.strftime('%H:%M')}.",
        nxt.session_date,
    )


def _upcoming_milestone(inputs: WorkspaceInputs) -> str:
    if inputs.readiness_snapshot is not None:
        readiness = inputs.readiness_snapshot
        if readiness.days_remaining is not None and readiness.target_exam_label:
            days = readiness.days_remaining
            return (
                f"Upcoming milestone: {readiness.target_exam_label} "
                f"in {days} day{'s' if days != 1 else ''}."
            )
        if readiness.milestone_count > 0:
            return (
                f"You have {readiness.milestone_count} readiness milestone"
                f"{'s' if readiness.milestone_count != 1 else ''} ahead."
            )
    if inputs.journey_snapshot is not None and inputs.journey_snapshot.milestone_count:
        count = inputs.journey_snapshot.milestone_count
        return (
            f"You have {count} learning journey milestone"
            f"{'s' if count != 1 else ''} ahead."
        )
    if (
        inputs.home_snapshot is not None
        and inputs.home_snapshot.exam_days_remaining is not None
    ):
        days = inputs.home_snapshot.exam_days_remaining
        label = inputs.home_snapshot.exam_readiness_label or "exam"
        return f"Upcoming milestone: {label} in {days} day{'s' if days != 1 else ''}."
    return "Upcoming milestones will appear as your plan develops."


def _readiness_impact_summary(inputs: WorkspaceInputs) -> str:
    if inputs.readiness_snapshot is not None:
        readiness = inputs.readiness_snapshot
        if readiness.readiness_available:
            parts = [f"Current readiness: {readiness.readiness_label}."]
            if readiness.direction_message:
                parts.append(readiness.direction_message)
            return " ".join(parts)
        return "Readiness impact will appear once an assessment is available."
    if inputs.home_snapshot is not None and inputs.home_snapshot.exam_available:
        label = inputs.home_snapshot.exam_readiness_label or "available"
        return f"Exam readiness is currently {label}."
    if inputs.journey_snapshot is not None:
        return inputs.journey_snapshot.trajectory_message
    return "Readiness impact will appear as study evidence builds."
