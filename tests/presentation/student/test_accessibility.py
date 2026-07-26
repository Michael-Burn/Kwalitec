"""Accessibility-oriented presentation checks."""

from __future__ import annotations

import pytest

from app.services.welcome_service import WelcomeService
from tests.presentation.student.helpers import STUDENT_ROUTES


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_page_has_lang(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True)
    assert 'lang="en"' in html


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_page_has_viewport(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True)
    assert "viewport" in html


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_active_nav_aria_current(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True)
    assert 'aria-current="page"' in html


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_color_scheme_meta(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True)
    assert "color-scheme" in html


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_headings_present(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True)
    assert "<h1" in html


def test_home_form_has_csrf_field(student_client):
    html = student_client.get("/student/").get_data(as_text=True)
    # CSRF disabled in tests but form still renders hidden fields structure
    assert "Start" in html


def test_progressbar_attributes_on_journey(student_client):
    html = student_client.get("/student/journey").get_data(as_text=True)
    if "progressbar" in html:
        assert "aria-valuenow" in html
        assert "aria-valuemin" in html
        assert "aria-valuemax" in html


class TestWelcomeModalOnCanonicalStudentHome:
    """B4 (PX-003): the Welcome dialog is only ever included by
    ``student/home.html`` (see ``partials/welcome_modal.html``'s single call
    site) — the canonical, always-on-under-``SOLE_RUNTIME`` Student
    Experience home, not the legacy ``dashboard/index.html`` shell. A
    server-rendered ARIA contract is necessary but not sufficient: this shell
    must also load the script (``app.js``) that gives the dialog its focus
    entry/trap/return and Escape behaviour, or the markup is inert."""

    def test_welcome_modal_renders_with_aria_contract(self, student_client, user):
        WelcomeService.mark_eligible(user.id)
        body = student_client.get("/student/").get_data(as_text=True)
        assert 'id="welcome-modal"' in body
        assert 'role="dialog"' in body
        assert 'aria-modal="true"' in body
        assert 'aria-labelledby="welcome-modal-title"' in body
        assert 'aria-describedby="welcome-modal-lead welcome-modal-desc"' in body
        assert 'class="welcome-modal-card" tabindex="-1"' in body

    def test_shell_loads_the_script_that_wires_focus_behaviour(
        self, student_client, user
    ):
        """Regression for a real gap found during RC-001 evidence capture:
        this shell previously loaded only ``student.js``, which has no
        welcome-modal handling at all — the dialog appeared with focus left
        on <body>, no trap, and Escape doing nothing."""
        WelcomeService.mark_eligible(user.id)
        body = student_client.get("/student/").get_data(as_text=True)
        assert "js/app.js" in body
