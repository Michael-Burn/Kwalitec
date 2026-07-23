"""Navigation and surface-state tests for Experience Integration (PX-002)."""

from __future__ import annotations

from application.education.mission_execution import ExecutionStatus
from application.education.mission_generation import MissionType
from application.student_experience.home import FocusActionKind
from application.student_experience.integration import (
    JourneySurface,
    action_key_for_focus,
    destination_for_action,
)
from tests.application.student_experience.home.conftest import (
    make_execution,
    make_mission,
    make_plan,
    make_schedule,
    make_session,
)
from tests.application.student_experience.integration.conftest import (
    make_integration_inputs,
    make_service,
)


def test_action_destinations_follow_continuous_journey() -> None:
    assert destination_for_action(FocusActionKind.CONTINUE_MISSION) is (
        JourneySurface.WORKSPACE
    )
    assert destination_for_action(FocusActionKind.RESUME_SESSION) is (
        JourneySurface.WORKSPACE
    )
    assert destination_for_action(FocusActionKind.REVIEW_REFLECTION) is (
        JourneySurface.REFLECTION
    )
    assert destination_for_action(FocusActionKind.PREPARE_CHECKPOINT) is (
        JourneySurface.WORKSPACE
    )
    assert action_key_for_focus(FocusActionKind.REVIEW_REFLECTION) == (
        "open_reflection"
    )
    assert action_key_for_focus(FocusActionKind.PREPARE_CHECKPOINT) == (
        "prepare_checkpoint"
    )


def test_empty_states_explain_why() -> None:
    service = make_service()
    from application.student_experience.home import HomeInputs
    from application.student_experience.integration import IntegrationInputs
    from application.student_experience.integration.integration_composer import (
        aligned_module_inputs,
    )
    from tests.application.student_experience.home.conftest import AS_OF, STUDENT_ID

    home = HomeInputs(student_id=STUDENT_ID, as_of=AS_OF)
    journey, readiness, workspace = aligned_module_inputs(home)
    view = service.build_experience(
        IntegrationInputs(
            home=home,
            journey=journey,
            readiness=readiness,
            workspace=workspace,
        )
    )
    home_state = next(
        s for s in view.surface_states if s.surface is JourneySurface.HOME
    )
    assert home_state.is_empty is True
    assert home_state.empty_reason
    assert "queued" in home_state.empty_reason.lower() or "update" in (
        home_state.empty_reason.lower()
    )


def test_success_states_show_visible_progress() -> None:
    service = make_service()
    view = service.refresh_after_reflection(make_integration_inputs())
    reflection = next(
        s for s in view.surface_states if s.surface is JourneySurface.REFLECTION
    )
    assert reflection.progress_visible is True
    assert reflection.success_message
    assert view.evidence_recorded is True
    home_state = next(
        s for s in view.surface_states if s.surface is JourneySurface.HOME
    )
    assert home_state.success_message or not home_state.is_empty


def test_readiness_change_surfaces_naturally() -> None:
    service = make_service()
    first = service.build_experience(make_integration_inputs())
    second_inputs = make_integration_inputs()
    from application.student_experience.integration import IntegrationInputs

    second = service.build_experience(
        IntegrationInputs(
            home=second_inputs.home,
            journey=second_inputs.journey,
            readiness=second_inputs.readiness,
            workspace=second_inputs.workspace,
            prior_readiness_snapshot=first.readiness_snapshot,
        )
    )
    assert second.readiness_change.message
    assert (
        second.readiness_change.current_label
        == first.readiness_snapshot.readiness_label
    )


def test_state_aware_ctas_cover_px002_examples() -> None:
    service = make_service()
    plan = make_plan()

    continue_action = service.resolve_next_action(
        make_integration_inputs(
            mission_plan=plan,
            current_execution=make_execution(plan, status=ExecutionStatus.STARTED),
        ).home
    )
    assert continue_action.label == "Continue Mission"

    resume_action = service.resolve_next_action(
        make_integration_inputs(
            mission_plan=plan,
            current_execution=make_execution(plan, status=ExecutionStatus.PAUSED),
        ).home
    )
    assert resume_action.label == "Resume Session"

    reflection_action = service.resolve_next_action(
        make_integration_inputs(
            mission_plan=plan,
            current_execution=make_execution(plan, status=ExecutionStatus.COMPLETED),
        ).home
    )
    assert reflection_action.label == "Review Reflection"

    checkpoint_plan = make_plan(
        (
            make_mission(
                "mission-checkpoint",
                mission_type=MissionType.CHECKPOINT_PREPARATION,
            ),
        )
    )
    checkpoint_action = service.resolve_next_action(
        make_integration_inputs(
            mission_plan=checkpoint_plan,
            schedule=make_schedule(
                sessions=(make_session(mission_ids=("mission-checkpoint",)),)
            ),
        ).home
    )
    assert checkpoint_action.label == "Prepare Checkpoint"
