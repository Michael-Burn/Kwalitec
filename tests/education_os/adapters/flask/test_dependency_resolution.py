"""Dependency resolution tests for the Flask adapter layer (V4-002)."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from flask import Flask, g

from adapters.flask.dashboard.dependency_provider import (
    ADAPTER_DEPS_EXTENSION,
    ADAPTER_DEPS_G_KEY,
    AdapterDependencies,
    FlaskDependencyProvider,
    get_dependencies,
)


def test_default_dependencies_are_null_safe() -> None:
    deps = AdapterDependencies()
    assert deps.load_pipeline_result("student-1") is None
    assert deps.student_id_resolver() == ""


def test_provider_override_replaces_fields() -> None:
    provider = FlaskDependencyProvider()
    calls: list[str] = []

    def loader(student_id: str) -> str:
        calls.append(student_id)
        return f"result:{student_id}"

    deps = provider.override(
        load_pipeline_result=loader,
        student_id_resolver=lambda: "student-ada",
    )

    assert deps.load_pipeline_result("student-ada") == "result:student-ada"
    assert deps.student_id_resolver() == "student-ada"
    assert calls == ["student-ada"]


def test_bind_attaches_dependencies_to_app_extensions() -> None:
    app = Flask("deps_bind_test")
    deps = AdapterDependencies(student_id_resolver=lambda: "bound-student")
    FlaskDependencyProvider.bind(app, deps)

    assert app.extensions[ADAPTER_DEPS_EXTENSION] is deps
    with app.app_context():
        resolved = FlaskDependencyProvider().resolve()
    assert resolved.student_id_resolver() == "bound-student"


def test_bind_request_overrides_for_active_request() -> None:
    app = Flask("deps_request_test")
    FlaskDependencyProvider.bind(
        app,
        AdapterDependencies(student_id_resolver=lambda: "app-student"),
    )
    request_deps = AdapterDependencies(
        student_id_resolver=lambda: "request-student",
    )

    with app.test_request_context("/"):
        FlaskDependencyProvider.bind_request(request_deps)
        resolved = get_dependencies()
        assert resolved.student_id_resolver() == "request-student"
        assert getattr(g, ADAPTER_DEPS_G_KEY) is request_deps


def test_bind_request_requires_request_context() -> None:
    with pytest.raises(RuntimeError, match="request context"):
        FlaskDependencyProvider.bind_request(AdapterDependencies())


def test_from_container_builds_null_safe_loader() -> None:
    container = SimpleNamespace(educational_pipeline=object())
    deps = FlaskDependencyProvider.from_container(container)
    assert deps.load_pipeline_result("student-x") is None


def test_from_container_runs_pipeline_with_request_builder() -> None:
    calls: list[str] = []

    class Pipeline:
        def run(self, request):
            calls.append(request)
            return f"result:{request}"

    deps = FlaskDependencyProvider.from_container(
        SimpleNamespace(educational_pipeline=Pipeline()),
        request_builder=lambda student_id: f"req:{student_id}",
        student_id_resolver=lambda: "student-ada",
    )
    assert deps.load_pipeline_result("student-ada") == "result:req:student-ada"
    assert calls == ["req:student-ada"]
