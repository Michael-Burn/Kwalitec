"""Spacing state adapter over SessionDocumentStore (Twin durability pattern).

Uses the same opaque document store and ``LearningSessionDocument`` aggregate
as Twin/session when ``KWALITEC_V2_DURABLE_STORE`` is on. Spacing docs live in
a dedicated namespace so they never mix with Twin snapshots.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from app.domain.spacing_scheduler.types import ExposureKind, SpacingState
from app.infrastructure.session.store import SessionDocumentStore

NS_SPACING_STATE = "spacing.state"


class SessionDocumentSpacingStateStore:
    """``SpacingStateStore`` backed by ``SessionDocumentStore``.

    Durable when the document store is built with aggregate SQL backing
    (``build_session_document_store`` under ``ENABLE_DURABLE_STORE``).
    """

    def __init__(self, *, store: SessionDocumentStore) -> None:
        self._store = store

    @property
    def document_store(self) -> SessionDocumentStore:
        return self._store

    def get(self, learner_id: str, unit_id: str) -> SpacingState | None:
        doc = self._store.get(
            NS_SPACING_STATE, self._key(learner_id.strip(), unit_id.strip())
        )
        if doc is None:
            return None
        return self._from_doc(doc)

    def put(self, state: SpacingState) -> None:
        self._store.save(
            NS_SPACING_STATE,
            self._key(state.learner_id, state.unit_id),
            self._to_doc(state),
        )

    def list_for_learner(self, learner_id: str) -> tuple[SpacingState, ...]:
        lid = learner_id.strip()
        states: list[SpacingState] = []
        for doc in self._store.list_documents(NS_SPACING_STATE):
            if not isinstance(doc, dict):
                continue
            if str(doc.get("learner_id", "")).strip() != lid:
                continue
            states.append(self._from_doc(doc))
        return tuple(states)

    def clear(self) -> None:
        """Remove only spacing-namespace documents (tests / isolation)."""
        for doc in list(self._store.list_documents(NS_SPACING_STATE)):
            if not isinstance(doc, dict):
                continue
            learner = str(doc.get("learner_id", "")).strip()
            unit = str(doc.get("unit_id", "")).strip()
            if not learner or not unit:
                continue
            self._store.delete(NS_SPACING_STATE, self._key(learner, unit))

    @staticmethod
    def _key(learner_id: str, unit_id: str) -> str:
        return f"{learner_id}::{unit_id}"

    @staticmethod
    def _to_doc(state: SpacingState) -> dict[str, Any]:
        return {
            "learner_id": state.learner_id,
            "unit_id": state.unit_id,
            "last_completed_on": state.last_completed_on.isoformat(),
            "current_interval_days": state.current_interval_days,
            "next_due_on": state.next_due_on.isoformat(),
            "review_cycle_count": state.review_cycle_count,
            "last_exposure_kind": state.last_exposure_kind.value,
        }

    @staticmethod
    def _from_doc(doc: dict[str, Any]) -> SpacingState:
        return SpacingState(
            learner_id=str(doc["learner_id"]).strip(),
            unit_id=str(doc["unit_id"]).strip(),
            last_completed_on=date.fromisoformat(str(doc["last_completed_on"])),
            current_interval_days=int(doc["current_interval_days"]),
            next_due_on=date.fromisoformat(str(doc["next_due_on"])),
            review_cycle_count=int(doc["review_cycle_count"]),
            last_exposure_kind=ExposureKind(str(doc["last_exposure_kind"])),
        )
