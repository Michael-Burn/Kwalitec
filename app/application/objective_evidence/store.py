"""Append-only Objective Assessment Evidence store (OEA Phase 2).

Backed by ``SessionDocumentStore`` via ``build_session_document_store``.
When ``KWALITEC_V2_DURABLE_STORE=1``, evidence survives process restart in
``v2_aggregate_documents``. When the flag is off, the store is process-local
RAM only. Zero production downstream readers in this wave beyond the write path.
"""

from __future__ import annotations

import threading
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.application.objective_evidence.records import AssessmentEvidenceRecord
from app.infrastructure.session.store import SessionDocumentStore

NS_OEA_ASSESSMENT_EVIDENCE = "oea.assessment_evidence"

_STORE_LOCK = threading.RLock()
_DEFAULT_STORE: ObjectiveAssessmentEvidenceStore | None = None
_DEFAULT_DURABLE: bool | None = None


def _parse_occurred_at(raw: Any) -> datetime:
    text = str(raw or "").strip()
    if not text:
        return datetime.now(tz=UTC)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    when = datetime.fromisoformat(text)
    if when.tzinfo is None:
        when = when.replace(tzinfo=UTC)
    return when


def _record_to_doc(record: AssessmentEvidenceRecord) -> dict[str, Any]:
    return {
        "evidence_id": record.evidence_id,
        "student_id": record.student_id,
        "objective_id": record.objective_id,
        "item_id": record.item_id,
        "package_id": record.package_id,
        "session_id": record.session_id,
        "response_type": record.response_type,
        "scored_correct": record.scored_correct,
        "occurred_at": record.occurred_at.isoformat(),
        "source": record.source,
        "selected_misconception_tag": record.selected_misconception_tag,
    }


def _doc_to_record(doc: dict[str, Any]) -> AssessmentEvidenceRecord:
    scored = doc.get("scored_correct")
    if scored is not None:
        scored = bool(scored)
    return AssessmentEvidenceRecord(
        evidence_id=str(doc.get("evidence_id") or "").strip(),
        student_id=str(doc.get("student_id") or "").strip(),
        objective_id=str(doc.get("objective_id") or "").strip(),
        item_id=str(doc.get("item_id") or "").strip(),
        package_id=str(doc.get("package_id") or "").strip(),
        session_id=str(doc.get("session_id") or "").strip(),
        response_type=str(doc.get("response_type") or "").strip(),
        scored_correct=scored,
        occurred_at=_parse_occurred_at(doc.get("occurred_at")),
        source=str(doc.get("source") or "").strip(),
        selected_misconception_tag=str(
            doc.get("selected_misconception_tag") or ""
        ).strip(),
    )


