"""Adaptive Study Workspace enumerations.

Presentation vocabulary only — never mastery bands, recommendation
categories, or educational reasoning codes exposed as domain types.
"""

from __future__ import annotations

from enum import StrEnum


class SessionPresence(StrEnum):
    """Whether a current study session is available to the workspace."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class PriorityLabel(StrEnum):
    """Student-facing mission priority labels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class ObjectiveStatus(StrEnum):
    """Status of one composed workspace objective."""

    CURRENT = "current"
    COMPLETED = "completed"
    REMAINING = "remaining"
    SKIPPED = "skipped"


class FocusPromptKind(StrEnum):
    """Deterministic focus prompts — never newly generated recommendations."""

    CONTINUE_CURRENT_OBJECTIVE = "continue_current_objective"
    FINISH_CURRENT_STEP = "finish_current_step"
    PREPARE_CHECKPOINT = "prepare_checkpoint"
    REVIEW_PREVIOUS_MISTAKE = "review_previous_mistake"
    NONE = "none"


class QualityIndicatorKind(StrEnum):
    """Study-quality indicators projected from existing execution metrics."""

    COMPLETION_RATE = "completion_rate"
    TIME_ON_TASK = "time_on_task"
    CONFIDENCE_TREND = "confidence_trend"
    REFLECTION_ACTIVITY = "reflection_activity"


class ResourceKind(StrEnum):
    """Kinds of study resources surfaced in the workspace."""

    TASK = "task"
    REFERENCE = "reference"
    TIP = "tip"
    CHECKPOINT = "checkpoint"
    OTHER = "other"


class TimerDisplayState(StrEnum):
    """Display state for session timing — never an active timer implementation."""

    IDLE = "idle"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETE = "complete"
    UNAVAILABLE = "unavailable"
