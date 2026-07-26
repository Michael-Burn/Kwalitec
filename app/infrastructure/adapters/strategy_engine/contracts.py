"""Learning Strategy contracts (MS-005 S0 / S1 / S2).

Immutable DTOs and Protocol interfaces. S0 defines LearningIntervention /
InterventionStep / StrategyContext contracts and the StrategyAdapter surface.
S1 adds intervention advice components and StrategyContext input payloads for
core orchestration. S2 adds StrategyExplanationBundle explainability DTOs and
Experience-facing StrategyProjection DTOs. No Experience authority cutover,
Runtime A / Twin / Adaptive mutation, shadow validation, or educational writes.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date, datetime
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable

# Shared failure codes (STRATEGY_INTERFACE_SPECIFICATION.md).
UNAVAILABLE = "UNAVAILABLE"
NO_ACTIVE_PLAN = "NO_ACTIVE_PLAN"
NOT_FOUND = "NOT_FOUND"
FORBIDDEN = "FORBIDDEN"
INVALID_STATE = "INVALID_STATE"
STRATEGY_EXPLAINABILITY_INCOMPLETE = "STRATEGY_EXPLAINABILITY_INCOMPLETE"
STRATEGY_INPUT_UNAVAILABLE = "STRATEGY_INPUT_UNAVAILABLE"
BEHAVIOUR_MISMATCH = "BEHAVIOUR_MISMATCH"

STRATEGY_ERROR_CODES = frozenset(
    {
        UNAVAILABLE,
        NO_ACTIVE_PLAN,
        NOT_FOUND,
        FORBIDDEN,
        INVALID_STATE,
        STRATEGY_EXPLAINABILITY_INCOMPLETE,
        STRATEGY_INPUT_UNAVAILABLE,
        BEHAVIOUR_MISMATCH,
    }
)

AUTHORITY_STRATEGY_ENGINE = "strategy_engine"
AUTHORITY_RUNTIME_A = "runtime_a"
AUTHORITY_ADAPTIVE_ENGINE = "adaptive_engine"
AUTHORITY_DIGITAL_TWIN = "digital_twin"

KIND_STUDY_PLAN = "STUDY_PLAN"
KIND_SESSION_PLAN = "SESSION_PLAN"
KIND_REVISION_PLAN = "REVISION_PLAN"
KIND_RECOVERY_PLAN = "RECOVERY_PLAN"
KIND_FATIGUE_MANAGEMENT = "FATIGUE_MANAGEMENT"
KIND_CONFIDENCE_INTERVENTION = "CONFIDENCE_INTERVENTION"
KIND_CONTINUE = "CONTINUE"
KIND_BREAK = "BREAK"
KIND_ASSESS = "ASSESS"

INTERVENTION_KINDS = frozenset(
    {
        KIND_STUDY_PLAN,
        KIND_SESSION_PLAN,
        KIND_REVISION_PLAN,
        KIND_RECOVERY_PLAN,
        KIND_FATIGUE_MANAGEMENT,
        KIND_CONFIDENCE_INTERVENTION,
        KIND_CONTINUE,
        KIND_BREAK,
        KIND_ASSESS,
        "",
    }
)

AVAILABILITY_AVAILABLE = "available"
AVAILABILITY_UNAVAILABLE = "unavailable"
AVAILABILITY_VALUES = frozenset(
    {AVAILABILITY_AVAILABLE, AVAILABILITY_UNAVAILABLE, ""}
)

PROVENANCE_KINDS = frozenset(
    {
        "fact",
        "runtime_a_derived",
        "twin_derived",
        "adaptive_derived",
        "strategy_derived",
        "",
    }
)

STRATEGY_VERSION_S0 = "s0.1"
STRATEGY_VERSION_S1 = "s1.0"
STRATEGY_VERSION_S2 = "s2.0"

TWIN_FACTOR_ROLES = frozenset(
    {
        "primary_driver",
        "modulator",
        "ignored_unavailable",
        "supporting",
        "",
    }
)
CONFIDENCE_BANDS = frozenset({"low", "medium", "high", ""})
RUNTIME_A_EVIDENCE_KINDS = frozenset(
    {
        "attempt",
        "mission",
        "topic",
        "topic_progress",
        "readiness",
        "study_plan",
        "recommendation",
        "evidence",
        "opaque",
        "",
    }
)

SEVERITY_BANDS = frozenset({"low", "medium", "high", "critical", ""})
DIVERGENCE_BANDS = frozenset({"none", "mild", "material", "severe", ""})
PRIORITY_BANDS = frozenset(
    {"critical", "high", "medium", "low", "advisory", ""}
)
FATIGUE_ACTIONS = frozenset(
    {
        "reduce_intensity",
        "insert_break",
        "stop_for_tonight",
        "shorten_session",
        "",
    }
)
CONFIDENCE_ACTIONS = frozenset(
    {
        "affirm_cautious",
        "request_practice_close",
        "reduce_certainty_copy",
        "assess_structure",
        "",
    }
)
RECOVERY_TRIGGERS = frozenset(
    {
        "abandoned_mission",
        "failed_attempt",
        "long_gap",
        "interrupted_session",
        "",
    }
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
    raise TypeError(f"Unsupported strategy contract value type: {type(value)!r}")


def serialize_canonical(value: Any) -> str:
    """Deterministic JSON serialization (sorted keys, compact separators)."""
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class StrategyExplanationPlaceholder:
    """Explanation placeholder (structure only — no orchestration in S0)."""

    why_summary: str = ""
    educational_principle_ids: tuple[str, ...] = ()
    limitations_codes: tuple[str, ...] = ()
    limitations_summary: str = ""
    input_summary: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "educational_principle_ids",
            _freeze_str_tuple(self.educational_principle_ids),
        )
        object.__setattr__(
            self,
            "limitations_codes",
            _freeze_str_tuple(self.limitations_codes),
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "educational_principle_ids": list(self.educational_principle_ids),
            "input_summary": self.input_summary,
            "limitations_codes": list(self.limitations_codes),
            "limitations_summary": self.limitations_summary,
            "why_summary": self.why_summary,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class StrategyProvenancePlaceholder:
    """Provenance placeholder for Strategy interventions (S0)."""

    source_service: str = ""
    source_entity: str = ""
    collected_at: str | None = None
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = ""
    kind: str = ""

    def __post_init__(self) -> None:
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
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

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class StudyPlanAdvice:
    """Multi-horizon study structure advice (not StudyPlan SQL ownership)."""

    horizon_sessions: int | None = None
    focus_topics: tuple[str, ...] = ()
    daily_minutes_band: str = ""
    stage_policy: str = ""
    twin_factors_used: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    available: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "focus_topics", _freeze_str_tuple(self.focus_topics))
        object.__setattr__(
            self, "twin_factors_used", _freeze_str_tuple(self.twin_factors_used)
        )
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        if self.horizon_sessions is not None and not isinstance(
            self.horizon_sessions, int
        ):
            raise TypeError("horizon_sessions must be an int or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "daily_minutes_band": self.daily_minutes_band,
            "focus_topics": list(self.focus_topics),
            "horizon_sessions": self.horizon_sessions,
            "limitations": list(self.limitations),
            "stage_policy": self.stage_policy,
            "twin_factors_used": list(self.twin_factors_used),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class SessionPlanAdvice:
    """Tonight's completable session shell."""

    primary_topic: str = ""
    advisory_topic: str = ""
    phases: tuple[InterventionStep, ...] = ()
    total_minutes: int | None = None
    close_ritual: str = ""
    materials_note: str = ""
    twin_factors_used: tuple[str, ...] = ()
    adaptive_decision_ref: str = ""
    educational_principle_ids: tuple[str, ...] = ()
    mission_aligned: bool = False
    limitations: tuple[str, ...] = ()
    available: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "phases", tuple(self.phases or ()))
        for phase in self.phases:
            if not isinstance(phase, InterventionStep):
                raise TypeError("phases must contain InterventionStep values")
        object.__setattr__(
            self, "twin_factors_used", _freeze_str_tuple(self.twin_factors_used)
        )
        object.__setattr__(
            self,
            "educational_principle_ids",
            _freeze_str_tuple(self.educational_principle_ids),
        )
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        if self.total_minutes is not None and not isinstance(self.total_minutes, int):
            raise TypeError("total_minutes must be an int or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adaptive_decision_ref": self.adaptive_decision_ref,
            "advisory_topic": self.advisory_topic,
            "available": self.available,
            "close_ritual": self.close_ritual,
            "educational_principle_ids": list(self.educational_principle_ids),
            "limitations": list(self.limitations),
            "materials_note": self.materials_note,
            "mission_aligned": self.mission_aligned,
            "phases": [phase.to_canonical_dict() for phase in self.phases],
            "primary_topic": self.primary_topic,
            "total_minutes": self.total_minutes,
            "twin_factors_used": list(self.twin_factors_used),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class RevisionWindow:
    """One revision window within RevisionPlanAdvice."""

    window_id: str = ""
    due_band: str = ""
    topics: tuple[str, ...] = ()
    suggested_minutes: int | None = None
    rationale_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "topics", _freeze_str_tuple(self.topics))
        object.__setattr__(
            self, "rationale_codes", _freeze_str_tuple(self.rationale_codes)
        )
        if self.suggested_minutes is not None and not isinstance(
            self.suggested_minutes, int
        ):
            raise TypeError("suggested_minutes must be an int or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "due_band": self.due_band,
            "rationale_codes": list(self.rationale_codes),
            "suggested_minutes": self.suggested_minutes,
            "topics": list(self.topics),
            "window_id": self.window_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class RevisionPlanAdvice:
    """Structured revision windows from Adaptive revision priority (no re-rank)."""

    windows: tuple[RevisionWindow, ...] = ()
    primary_revision_topic: str = ""
    spacing_note: str = ""
    twin_revision_behaviour_ref: str = ""
    adaptive_decision_ref: str = ""
    limitations: tuple[str, ...] = ()
    available: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "windows", tuple(self.windows or ()))
        for window in self.windows:
            if not isinstance(window, RevisionWindow):
                raise TypeError("windows must contain RevisionWindow values")
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adaptive_decision_ref": self.adaptive_decision_ref,
            "available": self.available,
            "limitations": list(self.limitations),
            "primary_revision_topic": self.primary_revision_topic,
            "spacing_note": self.spacing_note,
            "twin_revision_behaviour_ref": self.twin_revision_behaviour_ref,
            "windows": [window.to_canonical_dict() for window in self.windows],
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class RecoveryPlanAdvice:
    """Restart-after-failure structure without pep-talk theatre."""

    trigger_kind: str = ""
    runtime_a_refs: tuple[str, ...] = ()
    restart_topic: str = ""
    steps: tuple[InterventionStep, ...] = ()
    what_still_counts: str = ""
    what_does_not_count: str = ""
    twin_persistence_ref: str = ""
    educational_principle_ids: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    available: bool = False

    def __post_init__(self) -> None:
        trigger = (self.trigger_kind or "").strip().lower()
        if trigger not in RECOVERY_TRIGGERS:
            allowed = sorted(k for k in RECOVERY_TRIGGERS if k)
            raise ValueError(f"trigger_kind must be one of {allowed} or empty")
        object.__setattr__(self, "trigger_kind", trigger)
        object.__setattr__(
            self, "runtime_a_refs", _freeze_str_tuple(self.runtime_a_refs)
        )
        object.__setattr__(self, "steps", tuple(self.steps or ()))
        for step in self.steps:
            if not isinstance(step, InterventionStep):
                raise TypeError("steps must contain InterventionStep values")
        object.__setattr__(
            self,
            "educational_principle_ids",
            _freeze_str_tuple(self.educational_principle_ids),
        )
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "educational_principle_ids": list(self.educational_principle_ids),
            "limitations": list(self.limitations),
            "restart_topic": self.restart_topic,
            "runtime_a_refs": list(self.runtime_a_refs),
            "steps": [step.to_canonical_dict() for step in self.steps],
            "trigger_kind": self.trigger_kind,
            "twin_persistence_ref": self.twin_persistence_ref,
            "what_does_not_count": self.what_does_not_count,
            "what_still_counts": self.what_still_counts,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class FatigueIntervention:
    """Fatigue / load guidance derived from Twin + Runtime A activity."""

    severity_band: str = ""
    recommended_action: str = ""
    minutes_adjustment: int | None = None
    twin_cognitive_load_ref: str = ""
    runtime_a_activity_refs: tuple[str, ...] = ()
    educational_principle_ids: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    available: bool = False

    def __post_init__(self) -> None:
        band = (self.severity_band or "").strip().lower()
        if band not in SEVERITY_BANDS:
            allowed = sorted(k for k in SEVERITY_BANDS if k)
            raise ValueError(f"severity_band must be one of {allowed} or empty")
        object.__setattr__(self, "severity_band", band)
        action = (self.recommended_action or "").strip().lower()
        if action not in FATIGUE_ACTIONS:
            allowed = sorted(k for k in FATIGUE_ACTIONS if k)
            raise ValueError(f"recommended_action must be one of {allowed} or empty")
        object.__setattr__(self, "recommended_action", action)
        object.__setattr__(
            self,
            "runtime_a_activity_refs",
            _freeze_str_tuple(self.runtime_a_activity_refs),
        )
        object.__setattr__(
            self,
            "educational_principle_ids",
            _freeze_str_tuple(self.educational_principle_ids),
        )
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        if self.minutes_adjustment is not None and not isinstance(
            self.minutes_adjustment, int
        ):
            raise TypeError("minutes_adjustment must be an int or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "educational_principle_ids": list(self.educational_principle_ids),
            "limitations": list(self.limitations),
            "minutes_adjustment": self.minutes_adjustment,
            "recommended_action": self.recommended_action,
            "runtime_a_activity_refs": list(self.runtime_a_activity_refs),
            "severity_band": self.severity_band,
            "twin_cognitive_load_ref": self.twin_cognitive_load_ref,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ConfidenceIntervention:
    """Confidence calibration guidance vs Runtime A performance evidence."""

    divergence_band: str = ""
    twin_confidence_trend_ref: str = ""
    runtime_a_performance_refs: tuple[str, ...] = ()
    recommended_action: str = ""
    honesty_guard_copy_codes: tuple[str, ...] = ()
    educational_principle_ids: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    available: bool = False

    def __post_init__(self) -> None:
        band = (self.divergence_band or "").strip().lower()
        if band not in DIVERGENCE_BANDS:
            allowed = sorted(k for k in DIVERGENCE_BANDS if k)
            raise ValueError(f"divergence_band must be one of {allowed} or empty")
        object.__setattr__(self, "divergence_band", band)
        action = (self.recommended_action or "").strip().lower()
        if action not in CONFIDENCE_ACTIONS:
            allowed = sorted(k for k in CONFIDENCE_ACTIONS if k)
            raise ValueError(f"recommended_action must be one of {allowed} or empty")
        object.__setattr__(self, "recommended_action", action)
        object.__setattr__(
            self,
            "runtime_a_performance_refs",
            _freeze_str_tuple(self.runtime_a_performance_refs),
        )
        object.__setattr__(
            self,
            "honesty_guard_copy_codes",
            _freeze_str_tuple(self.honesty_guard_copy_codes),
        )
        object.__setattr__(
            self,
            "educational_principle_ids",
            _freeze_str_tuple(self.educational_principle_ids),
        )
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "divergence_band": self.divergence_band,
            "educational_principle_ids": list(self.educational_principle_ids),
            "honesty_guard_copy_codes": list(self.honesty_guard_copy_codes),
            "limitations": list(self.limitations),
            "recommended_action": self.recommended_action,
            "runtime_a_performance_refs": list(self.runtime_a_performance_refs),
            "twin_confidence_trend_ref": self.twin_confidence_trend_ref,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class InterventionSequencing:
    """Primary + supporting intervention ordering for one LearningIntervention."""

    primary_kind: str = ""
    supporting_kinds: tuple[str, ...] = ()
    priority_band: str = ""
    composition_rule: str = ""

    def __post_init__(self) -> None:
        kind = (self.primary_kind or "").strip().upper()
        if kind and kind not in INTERVENTION_KINDS:
            allowed = sorted(k for k in INTERVENTION_KINDS if k)
            raise ValueError(f"primary_kind must be one of {allowed} or empty")
        object.__setattr__(self, "primary_kind", kind)
        supporting: list[str] = []
        for item in self.supporting_kinds or ():
            value = str(item).strip().upper()
            if value and value not in INTERVENTION_KINDS:
                allowed = sorted(k for k in INTERVENTION_KINDS if k)
                raise ValueError(f"supporting kind must be one of {allowed}")
            if value:
                supporting.append(value)
        object.__setattr__(self, "supporting_kinds", tuple(supporting))
        band = (self.priority_band or "").strip().lower()
        if band not in PRIORITY_BANDS:
            allowed = sorted(k for k in PRIORITY_BANDS if k)
            raise ValueError(f"priority_band must be one of {allowed} or empty")
        object.__setattr__(self, "priority_band", band)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "composition_rule": self.composition_rule,
            "primary_kind": self.primary_kind,
            "priority_band": self.priority_band,
            "supporting_kinds": list(self.supporting_kinds),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class InterventionStep:
    """Ordered structural step within a LearningIntervention (no execution)."""

    order: int = 0
    action_code: str = ""
    summary: str = ""
    minutes: int | None = None
    intent: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.order, int):
            raise TypeError("order must be an int")
        if self.minutes is not None and not isinstance(self.minutes, int):
            raise TypeError("minutes must be an int or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "action_code": self.action_code,
            "intent": self.intent,
            "minutes": self.minutes,
            "order": self.order,
            "summary": self.summary,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class LearningIntervention:
    """Immutable Learning Intervention artefact (S0/S1 contract).

    Every intervention exposes identity, strategy version, contributing Adaptive /
    Twin / Runtime A references, educational objective, and explanation /
    provenance placeholders. S1 adds study / session / revision / recovery /
    fatigue / confidence components plus sequencing from one StrategyContext.
    """

    intervention_id: str = ""
    strategy_version: str = STRATEGY_VERSION_S0
    adaptive_recommendation_ref: str = ""
    twin_ref: str = ""
    runtime_a_evidence_ref: str = ""
    educational_objective: str = ""
    explanation: StrategyExplanationPlaceholder = field(
        default_factory=StrategyExplanationPlaceholder
    )
    provenance: StrategyProvenancePlaceholder = field(
        default_factory=StrategyProvenancePlaceholder
    )
    kind: str = ""
    steps: tuple[InterventionStep, ...] = ()
    topic_refs: tuple[str, ...] = ()
    educational_principle_ids: tuple[str, ...] = ()
    runtime_a_refs: tuple[str, ...] = ()
    minutes_budget: int | None = None
    authority: str = AUTHORITY_STRATEGY_ENGINE
    limitations: tuple[str, ...] = ()
    study: StudyPlanAdvice = field(default_factory=StudyPlanAdvice)
    session: SessionPlanAdvice = field(default_factory=SessionPlanAdvice)
    revision: RevisionPlanAdvice = field(default_factory=RevisionPlanAdvice)
    recovery: RecoveryPlanAdvice = field(default_factory=RecoveryPlanAdvice)
    fatigue: FatigueIntervention = field(default_factory=FatigueIntervention)
    confidence: ConfidenceIntervention = field(
        default_factory=ConfidenceIntervention
    )
    sequencing: InterventionSequencing = field(
        default_factory=InterventionSequencing
    )

    def __post_init__(self) -> None:
        kind = (self.kind or "").strip().upper()
        if kind not in INTERVENTION_KINDS:
            allowed = sorted(k for k in INTERVENTION_KINDS if k)
            raise ValueError(f"kind must be one of {allowed} or empty")
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "steps", tuple(self.steps or ()))
        for step in self.steps:
            if not isinstance(step, InterventionStep):
                raise TypeError("steps must contain InterventionStep values")
        object.__setattr__(self, "topic_refs", _freeze_str_tuple(self.topic_refs))
        object.__setattr__(
            self,
            "educational_principle_ids",
            _freeze_str_tuple(self.educational_principle_ids),
        )
        object.__setattr__(
            self,
            "runtime_a_refs",
            _freeze_str_tuple(self.runtime_a_refs),
        )
        object.__setattr__(self, "limitations", _freeze_str_tuple(self.limitations))
        if not isinstance(self.explanation, StrategyExplanationPlaceholder):
            raise TypeError("explanation must be a StrategyExplanationPlaceholder")
        if not isinstance(self.provenance, StrategyProvenancePlaceholder):
            raise TypeError("provenance must be a StrategyProvenancePlaceholder")
        if self.minutes_budget is not None and not isinstance(self.minutes_budget, int):
            raise TypeError("minutes_budget must be an int or None")
        if not isinstance(self.study, StudyPlanAdvice):
            raise TypeError("study must be a StudyPlanAdvice")
        if not isinstance(self.session, SessionPlanAdvice):
            raise TypeError("session must be a SessionPlanAdvice")
        if not isinstance(self.revision, RevisionPlanAdvice):
            raise TypeError("revision must be a RevisionPlanAdvice")
        if not isinstance(self.recovery, RecoveryPlanAdvice):
            raise TypeError("recovery must be a RecoveryPlanAdvice")
        if not isinstance(self.fatigue, FatigueIntervention):
            raise TypeError("fatigue must be a FatigueIntervention")
        if not isinstance(self.confidence, ConfidenceIntervention):
            raise TypeError("confidence must be a ConfidenceIntervention")
        if not isinstance(self.sequencing, InterventionSequencing):
            raise TypeError("sequencing must be an InterventionSequencing")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adaptive_recommendation_ref": self.adaptive_recommendation_ref,
            "authority": self.authority,
            "confidence": self.confidence.to_canonical_dict(),
            "educational_objective": self.educational_objective,
            "educational_principle_ids": list(self.educational_principle_ids),
            "explanation": self.explanation.to_canonical_dict(),
            "fatigue": self.fatigue.to_canonical_dict(),
            "intervention_id": self.intervention_id,
            "kind": self.kind,
            "limitations": list(self.limitations),
            "minutes_budget": self.minutes_budget,
            "provenance": self.provenance.to_canonical_dict(),
            "recovery": self.recovery.to_canonical_dict(),
            "revision": self.revision.to_canonical_dict(),
            "runtime_a_evidence_ref": self.runtime_a_evidence_ref,
            "runtime_a_refs": list(self.runtime_a_refs),
            "sequencing": self.sequencing.to_canonical_dict(),
            "session": self.session.to_canonical_dict(),
            "steps": [step.to_canonical_dict() for step in self.steps],
            "strategy_version": self.strategy_version,
            "study": self.study.to_canonical_dict(),
            "topic_refs": list(self.topic_refs),
            "twin_ref": self.twin_ref,
        }

    def serialize(self) -> str:
        """Deterministic JSON serialization."""
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class StrategyContext:
    """Immutable Strategy input context (S0/S1 contract).

    Carries student identity, decision clock, contributing Adaptive / Twin /
    Runtime A references, and opaque input payloads. Assembler freezes inputs;
    planners must not mutate them.
    """

    student_id: str
    as_of: str | None = None
    adaptive_recommendation_ref: str = ""
    twin_ref: str = ""
    runtime_a_evidence_ref: str = ""
    adaptive_availability: str = AVAILABILITY_UNAVAILABLE
    twin_availability: str = AVAILABILITY_UNAVAILABLE
    runtime_a_availability: str = AVAILABILITY_UNAVAILABLE
    adaptive_unavailable_reason: str = ""
    twin_unavailable_reason: str = ""
    runtime_a_unavailable_reason: str = ""
    intervention_kinds: tuple[str, ...] = ()
    lifecycle_stage: str = ""
    mission_id: str = ""
    field_provenance: Mapping[str, Any] = field(default_factory=dict)
    authority_tags: tuple[str, ...] = ()
    runtime_a: Mapping[str, Any] = field(default_factory=dict)
    twin: Mapping[str, Any] = field(default_factory=dict)
    adaptive: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        sid = (self.student_id or "").strip()
        if not sid:
            raise ValueError("student_id must be a non-empty string")
        object.__setattr__(self, "student_id", sid)
        if self.as_of is not None and not isinstance(self.as_of, str):
            raise TypeError("as_of must be an ISO string or None (no auto clock)")
        for attr in (
            "adaptive_availability",
            "twin_availability",
            "runtime_a_availability",
        ):
            value = (getattr(self, attr) or "").strip().lower()
            if value not in AVAILABILITY_VALUES:
                raise ValueError(
                    f"{attr} must be 'available', 'unavailable', or empty"
                )
            object.__setattr__(self, attr, value)
        kinds: list[str] = []
        for item in self.intervention_kinds or ():
            kind = str(item).strip().upper()
            if kind and kind not in INTERVENTION_KINDS:
                allowed = sorted(k for k in INTERVENTION_KINDS if k)
                raise ValueError(f"intervention kind must be one of {allowed}")
            if kind:
                kinds.append(kind)
        object.__setattr__(self, "intervention_kinds", tuple(kinds))
        object.__setattr__(
            self,
            "authority_tags",
            _freeze_str_tuple(self.authority_tags),
        )
        object.__setattr__(
            self,
            "field_provenance",
            _freeze_mapping(self.field_provenance),
        )
        object.__setattr__(self, "runtime_a", _freeze_mapping(self.runtime_a))
        object.__setattr__(self, "twin", _freeze_mapping(self.twin))
        object.__setattr__(self, "adaptive", _freeze_mapping(self.adaptive))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adaptive": dict(self.adaptive),
            "adaptive_availability": self.adaptive_availability,
            "adaptive_recommendation_ref": self.adaptive_recommendation_ref,
            "adaptive_unavailable_reason": self.adaptive_unavailable_reason,
            "as_of": self.as_of,
            "authority_tags": list(self.authority_tags),
            "field_provenance": {
                str(k): dict(v) if isinstance(v, Mapping) else v
                for k, v in sorted(self.field_provenance.items())
            },
            "intervention_kinds": list(self.intervention_kinds),
            "lifecycle_stage": self.lifecycle_stage,
            "mission_id": self.mission_id,
            "runtime_a": dict(self.runtime_a),
            "runtime_a_availability": self.runtime_a_availability,
            "runtime_a_evidence_ref": self.runtime_a_evidence_ref,
            "runtime_a_unavailable_reason": self.runtime_a_unavailable_reason,
            "student_id": self.student_id,
            "twin": dict(self.twin),
            "twin_availability": self.twin_availability,
            "twin_ref": self.twin_ref,
            "twin_unavailable_reason": self.twin_unavailable_reason,
        }

    def serialize(self) -> str:
        """Deterministic JSON serialization of material context fields."""
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class StrategyResult:
    """Result envelope for Strategy Adapter calls."""

    ok: bool
    value: LearningIntervention | None = None
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


