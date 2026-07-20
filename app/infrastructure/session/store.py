"""Opaque document store for Session Experience adapters.

Defaults to process-local memory. When a backing repository factory is
provided, documents are persisted via AggregateRepository (SQLAlchemy).
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from app.infrastructure.repositories.contracts import AggregateRepository

BackingFactory = Callable[[], AggregateRepository]


class SessionDocumentStore:
    """Opaque document store keyed by namespace + id."""

    def __init__(
        self,
        *,
        backing_repository_factory: BackingFactory | None = None,
    ) -> None:
        self._docs: dict[tuple[str, str], dict[str, Any]] = {}
        self._backing_factory = backing_repository_factory

    def _key(self, namespace: str, key: str) -> str:
        return f"{namespace.strip()}:{key.strip()}"

    def get(self, namespace: str, key: str) -> dict[str, Any] | None:
        if self._backing_factory is not None:
            doc = self._backing_factory().get(self._key(namespace, key))
            return None if doc is None else deepcopy(doc)
        doc = self._docs.get((namespace, key.strip()))
        return None if doc is None else deepcopy(doc)

    def save(self, namespace: str, key: str, document: dict[str, Any]) -> None:
        if self._backing_factory is not None:
            self._backing_factory().save(self._key(namespace, key), deepcopy(document))
            return
        self._docs[(namespace, key.strip())] = deepcopy(document)

    def delete(self, namespace: str, key: str) -> None:
        if self._backing_factory is not None:
            self._backing_factory().delete(self._key(namespace, key))
            return
        self._docs.pop((namespace, key.strip()), None)

    def clear(self) -> None:
        if self._backing_factory is not None:
            repo = self._backing_factory()
            for aggregate_id in repo.list_ids():
                repo.delete(aggregate_id)
            return
        self._docs.clear()
