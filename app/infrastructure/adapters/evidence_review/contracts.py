"""Educational Evidence Review Workspace contracts (P4-MS003).

Immutable DTOs for read-only human inspection of longitudinal educational
evidence. Review artefacts never modify Runtime A, recommendations, policy,
or Adaptive / Recovery behaviour.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from types import MappingProxyType
from typing import Any

from app.infrastructure.adapters.longitudinal_evidence.contracts import (
    LearningEvidenceRecord,
)

UNAVAILABLE = "UNAVAILABLE"
INVALID_STATE = "INVALID_STATE"

EVIDENCE_REVIEW_ERROR_CODES = frozenset({UNAVAILABLE, INVALID_STATE})

AUTHORITY_EVIDENCE_REVIEW = "evidence_review"
AUTHORITY_LONGITUDINAL_EVIDENCE = "longitudinal_evidence"
AUTHORITY_RUNTIME_A = "runtime_a"

EVIDENCE_REVIEW_SCHEMA_VERSION = "p4.ms003.1"

EXPORT_FORMAT_JSON = "json"
EXPORT_FORMAT_CSV = "csv"
EXPORT_FORMATS = frozenset({EXPORT_FORMAT_JSON, EXPORT_FORMAT_CSV})

# CSV column order is fixed for reproducible review exports.
CSV_COLUMNS = (
    "record_id",
    "student_id_hash",
    "event_type",
    "event_timestamp",
    "source_component",
    "policy_version",
    "advisory_field",
    "trial_id",
    "schema_version",
    "authority",
    "operational_only",
    "provenance_originating_component",
    "provenance_policy_version",
    "provenance_collected_at",
    "provenance_feature_flags",
    "provenance_trial_context",
    "provenance_advisory_provenance",
    "provenance_notes",
)


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
        f"Unsupported evidence review contract value type: {type(value)!r}"
    )


def serialize_canonical(value: Any) -> str:
    """Deterministic JSON serialization (sorted keys, compact separators)."""
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class EvidenceReviewFilter:
    """Immutable filter for read-only evidence inspection.

    Empty string fields are treated as unset (no constraint). Feature-flag
    filtering matches a named flag inside each record's provenance snapshot.
    """

    start_timestamp: str = ""
    end_timestamp: str = ""
    event_type: str = ""
    policy_version: str = ""
    trial_id: str = ""
    advisory_field: str = ""
    feature_flag: str = ""
    feature_flag_value: Any = True

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "start_timestamp", (self.start_timestamp or "").strip()
        )
        object.__setattr__(
            self, "end_timestamp", (self.end_timestamp or "").strip()
        )
        object.__setattr__(self, "event_type", (self.event_type or "").strip())
        object.__setattr__(
            self, "policy_version", (self.policy_version or "").strip()
        )
        object.__setattr__(self, "trial_id", (self.trial_id or "").strip())
        object.__setattr__(
            self, "advisory_field", (self.advisory_field or "").strip()
        )
        object.__setattr__(
            self, "feature_flag", (self.feature_flag or "").strip()
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_field": self.advisory_field,
            "end_timestamp": self.end_timestamp,
            "event_type": self.event_type,
            "feature_flag": self.feature_flag,
            "feature_flag_value": self.feature_flag_value,
            "policy_version": self.policy_version,
            "start_timestamp": self.start_timestamp,
            "trial_id": self.trial_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EvidenceTimeWindow:
    """Inclusive time window covered by a timeline view."""

    start_timestamp: str = ""
    end_timestamp: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "start_timestamp", (self.start_timestamp or "").strip()
        )
        object.__setattr__(
            self, "end_timestamp", (self.end_timestamp or "").strip()
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "end_timestamp": self.end_timestamp,
            "start_timestamp": self.start_timestamp,
        }


@dataclass(frozen=True)
class EvidenceEventGroup:
    """Immutable group of observations sharing an event type."""

    event_type: str = ""
    observation_count: int = 0
    record_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "event_type", (self.event_type or "").strip())
        object.__setattr__(
            self, "observation_count", int(self.observation_count or 0)
        )
        object.__setattr__(
            self,
            "record_ids",
            tuple(str(item) for item in (self.record_ids or ())),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "observation_count": self.observation_count,
            "record_ids": list(self.record_ids),
        }


@dataclass(frozen=True)
class EvidenceProvenanceSummary:
    """Aggregated provenance facts for a timeline (no interpretation)."""

    originating_components: tuple[str, ...] = ()
    policy_versions: tuple[str, ...] = ()
    trial_ids: tuple[str, ...] = ()
    advisory_fields: tuple[str, ...] = ()
    feature_flags_observed: Mapping[str, Any] = field(default_factory=dict)
    schema_versions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "originating_components",
            tuple(str(item) for item in (self.originating_components or ())),
        )
        object.__setattr__(
            self,
            "policy_versions",
            tuple(str(item) for item in (self.policy_versions or ())),
        )
        object.__setattr__(
            self,
            "trial_ids",
            tuple(str(item) for item in (self.trial_ids or ())),
        )
        object.__setattr__(
            self,
            "advisory_fields",
            tuple(str(item) for item in (self.advisory_fields or ())),
        )
        object.__setattr__(
            self,
            "feature_flags_observed",
            _freeze_mapping(self.feature_flags_observed),
        )
        object.__setattr__(
            self,
            "schema_versions",
            tuple(str(item) for item in (self.schema_versions or ())),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_fields": list(self.advisory_fields),
            "feature_flags_observed": dict(self.feature_flags_observed),
            "originating_components": list(self.originating_components),
            "policy_versions": list(self.policy_versions),
            "schema_versions": list(self.schema_versions),
            "trial_ids": list(self.trial_ids),
        }


@dataclass(frozen=True)
class EvidenceTimeline:
    """Immutable timeline view over longitudinal observations."""

    timeline_id: str = ""
    observation_count: int = 0
    time_window: EvidenceTimeWindow | Mapping[str, Any] = field(
        default_factory=EvidenceTimeWindow
    )
    event_groups: tuple[EvidenceEventGroup, ...] = ()
    provenance_summary: EvidenceProvenanceSummary | Mapping[str, Any] = field(
        default_factory=EvidenceProvenanceSummary
    )
    record_ids: tuple[str, ...] = ()
    filter_snapshot: Mapping[str, Any] = field(default_factory=dict)
    schema_version: str = EVIDENCE_REVIEW_SCHEMA_VERSION
    authority: str = AUTHORITY_EVIDENCE_REVIEW
    read_only: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "timeline_id", (self.timeline_id or "").strip())
        object.__setattr__(
            self, "observation_count", int(self.observation_count or 0)
        )
        object.__setattr__(self, "time_window", _coerce_time_window(self.time_window))
        object.__setattr__(
            self, "event_groups", _coerce_event_groups(self.event_groups)
        )
        object.__setattr__(
            self,
            "provenance_summary",
            _coerce_provenance_summary(self.provenance_summary),
        )
        object.__setattr__(
            self,
            "record_ids",
            tuple(str(item) for item in (self.record_ids or ())),
        )
        object.__setattr__(
            self, "filter_snapshot", _freeze_mapping(self.filter_snapshot)
        )
        object.__setattr__(
            self,
            "schema_version",
            (self.schema_version or EVIDENCE_REVIEW_SCHEMA_VERSION).strip(),
        )
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_EVIDENCE_REVIEW).strip(),
        )
        object.__setattr__(self, "read_only", True)

    def to_canonical_dict(self) -> dict[str, Any]:
        window = self.time_window
        if isinstance(window, EvidenceTimeWindow):
            window_payload = window.to_canonical_dict()
        else:
            window_payload = dict(window)
        summary = self.provenance_summary
        if isinstance(summary, EvidenceProvenanceSummary):
            summary_payload = summary.to_canonical_dict()
        else:
            summary_payload = dict(summary)
        return {
            "authority": self.authority,
            "event_groups": [
                item.to_canonical_dict()
                if isinstance(item, EvidenceEventGroup)
                else dict(item)
                for item in self.event_groups
            ],
            "filter_snapshot": dict(self.filter_snapshot),
            "observation_count": self.observation_count,
            "provenance_summary": summary_payload,
            "read_only": self.read_only,
            "record_ids": list(self.record_ids),
            "schema_version": self.schema_version,
            "time_window": window_payload,
            "timeline_id": self.timeline_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EvidenceReviewExport:
    """Immutable export artefact suitable for offline review."""

    export_id: str = ""
    format: str = EXPORT_FORMAT_JSON
    content: str = ""
    record_count: int = 0
    filter_snapshot: Mapping[str, Any] = field(default_factory=dict)
    content_digest: str = ""
    schema_version: str = EVIDENCE_REVIEW_SCHEMA_VERSION
    authority: str = AUTHORITY_EVIDENCE_REVIEW
    read_only: bool = True
    reproducible: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "export_id", (self.export_id or "").strip())
        fmt = (self.format or EXPORT_FORMAT_JSON).strip().lower()
        if fmt not in EXPORT_FORMATS:
            fmt = EXPORT_FORMAT_JSON
        object.__setattr__(self, "format", fmt)
        object.__setattr__(self, "content", self.content if self.content else "")
        object.__setattr__(self, "record_count", int(self.record_count or 0))
        object.__setattr__(
            self, "filter_snapshot", _freeze_mapping(self.filter_snapshot)
        )
        object.__setattr__(
            self, "content_digest", (self.content_digest or "").strip()
        )
        object.__setattr__(
            self,
            "schema_version",
            (self.schema_version or EVIDENCE_REVIEW_SCHEMA_VERSION).strip(),
        )
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_EVIDENCE_REVIEW).strip(),
        )
        object.__setattr__(self, "read_only", True)
        object.__setattr__(self, "reproducible", True)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "content": self.content,
            "content_digest": self.content_digest,
            "export_id": self.export_id,
            "filter_snapshot": dict(self.filter_snapshot),
            "format": self.format,
            "read_only": self.read_only,
            "record_count": self.record_count,
            "reproducible": self.reproducible,
            "schema_version": self.schema_version,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EvidenceReviewResult:
    """Result envelope for Evidence Query Service calls."""

    ok: bool
    records: tuple[LearningEvidenceRecord, ...] = ()
    timeline: EvidenceTimeline | None = None
    export: EvidenceReviewExport | None = None
    filter_snapshot: Mapping[str, Any] = field(default_factory=dict)
    error_code: str | None = None
    message: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "records",
            tuple(self.records or ()),
        )
        object.__setattr__(
            self, "filter_snapshot", _freeze_mapping(self.filter_snapshot)
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "export": (
                None if self.export is None else self.export.to_canonical_dict()
            ),
            "filter_snapshot": dict(self.filter_snapshot),
            "message": self.message,
            "ok": self.ok,
            "records": [
                item.to_canonical_dict()
                if hasattr(item, "to_canonical_dict")
                else dict(item)
                for item in self.records
            ],
            "timeline": (
                None
                if self.timeline is None
                else self.timeline.to_canonical_dict()
            ),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


def _coerce_time_window(
    value: EvidenceTimeWindow | Mapping[str, Any] | None,
) -> EvidenceTimeWindow:
    if value is None:
        return EvidenceTimeWindow()
    if isinstance(value, EvidenceTimeWindow):
        return value
    if isinstance(value, Mapping):
        return EvidenceTimeWindow(
            start_timestamp=str(value.get("start_timestamp", "") or ""),
            end_timestamp=str(value.get("end_timestamp", "") or ""),
        )
    raise TypeError("time_window must be EvidenceTimeWindow, Mapping, or None")


def _coerce_event_groups(
    value: Sequence[EvidenceEventGroup | Mapping[str, Any]] | None,
) -> tuple[EvidenceEventGroup, ...]:
    if not value:
        return ()
    groups: list[EvidenceEventGroup] = []
    for item in value:
        if isinstance(item, EvidenceEventGroup):
            groups.append(item)
        elif isinstance(item, Mapping):
            groups.append(
                EvidenceEventGroup(
                    event_type=str(item.get("event_type", "") or ""),
                    observation_count=int(item.get("observation_count", 0) or 0),
                    record_ids=tuple(item.get("record_ids") or ()),
                )
            )
        else:
            raise TypeError(
                "event_groups must contain EvidenceEventGroup or Mapping values"
            )
    return tuple(groups)


def _coerce_provenance_summary(
    value: EvidenceProvenanceSummary | Mapping[str, Any] | None,
) -> EvidenceProvenanceSummary:
    if value is None:
        return EvidenceProvenanceSummary()
    if isinstance(value, EvidenceProvenanceSummary):
        return value
    if isinstance(value, Mapping):
        return EvidenceProvenanceSummary(
            originating_components=tuple(
                value.get("originating_components") or ()
            ),
            policy_versions=tuple(value.get("policy_versions") or ()),
            trial_ids=tuple(value.get("trial_ids") or ()),
            advisory_fields=tuple(value.get("advisory_fields") or ()),
            feature_flags_observed=value.get("feature_flags_observed") or {},
            schema_versions=tuple(value.get("schema_versions") or ()),
        )
    raise TypeError(
        "provenance_summary must be EvidenceProvenanceSummary, Mapping, or None"
    )


__all__ = [
    "AUTHORITY_EVIDENCE_REVIEW",
    "AUTHORITY_LONGITUDINAL_EVIDENCE",
    "AUTHORITY_RUNTIME_A",
    "CSV_COLUMNS",
    "EVIDENCE_REVIEW_ERROR_CODES",
    "EVIDENCE_REVIEW_SCHEMA_VERSION",
    "EXPORT_FORMAT_CSV",
    "EXPORT_FORMAT_JSON",
    "EXPORT_FORMATS",
    "INVALID_STATE",
    "UNAVAILABLE",
    "EvidenceEventGroup",
    "EvidenceProvenanceSummary",
    "EvidenceReviewExport",
    "EvidenceReviewFilter",
    "EvidenceReviewResult",
    "EvidenceTimeWindow",
    "EvidenceTimeline",
    "serialize_canonical",
]
