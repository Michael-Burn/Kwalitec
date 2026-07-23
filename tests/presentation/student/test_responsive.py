"""Responsive / layout marker tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.presentation.student.helpers import STUDENT_ROUTES


def test_css_has_breakpoints():
    css = Path("app/static/css/student/student.css").read_text(encoding="utf-8")
    assert "@media (min-width: 640px)" in css
    assert "@media (min-width: 480px)" in css
    assert "@media (min-width: 768px)" in css
    assert "@media (min-width: 1280px)" in css


def test_css_has_decision_screen_layout():
    css = Path("app/static/css/student/student.css").read_text(encoding="utf-8")
    assert ".student-hero" in css
    assert ".student-secondary" in css
    assert ".student-tertiary" in css
    assert "prefers-reduced-motion" in css


def test_css_has_max_content_width():
    css = Path("app/static/css/student/student.css").read_text(encoding="utf-8")
    assert "--student-max-width" in css


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_pages_use_student_shell_classes(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True)
    assert "student-shell" in html
    assert "student-main" in html
    assert "student-page-title" in html


@pytest.mark.parametrize(("endpoint", "path"), STUDENT_ROUTES)
def test_bootstrap_loaded(student_client, endpoint, path):
    html = student_client.get(path).get_data(as_text=True)
    assert "bootstrap" in html.lower()
