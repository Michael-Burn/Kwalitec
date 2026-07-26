"""Immutable JourneyTrace — operational pipeline visibility (P2-MS007).

Traces JourneyEvent → ExperienceObservation → Evidence intake without
carrying student-identifying data or educational conclusions.
"""

from __future__ import annotations

import hashlib
from collections import deque
from dataclasses import dataclass, field
from threading import Lock
from typing import Any

from app.infrastructure.adapters.experience_observation.contracts import (
    serialize_canonical,
)

CONTRACT_VERSION = "p2.ms007.1"
AUTHORITY_JOURNEY_TRACE = "experience_diagnostics"

# Pipeline stages along the observation path (operational vocabulary only).
PIPELINE_STAGE_JOURNEY_EVENT = "journey_event"
PIPELINE_STAGE_ASSEMBLED = "assembled"
PIPELINE_STAGE_PUBLISH_ATTEMPTED = "publish_attempted"
PIPELINE_STAGE_EVIDENCE_ACK = "evidence_ack"
PIPELINE_STAGE_SKIPPED = "skipped"
PIPELINE_STAGE_FAILED = "failed"

PIPELINE_STAGES = frozenset(
    {
        PIPELINE_STAGE_JOURNEY_EVENT,
        PIPELINE_STAGE_ASSEMBLED,
        PIPELINE_STAGE_PUBLISH_ATTEMPTED,
        PIPELINE_STAGE_EVIDENCE_ACK,
        PIPELINE_STAGE_SKIPPED,
        PIPELINE_STAGE_FAILED,
    }
)

# Observation statuses mirrored from publish results (+ pending for early stages).
OBSERVATION_STATUS_PENDING = "pending"
OBSERVATION_STATUS_PUBLISHED = "published"
OBSERVATION_STATUS_SKIPPED = "skipped"
OBSERVATION_STATUS_FAILED = "failed"
OBSERVATION_STATUSES = frozenset(
    {
        OBSERVATION_STATUS_PENDING,
        OBSERVATION_STATUS_PUBLISHED,
        OBSERVATION_STATUS_SKIPPED,
        OBSERVATION_STATUS_FAILED,
    }
)

DEFAULT_TRACE_CAPACITY = 256


def deterministic_trace_id(
    *,
    correlation_id: str,
    journey_stage: str,
    experience_event: str,
    pipeline_stage: str,
    timestamp: str,
    observation_id: str = "",
    contract_version: str = CONTRACT_VERSION,
) -> str:
    """Derive trace_id from operational material fields (no wall-clock invent)."""
    material = {
        "contract_version": contract_version,
        "correlation_id": correlation_id,
        "experience_event": experience_event,
        "journey_stage": journey_stage,
        "observation_id": observation_id,
        "pipeline_stage": pipeline_stage,
        "timestamp": timestamp,
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"jtrace-{digest[:32]}"


@dataclass(frozen=True)
class JourneyTrace:
    """Immutable operational record of one observation-pipeline step.

    Must not contain student identifiers, educational scores, mastery,
    recommendations, or behavioural conclusions.
    """

    trace_id: str
    correlation_id: str
    journey_stage: str
    experience_event: str
    observation_status: str
    timestamp: str
    pipeline_stage: str
    observation_id: str = ""
    evidence_id: str = ""
    reason: str = ""
    latency_ms: float | None = None
    contract_version: str = CONTRACT_VERSION
    authority: str = AUTHORITY_JOURNEY_TRACE

    def __post_init__(self) -> None:
        object.__setattr__(self, "trace_id", (self.trace_id or "").strip())
        object.__setattr__(
            self, "correlation_id", (self.correlation_id or "").strip()
        )
        object.__setattr__(
            self, "journey_stage", (self.journey_stage or "").strip().lower()
        )
        object.__setattr__(
            self,
            "experience_event",
            (self.experience_event or "").strip().lower(),
        )
        status = (self.observation_status or "").strip().lower()
        if status not in OBSERVATION_STATUSES:
            raise ValueError(f"unknown observation_status: {self.observation_status!r}")
        object.__setattr__(self, "observation_status", status)
        object.__setattr__(self, "timestamp", (self.timestamp or "").strip())
        stage = (self.pipeline_stage or "").strip().lower()
        if stage not in PIPELINE_STAGES:
            raise ValueError(f"unknown pipeline_stage: {self.pipeline_stage!r}")
        object.__setattr__(self, "pipeline_stage", stage)
        object.__setattr__(
            self, "observation_id", (self.observation_id or "").strip()
        )
        object.__setattr__(self, "evidence_id", (self.evidence_id or "").strip())
        object.__setattr__(self, "reason", (self.reason or "").strip())
        if self.latency_ms is not None:
            object.__setattr__(self, "latency_ms", float(self.latency_ms))
        object.__setattr__(
            self,
            "contract_version",
            (self.contract_version or CONTRACT_VERSION).strip(),
        )
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_JOURNEY_TRACE).strip(),
        )
        if not self.trace_id:
            raise ValueError("trace_id is required")
        if not self.timestamp:
            raise ValueError("timestamp is required")
        if not self.experience_event:
            raise ValueError("experience_event is required")

    def to_canonical_dict(self) -> dict[str, Any]:
        """Deterministic dict projection (ops / tests). No PII fields."""
        return {
            "authority": self.authority,
            "contract_version": self.contract_version,
            "correlation_id": self.correlation_id,
            "evidence_id": self.evidence_id,
            "experience_event": self.experience_event,
            "journey_stage": self.journey_stage,
            "latency_ms": self.latency_ms,
            "observation_id": self.observation_id,
            "observation_status": self.observation_status,
            "pipeline_stage": self.pipeline_stage,
            "reason": self.reason,
            "timestamp": self.timestamp,
            "trace_id": self.trace_id,
        }


