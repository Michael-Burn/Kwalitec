"""Unit-of-work strategy for Version 2 persistence.

One UoW per request / orchestration cycle. Repositories register work;
commit flushes atomically (in-memory or SQLAlchemy session).
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


class UnitOfWorkError(Exception):
    """Raised for illegal UoW state transitions."""


@dataclass
class WorkItem:
    """Deferred unit of work entry (no business rules)."""

    repository: str
    operation: str
    payload: dict[str, Any] = field(default_factory=dict)


class UnitOfWork:
    """Tracks transactional work across repositories.

    Strategy:
    - Begin on enter.
    - Repositories enqueue writes via ``register``.
    - Commit applies flush callbacks then clears.
    - Rollback discards work and invokes rollback callbacks.
    - Nested UoW is not supported (one boundary per request).
    """

    def __init__(self) -> None:
        self._active = False
        self._committed = False
        self._items: list[WorkItem] = []
        self._flushers: list[Callable[[], None]] = []
        self._rollbacks: list[Callable[[], None]] = []
        self._metadata: dict[str, Any] = {}

    @property
    def is_active(self) -> bool:
        """True while inside a transaction boundary."""
        return self._active

    @property
    def is_committed(self) -> bool:
        """True after a successful commit."""
        return self._committed

    @property
    def items(self) -> tuple[WorkItem, ...]:
        """Queued work items (diagnostics)."""
        return tuple(self._items)

    def begin(self) -> None:
        """Open a transaction boundary."""
        if self._active:
            raise UnitOfWorkError("unit of work already active")
        self._active = True
        self._committed = False
        self._items.clear()

    def register(
        self,
        repository: str,
        operation: str,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Enqueue a repository write inside the active boundary."""
        if not self._active:
            raise UnitOfWorkError("unit of work is not active")
        self._items.append(
            WorkItem(
                repository=repository,
                operation=operation,
                payload=dict(payload or {}),
            )
        )

    def on_flush(self, callback: Callable[[], None]) -> None:
        """Register a flush callback invoked on commit."""
        self._flushers.append(callback)

    def on_rollback(self, callback: Callable[[], None]) -> None:
        """Register a rollback callback."""
        self._rollbacks.append(callback)

    def set_metadata(self, key: str, value: Any) -> None:
        """Attach operational metadata (correlation id, etc.)."""
        self._metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Read operational metadata."""
        return self._metadata.get(key, default)

    def commit(self) -> int:
        """Flush registered work atomically. Returns item count."""
        if not self._active:
            raise UnitOfWorkError("unit of work is not active")
        try:
            for flusher in self._flushers:
                flusher()
        except Exception:
            self.rollback()
            raise
        count = len(self._items)
        self._items.clear()
        self._flushers.clear()
        self._rollbacks.clear()
        self._active = False
        self._committed = True
        return count

    def rollback(self) -> None:
        """Discard work and invoke rollback callbacks."""
        if not self._active and not self._items:
            return
        for cb in self._rollbacks:
            cb()
        self._items.clear()
        self._flushers.clear()
        self._rollbacks.clear()
        self._active = False
        self._committed = False

    @contextmanager
    def transaction(self) -> Iterator[UnitOfWork]:
        """Context manager: begin / commit, rollback on error."""
        self.begin()
        try:
            yield self
            self.commit()
        except Exception:
            self.rollback()
            raise


class SqlAlchemyUnitOfWork(UnitOfWork):
    """UoW that flushes an optional SQLAlchemy session on commit.

    Session is injected so application services never import Flask globals.
    """

    def __init__(self, session: Any | None = None) -> None:
        super().__init__()
        self._session = session

    def commit(self) -> int:
        """Flush in-memory work then commit the ORM session when present."""
        count = super().commit()
        if self._session is not None:
            self._session.commit()
        return count

    def rollback(self) -> None:
        """Rollback in-memory work and the ORM session when present."""
        if self._session is not None:
            self._session.rollback()
        super().rollback()
