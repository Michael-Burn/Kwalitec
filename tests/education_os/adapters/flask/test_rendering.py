"""Rendering and template-mapping tests for the Flask adapter layer (V4-002)."""

from __future__ import annotations

from adapters.flask.dashboard.controller import DashboardController
from adapters.flask.dashboard.dependency_provider import AdapterDependencies
from adapters.flask.reflection.controller import ReflectionController
from adapters.flask.session.controller import SessionController
from adapters.flask.template_mapper import (
    DASHBOARD_TEMPLATE,
    REFLECTION_TEMPLATE,
    SESSION_TEMPLATE,
    TemplateMapper,
)
from application.pipeline import PipelineResult
from presentation.dashboard import DashboardViewModel
from presentation.design_system import ContainerWidth


def test_template_mapper_serializes_dashboard(
    adapter_deps: AdapterDependencies,
    pipeline_result: PipelineResult,
) -> None:
    view = DashboardController(adapter_deps).show("student-ada")
    context = TemplateMapper.for_dashboard(view)

    assert context["page"] == "dashboard"
    assert context["template_name"] == DASHBOARD_TEMPLATE
    assert context["title"] == "Learning Dashboard"
    assert context["container_width"] == ContainerWidth.WIDE.value
    assert isinstance(context["view"], dict)
    assert context["view"]["header"]["title"] == "Learning Dashboard"
    assert context["view"]["mission_card"]["body"] == (
        pipeline_result.mission.objective.statement
    )
    # Enums must become plain strings for Jinja.
    assert isinstance(context["view"]["container_width"], str)


def test_template_mapper_serializes_session(
    adapter_deps: AdapterDependencies,
) -> None:
    view = SessionController(adapter_deps).show("student-ada")
    context = TemplateMapper.for_session(view)

    assert context["page"] == "session"
    assert context["template_name"] == SESSION_TEMPLATE
    assert context["title"]
    assert isinstance(context["view"], dict)
    assert context["view"]["header"]["title"]
    assert isinstance(context["view"]["sections"], list)


def test_template_mapper_serializes_reflection(
    adapter_deps: AdapterDependencies,
) -> None:
    session = SessionController(adapter_deps).show("student-ada")
    view = ReflectionController(adapter_deps).show(session, confidence="confident")
    context = TemplateMapper.for_reflection(view)

    assert context["page"] == "reflection"
    assert context["template_name"] == REFLECTION_TEMPLATE
    assert context["title"] == "Reflection"
    assert context["is_ready"] is False
    assert isinstance(context["view"], dict)
    assert "confidence" in context["view"]


def test_serialize_handles_nested_tuples_and_enums() -> None:
    view = DashboardController(AdapterDependencies()).show(None)
    assert isinstance(view, DashboardViewModel)
    payload = TemplateMapper.serialize(view)
    assert isinstance(payload["learning_statistics"], list)
    assert payload["learning_statistics"] == []
    assert isinstance(payload["hero"], dict)
    assert isinstance(payload["readiness"], dict)
    assert isinstance(payload["journey"], dict)
    assert isinstance(payload["coach"], dict)
    assert isinstance(payload["upcoming_milestones"], list)
    assert isinstance(payload["quick_actions"], list)
    assert isinstance(payload["achievements"], list)
    assert isinstance(payload["container_width"], str)


def test_flask_rendering_uses_mapped_context(client) -> None:
    response = client.get("/eos/dashboard/?student_id=student-ada")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "<title>Learning Dashboard</title>" in html
    assert 'data-page="dashboard"' in html
    assert 'data-width="wide"' in html
    assert "Learning Dashboard" in html or "Today's Mission" in html
    assert 'data-dashboard-slot="primary"' in html
    assert 'data-dashboard-slot="secondary"' in html
    assert 'data-dashboard-slot="tertiary"' in html
    assert "eos-hero" in html
    assert 'data-student-cta="primary"' in html
    assert "Learning statistics" not in html
    assert "aria-label=\"Achievements\"" not in html


def test_session_rendering_includes_objective(client) -> None:
    response = client.get("/eos/session/?student_id=student-ada")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'data-page="session"' in html
    assert "<h1" in html
    assert "ds-mission-card" in html


def test_reflection_rendering_includes_form(client) -> None:
    response = client.get("/eos/reflection/?student_id=student-ada")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'data-page="reflection"' in html
    assert '<form' in html
    assert "Save" in html


def test_null_safe_rendering_without_pipeline(client, app) -> None:
    from adapters.flask.dashboard.dependency_provider import (
        AdapterDependencies,
        FlaskDependencyProvider,
    )

    FlaskDependencyProvider.bind(app, AdapterDependencies())
    response = client.get("/eos/dashboard/")
    assert response.status_code == 200
    assert b"Learning Dashboard" in response.data
