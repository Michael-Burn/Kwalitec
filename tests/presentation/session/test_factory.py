"""Factory / forms / navigation / regression presentation tests."""

from __future__ import annotations

from app.application.session_experience.facade import SessionExperienceService
from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.session.factory import (
    build_session_experience_service,
    get_session_experience_service,
    set_session_experience_service,
)
from app.presentation.session.forms import (
    AdvanceActivityForm,
    BeginSessionForm,
    CompleteSessionForm,
    ContinueReflectionForm,
    SubmitAnswerForm,
)
from app.presentation.session.navigation import page_meta
from tests.application.session_experience.helpers import make_session_experience
from tests.presentation.session.helpers import wire_session_experience


def test_build_service_returns_facade():
    service = build_session_experience_service()
    assert isinstance(service, SessionExperienceService)


def test_set_and_get_service(session_app):
    custom = make_session_experience()
    set_session_experience_service(custom, app=session_app)
    with session_app.app_context():
        assert get_session_experience_service() is custom


def test_wire_helper(session_app):
    service = wire_session_experience(session_app)
    assert isinstance(service, SessionExperienceService)


def test_begin_session_form_fields(session_app):
    with session_app.app_context():
        form = BeginSessionForm()
        assert "session_id" in form._fields
        assert "mission_id" in form._fields


def test_submit_answer_form_fields(session_app):
    with session_app.app_context():
        form = SubmitAnswerForm()
        assert "response" in form._fields
        assert "activity_id" in form._fields


def test_other_forms_construct(session_app):
    with session_app.app_context():
        assert AdvanceActivityForm()
        assert ContinueReflectionForm()
        assert CompleteSessionForm()


def test_page_meta_for_each_surface():
    for surface in SessionSurface:
        eyebrow, title, description = page_meta(surface)
        assert eyebrow
        assert title
        assert description


def test_regression_blueprint_rules(session_app):
    rules = {rule.endpoint for rule in session_app.url_map.iter_rules()}
    for endpoint in (
        "session.overview",
        "session.begin",
        "session.activity",
        "session.answer",
        "session.advance",
        "session.reflection",
        "session.reflection_continue",
        "session.summary",
        "session.complete",
        "session.finish",
    ):
        assert endpoint in rules


def test_student_start_hands_off_to_session():
    """Student Experience start_session route redirects into /session/."""
    import inspect

    from app.presentation.student import routes as student_routes

    source = inspect.getsource(student_routes.start_session)
    assert "session.overview" in source
