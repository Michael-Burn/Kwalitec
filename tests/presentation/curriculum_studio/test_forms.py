"""Form behaviour tests for Curriculum Studio Founder UX."""

from __future__ import annotations

import pytest

from app.presentation.curriculum_studio.forms import (
    AdvanceWorkflowForm,
    ApproveWorkspaceForm,
    AssignVersionForm,
    CreateSubjectForm,
    CreateWorkspaceForm,
    PreviewWorkspaceForm,
    PublishWorkspaceForm,
    ValidateWorkspaceForm,
)


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        with app.test_request_context():
            yield


FORM_CLASSES = (
    CreateSubjectForm,
    CreateWorkspaceForm,
    ValidateWorkspaceForm,
    PublishWorkspaceForm,
    AssignVersionForm,
)


@pytest.mark.parametrize("form_cls", FORM_CLASSES)
def test_forms_have_submit_labels(app_ctx, form_cls):
    form = form_cls()
    assert form.submit.label.text
    assert "execute" not in form.submit.label.text.lower()


def test_create_subject_requires_code(app_ctx):
    form = CreateSubjectForm(meta={"csrf": False}, formdata=None)
    form.subject_code.data = ""
    form.title.data = "Title"
    assert form.validate() is False
    assert "required" in form.subject_code.errors[0].lower()


def test_create_subject_accepts_valid(app_ctx):
    form = CreateSubjectForm(
        data={"subject_code": "CS1", "title": "Core Stats"},
        meta={"csrf": False},
    )
    assert form.validate() is True


def test_create_workspace_placeholder(app_ctx):
    form = CreateWorkspaceForm()
    assert "CS1" in (form.subject_code.render_kw or {}).get("placeholder", "")
    assert form.subject_code.render_kw.get("aria-required") == "true"


def test_publish_button_says_publish_curriculum(app_ctx):
    form = PublishWorkspaceForm()
    assert form.submit.label.text == "Publish Curriculum"


def test_validate_button_says_validate_curriculum(app_ctx):
    form = ValidateWorkspaceForm()
    assert form.submit.label.text == "Validate Curriculum"


def test_approve_optional_reason_placeholder(app_ctx):
    form = ApproveWorkspaceForm()
    assert "Optional" in (form.reason.render_kw or {}).get("placeholder", "")


def test_assign_version_requires_label(app_ctx):
    form = AssignVersionForm(
        data={"workspace_id": "ws-1", "version_label": ""},
        meta={"csrf": False},
    )
    assert form.validate() is False
    assert form.version_label.errors


def test_assign_version_accepts_semver(app_ctx):
    form = AssignVersionForm(
        data={"workspace_id": "ws-1", "version_label": "1.0.0"},
        meta={"csrf": False},
    )
    assert form.validate() is True


def test_advance_and_preview_labels(app_ctx):
    assert AdvanceWorkflowForm().submit.label.text == "Advance to Next Stage"
    assert PreviewWorkspaceForm().submit.label.text == "Build Preview"


def test_required_fields_expose_aria(app_ctx):
    subject = CreateSubjectForm()
    version = AssignVersionForm()
    assert subject.subject_code.render_kw["aria-required"] == "true"
    assert version.version_label.render_kw["aria-required"] == "true"
