"""Qualifying study day index persistence (Honest Progress foundation).

Additive opaque documents in SessionDocumentStore. Populated when Accepted
Evidence Packages are persisted; independent of Twin write path and
``SR_TWIN_DAILY_LOOP``.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.application.learner_progress.index_document import merge_qualifying_date
from app.application.learner_progress.qualifying_package import (
    learner_id_from_package,
    package_qualifies_for_study_day,
    study_date_from_package,
)
from app.infrastructure.session.store import SessionDocumentStore

NS_QUALIFYING_STUDY_DAYS = "lp.qualifying_study_days"


class QualifyingStudyDayIndexPersistence:
    """Persist qualifying study day index documents per learner."""

    def __init__(self, *, store: SessionDocumentStore | None = None) -> None:
        self._store = store or SessionDocumentStore()

    @property
    def store(self) -> SessionDocumentStore:
        return self._store

    def _key(self, *, learner_id: str) -> str:
        return learner_id.strip()

    def load_index(self, *, learner_id: str) -> dict[str, Any] | None:
        key = self._key(learner_id=learner_id)
        doc = self._store.get(NS_QUALIFYING_STUDY_DAYS, key)
        return None if doc is None else deepcopy(doc)

    def save_index(
        self, *, learner_id: str, document: dict[str, Any]
    ) -> dict[str, Any]:
        key = self._key(learner_id=learner_id)
        payload = deepcopy(document)
        payload["learner_id"] = key
        self._store.save(NS_QUALIFYING_STUDY_DAYS, key, payload)
        return deepcopy(payload)

    def record_from_evidence_package(self, package: dict[str, Any]) -> bool:
        """Update index when package qualifies; return True when indexed."""
        if not package_qualifies_for_study_day(package):
            return False
        learner_id = learner_id_from_package(package)
        study_date = study_date_from_package(package)
        if learner_id is None or study_date is None:
            return False
        existing = self.load_index(learner_id=learner_id)
        updated = merge_qualifying_date(
            existing,
            learner_id=learner_id,
            study_date=study_date,
        )
        self.save_index(learner_id=learner_id, document=updated)
        return True
