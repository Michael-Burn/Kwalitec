"""Fixtures for Student Experience presentation tests."""

from __future__ import annotations

import pytest

from tests.presentation.student.helpers import wire_experience


@pytest.fixture
def experience_app(app):
    """App with Student Experience wired to fake ports."""
    wire_experience(app)
    return app


@pytest.fixture
def student_client(experience_app, client, ctx, user):
    """Logged-in client against an experience-wired app."""
    # Wire before login so the first authenticated request uses fakes.
    wire_experience(experience_app)
    client.post(
        "/auth/login",
        data={"email": "test@kwalitec.example", "password": "password123"},
        follow_redirects=True,
    )
    return client
