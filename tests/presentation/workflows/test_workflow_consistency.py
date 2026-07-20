"""Consistency checks — breadcrumbs, titles, CTAs, terminology, flashes."""

from __future__ import annotations

import pytest

from app.domain.curriculum_studio.workflow_stage import WorkflowStage
from app.domain.session_experience.session_workspace import (
    SURFACE_LABELS,
    SessionSurface,
)
from app.presentation.curriculum_studio.view_models import (
    FLASH_SUCCESS,
    FLASH_WARNING,
    STAGE_LABELS,
)
from app.presentation.session.navigation import page_meta
from tests.presentation.workflows.helpers import (
    login_founder,
    login_student,
    wire_session,
    wire_studio,
)


@pytest.fixture
def student_client(app, client, ctx, user):
    wire_session(app)
    login_student(client)
    return client


@pytest.fixture
def founder_client(app, client, ctx):
    wire_studio(app, with_workspace=True)
    login_founder(client, app)
    return client


STUDIO_SUCCESS_KEYS = (
    "subject_created",
    "workspace_opened",
    "workflow_advanced",
    "validation_ok",
    "preview_ok",
    "approved",
    "published",
    "version_assigned",
)

STUDIO_WARNING_KEYS = (
    "subject_create",
    "workspace_open",
    "advance",
    "validate",
    "preview",
    "approve",
    "publish",
    "version",
    "workspace_missing",
)


@pytest.mark.parametrize("key", STUDIO_SUCCESS_KEYS)
def test_studio_success_flashes_are_sentences(key):
    msg = FLASH_SUCCESS[key]
    assert msg.endswith(".")
    assert msg[0].isupper()
    assert "successfully" in msg.lower() or "advanced" in msg.lower()


@pytest.mark.parametrize("key", STUDIO_WARNING_KEYS)
def test_studio_warning_flashes_guide_recovery(key):
    msg = FLASH_WARNING[key]
    assert msg.endswith(".")
    assert "try again" in msg.lower() or "found" in msg.lower()


@pytest.mark.parametrize("stage", list(WorkflowStage))
def test_studio_stage_labels_title_case(stage):
    label = STAGE_LABELS[stage.value]
    assert label[0].isupper()
    assert "_" not in label


@pytest.mark.parametrize("surface", list(SessionSurface))
def test_session_surface_labels_stable(surface):
    label = SURFACE_LABELS[surface]
    assert label
    assert label[0].isupper()
    eyebrow, title, _ = page_meta(surface)
    assert title == label
    assert "Step" in eyebrow


def test_session_primary_cta_language(student_client):
    html = student_client.get("/session/sess-cta/overview").get_data(as_text=True)
    assert "Begin Session" in html


def test_studio_primary_buttons_human_language(founder_client):
    html = founder_client.get("/founder/studio/workspaces/ws-cs1").get_data(
        as_text=True
    )
    # Prefer product language over command jargon.
    assert "execute publish" not in html.lower()
    assert "Publish" in html or "publish" in html.lower()


def test_student_page_titles(student_client):
    for path, needle in (
        ("/student/", "Home"),
        ("/student/journey", "Journey"),
        ("/student/revision", "Revision"),
        ("/student/history", "History"),
        ("/student/profile", "Profile"),
    ):
        html = student_client.get(path).get_data(as_text=True)
        assert needle in html


def test_founder_page_titles(founder_client):
    for path, needle in (
        ("/founder/studio/", "Curriculum Studio"),
        ("/founder/intelligence", "Founder Intelligence"),
        ("/founder/evidence-gates", "Evidence Gates"),
    ):
        html = founder_client.get(path).get_data(as_text=True)
        assert needle in html


def test_flash_partial_included_on_student(student_client):
    html = student_client.get("/student/").get_data(as_text=True)
    assert 'id="student-main"' in html or "student-main" in html
    assert "student-shell" in html


def test_session_and_student_share_brand(student_client):
    student = student_client.get("/student/").get_data(as_text=True)
    session = student_client.get("/session/sess-brand2/overview").get_data(as_text=True)
    assert "Kwalitec" in student
    assert "Kwalitec" in session


def test_no_duplicate_primary_nav_labels():
    from app.founder.dashboard.nav import COMMAND_CENTRE_NAV

    labels = [i.label for i in COMMAND_CENTRE_NAV]
    assert labels.count("Studio") == 1
    assert labels.count("Intelligence") == 1
    assert labels.count("Evidence Gates") == 1


def test_publication_stage_ui_says_publish_not_publication():
    assert STAGE_LABELS[WorkflowStage.PUBLICATION.value] == "Publish"


def test_content_sources_label_human():
    assert STAGE_LABELS[WorkflowStage.CONTENT_SOURCES.value] == "Content Sources"
