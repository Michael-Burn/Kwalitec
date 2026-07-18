"""Immutable snapshot of Learning Activity Engine posture."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.learning_activity.dto.activity_result import ActivityResult
from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.domain.learning_activity.entities.activity_progress import ActivityProgress
from app.domain.learning_activity.entities.learning_activity import LearningActivity
from app.domain.learning_activity.value_objects.activity_state import ActivityState


@dataclass(frozen=True)
class ActivitySnapshot:
    """Read-only educational snapshot of activity execution inside a session.

    Attributes:
        session_id: Parent Learning Session identity.
        sequence_id: Activity sequence identity.
        current_activity: Activity currently in focus, if any.
        current_state: State of the current activity, if any.
        progress: Sequence progress summary.
        sequence: Full ordered sequence.
        result: Latest completion evaluation, if evaluated.
        ready_for_session_completion: True when sequence is educationally closed
            and the Session Runtime may consider session completion.
        next_activity: Next remaining activity after current, if any.
        previous_activity: Previous activity before current, if any.
    """

    session_id: str
    sequence_id: str
    current_activity: LearningActivity | None
    current_state: ActivityState | None
    progress: ActivityProgress
    sequence: ActivitySequence
    result: ActivityResult | None
    ready_for_session_completion: bool
    next_activity: LearningActivity | None
    previous_activity: LearningActivity | None
