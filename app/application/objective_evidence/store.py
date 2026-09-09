"""Append-only Objective Assessment Evidence store (OEA Phase 2).

Process-local persistence for Phase 2. Exists to be written and queried in
tests only. Zero production downstream readers in this wave.
"""

from __future__ import annotations

import threading
from datetime import UTC, datetime
from uuid import uuid4

from app.application.objective_evidence.records import AssessmentEvidenceRecord

_STORE_LOCK = threading.RLock()
_DEFAULT_STORE: ObjectiveAssessmentEvidenceStore | None = None


class ObjectiveAssessmentEvidenceStore:
    """Append-only in-memory Assessment Evidence store."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._records: dict[str, AssessmentEvidenceRecord] = {}
        self._order: list[str] = []

    def append(self, record: AssessmentEvidenceRecord) -> AssessmentEvidenceRecord:
        """Append an immutable evidence record. Duplicate ids raise ValueError."""
        eid = (record.evidence_id or "").strip()
        if not eid:
            raise ValueError("evidence_id required")
        with self._lock:
            if eid in self._records:
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
            self._records[eid] = stored
            self._order.append(eid)
            return stored

    def get(self, evidence_id: str) -> AssessmentEvidenceRecord | None:
        """Load one evidence record by id."""
        return self._records.get((evidence_id or "").strip())

    def list_all(self) -> tuple[AssessmentEvidenceRecord, ...]:
        """All records in append order."""
        with self._lock:
            return tuple(self._records[i] for i in self._order if i in self._records)

    def list_for_student(
        self, student_id: str
    ) -> tuple[AssessmentEvidenceRecord, ...]:
        """Records for one student in append order."""
        sid = (student_id or "").strip()
        return tuple(r for r in self.list_all() if r.student_id == sid)

    def list_for_objective(
        self, objective_id: str
    ) -> tuple[AssessmentEvidenceRecord, ...]:
        """Records for one objective in append order."""
        oid = (objective_id or "").strip()
        return tuple(r for r in self.list_all() if r.objective_id == oid)

    def count(self) -> int:
        """Total evidence records."""
        return len(self._records)

    def clear(self) -> None:
        """Drop all records (tests only)."""
        with self._lock:
            self._records.clear()
            self._order.clear()


def get_objective_assessment_evidence_store() -> ObjectiveAssessmentEvidenceStore:
    """Process-default Assessment Evidence store (tests / Phase 2 write path)."""
    global _DEFAULT_STORE
    with _STORE_LOCK:
        if _DEFAULT_STORE is None:
            _DEFAULT_STORE = ObjectiveAssessmentEvidenceStore()
        return _DEFAULT_STORE


def reset_objective_assessment_evidence_store() -> None:
    """Replace the process-default store (tests)."""
    global _DEFAULT_STORE
    with _STORE_LOCK:
        _DEFAULT_STORE = ObjectiveAssessmentEvidenceStore()


def new_evidence_id() -> str:
    """Allocate a unique evidence id."""
    return f"oae-{uuid4().hex}"


def utc_now() -> datetime:
    """Timezone-aware UTC timestamp for evidence rows."""
    return datetime.now(tz=UTC)
