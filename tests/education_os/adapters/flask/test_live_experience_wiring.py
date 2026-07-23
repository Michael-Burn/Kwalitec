"""R1-001 Live Experience Wiring — adapter integration tests."""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from flask import Flask
from jinja2 import FileSystemLoader

from adapters.flask import register_adapter_blueprints
from adapters.flask.dashboard.controller import DashboardController
from adapters.flask.dashboard.dependency_provider import (
    AdapterDependencies,
    FlaskDependencyProvider,
)
from adapters.flask.experience import (
    ExperienceGateway,
    ExperienceSurfaceController,
    MappingPriorReadinessStore,
    build_home_inputs,
    build_integration_inputs,
)
from adapters.flask.mission.controller import MissionController
from adapters.flask.reflection.controller import ReflectionController
from adapters.flask.rendering import TEMPLATES_DIR
from adapters.flask.session.controller import SessionController
from application.student_experience.integration import ExperienceIntegrationService
from application.student_experience.integration.enums import JourneySurface
from presentation.dashboard import DashboardViewModel
from presentation.mission_workspace import MissionWorkspaceViewModel

FIXED_AS_OF = datetime(2026, 7, 23, 12, 0, tzinfo=UTC)


@pytest.fixture
def experience_gateway() -> ExperienceGateway:
    return ExperienceGateway(
        experience_service=ExperienceIntegrationService(),
        as_of_resolver=lambda: FIXED_AS_OF,
        prior_readiness_store=MappingPriorReadinessStore(),
    )


@pytest.fixture
def wired_deps(
    pipeline_loader, evidence_updates, experience_gateway
) -> AdapterDependencies:
    def update_evidence(captured):
        evidence_updates.append(captured)
        return {"evidence_id": captured.evidence_id, "outcome": "recorded"}

    return AdapterDependencies(
        load_pipeline_result=pipeline_loader,
        student_id_resolver=lambda: "student-ada",
        update_evidence=update_evidence,
        experience_gateway=experience_gateway,
    )


@pytest.fixture
def wired_app(wired_deps: AdapterDependencies) -> Flask:
    flask_app = Flask("eos_experience_wiring_test")
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "eos-experience-test-secret"
    flask_app.jinja_loader = FileSystemLoader(str(TEMPLATES_DIR))
    FlaskDependencyProvider.bind(flask_app, wired_deps)
    register_adapter_blueprints(flask_app)
    return flask_app


@pytest.fixture
def wired_client(wired_app: Flask):
    return wired_app.test_client()


def test_dashboard_wiring_uses_live_experience(wired_deps: AdapterDependencies) -> None:
    controller = DashboardController(wired_deps)
    view = controller.show("student-ada")
    experience = controller.current_experience("student-ada")

    assert isinstance(view, DashboardViewModel)
    assert experience is not None
    assert experience.student_id == "student-ada"
    assert experience.home_snapshot is not None
    assert experience.journey_snapshot is not None
    assert experience.readiness_snapshot is not None
    assert experience.coach_snapshot is not None
    assert wired_deps.experience_gateway.compose_count == 1


def test_home_journey_readiness_coach_wiring(wired_client) -> None:
    for path in (
        "/eos/home/?student_id=student-ada",
        "/eos/journey/?student_id=student-ada",
        "/eos/readiness/?student_id=student-ada",
        "/eos/coach/?student_id=student-ada",
        "/eos/workspace/?student_id=student-ada",
    ):
        response = wired_client.get(path)
        assert response.status_code == 200, path
        html = response.get_data(as_text=True)
        assert "eos-shell" in html


def test_workspace_and_reflection_wiring(wired_deps: AdapterDependencies) -> None:
    mission = MissionController(wired_deps).show("student-ada")
    assert isinstance(mission, MissionWorkspaceViewModel)

    session = SessionController(wired_deps).show("student-ada")
    reflection = ReflectionController(wired_deps)
    view = reflection.show(session, student_id="student-ada")
    assert view.header.title == "Reflection"
    experience = reflection.current_experience("student-ada")
    assert experience is not None
    # Dashboard + mission + reflection share one compose when gateway is reused.
    assert wired_deps.experience_gateway.compose_count >= 1


def test_snapshot_reuse_within_request(
    wired_app: Flask, wired_deps: AdapterDependencies
) -> None:
    with wired_app.test_request_context("/eos/dashboard/?student_id=student-ada"):
        FlaskDependencyProvider.bind_request(wired_deps)
        first = wired_deps.experience_gateway.get("student-ada")
        second = wired_deps.experience_gateway.get("student-ada")
        dashboard = DashboardController(wired_deps).show("student-ada")
        surface = ExperienceSurfaceController(wired_deps).show_surface(
            JourneySurface.JOURNEY, "student-ada"
        )

        assert first is second
        assert isinstance(dashboard, DashboardViewModel)
        assert surface[1] is first
        assert wired_deps.experience_gateway.compose_count == 1


def test_reflection_submit_refreshes_experience(
    wired_deps: AdapterDependencies,
) -> None:
    session = SessionController(wired_deps).show("student-ada")
    result = ReflectionController(wired_deps).submit(
        session,
        student_id="student-ada",
        confidence="confident",
        difficulty="about_right",
    )
    assert result.experience is not None
    assert result.experience.evidence_recorded is True
    # Fresh cascade replaces the request snapshot.
    assert wired_deps.experience_gateway.get("student-ada") is result.experience


def test_null_safety_without_pipeline(null_deps: AdapterDependencies) -> None:
    view = DashboardController(null_deps).show("anyone")
    assert isinstance(view, DashboardViewModel)

    surface, experience = ExperienceSurfaceController(null_deps).show_surface(
        JourneySurface.COACH, "anyone"
    )
    assert surface.title == "Learning coach"
    # Null deps still compose a degraded experience from student_id + as_of.
    assert experience is not None or surface.empty is True


def test_dependency_injection_uses_injected_gateway() -> None:
    calls: list[str] = []

    class CountingService(ExperienceIntegrationService):
        def build_experience(self, inputs, **kwargs):  # type: ignore[no-untyped-def]
            calls.append(inputs.student_id)
            return super().build_experience(inputs, **kwargs)

    gateway = ExperienceGateway(
        experience_service=CountingService(),
        as_of_resolver=lambda: FIXED_AS_OF,
    )
    deps = AdapterDependencies(
        student_id_resolver=lambda: "injected-student",
        experience_gateway=gateway,
    )
    DashboardController(deps).show()
    assert calls == ["injected-student"]
    assert gateway.compose_count == 1


def test_inputs_builder_null_safe() -> None:
    home = build_home_inputs("ada", FIXED_AS_OF, cargo=SimpleNamespace(not_valid=True))
    assert home.student_id == "ada"
    inputs = build_integration_inputs("ada", FIXED_AS_OF)
    assert inputs.student_id == "ada"
    assert inputs.journey.student_id == "ada"


def test_architecture_purity_no_education_os_mutation() -> None:
    """Adapter experience package must not import Education OS engines."""
    import ast
    from pathlib import Path

    root = (
        Path(__file__).resolve().parents[4]
        / "src"
        / "adapters"
        / "flask"
        / "experience"
    )
    forbidden = (
        "application.education.orchestration.educational_orchestrator",
        "application.education.mission_generation.adaptive_mission_generator",
        "application.education.mission_execution.mission_execution_engine",
        "domain.recommendation",
        "domain.education.recommendation_engine",
    )
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                module = node.module
                assert module not in forbidden, path
                assert not module.startswith("domain.recommendation"), path
