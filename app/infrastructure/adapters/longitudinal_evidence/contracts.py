"""Longitudinal Learning Evidence Repository contracts (P4-MS002).

Immutable DTOs for durable storage of educational observations collected
across study sessions, missions, reflections, advisory activations, and
educational trials.

This repository stores **evidence only**. It must not influence Runtime A
during P4-MS002. No analytical behaviour. No recommendation changes.
No Adaptive / Recovery / policy weighting mutation.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable

UNAVAILABLE = "UNAVAILABLE"
INVALID_STATE = "INVALID_STATE"
APPEND_ONLY_VIOLATION = "APPEND_ONLY_VIOLATION"
SCHEMA_INCOMPATIBLE = "SCHEMA_INCOMPATIBLE"

LONGITUDINAL_ERROR_CODES = frozenset(
    {
        UNAVAILABLE,
        INVALID_STATE,
        APPEND_ONLY_VIOLATION,
        SCHEMA_INCOMPATIBLE,
    }
)

AUTHORITY_LONGITUDINAL_EVIDENCE = "longitudinal_evidence"
AUTHORITY_RUNTIME_A = "runtime_a"

LONGITUDINAL_EVIDENCE_SCHEMA_VERSION = "p4.ms002.1"
SUPPORTED_SCHEMA_VERSIONS = frozenset({LONGITUDINAL_EVIDENCE_SCHEMA_VERSION})

# Observation event types (operational educational observations only).
EVENT_STUDY_SESSION = "study_session"
EVENT_MISSION = "mission"
EVENT_REFLECTION = "reflection"
EVENT_ADVISORY_ACTIVATION = "advisory_activation"
EVENT_EDUCATIONAL_TRIAL = "educational_trial"

LONGITUDINAL_EVENT_TYPES = frozenset(
    {
        EVENT_STUDY_SESSION,
        EVENT_MISSION,
        EVENT_REFLECTION,
        EVENT_ADVISORY_ACTIVATION,
        EVENT_EDUCATIONAL_TRIAL,
    }
)

# Originating components that may publish observations.
SOURCE_UNIFIED_JOURNEY = "unified_journey"
SOURCE_STUDENT_EXPERIENCE = "student_experience"
SOURCE_CONTROLLED_ADVISORY = "controlled_advisory"
SOURCE_ADVISORY_OUTCOME = "advisory_outcome_measurement"
SOURCE_EDUCATIONAL_TRIAL = "educational_trial"
SOURCE_EVIDENCE_PLATFORM = "evidence_platform"
SOURCE_RECOMMENDATION_POLICY = "recommendation_policy"
SOURCE_RUNTIME_A = "runtime_a"

LONGITUDINAL_SOURCE_COMPONENTS = frozenset(
    {
        SOURCE_UNIFIED_JOURNEY,
        SOURCE_STUDENT_EXPERIENCE,
        SOURCE_CONTROLLED_ADVISORY,
        SOURCE_ADVISORY_OUTCOME,
        SOURCE_EDUCATIONAL_TRIAL,
        SOURCE_EVIDENCE_PLATFORM,
        SOURCE_RECOMMENDATION_POLICY,
        SOURCE_RUNTIME_A,
    }
)

# Approved advisory field — locked to existing Programme III / IV surface.
APPROVED_ADVISORY_FIELD = "consistency_summary"
APPROVED_ADVISORY_FIELDS = frozenset({APPROVED_ADVISORY_FIELD, ""})


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if isinstance(value, MappingProxyType):
        return value
    frozen: dict[str, Any] = {}
    for key, item in dict(value).items():
        if isinstance(item, Mapping):
            frozen[str(key)] = dict(item)
        elif isinstance(item, list | tuple):
            frozen[str(key)] = list(item)
        else:
            frozen[str(key)] = item
    return MappingProxyType(frozen)


def _canonical(value: Any) -> Any:
    """Recursively convert values into JSON-stable plain data."""
    if value is None or isinstance(value, bool | int | float | str):
        return value
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {
            str(k): _canonical(v)
            for k, v in sorted(value.items(), key=lambda i: str(i[0]))
        }
    if isinstance(value, list | tuple):
        return [_canonical(item) for item in value]
    if hasattr(value, "to_canonical_dict"):
        return value.to_canonical_dict()
    raise TypeError(
        f"Unsupported longitudinal evidence contract value type: {type(value)!r}"
    )


def serialize_canonical(value: Any) -> str:
    """Deterministic JSON serialization (sorted keys, compact separators)."""
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


def snapshot_mapping(value: Any | None) -> Mapping[str, Any] | None:
    """Freeze a DTO or mapping into a canonical snapshot."""
    if value is None:
        return None
    if hasattr(value, "to_canonical_dict"):
        return _freeze_mapping(value.to_canonical_dict())
    if isinstance(value, Mapping):
        return _freeze_mapping(value)
    raise TypeError("value must be a Mapping, DTO with to_canonical_dict, or None")


def _normalise_timestamp(value: str | datetime | None) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value).strip()


@dataclass(frozen=True)
class LongitudinalEvidenceProvenance:
    """Immutable provenance block required on every stored record.

    Preserves originating component, policy version, feature flags,
    trial context, and advisory provenance for later educational review.
    """

    originating_component: str = ""
    policy_version: str = ""
    feature_flags: Mapping[str, Any] = field(default_factory=dict)
    trial_context: Mapping[str, Any] = field(default_factory=dict)
    advisory_provenance: Mapping[str, Any] = field(default_factory=dict)
    collected_at: str = ""
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "originating_component",
            (self.originating_component or "").strip(),
        )
        object.__setattr__(
            self, "policy_version", (self.policy_version or "").strip()
        )
        object.__setattr__(
            self, "feature_flags", _freeze_mapping(self.feature_flags)
        )
        object.__setattr__(
            self, "trial_context", _freeze_mapping(self.trial_context)
        )
        object.__setattr__(
            self, "advisory_provenance", _freeze_mapping(self.advisory_provenance)
        )
        object.__setattr__(
            self, "collected_at", _normalise_timestamp(self.collected_at)
        )
        object.__setattr__(
            self, "notes", tuple(str(item) for item in (self.notes or ()))
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_provenance": dict(self.advisory_provenance),
            "collected_at": self.collected_at,
            "feature_flags": dict(self.feature_flags),
            "notes": list(self.notes),
            "originating_component": self.originating_component,
            "policy_version": self.policy_version,
            "trial_context": dict(self.trial_context),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


def build_provenance(
    *,
    originating_component: str,
    policy_version: str = "",
    feature_flags: Mapping[str, Any] | None = None,
    trial_context: Mapping[str, Any] | None = None,
    advisory_provenance: Mapping[str, Any] | None = None,
    collected_at: str | datetime | None = None,
    notes: Sequence[str] | None = None,
) -> LongitudinalEvidenceProvenance:
    """Construct a complete provenance block for a longitudinal record."""
    return LongitudinalEvidenceProvenance(
        originating_component=originating_component,
        policy_version=policy_version,
        feature_flags=feature_flags or {},
        trial_context=trial_context or {},
        advisory_provenance=advisory_provenance or {},
        collected_at=_normalise_timestamp(collected_at),
        notes=tuple(notes or ()),
    )


def _coerce_provenance(
    value: LongitudinalEvidenceProvenance | Mapping[str, Any] | None,
) -> LongitudinalEvidenceProvenance:
    if value is None:
        return LongitudinalEvidenceProvenance()
    if isinstance(value, LongitudinalEvidenceProvenance):
        return value
    if isinstance(value, Mapping):
        return LongitudinalEvidenceProvenance(
            originating_component=str(value.get("originating_component", "") or ""),
            policy_version=str(value.get("policy_version", "") or ""),
            feature_flags=value.get("feature_flags") or {},
            trial_context=value.get("trial_context") or {},
            advisory_provenance=value.get("advisory_provenance") or {},
            collected_at=str(value.get("collected_at", "") or ""),
            notes=tuple(value.get("notes") or ()),
        )
    raise TypeError(
        "provenance must be LongitudinalEvidenceProvenance, Mapping, or None"
    )


@dataclass(frozen=True)
class LearningEvidenceRecord:
    """Immutable longitudinal learning evidence record (P4-MS002).

    Stores operational educational observations only. Uses
    ``student_id_hash`` — never raw personal identifiers.
    """

    record_id: str = ""
    student_id_hash: str = ""
    event_type: str = ""
    event_timestamp: str = ""
    source_component: str = ""
    policy_version: str = ""
    advisory_field: str = ""
    trial_id: str = ""
    provenance: LongitudinalEvidenceProvenance | Mapping[str, Any] = field(
        default_factory=LongitudinalEvidenceProvenance
    )
    schema_version: str = LONGITUDINAL_EVIDENCE_SCHEMA_VERSION
    authority: str = AUTHORITY_LONGITUDINAL_EVIDENCE
    operational_only: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "record_id", (self.record_id or "").strip())
        object.__setattr__(
            self, "student_id_hash", (self.student_id_hash or "").strip()
        )

        event_type = (self.event_type or "").strip()
        if event_type and event_type not in LONGITUDINAL_EVENT_TYPES:
            event_type = ""
        object.__setattr__(self, "event_type", event_type)

        object.__setattr__(
            self, "event_timestamp", _normalise_timestamp(self.event_timestamp)
        )

        source = (self.source_component or "").strip()
        if source and source not in LONGITUDINAL_SOURCE_COMPONENTS:
            # Preserve unknown source labels as-is for forward compatibility,
            # but prefer known catalogue values when callers send blanks.
            pass
        object.__setattr__(self, "source_component", source)

        object.__setattr__(
            self, "policy_version", (self.policy_version or "").strip()
        )

        advisory = (self.advisory_field or "").strip()
        if advisory and advisory not in APPROVED_ADVISORY_FIELDS:
            advisory = APPROVED_ADVISORY_FIELD
        object.__setattr__(self, "advisory_field", advisory)

        object.__setattr__(self, "trial_id", (self.trial_id or "").strip())
        object.__setattr__(self, "provenance", _coerce_provenance(self.provenance))

        schema = (self.schema_version or LONGITUDINAL_EVIDENCE_SCHEMA_VERSION).strip()
        object.__setattr__(self, "schema_version", schema)

        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_LONGITUDINAL_EVIDENCE).strip(),
        )
        object.__setattr__(self, "operational_only", True)

    def to_canonical_dict(self) -> dict[str, Any]:
        provenance = self.provenance
        if isinstance(provenance, LongitudinalEvidenceProvenance):
            provenance_payload = provenance.to_canonical_dict()
        else:
            provenance_payload = dict(provenance)
        return {
            "advisory_field": self.advisory_field,
            "authority": self.authority,
            "event_timestamp": self.event_timestamp,
            "event_type": self.event_type,
            "operational_only": self.operational_only,
            "policy_version": self.policy_version,
            "provenance": provenance_payload,
            "record_id": self.record_id,
            "schema_version": self.schema_version,
            "source_component": self.source_component,
            "student_id_hash": self.student_id_hash,
            "trial_id": self.trial_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class LongitudinalEvidenceResult:
    """Result envelope for LongitudinalEvidenceRepository calls."""

    ok: bool
    record: LearningEvidenceRecord | None = None
    records: tuple[LearningEvidenceRecord, ...] = ()
    error_code: str | None = None
    message: str | None = None

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "message": self.message,
            "ok": self.ok,
            "record": (
                None if self.record is None else self.record.to_canonical_dict()
            ),
            "records": [item.to_canonical_dict() for item in self.records],
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


def validate_learning_evidence_record(
    record: LearningEvidenceRecord,
) -> tuple[bool, str]:
    """Validate a record for append into the longitudinal repository."""
    if not isinstance(record, LearningEvidenceRecord):
        return False, "record_must_be_learning_evidence_record"
    if not record.record_id:
        return False, "record_id_required"
    if not record.student_id_hash:
        return False, "student_id_hash_required"
    if record.event_type not in LONGITUDINAL_EVENT_TYPES:
        return False, "event_type_invalid"
    if not record.event_timestamp:
        return False, "event_timestamp_required"
    if not record.source_component:
        return False, "source_component_required"
    if record.schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        return False, "schema_version_unsupported"
    provenance = record.provenance
    if not isinstance(provenance, LongitudinalEvidenceProvenance):
        return False, "provenance_required"
    if not provenance.originating_component:
        return False, "provenance_originating_component_required"
    return True, "ok"


def is_schema_compatible(schema_version: str) -> bool:
    """Return True when ``schema_version`` is readable by this milestone."""
    return (schema_version or "").strip() in SUPPORTED_SCHEMA_VERSIONS


@runtime_checkable
class LongitudinalEvidenceRepository(Protocol):
    """Append-only repository for longitudinal learning evidence.

    Retrieval only. No analytical aggregation or educational interpretation.
    """

    def is_enabled(self) -> bool:
        """Return True when the repository accepts append / query traffic."""
        ...

    def append(self, record: LearningEvidenceRecord) -> LongitudinalEvidenceResult:
        """Append an immutable evidence record (never update / delete)."""
        ...

    def get_by_record_id(self, record_id: str) -> LongitudinalEvidenceResult:
        """Retrieve a single record by id when present."""
        ...

    def get_by_time_window(
        self,
        *,
        start_timestamp: str,
        end_timestamp: str,
    ) -> LongitudinalEvidenceResult:
        """Retrieve records whose event_timestamp falls in ``[start, end]``."""
        ...

    def get_by_event_type(self, event_type: str) -> LongitudinalEvidenceResult:
        """Retrieve records matching ``event_type``."""
        ...

    def get_by_policy_version(
        self, policy_version: str
    ) -> LongitudinalEvidenceResult:
        """Retrieve records matching ``policy_version``."""
        ...

    def get_by_trial_id(self, trial_id: str) -> LongitudinalEvidenceResult:
        """Retrieve records matching ``trial_id``."""
        ...

    def get_by_advisory_field(
        self, advisory_field: str
    ) -> LongitudinalEvidenceResult:
        """Retrieve records matching ``advisory_field``."""
        ...

    def list_all(self) -> LongitudinalEvidenceResult:
        """Retrieve all stored records in append order (read-only)."""
        ...

    def count(self) -> int:
        """Return the number of stored records (ops / tests only)."""
        ...


__all__ = [
    "APPEND_ONLY_VIOLATION",
    "APPROVED_ADVISORY_FIELD",
    "APPROVED_ADVISORY_FIELDS",
    "AUTHORITY_LONGITUDINAL_EVIDENCE",
    "AUTHORITY_RUNTIME_A",
    "EVENT_ADVISORY_ACTIVATION",
    "EVENT_EDUCATIONAL_TRIAL",
    "EVENT_MISSION",
    "EVENT_REFLECTION",
    "EVENT_STUDY_SESSION",
    "INVALID_STATE",
    "LONGITUDINAL_ERROR_CODES",
    "LONGITUDINAL_EVENT_TYPES",
    "LONGITUDINAL_EVIDENCE_SCHEMA_VERSION",
    "LONGITUDINAL_SOURCE_COMPONENTS",
    "SCHEMA_INCOMPATIBLE",
    "SOURCE_ADVISORY_OUTCOME",
    "SOURCE_CONTROLLED_ADVISORY",
    "SOURCE_EDUCATIONAL_TRIAL",
    "SOURCE_EVIDENCE_PLATFORM",
    "SOURCE_RECOMMENDATION_POLICY",
    "SOURCE_RUNTIME_A",
    "SOURCE_STUDENT_EXPERIENCE",
    "SOURCE_UNIFIED_JOURNEY",
    "SUPPORTED_SCHEMA_VERSIONS",
    "UNAVAILABLE",
    "LearningEvidenceRecord",
    "LongitudinalEvidenceProvenance",
    "LongitudinalEvidenceRepository",
    "LongitudinalEvidenceResult",
    "build_provenance",
    "is_schema_compatible",
    "serialize_canonical",
    "snapshot_mapping",
    "validate_learning_evidence_record",
]
