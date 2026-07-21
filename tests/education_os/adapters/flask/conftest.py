"""Shared fixtures for Flask adapter layer tests (V4-002 / V4-004)."""

from __future__ import annotations

import pytest
from flask import Flask
from jinja2 import FileSystemLoader

from adapters.flask import register_adapter_blueprints
from adapters.flask.checkpoint_store import InMemoryCheckpointStore
from adapters.flask.dashboard.dependency_provider import (
    AdapterDependencies,
    FlaskDependencyProvider,
)
from adapters.flask.rendering import TEMPLATES_DIR
from application.pipeline import EducationalPipeline, PipelineResult
from tests.education_os.application.pipeline.test_educational_pipeline import (
    make_pipeline_request,
)


@pytest.fixture(scope="module")
def pipeline_result() -> PipelineResult:
    return EducationalPipeline().run(make_pipeline_request())


@pytest.fixture
def pipeline_loader(pipeline_result: PipelineResult):
    def _load(_student_id: str) -> PipelineResult:
        return pipeline_result

    return _load


@pytest.fixture
def evidence_updates() -> list:
    return []


@pytest.fixture
def adapter_deps(pipeline_loader, evidence_updates) -> AdapterDependencies:
    store = InMemoryCheckpointStore()

    def update_evidence(captured):
        evidence_updates.append(captured)
        return {"evidence_id": captured.evidence_id, "outcome": "recorded"}

    return AdapterDependencies(
        load_pipeline_result=pipeline_loader,
        student_id_resolver=lambda: "student-ada",
        update_evidence=update_evidence,
        checkpoint_store=store,
    )


@pytest.fixture
def app(adapter_deps: AdapterDependencies) -> Flask:
    flask_app = Flask("eos_adapter_test")
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "eos-adapter-test-secret"
    flask_app.jinja_loader = FileSystemLoader(str(TEMPLATES_DIR))
    FlaskDependencyProvider.bind(flask_app, adapter_deps)
    register_adapter_blueprints(flask_app)
    return flask_app


@pytest.fixture
def client(app: Flask):
    return app.test_client()


@pytest.fixture
def null_deps() -> AdapterDependencies:
    return AdapterDependencies()
