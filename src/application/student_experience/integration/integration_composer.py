"""Experience Integration composers — chain XP modules without new reasoning.

Composition only. Never estimates mastery, generates recommendations,
generates missions, schedules work, persists data, or invokes AI.
"""

from __future__ import annotations

from dataclasses import replace

from application.student_experience.coach.coach_inputs import CoachInputs
from application.student_experience.coach.learning_coach_service import (
    LearningCoachService,
)
from application.student_experience.coach.models.celebration_moments import (
    CelebrationMoments,
)
from application.student_experience.home.enums import FocusActionKind
from application.student_experience.home.home_inputs import HomeInputs
from application.student_experience.home.models.home_view_model import HomeViewModel
from application.student_experience.home.student_home_service import StudentHomeService
from application.student_experience.integration.enums import (
    CascadeStep,
    IntegrationTrigger,
    JourneySurface,
)
from application.student_experience.integration.ids import ExperienceBundleId
from application.student_experience.integration.integration_inputs import (
    IntegrationInputs,
)
from application.student_experience.integration.models import (
    ExperienceJourneyViewModel,
    IntegratedNextAction,
    ReadinessChangeNotice,
    SurfaceState,
)
from application.student_experience.integration.navigation import next_action_from_focus
from application.student_experience.progress.journey_inputs import JourneyInputs
from application.student_experience.progress.learning_journey_service import (
    LearningJourneyService,
)
from application.student_experience.readiness.exam_readiness_service import (
    ExamReadinessService,
)
from application.student_experience.readiness.models.readiness_snapshot import (
    ReadinessSnapshot,
)
from application.student_experience.readiness.readiness_inputs import ReadinessInputs
from application.student_experience.workspace.study_workspace_service import (
    StudyWorkspaceService,
)
from application.student_experience.workspace.workspace_inputs import WorkspaceInputs

_MISSION_COMPLETE_CASCADE: tuple[CascadeStep, ...] = (
    CascadeStep.WORKSPACE,
    CascadeStep.REFLECTION,
    CascadeStep.EVIDENCE,
    CascadeStep.JOURNEY_REFRESH,
    CascadeStep.READINESS_REFRESH,
    CascadeStep.COACH_CELEBRATION,
    CascadeStep.HOME_REFRESH,
)


