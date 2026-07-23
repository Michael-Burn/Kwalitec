"""Lightweight SQLAlchemy query counter for route profiling (PR-001)."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from flask import Flask
from sqlalchemy import event
from sqlalchemy.engine import Engine

logger = logging.getLogger("kwalitec.performance")


@dataclass
class QueryProfile:
    """Collected query counts for a profiled block."""

    statements: int = 0

    def record(self, *_args, **_kwargs) -> None:
        self.statements += 1


@contextmanager
def count_queries(engine: Engine | None = None) -> Iterator[QueryProfile]:
    """Context manager that counts SQL statements on the given engine."""
    from app.extensions import db

    target = engine or db.engine
    profile = QueryProfile()
    event.listen(target, "before_cursor_execute", profile.record)
    try:
        yield profile
    finally:
        event.remove(target, "before_cursor_execute", profile.record)
        logger.info("query_profile statements=%s", profile.statements)


def register_query_profiling(app: Flask) -> None:
    """Optionally log per-request query counts when ``PROFILE_SQL=1``."""
    import os

    if os.getenv("PROFILE_SQL", "").strip() not in {"1", "true", "TRUE", "yes"}:
        return

    @app.before_request
    def _start_sql_profile():
        from flask import g

        from app.extensions import db

        profile = QueryProfile()
        g._sql_profile = profile
        g._sql_profile_listen = True
        event.listen(db.engine, "before_cursor_execute", profile.record)

    @app.after_request
    def _finish_sql_profile(response):
        from flask import g, request

        from app.extensions import db

        profile = getattr(g, "_sql_profile", None)
        if profile is not None:
            try:
                event.remove(db.engine, "before_cursor_execute", profile.record)
            except Exception:  # noqa: BLE001
                pass
            logger.info(
                "sql_profile method=%s path=%s statements=%s",
                request.method,
                request.path,
                profile.statements,
            )
        return response
