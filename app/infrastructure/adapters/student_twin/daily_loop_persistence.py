"""Daily-loop Twin persistence (SDT-004).

Opaque documents keyed by learner (+ optional subject). Additive store —
no Alembic revision. Retained when ``SR_TWIN_DAILY_LOOP`` rolls back OFF.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.infrastructure.session.store import SessionDocumentStore

NS_DAILY_LOOP_TWIN = "sdt.daily_loop_twin"


class DailyLoopTwinPersistence:
    """Persist Student Twin daily-loop snapshots via SessionDocumentStore."""

    def __init__(self, *, store: SessionDocumentStore | None = None) -> None:
        self._store = store or SessionDocumentStore()

    @property
    def store(self) -> SessionDocumentStore:
        return self._store

    def _key(self, *, learner_id: str, subject_code: str | None) -> str:
        sid = learner_id.strip()
        subject = (subject_code or "").strip()
        return f"{sid}::{subject}" if subject else sid

    def save_twin(
        self,
        *,
        learner_id: str,
        subject_code: str | None,
        document: dict[str, Any],
    ) -> dict[str, Any]:
        key = self._key(learner_id=learner_id, subject_code=subject_code)
        payload = deepcopy(document)
        payload["learner_id"] = learner_id.strip()
        if subject_code:
            payload["subject_code"] = subject_code.strip()
        self._store.save(NS_DAILY_LOOP_TWIN, key, payload)
        return payload

    def load_twin(
        self,
        *,
        learner_id: str,
        subject_code: str | None = None,
    ) -> dict[str, Any] | None:
        key = self._key(learner_id=learner_id, subject_code=subject_code)
        doc = self._store.get(NS_DAILY_LOOP_TWIN, key)
        if doc is not None:
            return doc
        # Fall back to learner-only key when subject-scoped miss.
        if subject_code:
            return self._store.get(NS_DAILY_LOOP_TWIN, learner_id.strip())
        return None