def compose_experience(
    inputs: IntegrationInputs,
    *,
    bundle_id: ExperienceBundleId,
    trigger: IntegrationTrigger,
    home_service: StudentHomeService,
    journey_service: LearningJourneyService,
    readiness_service: ExamReadinessService,
    workspace_service: StudyWorkspaceService,
    coach_service: LearningCoachService,
    publish: bool = False,
) -> ExperienceJourneyViewModel:
    """Compose the continuous learning journey across XP modules.

    Snapshot chaining order (dependency):
        Home → Journey → Readiness → Workspace → Coach

    Mission-complete cascade steps are recorded for presentation when the
    trigger is completion / reflection — without inventing educational state.
    """
    home_inputs = inputs.home
    if publish:
        home = home_service.refresh_home(home_inputs)
    else:
        home = home_service.build_home(home_inputs)
    home_snapshot = home_service.build_snapshot(home)
    primary_focus = home_service.determine_primary_focus(home_inputs)
    next_action = next_action_from_focus(primary_focus)

    journey_inputs = replace(inputs.journey, home_snapshot=home_snapshot)
    if publish:
        journey = journey_service.refresh_journey(journey_inputs)
    else:
        journey = journey_service.build_journey(journey_inputs)
    journey_snapshot = journey_service.build_snapshot(
        journey,
        home_focus_headline=home_snapshot.focus_headline,
    )

    readiness_inputs = replace(
        inputs.readiness,
        home_snapshot=home_snapshot,
        journey_snapshot=journey_snapshot,
    )
    if publish:
        readiness = readiness_service.refresh_readiness(readiness_inputs)
    else:
        readiness = readiness_service.build_readiness(readiness_inputs)
    readiness_snapshot = readiness_service.build_snapshot(
        readiness,
        home_focus_headline=home_snapshot.focus_headline,
        journey_trajectory_message=journey_snapshot.trajectory_message,
    )

    workspace_inputs = replace(
        inputs.workspace,
        home_snapshot=home_snapshot,
        journey_snapshot=journey_snapshot,
        readiness_snapshot=readiness_snapshot,
    )
    if publish:
        workspace = workspace_service.refresh_workspace(workspace_inputs)
    else:
        workspace = workspace_service.build_workspace(workspace_inputs)
    workspace_snapshot = workspace_service.build_snapshot(workspace)

    coach_inputs = CoachInputs(
        student_id=inputs.student_id,
        as_of=inputs.as_of,
        home_snapshot=home_snapshot,
        journey_snapshot=journey_snapshot,
        readiness_snapshot=readiness_snapshot,
        workspace_snapshot=workspace_snapshot,
        evaluation=inputs.evaluation,
        mission_plan=inputs.mission_plan,
        schedule=inputs.schedule,
        mission_execution=inputs.mission_execution,
    )
    # Coach always receives the updated CoachContext — no manual refresh.
    coach_context = coach_service.refresh_coach(coach_inputs)
    conversation = coach_service.build_conversation(
        coach_inputs, context=coach_context
    )
    reflection = coach_service.build_reflection(coach_inputs)
    coach_snapshot = coach_service.build_snapshot(
        coach_context,
        suggested_question_count=len(conversation.suggested_questions.questions),
        reflection_prompt_count=len(reflection.prompts),
    )
    celebrations = coach_context.celebration_moments

    readiness_change = compose_readiness_change(
        prior=inputs.prior_readiness_snapshot,
        current=readiness_snapshot,
    )
    cascade_steps = (
        _MISSION_COMPLETE_CASCADE
        if trigger
        in (
            IntegrationTrigger.MISSION_COMPLETE,
            IntegrationTrigger.REFLECTION_SUBMITTED,
        )
        else ()
    )
    surface_states = compose_surface_states(
        home=home,
        next_action=next_action,
        readiness_change=readiness_change,
        celebrations=celebrations,
        evidence_recorded=inputs.evidence_recorded,
        cascade=bool(cascade_steps),
    )

    return ExperienceJourneyViewModel(
        bundle_id=bundle_id,
        student_id=inputs.student_id,
        composed_at=inputs.as_of,
        trigger=trigger,
        home=home,
        journey=journey,
        readiness=readiness,
        workspace=workspace,
        coach_context=coach_context,
        conversation=conversation,
        reflection=reflection,
        celebrations=celebrations,
        home_snapshot=home_snapshot,
        journey_snapshot=journey_snapshot,
        readiness_snapshot=readiness_snapshot,
        workspace_snapshot=workspace_snapshot,
        coach_snapshot=coach_snapshot,
        next_action=next_action,
        primary_focus=primary_focus,
        readiness_change=readiness_change,
        surface_states=surface_states,
        cascade_steps=cascade_steps,
        evidence_recorded=inputs.evidence_recorded,
    )


def compose_readiness_change(
    *,
    prior: ReadinessSnapshot | None,
    current: ReadinessSnapshot,
) -> ReadinessChangeNotice:
    """Surface readiness changes naturally beside the continuous journey."""
    current_label = (current.readiness_label or "").strip() or None
    if prior is None:
        if current_label:
            return ReadinessChangeNotice(
                changed=False,
                previous_label=None,
                current_label=current_label,
                message=f"Exam readiness is currently {current_label}.",
            )
        return ReadinessChangeNotice(
            changed=False,
            previous_label=None,
            current_label=None,
            message=(
                "Exam readiness will appear here once study evidence "
                "is available."
            ),
        )

    previous_label = (prior.readiness_label or "").strip() or None
    if previous_label == current_label:
        label = current_label or "unchanged"
        return ReadinessChangeNotice(
            changed=False,
            previous_label=previous_label,
            current_label=current_label,
            message=f"Exam readiness remains {label}.",
        )
    previous = previous_label or "not yet assessed"
    current_text = current_label or "updated"
    return ReadinessChangeNotice(
        changed=True,
        previous_label=previous_label,
        current_label=current_label,
        message=f"Exam readiness moved from {previous} to {current_text}.",
    )


