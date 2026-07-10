"""Behaviour domain state for the Student Digital Twin.

Represents study behaviour structure. Structural slots only — no adherence
scoring, burnout detection, or pattern inference algorithms.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class BehaviourState:
    """How the learner actually studies — structural snapshot.

    Attributes:
        consistency_metrics: Named metric values stored by later pipelines
            (e.g. adherence ratio). Not computed here.
        session_history_ids: References to study session history records.
        study_pattern_ids: References to study pattern records.
        last_updated: When this behaviour snapshot was last materialised.
    """

    consistency_metrics: dict[str, Any] = field(default_factory=dict)
    session_history_ids: tuple[str, ...] = ()
    study_pattern_ids: tuple[str, ...] = ()
    last_updated: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        consistency_metrics: dict[str, Any] | None = None,
        session_history_ids: list[str] | tuple[str, ...] | None = None,
        study_pattern_ids: list[str] | tuple[str, ...] | None = None,
        last_updated: datetime | None = None,
    ) -> BehaviourState:
        """Construct a BehaviourState.

        Args:
            consistency_metrics: Optional metric bag (defensively copied).
            session_history_ids: Optional session history references.
            study_pattern_ids: Optional study pattern references.
            last_updated: Optional materialisation timestamp.

        Returns:
            A frozen BehaviourState instance.
        """
        return cls(
            consistency_metrics=dict(consistency_metrics or {}),
            session_history_ids=tuple(session_history_ids or ()),
            study_pattern_ids=tuple(study_pattern_ids or ()),
            last_updated=last_updated,
        )
