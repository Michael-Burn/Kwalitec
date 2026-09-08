"""Spacing Scheduler application package — canonical due-state authority.

Sole lawful entry for time-based review scheduling. Does not touch Revision,
the daily study composer, or the Adaptive Decision Engine.
"""

from __future__ import annotations

from app.application.spacing_scheduler.service import (
    SpacingSchedulerService,
    get_spacing_scheduler,
    reset_canonical_spacing_scheduler_for_tests,
)
from app.application.spacing_scheduler.store import (
    InMemorySpacingStateStore,
    SpacingStateStore,
)
from app.domain.spacing_scheduler.policy import SpacingIntervalPolicy
from app.domain.spacing_scheduler.types import (
    ExposureKind,
    ReviewableUnitId,
    SchedulingDecision,
    SchedulingStatus,
    SpacingState,
)

__all__ = [
    "ExposureKind",
    "InMemorySpacingStateStore",
    "ReviewableUnitId",
    "SchedulingDecision",
    "SchedulingStatus",
    "SpacingIntervalPolicy",
    "SpacingSchedulerService",
    "SpacingState",
    "SpacingStateStore",
    "get_spacing_scheduler",
    "reset_canonical_spacing_scheduler_for_tests",
]
