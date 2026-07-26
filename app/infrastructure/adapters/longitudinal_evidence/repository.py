"""In-memory Longitudinal Learning Evidence Repository (P4-MS002).

Append-only persistence adapter. Process-local storage is acceptable for
this milestone; the ``LongitudinalEvidenceRepository`` Protocol remains the
stable interface for a future durable datastore.

Stores evidence only. Never influences Runtime A. No analytical behaviour.
"""

from __future__ import annotations

import hashlib
import logging
import threading
from typing import Any

from .contracts import (
    APPEND_ONLY_VIOLATION,
    AUTHORITY_LONGITUDINAL_EVIDENCE,
    INVALID_STATE,
    LONGITUDINAL_EVIDENCE_SCHEMA_VERSION,
    SCHEMA_INCOMPATIBLE,
    UNAVAILABLE,
    LearningEvidenceRecord,
    LongitudinalEvidenceProvenance,
    LongitudinalEvidenceResult,
    is_schema_compatible,
    serialize_canonical,
    validate_learning_evidence_record,
)

logger = logging.getLogger(__name__)

REPOSITORY_ID = "longitudinal_evidence_repository"
SOURCE_SERVICE = "longitudinal_evidence"
REPOSITORY_VERSION = LONGITUDINAL_EVIDENCE_SCHEMA_VERSION


def deterministic_record_id(
    *,
    student_id_hash: str = "",
    event_type: str = "",
    event_timestamp: str = "",
    source_component: str = "",
    policy_version: str = "",
    trial_id: str = "",
    advisory_field: str = "",
) -> str:
    """Deterministic record id from observation material (idempotent append key)."""
    material = {
        "advisory_field": (advisory_field or "").strip(),
        "event_timestamp": (event_timestamp or "").strip(),
        "event_type": (event_type or "").strip(),
        "policy_version": (policy_version or "").strip(),
        "source_component": (source_component or "").strip(),
        "student_id_hash": (student_id_hash or "").strip(),
        "trial_id": (trial_id or "").strip(),
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"lerec-{digest}"


def opaque_student_id_hash(student_id: str, *, salt: str = "kwalitec-p4-ms002") -> str:
    """Hash a student identifier for storage (never store raw ids)."""
    raw = (student_id or "").strip()
    if not raw:
        return ""
    digest = hashlib.sha256(f"{salt}:{raw}".encode()).hexdigest()[:24]
    return f"stuhash-{digest}"


class InMemoryLongitudinalEvidenceRepository:
    """Append-only in-memory longitudinal evidence store (P4-MS002).

    Thread-safe for process-local use. Does not update or delete records.
    Duplicate ``record_id`` appends are rejected as append-only violations.
    """

    def __init__(self, *, enabled: bool = True) -> None:
        self._enabled = bool(enabled)
        self._lock = threading.RLock()
        self._records: list[LearningEvidenceRecord] = []
        self._by_id: dict[str, LearningEvidenceRecord] = {}

    @property
    def repository_id(self) -> str:
        return REPOSITORY_ID

    @property
    def repository_version(self) -> str:
        return REPOSITORY_VERSION

    @property
    def authority(self) -> str:
        return AUTHORITY_LONGITUDINAL_EVIDENCE

    def is_enabled(self) -> bool:
        return self._enabled

    def append(self, record: LearningEvidenceRecord) -> LongitudinalEvidenceResult:
        """Append an immutable evidence record.

        Never updates an existing ``record_id``. Callers that need
        idempotent observation should reuse deterministic ids and treat
        duplicate-id rejection as a no-op success path when desired.
        """
        if not self._enabled:
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_LONGITUDINAL_EVIDENCE is OFF",
            )
        if not isinstance(record, LearningEvidenceRecord):
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=INVALID_STATE,
                message="record_must_be_learning_evidence_record",
            )
        ok, detail = validate_learning_evidence_record(record)
        if not ok:
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=INVALID_STATE,
                message=detail,
            )
        if not is_schema_compatible(record.schema_version):
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=SCHEMA_INCOMPATIBLE,
                message="schema_version_unsupported",
            )

        with self._lock:
            if record.record_id in self._by_id:
                return LongitudinalEvidenceResult(
                    ok=False,
                    record=self._by_id[record.record_id],
                    error_code=APPEND_ONLY_VIOLATION,
                    message="record_id_already_exists",
                )
            # Store a frozen snapshot so callers cannot mutate shared state.
            stored = LearningEvidenceRecord(**record.to_canonical_dict())
            self._records.append(stored)
            self._by_id[stored.record_id] = stored
            logger.debug(
                "longitudinal_evidence_appended record_id=%s event_type=%s",
                stored.record_id,
                stored.event_type,
            )
            return LongitudinalEvidenceResult(ok=True, record=stored)

    def get_by_record_id(self, record_id: str) -> LongitudinalEvidenceResult:
        if not self._enabled:
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_LONGITUDINAL_EVIDENCE is OFF",
            )
        key = (record_id or "").strip()
        with self._lock:
            found = self._by_id.get(key)
        if found is None:
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=INVALID_STATE,
                message="record_not_found",
            )
        return LongitudinalEvidenceResult(ok=True, record=found, records=(found,))

    def get_by_time_window(
        self,
        *,
        start_timestamp: str,
        end_timestamp: str,
    ) -> LongitudinalEvidenceResult:
        if not self._enabled:
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_LONGITUDINAL_EVIDENCE is OFF",
            )
        start = (start_timestamp or "").strip()
        end = (end_timestamp or "").strip()
        if not start or not end:
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=INVALID_STATE,
                message="time_window_requires_start_and_end",
            )
        if start > end:
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=INVALID_STATE,
                message="time_window_start_after_end",
            )
        with self._lock:
            matched = tuple(
                item
                for item in self._records
                if start <= item.event_timestamp <= end
            )
        return LongitudinalEvidenceResult(ok=True, records=matched)

    def get_by_event_type(self, event_type: str) -> LongitudinalEvidenceResult:
        if not self._enabled:
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_LONGITUDINAL_EVIDENCE is OFF",
            )
        label = (event_type or "").strip()
        with self._lock:
            matched = tuple(
                item for item in self._records if item.event_type == label
            )
        return LongitudinalEvidenceResult(ok=True, records=matched)

    def get_by_policy_version(
        self, policy_version: str
    ) -> LongitudinalEvidenceResult:
        if not self._enabled:
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_LONGITUDINAL_EVIDENCE is OFF",
            )
        version = (policy_version or "").strip()
        with self._lock:
            matched = tuple(
                item for item in self._records if item.policy_version == version
            )
        return LongitudinalEvidenceResult(ok=True, records=matched)

    def get_by_trial_id(self, trial_id: str) -> LongitudinalEvidenceResult:
        if not self._enabled:
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_LONGITUDINAL_EVIDENCE is OFF",
            )
        key = (trial_id or "").strip()
        with self._lock:
            matched = tuple(
                item for item in self._records if item.trial_id == key
            )
        return LongitudinalEvidenceResult(ok=True, records=matched)

    def get_by_advisory_field(
        self, advisory_field: str
    ) -> LongitudinalEvidenceResult:
        if not self._enabled:
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_LONGITUDINAL_EVIDENCE is OFF",
            )
        field = (advisory_field or "").strip()
        with self._lock:
            matched = tuple(
                item for item in self._records if item.advisory_field == field
            )
        return LongitudinalEvidenceResult(ok=True, records=matched)

    def list_all(self) -> LongitudinalEvidenceResult:
        if not self._enabled:
            return LongitudinalEvidenceResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_LONGITUDINAL_EVIDENCE is OFF",
            )
        with self._lock:
            return LongitudinalEvidenceResult(ok=True, records=tuple(self._records))

    def count(self) -> int:
        with self._lock:
            return len(self._records)

    def snapshot(self) -> tuple[LearningEvidenceRecord, ...]:
        """Return an ordered snapshot of all stored records (tests / ops)."""
        with self._lock:
            return tuple(self._records)


