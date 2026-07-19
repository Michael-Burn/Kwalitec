"""Form tests for Student Experience presentation."""

from __future__ import annotations

from app.presentation.student.forms import BeginRevisionForm, StartSessionForm


def test_start_session_form_fields(experience_app):
    with experience_app.test_request_context():
        form = StartSessionForm()
        assert "mission_id" in form._fields
        assert "session_id" in form._fields
        assert "submit" in form._fields


def test_begin_revision_form_fields(experience_app):
    with experience_app.test_request_context():
        form = BeginRevisionForm()
        assert "option_id" in form._fields
        assert form.submit.label.text == "Begin Revision"


def test_start_session_submit_label(experience_app):
    with experience_app.test_request_context():
        form = StartSessionForm()
        assert "Session" in form.submit.label.text
