"""Spacing Scheduler domain — time-based due scheduling only.

This package is the sole lawful authority for whether a reviewable learning
block is due for return based on elapsed time. It never encodes weakness,
mastery, accuracy, or any other performance judgement.

See ``app.application.spacing_scheduler`` for the application entry point.
"""

from __future__ import annotations

from app.domain.spacing_scheduler.policy import SpacingIntervalPolicy
from app.domain.spacing_scheduler.scheduler import SpacingScheduler
from app.domain.spacing_scheduler.types import (
    ExposureKind,
    ReviewableUnitId,
    SchedulingDecision,
    SchedulingStatus,
    SpacingState,
)

__all__ = [
    "ExposureKind",
    "ReviewableUnitId",
    "SchedulingDecision",
    "SchedulingStatus",
    "SpacingIntervalPolicy",
    "SpacingScheduler",
    "SpacingState",
]
