"""Immutable Learning Feedback contracts (EP-003.4).

Records observed student behavioural evidence only. Does not infer mastery,
readiness, recommendation quality, or any educational conclusion.

Constitutional rules:
- Observed evidence precedes educational inference (Educational Constitution
  Art. III §2).
- Recommendation accept/dismiss is preference history, never mastery evidence
  (Art. V §2).
- Feedback infrastructure never makes educational decisions.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable

CONTRACT_VERSION = "ep003.4.1"
AUTHORITY_LEARNING_FEEDBACK = "learning_feedback"

# Observed behavioural event types (evidence to capture).
FEEDBACK_EVENT_PLAN_COMPLETED = "plan_completed"
FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED = "recommendation_accepted"
FEEDBACK_EVENT_RECOMMENDATION_DISMISSED = "recommendation_dismissed"
FEEDBACK_EVENT_SESSION_MISSED = "session_missed"
FEEDBACK_EVENT_RECOVERY_APPLIED = "recovery_applied"
FEEDBACK_EVENT_REVISION_ADHERED = "revision_adhered"
FEEDBACK_EVENT_REVISION_DEFERRED = "revision_deferred"
FEEDBACK_EVENT_STUDY_CONSISTENCY = "study_consistency_observed"
# EP-008.3A — observational commitment / follow-through (research only).
FEEDBACK_EVENT_COMMITMENT_CONFIRMED = "commitment_confirmed"
FEEDBACK_EVENT_COMMITMENT_DEFERRED = "commitment_deferred"
FEEDBACK_EVENT_COMMITMENT_COMPLETED = "commitment_completed"
FEEDBACK_EVENT_REFLECTION_VIEWED = "reflection_viewed"

OBSERVABLE_FEEDBACK_EVENTS = frozenset(
    {
        FEEDBACK_EVENT_PLAN_COMPLETED,
        FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
        FEEDBACK_EVENT_RECOMMENDATION_DISMISSED,
        FEEDBACK_EVENT_SESSION_MISSED,
        FEEDBACK_EVENT_RECOVERY_APPLIED,
        FEEDBACK_EVENT_REVISION_ADHERED,
        FEEDBACK_EVENT_REVISION_DEFERRED,
        FEEDBACK_EVENT_STUDY_CONSISTENCY,
        FEEDBACK_EVENT_COMMITMENT_CONFIRMED,
        FEEDBACK_EVENT_COMMITMENT_DEFERRED,
        FEEDBACK_EVENT_COMMITMENT_COMPLETED,
        FEEDBACK_EVENT_REFLECTION_VIEWED,
    }
)

# Claim boundaries — what the event may lawfully assert.
CLAIM_OBSERVED_BEHAVIOUR = "observed_behaviour"
CLAIM_PREFERENCE_JOURNAL = "preference_journal"
CLAIM_PLAN_INTERACTION = "plan_interaction"
CLAIM_STUDY_HABIT_SIGNAL = "study_habit_signal"

ALLOWED_CLAIM_BOUNDARIES = frozenset(
    {
        CLAIM_OBSERVED_BEHAVIOUR,
        CLAIM_PREFERENCE_JOURNAL,
        CLAIM_PLAN_INTERACTION,
        CLAIM_STUDY_HABIT_SIGNAL,
    }
)

# Explicitly forbidden as educational conclusions on feedback records.
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
    }
)

# Source authorities permitted to emit (Runtime A ownership).
SOURCE_RECOMMENDATION = "recommendation_service"
SOURCE_READINESS = "readiness_service"
SOURCE_PLANNING = "planning_service"

ALLOWED_SOURCE_AUTHORITIES = frozenset(
    {
        SOURCE_RECOMMENDATION,
        SOURCE_READINESS,
        SOURCE_PLANNING,
    }
)

# Evidence kind — always observed; never conclusion.
EVIDENCE_KIND_OBSERVED = "observed_evidence"

RECORD_STATUS_RECORDED = "recorded"
RECORD_STATUS_SKIPPED = "skipped"
RECORD_STATUS_FAILED = "failed"
RECORD_STATUSES = frozenset(
    {
        RECORD_STATUS_RECORDED,
        RECORD_STATUS_SKIPPED,
        RECORD_STATUS_FAILED,
    }
)

REASON_FLAG_OFF = "learning_feedback_flag_off"
REASON_SCHEMA_INVALID = "feedback_schema_invalid"
REASON_FORBIDDEN_INFERENCE = "forbidden_inference_payload"
REASON_UNKNOWN_EVENT = "feedback_event_unknown"
REASON_UNKNOWN_SOURCE = "feedback_source_unknown"
REASON_RECORDER_ERROR = "recorder_error"


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    raw = dict(value or {})
    frozen: dict[str, Any] = {}
    for key, item in raw.items():
        key_s = str(key)
        if key_s.lower() in FORBIDDEN_INFERENCE_KEYS:
            raise ValueError(
                f"forbidden inference key in payload: {key_s!r}"
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


def deterministic_feedback_id(
    *,
    student_id: str,
    timestamp: str,
    event_type: str,
    source_authority: str,
    claim_boundary: str,
    payload: Mapping[str, Any],
    correlation_id: str,
    contract_version: str = CONTRACT_VERSION,
) -> str:
    """Derive feedback_id from factual material fields (no wall-clock)."""
    material = {
        "claim_boundary": claim_boundary,
        "contract_version": contract_version,
        "correlation_id": correlation_id,
        "event_type": event_type,
        "payload": dict(payload),
        "source_authority": source_authority,
        "student_id": student_id,
        "timestamp": timestamp,
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"lfeed-{digest[:32]}"


@dataclass(frozen=True)
class LearningFeedbackEvent:
    """Immutable observed behavioural feedback event.

    Every field is factual observation or provenance. Must not carry
    educational conclusions, mastery scores, or readiness judgements.
    """

    feedback_id: str
    timestamp: str
    event_type: str
    source_authority: str
    claim_boundary: str
    student_id: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    correlation_id: str = ""
    evidence_kind: str = EVIDENCE_KIND_OBSERVED
    contract_version: str = CONTRACT_VERSION
    authority: str = AUTHORITY_LEARNING_FEEDBACK

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "feedback_id", (self.feedback_id or "").strip()
        )
        object.__setattr__(self, "timestamp", (self.timestamp or "").strip())
        object.__setattr__(
            self, "event_type", (self.event_type or "").strip().lower()
        )
        object.__setattr__(
            self,
            "source_authority",
            (self.source_authority or "").strip().lower(),
        )
        object.__setattr__(
            self,
            "claim_boundary",
            (self.claim_boundary or "").strip().lower(),
        )
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self, "correlation_id", (self.correlation_id or "").strip()
        )
        object.__setattr__(
            self,
            "evidence_kind",
            (self.evidence_kind or EVIDENCE_KIND_OBSERVED).strip().lower(),
        )
        object.__setattr__(
            self,
            "contract_version",
            (self.contract_version or CONTRACT_VERSION).strip(),
        )
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_LEARNING_FEEDBACK).strip(),
        )
        object.__setattr__(self, "payload", _freeze_mapping(self.payload))

        if not self.feedback_id:
            raise ValueError("feedback_id is required")
        if not self.timestamp:
            raise ValueError("timestamp is required")
        if not self.student_id:
            raise ValueError("student_id is required")
        if self.event_type not in OBSERVABLE_FEEDBACK_EVENTS:
            raise ValueError(f"unknown feedback event_type: {self.event_type!r}")
        if self.source_authority not in ALLOWED_SOURCE_AUTHORITIES:
            raise ValueError(
                f"unknown source_authority: {self.source_authority!r}"
            )
        if self.claim_boundary not in ALLOWED_CLAIM_BOUNDARIES:
            raise ValueError(
                f"unknown claim_boundary: {self.claim_boundary!r}"
            )
        if self.evidence_kind != EVIDENCE_KIND_OBSERVED:
            raise ValueError(
                "evidence_kind must be observed_evidence "
                f"(got {self.evidence_kind!r})"
            )

    def to_canonical_dict(self) -> dict[str, Any]:
        """Deterministic dict projection for tests / fingerprints."""
        return {
            "authority": self.authority,
            "claim_boundary": self.claim_boundary,
            "contract_version": self.contract_version,
            "correlation_id": self.correlation_id,
            "event_type": self.event_type,
            "evidence_kind": self.evidence_kind,
            "feedback_id": self.feedback_id,
            "payload": dict(self.payload),
            "source_authority": self.source_authority,
            "student_id": self.student_id,
            "timestamp": self.timestamp,
        }

    def serialize(self) -> str:
        """Deterministic serialization of the event."""
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class FeedbackRecordResult:
    """Immutable result of a feedback record attempt.

    Recording is observational only — never educational authority.
    """

    ok: bool
    status: str
    event: LearningFeedbackEvent | None = None
    reason: str = ""
    message: str = ""

    def __post_init__(self) -> None:
        status = (self.status or "").strip().lower()
        if status not in RECORD_STATUSES:
            raise ValueError(f"unknown record status: {self.status!r}")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "ok", bool(self.ok))
        object.__setattr__(self, "reason", (self.reason or "").strip())
        object.__setattr__(self, "message", (self.message or "").strip())


@runtime_checkable
class LearningFeedbackRecorderPort(Protocol):
    """Public recorder surface used by Runtime A emitters."""

    def record(self, event: LearningFeedbackEvent) -> FeedbackRecordResult:
        """Record one observed feedback event (or skip when gated)."""
