"""Navigation chrome tests."""

from __future__ import annotations

import pytest

from app.domain.student_experience.experience_workspace import (
    CANONICAL_SURFACES,
    ExperienceSurface,
)
from app.presentation.student.navigation import (
    SURFACE_ENDPOINTS,
    build_navigation,
    endpoint_for,
    surface_for_endpoint,
)


@pytest.mark.parametrize("surface", list(ExperienceSurface))
def test_endpoint_for_each_surface(surface):
    endpoint = endpoint_for(surface)
    assert endpoint.startswith("student.")
    assert SURFACE_ENDPOINTS[surface] == endpoint


@pytest.mark.parametrize("surface", list(CANONICAL_SURFACES))
def test_build_navigation_active(surface):
    nav = build_navigation(surface)
    assert len(nav) == 5
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
        (None, ExperienceSurface.HOME),
        ("other.thing", ExperienceSurface.HOME),
    ],
)
def test_surface_for_endpoint(endpoint, expected):
    assert surface_for_endpoint(endpoint) is expected


def test_navigation_labels_student_facing():
    nav = build_navigation("home")
    labels = {item.label for item in nav}
    assert labels == {"Home", "Journey", "Revision", "History", "Profile"}
