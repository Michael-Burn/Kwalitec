"""Navigation chrome tests."""

from __future__ import annotations

import pytest
from flask import render_template

from app.domain.student_experience.experience_workspace import (
    CANONICAL_SURFACES,
    ExperienceSurface,
)
from app.presentation.student.navigation import (
    SURFACE_ENDPOINTS,
    build_navigation,
    build_navigation_for_request,
    endpoint_for,
    surface_for_endpoint,
)

# Intentional feature-mode destinations (Part 1: no fully redundant removals).
_FEATURE_NAV_LABELS = {
    "Home",
    "Study",
    "Syllabus",
    "Revision",
    "History",
    "Stats",
    "Settings",
    "Choose Exam",
    "Help",
}

_FEATURE_NAV_ORDER = (
    "Home",
    "Study",
    "Syllabus",
    "Revision",
    "History",
    "Stats",
    "Settings",
    "Choose Exam",
    "Help",
)

_FEATURE_NAV_GROUPS = {
    "Home": "primary",
    "Study": "primary",
    "Syllabus": "primary",
    "Revision": "reinforce",
    "History": "reinforce",
    "Stats": "account",
    "Settings": "account",
    "Choose Exam": "system",
    "Help": "system",
}


@pytest.mark.parametrize("surface", list(ExperienceSurface))
def test_endpoint_for_each_surface(surface):
    endpoint = endpoint_for(surface)
    assert endpoint.startswith("student.")
    assert SURFACE_ENDPOINTS[surface] == endpoint


@pytest.mark.parametrize("surface", list(CANONICAL_SURFACES))
def test_build_navigation_active(surface):
    nav = build_navigation(surface)
    assert len(nav) == 9
    active = [item for item in nav if item.active]
    assert len(active) == 1
    assert active[0].surface == surface.value


@pytest.mark.parametrize(
    ("endpoint", "expected"),
    [
        ("student.home", ExperienceSurface.HOME),
        ("student.journey", ExperienceSurface.JOURNEY),
        ("student.revision", ExperienceSurface.REVISION),
        ("student.history", ExperienceSurface.HISTORY),
        ("student.profile", ExperienceSurface.PROFILE),
        ("settings.profile", ExperienceSurface.PROFILE),
        ("settings.preferences", ExperienceSurface.PROFILE),
        (None, ExperienceSurface.HOME),
        ("other.thing", ExperienceSurface.HOME),
    ],
)
def test_surface_for_endpoint(endpoint, expected):
    assert surface_for_endpoint(endpoint) is expected


def test_build_navigation_for_request_study_plan_active():
    nav = build_navigation_for_request("study_plan.wizard_step")
    active = [item for item in nav if item.active]
    assert len(active) == 1
    assert active[0].surface == "study_plan"


def test_build_navigation_for_request_help_active():
    nav = build_navigation_for_request("alpha.help_centre")
    active = [item for item in nav if item.active]
    assert len(active) == 1
    assert active[0].surface == "help"


def test_build_navigation_for_request_settings_maps_to_profile():
    nav = build_navigation_for_request("settings.preferences")
    active = [item for item in nav if item.active]
    assert len(active) == 1
    assert active[0].surface == ExperienceSurface.PROFILE.value


def test_navigation_labels_student_facing():
    nav = build_navigation("home")
    labels = {item.label for item in nav}
    assert labels == _FEATURE_NAV_LABELS


def test_navigation_has_no_duplicate_labels():
    nav = build_navigation("home")
    labels = [item.label for item in nav]
    assert len(labels) == len(set(labels))
    assert labels == list(_FEATURE_NAV_ORDER)


def test_navigation_groups_are_intentional():
    nav = build_navigation("home")
    by_label = {item.label: item.group for item in nav}
    assert by_label == _FEATURE_NAV_GROUPS
    # Revision and History remain reachable primary destinations.
    assert by_label["Revision"] == "reinforce"
    assert by_label["History"] == "reinforce"


def test_build_navigation_for_request_study_active():
    nav = build_navigation_for_request("student.study")
    active = [item for item in nav if item.active]
    assert len(active) == 1
    assert active[0].endpoint == "student.study"
    assert active[0].label == "Study"
    assert active[0].group == "primary"


def test_build_navigation_for_request_stats_active():
    nav = build_navigation_for_request("student.progress")
    active = [item for item in nav if item.active]
    assert len(active) == 1
    assert active[0].endpoint == "student.progress"
    assert active[0].label == "Stats"
    assert active[0].surface == "progress"
    assert active[0].group == "account"


def test_primary_nav_without_system_items():
    nav = build_navigation("home", include_system=False)
    assert len(nav) == 7
    assert {item.label for item in nav} == {
        "Home",
        "Study",
        "Syllabus",
        "Revision",
        "History",
        "Stats",
        "Settings",
    }
    assert all(item.group != "system" for item in nav)


def test_navigation_template_renders_group_separators(app, ctx):
    nav = build_navigation("home")
    with app.test_request_context("/student/"):
        html = render_template(
            "student/components/navigation.html",
            page=None,
            eos_navigation=nav,
        )
    assert 'data-nav-group="primary"' in html
    assert 'data-nav-group="reinforce"' in html
    assert 'data-nav-group="account"' in html
    assert 'data-nav-group="system"' in html
    assert 'data-nav-separator="primary-reinforce"' in html
    assert 'data-nav-separator="reinforce-account"' in html
    assert 'data-nav-separator="account-system"' in html
    assert "Revision" in html
    assert "History" in html
