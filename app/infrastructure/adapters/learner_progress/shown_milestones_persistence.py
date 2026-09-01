"""Persistence for milestones already announced (Honest Progress).

Append-only opaque documents in SessionDocumentStore. Independent of Twin
write path and Study Progress writers.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import date
from typing import Any

from app.application.learner_progress.shown_milestones import (
    ShownMilestoneRecord,
    append_shown_milestone,
    parse_shown_records,
    shown_milestone_ids,
)
from app.infrastructure.session.store import SessionDocumentStore

NS_MILESTONES_SHOWN = "lp.milestones_shown"


class MilestonesShownPersistence:
    """Persist which milestones have already been announced to a learner."""

    def __init__(self, *, store: SessionDocumentStore | None = None) -> None:
        self._store = store or SessionDocumentStore()

    @property
    def store(self) -> SessionDocumentStore:
        return self._store

    def _key(self, *, learner_id: str) -> str:
        return learner_id.strip()

    def load_document(self, *, learner_id: str) -> dict[str, Any] | None:
        key = self._key(learner_id=learner_id)
        doc = self._store.get(NS_MILESTONES_SHOWN, key)
        return None if doc is None else deepcopy(doc)

    def save_document(
        self, *, learner_id: str, document: dict[str, Any]
    ) -> dict[str, Any]:
        key = self._key(learner_id=learner_id)
        payload = deepcopy(document)
        payload["learner_id"] = key
        self._store.save(NS_MILESTONES_SHOWN, key, payload)
        return deepcopy(payload)

    def previously_shown_ids(self, *, learner_id: str) -> frozenset[str]:
        return shown_milestone_ids(self.load_document(learner_id=learner_id))

    def list_shown(self, *, learner_id: str) -> tuple[ShownMilestoneRecord, ...]:
        return parse_shown_records(self.load_document(learner_id=learner_id))

    def record_shown(
        self,
        *,
        learner_id: str,
        milestone_id: str,
        label: str,
        shown_at: date,
    ) -> bool:
        """Append one shown milestone. Return True when newly recorded."""
        existing = self.load_document(learner_id=learner_id)
        before = shown_milestone_ids(existing)
        mid = (milestone_id or "").strip()
        if not mid or mid in before:
            return False
        updated = append_shown_milestone(
            existing,
            learner_id=learner_id,
            milestone_id=mid,
            label=label,
            shown_at=shown_at,
        )
        self.save_document(learner_id=learner_id, document=updated)
        return True