def build_longitudinal_evidence_repository(
    *,
    enabled: bool = False,
) -> InMemoryLongitudinalEvidenceRepository | None:
    """Construct the longitudinal evidence repository when the flag is ON.

    Returns ``None`` when disabled so composition does not expose a sink
    that could later be mistaken for Runtime A influence.
    """
    if not enabled:
        return None
    return InMemoryLongitudinalEvidenceRepository(enabled=True)


def make_record(
    *,
    student_id_hash: str,
    event_type: str,
    event_timestamp: str,
    source_component: str,
    policy_version: str = "",
    advisory_field: str = "",
    trial_id: str = "",
    provenance: LongitudinalEvidenceProvenance | dict[str, Any] | None = None,
    record_id: str | None = None,
    schema_version: str = LONGITUDINAL_EVIDENCE_SCHEMA_VERSION,
) -> LearningEvidenceRecord:
    """Helper to build a fully identified ``LearningEvidenceRecord``."""
    rid = (record_id or "").strip() or deterministic_record_id(
        student_id_hash=student_id_hash,
        event_type=event_type,
        event_timestamp=event_timestamp,
        source_component=source_component,
        policy_version=policy_version,
        trial_id=trial_id,
        advisory_field=advisory_field,
    )
    return LearningEvidenceRecord(
        record_id=rid,
        student_id_hash=student_id_hash,
        event_type=event_type,
        event_timestamp=event_timestamp,
        source_component=source_component,
        policy_version=policy_version,
        advisory_field=advisory_field,
        trial_id=trial_id,
        provenance=provenance or LongitudinalEvidenceProvenance(
            originating_component=source_component,
            policy_version=policy_version,
        ),
        schema_version=schema_version,
    )


__all__ = [
    "REPOSITORY_ID",
    "REPOSITORY_VERSION",
    "SOURCE_SERVICE",
    "InMemoryLongitudinalEvidenceRepository",
    "build_longitudinal_evidence_repository",
    "deterministic_record_id",
    "make_record",
    "opaque_student_id_hash",
]
