"""Fixtures for Assessment Delivery presentation tests."""

from __future__ import annotations

import pytest

from tests.presentation.assessment.helpers import wire_assessment_delivery


@pytest.fixture
def assessment_app(app):
    wire_assessment_delivery(app)
    return app


@pytest.fixture
def assessment_client(assessment_app, client, ctx, user):
    wire_assessment_delivery(assessment_app)
    client.post(
        "/auth/login",
        data={"email": "test@kwalitec.example", "password": "password123"},
        follow_redirects=True,
    )
    return client
