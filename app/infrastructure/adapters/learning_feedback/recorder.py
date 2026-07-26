"""LearningFeedbackRecorder — process-local observed evidence buffer (EP-003.4).

Records immutable LearningFeedbackEvent records for future analytics.
Never interprets educationally, never changes Runtime A decisions, never
raises into student-facing control flows.
"""

from __future__ import annotations

import logging
from collections import deque
from threading import Lock
from typing import Any

from app.infrastructure.adapters.learning_feedback.contracts import (
    OBSERVABLE_FEEDBACK_EVENTS,
    REASON_FLAG_OFF,
    REASON_RECORDER_ERROR,
    REASON_SCHEMA_INVALID,
    REASON_UNKNOWN_EVENT,
    RECORD_STATUS_FAILED,
    RECORD_STATUS_RECORDED,
    RECORD_STATUS_SKIPPED,
    FeedbackRecordResult,
    LearningFeedbackEvent,
)

logger = logging.getLogger(__name__)

_DEFAULT_BUFFER_CAP = 10_000


class LearningFeedbackRecorder:
    """Record observed behavioural feedback into a process-local buffer.

    Responsibilities:
    - validate and append immutable events
    - respect feature flags
    - support dependency injection / queries for tests

    Non-responsibilities: educational interpretation, Twin writes,
    recommendation / readiness / planning decisions, durable persistence.
    """

    RECORDER_ID = "learning_feedback_recorder"
    RECORDER_VERSION = "1.0.0-ep003.4"

    def __init__(
        self,
        *,
        enabled: bool = True,
        buffer_cap: int = _DEFAULT_BUFFER_CAP,
    ) -> None:
        self._enabled = bool(enabled)
        self._buffer_cap = max(1, int(buffer_cap))
        self._buffer: deque[LearningFeedbackEvent] = deque(
            maxlen=self._buffer_cap
        )
        self._lock = Lock()
        self._recorded_count = 0
        self._skipped_count = 0
        self._failed_count = 0

    @property
    def recorder_id(self) -> str:
        return self.RECORDER_ID

    @property
    def recorder_version(self) -> str:
        return self.RECORDER_VERSION

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def recorded_count(self) -> int:
        return self._recorded_count

    @property
    def skipped_count(self) -> int:
        return self._skipped_count

    @property
    def failed_count(self) -> int:
        return self._failed_count

    def record(self, event: LearningFeedbackEvent) -> FeedbackRecordResult:
        """Append one observed event, or skip / fail without raising."""
        if not self._enabled:
            self._skipped_count += 1
            return FeedbackRecordResult(
                ok=False,
                status=RECORD_STATUS_SKIPPED,
                event=event if isinstance(event, LearningFeedbackEvent) else None,
                reason=REASON_FLAG_OFF,
                message="ENABLE_LEARNING_FEEDBACK is OFF",
            )
        if not isinstance(event, LearningFeedbackEvent):
            self._failed_count += 1
            return FeedbackRecordResult(
                ok=False,
                status=RECORD_STATUS_FAILED,
                reason=REASON_SCHEMA_INVALID,
                message="event must be a LearningFeedbackEvent",
            )
        if event.event_type not in OBSERVABLE_FEEDBACK_EVENTS:
            self._failed_count += 1
            return FeedbackRecordResult(
                ok=False,
                status=RECORD_STATUS_FAILED,
                event=event,
                reason=REASON_UNKNOWN_EVENT,
                message=f"event_type {event.event_type!r} not observable",
            )
        try:
            with self._lock:
                self._buffer.append(event)
                self._recorded_count += 1
        except Exception as exc:  # noqa: BLE001 — recorder must not raise
            logger.warning(
                "learning_feedback_record_failed feedback_id=%s error=%s",
                getattr(event, "feedback_id", ""),
                exc,
            )
            self._failed_count += 1
            return FeedbackRecordResult(
                ok=False,
                status=RECORD_STATUS_FAILED,
                event=event,
                reason=REASON_RECORDER_ERROR,
                message=str(exc),
            )
        return FeedbackRecordResult(
            ok=True,
            status=RECORD_STATUS_RECORDED,
            event=event,
            message="recorded in learning feedback buffer",
        )

    def list_events(
        self,
        *,
        student_id: str | None = None,
        event_type: str | None = None,
        limit: int = 100,
    ) -> list[LearningFeedbackEvent]:
        """Return recent buffered events (newest last), optionally filtered."""
        with self._lock:
            items = list(self._buffer)
        if student_id is not None:
            sid = str(student_id).strip()
            items = [e for e in items if e.student_id == sid]
        if event_type is not None:
            et = str(event_type).strip().lower()
            items = [e for e in items if e.event_type == et]
        if limit > 0:
            items = items[-limit:]
        return items

    def clear(self) -> None:
        """Drop buffered events (tests / ops)."""
        with self._lock:
            self._buffer.clear()

    def stats(self) -> dict[str, Any]:
        """Operational counters (not educational metrics)."""
        with self._lock:
            size = len(self._buffer)
        return {
            "buffer_size": size,
            "buffer_cap": self._buffer_cap,
            "recorded_count": self._recorded_count,
            "skipped_count": self._skipped_count,
            "failed_count": self._failed_count,
            "enabled": self._enabled,
            "recorder_id": self.RECORDER_ID,
            "recorder_version": self.RECORDER_VERSION,
        }


def build_learning_feedback_recorder(
    *,
    enabled: bool,
    buffer_cap: int = _DEFAULT_BUFFER_CAP,
) -> LearningFeedbackRecorder | None:
    """DI helper — construct recorder only when ENABLE_LEARNING_FEEDBACK is ON."""
    if not enabled:
        return None
    return LearningFeedbackRecorder(enabled=True, buffer_cap=buffer_cap)
