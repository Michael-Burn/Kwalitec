"""Associate reflection identifiers with Learning Activities.

Reflections are attributed to activities — not sessions. No persistence.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.application.learning_activity.exceptions import (
    ActivityNotFound,
    ReflectionRoutingError,
)
from app.domain.learning_activity.entities.learning_activity import LearningActivity
from app.domain.learning_activity.value_objects.activity_state import ActivityState
from app.domain.learning_activity.value_objects.activity_type import ActivityType


@dataclass(frozen=True)
class ReflectionRouteResult:
    """Outcome of associating a reflection with an activity."""

    activity: LearningActivity
    sequence: ActivitySequence
    reflection_id: str


class ReflectionRouter:
    """Associate reflection identifiers with Learning Activities."""

    def associate(
        self,
        sequence: ActivitySequence,
        *,
        reflection_id: str,
        activity_id: str | None = None,
        prefer_reflection_type: bool = True,
    ) -> ReflectionRouteResult:
        """Attach ``reflection_id`` to the target activity.

        When ``activity_id`` is omitted:
        - prefer a REFLECTION-typed activity that is ACTIVE/PAUSED/COMPLETED
        - otherwise the current ACTIVE activity
        Never attributes reflections at session scope.
        """
        rid = (reflection_id or "").strip()
        if not rid:
            raise ReflectionRoutingError("reflection_id must be non-empty")

        if activity_id is not None:
            activity = sequence.activity_by_id(activity_id)
            if activity is None:
                raise ActivityNotFound(
                    f"Activity {activity_id!r} not found for reflection routing"
                )
        else:
            activity = self._resolve_default(
                sequence, prefer_reflection_type=prefer_reflection_type
            )

        if activity.state == ActivityState.NOT_STARTED:
            raise ReflectionRoutingError(
                f"Cannot associate reflection with activity "
                f"{activity.activity_id!r} in state not_started"
            )
        if activity.state == ActivityState.SKIPPED:
            raise ReflectionRoutingError(
                f"Cannot associate reflection with skipped activity "
                f"{activity.activity_id!r}"
            )

        updated = activity.with_reflection(rid)
        return ReflectionRouteResult(
            activity=updated,
            sequence=sequence.with_activity(updated),
            reflection_id=rid,
        )

    def reflections_for(
        self, sequence: ActivitySequence, activity_id: str
    ) -> tuple[str, ...]:
        """Return reflection ids attached to an activity."""
        activity = sequence.activity_by_id(activity_id)
        if activity is None:
            raise ActivityNotFound(f"Activity {activity_id!r} not found")
        return activity.reflection_ids

    @staticmethod
    def _resolve_default(
        sequence: ActivitySequence,
        *,
        prefer_reflection_type: bool,
    ) -> LearningActivity:
        if prefer_reflection_type:
            reflection_typed = [
                a
                for a in sequence.activities
                if a.activity_type == ActivityType.REFLECTION
                and a.state
                in {
                    ActivityState.ACTIVE,
                    ActivityState.PAUSED,
                    ActivityState.COMPLETED,
                }
            ]
            if reflection_typed:
                return min(reflection_typed, key=lambda a: a.sequence_index)

        active = [
            a for a in sequence.activities if a.state == ActivityState.ACTIVE
        ]
        if len(active) == 1:
            return active[0]
        if len(active) > 1:
            raise ReflectionRoutingError(
                "Multiple ACTIVE activities; activity_id is required"
            )
        raise ReflectionRoutingError(
            "No suitable activity for reflection association; "
            "provide activity_id"
        )
