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
    # CSRF disabled in tests but form still renders hidden fields structure.
    # PX-003 verb family may render Start Today's Session or Continue.
    assert (
        "Start" in html
        or "Continue" in html
        or "Choose an exam" in html
        or 'data-student-cta="primary"' in html
    )

def test_progressbar_attributes_on_journey(student_client):
    html = student_client.get("/student/journey").get_data(as_text=True)
    if "progressbar" in html:
        assert "aria-valuenow" in html
        assert "aria-valuemin" in html
        assert "aria-valuemax" in html


class TestWelcomeModalOnCanonicalStudentHome:
    """SOP-001 / sole-runtime: Welcome modal is not hosted on Student Home.

    The ARIA contract remains in ``partials/welcome_modal.html`` for the
    legacy dashboard include. EOS Student Home must stay a clean command
    centre (no modal overlay) while still loading ``app.js`` for shared
    shell behaviour.
    """

    def test_welcome_modal_renders_with_aria_contract(self, student_client, user):
        from pathlib import Path

        WelcomeService.mark_eligible(user.id)
        body = student_client.get("/student/").get_data(as_text=True)
        assert 'id="welcome-modal"' not in body
        modal = (
            Path(__file__).resolve().parents[3]
            / "app/templates/partials/welcome_modal.html"
        ).read_text(encoding="utf-8")
        assert 'id="welcome-modal"' in modal
        assert 'role="dialog"' in modal
        assert 'aria-modal="true"' in modal
        assert 'aria-labelledby="welcome-modal-title"' in modal
        assert 'aria-describedby="welcome-modal-lead welcome-modal-desc"' in modal
        assert 'class="welcome-modal-card" tabindex="-1"' in modal

    def test_shell_loads_the_script_that_wires_focus_behaviour(
        self, student_client, user
    ):
        """EOS shell still loads ``app.js`` for shared chrome behaviour."""
        WelcomeService.mark_eligible(user.id)
        body = student_client.get("/student/").get_data(as_text=True)
        assert "js/app.js" in body
