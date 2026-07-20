"""Shared fixtures for INF-003 SQLAlchemy repository tests."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from infrastructure.persistence.sqlalchemy import metadata


@pytest.fixture()
def engine():
    eng = create_engine("sqlite:///:memory:")
    metadata.create_all(eng)
    yield eng
    eng.dispose()


@pytest.fixture()
def session_factory(engine):
    return sessionmaker(bind=engine, expire_on_commit=False, class_=Session)


@pytest.fixture()
def session(session_factory):
    with session_factory() as sess:
        yield sess
        sess.rollback()
