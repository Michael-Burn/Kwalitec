"""Mission Execution Engine enumerations.

Lifecycle and execution vocabulary for student interaction with mission
work. Categories here describe runtime state — never mastery bands,
recommendation intent, or mission generation.
"""

from __future__ import annotations

from enum import StrEnum


class ExecutionStatus(StrEnum):
    """Immutable lifecycle status of a MissionExecution."""

    PLANNED = "planned"
    STARTED = "started"
    PAUSED = "paused"
    RESUMED = "resumed"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    EXPIRED = "expired"


class ExecutionEventKind(StrEnum):
    """Kind of immutable mission execution event."""

    MISSION_STARTED = "mission_started"
    MISSION_PAUSED = "mission_paused"
    MISSION_RESUMED = "mission_resumed"
    STEP_COMPLETED = "step_completed"
    STEP_SKIPPED = "step_skipped"
    CONFIDENCE_RECORDED = "confidence_recorded"
    REFLECTION_RECORDED = "reflection_recorded"
    MISSION_COMPLETED = "mission_completed"
    MISSION_ABANDONED = "mission_abandoned"
    MISSION_EXPIRED = "mission_expired"


class ConfidenceTrend(StrEnum):
    """Deterministic trend derived from confidence history."""

    NONE = "none"
    STABLE = "stable"
    RISING = "rising"
    FALLING = "falling"
    MIXED = "mixed"


class StepOutcome(StrEnum):
    """Outcome recorded for a single mission step."""

    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"
