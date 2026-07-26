"""Immutable Personal Learning Profile contracts (EP-004.1).

Summarises long-term observed learning behaviours and preferences from
Learning Feedback evidence. Does not make educational decisions.

Constitutional rules:
- Profile summarises evidence; it does not rank, plan, or score readiness.
- No service may delegate its constitutional authority to the profile.
- Attributes must remain explainable and traceable to observed evidence.
- Observed facts, derived indicators, and unsupported assumptions are
  labelled explicitly.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable

CONTRACT_VERSION = "ep004.1.1"
AUTHORITY_PERSONAL_LEARNING_PROFILE = "personal_learning_profile"

# Attribute keys (stable consumer contract).
ATTR_PREFERRED_SESSION_DURATION = "preferred_study_session_duration"
ATTR_CONSISTENCY_TREND = "consistency_trend"
ATTR_RECOVERY_EFFECTIVENESS = "recovery_effectiveness"
ATTR_REVISION_ADHERENCE = "revision_adherence"
ATTR_RECOMMENDATION_RESPONSIVENESS = "recommendation_responsiveness"
ATTR_PLANNING_COMPLETION_RATE = "planning_completion_rate"
ATTR_PREFERRED_STUDY_WINDOWS = "preferred_study_windows"

PROFILE_ATTRIBUTE_KEYS = frozenset(
    {
        ATTR_PREFERRED_SESSION_DURATION,
        ATTR_CONSISTENCY_TREND,
        ATTR_RECOVERY_EFFECTIVENESS,
        ATTR_REVISION_ADHERENCE,
        ATTR_RECOMMENDATION_RESPONSIVENESS,
        ATTR_PLANNING_COMPLETION_RATE,
        ATTR_PREFERRED_STUDY_WINDOWS,
    }
)

# Epistemic kinds — how the attribute relates to evidence.
KIND_OBSERVED_FACT = "observed_fact"
KIND_DERIVED_INDICATOR = "derived_indicator"
KIND_UNSUPPORTED = "unsupported"

ALLOWED_ATTRIBUTE_KINDS = frozenset(
    {
        KIND_OBSERVED_FACT,
        KIND_DERIVED_INDICATOR,
        KIND_UNSUPPORTED,
    }
)

# Availability of a value for consumers.
STATUS_AVAILABLE = "available"
STATUS_UNAVAILABLE = "unavailable"
STATUS_UNSUPPORTED = "unsupported"

ALLOWED_ATTRIBUTE_STATUSES = frozenset(
    {
        STATUS_AVAILABLE,
        STATUS_UNAVAILABLE,
        STATUS_UNSUPPORTED,
    }
)

# Claim boundaries for profile attributes (never educational conclusions).
CLAIM_BEHAVIOUR_SUMMARY = "behaviour_summary"
CLAIM_PREFERENCE_SUMMARY = "preference_summary"
CLAIM_HABIT_SUMMARY = "habit_summary"
CLAIM_UNSUPPORTED = "unsupported_assumption"

ALLOWED_CLAIM_BOUNDARIES = frozenset(
    {
        CLAIM_BEHAVIOUR_SUMMARY,
        CLAIM_PREFERENCE_SUMMARY,
        CLAIM_HABIT_SUMMARY,
        CLAIM_UNSUPPORTED,
    }
)

# Forbidden as educational conclusions on profile attributes / evidence bags.
FORBIDDEN_INFERENCE_KEYS = frozenset(
    {
        "mastery",
        "estimated_knowledge",
        "readiness_score",
        "recommendation_quality",
        "learning_gain",
        "educational_conclusion",
        "inferred_weakness",
        "inferred_strength",
        "next_action",
        "plan_slots",
    }
)

RESOLVE_STATUS_OK = "ok"
RESOLVE_STATUS_SKIPPED = "skipped"
RESOLVE_STATUS_FAILED = "failed"
RESOLVE_STATUSES = frozenset(
    {
        RESOLVE_STATUS_OK,
        RESOLVE_STATUS_SKIPPED,
        RESOLVE_STATUS_FAILED,
    }
)

REASON_FLAG_OFF = "personal_learning_profile_flag_off"
REASON_NO_EVIDENCE = "no_observed_evidence"
REASON_SCHEMA_INVALID = "profile_schema_invalid"
REASON_FORBIDDEN_INFERENCE = "forbidden_inference_payload"
REASON_AGGREGATOR_ERROR = "aggregator_error"
REASON_STORE_ERROR = "store_error"

# Sample-size thresholds for confidence (deterministic, documented).
CONFIDENCE_FULL_SAMPLE = 10
CONFIDENCE_MIN_SAMPLE = 1


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    raw = dict(value or {})
    frozen: dict[str, Any] = {}
    for key, item in raw.items():
        key_s = str(key)
        if key_s.lower() in FORBIDDEN_INFERENCE_KEYS:
            raise ValueError(
                f"forbidden inference key in profile payload: {key_s!r}"
            )
        if isinstance(item, Mapping):
            frozen[key_s] = dict(item)
        elif isinstance(item, list | tuple):
            frozen[key_s] = list(item)
        else:
            frozen[key_s] = item
    return MappingProxyType(frozen)


def serialize_canonical(value: Any) -> str:
    """Deterministic JSON serialization (sorted keys, compact separators)."""
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        items = sorted(value.items(), key=lambda i: str(i[0]))
        return {str(k): _canonical(v) for k, v in items}
    if isinstance(value, list | tuple):
        return [_canonical(v) for v in value]
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int | float):
        return value
    return str(value)


def confidence_from_sample_size(sample_size: int) -> float:
    """Map observation count to [0, 1] confidence (deterministic)."""
    n = max(0, int(sample_size or 0))
    if n < CONFIDENCE_MIN_SAMPLE:
        return 0.0
    return min(1.0, round(n / CONFIDENCE_FULL_SAMPLE, 4))


def deterministic_profile_id(
    *,
    student_id: str,
    as_of: str,
    evidence_fingerprint: str,
    contract_version: str = CONTRACT_VERSION,
) -> str:
    """Derive profile_id from factual material fields."""
    material = {
        "as_of": as_of,
        "contract_version": contract_version,
        "evidence_fingerprint": evidence_fingerprint,
        "student_id": student_id,
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"plp-{digest[:32]}"


@dataclass(frozen=True)
class ProfileEvidenceRef:
    """Traceability pointer from a profile attribute to observed evidence."""

    feedback_id: str
    event_type: str
    source_authority: str
    timestamp: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "feedback_id", (self.feedback_id or "").strip()
        )
        object.__setattr__(
            self, "event_type", (self.event_type or "").strip().lower()
        )
        object.__setattr__(
            self,
            "source_authority",
            (self.source_authority or "").strip().lower(),
        )
        object.__setattr__(self, "timestamp", (self.timestamp or "").strip())
        if not self.feedback_id:
            raise ValueError("feedback_id is required on ProfileEvidenceRef")
        if not self.event_type:
            raise ValueError("event_type is required on ProfileEvidenceRef")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "feedback_id": self.feedback_id,
            "source_authority": self.source_authority,
            "timestamp": self.timestamp,
        }


@dataclass(frozen=True)
class ProfileAttribute:
    """One explainable Personal Learning Profile attribute.

    ``kind`` distinguishes observed facts, derived indicators, and
    unsupported assumptions. ``status`` tells consumers whether a value
    may lawfully be used.
    """

    key: str
    kind: str
    status: str
    claim_boundary: str
    value: Any = None
    confidence: float = 0.0
    sample_size: int = 0
    explanation: str = ""
    evidence_refs: tuple[ProfileEvidenceRef, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "key", (self.key or "").strip().lower())
        object.__setattr__(self, "kind", (self.kind or "").strip().lower())
        object.__setattr__(
            self, "status", (self.status or "").strip().lower()
        )
        object.__setattr__(
            self,
            "claim_boundary",
            (self.claim_boundary or "").strip().lower(),
        )
        object.__setattr__(
            self, "explanation", (self.explanation or "").strip()
        )
        object.__setattr__(self, "sample_size", max(0, int(self.sample_size or 0)))
        conf = float(self.confidence or 0.0)
        if conf < 0.0 or conf > 1.0:
            raise ValueError("confidence must be in [0, 1]")
        object.__setattr__(self, "confidence", conf)
        refs = tuple(self.evidence_refs or ())
        object.__setattr__(self, "evidence_refs", refs)
        limits = tuple(
            str(x).strip()
            for x in (self.limitations or ())
            if str(x).strip()
        )
        object.__setattr__(self, "limitations", limits)

        if self.key not in PROFILE_ATTRIBUTE_KEYS:
            raise ValueError(f"unknown profile attribute key: {self.key!r}")
        if self.kind not in ALLOWED_ATTRIBUTE_KINDS:
            raise ValueError(f"unknown attribute kind: {self.kind!r}")
        if self.status not in ALLOWED_ATTRIBUTE_STATUSES:
            raise ValueError(f"unknown attribute status: {self.status!r}")
        if self.claim_boundary not in ALLOWED_CLAIM_BOUNDARIES:
            raise ValueError(
                f"unknown claim_boundary: {self.claim_boundary!r}"
            )
        if self.status == STATUS_UNSUPPORTED and self.kind != KIND_UNSUPPORTED:
            raise ValueError(
                "unsupported status requires kind=unsupported"
            )
        if self.kind == KIND_UNSUPPORTED and self.status != STATUS_UNSUPPORTED:
            raise ValueError(
                "kind=unsupported requires status=unsupported"
            )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "claim_boundary": self.claim_boundary,
            "confidence": self.confidence,
            "evidence_refs": [r.to_canonical_dict() for r in self.evidence_refs],
            "explanation": self.explanation,
            "key": self.key,
            "kind": self.kind,
            "limitations": list(self.limitations),
            "sample_size": self.sample_size,
            "status": self.status,
            "value": self.value,
        }


@dataclass(frozen=True)
class PersonalLearningProfile:
    """Immutable Personal Learning Profile snapshot for one student.

    Summarises observed behavioural evidence. Never an educational authority.
    """

    profile_id: str
    student_id: str
    as_of: str
    attributes: Mapping[str, ProfileAttribute]
    evidence_fingerprint: str
    evidence_event_count: int = 0
    contract_version: str = CONTRACT_VERSION
    authority: str = AUTHORITY_PERSONAL_LEARNING_PROFILE
    provenance: Mapping[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "profile_id", (self.profile_id or "").strip()
        )
        object.__setattr__(
            self, "student_id", (self.student_id or "").strip()
        )
        object.__setattr__(self, "as_of", (self.as_of or "").strip())
        object.__setattr__(
            self,
            "evidence_fingerprint",
            (self.evidence_fingerprint or "").strip(),
        )
        object.__setattr__(
            self,
            "evidence_event_count",
            max(0, int(self.evidence_event_count or 0)),
        )
        object.__setattr__(
            self,
            "contract_version",
            (self.contract_version or CONTRACT_VERSION).strip(),
        )
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_PERSONAL_LEARNING_PROFILE).strip(),
        )
        attrs = dict(self.attributes or {})
        frozen_attrs: dict[str, ProfileAttribute] = {}
        for key, attr in attrs.items():
            key_s = str(key).strip().lower()
            if not isinstance(attr, ProfileAttribute):
                raise ValueError(
                    f"attribute {key_s!r} must be a ProfileAttribute"
                )
            if attr.key != key_s:
                raise ValueError(
                    f"attribute map key {key_s!r} != attribute.key {attr.key!r}"
                )
            frozen_attrs[key_s] = attr
        missing = PROFILE_ATTRIBUTE_KEYS - frozenset(frozen_attrs)
        if missing:
            raise ValueError(
                f"profile missing required attributes: {sorted(missing)}"
            )
        object.__setattr__(
            self, "attributes", MappingProxyType(frozen_attrs)
        )
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        limits = tuple(
            str(x).strip() for x in (self.limitations or ()) if str(x).strip()
        )
        object.__setattr__(self, "limitations", limits)

        if not self.profile_id:
            raise ValueError("profile_id is required")
        if not self.student_id:
            raise ValueError("student_id is required")
        if not self.as_of:
            raise ValueError("as_of is required")

    def get(self, key: str) -> ProfileAttribute | None:
        """Return one attribute by stable key, or None."""
        return self.attributes.get((key or "").strip().lower())

    def consumer_view(self) -> dict[str, Any]:
        """Stable consumer projection (no implementation details)."""
        return {
            "as_of": self.as_of,
            "attributes": {
                key: {
                    "claim_boundary": attr.claim_boundary,
                    "confidence": attr.confidence,
                    "explanation": attr.explanation,
                    "kind": attr.kind,
                    "limitations": list(attr.limitations),
                    "sample_size": attr.sample_size,
                    "status": attr.status,
                    "value": attr.value,
                }
                for key, attr in sorted(self.attributes.items())
            },
            "authority": self.authority,
            "contract_version": self.contract_version,
            "evidence_event_count": self.evidence_event_count,
            "limitations": list(self.limitations),
            "profile_id": self.profile_id,
            "student_id": self.student_id,
        }

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "attributes": {
                k: v.to_canonical_dict()
                for k, v in sorted(self.attributes.items())
            },
            "authority": self.authority,
            "contract_version": self.contract_version,
            "evidence_event_count": self.evidence_event_count,
            "evidence_fingerprint": self.evidence_fingerprint,
            "limitations": list(self.limitations),
            "profile_id": self.profile_id,
            "provenance": dict(self.provenance),
            "student_id": self.student_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ProfileResolveResult:
    """Fail-open result of resolving a Personal Learning Profile."""

    ok: bool
    status: str
    profile: PersonalLearningProfile | None = None
    reason: str = ""
    message: str = ""

    def __post_init__(self) -> None:
        status = (self.status or "").strip().lower()
        if status not in RESOLVE_STATUSES:
            raise ValueError(f"unknown resolve status: {self.status!r}")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "ok", bool(self.ok))
        object.__setattr__(self, "reason", (self.reason or "").strip())
        object.__setattr__(self, "message", (self.message or "").strip())


@runtime_checkable
class PersonalLearningProfilePort(Protocol):
    """Public consumer surface for Runtime A services.

    Services depend on this Protocol only — never on aggregator / store
    implementation details. Profile is never educational authority.
    """

    def resolve(
        self,
        student_id: str | int,
        *,
        events: Sequence[Any] | None = None,
        declared_session_minutes: int | None = None,
        as_of: str | None = None,
    ) -> ProfileResolveResult:
        """Resolve (or skip) a Personal Learning Profile snapshot."""

    def get_cached(
        self, student_id: str | int
    ) -> PersonalLearningProfile | None:
        """Return last stored profile for the student, if any."""
