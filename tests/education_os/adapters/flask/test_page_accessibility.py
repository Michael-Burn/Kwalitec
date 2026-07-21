"""Accessibility checks for end-to-end eos page templates (V4-004)."""

from __future__ import annotations

import re

import pytest


@pytest.mark.parametrize(
    "path",
    (
        "/eos/login/",
        "/eos/dashboard/?student_id=student-ada",
        "/eos/mission/?student_id=student-ada",
        "/eos/session/?student_id=student-ada",
        "/eos/reflection/?student_id=student-ada",
    ),
)
def test_pages_have_main_landmark_and_lang(client, path: str) -> None:
    html = client.get(path).get_data(as_text=True)
    assert 'lang="en"' in html
    assert 'role="main"' in html or "<main" in html
    assert "<h1" in html


def test_dashboard_nav_is_labelled(client) -> None:
    html = client.get("/eos/dashboard/?student_id=student-ada").get_data(as_text=True)
    assert 'aria-label="Student journey"' in html


def test_reflection_form_fields_are_labelled(client) -> None:
    html = client.get("/eos/reflection/?student_id=student-ada").get_data(as_text=True)
    assert 'for="confidence"' in html
    assert 'id="confidence"' in html
    assert 'for="difficulty"' in html
    assert 'for="weak_concept"' in html
    assert 'for="student_notes"' in html


def test_session_actions_form_labelled(client) -> None:
    html = client.get("/eos/session/?student_id=student-ada").get_data(as_text=True)
    assert 'aria-label="Session actions"' in html
    assert re.search(r'name="action"\s+value="start"', html)


def test_login_input_has_accessible_name(client) -> None:
    html = client.get("/eos/login/").get_data(as_text=True)
    assert 'for="student_id"' in html
    assert 'id="student_id"' in html
