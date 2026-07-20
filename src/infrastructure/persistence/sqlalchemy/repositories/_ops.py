"""Shared persistence helpers for SQLAlchemy repository adapters."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

AggregateTracker = Callable[[Any], None]
"""Callback invoked when a repository persists a domain aggregate."""

def _noop_tracker(_: Any) -> None:
    pass


def get_by_pk(session: Session, model_cls: type[Any], primary_key: str) -> Any | None:
    return session.get(model_cls, primary_key)


def list_by_student(
    session: Session,
    model_cls: type[Any],
    student_id: str,
) -> list[Any]:
    statement = select(model_cls).where(model_cls.student_id == student_id)
    return list(session.scalars(statement))


def upsert(session: Session, row: Any) -> None:
    session.merge(row)
