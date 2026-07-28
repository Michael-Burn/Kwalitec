"""Adaptive Assessment product telemetry — behavioural events only.

Never capture educational answers, item content, scores, Twin state, or
other learner educational state. Privacy-preserving operational signals.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Protocol
from uuid import uuid4

# Payload keys that must never appear (educational / PII-adjacent content).
FORBIDDEN_PAYLOAD_KEYS: frozenset[str] = frozenset(
    {
        "answer",
        "answers",
        "response",
        "responses",
        "item_stem",
        "question_text",
        "score",
        "mastery",
        "readiness_score",
        "twin_state",
        "learner_state",
        "correct",
        "incorrect",
        "grade",
        "pass",
        "fail",
    }
)


class TelemetryEventName(StrEnum):
    """Allowlisted Adaptive Assessment product telemetry event names."""

    ADAPTIVE_ASSESSMENT_VIEWED = "AdaptiveAssessmentViewed"
    QUICK_CHECK_STARTED = "QuickCheckStarted"
    QUICK_CHECK_DISMISSED = "QuickCheckDismissed"
    QUICK_CHECK_COMPLETED = "QuickCheckCompleted"
    ASSESSMENT_DEFERRED = "AssessmentDeferred"
    ASSESSMENT_EXPLAINED = "AssessmentExplained"
    # ILE-001C — behavioural framing events (never educational outcomes).
    CONTEXT_VIEWED = "ContextViewed"
    WHY_RECOMMENDATION_OPENED = "WhyRecommendationOpened"
    EXPLANATION_EXPANDED = "ExplanationExpanded"
    RECOMMENDATION_ACCEPTED = "RecommendationAccepted"
    RECOMMENDATION_DEFERRED = "RecommendationDeferred"
    REFLECTION_COMPLETED = "ReflectionCompleted"


@dataclass(frozen=True)
class AdaptiveAssessmentTelemetryEvent:
    """Immutable behavioural product event (no educational payload).

    Attributes:
        event_name: Allowlisted event name.
        occurred_at: Event timestamp (UTC).
        event_id: Stable UUID hex.
        session_type_id: Optional session type identifier (product metadata).
        subject_code: Optional subject code (not educational state).
        payload: Metadata-only fields (flags, UI surface ids, durations).
    """

    event_name: str
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(tz=UTC)
    )
    event_id: str = field(default_factory=lambda: uuid4().hex)
    session_type_id: str = ""
    subject_code: str = ""
    payload: dict[str, Any] = field(default_factory=dict)


class ProductTelemetrySink(Protocol):
    """Port for emitting product telemetry (tests / future analytics bridge)."""

    def emit(self, event: AdaptiveAssessmentTelemetryEvent) -> None:
        ...


class InMemoryTelemetrySink:
    """Test / local sink that retains events in process memory."""

    def __init__(self) -> None:
        self.events: list[AdaptiveAssessmentTelemetryEvent] = []

    def emit(self, event: AdaptiveAssessmentTelemetryEvent) -> None:
        self.events.append(event)


class ProductTelemetryRecorder:
    """Validates and records Adaptive Assessment behavioural events."""

    def __init__(self, sink: ProductTelemetrySink | None = None) -> None:
        self._sink = sink if sink is not None else InMemoryTelemetrySink()

    @property
    def sink(self) -> ProductTelemetrySink:
        return self._sink

    def record(self, event: AdaptiveAssessmentTelemetryEvent) -> None:
        """Validate privacy constraints then emit."""
        _assert_event_safe(event)
        self._sink.emit(event)


def build_telemetry_event(
    event_name: str | TelemetryEventName,
    *,
    session_type_id: str = "",
    subject_code: str = "",
    payload: dict[str, Any] | None = None,
    occurred_at: datetime | None = None,
    event_id: str | None = None,
) -> AdaptiveAssessmentTelemetryEvent:
    """Construct a validated behavioural telemetry event."""
    name = str(event_name)
    if name not in {e.value for e in TelemetryEventName}:
        raise ValueError(f"unknown Adaptive Assessment telemetry event: {name}")
    event = AdaptiveAssessmentTelemetryEvent(
        event_name=name,
        session_type_id=(session_type_id or "").strip(),
        subject_code=(subject_code or "").strip(),
        payload=dict(payload or {}),
        occurred_at=occurred_at
        if occurred_at is not None
        else datetime.now(tz=UTC),
        event_id=(event_id or "").strip() or uuid4().hex,
    )
    _assert_event_safe(event)
    return event


def _assert_event_safe(event: AdaptiveAssessmentTelemetryEvent) -> None:
    """Raise if payload contains educational or forbidden keys."""
    for key in event.payload:
        lowered = str(key).strip().lower()
        if lowered in FORBIDDEN_PAYLOAD_KEYS:
            raise ValueError(
                "Adaptive Assessment telemetry must not capture educational "
                f"or learner-state fields: {key!r}"
            )
        # Nested dicts: reject recursively on keys only.
        value = event.payload[key]
        if isinstance(value, dict):
            nested = AdaptiveAssessmentTelemetryEvent(
                event_name=event.event_name,
                payload=value,
            )
            _assert_event_safe(nested)
