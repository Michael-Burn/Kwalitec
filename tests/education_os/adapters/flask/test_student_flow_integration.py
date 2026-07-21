"""Integration tests for V4-004 student-flow wiring through create_app."""

from __future__ import annotations

import pytest

from adapters.flask.dashboard.dependency_provider import (
    ADAPTER_DEPS_EXTENSION,
    FlaskDependencyProvider,
)
from application.pipeline import EducationalPipeline
from tests.education_os.application.pipeline.test_educational_pipeline import (
    make_pipeline_request,
)
from web.app import WebConfig, create_app


@pytest.fixture
def eos_app():
    app = create_app(
        WebConfig(
            database_url="sqlite+pysqlite:///:memory:",
            secret_key="eos-integration-secret",
            testing=True,
            environment="testing",
        )
    )

    def request_builder(student_id: str):
        return make_pipeline_request(student_id=student_id)

    pipeline = app.extensions["container"].educational_pipeline
    assert isinstance(pipeline, EducationalPipeline)

    updates: list = []

    def update_evidence(captured):
        updates.append(captured)
        return {"ok": True, "evidence_id": captured.evidence_id}

    deps = FlaskDependencyProvider.from_container(
        app.extensions["container"],
        request_builder=request_builder,
        update_evidence=update_evidence,
        checkpoint_store=app.extensions[ADAPTER_DEPS_EXTENSION].checkpoint_store,
    )
    FlaskDependencyProvider.bind(app, deps)
    app.extensions["eos_test_evidence_updates"] = updates
    return app


@pytest.fixture
def eos_client(eos_app):
    return eos_app.test_client()


@pytest.mark.integration
def test_create_app_registers_student_flow_routes(eos_app) -> None:
    rules = {rule.rule for rule in eos_app.url_map.iter_rules()}
    assert "/eos/login/" in rules
    assert "/eos/dashboard/" in rules
    assert "/eos/mission/" in rules
    assert "/eos/session/action" in rules
    assert "/eos/reflection/" in rules


@pytest.mark.integration
def test_integration_dashboard_uses_pipeline_cargo(eos_client) -> None:
    response = eos_client.get("/eos/dashboard/?student_id=student-ada")
    assert response.status_code == 200
    assert b"Learning Dashboard" in response.data
    assert b"ds-mission-card" in response.data


@pytest.mark.integration
def test_integration_reflection_updates_evidence(eos_app, eos_client) -> None:
    response = eos_client.post(
        "/eos/reflection/",
        data={
            "student_id": "student-ada",
            "session_id": "integration-1",
            "mission_id": "mission-1",
            "confidence": "confident",
            "difficulty": "hard",
            "weak_concept": "Credibility",
            "student_notes": "Need another pass",
            "redirect": "true",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b'data-page="dashboard"' in response.data
    updates = eos_app.extensions["eos_test_evidence_updates"]
    assert len(updates) == 1