def compose_surface_states(
    *,
    home: HomeViewModel,
    next_action: IntegratedNextAction,
    readiness_change: ReadinessChangeNotice,
    celebrations: CelebrationMoments,
    evidence_recorded: bool,
    cascade: bool,
) -> tuple[SurfaceState, ...]:
    """Build empty / success states that explain why and show progress."""
    states: list[SurfaceState] = []

    home_empty = not home.todays_focus.has_focus
    states.append(
        SurfaceState(
            surface=JourneySurface.HOME,
            is_empty=home_empty,
            empty_reason=(
                home.todays_focus.reason
                if home_empty
                else None
            ),
            success_message=(
                None
                if home_empty
                else f"Primary next step: {next_action.label}."
            ),
            progress_visible=not home_empty,
        )
    )

    workspace_empty = next_action.destination not in (
        JourneySurface.WORKSPACE,
        JourneySurface.REFLECTION,
    ) and next_action.action_kind in (
        FocusActionKind.NONE,
        FocusActionKind.VIEW_SCHEDULE,
    )
    states.append(
        SurfaceState(
            surface=JourneySurface.WORKSPACE,
            is_empty=workspace_empty,
            empty_reason=(
                "No active mission or session is ready in the workspace yet."
                if workspace_empty
                else None
            ),
            success_message=(
                "Workspace is ready to continue your current learning state."
                if not workspace_empty
                else None
            ),
            progress_visible=not workspace_empty,
        )
    )

    reflection_needed = (
        next_action.action_kind is FocusActionKind.REVIEW_REFLECTION or cascade
    )
    states.append(
        SurfaceState(
            surface=JourneySurface.REFLECTION,
            is_empty=not reflection_needed and not evidence_recorded,
            empty_reason=(
                "Reflection opens after you complete a mission."
                if not reflection_needed and not evidence_recorded
                else None
            ),
            success_message=(
                "Reflection captured — your learning journey is updating."
                if evidence_recorded
                else (
                    "Capture a short reflection to keep learning continuous."
                    if reflection_needed
                    else None
                )
            ),
            progress_visible=evidence_recorded or reflection_needed,
        )
    )

    states.append(
        SurfaceState(
            surface=JourneySurface.JOURNEY,
            is_empty=False,
            empty_reason=None,
            success_message=(
                "Learning journey refreshed with your latest progress."
                if cascade
                else home.progress.mastery_message
            ),
            progress_visible=True,
        )
    )

    states.append(
        SurfaceState(
            surface=JourneySurface.READINESS,
            is_empty=readiness_change.current_label is None,
            empty_reason=(
                readiness_change.message
                if readiness_change.current_label is None
                else None
            ),
            success_message=(
                readiness_change.message
                if readiness_change.current_label is not None
                else None
            ),
            progress_visible=readiness_change.changed or cascade,
        )
    )

    coach_empty = not celebrations.available and not cascade
    states.append(
        SurfaceState(
            surface=JourneySurface.COACH,
            is_empty=coach_empty,
            empty_reason=(
                "Coach conversation context will appear as study progress arrives."
                if coach_empty
                else None
            ),
            success_message=(
                celebrations.summary
                if celebrations.available
                else (
                    "Coach received your updated learning context."
                    if cascade
                    else None
                )
            ),
            progress_visible=celebrations.available or cascade,
        )
    )
    return tuple(states)


def aligned_module_inputs(home: HomeInputs) -> tuple[
    JourneyInputs, ReadinessInputs, WorkspaceInputs
]:
    """Derive sibling module inputs from a HomeInputs root.

    Histories start empty unless the caller enriches them — graceful
    degradation is intentional.
    """
    journey = JourneyInputs(
        student_id=home.student_id,
        as_of=home.as_of,
        evaluation_history=(home.evaluation,) if home.evaluation is not None else (),
        execution_history=(
            (home.current_execution,) if home.current_execution is not None else ()
        ),
        schedule_history=(home.schedule,) if home.schedule is not None else (),
        assessment_history=(home.assessment,) if home.assessment is not None else (),
        recommendation_history=(
            (home.recommendation_set,) if home.recommendation_set is not None else ()
        ),
    )
    readiness = ReadinessInputs(
        student_id=home.student_id,
        as_of=home.as_of,
        evaluation=home.evaluation,
        assessment=home.assessment,
        recommendation_set=home.recommendation_set,
        schedule=home.schedule,
        execution_history=(
            (home.current_execution,) if home.current_execution is not None else ()
        ),
        exam_target=home.exam_target,
    )
    workspace = WorkspaceInputs(
        student_id=home.student_id,
        as_of=home.as_of,
        schedule=home.schedule,
        mission_execution=home.current_execution,
        mission_plan=home.mission_plan,
    )
    return journey, readiness, workspace
