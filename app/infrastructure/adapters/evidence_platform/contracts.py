"""Learning Evidence Platform contracts (MS-006 E0 / E1 / E2 / E3 / E4 / E5).

Immutable DTOs and Protocol interfaces. E0 defines EvidenceRecord,
ExperimentDefinition, PolicyEvaluation, OutcomeMetric, analytics export
placeholders, LearningEvidenceContract, and EvidenceAdapter. E1 extends
EvidenceRecord with collection fields and adds ObservedEvent for intake.
E2 adds ExperimentObservation for deterministic experiment assignment.
E3 adds PolicyDefinition and evaluation artefacts for governed policy
assessment. E4 adds AnalyticsSummary, EvidenceProjection, MetricSeries,
ScorecardSlice, and EvidenceProjectionPort for governance-facing analytics
aggregation and read-only projection. E5 adds readiness version metadata
(``EVIDENCE_VERSION_E5``) consumed by observational shadow validation.
P2-MS008 adds EvidenceFactualSummary and EvidenceReadPort. P2-MS009 adds
EvidenceAdvisory and EvidenceAdvisoryPort for Runtime A factual advisory
inputs. No persistence, policy promotion, or upstream educational writes.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable

# Shared failure codes (observational measurement surface).
UNAVAILABLE = "UNAVAILABLE"
NOT_FOUND = "NOT_FOUND"
FORBIDDEN = "FORBIDDEN"
INVALID_STATE = "INVALID_STATE"
EVIDENCE_QUALITY_INCOMPLETE = "EVIDENCE_QUALITY_INCOMPLETE"
CLAIM_BOUNDARY_LEAKAGE = "CLAIM_BOUNDARY_LEAKAGE"
BEHAVIOUR_MISMATCH = "BEHAVIOUR_MISMATCH"

EVIDENCE_ERROR_CODES = frozenset(
    {
        UNAVAILABLE,
        NOT_FOUND,
        FORBIDDEN,
        INVALID_STATE,
        EVIDENCE_QUALITY_INCOMPLETE,
        CLAIM_BOUNDARY_LEAKAGE,
        BEHAVIOUR_MISMATCH,
    }
)

AUTHORITY_EVIDENCE_PLATFORM = "evidence_platform"
AUTHORITY_RUNTIME_A = "runtime_a"

EVIDENCE_VERSION_E0 = "e0.1"
EVIDENCE_VERSION_E1 = "e1.0"
EVIDENCE_VERSION_E2 = "e2.0"
EVIDENCE_VERSION_E3 = "e3.0"
EVIDENCE_VERSION_E4 = "e4.0"
EVIDENCE_VERSION_E5 = "e5.0"

TREND_DIRECTION_FLAT = "flat"
TREND_DIRECTION_UP = "up"
TREND_DIRECTION_DOWN = "down"
TREND_DIRECTION_NOT_ESTIMABLE = "not_estimable"

TREND_DIRECTIONS = frozenset(
    {
        TREND_DIRECTION_FLAT,
        TREND_DIRECTION_UP,
        TREND_DIRECTION_DOWN,
        TREND_DIRECTION_NOT_ESTIMABLE,
        "",
    }
)

GRAIN_NIGHT = "night"
GRAIN_STUDENT = "student"
GRAIN_COHORT = "cohort"
GRAIN_SYSTEM = "system"

ANALYTICS_GRAINS = frozenset(
    {GRAIN_NIGHT, GRAIN_STUDENT, GRAIN_COHORT, GRAIN_SYSTEM, ""}
)

ASSIGNMENT_MECHANISM_HASH = "hash"
ASSIGNMENT_MECHANISM_MANUAL_ALLOWLIST = "manual_allowlist"
ASSIGNMENT_MECHANISM_OPS_OVERRIDE = "ops_override"

ASSIGNMENT_MECHANISMS = frozenset(
    {
        ASSIGNMENT_MECHANISM_HASH,
        ASSIGNMENT_MECHANISM_MANUAL_ALLOWLIST,
        ASSIGNMENT_MECHANISM_OPS_OVERRIDE,
        "",
    }
)

CLAIM_ORGANISATION = "organisation"
CLAIM_LEARNING_SIGNAL = "learning_signal"
CLAIM_LEARNING_DEPTH = "learning_depth"
CLAIM_TRANSFER = "transfer"
CLAIM_TRUST_INSPECTABILITY = "trust_inspectability"

CLAIM_BOUNDARIES = frozenset(
    {
        CLAIM_ORGANISATION,
        CLAIM_LEARNING_SIGNAL,
        CLAIM_LEARNING_DEPTH,
        CLAIM_TRANSFER,
        CLAIM_TRUST_INSPECTABILITY,
        "",
    }
)

REF_KIND_RUNTIME_A = "runtime_a"
REF_KIND_TWIN = "twin"
REF_KIND_ADAPTIVE = "adaptive"
REF_KIND_STRATEGY = "strategy"
REF_KIND_EXPERIENCE = "experience"
REF_KIND_TELEMETRY = "telemetry"

REF_KINDS = frozenset(
    {
        REF_KIND_RUNTIME_A,
        REF_KIND_TWIN,
        REF_KIND_ADAPTIVE,
        REF_KIND_STRATEGY,
        REF_KIND_EXPERIENCE,
        REF_KIND_TELEMETRY,
        "",
    }
)

CLASS_FACT_EVENT = "FACT_EVENT"
CLASS_DELIVERY_EVENT = "DELIVERY_EVENT"
CLASS_ADVICE_EVENT = "ADVICE_EVENT"
CLASS_ORCHESTRATION_EVENT = "ORCHESTRATION_EVENT"
CLASS_INTERPRETATION_EVENT = "INTERPRETATION_EVENT"
CLASS_OPS_EVENT = "OPS_EVENT"
CLASS_RESEARCH_EVENT = "RESEARCH_EVENT"

EVIDENCE_CLASSES = frozenset(
    {
        CLASS_FACT_EVENT,
        CLASS_DELIVERY_EVENT,
        CLASS_ADVICE_EVENT,
        CLASS_ORCHESTRATION_EVENT,
        CLASS_INTERPRETATION_EVENT,
        CLASS_OPS_EVENT,
        CLASS_RESEARCH_EVENT,
        "",
    }
)

QUALITY_PASS = "pass"
QUALITY_FAIL = "fail"
QUALITY_INELIGIBLE = "ineligible"
QUALITY_RESULTS = frozenset(
    {QUALITY_PASS, QUALITY_FAIL, QUALITY_INELIGIBLE, ""}
)

EXPERIMENT_STATUS_DRAFT = "draft"
EXPERIMENT_STATUS_REGISTERED = "registered"
EXPERIMENT_STATUS_RUNNING = "running"
EXPERIMENT_STATUS_PAUSED = "paused"
EXPERIMENT_STATUS_ANALYSED = "analysed"
EXPERIMENT_STATUS_CLOSED = "closed"
EXPERIMENT_STATUS_ABORTED = "aborted"

EXPERIMENT_STATUSES = frozenset(
    {
        EXPERIMENT_STATUS_DRAFT,
        EXPERIMENT_STATUS_REGISTERED,
        EXPERIMENT_STATUS_RUNNING,
        EXPERIMENT_STATUS_PAUSED,
        EXPERIMENT_STATUS_ANALYSED,
        EXPERIMENT_STATUS_CLOSED,
        EXPERIMENT_STATUS_ABORTED,
        "",
    }
)

# Statuses that may receive deterministic assignment (E2).
ASSIGNABLE_EXPERIMENT_STATUSES = frozenset(
    {
        EXPERIMENT_STATUS_REGISTERED,
        EXPERIMENT_STATUS_RUNNING,
    }
)

EXPOSURE_SHADOW_ONLY = "shadow_only"
EXPOSURE_FLAG_MEDIATED_SERVE = "flag_mediated_serve"
EXPOSURE_MODES = frozenset(
    {EXPOSURE_SHADOW_ONLY, EXPOSURE_FLAG_MEDIATED_SERVE, ""}
)

GATE_PASSED = "passed"
GATE_FAILED = "failed"
GATE_INELIGIBLE = "ineligible"
GATE_RESULTS = frozenset({GATE_PASSED, GATE_FAILED, GATE_INELIGIBLE, ""})

RECOMMENDATION_KEEP = "keep"
RECOMMENDATION_REVISE = "revise"
RECOMMENDATION_ROLL_BACK = "roll_back"
RECOMMENDATION_EXPAND_SOAK = "expand_soak"
RECOMMENDATION_INCONCLUSIVE = "inconclusive"

EVALUATION_RECOMMENDATIONS = frozenset(
    {
        RECOMMENDATION_KEEP,
        RECOMMENDATION_REVISE,
        RECOMMENDATION_ROLL_BACK,
        RECOMMENDATION_EXPAND_SOAK,
        RECOMMENDATION_INCONCLUSIVE,
        "",
    }
)

CONFIDENCE_BANDS = frozenset(
    {"high", "medium", "low", "insufficient", ""}
)

POLICY_OWNER_ADAPTIVE = "adaptive"
POLICY_OWNER_STRATEGY = "strategy"
POLICY_OWNER_EXPERIENCE_ROUTING = "experience_routing"
POLICY_OWNER_TWIN_PROJECTION = "twin_projection"
POLICY_OWNER_CROSS_CUTTING = "cross_cutting"
POLICY_OWNER_OPS_GATE = "ops_gate"

POLICY_OWNER_LAYERS = frozenset(
    {
        POLICY_OWNER_ADAPTIVE,
        POLICY_OWNER_STRATEGY,
        POLICY_OWNER_EXPERIENCE_ROUTING,
        POLICY_OWNER_TWIN_PROJECTION,
        POLICY_OWNER_CROSS_CUTTING,
        POLICY_OWNER_OPS_GATE,
        "",
    }
)

POLICY_STATUS_PROPOSED = "proposed"
POLICY_STATUS_ACTIVE = "active"
POLICY_STATUS_DEPRECATED = "deprecated"
POLICY_STATUS_ROLLED_BACK = "rolled_back"

POLICY_STATUSES = frozenset(
    {
        POLICY_STATUS_PROPOSED,
        POLICY_STATUS_ACTIVE,
        POLICY_STATUS_DEPRECATED,
        POLICY_STATUS_ROLLED_BACK,
        "",
    }
)

# Statuses that may receive deterministic policy evaluation (E3).
EVALUABLE_POLICY_STATUSES = frozenset(
    {
        POLICY_STATUS_PROPOSED,
        POLICY_STATUS_ACTIVE,
    }
)

EVALUATION_KIND_SHADOW_DESCRIPTIVE = "shadow_descriptive"
EVALUATION_KIND_SHADOW_COMPARE = "shadow_compare"
EVALUATION_KIND_FLAG_MEDIATED_COMPARE = "flag_mediated_compare"
EVALUATION_KIND_POST_HOC_INCIDENT = "post_hoc_incident"
EVALUATION_KIND_RESEARCH_LINKAGE = "research_linkage"

EVALUATION_KINDS = frozenset(
    {
        EVALUATION_KIND_SHADOW_DESCRIPTIVE,
        EVALUATION_KIND_SHADOW_COMPARE,
        EVALUATION_KIND_FLAG_MEDIATED_COMPARE,
        EVALUATION_KIND_POST_HOC_INCIDENT,
        EVALUATION_KIND_RESEARCH_LINKAGE,
        "",
    }
)

STATISTICAL_DESIGN_DESCRIPTIVE_SOAK = "descriptive_soak"
STATISTICAL_DESIGN_PRE_REGISTERED_COMPARE = "pre_registered_compare"
STATISTICAL_DESIGN_INTERRUPTED_TIME = "interrupted_time"
STATISTICAL_DESIGN_OTHER = "other"

STATISTICAL_DESIGNS = frozenset(
    {
        STATISTICAL_DESIGN_DESCRIPTIVE_SOAK,
        STATISTICAL_DESIGN_PRE_REGISTERED_COMPARE,
        STATISTICAL_DESIGN_INTERRUPTED_TIME,
        STATISTICAL_DESIGN_OTHER,
        "",
    }
)

GATE_CODE_CLAIM_BOUNDARY_LEAKAGE = "CLAIM_BOUNDARY_LEAKAGE"
GATE_CODE_MISSING_RUNTIME_A = "MISSING_RUNTIME_A"
GATE_CODE_STATISTICS_INCOMPLETE = "STATISTICS_INCOMPLETE"
GATE_CODE_OVERCLAIM = "OVERCLAIM"
GATE_CODE_DEMO_THEATRE = "DEMO_THEATRE"
GATE_CODE_INCOMPLETE_EXPLAINABILITY = "INCOMPLETE_EXPLAINABILITY"
GATE_CODE_INSUFFICIENT_OBSERVATIONS = "INSUFFICIENT_OBSERVATIONS"

EVALUATION_GATE_CODES = frozenset(
    {
        GATE_CODE_CLAIM_BOUNDARY_LEAKAGE,
        GATE_CODE_MISSING_RUNTIME_A,
        GATE_CODE_STATISTICS_INCOMPLETE,
        GATE_CODE_OVERCLAIM,
        GATE_CODE_DEMO_THEATRE,
        GATE_CODE_INCOMPLETE_EXPLAINABILITY,
        GATE_CODE_INSUFFICIENT_OBSERVATIONS,
    }
)

ANALYTICS_AUDIENCE_GOVERNANCE = "governance"
ANALYTICS_AUDIENCE_RESEARCH = "research"
ANALYTICS_AUDIENCE_ENGINEERING_OPS = "engineering_ops"

ANALYTICS_AUDIENCES = frozenset(
    {
        ANALYTICS_AUDIENCE_GOVERNANCE,
        ANALYTICS_AUDIENCE_RESEARCH,
        ANALYTICS_AUDIENCE_ENGINEERING_OPS,
        "",
    }
)

AVAILABILITY_AVAILABLE = "available"
AVAILABILITY_UNAVAILABLE = "unavailable"
AVAILABILITY_VALUES = frozenset(
    {AVAILABILITY_AVAILABLE, AVAILABILITY_UNAVAILABLE, ""}
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
    raise TypeError(f"Unsupported evidence contract value type: {type(value)!r}")


def serialize_canonical(value: Any) -> str:
    """Deterministic JSON serialization (sorted keys, compact separators)."""
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


def _normalize_claim_boundary(value: str) -> str:
    boundary = (value or "").strip().lower()
    if boundary not in CLAIM_BOUNDARIES:
        allowed = sorted(k for k in CLAIM_BOUNDARIES if k)
        raise ValueError(f"claim_boundary must be one of {allowed} or empty")
    return boundary


@dataclass(frozen=True)
class ObservationRef:
    """Minimal pointer into an upstream authority (prefer ids / fingerprints)."""

    ref_kind: str = ""
    entity_kind: str = ""
    entity_id: str = ""
    fingerprint: str = ""
    observed_at: str | None = None
    as_of: str | None = None
    student_id: str = ""
    claim_boundary: str = ""

    def __post_init__(self) -> None:
        kind = (self.ref_kind or "").strip().lower()
        if kind not in REF_KINDS:
            allowed = sorted(k for k in REF_KINDS if k)
            raise ValueError(f"ref_kind must be one of {allowed} or empty")
        object.__setattr__(self, "ref_kind", kind)
        object.__setattr__(
            self, "claim_boundary", _normalize_claim_boundary(self.claim_boundary)
        )
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        for label, value in (
            ("observed_at", self.observed_at),
            ("as_of", self.as_of),
        ):
            if value is not None and not isinstance(value, str):
                raise TypeError(f"{label} must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "claim_boundary": self.claim_boundary,
            "entity_id": self.entity_id,
            "entity_kind": self.entity_kind,
            "fingerprint": self.fingerprint,
            "observed_at": self.observed_at,
            "ref_kind": self.ref_kind,
            "student_id": self.student_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EvidenceQuality:
    """Structural quality gate result (no intake logic in E0)."""

    result: str = ""
    codes: tuple[str, ...] = ()
    summary: str = ""
    runtime_a_ref_present: bool = False

    def __post_init__(self) -> None:
        result = (self.result or "").strip().lower()
        if result not in QUALITY_RESULTS:
            allowed = sorted(k for k in QUALITY_RESULTS if k)
            raise ValueError(f"result must be one of {allowed} or empty")
        object.__setattr__(self, "result", result)
        object.__setattr__(self, "codes", _freeze_str_tuple(self.codes))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "codes": list(self.codes),
            "result": self.result,
            "runtime_a_ref_present": self.runtime_a_ref_present,
            "summary": self.summary,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EvidenceContext:
    """Immutable observational input context (E0/E1 contract).

    Carries student identity, decision clock, and upstream observation refs.
    Assemblers freeze inputs; E1 intake may project this into EvidenceRecord.
    """

    student_id: str
    as_of: str | None = None
    source_refs: tuple[ObservationRef, ...] = ()
    claim_boundary: str = ""
    evidence_class: str = ""
    field_provenance: Mapping[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        sid = (self.student_id or "").strip()
        if not sid:
            raise ValueError("student_id must be a non-empty string")
        object.__setattr__(self, "student_id", sid)
        if self.as_of is not None and not isinstance(self.as_of, str):
            raise TypeError("as_of must be an ISO string or None (no auto clock)")
        object.__setattr__(self, "source_refs", tuple(self.source_refs or ()))
        for ref in self.source_refs:
            if not isinstance(ref, ObservationRef):
                raise TypeError("source_refs must contain ObservationRef values")
        object.__setattr__(
            self, "claim_boundary", _normalize_claim_boundary(self.claim_boundary)
        )
        evidence_class = (self.evidence_class or "").strip().upper()
        if evidence_class not in EVIDENCE_CLASSES:
            allowed = sorted(k for k in EVIDENCE_CLASSES if k)
            raise ValueError(f"evidence_class must be one of {allowed} or empty")
        object.__setattr__(self, "evidence_class", evidence_class)
        object.__setattr__(
            self, "field_provenance", _freeze_mapping(self.field_provenance)
        )
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "claim_boundary": self.claim_boundary,
            "evidence_class": self.evidence_class,
            "field_provenance": {
                str(k): dict(v) if isinstance(v, Mapping) else v
                for k, v in sorted(self.field_provenance.items())
            },
            "limitations": list(self.limitations),
            "source_refs": [ref.to_canonical_dict() for ref in self.source_refs],
            "student_id": self.student_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ObservedEvent:
    """Immutable observed educational / delivery event for E1 intake.

    Carries observation and ingestion clocks explicitly — no wall-clock.
    Upstream payloads (runtime_a / twin / adaptive / strategy / experience)
    are reference sources only; collectors freeze them and never mutate inputs.
    """

    student_id: str
    event_type: str = ""
    observed_at: str | None = None
    ingested_at: str | None = None
    as_of: str | None = None
    claim_boundary: str = ""
    evidence_class: str = ""
    source_refs: tuple[ObservationRef, ...] = ()
    runtime_a: Mapping[str, Any] = field(default_factory=dict)
    experience: Mapping[str, Any] = field(default_factory=dict)
    strategy: Mapping[str, Any] = field(default_factory=dict)
    adaptive: Mapping[str, Any] = field(default_factory=dict)
    twin: Mapping[str, Any] = field(default_factory=dict)
    payload_summary: Mapping[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        sid = (self.student_id or "").strip()
        if not sid:
            raise ValueError("student_id must be a non-empty string")
        object.__setattr__(self, "student_id", sid)
        object.__setattr__(self, "event_type", (self.event_type or "").strip())
        for label, value in (
            ("observed_at", self.observed_at),
            ("ingested_at", self.ingested_at),
            ("as_of", self.as_of),
        ):
            if value is not None and not isinstance(value, str):
                raise TypeError(
                    f"{label} must be an ISO string or None (no auto clock)"
                )
        object.__setattr__(self, "source_refs", tuple(self.source_refs or ()))
        for ref in self.source_refs:
            if not isinstance(ref, ObservationRef):
                raise TypeError("source_refs must contain ObservationRef values")
        object.__setattr__(
            self, "claim_boundary", _normalize_claim_boundary(self.claim_boundary)
        )
        evidence_class = (self.evidence_class or "").strip().upper()
        if evidence_class not in EVIDENCE_CLASSES:
            allowed = sorted(k for k in EVIDENCE_CLASSES if k)
            raise ValueError(f"evidence_class must be one of {allowed} or empty")
        object.__setattr__(self, "evidence_class", evidence_class)
        object.__setattr__(self, "runtime_a", _freeze_mapping(self.runtime_a))
        object.__setattr__(self, "experience", _freeze_mapping(self.experience))
        object.__setattr__(self, "strategy", _freeze_mapping(self.strategy))
        object.__setattr__(self, "adaptive", _freeze_mapping(self.adaptive))
        object.__setattr__(self, "twin", _freeze_mapping(self.twin))
        object.__setattr__(
            self, "payload_summary", _freeze_mapping(self.payload_summary)
        )
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adaptive": dict(self.adaptive),
            "as_of": self.as_of,
            "claim_boundary": self.claim_boundary,
            "evidence_class": self.evidence_class,
            "event_type": self.event_type,
            "experience": dict(self.experience),
            "ingested_at": self.ingested_at,
            "limitations": list(self.limitations),
            "observed_at": self.observed_at,
            "payload_summary": dict(self.payload_summary),
            "runtime_a": dict(self.runtime_a),
            "source_refs": [ref.to_canonical_dict() for ref in self.source_refs],
            "strategy": dict(self.strategy),
            "student_id": self.student_id,
            "twin": dict(self.twin),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EvidenceRecord:
    """Immutable observational EvidenceRecord (E0/E1 contract).

    Logical counterpart to EvidenceItem in EVIDENCE_MODEL.md. Observational
    only — never educational source of truth. E1 collection preserves
    observation and ingestion timestamps without interpretation or scoring.
    """

    evidence_id: str = ""
    evidence_version: str = EVIDENCE_VERSION_E1
    student_id: str = ""
    source_refs: tuple[ObservationRef, ...] = ()
    evidence_class: str = ""
    event_type: str = ""
    claim_boundary: str = ""
    quality: EvidenceQuality = field(default_factory=EvidenceQuality)
    payload_summary: Mapping[str, Any] = field(default_factory=dict)
    provenance: Mapping[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()
    engine_version: str = EVIDENCE_VERSION_E1
    observed_at: str | None = None
    ingested_at: str | None = None
    as_of: str | None = None
    authority: str = AUTHORITY_EVIDENCE_PLATFORM
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(self, "event_type", (self.event_type or "").strip())
        object.__setattr__(self, "source_refs", tuple(self.source_refs or ()))
        for ref in self.source_refs:
            if not isinstance(ref, ObservationRef):
                raise TypeError("source_refs must contain ObservationRef values")
        evidence_class = (self.evidence_class or "").strip().upper()
        if evidence_class not in EVIDENCE_CLASSES:
            allowed = sorted(k for k in EVIDENCE_CLASSES if k)
            raise ValueError(f"evidence_class must be one of {allowed} or empty")
        object.__setattr__(self, "evidence_class", evidence_class)
        object.__setattr__(
            self, "claim_boundary", _normalize_claim_boundary(self.claim_boundary)
        )
        if not isinstance(self.quality, EvidenceQuality):
            raise TypeError("quality must be an EvidenceQuality")
        object.__setattr__(
            self, "payload_summary", _freeze_mapping(self.payload_summary)
        )
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)
        for label, value in (
            ("observed_at", self.observed_at),
            ("ingested_at", self.ingested_at),
            ("as_of", self.as_of),
        ):
            if value is not None and not isinstance(value, str):
                raise TypeError(f"{label} must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "authority": self.authority,
            "availability": self.availability,
            "claim_boundary": self.claim_boundary,
            "engine_version": self.engine_version,
            "event_type": self.event_type,
            "evidence_class": self.evidence_class,
            "evidence_id": self.evidence_id,
            "evidence_version": self.evidence_version,
            "ingested_at": self.ingested_at,
            "limitations": list(self.limitations),
            "observed_at": self.observed_at,
            "payload_summary": dict(self.payload_summary),
            "provenance": dict(self.provenance),
            "quality": self.quality.to_canonical_dict(),
            "source_refs": [ref.to_canonical_dict() for ref in self.source_refs],
            "student_id": self.student_id,
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ExperimentArm:
    """One experiment arm (flag-mediated; Evidence Platform never owns serve)."""

    arm_id: str = ""
    label: str = ""
    exposure: str = ""
    upstream_flag_snapshot: Mapping[str, Any] = field(default_factory=dict)
    forbidden_writes: tuple[str, ...] = ()
    notes: str = ""

    def __post_init__(self) -> None:
        exposure = (self.exposure or "").strip().lower()
        if exposure not in EXPOSURE_MODES:
            allowed = sorted(k for k in EXPOSURE_MODES if k)
            raise ValueError(f"exposure must be one of {allowed} or empty")
        object.__setattr__(self, "exposure", exposure)
        object.__setattr__(
            self,
            "upstream_flag_snapshot",
            _freeze_mapping(self.upstream_flag_snapshot),
        )
        object.__setattr__(
            self, "forbidden_writes", _freeze_str_tuple(self.forbidden_writes)
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "arm_id": self.arm_id,
            "exposure": self.exposure,
            "forbidden_writes": list(self.forbidden_writes),
            "label": self.label,
            "notes": self.notes,
            "upstream_flag_snapshot": dict(self.upstream_flag_snapshot),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ExperimentDefinition:
    """Immutable experiment protocol definition (E0 contract).

    Logical counterpart to ExperimentProtocol in EXPERIMENT_FRAMEWORK.md.
    Structure only — no assignment or measurement execution in E0.
    """

    experiment_id: str = ""
    definition_version: str = EVIDENCE_VERSION_E0
    title: str = ""
    hypothesis: str = ""
    policy_id: str = ""
    baseline_policy_version: str = ""
    treatment_policy_version: str = ""
    arms: tuple[ExperimentArm, ...] = ()
    eligibility: Mapping[str, Any] = field(default_factory=dict)
    assignment_mechanism: str = ""
    primary_outcomes: tuple[str, ...] = ()
    secondary_outcomes: tuple[str, ...] = ()
    guardrail_outcomes: tuple[str, ...] = ()
    window: Mapping[str, Any] = field(default_factory=dict)
    pre_registration: str = ""
    statistical_plan: Mapping[str, Any] = field(default_factory=dict)
    educational_rationale: Mapping[str, Any] = field(default_factory=dict)
    rollback_map: Mapping[str, Any] = field(default_factory=dict)
    status: str = ""
    limitations: tuple[str, ...] = ()
    authority: str = AUTHORITY_EVIDENCE_PLATFORM

    def __post_init__(self) -> None:
        object.__setattr__(self, "arms", tuple(self.arms or ()))
        for arm in self.arms:
            if not isinstance(arm, ExperimentArm):
                raise TypeError("arms must contain ExperimentArm values")
        status = (self.status or "").strip().lower()
        if status not in EXPERIMENT_STATUSES:
            allowed = sorted(k for k in EXPERIMENT_STATUSES if k)
            raise ValueError(f"status must be one of {allowed} or empty")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "eligibility", _freeze_mapping(self.eligibility))
        object.__setattr__(
            self, "primary_outcomes", _freeze_str_tuple(self.primary_outcomes)
        )
        object.__setattr__(
            self, "secondary_outcomes", _freeze_str_tuple(self.secondary_outcomes)
        )
        object.__setattr__(
            self, "guardrail_outcomes", _freeze_str_tuple(self.guardrail_outcomes)
        )
        object.__setattr__(self, "window", _freeze_mapping(self.window))
        object.__setattr__(
            self, "statistical_plan", _freeze_mapping(self.statistical_plan)
        )
        object.__setattr__(
            self,
            "educational_rationale",
            _freeze_mapping(self.educational_rationale),
        )
        object.__setattr__(self, "rollback_map", _freeze_mapping(self.rollback_map))
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        mechanism = (self.assignment_mechanism or "").strip().lower()
        if mechanism not in ASSIGNMENT_MECHANISMS:
            allowed = sorted(k for k in ASSIGNMENT_MECHANISMS if k)
            raise ValueError(
                f"assignment_mechanism must be one of {allowed} or empty"
            )
        object.__setattr__(self, "assignment_mechanism", mechanism)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "arms": [arm.to_canonical_dict() for arm in self.arms],
            "assignment_mechanism": self.assignment_mechanism,
            "authority": self.authority,
            "baseline_policy_version": self.baseline_policy_version,
            "definition_version": self.definition_version,
            "educational_rationale": dict(self.educational_rationale),
            "eligibility": dict(self.eligibility),
            "experiment_id": self.experiment_id,
            "guardrail_outcomes": list(self.guardrail_outcomes),
            "hypothesis": self.hypothesis,
            "limitations": list(self.limitations),
            "policy_id": self.policy_id,
            "pre_registration": self.pre_registration,
            "primary_outcomes": list(self.primary_outcomes),
            "rollback_map": dict(self.rollback_map),
            "secondary_outcomes": list(self.secondary_outcomes),
            "statistical_plan": dict(self.statistical_plan),
            "status": self.status,
            "title": self.title,
            "treatment_policy_version": self.treatment_policy_version,
            "window": dict(self.window),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ExperimentObservation:
    """Immutable experiment participation observation (E2).

    Records deterministic cohort assignment of a validated EvidenceRecord to a
    registered ExperimentDefinition. Observational only — no scoring, no
    winner declaration, no EvidenceRecord mutation, no educational behaviour
    change.
    """

    observation_id: str = ""
    observation_version: str = EVIDENCE_VERSION_E2
    experiment_id: str = ""
    experiment_version: str = ""
    arm_id: str = ""
    cohort: str = ""
    evidence_id: str = ""
    evidence_ref: Mapping[str, Any] = field(default_factory=dict)
    student_id: str = ""
    assignment_mechanism: str = ""
    assignment_rationale: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)
    observed_at: str | None = None
    authority: str = AUTHORITY_EVIDENCE_PLATFORM

    def __post_init__(self) -> None:
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(self, "experiment_id", (self.experiment_id or "").strip())
        object.__setattr__(
            self, "experiment_version", (self.experiment_version or "").strip()
        )
        object.__setattr__(self, "arm_id", (self.arm_id or "").strip())
        object.__setattr__(self, "cohort", (self.cohort or "").strip())
        object.__setattr__(self, "evidence_id", (self.evidence_id or "").strip())
        object.__setattr__(
            self, "observation_id", (self.observation_id or "").strip()
        )
        mechanism = (self.assignment_mechanism or "").strip().lower()
        if mechanism not in ASSIGNMENT_MECHANISMS:
            allowed = sorted(k for k in ASSIGNMENT_MECHANISMS if k)
            raise ValueError(
                f"assignment_mechanism must be one of {allowed} or empty"
            )
        object.__setattr__(self, "assignment_mechanism", mechanism)
        object.__setattr__(self, "evidence_ref", _freeze_mapping(self.evidence_ref))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))
        if self.observed_at is not None and not isinstance(self.observed_at, str):
            raise TypeError("observed_at must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "arm_id": self.arm_id,
            "assignment_mechanism": self.assignment_mechanism,
            "assignment_rationale": self.assignment_rationale,
            "authority": self.authority,
            "cohort": self.cohort,
            "evidence_id": self.evidence_id,
            "evidence_ref": dict(self.evidence_ref),
            "experiment_id": self.experiment_id,
            "experiment_version": self.experiment_version,
            "metadata": dict(self.metadata),
            "observation_id": self.observation_id,
            "observation_version": self.observation_version,
            "observed_at": self.observed_at,
            "student_id": self.student_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class OutcomeMetric:
    """Immutable typed outcome / analytics metric (E0 contract).

    Must carry a claim_boundary. Organisation metrics must never silently alias
    as learning_depth (EP-004 SP8).
    """

    metric_id: str = ""
    metric_version: str = EVIDENCE_VERSION_E0
    outcome_definition_id: str = ""
    claim_boundary: str = ""
    grain: str = ""
    value: str | int | float | None = None
    uncertainty: str = ""
    n: int | None = None
    subject_scope: str = ""
    evidence_bundle_id: str = ""
    limitations: tuple[str, ...] = ()
    filters: Mapping[str, Any] = field(default_factory=dict)
    authority: str = AUTHORITY_EVIDENCE_PLATFORM

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "claim_boundary", _normalize_claim_boundary(self.claim_boundary)
        )
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        object.__setattr__(self, "filters", _freeze_mapping(self.filters))
        if self.n is not None and not isinstance(self.n, int):
            raise TypeError("n must be an int or None")
        if self.value is not None and not isinstance(
            self.value, str | int | float
        ):
            raise TypeError("value must be a scalar string/number or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "claim_boundary": self.claim_boundary,
            "evidence_bundle_id": self.evidence_bundle_id,
            "filters": dict(self.filters),
            "grain": self.grain,
            "limitations": list(self.limitations),
            "metric_id": self.metric_id,
            "metric_version": self.metric_version,
            "n": self.n,
            "outcome_definition_id": self.outcome_definition_id,
            "subject_scope": self.subject_scope,
            "uncertainty": self.uncertainty,
            "value": self.value,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class AnalyticsExport:
    """Governance / research analytics export placeholder (E0).

    Forbidden audience: student_coaching. No aggregation behaviour in E0.
    """

    export_id: str = ""
    export_version: str = EVIDENCE_VERSION_E0
    audience: str = ""
    contents_ref: str = ""
    redaction_level: str = ""
    metric_ids: tuple[str, ...] = ()
    created_at: str | None = None
    limitations: tuple[str, ...] = ()
    authority: str = AUTHORITY_EVIDENCE_PLATFORM

    def __post_init__(self) -> None:
        audience = (self.audience or "").strip().lower()
        if audience not in ANALYTICS_AUDIENCES:
            allowed = sorted(k for k in ANALYTICS_AUDIENCES if k)
            raise ValueError(f"audience must be one of {allowed} or empty")
        if audience == "student_coaching":
            raise ValueError("student_coaching is a forbidden analytics audience")
        object.__setattr__(self, "audience", audience)
        object.__setattr__(self, "metric_ids", _freeze_str_tuple(self.metric_ids))
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        if self.created_at is not None and not isinstance(self.created_at, str):
            raise TypeError("created_at must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "audience": self.audience,
            "authority": self.authority,
            "contents_ref": self.contents_ref,
            "created_at": self.created_at,
            "export_id": self.export_id,
            "export_version": self.export_version,
            "limitations": list(self.limitations),
            "metric_ids": list(self.metric_ids),
            "redaction_level": self.redaction_level,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class PolicyDefinition:
    """Immutable registered educational policy definition (E3).

    Logical counterpart to EducationalPolicy / PolicyVersion in
    POLICY_EVALUATION.md. Evidence Platform records and evaluates policy
    versions; it does not own the upstream control plane that applies them.
    """

    policy_id: str = ""
    policy_version: str = ""
    definition_version: str = EVIDENCE_VERSION_E3
    title: str = ""
    intent: str = ""
    owner_layer: str = ""
    claim_boundary_intent: str = ""
    principles: tuple[str, ...] = ()
    sp_mapping: tuple[str, ...] = ()
    upstream_controls: Mapping[str, Any] = field(default_factory=dict)
    baseline_policy_version: str = ""
    experiment_ids: tuple[str, ...] = ()
    evaluation_kind: str = ""
    evaluation_eligibility: Mapping[str, Any] = field(default_factory=dict)
    educational_rationale: Mapping[str, Any] = field(default_factory=dict)
    statistical_plan: Mapping[str, Any] = field(default_factory=dict)
    status: str = ""
    limitations: tuple[str, ...] = ()
    spec_ref: str = ""
    authority: str = AUTHORITY_EVIDENCE_PLATFORM

    def __post_init__(self) -> None:
        object.__setattr__(self, "policy_id", (self.policy_id or "").strip())
        object.__setattr__(
            self, "policy_version", (self.policy_version or "").strip()
        )
        owner = (self.owner_layer or "").strip().lower()
        if owner not in POLICY_OWNER_LAYERS:
            allowed = sorted(k for k in POLICY_OWNER_LAYERS if k)
            raise ValueError(f"owner_layer must be one of {allowed} or empty")
        object.__setattr__(self, "owner_layer", owner)
        object.__setattr__(
            self,
            "claim_boundary_intent",
            _normalize_claim_boundary(self.claim_boundary_intent),
        )
        object.__setattr__(self, "principles", _freeze_str_tuple(self.principles))
        object.__setattr__(self, "sp_mapping", _freeze_str_tuple(self.sp_mapping))
        object.__setattr__(
            self, "upstream_controls", _freeze_mapping(self.upstream_controls)
        )
        object.__setattr__(
            self, "experiment_ids", _freeze_str_tuple(self.experiment_ids)
        )
        kind = (self.evaluation_kind or "").strip().lower()
        if kind not in EVALUATION_KINDS:
            allowed = sorted(k for k in EVALUATION_KINDS if k)
            raise ValueError(f"evaluation_kind must be one of {allowed} or empty")
        object.__setattr__(self, "evaluation_kind", kind)
        object.__setattr__(
            self,
            "evaluation_eligibility",
            _freeze_mapping(self.evaluation_eligibility),
        )
        object.__setattr__(
            self,
            "educational_rationale",
            _freeze_mapping(self.educational_rationale),
        )
        object.__setattr__(
            self, "statistical_plan", _freeze_mapping(self.statistical_plan)
        )
        status = (self.status or "").strip().lower()
        if status not in POLICY_STATUSES:
            allowed = sorted(k for k in POLICY_STATUSES if k)
            raise ValueError(f"status must be one of {allowed} or empty")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "baseline_policy_version": self.baseline_policy_version,
            "claim_boundary_intent": self.claim_boundary_intent,
            "definition_version": self.definition_version,
            "educational_rationale": dict(self.educational_rationale),
            "evaluation_eligibility": dict(self.evaluation_eligibility),
            "evaluation_kind": self.evaluation_kind,
            "experiment_ids": list(self.experiment_ids),
            "intent": self.intent,
            "limitations": list(self.limitations),
            "owner_layer": self.owner_layer,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "principles": list(self.principles),
            "sp_mapping": list(self.sp_mapping),
            "spec_ref": self.spec_ref,
            "statistical_plan": dict(self.statistical_plan),
            "status": self.status,
            "title": self.title,
            "upstream_controls": dict(self.upstream_controls),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class PolicyEvaluationExplanationPlaceholder:
    """Five-answer explainability bundle (structure; gate enforced in E3)."""

    evidence_considered: Mapping[str, Any] = field(default_factory=dict)
    statistical_basis: Mapping[str, Any] = field(default_factory=dict)
    educational_rationale: Mapping[str, Any] = field(default_factory=dict)
    policy_version: Mapping[str, Any] = field(default_factory=dict)
    confidence: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "evidence_considered",
            _freeze_mapping(self.evidence_considered),
        )
        object.__setattr__(
            self, "statistical_basis", _freeze_mapping(self.statistical_basis)
        )
        object.__setattr__(
            self,
            "educational_rationale",
            _freeze_mapping(self.educational_rationale),
        )
        object.__setattr__(
            self, "policy_version", _freeze_mapping(self.policy_version)
        )
        object.__setattr__(self, "confidence", _freeze_mapping(self.confidence))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "confidence": dict(self.confidence),
            "educational_rationale": dict(self.educational_rationale),
            "evidence_considered": dict(self.evidence_considered),
            "policy_version": dict(self.policy_version),
            "statistical_basis": dict(self.statistical_basis),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


# E3 public name for the five-answer explainability bundle.
PolicyEvaluationExplanationBundle = PolicyEvaluationExplanationPlaceholder


@dataclass(frozen=True)
class PolicyEvaluation:
    """Immutable policy evaluation artefact (E0/E3 contract).

    Logical counterpart to EvaluationRecord in POLICY_EVALUATION.md.
    Governance recommendation only — never student-facing decision authority.
    Never promotes policies or changes educational behaviour.
    """

    evaluation_id: str = ""
    evaluation_version: str = EVIDENCE_VERSION_E0
    policy_id: str = ""
    policy_version: str = ""
    baseline_policy_version: str = ""
    experiment_id: str = ""
    experiment_refs: tuple[str, ...] = ()
    evidence_bundle_ids: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    outcome_metrics: tuple[OutcomeMetric, ...] = ()
    statistical_summary: Mapping[str, Any] = field(default_factory=dict)
    explanation: PolicyEvaluationExplanationPlaceholder = field(
        default_factory=PolicyEvaluationExplanationPlaceholder
    )
    gate_result: str = ""
    gate_codes: tuple[str, ...] = ()
    recommendation: str = ""
    limitations: tuple[str, ...] = ()
    confidence_band: str = ""
    confidence_rationale: str = ""
    provenance: Mapping[str, Any] = field(default_factory=dict)
    created_at: str | None = None
    engine_version: str = EVIDENCE_VERSION_E0
    authority: str = AUTHORITY_EVIDENCE_PLATFORM

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "evidence_bundle_ids",
            _freeze_str_tuple(self.evidence_bundle_ids),
        )
        object.__setattr__(
            self, "experiment_refs", _freeze_str_tuple(self.experiment_refs)
        )
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )
        object.__setattr__(
            self, "outcome_metrics", tuple(self.outcome_metrics or ())
        )
        for metric in self.outcome_metrics:
            if not isinstance(metric, OutcomeMetric):
                raise TypeError("outcome_metrics must contain OutcomeMetric values")
        object.__setattr__(
            self,
            "statistical_summary",
            _freeze_mapping(self.statistical_summary),
        )
        if not isinstance(self.explanation, PolicyEvaluationExplanationPlaceholder):
            raise TypeError(
                "explanation must be a PolicyEvaluationExplanationPlaceholder"
            )
        gate = (self.gate_result or "").strip().lower()
        if gate not in GATE_RESULTS:
            allowed = sorted(k for k in GATE_RESULTS if k)
            raise ValueError(f"gate_result must be one of {allowed} or empty")
        object.__setattr__(self, "gate_result", gate)
        object.__setattr__(self, "gate_codes", _freeze_str_tuple(self.gate_codes))
        recommendation = (self.recommendation or "").strip().lower()
        if recommendation not in EVALUATION_RECOMMENDATIONS:
            allowed = sorted(k for k in EVALUATION_RECOMMENDATIONS if k)
            raise ValueError(f"recommendation must be one of {allowed} or empty")
        object.__setattr__(self, "recommendation", recommendation)
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        band = (self.confidence_band or "").strip().lower()
        if band not in CONFIDENCE_BANDS:
            allowed = sorted(k for k in CONFIDENCE_BANDS if k)
            raise ValueError(f"confidence_band must be one of {allowed} or empty")
        object.__setattr__(self, "confidence_band", band)
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        if self.created_at is not None and not isinstance(self.created_at, str):
            raise TypeError("created_at must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "baseline_policy_version": self.baseline_policy_version,
            "confidence_band": self.confidence_band,
            "confidence_rationale": self.confidence_rationale,
            "created_at": self.created_at,
            "engine_version": self.engine_version,
            "evaluation_id": self.evaluation_id,
            "evaluation_version": self.evaluation_version,
            "evidence_bundle_ids": list(self.evidence_bundle_ids),
            "evidence_refs": list(self.evidence_refs),
            "experiment_id": self.experiment_id,
            "experiment_refs": list(self.experiment_refs),
            "explanation": self.explanation.to_canonical_dict(),
            "gate_codes": list(self.gate_codes),
            "gate_result": self.gate_result,
            "limitations": list(self.limitations),
            "outcome_metrics": [
                metric.to_canonical_dict() for metric in self.outcome_metrics
            ],
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "provenance": dict(self.provenance),
            "recommendation": self.recommendation,
            "statistical_summary": dict(self.statistical_summary),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class MetricPoint:
    """One deterministic point in a MetricSeries (OUTCOME_ANALYTICS §4.1)."""

    t: str = ""
    value: str | int | float | None = None
    n: int | None = None
    uncertainty: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "t", (self.t or "").strip())
        if self.n is not None and not isinstance(self.n, int):
            raise TypeError("n must be an int or None")
        if self.value is not None and not isinstance(
            self.value, str | int | float
        ):
            raise TypeError("value must be a scalar string/number or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "n": self.n,
            "t": self.t,
            "uncertainty": self.uncertainty,
            "value": self.value,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class MetricSeries:
    """Immutable metric series for governance analytics (E4)."""

    metric_id: str = ""
    metric_version: str = EVIDENCE_VERSION_E4
    outcome_definition_id: str = ""
    claim_boundary: str = ""
    grain: str = ""
    points: tuple[MetricPoint, ...] = ()
    filters: Mapping[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()
    authority: str = AUTHORITY_EVIDENCE_PLATFORM

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "claim_boundary", _normalize_claim_boundary(self.claim_boundary)
        )
        grain = (self.grain or "").strip().lower()
        if grain not in ANALYTICS_GRAINS:
            allowed = sorted(k for k in ANALYTICS_GRAINS if k)
            raise ValueError(f"grain must be one of {allowed} or empty")
        object.__setattr__(self, "grain", grain)
        object.__setattr__(self, "points", tuple(self.points or ()))
        for point in self.points:
            if not isinstance(point, MetricPoint):
                raise TypeError("points must contain MetricPoint values")
        object.__setattr__(self, "filters", _freeze_mapping(self.filters))
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "authority": self.authority,
            "claim_boundary": self.claim_boundary,
            "filters": dict(self.filters),
            "grain": self.grain,
            "limitations": list(self.limitations),
            "metric_id": self.metric_id,
            "metric_version": self.metric_version,
            "outcome_definition_id": self.outcome_definition_id,
            "points": [point.to_canonical_dict() for point in self.points],
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ScorecardSlice:
    """Governance-facing scorecard slice (OUTCOME_ANALYTICS §4.2)."""

    slice_id: str = ""
    period: Mapping[str, Any] = field(default_factory=dict)
    organisation_block: Mapping[str, Any] = field(default_factory=dict)
    learning_signal_block: Mapping[str, Any] = field(default_factory=dict)
    learning_depth_block: Mapping[str, Any] = field(default_factory=dict)
    guardrails_block: Mapping[str, Any] = field(default_factory=dict)
    narrative_constraints: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "period", _freeze_mapping(self.period))
        object.__setattr__(
            self, "organisation_block", _freeze_mapping(self.organisation_block)
        )
        object.__setattr__(
            self,
            "learning_signal_block",
            _freeze_mapping(self.learning_signal_block),
        )
        object.__setattr__(
            self,
            "learning_depth_block",
            _freeze_mapping(self.learning_depth_block),
        )
        object.__setattr__(
            self, "guardrails_block", _freeze_mapping(self.guardrails_block)
        )
        object.__setattr__(
            self,
            "narrative_constraints",
            _freeze_str_tuple(self.narrative_constraints),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "guardrails_block": dict(self.guardrails_block),
            "learning_depth_block": dict(self.learning_depth_block),
            "learning_signal_block": dict(self.learning_signal_block),
            "narrative_constraints": list(self.narrative_constraints),
            "organisation_block": dict(self.organisation_block),
            "period": dict(self.period),
            "slice_id": self.slice_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class PolicySummaryProjection:
    """Governance roll-up of one PolicyEvaluation (E4)."""

    policy_id: str = ""
    policy_version: str = ""
    evaluation_id: str = ""
    evaluation_kind: str = ""
    gate_result: str = ""
    recommendation: str = ""
    confidence_band: str = ""
    claim_boundary_intent: str = ""
    observation_count: int = 0
    experiment_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "claim_boundary_intent",
            _normalize_claim_boundary(self.claim_boundary_intent),
        )
        object.__setattr__(
            self, "experiment_refs", _freeze_str_tuple(self.experiment_refs)
        )
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        if not isinstance(self.observation_count, int):
            raise TypeError("observation_count must be an int")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "claim_boundary_intent": self.claim_boundary_intent,
            "confidence_band": self.confidence_band,
            "evaluation_id": self.evaluation_id,
            "evaluation_kind": self.evaluation_kind,
            "evidence_refs": list(self.evidence_refs),
            "experiment_refs": list(self.experiment_refs),
            "gate_result": self.gate_result,
            "limitations": list(self.limitations),
            "observation_count": self.observation_count,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "recommendation": self.recommendation,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ExperimentSummaryProjection:
    """Governance roll-up of experiment observations (E4)."""

    experiment_id: str = ""
    experiment_version: str = ""
    arm_distribution: Mapping[str, int] = field(default_factory=dict)
    observation_count: int = 0
    student_count: int = 0
    evidence_count: int = 0
    cohort_distribution: Mapping[str, int] = field(default_factory=dict)
    assignment_mechanisms: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "arm_distribution", _freeze_mapping(self.arm_distribution)
        )
        object.__setattr__(
            self,
            "cohort_distribution",
            _freeze_mapping(self.cohort_distribution),
        )
        object.__setattr__(
            self,
            "assignment_mechanisms",
            _freeze_str_tuple(self.assignment_mechanisms),
        )
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        for label, value in (
            ("observation_count", self.observation_count),
            ("student_count", self.student_count),
            ("evidence_count", self.evidence_count),
        ):
            if not isinstance(value, int):
                raise TypeError(f"{label} must be an int")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "arm_distribution": dict(self.arm_distribution),
            "assignment_mechanisms": list(self.assignment_mechanisms),
            "cohort_distribution": dict(self.cohort_distribution),
            "evidence_count": self.evidence_count,
            "experiment_id": self.experiment_id,
            "experiment_version": self.experiment_version,
            "limitations": list(self.limitations),
            "observation_count": self.observation_count,
            "student_count": self.student_count,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ConfidenceSummaryProjection:
    """Aggregate confidence / gate bands across evaluations (E4)."""

    bands: Mapping[str, int] = field(default_factory=dict)
    dominant_band: str = ""
    rationale_summary: str = ""
    evaluations_with_gate_passed: int = 0
    evaluations_with_gate_failed: int = 0
    evaluations_with_gate_ineligible: int = 0
    not_proven: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "bands", _freeze_mapping(self.bands))
        band = (self.dominant_band or "").strip().lower()
        if band not in CONFIDENCE_BANDS:
            allowed = sorted(k for k in CONFIDENCE_BANDS if k)
            raise ValueError(f"dominant_band must be one of {allowed} or empty")
        object.__setattr__(self, "dominant_band", band)
        object.__setattr__(self, "not_proven", _freeze_str_tuple(self.not_proven))
        for label, value in (
            ("evaluations_with_gate_passed", self.evaluations_with_gate_passed),
            ("evaluations_with_gate_failed", self.evaluations_with_gate_failed),
            (
                "evaluations_with_gate_ineligible",
                self.evaluations_with_gate_ineligible,
            ),
        ):
            if not isinstance(value, int):
                raise TypeError(f"{label} must be an int")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "bands": dict(self.bands),
            "dominant_band": self.dominant_band,
            "evaluations_with_gate_failed": self.evaluations_with_gate_failed,
            "evaluations_with_gate_ineligible": (
                self.evaluations_with_gate_ineligible
            ),
            "evaluations_with_gate_passed": self.evaluations_with_gate_passed,
            "not_proven": list(self.not_proven),
            "rationale_summary": self.rationale_summary,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class TrendMetadata:
    """Trend / comparability metadata for analytics exports (E4)."""

    grain: str = ""
    comparable: bool = False
    direction: str = ""
    prior_period_ref: str = ""
    delta_summary: Mapping[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        grain = (self.grain or "").strip().lower()
        if grain not in ANALYTICS_GRAINS:
            allowed = sorted(k for k in ANALYTICS_GRAINS if k)
            raise ValueError(f"grain must be one of {allowed} or empty")
        object.__setattr__(self, "grain", grain)
        direction = (self.direction or "").strip().lower()
        if direction not in TREND_DIRECTIONS:
            allowed = sorted(k for k in TREND_DIRECTIONS if k)
            raise ValueError(f"direction must be one of {allowed} or empty")
        object.__setattr__(self, "direction", direction)
        object.__setattr__(self, "delta_summary", _freeze_mapping(self.delta_summary))
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "comparable": bool(self.comparable),
            "delta_summary": dict(self.delta_summary),
            "direction": self.direction,
            "grain": self.grain,
            "limitations": list(self.limitations),
            "prior_period_ref": self.prior_period_ref,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class AnalyticsSummary:
    """Immutable analytics aggregate (E4).

    Observational roll-up of PolicyEvaluation / ExperimentObservation /
    EvidenceRecord inputs. Never mutates inputs, never promotes policy, never
    changes educational behaviour.
    """

    summary_id: str = ""
    summary_version: str = EVIDENCE_VERSION_E4
    engine_version: str = EVIDENCE_VERSION_E4
    as_of: str | None = None
    period: Mapping[str, Any] = field(default_factory=dict)
    audience: str = ANALYTICS_AUDIENCE_GOVERNANCE
    evidence_count: int = 0
    observation_count: int = 0
    evaluation_count: int = 0
    student_count: int = 0
    experiment_count: int = 0
    policy_summaries: tuple[PolicySummaryProjection, ...] = ()
    experiment_summaries: tuple[ExperimentSummaryProjection, ...] = ()
    confidence_summary: ConfidenceSummaryProjection = field(
        default_factory=ConfidenceSummaryProjection
    )
    metric_series: tuple[MetricSeries, ...] = ()
    scorecard_slice: ScorecardSlice | None = None
    trend_metadata: TrendMetadata = field(default_factory=TrendMetadata)
    claim_boundary_mix: Mapping[str, int] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()
    narrative_constraints: tuple[str, ...] = ()
    provenance: Mapping[str, Any] = field(default_factory=dict)
    evaluation_ids: tuple[str, ...] = ()
    experiment_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    contents_ref: str = ""
    authority: str = AUTHORITY_EVIDENCE_PLATFORM
    availability: str = AVAILABILITY_AVAILABLE
    unavailable_reason: str = ""

    def __post_init__(self) -> None:
        audience = (self.audience or "").strip().lower()
        if audience not in ANALYTICS_AUDIENCES:
            allowed = sorted(k for k in ANALYTICS_AUDIENCES if k)
            raise ValueError(f"audience must be one of {allowed} or empty")
        if audience == "student_coaching":
            raise ValueError("student_coaching is a forbidden analytics audience")
        object.__setattr__(self, "audience", audience)
        object.__setattr__(self, "period", _freeze_mapping(self.period))
        object.__setattr__(
            self, "policy_summaries", tuple(self.policy_summaries or ())
        )
        for item in self.policy_summaries:
            if not isinstance(item, PolicySummaryProjection):
                raise TypeError(
                    "policy_summaries must contain PolicySummaryProjection values"
                )
        object.__setattr__(
            self, "experiment_summaries", tuple(self.experiment_summaries or ())
        )
        for item in self.experiment_summaries:
            if not isinstance(item, ExperimentSummaryProjection):
                raise TypeError(
                    "experiment_summaries must contain "
                    "ExperimentSummaryProjection values"
                )
        if not isinstance(self.confidence_summary, ConfidenceSummaryProjection):
            raise TypeError(
                "confidence_summary must be a ConfidenceSummaryProjection"
            )
        object.__setattr__(self, "metric_series", tuple(self.metric_series or ()))
        for series in self.metric_series:
            if not isinstance(series, MetricSeries):
                raise TypeError("metric_series must contain MetricSeries values")
        if self.scorecard_slice is not None and not isinstance(
            self.scorecard_slice, ScorecardSlice
        ):
            raise TypeError("scorecard_slice must be a ScorecardSlice or None")
        if not isinstance(self.trend_metadata, TrendMetadata):
            raise TypeError("trend_metadata must be a TrendMetadata")
        object.__setattr__(
            self, "claim_boundary_mix", _freeze_mapping(self.claim_boundary_mix)
        )
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        object.__setattr__(
            self,
            "narrative_constraints",
            _freeze_str_tuple(self.narrative_constraints),
        )
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(
            self, "evaluation_ids", _freeze_str_tuple(self.evaluation_ids)
        )
        object.__setattr__(
            self, "experiment_refs", _freeze_str_tuple(self.experiment_refs)
        )
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)
        if self.as_of is not None and not isinstance(self.as_of, str):
            raise TypeError("as_of must be an ISO string or None")
        for label, value in (
            ("evidence_count", self.evidence_count),
            ("observation_count", self.observation_count),
            ("evaluation_count", self.evaluation_count),
            ("student_count", self.student_count),
            ("experiment_count", self.experiment_count),
        ):
            if not isinstance(value, int):
                raise TypeError(f"{label} must be an int")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "audience": self.audience,
            "authority": self.authority,
            "availability": self.availability,
            "claim_boundary_mix": dict(self.claim_boundary_mix),
            "confidence_summary": self.confidence_summary.to_canonical_dict(),
            "contents_ref": self.contents_ref,
            "engine_version": self.engine_version,
            "evaluation_count": self.evaluation_count,
            "evaluation_ids": list(self.evaluation_ids),
            "evidence_count": self.evidence_count,
            "evidence_refs": list(self.evidence_refs),
            "experiment_count": self.experiment_count,
            "experiment_refs": list(self.experiment_refs),
            "experiment_summaries": [
                item.to_canonical_dict() for item in self.experiment_summaries
            ],
            "limitations": list(self.limitations),
            "metric_series": [
                series.to_canonical_dict() for series in self.metric_series
            ],
            "narrative_constraints": list(self.narrative_constraints),
            "observation_count": self.observation_count,
            "period": dict(self.period),
            "policy_summaries": [
                item.to_canonical_dict() for item in self.policy_summaries
            ],
            "provenance": dict(self.provenance),
            "scorecard_slice": (
                None
                if self.scorecard_slice is None
                else self.scorecard_slice.to_canonical_dict()
            ),
            "student_count": self.student_count,
            "summary_id": self.summary_id,
            "summary_version": self.summary_version,
            "trend_metadata": self.trend_metadata.to_canonical_dict(),
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EvidenceProjectionProvenance:
    """Provenance for a governance EvidenceProjection (E4)."""

    summary_id: str = ""
    evaluation_ids: tuple[str, ...] = ()
    experiment_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    authority: str = AUTHORITY_EVIDENCE_PLATFORM
    as_of: str | None = None
    provenance_refs: tuple[str, ...] = ()
    source_services: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "evaluation_ids", _freeze_str_tuple(self.evaluation_ids)
        )
        object.__setattr__(
            self, "experiment_refs", _freeze_str_tuple(self.experiment_refs)
        )
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )
        object.__setattr__(
            self, "provenance_refs", _freeze_str_tuple(self.provenance_refs)
        )
        object.__setattr__(
            self, "source_services", _freeze_str_tuple(self.source_services)
        )
        if self.as_of is not None and not isinstance(self.as_of, str):
            raise TypeError("as_of must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "authority": self.authority,
            "evaluation_ids": list(self.evaluation_ids),
            "evidence_refs": list(self.evidence_refs),
            "experiment_refs": list(self.experiment_refs),
            "provenance_refs": list(self.provenance_refs),
            "source_services": list(self.source_services),
            "summary_id": self.summary_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EvidenceProjection:
    """Immutable governance-facing Evidence Platform projection (E4).

    Read-only presentation of AnalyticsSummary. Never educational authority.
    Forbidden audience: student_coaching.
    """

    projection_id: str = ""
    summary_id: str = ""
    as_of: str | None = None
    projection_version: str = EVIDENCE_VERSION_E4
    authority: str = AUTHORITY_EVIDENCE_PLATFORM
    audience: str = ANALYTICS_AUDIENCE_GOVERNANCE
    availability: str = AVAILABILITY_AVAILABLE
    unavailable_reason: str = ""
    limitations_codes: tuple[str, ...] = ()
    headline: str = ""
    policy_summaries: tuple[PolicySummaryProjection, ...] = ()
    experiment_summaries: tuple[ExperimentSummaryProjection, ...] = ()
    evidence_counts: Mapping[str, int] = field(default_factory=dict)
    confidence_summary: ConfidenceSummaryProjection = field(
        default_factory=ConfidenceSummaryProjection
    )
    metric_series: tuple[MetricSeries, ...] = ()
    scorecard_slice: ScorecardSlice | None = None
    trend_metadata: TrendMetadata = field(default_factory=TrendMetadata)
    export_ref: str = ""
    redaction_level: str = ""
    provenance: EvidenceProjectionProvenance = field(
        default_factory=EvidenceProjectionProvenance
    )

    def __post_init__(self) -> None:
        audience = (self.audience or "").strip().lower()
        if audience not in ANALYTICS_AUDIENCES:
            allowed = sorted(k for k in ANALYTICS_AUDIENCES if k)
            raise ValueError(f"audience must be one of {allowed} or empty")
        if audience == "student_coaching":
            raise ValueError("student_coaching is a forbidden analytics audience")
        object.__setattr__(self, "audience", audience)
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)
        object.__setattr__(
            self, "limitations_codes", _freeze_str_tuple(self.limitations_codes)
        )
        object.__setattr__(
            self, "policy_summaries", tuple(self.policy_summaries or ())
        )
        for item in self.policy_summaries:
            if not isinstance(item, PolicySummaryProjection):
                raise TypeError(
                    "policy_summaries must contain PolicySummaryProjection values"
                )
        object.__setattr__(
            self, "experiment_summaries", tuple(self.experiment_summaries or ())
        )
        for item in self.experiment_summaries:
            if not isinstance(item, ExperimentSummaryProjection):
                raise TypeError(
                    "experiment_summaries must contain "
                    "ExperimentSummaryProjection values"
                )
        object.__setattr__(
            self, "evidence_counts", _freeze_mapping(self.evidence_counts)
        )
        if not isinstance(self.confidence_summary, ConfidenceSummaryProjection):
            raise TypeError(
                "confidence_summary must be a ConfidenceSummaryProjection"
            )
        object.__setattr__(self, "metric_series", tuple(self.metric_series or ()))
        for series in self.metric_series:
            if not isinstance(series, MetricSeries):
                raise TypeError("metric_series must contain MetricSeries values")
        if self.scorecard_slice is not None and not isinstance(
            self.scorecard_slice, ScorecardSlice
        ):
            raise TypeError("scorecard_slice must be a ScorecardSlice or None")
        if not isinstance(self.trend_metadata, TrendMetadata):
            raise TypeError("trend_metadata must be a TrendMetadata")
        if not isinstance(self.provenance, EvidenceProjectionProvenance):
            raise TypeError("provenance must be an EvidenceProjectionProvenance")
        if self.as_of is not None and not isinstance(self.as_of, str):
            raise TypeError("as_of must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "audience": self.audience,
            "authority": self.authority,
            "availability": self.availability,
            "confidence_summary": self.confidence_summary.to_canonical_dict(),
            "evidence_counts": dict(self.evidence_counts),
            "experiment_summaries": [
                item.to_canonical_dict() for item in self.experiment_summaries
            ],
            "export_ref": self.export_ref,
            "headline": self.headline,
            "limitations_codes": list(self.limitations_codes),
            "metric_series": [
                series.to_canonical_dict() for series in self.metric_series
            ],
            "policy_summaries": [
                item.to_canonical_dict() for item in self.policy_summaries
            ],
            "projection_id": self.projection_id,
            "projection_version": self.projection_version,
            "provenance": self.provenance.to_canonical_dict(),
            "redaction_level": self.redaction_level,
            "scorecard_slice": (
                None
                if self.scorecard_slice is None
                else self.scorecard_slice.to_canonical_dict()
            ),
            "summary_id": self.summary_id,
            "trend_metadata": self.trend_metadata.to_canonical_dict(),
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EvidenceProjectionResult:
    """Result envelope for EvidenceProjectionPort calls."""

    ok: bool
    value: EvidenceProjection | AnalyticsSummary | AnalyticsExport | None = None
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


EVIDENCE_VERSION_ADVISORY = "p2.ms009.1"


@dataclass(frozen=True)
class EvidenceFactualSummary:
    """Immutable student-facing factual observation roll-up (P2-MS008).

    Counts previously observed delivery/event facts only. Never scores,
    predictions, mastery, recommendations, or educational interpretation.
    Consumed by Experience Feedback via EvidenceReadPort only.
    """

    summary_id: str = ""
    student_id: str = ""
    reporting_period: str = "this_week"
    completed_missions: int = 0
    completed_reflections: int = 0
    study_sessions: int = 0
    active_streak: int = 0
    generated_at: str | None = None
    evidence_refs: tuple[str, ...] = ()
    event_counts: Mapping[str, int] = field(default_factory=dict)
    provenance: Mapping[str, Any] = field(default_factory=dict)
    source_description: str = (
        "Based on your recorded study activity."
    )
    authority: str = AUTHORITY_EVIDENCE_PLATFORM
    availability: str = AVAILABILITY_AVAILABLE
    unavailable_reason: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary_id", (self.summary_id or "").strip())
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self,
            "reporting_period",
            (self.reporting_period or "this_week").strip().lower() or "this_week",
        )
        for label, value in (
            ("completed_missions", self.completed_missions),
            ("completed_reflections", self.completed_reflections),
            ("study_sessions", self.study_sessions),
            ("active_streak", self.active_streak),
        ):
            if not isinstance(value, int):
                raise TypeError(f"{label} must be an int")
            if value < 0:
                raise ValueError(f"{label} must be >= 0")
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )
        object.__setattr__(self, "event_counts", _freeze_mapping(self.event_counts))
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(
            self,
            "source_description",
            (self.source_description or "").strip()
            or "Based on your recorded study activity.",
        )
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)
        object.__setattr__(
            self, "authority", (self.authority or AUTHORITY_EVIDENCE_PLATFORM).strip()
        )
        object.__setattr__(
            self, "unavailable_reason", (self.unavailable_reason or "").strip()
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "active_streak": self.active_streak,
            "authority": self.authority,
            "availability": self.availability,
            "completed_missions": self.completed_missions,
            "completed_reflections": self.completed_reflections,
            "evidence_refs": list(self.evidence_refs),
            "event_counts": dict(self.event_counts),
            "generated_at": self.generated_at,
            "provenance": dict(self.provenance),
            "reporting_period": self.reporting_period,
            "source_description": self.source_description,
            "student_id": self.student_id,
            "study_sessions": self.study_sessions,
            "summary_id": self.summary_id,
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ObservedPattern:
    """One factual observation pattern for EvidenceAdvisory (P2-MS009).

    Describes what was recorded — never what the student should do next.
    """

    pattern_key: str = ""
    observation: str = ""
    count: int = 0
    evidence_refs: tuple[str, ...] = ()
    source_description: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "pattern_key", (self.pattern_key or "").strip())
        object.__setattr__(self, "observation", (self.observation or "").strip())
        if not isinstance(self.count, int):
            raise TypeError("count must be an int")
        if self.count < 0:
            raise ValueError("count must be >= 0")
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )
        object.__setattr__(
            self, "source_description", (self.source_description or "").strip()
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "count": self.count,
            "evidence_refs": list(self.evidence_refs),
            "observation": self.observation,
            "pattern_key": self.pattern_key,
            "source_description": self.source_description,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EngagementSummary:
    """Factual engagement tallies for EvidenceAdvisory (P2-MS009)."""

    completed_missions: int = 0
    study_sessions: int = 0
    completed_reflections: int = 0
    event_counts: Mapping[str, int] = field(default_factory=dict)
    source_description: str = ""

    def __post_init__(self) -> None:
        for label, value in (
            ("completed_missions", self.completed_missions),
            ("study_sessions", self.study_sessions),
            ("completed_reflections", self.completed_reflections),
        ):
            if not isinstance(value, int):
                raise TypeError(f"{label} must be an int")
            if value < 0:
                raise ValueError(f"{label} must be >= 0")
        object.__setattr__(self, "event_counts", _freeze_mapping(self.event_counts))
        object.__setattr__(
            self, "source_description", (self.source_description or "").strip()
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "completed_missions": self.completed_missions,
            "completed_reflections": self.completed_reflections,
            "event_counts": dict(self.event_counts),
            "source_description": self.source_description,
            "study_sessions": self.study_sessions,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ConsistencySummary:
    """Factual consistency tallies for EvidenceAdvisory (P2-MS009)."""

    active_streak: int = 0
    source_description: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.active_streak, int):
            raise TypeError("active_streak must be an int")
        if self.active_streak < 0:
            raise ValueError("active_streak must be >= 0")
        object.__setattr__(
            self, "source_description", (self.source_description or "").strip()
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "active_streak": self.active_streak,
            "source_description": self.source_description,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class FactualConstraint:
    """One factual constraint derived from observations (P2-MS009).

    Constraints describe recorded absences / window limits only — never
    recommendations, predictions, or inferred mastery.
    """

    constraint_key: str = ""
    statement: str = ""
    source_description: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "constraint_key", (self.constraint_key or "").strip()
        )
        object.__setattr__(self, "statement", (self.statement or "").strip())
        object.__setattr__(
            self, "source_description", (self.source_description or "").strip()
        )
        if not self.constraint_key:
            raise ValueError("constraint_key is required")
        if not self.statement:
            raise ValueError("statement is required")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "constraint_key": self.constraint_key,
            "source_description": self.source_description,
            "statement": self.statement,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EvidenceAdvisory:
    """Immutable advisory inputs for Runtime A (P2-MS009).

    Factual, explainable observations only. Evidence answers "what has been
    observed?" — never "what should the student do next?". No predictions,
    recommendations, scoring, or inferred mastery.
    """

    advisory_id: str = ""
    reporting_period: str = "this_week"
    observed_patterns: tuple[ObservedPattern, ...] = ()
    engagement_summary: EngagementSummary = field(
        default_factory=EngagementSummary
    )
    consistency_summary: ConsistencySummary = field(
        default_factory=ConsistencySummary
    )
    factual_constraints: tuple[FactualConstraint, ...] = ()
    provenance: Mapping[str, Any] = field(default_factory=dict)
    generated_at: str | None = None
    student_id: str = ""
    evidence_summary_id: str = ""
    evidence_refs: tuple[str, ...] = ()
    source_description: str = (
        "Derived from recorded study activity."
    )
    authority: str = AUTHORITY_EVIDENCE_PLATFORM
    availability: str = AVAILABILITY_AVAILABLE
    unavailable_reason: str = ""
    advisory_version: str = EVIDENCE_VERSION_ADVISORY

    def __post_init__(self) -> None:
        object.__setattr__(self, "advisory_id", (self.advisory_id or "").strip())
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self,
            "reporting_period",
            (self.reporting_period or "this_week").strip().lower() or "this_week",
        )
        object.__setattr__(
            self, "observed_patterns", tuple(self.observed_patterns or ())
        )
        for pattern in self.observed_patterns:
            if not isinstance(pattern, ObservedPattern):
                raise TypeError(
                    "observed_patterns must contain ObservedPattern values"
                )
        if not isinstance(self.engagement_summary, EngagementSummary):
            raise TypeError("engagement_summary must be an EngagementSummary")
        if not isinstance(self.consistency_summary, ConsistencySummary):
            raise TypeError("consistency_summary must be a ConsistencySummary")
        object.__setattr__(
            self, "factual_constraints", tuple(self.factual_constraints or ())
        )
        for constraint in self.factual_constraints:
            if not isinstance(constraint, FactualConstraint):
                raise TypeError(
                    "factual_constraints must contain FactualConstraint values"
                )
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        if self.generated_at is not None and not isinstance(self.generated_at, str):
            raise TypeError("generated_at must be an ISO string or None")
        object.__setattr__(
            self, "evidence_summary_id", (self.evidence_summary_id or "").strip()
        )
        object.__setattr__(
            self, "evidence_refs", _freeze_str_tuple(self.evidence_refs)
        )
        object.__setattr__(
            self,
            "source_description",
            (self.source_description or "").strip()
            or "Derived from recorded study activity.",
        )
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)
        object.__setattr__(
            self, "authority", (self.authority or AUTHORITY_EVIDENCE_PLATFORM).strip()
        )
        object.__setattr__(
            self, "unavailable_reason", (self.unavailable_reason or "").strip()
        )
        object.__setattr__(
            self,
            "advisory_version",
            (self.advisory_version or EVIDENCE_VERSION_ADVISORY).strip(),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_id": self.advisory_id,
            "advisory_version": self.advisory_version,
            "authority": self.authority,
            "availability": self.availability,
            "consistency_summary": self.consistency_summary.to_canonical_dict(),
            "engagement_summary": self.engagement_summary.to_canonical_dict(),
            "evidence_refs": list(self.evidence_refs),
            "evidence_summary_id": self.evidence_summary_id,
            "factual_constraints": [
                item.to_canonical_dict() for item in self.factual_constraints
            ],
            "generated_at": self.generated_at,
            "observed_patterns": [
                item.to_canonical_dict() for item in self.observed_patterns
            ],
            "provenance": dict(self.provenance),
            "reporting_period": self.reporting_period,
            "source_description": self.source_description,
            "student_id": self.student_id,
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EvidenceResult:
    """Result envelope for Evidence Adapter calls."""

    ok: bool
    value: (
        EvidenceRecord
        | ExperimentObservation
        | PolicyEvaluation
        | AnalyticsSummary
        | EvidenceProjection
        | AnalyticsExport
        | EvidenceFactualSummary
        | EvidenceAdvisory
        | None
    ) = None
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
class LearningEvidenceContract(Protocol):
    """Pure Learning Evidence contract — context in, EvidenceRecord out.

    Implementations must be deterministic for identical EvidenceContext material
    fields. Must not write Runtime A, Twin, Adaptive, Strategy, or Experience
    educational state. E1 performs observational intake only.
    """

    def observe(self, context: EvidenceContext) -> EvidenceRecord:
        """Project an EvidenceContext into an EvidenceRecord."""


@runtime_checkable
class EvidenceAdapter(Protocol):
    """Adapter interface for the Learning Evidence Platform.

    Read-only relative to educational history. Must not call Planning write
    APIs, Evidence acceptance, TopicProgress writes, mission mutations, Twin
    synthesis, Adaptive re-ranking, or Strategy orchestration writes.
    """

    @property
    def adapter_id(self) -> str:
        """Stable Evidence Platform Adapter identity."""

    def assemble_record(
        self,
        student_id: str,
        *,
        context: EvidenceContext | None = None,
        as_of: str | None = None,
        mode: str = "collection",
    ) -> EvidenceResult:
        """Produce an EvidenceRecord behind the Learning Evidence contract."""


@runtime_checkable
class EvidenceProjectionPort(Protocol):
    """Read-only governance projection port for Evidence Platform analytics (E4).

    Must not write Runtime A, Twin, Adaptive, Strategy, or Experience state.
    Must not promote policies or serve student coaching surfaces.
    """

    @property
    def port_id(self) -> str:
        """Stable EvidenceProjectionPort identity."""

    def is_available(self) -> bool:
        """Whether the projection port is enabled and wired."""

    def project_summary(
        self,
        summary: AnalyticsSummary,
        *,
        audience: str = ANALYTICS_AUDIENCE_GOVERNANCE,
        as_of: str | None = None,
    ) -> EvidenceProjection:
        """Project an AnalyticsSummary into an EvidenceProjection."""

    def get_projection(self, summary_id: str) -> EvidenceProjection | None:
        """Return a previously bound projection by summary_id, if any."""

    def get_governance_export(
        self, summary_id: str
    ) -> EvidenceProjectionResult:
        """Return a governance-facing export envelope for a bound projection."""


@runtime_checkable
class EvidenceReadPort(Protocol):
    """Public Evidence query/read surface for factual observation summaries.

    Experience Feedback (P2-MS008) must use this contract only — no repository
    / collector / aggregator bypass. Returns non-interpretive counts only.
    Must not write Runtime A, Twin, Adaptive, Strategy, or Experience state.
    Must not score, predict, or serve educational recommendations.
    """

    def query_factual_summary(
        self,
        student_id: str,
        *,
        reporting_period: str = "this_week",
        as_of: str | None = None,
        evidence_records: Sequence[EvidenceRecord] | None = None,
    ) -> EvidenceResult:
        """Return an EvidenceFactualSummary for the student (or error envelope)."""


@runtime_checkable
class EvidenceAdvisoryPort(Protocol):
    """Public Evidence advisory read surface for Runtime A (P2-MS009).

    Runtime A consumes this contract only — no repository / collector /
    aggregator bypass. Returns factual, explainable advisory inputs only.
    Must not write Runtime A, Twin, Adaptive, Strategy, or Experience state.
    Must not score, predict, recommend, or infer mastery.
    """

    @property
    def port_id(self) -> str:
        """Stable EvidenceAdvisoryPort identity."""

    def is_available(self) -> bool:
        """Whether the advisory port is enabled and wired."""

    def query_advisory(
        self,
        student_id: str,
        *,
        reporting_period: str = "this_week",
        as_of: str | None = None,
        evidence_records: Sequence[EvidenceRecord] | None = None,
    ) -> EvidenceResult:
        """Return an EvidenceAdvisory for the student (or error envelope)."""
