"""Spacing Scheduler application package — canonical due-state authority.

Sole lawful entry for time-based review scheduling. Revision and the daily
study composer must read due status only through this facade. Does not own
the Adaptive Decision Engine.
"""

from __future__ import annotations

from app.application.spacing_scheduler.board import (
    SpacingBoardEntry,
    SpacingRevisionBoard,
)
from app.application.spacing_scheduler.service import (
    SpacingSchedulerService,
    discard_canonical_spacing_scheduler_for_tests,
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
    "SpacingBoardEntry",
    "SpacingIntervalPolicy",
    "SpacingRevisionBoard",
    "SpacingSchedulerService",
    "SpacingState",
    "SpacingStateStore",
    "discard_canonical_spacing_scheduler_for_tests",
    "get_spacing_scheduler",
    "reset_canonical_spacing_scheduler_for_tests",
]