# --- Explainability DTOs (MS-005 S2) ----------------------------------------


@dataclass(frozen=True)
class StrategyWhyExplanation:
    """Plain-language why + stable reason codes for one intervention."""

    summary: str = ""
    reason_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "reason_codes", _freeze_str_tuple(self.reason_codes)
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "reason_codes": list(self.reason_codes),
            "summary": self.summary,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class RuntimeAEvidenceRef:
    """One Runtime A evidence citation (never invented)."""

    kind: str = ""
    id: str = ""
    observed_at: str | None = None
    note: str = ""

    def __post_init__(self) -> None:
        kind = (self.kind or "").strip().lower()
        if kind not in RUNTIME_A_EVIDENCE_KINDS:
            allowed = sorted(k for k in RUNTIME_A_EVIDENCE_KINDS if k)
            raise ValueError(f"evidence kind must be one of {allowed} or empty")
        object.__setattr__(self, "kind", kind)
        if self.observed_at is not None and not isinstance(self.observed_at, str):
            raise TypeError("observed_at must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "note": self.note,
            "observed_at": self.observed_at,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class TwinFactorConsidered:
    """One Twin facet considered during Strategy orchestration."""

    facet_id: str = ""
    availability: str = AVAILABILITY_UNAVAILABLE
    role: str = ""
    note: str = ""

    def __post_init__(self) -> None:
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)
        role = (self.role or "").strip().lower()
        if role not in TWIN_FACTOR_ROLES:
            allowed = sorted(k for k in TWIN_FACTOR_ROLES if k)
            raise ValueError(f"role must be one of {allowed} or empty")
        object.__setattr__(self, "role", role)
        object.__setattr__(self, "facet_id", (self.facet_id or "").strip())

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "availability": self.availability,
            "facet_id": self.facet_id,
            "note": self.note,
            "role": self.role,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class TwinFactorsExplanation:
    """Twin factors considered for intervention structure (not topic invention)."""

    snapshot_ref: str = ""
    factors_considered: tuple[TwinFactorConsidered, ...] = ()
    summary: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "factors_considered", tuple(self.factors_considered or ())
        )
        for item in self.factors_considered:
            if not isinstance(item, TwinFactorConsidered):
                raise TypeError(
                    "factors_considered must contain TwinFactorConsidered only"
                )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "factors_considered": [
                item.to_canonical_dict() for item in self.factors_considered
            ],
            "snapshot_ref": self.snapshot_ref,
            "summary": self.summary,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class AdaptiveConsumedExplanation:
    """Adaptive recommendation consumption record (no re-ranking)."""

    decision_id: str = ""
    primary_topic: str = ""
    recommendation_summary: str = ""
    alternatives_preserved: tuple[str, ...] = ()
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "alternatives_preserved",
            _freeze_str_tuple(self.alternatives_preserved),
        )
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "alternatives_preserved": list(self.alternatives_preserved),
            "availability": self.availability,
            "decision_id": self.decision_id,
            "primary_topic": self.primary_topic,
            "recommendation_summary": self.recommendation_summary,
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class EducationalPrincipleApplied:
    """Registered educational principle applied to this intervention."""

    principle_id: str = ""
    version: str = ""
    description: str = ""
    how_applied: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "description": self.description,
            "how_applied": self.how_applied,
            "principle_id": self.principle_id,
            "version": self.version,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class StrategyConfidenceExplanation:
    """Orchestration-completeness confidence (not Adaptive confidence copy)."""

    score: float | None = None
    band: str = ""
    rationale: str = ""

    def __post_init__(self) -> None:
        band = (self.band or "").strip().lower()
        if band not in CONFIDENCE_BANDS:
            allowed = sorted(k for k in CONFIDENCE_BANDS if k)
            raise ValueError(f"band must be one of {allowed} or empty")
        object.__setattr__(self, "band", band)
        if self.score is not None and not isinstance(self.score, int | float):
            raise TypeError("score must be a number or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "band": self.band,
            "rationale": self.rationale,
            "score": self.score,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class AlternativeInterventionItem:
    """One non-selected supporting intervention kind."""

    intervention_kind: str = ""
    rank: int = 0
    reason_codes: tuple[str, ...] = ()
    why_not_selected: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.rank, int):
            raise TypeError("rank must be an int")
        object.__setattr__(
            self, "reason_codes", _freeze_str_tuple(self.reason_codes)
        )
        kind = (self.intervention_kind or "").strip().upper()
        if kind and kind not in INTERVENTION_KINDS:
            allowed = sorted(k for k in INTERVENTION_KINDS if k)
            raise ValueError(f"intervention_kind must be one of {allowed} or empty")
        object.__setattr__(self, "intervention_kind", kind)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "intervention_kind": self.intervention_kind,
            "rank": self.rank,
            "reason_codes": list(self.reason_codes),
            "why_not_selected": self.why_not_selected,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class StrategyAlternativesExplanation:
    """Supporting / non-primary intervention alternatives."""

    items: tuple[AlternativeInterventionItem, ...] = ()
    rationale: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "items", tuple(self.items or ()))
        for item in self.items:
            if not isinstance(item, AlternativeInterventionItem):
                raise TypeError(
                    "items must contain AlternativeInterventionItem only"
                )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "items": [item.to_canonical_dict() for item in self.items],
            "rationale": self.rationale,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class StrategyLimitationsExplanation:
    """Honest limitations for orchestration completeness."""

    codes: tuple[str, ...] = ()
    summary: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "codes", _freeze_str_tuple(self.codes))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {"codes": list(self.codes), "summary": self.summary}

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class MissionNoteExplanation:
    """Mission-alignment note for session-shaped interventions."""

    mission_aligned: bool = False
    summary: str = ""

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "mission_aligned": self.mission_aligned,
            "summary": self.summary,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class PlannerContribution:
    """Documented contribution from one Strategy planner."""

    planner_id: str = ""
    available: bool = False
    contribution_summary: str = ""
    twin_factors_used: tuple[str, ...] = ()
    principle_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "twin_factors_used", _freeze_str_tuple(self.twin_factors_used)
        )
        object.__setattr__(
            self, "principle_ids", _freeze_str_tuple(self.principle_ids)
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "contribution_summary": self.contribution_summary,
            "planner_id": self.planner_id,
            "principle_ids": list(self.principle_ids),
            "twin_factors_used": list(self.twin_factors_used),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class StrategyExplanationBundle:
    """Deterministic explainability for one LearningIntervention (MS-005 S2).

    Answers educational objective, Runtime A evidence, Twin factors, Adaptive
    consumption, educational principles, and planner contributions. No hidden
    reasoning. Does not mutate the intervention.
    """

    intervention_id: str = ""
    explainability_version: str = STRATEGY_VERSION_S2
    educational_objective: str = ""
    why: StrategyWhyExplanation = field(default_factory=StrategyWhyExplanation)
    runtime_a_evidence_refs: tuple[RuntimeAEvidenceRef, ...] = ()
    twin_factors: TwinFactorsExplanation = field(
        default_factory=TwinFactorsExplanation
    )
    adaptive_consumed: AdaptiveConsumedExplanation = field(
        default_factory=AdaptiveConsumedExplanation
    )
    educational_principles: tuple[EducationalPrincipleApplied, ...] = ()
    confidence: StrategyConfidenceExplanation = field(
        default_factory=StrategyConfidenceExplanation
    )
    alternatives: StrategyAlternativesExplanation = field(
        default_factory=StrategyAlternativesExplanation
    )
    limitations: StrategyLimitationsExplanation = field(
        default_factory=StrategyLimitationsExplanation
    )
    mission_note: MissionNoteExplanation | None = None
    planner_contributions: tuple[PlannerContribution, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "runtime_a_evidence_refs",
            tuple(self.runtime_a_evidence_refs or ()),
        )
        for item in self.runtime_a_evidence_refs:
            if not isinstance(item, RuntimeAEvidenceRef):
                raise TypeError(
                    "runtime_a_evidence_refs must contain RuntimeAEvidenceRef only"
                )
        object.__setattr__(
            self,
            "educational_principles",
            tuple(self.educational_principles or ()),
        )
        for item in self.educational_principles:
            if not isinstance(item, EducationalPrincipleApplied):
                raise TypeError(
                    "educational_principles must contain "
                    "EducationalPrincipleApplied only"
                )
        object.__setattr__(
            self,
            "planner_contributions",
            tuple(self.planner_contributions or ()),
        )
        for item in self.planner_contributions:
            if not isinstance(item, PlannerContribution):
                raise TypeError(
                    "planner_contributions must contain PlannerContribution only"
                )
        if not isinstance(self.why, StrategyWhyExplanation):
            raise TypeError("why must be a StrategyWhyExplanation")
        if not isinstance(self.twin_factors, TwinFactorsExplanation):
            raise TypeError("twin_factors must be a TwinFactorsExplanation")
        if not isinstance(self.adaptive_consumed, AdaptiveConsumedExplanation):
            raise TypeError(
                "adaptive_consumed must be an AdaptiveConsumedExplanation"
            )
        if not isinstance(self.confidence, StrategyConfidenceExplanation):
            raise TypeError("confidence must be a StrategyConfidenceExplanation")
        if not isinstance(self.alternatives, StrategyAlternativesExplanation):
            raise TypeError(
                "alternatives must be a StrategyAlternativesExplanation"
            )
        if not isinstance(self.limitations, StrategyLimitationsExplanation):
            raise TypeError(
                "limitations must be a StrategyLimitationsExplanation"
            )
        if self.mission_note is not None and not isinstance(
            self.mission_note, MissionNoteExplanation
        ):
            raise TypeError("mission_note must be a MissionNoteExplanation or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adaptive_consumed": self.adaptive_consumed.to_canonical_dict(),
            "alternatives": self.alternatives.to_canonical_dict(),
            "confidence": self.confidence.to_canonical_dict(),
            "educational_objective": self.educational_objective,
            "educational_principles": [
                item.to_canonical_dict() for item in self.educational_principles
            ],
            "explainability_version": self.explainability_version,
            "intervention_id": self.intervention_id,
            "limitations": self.limitations.to_canonical_dict(),
            "mission_note": (
                None
                if self.mission_note is None
                else self.mission_note.to_canonical_dict()
            ),
            "planner_contributions": [
                item.to_canonical_dict() for item in self.planner_contributions
            ],
            "runtime_a_evidence_refs": [
                item.to_canonical_dict() for item in self.runtime_a_evidence_refs
            ],
            "twin_factors": self.twin_factors.to_canonical_dict(),
            "why": self.why.to_canonical_dict(),
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


# --- Experience projection DTOs (MS-005 S2) ---------------------------------


@dataclass(frozen=True)
class StrategyExplanationSummaryProjection:
    """Condensed StrategyExplanationBundle for Experience."""

    why_summary: str = ""
    educational_objective: str = ""
    confidence_band: str = ""
    confidence_rationale: str = ""
    principle_ids: tuple[str, ...] = ()
    runtime_a_ref_count: int = 0
    twin_factor_count: int = 0
    adaptive_availability: str = AVAILABILITY_UNAVAILABLE
    limitations_codes: tuple[str, ...] = ()
    planner_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "principle_ids", _freeze_str_tuple(self.principle_ids)
        )
        object.__setattr__(
            self, "limitations_codes", _freeze_str_tuple(self.limitations_codes)
        )
        object.__setattr__(self, "planner_ids", _freeze_str_tuple(self.planner_ids))
        if not isinstance(self.runtime_a_ref_count, int):
            raise TypeError("runtime_a_ref_count must be an int")
        if not isinstance(self.twin_factor_count, int):
            raise TypeError("twin_factor_count must be an int")
        availability = (self.adaptive_availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                "adaptive_availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "adaptive_availability", availability)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adaptive_availability": self.adaptive_availability,
            "confidence_band": self.confidence_band,
            "confidence_rationale": self.confidence_rationale,
            "educational_objective": self.educational_objective,
            "limitations_codes": list(self.limitations_codes),
            "planner_ids": list(self.planner_ids),
            "principle_ids": list(self.principle_ids),
            "runtime_a_ref_count": self.runtime_a_ref_count,
            "twin_factor_count": self.twin_factor_count,
            "why_summary": self.why_summary,
        }


@dataclass(frozen=True)
class StrategyProjectionProvenance:
    """Provenance references for an Experience Strategy projection."""

    intervention_id: str = ""
    adaptive_decision_id: str = ""
    twin_snapshot_ref: str = ""
    runtime_a_evidence_ref: str = ""
    authority: str = AUTHORITY_STRATEGY_ENGINE
    as_of: str | None = None
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "provenance_refs", _freeze_str_tuple(self.provenance_refs)
        )
        if self.as_of is not None and not isinstance(self.as_of, str):
            raise TypeError("as_of must be an ISO string or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adaptive_decision_id": self.adaptive_decision_id,
            "as_of": self.as_of,
            "authority": self.authority,
            "intervention_id": self.intervention_id,
            "provenance_refs": list(self.provenance_refs),
            "runtime_a_evidence_ref": self.runtime_a_evidence_ref,
            "twin_snapshot_ref": self.twin_snapshot_ref,
        }


