"""Immutable DTOs for the Learning Activity Engine."""

from __future__ import annotations

from app.application.learning_activity.dto.activity_plan import ActivityPlan
from app.application.learning_activity.dto.activity_result import ActivityResult
from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.application.learning_activity.dto.activity_snapshot import ActivitySnapshot
from app.application.learning_activity.dto.activity_transition import (
    ActivityTransition,
)

__all__ = [
    "ActivityPlan",
    "ActivityResult",
    "ActivitySequence",
    "ActivitySnapshot",
    "ActivityTransition",
]
