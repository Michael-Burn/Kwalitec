"""Controller unit tests for the Flask adapter layer (V4-002)."""

from __future__ import annotations

from adapters.flask.dashboard.controller import DashboardController
from adapters.flask.dashboard.dependency_provider import AdapterDependencies
from adapters.flask.reflection.controller import ReflectionController
from adapters.flask.session.controller import SessionController
from application.evidence_capture import CapturedEvidence
from application.pipeline import PipelineResult
from application.session_runtime import SessionRuntime, SessionStage
from presentation.dashboard import DashboardViewModel
from presentation.reflection import ReflectionViewModel
from presentation.study_session import StudySessionViewModel


def test_dashboard_controller_presents_pipeline_result(
    adapter_deps: AdapterDependencies,
    pipeline_result: PipelineResult,
) -> None:
    controller = DashboardController(adapter_deps)
    view = controller.show("student-ada")

    assert isinstance(view, DashboardViewModel)
    assert view.header.title == "Learning Dashboard"
    assert view.mission_card.body == pipeline_result.mission.objective.statement


def test_dashboard_controller_uses_student_id_resolver(
    pipeline_result: PipelineResult,
) -> None:
    seen: list[str] = []

    def loader(student_id: str) -> PipelineResult:
        seen.append(student_id)
        return pipeline_result

    deps = AdapterDependencies(
        load_pipeline_result=loader,
        student_id_resolver=lambda: "resolved-student",
    )
    view = DashboardController(deps).show()

    assert seen == ["resolved-student"]
    assert isinstance(view, DashboardViewModel)


def test_dashboard_controller_null_safe(null_deps: AdapterDependencies) -> None:
    view = DashboardController(null_deps).show("anyone")
    assert isinstance(view, DashboardViewModel)
    assert view.header.title == "Learning Dashboard"


def test_session_controller_presents_and_opens_runtime(
    adapter_deps: AdapterDependencies,
) -> None:
    controller = SessionController(adapter_deps)
    view = controller.show("student-ada", session_id="session-1")

    assert isinstance(view, StudySessionViewModel)
    assert view.header.title

    runtime = controller.open_runtime(view, session_id="session-1")
    assert isinstance(runtime, SessionRuntime)
    assert runtime.state.session_id == "session-1"
    assert runtime.state.stage is SessionStage.NOT_STARTED
    assert controller.current_state(runtime) is runtime.state


def test_reflection_controller_show_and_capture(
    adapter_deps: AdapterDependencies,
) -> None:
    session = SessionController(adapter_deps).show("student-ada")
    controller = ReflectionController(adapter_deps)

    view = controller.show(
        session,
        confidence="confident",
        difficulty="about_right",
        weak_concept="Bayes theorem",
        student_notes="Need more practice",
    )
    assert isinstance(view, ReflectionViewModel)
    assert view.header.title == "Reflection"

    captured = controller.capture(
        session,
        reflection=view,
        student_id="student-ada",
        mission_id="mission-1",
        evidence_id="evidence-1",
    )
    assert isinstance(captured, CapturedEvidence)
    assert captured.evidence_id == "evidence-1"
    assert captured.outcome.student_id == "student-ada"


def test_session_controller_apply_action_advances(
    adapter_deps: AdapterDependencies,
) -> None:
    controller = SessionController(adapter_deps)
    result = controller.apply_action(
        "start",
        "student-ada",
        session_id="session-runtime-1",
    )
    assert result.state.stage is SessionStage.PREPARING
    assert result.error == ""

    advanced = controller.apply_action(
        "advance",
        "student-ada",
        session_id="session-runtime-1",
    )
    assert advanced.state.stage is SessionStage.LEARNING


def test_reflection_controller_submit_updates_evidence(
    adapter_deps: AdapterDependencies,
    evidence_updates: list,
) -> None:
    session = SessionController(adapter_deps).show("student-ada")
    result = ReflectionController(adapter_deps).submit(
        session,
        student_id="student-ada",
        mission_id="mission-1",
        confidence="confident",
    )
    assert isinstance(result.view_model, ReflectionViewModel)
    assert len(evidence_updates) == 1
    assert result.update_result is not None