@dataclass(frozen=True)
class StrategyProjection:
    """Dedicated Experience-facing Strategy projection (MS-005 S2).

    Experience may consume only this DTO (or opaque dicts derived from it).
    Must not expose raw LearningIntervention objects, planner internals, or
    mutable Strategy state.
    """

    student_id: str = ""
    intervention_id: str = ""
    strategy_decision_id: str = ""
    as_of: str | None = None
    projection_version: str = STRATEGY_VERSION_S2
    authority: str = AUTHORITY_STRATEGY_ENGINE
    primary_intervention_kind: str = ""
    educational_objective: str = ""
    topic_code: str = ""
    topic_title: str = ""
    topic_refs: tuple[str, ...] = ()
    minutes_budget: int | None = None
    steps: tuple[Mapping[str, Any], ...] = ()
    session_plan: Mapping[str, Any] = field(default_factory=dict)
    study_plan: Mapping[str, Any] = field(default_factory=dict)
    revision_plan: Mapping[str, Any] = field(default_factory=dict)
    recovery_plan: Mapping[str, Any] = field(default_factory=dict)
    fatigue: Mapping[str, Any] = field(default_factory=dict)
    confidence_intervention: Mapping[str, Any] = field(default_factory=dict)
    explanation_summary: StrategyExplanationSummaryProjection = field(
        default_factory=StrategyExplanationSummaryProjection
    )
    educational_principle_ids: tuple[str, ...] = ()
    adaptive_decision_id: str = ""
    twin_snapshot_ref: str = ""
    confidence_band: str = ""
    mission_aligned: bool = False
    availability: str = AVAILABILITY_UNAVAILABLE
    unavailable_reason: str = ""
    limitations_codes: tuple[str, ...] = ()
    explanation: Mapping[str, Any] = field(default_factory=dict)
    provenance: StrategyProjectionProvenance = field(
        default_factory=StrategyProjectionProvenance
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "topic_refs", _freeze_str_tuple(self.topic_refs))
        object.__setattr__(
            self,
            "educational_principle_ids",
            _freeze_str_tuple(self.educational_principle_ids),
        )
        object.__setattr__(
            self, "limitations_codes", _freeze_str_tuple(self.limitations_codes)
        )
        object.__setattr__(
            self,
            "steps",
            tuple(_freeze_mapping(step) for step in (self.steps or ())),
        )
        object.__setattr__(self, "session_plan", _freeze_mapping(self.session_plan))
        object.__setattr__(self, "study_plan", _freeze_mapping(self.study_plan))
        object.__setattr__(
            self, "revision_plan", _freeze_mapping(self.revision_plan)
        )
        object.__setattr__(
            self, "recovery_plan", _freeze_mapping(self.recovery_plan)
        )
        object.__setattr__(self, "fatigue", _freeze_mapping(self.fatigue))
        object.__setattr__(
            self,
            "confidence_intervention",
            _freeze_mapping(self.confidence_intervention),
        )
        object.__setattr__(self, "explanation", _freeze_mapping(self.explanation))
        if not isinstance(
            self.explanation_summary, StrategyExplanationSummaryProjection
        ):
            raise TypeError(
                "explanation_summary must be a StrategyExplanationSummaryProjection"
            )
        if not isinstance(self.provenance, StrategyProjectionProvenance):
            raise TypeError("provenance must be a StrategyProjectionProvenance")
        availability = (self.availability or "").strip().lower()
        if availability not in AVAILABILITY_VALUES:
            raise ValueError(
                "availability must be 'available', 'unavailable', or empty"
            )
        object.__setattr__(self, "availability", availability)
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        if self.as_of is not None and not isinstance(self.as_of, str):
            raise TypeError("as_of must be an ISO string or None")
        if self.minutes_budget is not None and not isinstance(
            self.minutes_budget, int
        ):
            raise TypeError("minutes_budget must be an int or None")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "adaptive_decision_id": self.adaptive_decision_id,
            "as_of": self.as_of,
            "authority": self.authority,
            "availability": self.availability,
            "confidence_band": self.confidence_band,
            "confidence_intervention": dict(self.confidence_intervention),
            "educational_objective": self.educational_objective,
            "educational_principle_ids": list(self.educational_principle_ids),
            "explanation": dict(self.explanation),
            "explanation_summary": self.explanation_summary.to_canonical_dict(),
            "fatigue": dict(self.fatigue),
            "intervention_id": self.intervention_id,
            "limitations_codes": list(self.limitations_codes),
            "minutes_budget": self.minutes_budget,
            "mission_aligned": self.mission_aligned,
            "primary_intervention_kind": self.primary_intervention_kind,
            "projection_version": self.projection_version,
            "provenance": self.provenance.to_canonical_dict(),
            "recovery_plan": dict(self.recovery_plan),
            "revision_plan": dict(self.revision_plan),
            "session_plan": dict(self.session_plan),
            "steps": [dict(step) for step in self.steps],
            "strategy_decision_id": self.strategy_decision_id,
            "student_id": self.student_id,
            "study_plan": dict(self.study_plan),
            "topic_code": self.topic_code,
            "topic_refs": list(self.topic_refs),
            "topic_title": self.topic_title,
            "twin_snapshot_ref": self.twin_snapshot_ref,
            "unavailable_reason": self.unavailable_reason,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class StrategyProjectionResult:
    """Result envelope for StrategyProjectionPort calls."""

    ok: bool
    value: StrategyProjection | None = None
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
class LearningStrategyContract(Protocol):
    """Pure Learning Strategy contract — context in, intervention out.

    Implementations must be deterministic for identical StrategyContext material
    fields. Must not write Runtime A, Twin, or Adaptive educational state.
    """

    def evaluate(self, context: StrategyContext) -> LearningIntervention:
        """Evaluate a StrategyContext into a LearningIntervention."""


