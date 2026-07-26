"""Facet provenance helpers for Twin Facet Synthesis (MS-004 T1–T3).

Every synthesised facet exposes source service, source entity, collection
timestamp, availability, and unavailable reason. Missing Runtime A evidence
yields explicit ``unavailable`` — never estimated.

T2 adds snapshot-level provenance aggregation over facet provenance maps.
T3 adds provenance expansion into explainability-facing references.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    FACET_COGNITIVE_LOAD,
    FACET_CONFIDENCE_TREND,
    FACET_CONSISTENCY,
    FACET_LEARNING_RHYTHM,
    FACET_PERSISTENCE,
    FACET_REVISION_BEHAVIOUR,
    FACET_SESSION_HABITS,
    TWIN_FACET_NAMES,
    SnapshotProvenanceSummary,
    TwinProvenance,
)

# Documented unavailable reasons (explicit contracts — no estimation).
REASON_NO_ACTIVE_PLAN = "NO_ACTIVE_PLAN"
REASON_NOT_FOUND = "NOT_FOUND"
REASON_UNAVAILABLE = "UNAVAILABLE"
REASON_COLLECTOR_ERROR = "COLLECTOR_ERROR"
REASON_INVALID_STUDENT_ID = "INVALID_STUDENT_ID"
REASON_NO_CURRICULUM = "NO_CURRICULUM"
REASON_INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
REASON_NO_CONFIDENCE_EVIDENCE = "NO_CONFIDENCE_EVIDENCE"
REASON_INSUFFICIENT_DURATION_EVIDENCE = "INSUFFICIENT_DURATION_EVIDENCE"

# Runtime A input field names consumed by Twin facet synthesis.
FIELD_EVIDENCE = "evidence"
FIELD_TOPIC_PROGRESS = "topic_progress"
FIELD_STUDY_ATTEMPTS = "study_attempts"
FIELD_MISSION = "mission"
FIELD_READINESS = "readiness"
FIELD_CURRICULUM = "curriculum"
FIELD_STUDENT_GOALS = "student_goals"
FIELD_LIFECYCLE_STAGE = "lifecycle_stage"

RUNTIME_A_FIELD_NAMES = (
    FIELD_EVIDENCE,
    FIELD_TOPIC_PROGRESS,
    FIELD_STUDY_ATTEMPTS,
    FIELD_MISSION,
    FIELD_READINESS,
    FIELD_CURRICULUM,
    FIELD_STUDENT_GOALS,
    FIELD_LIFECYCLE_STAGE,
)

FACET_SYNTHESIS_ORDER = (
    FACET_LEARNING_RHYTHM,
    FACET_CONSISTENCY,
    FACET_PERSISTENCE,
    FACET_REVISION_BEHAVIOUR,
    FACET_CONFIDENCE_TREND,
    FACET_SESSION_HABITS,
    FACET_COGNITIVE_LOAD,
)

assert frozenset(FACET_SYNTHESIS_ORDER) == TWIN_FACET_NAMES

KIND_RUNTIME_A_DERIVED = "runtime_a_derived"
KIND_FACT = "fact"
KIND_TWIN_DERIVED = "twin_derived"

SOURCE_SERVICE_TWIN_FACET = "twin_facet_assembler"
SOURCE_SERVICE_TWIN_SNAPSHOT = "twin_snapshot_builder"


def freeze_provenance_map(
    value: Mapping[str, Mapping[str, Any] | TwinProvenance] | None,
) -> Mapping[str, Any]:
    """Freeze a facet→provenance mapping for TwinFacetBundle."""
    if value is None:
        return MappingProxyType({})
    frozen: dict[str, Any] = {}
    for key in sorted(value.keys(), key=str):
        entry = value[key]
        if isinstance(entry, TwinProvenance):
            frozen[str(key)] = MappingProxyType(entry.to_canonical_dict())
        else:
            frozen[str(key)] = MappingProxyType(dict(entry))
    return MappingProxyType(frozen)


def available_facet_provenance(
    *,
    source_service: str,
    source_entity: str,
    collected_at: str | None,
    kind: str = KIND_RUNTIME_A_DERIVED,
) -> TwinProvenance:
    """Build an available facet provenance annotation."""
    return TwinProvenance(
        source_service=source_service,
        source_entity=source_entity,
        collected_at=collected_at,
        availability=AVAILABILITY_AVAILABLE,
        unavailable_reason="",
        kind=kind,
    )


def unavailable_facet_provenance(
    *,
    source_service: str,
    source_entity: str,
    collected_at: str | None,
    reason: str,
    kind: str = KIND_RUNTIME_A_DERIVED,
) -> TwinProvenance:
    """Build an unavailable facet provenance annotation."""
    return TwinProvenance(
        source_service=source_service,
        source_entity=source_entity,
        collected_at=collected_at,
        availability=AVAILABILITY_UNAVAILABLE,
        unavailable_reason=(reason or "").strip() or REASON_UNAVAILABLE,
        kind=kind,
    )


def _provenance_dict(
    entry: TwinProvenance | Mapping[str, Any] | None,
) -> dict[str, Any]:
    if entry is None:
        return {}
    if isinstance(entry, TwinProvenance):
        return entry.to_canonical_dict()
    return dict(entry)


def aggregate_snapshot_provenance(
    field_provenance: Mapping[str, Any] | None,
    *,
    as_of: str | None = None,
    facet_order: tuple[str, ...] = FACET_SYNTHESIS_ORDER,
) -> SnapshotProvenanceSummary:
    """Aggregate facet provenance into a snapshot-level summary.

    Exposes contributing Runtime A sources, evidence window bounds, and
    unavailable inputs. Deterministic for identical provenance maps.
    """
    provenance = field_provenance or {}
    sources: list[str] = []
    timestamps: list[str] = []
    unavailable_inputs: list[str] = []

    for name in facet_order:
        payload = _provenance_dict(provenance.get(name))
        availability = str(payload.get("availability") or "").strip().lower()
        source_service = str(payload.get("source_service") or "").strip()
        collected_at = payload.get("collected_at")
        if isinstance(collected_at, str) and collected_at.strip():
            timestamps.append(collected_at.strip())

        if availability == AVAILABILITY_AVAILABLE:
            if source_service and source_service not in sources:
                sources.append(source_service)
            continue

        # Unavailable facet is an unavailable input at snapshot level.
        unavailable_inputs.append(name)

    # Deterministic unique ordering.
    contributing = tuple(sorted(sources))
    unique_unavailable = tuple(unavailable_inputs)

    window_start: str | None = None
    window_end: str | None = None
    if timestamps:
        window_start = min(timestamps)
        window_end = max(timestamps)
    elif as_of is not None and str(as_of).strip():
        clock = str(as_of).strip()
        window_start = clock
        window_end = clock

    return SnapshotProvenanceSummary(
        contributing_runtime_a_sources=contributing,
        evidence_window_start=window_start,
        evidence_window_end=window_end,
        unavailable_inputs=unique_unavailable,
    )


def snapshot_root_provenance(
    *,
    collected_at: str | None,
    completeness_status: str,
    contributing_sources: tuple[str, ...],
) -> TwinProvenance:
    """Build the TwinSnapshot root provenance annotation."""
    if completeness_status == "empty" or not contributing_sources:
        return TwinProvenance(
            source_service=SOURCE_SERVICE_TWIN_SNAPSHOT,
            source_entity="TwinSnapshot",
            collected_at=collected_at,
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason=(
                "no_available_facets"
                if completeness_status == "empty"
                else REASON_UNAVAILABLE
            ),
            kind=KIND_TWIN_DERIVED,
        )
    return TwinProvenance(
        source_service=SOURCE_SERVICE_TWIN_SNAPSHOT,
        source_entity="TwinSnapshot",
        collected_at=collected_at,
        availability=AVAILABILITY_AVAILABLE,
        unavailable_reason="",
        kind=KIND_TWIN_DERIVED,
    )


# --- T3 provenance expansion ------------------------------------------------

# Authoritative Runtime A fields each facet builder consumes (T1 catalogue).
# Mirrors FacetBuilder.source_fields (required Runtime A inputs only).
FACET_RUNTIME_A_FIELDS: Mapping[str, tuple[str, ...]] = MappingProxyType(
    {
        FACET_LEARNING_RHYTHM: (FIELD_STUDY_ATTEMPTS,),
        FACET_CONSISTENCY: (FIELD_MISSION,),
        FACET_PERSISTENCE: (FIELD_TOPIC_PROGRESS,),
        FACET_REVISION_BEHAVIOUR: (FIELD_TOPIC_PROGRESS,),
        FACET_CONFIDENCE_TREND: (FIELD_STUDY_ATTEMPTS,),
        FACET_SESSION_HABITS: (FIELD_MISSION, FIELD_STUDY_ATTEMPTS),
        FACET_COGNITIVE_LOAD: (FIELD_STUDY_ATTEMPTS,),
    }
)


@dataclass(frozen=True)
class ProvenanceExpansion:
    """Explainability-facing expansion of a TwinProvenance entry (MS-004 T3).

    Expands authoritative provenance into stable references without inventing
    evidence. Identical provenance input → identical expansion every time.
    """

    facet_name: str = ""
    source_service: str = ""
    source_entity: str = ""
    collected_at: str | None = None
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = ""
    kind: str = ""
    reference: str = ""
    contributing_runtime_a_fields: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "contributing_runtime_a_fields",
            tuple(str(item) for item in (self.contributing_runtime_a_fields or ())),
        )
        availability = (self.availability or "").strip().lower()
        object.__setattr__(self, "availability", availability)
        object.__setattr__(self, "facet_name", (self.facet_name or "").strip())

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "availability": self.availability,
            "collected_at": self.collected_at,
            "contributing_runtime_a_fields": list(
                self.contributing_runtime_a_fields
            ),
            "facet_name": self.facet_name,
            "kind": self.kind,
            "reference": self.reference,
            "source_entity": self.source_entity,
            "source_service": self.source_service,
            "unavailable_reason": self.unavailable_reason,
        }


def format_provenance_reference(
    *,
    source_service: str,
    source_entity: str,
    collected_at: str | None = None,
    availability: str = "",
    kind: str = "",
) -> str:
    """Format a deterministic provenance reference string."""
    service = (source_service or "").strip() or "unknown_service"
    entity = (source_entity or "").strip() or "unknown_entity"
    clock = (collected_at or "").strip()
    avail = (availability or "").strip().lower()
    kind_token = (kind or "").strip().lower()
    parts = [f"provenance:{service}/{entity}"]
    if clock:
        parts.append(f"at={clock}")
    if avail:
        parts.append(f"availability={avail}")
    if kind_token:
        parts.append(f"kind={kind_token}")
    return ";".join(parts)


def expand_facet_provenance(
    facet_name: str,
    entry: TwinProvenance | Mapping[str, Any] | None,
    *,
    contributing_fields: tuple[str, ...] | None = None,
) -> ProvenanceExpansion:
    """Expand one facet provenance entry into an explainability reference."""
    payload = _provenance_dict(entry)
    fields = contributing_fields
    if fields is None:
        fields = FACET_RUNTIME_A_FIELDS.get(facet_name, ())
    source_service = str(payload.get("source_service") or "").strip()
    source_entity = str(payload.get("source_entity") or "").strip()
    collected_at = payload.get("collected_at")
    if collected_at is not None:
        collected_at = str(collected_at).strip() or None
    availability = str(payload.get("availability") or "").strip().lower()
    unavailable_reason = str(payload.get("unavailable_reason") or "").strip()
    kind = str(payload.get("kind") or "").strip().lower()
    reference = format_provenance_reference(
        source_service=source_service,
        source_entity=source_entity,
        collected_at=collected_at,
        availability=availability,
        kind=kind,
    )
    return ProvenanceExpansion(
        facet_name=(facet_name or "").strip(),
        source_service=source_service,
        source_entity=source_entity,
        collected_at=collected_at,
        availability=availability or AVAILABILITY_UNAVAILABLE,
        unavailable_reason=unavailable_reason,
        kind=kind,
        reference=reference,
        contributing_runtime_a_fields=tuple(fields),
    )


def expand_snapshot_provenance(
    field_provenance: Mapping[str, Any] | None,
    *,
    facet_order: tuple[str, ...] = FACET_SYNTHESIS_ORDER,
    root: TwinProvenance | Mapping[str, Any] | None = None,
) -> tuple[ProvenanceExpansion, ...]:
    """Expand snapshot facet (+ optional root) provenance deterministically."""
    provenance = field_provenance or {}
    expansions: list[ProvenanceExpansion] = []
    for name in facet_order:
        expansions.append(
            expand_facet_provenance(name, provenance.get(name))
        )
    if root is not None:
        expansions.append(
            expand_facet_provenance(
                "TwinSnapshot",
                root,
                contributing_fields=(),
            )
        )
    return tuple(expansions)
