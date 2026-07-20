"""Session factory for Education OS persistence.

Provides a SQLAlchemy ``sessionmaker`` only. Repositories are constructed
separately with an injected ``Session``.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def create_session_factory(
    bind: Engine | str,
    **engine_kwargs: Any,
) -> sessionmaker[Session]:
    """Return a configured ``sessionmaker`` bound to ``bind``.

    Args:
        bind: An Engine instance or a database URL string.
        **engine_kwargs: Forwarded to ``create_engine`` when ``bind`` is a URL.

    Returns:
        A ``sessionmaker`` that produces ``Session`` instances.
    """
    engine = bind if isinstance(bind, Engine) else create_engine(bind, **engine_kwargs)
    return sessionmaker(bind=engine, expire_on_commit=False, class_=Session)
