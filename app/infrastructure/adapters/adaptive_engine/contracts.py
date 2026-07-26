"""Adaptive Decision contracts (MS-003 A0/A1/A2; MS-004 T4 Twin input).

Immutable DTOs and Protocol interfaces. A0 defines decision I/O contracts.
A1 adds field provenance on AdaptiveInputBundle. A2 populates explainability
inputs_used / inputs_unavailable via the AdaptiveEngineExecutor. MS-004 T4
adds optional read-only TwinAdaptiveInputAttachment on AdaptiveInputBundle.
No Experience cutover or educational writes from Twin consumption.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date, datetime
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable

# Shared failure codes (ADAPTIVE_INTERFACE_SPECIFICATION.md).
UNAVAILABLE = "UNAVAILABLE"
NO_ACTIVE_PLAN = "NO_ACTIVE_PLAN"
NOT_FOUND = "NOT_FOUND"
FORBIDDEN = "FORBIDDEN"
INVALID_STATE = "INVALID_STATE"
EXPLAINABILITY_INCOMPLETE = "EXPLAINABILITY_INCOMPLETE"
BEHAVIOUR_MISMATCH = "BEHAVIOUR_MISMATCH"

ADAPTIVE_ERROR_CODES = frozenset(
    {
        UNAVAILABLE,
        NO_ACTIVE_PLAN,
        NOT_FOUND,
        FORBIDDEN,
        INVALID_STATE,
        EXPLAINABILITY_INCOMPLETE,
        BEHAVIOUR_MISMATCH,
    }
)

AUTHORITY_ADAPTIVE_ENGINE = "adaptive_engine"
AUTHORITY_RUNTIME_A = "runtime_a"

CONFIDENCE_BANDS = frozenset({"low", "medium", "high", ""})


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
    raise TypeError(f"Unsupported adaptive contract value type: {type(value)!r}")


def serialize_canonical(value: Any) -> str:
    """Deterministic JSON serialization (sorted keys, compact separators)."""
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class EvidenceRef:
    """Reference to an authoritative educational evidence artefact."""

    kind: str = ""
    id: str = ""
    observed_at: str | None = None
    note: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "note": self.note,
            "observed_at": self.observed_at,
        }


@dataclass(frozen=True)
class TopicRef:
    """Curriculum topic reference used in explanations / outputs."""

    topic_code: str = ""
    title: str = ""
    role: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "title": self.title,
            "topic_code": self.topic_code,
        }


@dataclass(frozen=True)
class RuleRef:
    """Deterministic rule / model identity for explainability."""

    rule_or_model_id: str = ""
    version: str = ""
    description: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "description": self.description,
            "rule_or_model_id": self.rule_or_model_id,
            "version": self.version,
        }


@dataclass(frozen=True)
class ConfidencePlaceholder:
    """Confidence facet (placeholder until Engine compute exists)."""

    score: float | None = None
    band: str = ""
    rationale: str = ""

    def __post_init__(self) -> None:
        band = (self.band or "").strip().lower()
        if band not in CONFIDENCE_BANDS:
            allowed = sorted(CONFIDENCE_BANDS)
            raise ValueError(f"confidence band must be one of {allowed}")
        object.__setattr__(self, "band", band)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "band": self.band,
            "rationale": self.rationale,
            "score": self.score,
        }


@dataclass(frozen=True)
class RecommendationPlaceholder:
    """Recommendation facet (placeholder — no ranking / scoring in A0)."""

    topic_code: str | None = None
    title: str | None = None
    decision_kind: str = ""
    label: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "decision_kind": self.decision_kind,
            "label": self.label,
            "title": self.title,
            "topic_code": self.topic_code,
        }


@dataclass(frozen=True)
class ExplanationBundle:
    """Structured explainability contract for adaptive decisions.

    Structure is always complete; fields may be empty until Engine compute.
    Supports evidence refs, rule refs, confidence, input summary, and rationale.
    A2 populates inputs_used / inputs_unavailable from field provenance.
    """

    evidence_refs: tuple[EvidenceRef, ...] = ()
    rule_refs: tuple[RuleRef, ...] = ()
    confidence: ConfidencePlaceholder = field(default_factory=ConfidencePlaceholder)
    input_summary: str = ""
    recommendation_rationale: str = ""
    # Six-question groups (ADAPTIVE_EXPLAINABILITY.md) — may be empty.
    why_summary: str = ""
    why_reason_codes: tuple[str, ...] = ()
    topic_refs: tuple[TopicRef, ...] = ()
    alternatives_rationale: str = ""
    limitations_codes: tuple[str, ...] = ()
    limitations_summary: str = ""
    mission_aligned: bool | None = None
    mission_note: str = ""
    inputs_used: tuple[str, ...] = ()
    inputs_unavailable: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "evidence_refs",
            tuple(self.evidence_refs or ()),
        )
        object.__setattr__(self, "rule_refs", tuple(self.rule_refs or ()))
        object.__setattr__(self, "topic_refs", tuple(self.topic_refs or ()))
        object.__setattr__(
            self,
            "why_reason_codes",
            _freeze_str_tuple(self.why_reason_codes),
        )
        object.__setattr__(
            self,
            "limitations_codes",
            _freeze_str_tuple(self.limitations_codes),
        )
        object.__setattr__(self, "inputs_used", _freeze_str_tuple(self.inputs_used))
        object.__setattr__(
            self,
            "inputs_unavailable",
            _freeze_str_tuple(self.inputs_unavailable),
        )
        if not isinstance(self.confidence, ConfidencePlaceholder):
            raise TypeError("confidence must be a ConfidencePlaceholder")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "alternatives_rationale": self.alternatives_rationale,
            "confidence": self.confidence.to_canonical_dict(),
            "evidence_refs": [ref.to_canonical_dict() for ref in self.evidence_refs],
            "input_summary": self.input_summary,
            "inputs_unavailable": list(self.inputs_unavailable),
            "inputs_used": list(self.inputs_used),
            "limitations_codes": list(self.limitations_codes),
            "limitations_summary": self.limitations_summary,
            "mission_aligned": self.mission_aligned,
            "mission_note": self.mission_note,
            "recommendation_rationale": self.recommendation_rationale,
            "rule_refs": [ref.to_canonical_dict() for ref in self.rule_refs],
            "topic_refs": [ref.to_canonical_dict() for ref in self.topic_refs],
            "why_reason_codes": list(self.why_reason_codes),
            "why_summary": self.why_summary,
        }

    def serialize(self) -> str:
        """Deterministic JSON serialization."""
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class TwinAdaptiveInputAttachment:
    """Optional Twin enrichment attached to AdaptiveInputBundle (MS-004 T4).

    Read-only structural projection of an immutable TwinSnapshot. Adaptive may
    consume this attachment; it must never replace Runtime A collectors, mutate
    Twin state, trigger Twin synthesis, or persist Twin data.
    """

    twin_snapshot_ref: str = ""
    twin_id: str = ""
    as_of: str | None = None
    behaviour: Mapping[str, Any] = field(default_factory=dict)
    memory: Mapping[str, Any] = field(default_factory=dict)
    predictions: Mapping[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()
    completeness: Mapping[str, Any] = field(default_factory=dict)
    provenance: Mapping[str, Any] = field(default_factory=dict)
    explanation: Mapping[str, Any] = field(default_factory=dict)
    availability: str = "unavailable"
    unavailable_reason: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "behaviour", _freeze_mapping(self.behaviour))
        object.__setattr__(self, "memory", _freeze_mapping(self.memory))
        object.__setattr__(self, "predictions", _freeze_mapping(self.predictions))
        object.__setattr__(self, "completeness", _freeze_mapping(self.completeness))
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(self, "explanation", _freeze_mapping(self.explanation))
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        availability = (self.availability or "").strip().lower()
        if availability not in {"available", "unavailable", ""}:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)
        if self.as_of is not None and not isinstance(self.as_of, str):
            raise TypeError("as_of must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "availability": self.availability,
            "behaviour": dict(self.behaviour),
            "completeness": dict(self.completeness),
            "explanation": dict(self.explanation),
            "limitations": list(self.limitations),
            "memory": dict(self.memory),
            "predictions": dict(self.predictions),
            "provenance": dict(self.provenance),
            "twin_id": self.twin_id,
            "twin_snapshot_ref": self.twin_snapshot_ref,
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class AdaptiveInputBundle:
    """Immutable Adaptive Decision input snapshot (A0/A1/T4 contract).

    May contain Evidence, Topic Progress, Study Attempts, Readiness, Mission,
    Curriculum, and Student Goals blocks. Blocks are opaque Runtime A
    projections — this DTO performs no educational calculations.

    A1 adds ``field_provenance``: every input field exposes source service,
    source entity, collection timestamp (``as_of`` clock), and availability.
    Missing inputs are ``unavailable`` with a documented reason.

    MS-004 T4 adds optional ``twin`` (TwinAdaptiveInputAttachment projection).
    Twin is enrichment only — Runtime A remains primary Adaptive input.

    Determinism rules:
    - No auto-generated timestamps or random identifiers.
    - Collections are immutable tuples / MappingProxyType.
    - ``as_of`` is optional educational decision clock (ISO string or None).
    - ``field_provenance[*].collected_at`` equals ``as_of`` (or empty) — never
      wall-clock.
    """

    student_id: str
    as_of: str | None = None
    evidence: Mapping[str, Any] = field(default_factory=dict)
    topic_progress: tuple[Mapping[str, Any], ...] = ()
    study_attempts: tuple[Mapping[str, Any], ...] = ()
    readiness: Mapping[str, Any] = field(default_factory=dict)
    mission: Mapping[str, Any] = field(default_factory=dict)
    curriculum: Mapping[str, Any] = field(default_factory=dict)
    student_goals: Mapping[str, Any] = field(default_factory=dict)
    authority_tags: tuple[str, ...] = ()
    lifecycle_stage: str = ""
    field_provenance: Mapping[str, Any] = field(default_factory=dict)
    twin: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        from app.infrastructure.adapters.adaptive_engine.provenance import (
            freeze_provenance_map,
        )

        sid = (self.student_id or "").strip()
        if not sid:
            raise ValueError("student_id must be a non-empty string")
        object.__setattr__(self, "student_id", sid)
        object.__setattr__(self, "evidence", _freeze_mapping(self.evidence))
        object.__setattr__(self, "readiness", _freeze_mapping(self.readiness))
        object.__setattr__(self, "mission", _freeze_mapping(self.mission))
        object.__setattr__(self, "curriculum", _freeze_mapping(self.curriculum))
        object.__setattr__(self, "student_goals", _freeze_mapping(self.student_goals))
        twin_value: Mapping[str, Any] | TwinAdaptiveInputAttachment | None = self.twin
        if isinstance(twin_value, TwinAdaptiveInputAttachment):
            twin_value = twin_value.to_canonical_dict()
        object.__setattr__(self, "twin", _freeze_mapping(twin_value))
        object.__setattr__(
            self,
            "topic_progress",
            tuple(_freeze_mapping(item) for item in (self.topic_progress or ())),
        )
        object.__setattr__(
            self,
            "study_attempts",
            tuple(_freeze_mapping(item) for item in (self.study_attempts or ())),
        )
        object.__setattr__(
            self,
            "authority_tags",
            _freeze_str_tuple(self.authority_tags),
        )
        object.__setattr__(
            self,
            "field_provenance",
            freeze_provenance_map(self.field_provenance),
        )
        if self.as_of is not None and not isinstance(self.as_of, str):
            raise TypeError("as_of must be an ISO string or None (no auto clock)")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "authority_tags": list(self.authority_tags),
            "curriculum": dict(self.curriculum),
            "evidence": dict(self.evidence),
            "field_provenance": {
                str(k): dict(v) for k, v in sorted(self.field_provenance.items())
            },
            "lifecycle_stage": self.lifecycle_stage,
            "mission": dict(self.mission),
            "readiness": dict(self.readiness),
            "student_goals": dict(self.student_goals),
            "student_id": self.student_id,
            "study_attempts": [dict(item) for item in self.study_attempts],
            "topic_progress": [dict(item) for item in self.topic_progress],
            "twin": dict(self.twin),
        }

    def serialize(self) -> str:
        """Deterministic JSON serialization of material input fields."""
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class AdaptiveOutputBundle:
    """Immutable Adaptive Decision output artefact (A0 contract).

    Contains recommendation / confidence placeholders and a complete
    ExplanationBundle. No educational calculations in A0.
    """

    recommendation: RecommendationPlaceholder = field(
        default_factory=RecommendationPlaceholder
    )
    confidence: ConfidencePlaceholder = field(default_factory=ConfidencePlaceholder)
    explanation: ExplanationBundle = field(default_factory=ExplanationBundle)
    decision_id: str = ""
    authority: str = AUTHORITY_ADAPTIVE_ENGINE

    def __post_init__(self) -> None:
        if not isinstance(self.recommendation, RecommendationPlaceholder):
            raise TypeError("recommendation must be a RecommendationPlaceholder")
        if not isinstance(self.confidence, ConfidencePlaceholder):
            raise TypeError("confidence must be a ConfidencePlaceholder")
        if not isinstance(self.explanation, ExplanationBundle):
            raise TypeError("explanation must be an ExplanationBundle")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "confidence": self.confidence.to_canonical_dict(),
            "decision_id": self.decision_id,
            "explanation": self.explanation.to_canonical_dict(),
            "recommendation": self.recommendation.to_canonical_dict(),
        }

    def serialize(self) -> str:
        """Deterministic JSON serialization."""
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class AdaptiveDecisionResult:
    """Result envelope for Adaptive Engine Adapter calls."""

    ok: bool
    value: AdaptiveOutputBundle | None = None
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


@runtime_checkable
class AdaptiveDecisionContract(Protocol):
    """Pure Adaptive Decision contract — inputs in, explainable outputs out.

    Implementations must be deterministic for identical AdaptiveInputBundle
    material fields. Must not write Runtime A educational state.
    """

    def evaluate(self, inputs: AdaptiveInputBundle) -> AdaptiveOutputBundle:
        """Evaluate an AdaptiveInputBundle into an AdaptiveOutputBundle."""


@runtime_checkable
class AdaptiveEngineBridge(Protocol):
    """Adapter interface between Experience and Adaptive Decision contracts.

    Read-only relative to educational history. Must not call Planning write
    APIs, Evidence acceptance, TopicProgress writes, or mission mutations.
    """

    @property
    def adapter_id(self) -> str:
        """Stable Adaptive Engine Adapter identity."""

    def decide(
        self,
        student_id: str,
        *,
        inputs: AdaptiveInputBundle | None = None,
        decision_kinds: tuple[str, ...] | None = None,
        include_explanation: bool = True,
        shadow: bool = False,
    ) -> AdaptiveDecisionResult:
        """Produce an AdaptiveOutputBundle behind the Adaptive Decision contract."""
