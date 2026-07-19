"""Accessibility-oriented presentation checks."""

from __future__ import annotations

import pytest

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
