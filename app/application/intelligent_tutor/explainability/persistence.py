"""Explanation persistence — append-only store for Tutor explanations.

No Alembic migrations. Stores explanations / events in-process for
deterministic replay and duplicate-request protection.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from threading import RLock

from app.domain.intelligent_tutor.explainability.explanation import TutorExplanation
from app.domain.intelligent_tutor.explainability.result import (
    ExplanationEvent,
    ExplanationResult,
)


@dataclass
class _TwinExplanationLedger:
    """Append-only ledger for one twin."""

    twin_id: str
    explanations_by_id: dict[str, TutorExplanation] = field(default_factory=dict)
    events: list[ExplanationEvent] = field(default_factory=list)
    request_ids: set[str] = field(default_factory=set)
    versions: list[str] = field(default_factory=list)


class ExplanationPersistenceService:
    """Deterministic, idempotent explanation store with replay support."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._ledgers: dict[str, _TwinExplanationLedger] = {}

    def _ledger(self, *, twin_id: str) -> _TwinExplanationLedger:
        ledger = self._ledgers.get(twin_id)
        if ledger is None:
            ledger = _TwinExplanationLedger(twin_id=twin_id)
            self._ledgers[twin_id] = ledger
        return ledger

    def existing_request_ids(self, *, twin_id: str) -> frozenset[str]:
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return frozenset()
            return frozenset(ledger.request_ids)

    def get_explanation(
        self, *, twin_id: str, explanation_id: str
    ) -> TutorExplanation | None:
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return None
            return ledger.explanations_by_id.get(explanation_id)

    def list_explanations(self, *, twin_id: str) -> tuple[TutorExplanation, ...]:
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return ()
            return tuple(
                ledger.explanations_by_id[eid]
                for eid in sorted(ledger.explanations_by_id.keys())
            )

    def list_events(self, *, twin_id: str) -> tuple[ExplanationEvent, ...]:
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return ()
            return tuple(ledger.events)

    def version_history(self, *, twin_id: str) -> tuple[str, ...]:
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return ()
            return tuple(ledger.versions)

    def persist(self, result: ExplanationResult) -> ExplanationResult:
        """Append explanation result. Idempotent for identical request ids."""
        context = result.context
        with self._lock:
            ledger = self._ledger(twin_id=context.twin_id)
            ledger.explanations_by_id[result.explanation.explanation_id] = (
                result.explanation
            )
            ledger.events.extend(result.events)
            ledger.request_ids.add(context.explanation_request_id)
            ledger.versions.append(result.explanation.explanation_id)
            return result

    def snapshot(self, *, twin_id: str) -> dict:
        """Deterministic serialisable snapshot for replay comparison."""
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return {
                    "twin_id": twin_id,
                    "explanations": [],
                    "event_kinds": [],
                    "request_ids": [],
                    "versions": [],
                }
            return {
                "twin_id": twin_id,
                "explanations": [
                    {
                        "explanation_id": e.explanation_id,
                        "available": e.available,
                        "section_ids": list(e.section_ids),
                        "decision_ids": list(e.decision_ids),
                        "summary": e.summary,
                        "explanation_version": e.explanation_version,
                        "provenance": dict(e.provenance),
                    }
                    for e in sorted(
                        ledger.explanations_by_id.values(),
                        key=lambda item: item.explanation_id,
                    )
                ],
                "event_kinds": [e.kind.value for e in ledger.events],
                "request_ids": sorted(ledger.request_ids),
                "versions": list(ledger.versions),
            }

    def clear(self) -> None:
        with self._lock:
            self._ledgers.clear()

    def clone_empty(self) -> ExplanationPersistenceService:
        """Fresh store for isolated replay runs."""
        return ExplanationPersistenceService()

    def deep_copy(self) -> ExplanationPersistenceService:
        """Copy store state (tests / diagnostics)."""
        clone = ExplanationPersistenceService()
        with self._lock:
            clone._ledgers = deepcopy(self._ledgers)
        return clone
