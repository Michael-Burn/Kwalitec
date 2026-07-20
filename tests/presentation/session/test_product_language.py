"""ARP-004 product language tests — Student / Session presentation."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.product_language import (
    REJECTED_SYNONYMS,
    STUDENT_NAV_LABELS,
    STUDENT_PRIMARY_CTAS,
)
from app.presentation.session.forms import (
    AdvanceActivityForm,
    BeginSessionForm,
    CompleteSessionForm,
    ContinueReflectionForm,
    SubmitAnswerForm,
)
from app.presentation.session.messages import FLASH_SUCCESS, FLASH_WARNING
from app.presentation.session.navigation import page_meta
from app.presentation.student.forms import StartSessionForm
from tests.presentation.student.helpers import STUDENT_ROUTES, wire_experience
from tests.presentation.workflows.helpers import login_student, wire_session

GUIDE = Path("knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md")
SESSION_TEMPLATES = Path("app/templates/session")
STUDENT_TEMPLATES = Path("app/templates/student")


@pytest.fixture
def student_client(app, client, ctx, user):
    wire_experience(app)
    wire_session(app)
    login_student(client)
    return client


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        with app.test_request_context():
            yield


# --- Documentation ---------------------------------------------------------


def test_product_language_guide_exists():
    assert GUIDE.is_file()


@pytest.mark.parametrize(
    "heading",
    (
        "Approved terminology",
        "Writing principles",
        "Preferred button labels",
        "Error / warning",
        "Future naming conventions",
    ),
)
def test_guide_has_required_sections(heading):
    text = GUIDE.read_text(encoding="utf-8")
    assert heading in text


@pytest.mark.parametrize(
    "term",
    ("Session", "Publish", "Journey", "Learning Insights"),
)
def test_guide_lists_approved_terms(term):
    assert term in GUIDE.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "rejected",
    ("Study Session", "Learning Session", "Go Live", "Twin Insights"),
)
def test_guide_rejects_synonyms(rejected):
    assert rejected in GUIDE.read_text(encoding="utf-8")


# --- Student navigation ----------------------------------------------------


@pytest.mark.parametrize("label", STUDENT_NAV_LABELS)
def test_student_nav_label_on_home(student_client, label):
    html = student_client.get("/student/").get_data(as_text=True)
    assert label in html


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_student_routes_avoid_rejected_synonyms(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True).lower()
    for term in REJECTED_SYNONYMS:
        assert term not in html, f"{endpoint} contains rejected term {term!r}"


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_student_page_titles_use_approved_nav(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True)
    assert any(label in html for label in STUDENT_NAV_LABELS)


def test_home_primary_cta_label(app_ctx):
    assert StartSessionForm().submit.label.text == "Start Today's Session"


def test_home_cta_in_approved_list():
    assert "Start Today's Session" in STUDENT_PRIMARY_CTAS


# --- Session CTAs ----------------------------------------------------------


@pytest.mark.parametrize(
    ("form_cls", "label"),
    (
        (BeginSessionForm, "Begin Session"),
        (SubmitAnswerForm, "Submit Answer"),
        (AdvanceActivityForm, "Continue"),
        (ContinueReflectionForm, "Continue to Summary"),
        (CompleteSessionForm, "Return Home"),
    ),
)
def test_session_form_cta_labels(app_ctx, form_cls, label):
    assert form_cls().submit.label.text == label
    assert label in STUDENT_PRIMARY_CTAS


def test_session_overview_shows_begin_session(student_client):
    html = student_client.get("/session/sess-lang/overview").get_data(as_text=True)
    assert "Begin Session" in html


def test_session_eyebrow_uses_session_not_learning_session(student_client):
    html = student_client.get("/session/sess-lang2/overview").get_data(as_text=True)
    assert "Session · Step" in html
    assert "Learning Session ·" not in html


@pytest.mark.parametrize("surface", list(SessionSurface))
def test_session_page_meta_avoids_learning_session_prefix(surface):
    eyebrow, title, _ = page_meta(surface)
    assert eyebrow.startswith("Session · Step")
    assert "Learning Session" not in eyebrow
    assert title


# --- Session flash messages ------------------------------------------------


@pytest.mark.parametrize("key", list(FLASH_SUCCESS))
def test_session_success_flashes_are_sentences(key):
    msg = FLASH_SUCCESS[key]
    assert msg.endswith(".")
    assert msg[0].isupper()


@pytest.mark.parametrize("key", list(FLASH_WARNING))
def test_session_warning_flashes_guide_recovery(key):
    msg = FLASH_WARNING[key]
    lowered = msg.lower()
    assert msg.endswith(".")
    assert any(
        token in lowered
        for token in ("try again", "return home", "enter an answer", "check")
    )


def test_session_flash_avoids_learning_session_phrase():
    blob = " ".join(FLASH_SUCCESS.values()) + " " + " ".join(FLASH_WARNING.values())
    assert "learning session" not in blob.lower()
    assert "study session" not in blob.lower()


def test_resume_flash_copy():
    assert "continuing where you left off" in FLASH_SUCCESS["resumed"].lower()


def test_begun_flash_uses_session_started():
    assert FLASH_SUCCESS["begun"].startswith("Session started")


def test_completed_flash_mentions_home():
    assert "home" in FLASH_SUCCESS["completed"].lower()


def test_missing_session_flash_guides_home():
    assert "return home" in FLASH_WARNING["missing"].lower()


def test_begin_unavailable_uses_we_or_session():
    msg = FLASH_WARNING["begin_unavailable"].lower()
    assert "session" in msg
    assert "try again" in msg


# --- Template static checks ------------------------------------------------


def test_session_templates_avoid_study_session():
    for path in SESSION_TEMPLATES.rglob("*.html"):
        text = path.read_text(encoding="utf-8").lower()
        assert "study session" not in text, path


def test_session_templates_avoid_learning_session_chrome():
    for path in SESSION_TEMPLATES.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        assert "Learning Session ·" not in text, path
        assert "Focused Learning Session" not in text, path


def test_student_templates_avoid_roadmap_label():
    for path in STUDENT_TEMPLATES.rglob("*.html"):
        text = path.read_text(encoding="utf-8").lower()
        assert "roadmap" not in text, path
        assert "progress path" not in text, path


def test_student_home_empty_mentions_learning_insights():
    home = (STUDENT_TEMPLATES / "home.html").read_text(encoding="utf-8").lower()
    assert "learning insights" in home


def test_session_routes_use_flash_constants():
    source = Path("app/presentation/session/routes.py").read_text(encoding="utf-8")
    assert "FLASH_SUCCESS" in source
    assert "FLASH_WARNING" in source
    assert 'flash("Could not begin session' not in source
    assert "Learning Session is temporarily" not in source
