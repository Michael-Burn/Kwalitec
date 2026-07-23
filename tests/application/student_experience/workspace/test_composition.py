"""Workspace composition tests (XP-004)."""

from __future__ import annotations

from datetime import UTC, datetime

from application.education.mission_generation import MissionType
from application.student_experience.workspace import (
    FocusPromptKind,
    SessionPresence,
    StudyWorkspaceService,
    WorkspaceId,
)
from tests.application.student_experience.workspace.conftest import (
    STUDENT_ID,
    FakeWorkspaceResourceProvider,
    RecordingWorkspacePublisher,
    make_full_inputs,
    make_multi_step_mission,
    make_plan,
)


def test_build_workspace_composes_all_sections(
    service: StudyWorkspaceService,
) -> None:
    view = service.build_workspace(
        make_full_inputs(), workspace_id=WorkspaceId("workspace-001")
    )

    assert view.student_id == STUDENT_ID
    assert view.workspace_id.value == "workspace-001"
    assert view.current_session.available is True
    assert view.current_session.presence is SessionPresence.AVAILABLE
    assert view.mission.available is True
    assert view.objectives.has_objectives is True
    assert view.progress.available is True
    assert view.focus.has_prompts is True
    assert view.session_timer.available is True
    assert view.reflection.available is True
    assert view.completion.available is True


def test_workspace_never_exposes_domain_type_names(
    service: StudyWorkspaceService,
) -> None:
    view = service.build_workspace(make_full_inputs())
    blob = " ".join(
        [
            view.current_session.summary,
            view.current_session.estimated_completion_label,
            view.mission.title,
            view.mission.purpose,
            view.mission.dependencies_summary,
            view.objectives.summary,
            *(item.label for item in view.objectives.items),
            view.resources.summary,
            view.progress.summary,
            *(item.message for item in view.progress.quality_indicators),
            view.focus.summary,
            *(item.prompt for item in view.focus.prompts),
            view.session_timer.summary,
            view.reflection.summary,
            view.reflection.reflection_prompt,
            view.completion.summary,
            view.completion.next_session_preview,
            view.completion.upcoming_milestone,
            view.completion.readiness_impact_summary,
        ]
    )
    for forbidden in (
        "MasteryAssessment",
        "RecommendationSet",
        "MissionPlan",
        "EducationalEvaluation",
        "StudySchedule",
        "MissionExecution",
        "HomeSnapshot",
        "JourneySnapshot",
        "ReadinessSnapshot",
        "Education OS",
    ):
        assert forbidden not in blob


def test_mission_card_includes_satisfied_dependencies(
    service: StudyWorkspaceService,
) -> None:
    view = service.build_workspace(make_full_inputs())
    assert view.mission.dependencies_satisfied is True
    assert view.mission.dependency_labels
    assert any(
        "prerequisite" in label.lower() for label in view.mission.dependency_labels
    )


def test_focus_prompts_are_deterministic_kinds(
    service: StudyWorkspaceService,
) -> None:
    view = service.build_workspace(make_full_inputs())
    kinds = {prompt.kind for prompt in view.focus.prompts}
    assert FocusPromptKind.CONTINUE_CURRENT_OBJECTIVE in kinds
    assert FocusPromptKind.FINISH_CURRENT_STEP in kinds
    assert FocusPromptKind.NONE not in kinds


def test_checkpoint_mission_adds_prepare_prompt(
    service: StudyWorkspaceService,
) -> None:
    mission = make_multi_step_mission(
        "mission-cp",
        mission_type=MissionType.CHECKPOINT_PREPARATION,
    )
    plan = make_plan((mission,), plan_id="plan-cp")
    from application.education.mission_execution import (
        ExecutionId,
        ExecutionStatus,
        MissionExecution,
    )
    from application.education.mission_generation import MissionId

    execution = MissionExecution.plan_execution(
        execution_id=ExecutionId("exec-cp"),
        mission_plan=plan,
        mission_id=MissionId("mission-cp"),
    ).with_updates(
        status=ExecutionStatus.STARTED,
        started_at=view_as_of(),
        last_active_at=view_as_of(),
        elapsed_study_time_seconds=120.0,
    )
    view = service.build_workspace(
        make_full_inputs(mission_plan=plan, mission_execution=execution)
    )
    kinds = {prompt.kind for prompt in view.focus.prompts}
    assert FocusPromptKind.PREPARE_CHECKPOINT in kinds


def view_as_of():
    from tests.application.student_experience.workspace.conftest import AS_OF

    return AS_OF


def test_refresh_workspace_publishes() -> None:
    publisher = RecordingWorkspacePublisher()
    resources = FakeWorkspaceResourceProvider()
    service = StudyWorkspaceService(
        workspace_publisher=publisher,
        workspace_resource_provider=resources,
    )
    view = service.refresh_workspace(
        make_full_inputs(), workspace_id="workspace-refresh"
    )
    assert len(publisher.workspaces) == 1
    assert len(publisher.snapshots) == 1
    assert publisher.workspaces[0].workspace_id.value == "workspace-refresh"
    assert publisher.snapshots[0].student_id == view.student_id
    assert view.resources.has_resources is True
    assert len(view.resources.items) == 2


def test_deterministic_workspace_id_from_as_of(
    service: StudyWorkspaceService,
) -> None:
    inputs = make_full_inputs(as_of=datetime(2026, 7, 23, 8, 0, tzinfo=UTC))
    view = service.build_workspace(inputs)
    assert view.workspace_id.value == "workspace:student-001:20260723T080000"
