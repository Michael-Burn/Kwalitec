"""End-to-end continuous journey composition tests (PX-002)."""

from __future__ import annotations

from application.education.mission_execution import ExecutionStatus
from application.student_experience.home import FocusActionKind
from application.student_experience.integration import (
    CascadeStep,
    IntegrationTrigger,
    JourneySurface,
)
from tests.application.student_experience.home.conftest import (
    make_execution,
    make_plan,
)
from tests.application.student_experience.integration.conftest import (
    RecordingCoachContextPublisher,
    RecordingHomePublisher,
    RecordingIntegrationPublisher,
    RecordingJourneyPublisher,
    RecordingReadinessPublisher,
    RecordingWorkspacePublisher,
    make_integration_inputs,
    make_service,
)


def test_continuous_journey_composes_all_modules() -> None:
    service = make_service()
    journey = service.build_experience(make_integration_inputs())
    assert journey.home is not None
    assert journey.journey is not None
    assert journey.readiness is not None
    assert journey.workspace is not None
    assert journey.coach_context is not None
    assert journey.conversation is not None
    assert journey.reflection is not None
    assert journey.home_snapshot.student_id == journey.student_id
    assert journey.coach_snapshot.student_id == journey.student_id
    assert len(journey.surface_states) == 6


def test_mission_complete_cascade_order_and_publish() -> None:
    publisher = RecordingIntegrationPublisher()
    coach_pub = RecordingCoachContextPublisher()
    home_pub = RecordingHomePublisher()
    journey_pub = RecordingJourneyPublisher()
    readiness_pub = RecordingReadinessPublisher()
    workspace_pub = RecordingWorkspacePublisher()
    service = make_service(
        publisher=publisher,
        coach_context_publisher=coach_pub,
        home_publisher=home_pub,
        journey_publisher=journey_pub,
        readiness_publisher=readiness_pub,
        workspace_publisher=workspace_pub,
    )
    journey = service.refresh_after_mission_complete(make_integration_inputs())

    assert journey.trigger is IntegrationTrigger.MISSION_COMPLETE
    assert journey.cascade_steps == (
        CascadeStep.WORKSPACE,
        CascadeStep.REFLECTION,
        CascadeStep.EVIDENCE,
        CascadeStep.JOURNEY_REFRESH,
        CascadeStep.READINESS_REFRESH,
        CascadeStep.COACH_CELEBRATION,
        CascadeStep.HOME_REFRESH,
    )
    assert journey.evidence_recorded is True
    assert publisher.journeys and publisher.bundles
    assert coach_pub.contexts, "Coach must auto-receive updated CoachContext"
    assert home_pub.homes and journey_pub.journeys
    assert readiness_pub.readiness and workspace_pub.workspaces


def test_cross_module_context_preserved_in_snapshots() -> None:
    service = make_service()
    journey = service.build_experience(make_integration_inputs())
    assert journey.journey_snapshot.home_focus_headline == (
        journey.home_snapshot.focus_headline
    )
    assert journey.readiness_snapshot.home_focus_headline == (
        journey.home_snapshot.focus_headline
    )
    assert journey.coach_context.current_focus.headline
    bundle = journey.to_snapshot_bundle()
    assert bundle.home_snapshot.snapshot_id == journey.home_snapshot.snapshot_id
    assert bundle.next_action.label == journey.next_action.label


def test_primary_cta_continues_learning_state() -> None:
    service = make_service()
    plan = make_plan()
    execution = make_execution(plan, status=ExecutionStatus.STARTED)
    action = service.resolve_next_action(
        make_integration_inputs(
            mission_plan=plan, current_execution=execution
        ).home
    )
    assert action.action_kind is FocusActionKind.CONTINUE_MISSION
    assert action.label == "Continue Mission"
    assert action.destination is JourneySurface.WORKSPACE
    assert action.has_action is True
    assert service.action_key(
        make_integration_inputs(
            mission_plan=plan, current_execution=execution
        ).home
    ) == "continue_mission"


def test_refresh_flow_is_deterministic() -> None:
    service = make_service()
    inputs = make_integration_inputs()
    first = service.build_experience(inputs, bundle_id="bundle-a")
    second = service.build_experience(inputs, bundle_id="bundle-a")
    assert first.home_snapshot.focus_headline == second.home_snapshot.focus_headline
    assert first.next_action.label == second.next_action.label
    assert first.coach_snapshot.focus_headline == second.coach_snapshot.focus_headline
    assert first.readiness_change.message == second.readiness_change.message
