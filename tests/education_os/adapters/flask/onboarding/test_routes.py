"""Flask onboarding adapter integration tests (BR-002)."""

from __future__ import annotations

import re

import pytest
from flask import Flask

from adapters.flask.dashboard.dependency_provider import STUDENT_SESSION_KEY
from adapters.flask.onboarding import (
    OnboardingAdapterDependencies,
    build_onboarding_service,
    register_onboarding,
)
from application.onboarding.memory import (
    FixedClock,
    InMemoryOnboardingRepository,
    RecordingTwinInitializer,
    SequentialOnboardingIdGenerator,
)
from tests.education_os.application.onboarding.conftest import full_payloads


@pytest.fixture
def twin_initializer() -> RecordingTwinInitializer:
    return RecordingTwinInitializer()


@pytest.fixture
def app(twin_initializer: RecordingTwinInitializer) -> Flask:
    flask_app = Flask(__name__)
    flask_app.secret_key = "test-onboarding-secret"
    service = build_onboarding_service(
        repository=InMemoryOnboardingRepository(),
        twin_initializer=twin_initializer,
        clock=FixedClock(),
        id_generator=SequentialOnboardingIdGenerator(),
    )
    register_onboarding(
        flask_app,
        dependencies=OnboardingAdapterDependencies(onboarding_service=service),
    )
    return flask_app


@pytest.fixture
def client(app: Flask):
    return app.test_client()


def _csrf(html: str) -> str:
    match = re.search(r'name="csrf_token" value="([^"]+)"', html)
    assert match, "csrf token missing"
    return match.group(1)


def _onboarding_id(html: str) -> str:
    match = re.search(r'name="onboarding_id" value="([^"]+)"', html)
    assert match, "onboarding id missing"
    return match.group(1)


def test_get_starts_onboarding(client) -> None:
    with client.session_transaction() as sess:
        sess[STUDENT_SESSION_KEY] = "stu-web-1"
    response = client.get("/eos/onboarding/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Student Onboarding" in body
    assert 'role="progressbar"' in body
    assert "Welcome" in body


def test_end_to_end_http_flow(client, twin_initializer) -> None:
    with client.session_transaction() as sess:
        sess[STUDENT_SESSION_KEY] = "stu-web-e2e"
    response = client.get("/eos/onboarding/")
    html = response.get_data(as_text=True)
    csrf = _csrf(html)
    oid = _onboarding_id(html)
    payloads = full_payloads()
    steps = (
        "welcome",
        "ifoa_profile",
        "exam_history",
        "weekly_availability",
        "confidence",
        "study_habits",
        "optional_diagnostic",
        "review",
    )
    for step in steps:
        data = {
            "csrf_token": csrf,
            "onboarding_id": oid,
            "step": step,
            "action": "complete" if step == "review" else "advance",
        }
        raw = payloads[step]
        for key, value in raw.items():
            if isinstance(value, bool):
                if value:
                    data[key] = "true"
            else:
                data[key] = str(value)
        response = client.post("/eos/onboarding/", data=data, follow_redirects=False)
        if step == "review":
            assert response.status_code in {302, 303}
            assert "/eos/dashboard/" in (response.headers.get("Location") or "")
            break
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        csrf = _csrf(html)
        oid = _onboarding_id(html)
    assert twin_initializer.requests
    assert twin_initializer.requests[0].exam_paper == "CS1"


def test_autosave_then_resume(client) -> None:
    with client.session_transaction() as sess:
        sess[STUDENT_SESSION_KEY] = "stu-resume"
    first = client.get("/eos/onboarding/")
    html = first.get_data(as_text=True)
    csrf = _csrf(html)
    oid = _onboarding_id(html)
    client.post(
        "/eos/onboarding/",
        data={
            "csrf_token": csrf,
            "onboarding_id": oid,
            "step": "welcome",
            "action": "advance",
            "acknowledged": "true",
        },
    )
    second = client.get("/eos/onboarding/")
    body = second.get_data(as_text=True)
    assert "IFoA Profile" in body or "ifoa" in body.lower()
    assert oid in body
