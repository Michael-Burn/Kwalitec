"""Shared fixtures for Education OS web layer tests."""

from __future__ import annotations

import pytest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from application.composition import assemble
from web.app import WebConfig, create_app


@pytest.fixture
def session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=create_engine("sqlite+pysqlite:///:memory:"))


@pytest.fixture
def container(session_factory):
    return assemble(session_factory)


@pytest.fixture
def app(container) -> Flask:
    return create_app(
        WebConfig(testing=True, secret_key="test-secret"),
        container=container,
    )


@pytest.fixture
def client(app: Flask):
    return app.test_client()