@runtime_checkable
class StrategyAdapter(Protocol):
    """Adapter interface between Experience and Learning Strategy contracts.

    Read-only relative to educational history. Must not call Planning write
    APIs, Evidence acceptance, TopicProgress writes, mission mutations, Twin
    synthesis, or Adaptive re-ranking.
    """

    @property
    def adapter_id(self) -> str:
        """Stable Strategy Engine Adapter identity."""

    def orchestrate(
        self,
        student_id: str,
        *,
        context: StrategyContext | None = None,
        intervention_kinds: tuple[str, ...] | None = None,
        include_explanation: bool = True,
        shadow: bool = False,
    ) -> StrategyResult:
        """Produce a LearningIntervention behind the Learning Strategy contract."""


@runtime_checkable
class StrategyProjectionPort(Protocol):
    """Experience-facing port that serves StrategyProjection DTOs only.

    Must not expose raw LearningIntervention objects. Read-only relative to
    Runtime A / Twin / Adaptive / Strategy educational state. No authority
    cutover in S2 — construction is feature-flag gated only.
    """

    @property
    def port_id(self) -> str:
        """Stable Strategy Projection Port identity."""

    def get_tonight_projection(self, student_id: str) -> StrategyProjectionResult:
        """Return tonight's Experience-safe Strategy projection for a student."""

    def project_intervention(
        self,
        intervention: LearningIntervention,
        *,
        student_id: str = "",
        explanation: StrategyExplanationBundle | None = None,
        as_of: str | None = None,
    ) -> StrategyProjection:
        """Project an immutable LearningIntervention into StrategyProjection."""
