"""Student Digital Twin contracts (MS-004 T0–T3 / T5).

Immutable DTOs and Protocol interfaces. T0 defines Twin profile / facet /
snapshot contracts and the TwinAdapter surface. T2 adds snapshot version /
provenance / completeness DTOs. T3 adds FacetExplanation /
SnapshotExplanation explainability DTOs. T5 adds Experience-facing
StudentTwinProjection DTOs. No persistence, Adaptive authority changes,
Experience UX authority cutover, or educational writes.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date, datetime
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable

# Shared failure codes (DIGITAL_TWIN_INTERFACE_SPECIFICATION.md).
UNAVAILABLE = "UNAVAILABLE"
NO_ACTIVE_PLAN = "NO_ACTIVE_PLAN"
NOT_FOUND = "NOT_FOUND"
FORBIDDEN = "FORBIDDEN"
INVALID_STATE = "INVALID_STATE"
STALE_SNAPSHOT = "STALE_SNAPSHOT"
TWIN_EXPLAINABILITY_INCOMPLETE = "TWIN_EXPLAINABILITY_INCOMPLETE"
BEHAVIOUR_MISMATCH = "BEHAVIOUR_MISMATCH"

TWIN_ERROR_CODES = frozenset(
    {
        UNAVAILABLE,
        NO_ACTIVE_PLAN,
        NOT_FOUND,
        FORBIDDEN,
        INVALID_STATE,
        STALE_SNAPSHOT,
        TWIN_EXPLAINABILITY_INCOMPLETE,
        BEHAVIOUR_MISMATCH,
    }
)

AUTHORITY_DIGITAL_TWIN = "digital_twin_synthesis"
AUTHORITY_RUNTIME_A = "runtime_a"

FACET_LEARNING_RHYTHM = "learning_rhythm"
FACET_CONSISTENCY = "consistency"
FACET_PERSISTENCE = "persistence"
FACET_REVISION_BEHAVIOUR = "revision_behaviour"
FACET_CONFIDENCE_TREND = "confidence_trend"
FACET_SESSION_HABITS = "session_habits"
FACET_COGNITIVE_LOAD = "cognitive_load_indicators"

TWIN_FACET_NAMES = frozenset(
    {
        FACET_LEARNING_RHYTHM,
        FACET_CONSISTENCY,
        FACET_PERSISTENCE,
        FACET_REVISION_BEHAVIOUR,
        FACET_CONFIDENCE_TREND,
        FACET_SESSION_HABITS,
        FACET_COGNITIVE_LOAD,
    }
)

AVAILABILITY_AVAILABLE = "available"
AVAILABILITY_UNAVAILABLE = "unavailable"
PROVENANCE_KINDS = frozenset({"fact", "runtime_a_derived", "twin_derived", ""})

COMPLETENESS_COMPLETE = "complete"
COMPLETENESS_PARTIAL = "partial"
COMPLETENESS_EMPTY = "empty"
COMPLETENESS_STATUSES = frozenset(
    {COMPLETENESS_COMPLETE, COMPLETENESS_PARTIAL, COMPLETENESS_EMPTY, ""}
)


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if isinstance(value, MappingProxyType):
        return value
    return MappingProxyType(dict(value))


def _freeze_str_tuple(value: list[str] | tuple[str, ...] | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(str(item) for item in value)


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
    raise TypeError(f"Unsupported twin contract value type: {type(value)!r}")


def serialize_canonical(value: Any) -> str:
    """Deterministic JSON serialization (sorted keys, compact separators)."""
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class TwinProvenance:
    """Provenance for a Twin snapshot or facet claim (placeholder-safe)."""

    source_service: str = ""
    source_entity: str = ""
    collected_at: str | None = None
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = ""
    kind: str = ""

    def __post_init__(self) -> None:
        availability = (self.availability or "").strip().lower()
        if availability not in {AVAILABILITY_AVAILABLE, AVAILABILITY_UNAVAILABLE, ""}:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        kind = (self.kind or "").strip().lower()
        if kind not in PROVENANCE_KINDS:
            allowed = sorted(k for k in PROVENANCE_KINDS if k)
            raise ValueError(f"provenance kind must be one of {allowed} or empty")
        object.__setattr__(self, "availability", availability)
        object.__setattr__(self, "kind", kind)
        if self.collected_at is not None and not isinstance(self.collected_at, str):
            raise TypeError("collected_at must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "availability": self.availability,
            "collected_at": self.collected_at,
            "kind": self.kind,
            "source_entity": self.source_entity,
            "source_service": self.source_service,
            "unavailable_reason": self.unavailable_reason,
        }


@dataclass(frozen=True)
class TwinCompleteness:
    """Snapshot completeness contract (structural only — no value estimation)."""

    score: float | None = None
    facets_present: tuple[str, ...] = ()
    facets_unavailable: tuple[str, ...] = ()
    summary: str = ""
    status: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "facets_present", _freeze_str_tuple(self.facets_present)
        )
        object.__setattr__(
            self,
            "facets_unavailable",
            _freeze_str_tuple(self.facets_unavailable),
        )
        status = (self.status or "").strip().lower()
        if status not in COMPLETENESS_STATUSES:
            raise ValueError(
                "completeness status must be 'complete', 'partial', "
                "'empty', or empty"
            )
        object.__setattr__(self, "status", status)
        if self.score is not None and not isinstance(self.score, int | float):
            raise TypeError("score must be a number or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "facets_present": list(self.facets_present),
            "facets_unavailable": list(self.facets_unavailable),
            "score": self.score,
            "status": self.status,
            "summary": self.summary,
        }


@dataclass(frozen=True)
class SnapshotVersion:
    """Immutable TwinSnapshot version triad (MS-004 T2).

    - snapshot_version: construction / builder rules version
    - schema_version: TwinSnapshot material schema version
    - evidence_version: Runtime A evidence fingerprint
    """

    snapshot_version: str = ""
    schema_version: str = ""
    evidence_version: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "evidence_version": self.evidence_version,
            "schema_version": self.schema_version,
            "snapshot_version": self.snapshot_version,
        }


@dataclass(frozen=True)
class SnapshotProvenanceSummary:
    """Aggregated provenance across all Twin facets (MS-004 T2)."""

    contributing_runtime_a_sources: tuple[str, ...] = ()
    evidence_window_start: str | None = None
    evidence_window_end: str | None = None
    unavailable_inputs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "contributing_runtime_a_sources",
            _freeze_str_tuple(self.contributing_runtime_a_sources),
        )
        object.__setattr__(
            self,
            "unavailable_inputs",
            _freeze_str_tuple(self.unavailable_inputs),
        )
        for label, value in (
            ("evidence_window_start", self.evidence_window_start),
            ("evidence_window_end", self.evidence_window_end),
        ):
            if value is not None and not isinstance(value, str):
                raise TypeError(f"{label} must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "contributing_runtime_a_sources": list(
                self.contributing_runtime_a_sources
            ),
            "evidence_window_end": self.evidence_window_end,
            "evidence_window_start": self.evidence_window_start,
            "unavailable_inputs": list(self.unavailable_inputs),
        }


@dataclass(frozen=True)
class UnavailableSummary:
    """Explicit unavailable facet / input summary (never estimated)."""

    facets: tuple[str, ...] = ()
    reasons: Mapping[str, Any] = field(default_factory=dict)
    summary: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "facets", _freeze_str_tuple(self.facets))
        object.__setattr__(self, "reasons", _freeze_mapping(self.reasons))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "facets": list(self.facets),
            "reasons": {
                str(k): str(v)
                for k, v in sorted(self.reasons.items(), key=lambda i: str(i[0]))
            },
            "summary": self.summary,
        }


# --- Twin facet DTOs (placeholders — no algorithms) -------------------------


@dataclass(frozen=True)
class LearningRhythmFacet:
    """Learning Rhythm facet — placeholder structural fields only."""

    label: str = ""
    typical_session_minutes: float | None = None
    cadence_note: str = ""
    evidence_refs: tuple[str, ...] = ()
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = "estimate_deferred"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "availability": self.availability,
            "cadence_note": self.cadence_note,
            "evidence_refs": list(self.evidence_refs),
            "label": self.label,
            "typical_session_minutes": self.typical_session_minutes,
            "unavailable_reason": self.unavailable_reason,
        }


@dataclass(frozen=True)
class ConsistencyFacet:
    """Consistency facet — placeholder structural fields only."""

    label: str = ""
    adherence_note: str = ""
    evidence_refs: tuple[str, ...] = ()
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = "estimate_deferred"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adherence_note": self.adherence_note,
            "availability": self.availability,
            "evidence_refs": list(self.evidence_refs),
            "label": self.label,
            "unavailable_reason": self.unavailable_reason,
        }


@dataclass(frozen=True)
class PersistenceFacet:
    """Persistence facet — placeholder structural fields only."""

    label: str = ""
    continuity_note: str = ""
    evidence_refs: tuple[str, ...] = ()
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = "estimate_deferred"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "availability": self.availability,
            "continuity_note": self.continuity_note,
            "evidence_refs": list(self.evidence_refs),
            "label": self.label,
            "unavailable_reason": self.unavailable_reason,
        }


@dataclass(frozen=True)
class RevisionBehaviourFacet:
    """Revision Behaviour facet — placeholder structural fields only."""

    label: str = ""
    revision_note: str = ""
    evidence_refs: tuple[str, ...] = ()
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = "estimate_deferred"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "availability": self.availability,
            "evidence_refs": list(self.evidence_refs),
            "label": self.label,
            "revision_note": self.revision_note,
            "unavailable_reason": self.unavailable_reason,
        }


@dataclass(frozen=True)
class ConfidenceTrendFacet:
    """Confidence Trend facet — placeholder structural fields only."""

    label: str = ""
    trend_note: str = ""
    evidence_refs: tuple[str, ...] = ()
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = "estimate_deferred"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "availability": self.availability,
            "evidence_refs": list(self.evidence_refs),
            "label": self.label,
            "trend_note": self.trend_note,
            "unavailable_reason": self.unavailable_reason,
        }


@dataclass(frozen=True)
class SessionHabitsFacet:
    """Session Habits facet — placeholder structural fields only."""

    label: str = ""
    habits_note: str = ""
    evidence_refs: tuple[str, ...] = ()
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = "estimate_deferred"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "availability": self.availability,
            "evidence_refs": list(self.evidence_refs),
            "habits_note": self.habits_note,
            "label": self.label,
            "unavailable_reason": self.unavailable_reason,
        }


@dataclass(frozen=True)
class CognitiveLoadIndicatorsFacet:
    """Cognitive Load Indicators facet — placeholder structural fields only."""

    label: str = ""
    load_note: str = ""
    evidence_refs: tuple[str, ...] = ()
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = "estimate_deferred"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "availability": self.availability,
            "evidence_refs": list(self.evidence_refs),
            "label": self.label,
            "load_note": self.load_note,
            "unavailable_reason": self.unavailable_reason,
        }


@dataclass(frozen=True)
class TwinProfile:
    """Immutable Twin profile aggregating behavioural facet placeholders.

    T0: all facet values may be empty / unavailable. No synthesis algorithms.
    """

    student_id: str = ""
    learning_rhythm: LearningRhythmFacet = field(
        default_factory=LearningRhythmFacet
    )
    consistency: ConsistencyFacet = field(default_factory=ConsistencyFacet)
    persistence: PersistenceFacet = field(default_factory=PersistenceFacet)
    revision_behaviour: RevisionBehaviourFacet = field(
        default_factory=RevisionBehaviourFacet
    )
    confidence_trend: ConfidenceTrendFacet = field(
        default_factory=ConfidenceTrendFacet
    )
    session_habits: SessionHabitsFacet = field(default_factory=SessionHabitsFacet)
    cognitive_load_indicators: CognitiveLoadIndicatorsFacet = field(
        default_factory=CognitiveLoadIndicatorsFacet
    )
    limitations_codes: tuple[str, ...] = ()
    limitations_summary: str = ""

    def __post_init__(self) -> None:
        sid = (self.student_id or "").strip()
        object.__setattr__(self, "student_id", sid)
        object.__setattr__(
            self, "limitations_codes", _freeze_str_tuple(self.limitations_codes)
        )
        if not isinstance(self.learning_rhythm, LearningRhythmFacet):
            raise TypeError("learning_rhythm must be a LearningRhythmFacet")
        if not isinstance(self.consistency, ConsistencyFacet):
            raise TypeError("consistency must be a ConsistencyFacet")
        if not isinstance(self.persistence, PersistenceFacet):
            raise TypeError("persistence must be a PersistenceFacet")
        if not isinstance(self.revision_behaviour, RevisionBehaviourFacet):
            raise TypeError("revision_behaviour must be a RevisionBehaviourFacet")
        if not isinstance(self.confidence_trend, ConfidenceTrendFacet):
            raise TypeError("confidence_trend must be a ConfidenceTrendFacet")
        if not isinstance(self.session_habits, SessionHabitsFacet):
            raise TypeError("session_habits must be a SessionHabitsFacet")
        if not isinstance(
            self.cognitive_load_indicators, CognitiveLoadIndicatorsFacet
        ):
            raise TypeError(
                "cognitive_load_indicators must be a CognitiveLoadIndicatorsFacet"
            )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "cognitive_load_indicators": (
                self.cognitive_load_indicators.to_canonical_dict()
            ),
            "confidence_trend": self.confidence_trend.to_canonical_dict(),
            "consistency": self.consistency.to_canonical_dict(),
            "learning_rhythm": self.learning_rhythm.to_canonical_dict(),
            "limitations_codes": list(self.limitations_codes),
            "limitations_summary": self.limitations_summary,
            "persistence": self.persistence.to_canonical_dict(),
            "revision_behaviour": self.revision_behaviour.to_canonical_dict(),
            "session_habits": self.session_habits.to_canonical_dict(),
            "student_id": self.student_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class TwinSnapshot:
    """Immutable Twin snapshot — no mutable state; updates yield a new snapshot.

    Required metadata (MS-004 T0 + T2):
    - profile_version
    - source_evidence_version (evidence version)
    - snapshot_version / schema_version (T2)
    - generated_at (decision clock; never auto wall-clock)
    - provenance (+ provenance_summary aggregation, T2)
    - completeness (+ structural status, T2)
    - unavailable_summary (T2)
    """

    profile: TwinProfile = field(default_factory=TwinProfile)
    profile_version: str = ""
    source_evidence_version: str = ""
    generated_at: str | None = None
    provenance: TwinProvenance = field(default_factory=TwinProvenance)
    completeness: TwinCompleteness = field(default_factory=TwinCompleteness)
    twin_id: str = ""
    authority: str = AUTHORITY_DIGITAL_TWIN
    field_provenance: Mapping[str, Any] = field(default_factory=dict)
    snapshot_version: str = ""
    schema_version: str = ""
    provenance_summary: SnapshotProvenanceSummary = field(
        default_factory=SnapshotProvenanceSummary
    )
    unavailable_summary: UnavailableSummary = field(
        default_factory=UnavailableSummary
    )

    def __post_init__(self) -> None:
        if not isinstance(self.profile, TwinProfile):
            raise TypeError("profile must be a TwinProfile")
        if not isinstance(self.provenance, TwinProvenance):
            raise TypeError("provenance must be a TwinProvenance")
        if not isinstance(self.completeness, TwinCompleteness):
            raise TypeError("completeness must be a TwinCompleteness")
        if not isinstance(self.provenance_summary, SnapshotProvenanceSummary):
            raise TypeError(
                "provenance_summary must be a SnapshotProvenanceSummary"
            )
        if not isinstance(self.unavailable_summary, UnavailableSummary):
            raise TypeError("unavailable_summary must be an UnavailableSummary")
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError(
                "generated_at must be an ISO string or None (no auto clock)"
            )
        object.__setattr__(
            self, "field_provenance", _freeze_mapping(self.field_provenance)
        )

    def version(self) -> SnapshotVersion:
        """Expose the snapshot / schema / evidence version triad."""
        return SnapshotVersion(
            snapshot_version=self.snapshot_version,
            schema_version=self.schema_version,
            evidence_version=self.source_evidence_version,
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "completeness": self.completeness.to_canonical_dict(),
            "field_provenance": {
                str(k): dict(v) if isinstance(v, Mapping) else v
                for k, v in sorted(self.field_provenance.items())
            },
            "generated_at": self.generated_at,
            "profile": self.profile.to_canonical_dict(),
            "profile_version": self.profile_version,
            "provenance": self.provenance.to_canonical_dict(),
            "provenance_summary": self.provenance_summary.to_canonical_dict(),
            "schema_version": self.schema_version,
            "snapshot_version": self.snapshot_version,
            "source_evidence_version": self.source_evidence_version,
            "twin_id": self.twin_id,
            "unavailable_summary": self.unavailable_summary.to_canonical_dict(),
        }

    def serialize(self) -> str:
        """Deterministic JSON serialization of material snapshot fields."""
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class TwinResult:
    """Result envelope for TwinAdapter calls."""

    ok: bool
    value: TwinSnapshot | None = None
    error_code: str | None = None
    message: str | None = None
    fallback_used: bool = False

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "fallback_used": self.fallback_used,
            "message": self.message,
            "ok": self.ok,
            "value": None if self.value is None else self.value.to_canonical_dict(),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


# --- Explainability DTOs (MS-004 T3) ----------------------------------------


@dataclass(frozen=True)
class FacetExplanation:
    """Deterministic explanation for one Twin facet (MS-004 T3).

    Exposes contributing Runtime A evidence, derivation summary, completeness
    reasoning, unavailable reasoning, and provenance references. No hidden
    calculations and no inferred evidence — fields are derived only from the
    immutable TwinSnapshot / facet / provenance already assembled.
    """

    facet_name: str = ""
    availability: str = AVAILABILITY_UNAVAILABLE
    contributing_runtime_a_evidence: tuple[str, ...] = ()
    derivation_summary: str = ""
    completeness_reasoning: str = ""
    unavailable_reasoning: str = ""
    provenance_refs: tuple[str, ...] = ()
    rule_or_model_id: str = ""
    rule_version: str = ""
    rule_description: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "contributing_runtime_a_evidence",
            _freeze_str_tuple(self.contributing_runtime_a_evidence),
        )
        object.__setattr__(
            self, "provenance_refs", _freeze_str_tuple(self.provenance_refs)
        )
        availability = (self.availability or "").strip().lower()
        if availability not in {AVAILABILITY_AVAILABLE, AVAILABILITY_UNAVAILABLE, ""}:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)
        object.__setattr__(self, "facet_name", (self.facet_name or "").strip())

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "availability": self.availability,
            "completeness_reasoning": self.completeness_reasoning,
            "contributing_runtime_a_evidence": list(
                self.contributing_runtime_a_evidence
            ),
            "derivation_summary": self.derivation_summary,
            "facet_name": self.facet_name,
            "provenance_refs": list(self.provenance_refs),
            "rule_description": self.rule_description,
            "rule_or_model_id": self.rule_or_model_id,
            "rule_version": self.rule_version,
            "unavailable_reasoning": self.unavailable_reasoning,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class SnapshotExplanation:
    """Deterministic explanation for a TwinSnapshot (MS-004 T3).

    Aggregates overall completeness, unavailable summary, evidence coverage,
    and the ordered collection of FacetExplanation values.
    """

    twin_id: str = ""
    student_id: str = ""
    generated_at: str | None = None
    explainability_version: str = ""
    overall_completeness_explanation: str = ""
    unavailable_summary_explanation: str = ""
    evidence_coverage_summary: str = ""
    facet_explanations: tuple[FacetExplanation, ...] = ()
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "facet_explanations",
            tuple(self.facet_explanations or ()),
        )
        object.__setattr__(
            self, "provenance_refs", _freeze_str_tuple(self.provenance_refs)
        )
        for item in self.facet_explanations:
            if not isinstance(item, FacetExplanation):
                raise TypeError(
                    "facet_explanations must contain FacetExplanation only"
                )
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "evidence_coverage_summary": self.evidence_coverage_summary,
            "explainability_version": self.explainability_version,
            "facet_explanations": [
                item.to_canonical_dict() for item in self.facet_explanations
            ],
            "generated_at": self.generated_at,
            "overall_completeness_explanation": (
                self.overall_completeness_explanation
            ),
            "provenance_refs": list(self.provenance_refs),
            "student_id": self.student_id,
            "twin_id": self.twin_id,
            "unavailable_summary_explanation": (
                self.unavailable_summary_explanation
            ),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


# --- Experience projection DTOs (MS-004 T5) ---------------------------------


@dataclass(frozen=True)
class FacetSummaryProjection:
    """Experience-safe summary of one Twin facet (MS-004 T5).

    Exposes label / availability / note / evidence refs only — never builder
    internals, mutable state, or Runtime A entity objects.
    """

    facet_name: str = ""
    label: str = ""
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = ""
    summary_note: str = ""
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )
        availability = (self.availability or "").strip().lower()
        if availability not in {AVAILABILITY_AVAILABLE, AVAILABILITY_UNAVAILABLE, ""}:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)
        object.__setattr__(self, "facet_name", (self.facet_name or "").strip())

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "availability": self.availability,
            "evidence_refs": list(self.evidence_refs),
            "facet_name": self.facet_name,
            "label": self.label,
            "summary_note": self.summary_note,
            "unavailable_reason": self.unavailable_reason,
        }


@dataclass(frozen=True)
class ExplanationSummaryProjection:
    """Condensed SnapshotExplanation for Experience (MS-004 T5)."""

    overall_completeness_explanation: str = ""
    unavailable_summary_explanation: str = ""
    evidence_coverage_summary: str = ""
    facet_explanation_summaries: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "facet_explanation_summaries",
            _freeze_str_tuple(self.facet_explanation_summaries),
        )
        object.__setattr__(
            self, "provenance_refs", _freeze_str_tuple(self.provenance_refs)
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "evidence_coverage_summary": self.evidence_coverage_summary,
            "facet_explanation_summaries": list(self.facet_explanation_summaries),
            "overall_completeness_explanation": (
                self.overall_completeness_explanation
            ),
            "provenance_refs": list(self.provenance_refs),
            "unavailable_summary_explanation": (
                self.unavailable_summary_explanation
            ),
        }


@dataclass(frozen=True)
class ProjectionProvenance:
    """Provenance references for an Experience Twin projection (MS-004 T5).

    Carries snapshot identity + Runtime A source references only — never
    Twin builder internals or mutable Twin state.
    """

    twin_snapshot_ref: str = ""
    twin_id: str = ""
    authority: str = AUTHORITY_DIGITAL_TWIN
    source_evidence_version: str = ""
    as_of: str | None = None
    provenance_refs: tuple[str, ...] = ()
    contributing_runtime_a_sources: tuple[str, ...] = ()
    snapshot_provenance: Mapping[str, Any] = field(default_factory=dict)
    provenance_summary: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "provenance_refs", _freeze_str_tuple(self.provenance_refs)
        )
        object.__setattr__(
            self,
            "contributing_runtime_a_sources",
            _freeze_str_tuple(self.contributing_runtime_a_sources),
        )
        object.__setattr__(
            self, "snapshot_provenance", _freeze_mapping(self.snapshot_provenance)
        )
        object.__setattr__(
            self, "provenance_summary", _freeze_mapping(self.provenance_summary)
        )
        if self.as_of is not None and not isinstance(self.as_of, str):
            raise TypeError("as_of must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "authority": self.authority,
            "contributing_runtime_a_sources": list(
                self.contributing_runtime_a_sources
            ),
            "provenance_refs": list(self.provenance_refs),
            "provenance_summary": dict(self.provenance_summary),
            "snapshot_provenance": dict(self.snapshot_provenance),
            "source_evidence_version": self.source_evidence_version,
            "twin_id": self.twin_id,
            "twin_snapshot_ref": self.twin_snapshot_ref,
        }


@dataclass(frozen=True)
class StudentTwinProjection:
    """Dedicated Experience-facing Twin projection (MS-004 T5).

    May expose learner profile summary, facet summaries, completeness,
    explanation summaries, and provenance references. Must not expose Twin
    builder internals, mutable Twin state, or Runtime A entity objects.
    """

    student_id: str = ""
    twin_snapshot_ref: str = ""
    twin_id: str = ""
    as_of: str | None = None
    projection_version: str = ""
    learner_profile_summary: Mapping[str, Any] = field(default_factory=dict)
    facet_summaries: Mapping[str, Any] = field(default_factory=dict)
    completeness: Mapping[str, Any] = field(default_factory=dict)
    explanation_summary: ExplanationSummaryProjection = field(
        default_factory=ExplanationSummaryProjection
    )
    provenance: ProjectionProvenance = field(default_factory=ProjectionProvenance)
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = ""
    limitations_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "learner_profile_summary",
            _freeze_mapping(self.learner_profile_summary),
        )
        object.__setattr__(
            self, "facet_summaries", _freeze_mapping(self.facet_summaries)
        )
        object.__setattr__(self, "completeness", _freeze_mapping(self.completeness))
        object.__setattr__(
            self, "limitations_codes", _freeze_str_tuple(self.limitations_codes)
        )
        if not isinstance(self.explanation_summary, ExplanationSummaryProjection):
            raise TypeError(
                "explanation_summary must be an ExplanationSummaryProjection"
            )
        if not isinstance(self.provenance, ProjectionProvenance):
            raise TypeError("provenance must be a ProjectionProvenance")
        availability = (self.availability or "").strip().lower()
        if availability not in {AVAILABILITY_AVAILABLE, AVAILABILITY_UNAVAILABLE, ""}:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        if self.as_of is not None and not isinstance(self.as_of, str):
            raise TypeError("as_of must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "availability": self.availability,
            "completeness": dict(self.completeness),
            "explanation_summary": self.explanation_summary.to_canonical_dict(),
            "facet_summaries": {
                str(k): dict(v) if isinstance(v, Mapping) else v
                for k, v in sorted(self.facet_summaries.items())
            },
            "learner_profile_summary": dict(self.learner_profile_summary),
            "limitations_codes": list(self.limitations_codes),
            "projection_version": self.projection_version,
            "provenance": self.provenance.to_canonical_dict(),
            "student_id": self.student_id,
            "twin_id": self.twin_id,
            "twin_snapshot_ref": self.twin_snapshot_ref,
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@runtime_checkable
class StudentDigitalTwinContract(Protocol):
    """Pure Student Digital Twin contract — profile in, snapshot out.

    Implementations must be deterministic for identical material inputs.
    Must not write Runtime A educational state. T0 provides structure only.
    """

    def snapshot(self, profile: TwinProfile) -> TwinSnapshot:
        """Project a TwinProfile into an immutable TwinSnapshot."""


@runtime_checkable
class TwinAdapter(Protocol):
    """Adapter interface between Experience / infrastructure and Twin contracts.

    Read-only relative to educational history. Must not call Planning write
    APIs, Evidence acceptance, TopicProgress writes, or mission mutations.
    T0: no synthesis — returns empty authentic / contract stubs only.
    """

    @property
    def adapter_id(self) -> str:
        """Stable Digital Twin Adapter identity."""

    def assemble_snapshot(
        self,
        student_id: str,
        *,
        profile: TwinProfile | None = None,
        as_of: str | None = None,
        mode: str = "contracts",
    ) -> TwinResult:
        """Produce a TwinSnapshot behind the Student Digital Twin contract."""