def build_journey_trace(
    *,
    correlation_id: str,
    journey_stage: str,
    experience_event: str,
    observation_status: str,
    timestamp: str,
    pipeline_stage: str,
    observation_id: str = "",
    evidence_id: str = "",
    reason: str = "",
    latency_ms: float | None = None,
) -> JourneyTrace:
    """Construct an immutable JourneyTrace with a deterministic trace_id."""
    corr = (correlation_id or "").strip()
    stage = (journey_stage or "").strip().lower()
    event = (experience_event or "").strip().lower()
    pipe = (pipeline_stage or "").strip().lower()
    ts = (timestamp or "").strip()
    obs_id = (observation_id or "").strip()
    trace_id = deterministic_trace_id(
        correlation_id=corr,
        journey_stage=stage,
        experience_event=event,
        pipeline_stage=pipe,
        timestamp=ts,
        observation_id=obs_id,
    )
    return JourneyTrace(
        trace_id=trace_id,
        correlation_id=corr,
        journey_stage=stage,
        experience_event=event,
        observation_status=observation_status,
        timestamp=ts,
        pipeline_stage=pipe,
        observation_id=obs_id,
        evidence_id=(evidence_id or "").strip(),
        reason=(reason or "").strip(),
        latency_ms=latency_ms,
    )


@dataclass
class JourneyTraceStore:
    """Bounded in-memory ring of JourneyTrace records (no persistence)."""

    capacity: int = DEFAULT_TRACE_CAPACITY
    _lock: Lock = field(default_factory=Lock, repr=False)
    _traces: deque[JourneyTrace] = field(default_factory=deque, repr=False)

    def __post_init__(self) -> None:
        cap = max(1, int(self.capacity))
        object.__setattr__(self, "capacity", cap)
        object.__setattr__(self, "_traces", deque(maxlen=cap))

    def append(self, trace: JourneyTrace) -> None:
        """Append one immutable trace (drops oldest when at capacity)."""
        if not isinstance(trace, JourneyTrace):
            raise TypeError("trace must be a JourneyTrace")
        with self._lock:
            self._traces.append(trace)

    def recent(self, *, limit: int | None = None) -> tuple[JourneyTrace, ...]:
        """Return recent traces newest-last (ops order)."""
        with self._lock:
            items = tuple(self._traces)
        if limit is None:
            return items
        lim = max(0, int(limit))
        if lim == 0:
            return ()
        return items[-lim:]

    def by_correlation_id(self, correlation_id: str) -> tuple[JourneyTrace, ...]:
        """Return all stored traces for a correlation id (pipeline lineage)."""
        corr = (correlation_id or "").strip()
        if not corr:
            return ()
        with self._lock:
            return tuple(t for t in self._traces if t.correlation_id == corr)

    def clear(self) -> None:
        """Drop all stored traces (test / ops reset)."""
        with self._lock:
            self._traces.clear()

    def __len__(self) -> int:
        with self._lock:
            return len(self._traces)


def build_journey_trace_store(
    *, capacity: int = DEFAULT_TRACE_CAPACITY
) -> JourneyTraceStore:
    """DI helper for an in-memory JourneyTraceStore."""
    return JourneyTraceStore(capacity=capacity)
