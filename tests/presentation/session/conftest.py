"""Fixtures for Learning Session Experience presentation tests."""

from __future__ import annotations

import pytest

from tests.presentation.session.helpers import wire_session_experience


@pytest.fixture
def session_app(app):
    wire_session_experience(app)
    return app


@pytest.fixture
def session_client(session_app, client, ctx, user):
    wire_session_experience(session_app)
    client.post(
        "/auth/login",
        data={"email": "test@kwalitec.example", "password": "password123"},
        follow_redirects=True,
    )
    return client
