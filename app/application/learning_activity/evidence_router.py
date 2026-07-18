"""Route evidence identifiers to Learning Activities.

No persistence. No scoring. Attribution only.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.application.learning_activity.exceptions import (
    ActivityNotFound,
    EvidenceRoutingError,
)
from app.domain.learning_activity.entities.learning_activity import LearningActivity
from app.domain.learning_activity.value_objects.activity_state import ActivityState


@dataclass(frozen=True)
class EvidenceRouteResult:
    """Outcome of routing evidence to an activity."""

    activity: LearningActivity
    sequence: ActivitySequence
    evidence_id: str


class EvidenceRouter:
    """Route evidence identifiers onto Learning Activities."""

    def route(
        self,
        sequence: ActivitySequence,
        *,
        evidence_id: str,
        activity_id: str | None = None,
        require_active: bool = True,
    ) -> EvidenceRouteResult:
        """Attach ``evidence_id`` to the target activity.

        When ``activity_id`` is omitted, routes to the single ACTIVE activity.
        Never persists or scores evidence.
        """
        eid = (evidence_id or "").strip()
        if not eid:
            raise EvidenceRoutingError("evidence_id must be non-empty")

        if activity_id is not None:
            activity = sequence.activity_by_id(activity_id)
            if activity is None:
                raise ActivityNotFound(
                    f"Activity {activity_id!r} not found for evidence routing"
                )
        else:
            active = [
                a for a in sequence.activities if a.state == ActivityState.ACTIVE
            ]
            if len(active) != 1:
                raise EvidenceRoutingError(
                    "Evidence routing without activity_id requires exactly "
                    f"one ACTIVE activity (found {len(active)})"
                )
            activity = active[0]

        if require_active and activity.state not in {
            ActivityState.ACTIVE,
            ActivityState.PAUSED,
        }:
            raise EvidenceRoutingError(
                f"Cannot route evidence to activity {activity.activity_id!r} "
                f"in state {activity.state.value}"
            )

        updated = activity.with_evidence(eid)
        return EvidenceRouteResult(
            activity=updated,
            sequence=sequence.with_activity(updated),
            evidence_id=eid,
        )

    def evidence_for(
        self, sequence: ActivitySequence, activity_id: str
    ) -> tuple[str, ...]:
        """Return evidence ids attached to an activity."""
        activity = sequence.activity_by_id(activity_id)
        if activity is None:
            raise ActivityNotFound(f"Activity {activity_id!r} not found")
        return activity.evidence_ids
