"""Immutable Experience Observation contracts (P2-MS006).

Factual Experience → Evidence bridge DTOs only. No educational
interpretation, scoring, recommendations, or authority changes.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable

CONTRACT_VERSION = "p2.ms006.1"
AUTHORITY_EXPERIENCE_OBSERVATION = "experience_observation"

# Presentation events mapped into immutable observations (directive §6).
EXPERIENCE_EVENT_MISSION_STARTED = "mission_started"
EXPERIENCE_EVENT_SESSION_STARTED = "session_started"
EXPERIENCE_EVENT_SESSION_COMPLETED = "session_completed"
EXPERIENCE_EVENT_REFLECTION_STARTED = "reflection_started"
EXPERIENCE_EVENT_REFLECTION_COMPLETED = "reflection_completed"
EXPERIENCE_EVENT_REFLECTION_SKIPPED = "reflection_skipped"

OBSERVABLE_EXPERIENCE_EVENTS = frozenset(
    {
        EXPERIENCE_EVENT_MISSION_STARTED,
        EXPERIENCE_EVENT_SESSION_STARTED,
        EXPERIENCE_EVENT_SESSION_COMPLETED,
        EXPERIENCE_EVENT_REFLECTION_STARTED,
        EXPERIENCE_EVENT_REFLECTION_COMPLETED,
        EXPERIENCE_EVENT_REFLECTION_SKIPPED,
    }
)

PUBLISH_STATUS_PUBLISHED = "published"
PUBLISH_STATUS_SKIPPED = "skipped"
PUBLISH_STATUS_FAILED = "failed"
PUBLISH_STATUSES = frozenset(
    {
        PUBLISH_STATUS_PUBLISHED,
        PUBLISH_STATUS_SKIPPED,
        PUBLISH_STATUS_FAILED,
    }
)

REASON_FLAG_OFF = "experience_observation_flag_off"
REASON_EVIDENCE_UNAVAILABLE = "evidence_platform_unavailable"
REASON_NOT_OBSERVABLE = "experience_event_not_observable"
REASON_EVIDENCE_REJECTED = "evidence_intake_rejected"


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    raw = dict(value or {})
    frozen: dict[str, Any] = {}
    for key, item in raw.items():
        if isinstance(item, Mapping):
            frozen[str(key)] = dict(item)
        elif isinstance(item, list | tuple):
            frozen[str(key)] = list(item)
        else:
            frozen[str(key)] = item
    return MappingProxyType(frozen)


def _freeze_metadata(
    value: Mapping[str, str] | tuple[tuple[str, str], ...] | None,
) -> tuple[tuple[str, str], ...]:
    if value is None:
        return ()
    if isinstance(value, Mapping):
        return tuple((str(k), str(v)) for k, v in sorted(value.items()))
    return tuple((str(k), str(v)) for k, v in value)


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


def deterministic_observation_id(
    *,
    student_id: str,
    timestamp: str,
    journey_stage: str,
    experience_event: str,
    presentation_state: Mapping[str, Any],
    metadata: tuple[tuple[str, str], ...],
    correlation_id: str,
    contract_version: str = CONTRACT_VERSION,
) -> str:
    """Derive observation_id from factual material fields (no wall-clock)."""
    material = {
        "contract_version": contract_version,
        "correlation_id": correlation_id,
        "experience_event": experience_event,
        "journey_stage": journey_stage,
        "metadata": list(metadata),
        "presentation_state": dict(presentation_state),
        "student_id": student_id,
        "timestamp": timestamp,
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"expobs-{digest[:32]}"


@dataclass(frozen=True)
class ExperienceObservation:
    """Immutable factual observation from the Experience Layer.

    Represents what happened in presentation only. Must not carry
    educational conclusions, scores, mastery, or recommendations.
    """

    observation_id: str
    timestamp: str
    journey_stage: str
    experience_event: str
    presentation_state: Mapping[str, Any] = field(default_factory=dict)
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    correlation_id: str = ""
    student_id: str = ""
    contract_version: str = CONTRACT_VERSION
    authority: str = AUTHORITY_EXPERIENCE_OBSERVATION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "observation_id", (self.observation_id or "").strip()
        )
        object.__setattr__(self, "timestamp", (self.timestamp or "").strip())
        object.__setattr__(
            self, "journey_stage", (self.journey_stage or "").strip().lower()
        )
        object.__setattr__(
            self,
            "experience_event",
            (self.experience_event or "").strip().lower(),
        )
        object.__setattr__(
            self, "presentation_state", _freeze_mapping(self.presentation_state)
        )
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))
        object.__setattr__(
            self, "correlation_id", (self.correlation_id or "").strip()
        )
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self,
            "contract_version",
            (self.contract_version or CONTRACT_VERSION).strip(),
        )
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_EXPERIENCE_OBSERVATION).strip(),
        )
        if not self.observation_id:
            raise ValueError("observation_id is required")
        if not self.timestamp:
            raise ValueError("timestamp is required")
        if not self.experience_event:
            raise ValueError("experience_event is required")

    def to_canonical_dict(self) -> dict[str, Any]:
        """Deterministic dict projection for tests / fingerprints."""
        return {
            "authority": self.authority,
            "contract_version": self.contract_version,
            "correlation_id": self.correlation_id,
            "experience_event": self.experience_event,
            "journey_stage": self.journey_stage,
            "metadata": list(self.metadata),
            "observation_id": self.observation_id,
            "presentation_state": dict(self.presentation_state),
            "student_id": self.student_id,
            "timestamp": self.timestamp,
        }

    def serialize(self) -> str:
        """Deterministic serialization of the observation."""
        return serialize_canonical(self.to_canonical_dict())


@dataclass(frozen=True)
class ObservationPublishResult:
    """Immutable result of an observation publish attempt.

    Publishing is observational only — never educational authority.
    """

    ok: bool
    status: str
    observation: ExperienceObservation | None = None
    evidence_id: str = ""
    reason: str = ""
    message: str = ""

    def __post_init__(self) -> None:
        status = (self.status or "").strip().lower()
        if status not in PUBLISH_STATUSES:
            raise ValueError(f"unknown publish status: {self.status!r}")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "ok", bool(self.ok))
        object.__setattr__(self, "evidence_id", (self.evidence_id or "").strip())
        object.__setattr__(self, "reason", (self.reason or "").strip())
        object.__setattr__(self, "message", (self.message or "").strip())


@runtime_checkable
class EvidenceObservationPort(Protocol):
    """Public Evidence intake surface used by the observation publisher.

    Callers must use this contract only — no repository / collector bypass.
    """

    def collect_event(self, event: Any) -> Any:
        """Collect an ObservedEvent into an EvidenceRecord."""


@runtime_checkable
class ExperienceObservationPublisherPort(Protocol):
    """Publisher surface for immutable Experience observations."""

    def publish(
        self, observation: ExperienceObservation
    ) -> ObservationPublishResult:
        """Publish one observation to Evidence (or skip when gated)."""