class ObjectiveAssessmentEvidenceStore:
    """Append-only Assessment Evidence store over SessionDocumentStore."""

    def __init__(self, *, store: SessionDocumentStore | None = None) -> None:
        # Default must share the composition store (durable when flagged).
        # A bare SessionDocumentStore() here is a separate empty memory map and
        # silently diverges from session write paths even when
        # KWALITEC_V2_DURABLE_STORE=1.
        if store is not None:
            self._store = store
        else:
            from app.infrastructure.composition import build_session_document_store

            self._store = build_session_document_store()
        self._lock = threading.RLock()

    @property
    def document_store(self) -> SessionDocumentStore:
        return self._store

    def append(self, record: AssessmentEvidenceRecord) -> AssessmentEvidenceRecord:
        """Append an immutable evidence record. Duplicate ids raise ValueError."""
        eid = (record.evidence_id or "").strip()
        if not eid:
            raise ValueError("evidence_id required")
        with self._lock:
            if self._store.get(NS_OEA_ASSESSMENT_EVIDENCE, eid) is not None:
                raise ValueError(f"duplicate evidence_id: {eid}")
            stored = AssessmentEvidenceRecord(
                evidence_id=eid,
                student_id=str(record.student_id or "").strip(),
                objective_id=str(record.objective_id or "").strip(),
                item_id=str(record.item_id or "").strip(),
                package_id=str(record.package_id or "").strip(),
                session_id=str(record.session_id or "").strip(),
                response_type=str(record.response_type or "").strip(),
                scored_correct=record.scored_correct,
                occurred_at=record.occurred_at,
                source=str(record.source or "").strip(),
                selected_misconception_tag=str(
                    record.selected_misconception_tag or ""
                ).strip(),
            )
            self._store.save(
                NS_OEA_ASSESSMENT_EVIDENCE, eid, _record_to_doc(stored)
            )
            return stored

    def get(self, evidence_id: str) -> AssessmentEvidenceRecord | None:
        """Load one evidence record by id."""
        doc = self._store.get(NS_OEA_ASSESSMENT_EVIDENCE, (evidence_id or "").strip())
        if doc is None:
            return None
        return _doc_to_record(doc)

    def list_all(self) -> tuple[AssessmentEvidenceRecord, ...]:
        """All records ordered by occurred_at then evidence_id."""
        with self._lock:
            records = [
                _doc_to_record(doc)
                for doc in self._store.list_documents(NS_OEA_ASSESSMENT_EVIDENCE)
                if isinstance(doc, dict)
            ]
        records.sort(key=lambda r: (r.occurred_at, r.evidence_id))
        return tuple(records)

    def list_for_student(
        self, student_id: str
    ) -> tuple[AssessmentEvidenceRecord, ...]:
        """Records for one student in occurred_at order."""
        sid = (student_id or "").strip()
        return tuple(r for r in self.list_all() if r.student_id == sid)

    def list_for_objective(
        self, objective_id: str
    ) -> tuple[AssessmentEvidenceRecord, ...]:
        """Records for one objective in occurred_at order."""
        oid = (objective_id or "").strip()
        return tuple(r for r in self.list_all() if r.objective_id == oid)

    def count(self) -> int:
        """Total evidence records."""
        return len(self.list_all())

    def clear(self) -> None:
        """Drop only OEA-namespace documents (tests / isolation)."""
        with self._lock:
            for doc in list(self._store.list_documents(NS_OEA_ASSESSMENT_EVIDENCE)):
                if not isinstance(doc, dict):
                    continue
                eid = str(doc.get("evidence_id") or "").strip()
                if not eid:
                    continue
                self._store.delete(NS_OEA_ASSESSMENT_EVIDENCE, eid)


def get_objective_assessment_evidence_store() -> ObjectiveAssessmentEvidenceStore:
    """Process-default Assessment Evidence store (write path / tests).

    Rebuilds when ``KWALITEC_V2_DURABLE_STORE`` flips so tests can opt in
    without inheriting an import-time in-memory store.
    """
    global _DEFAULT_STORE, _DEFAULT_DURABLE
    from app.application.config.v2_flags import resolve_v2_feature_flags
    from app.infrastructure.composition import build_objective_assessment_evidence_store

    durable = resolve_v2_feature_flags().ENABLE_DURABLE_STORE
    with _STORE_LOCK:
        if _DEFAULT_STORE is None or _DEFAULT_DURABLE != durable:
            _DEFAULT_DURABLE = durable
            _DEFAULT_STORE = build_objective_assessment_evidence_store()
        return _DEFAULT_STORE


def discard_objective_assessment_evidence_store_for_tests() -> None:
    """Drop the process singleton without clearing backing data.

    Used to simulate a process restart while durable SQL rows remain.
    """
    global _DEFAULT_STORE, _DEFAULT_DURABLE
    with _STORE_LOCK:
        _DEFAULT_STORE = None
        _DEFAULT_DURABLE = None


def reset_objective_assessment_evidence_store() -> None:
    """Clear OEA docs (in-memory only) and drop the process singleton (tests).

    Durable SQL mode only drops the singleton: table truncation in the ``db``
    fixture owns SQL isolation.
    """
    global _DEFAULT_STORE, _DEFAULT_DURABLE
    with _STORE_LOCK:
        if _DEFAULT_STORE is not None and _DEFAULT_DURABLE is not True:
            _DEFAULT_STORE.clear()
        _DEFAULT_STORE = None
        _DEFAULT_DURABLE = None


def new_evidence_id() -> str:
    """Allocate a unique evidence id."""
    return f"oae-{uuid4().hex}"


def utc_now() -> datetime:
    """Timezone-aware UTC timestamp for evidence rows."""
    return datetime.now(tz=UTC)
