"""Revision plan — ordered revision interventions with scheduled windows."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.adaptive_learning.intervention import Intervention
from app.domain.adaptive_learning.intervention_type import InterventionType
from app.domain.adaptive_learning.revision_candidate import RevisionCandidate
from app.domain.adaptive_learning.revision_window import RevisionWindow


@dataclass(frozen=True)
class RevisionPlan:
    """Ordered revision plan produced by the Adaptive Decision Engine.

    Contains selected interventions, supporting candidates, and windows.
    Does not generate educational content or questions.
    """

    plan_id: str
    interventions: tuple[Intervention, ...]
    candidates: tuple[RevisionCandidate, ...] = field(default_factory=tuple)
    windows: tuple[RevisionWindow, ...] = field(default_factory=tuple)
    total_estimated_minutes: float = 0.0
    primary_topic_id: str | None = None

    @classmethod
    def empty(cls, plan_id: str = "plan-empty") -> RevisionPlan:
        """Return an empty revision plan."""
        return cls(
            plan_id=_require_non_empty(plan_id, "plan_id"),
            interventions=(),
        )

    @classmethod
    def create(
        cls,
        plan_id: str,
        *,
        interventions: list[Intervention] | tuple[Intervention, ...] | None = None,
        candidates: (
            list[RevisionCandidate] | tuple[RevisionCandidate, ...] | None
        ) = None,
        windows: list[RevisionWindow] | tuple[RevisionWindow, ...] | None = None,
        total_estimated_minutes: float | None = None,
        primary_topic_id: str | None = None,
    ) -> RevisionPlan:
        """Construct a RevisionPlan; validates revision-only interventions."""
        pid = _require_non_empty(plan_id, "plan_id")
        ints = tuple(interventions or ())
        for intervention in ints:
            if intervention.intervention_type is not InterventionType.REVISION:
                raise ValueError(
                    "RevisionPlan accepts REVISION interventions only; "
                    f"got {intervention.intervention_type.value!r}"
                )
        cands = tuple(candidates or ())
        wins = tuple(windows or ())
        if total_estimated_minutes is None:
            total = sum(i.estimated_study_minutes for i in ints)
        else:
            total = _non_negative(total_estimated_minutes, "total_estimated_minutes")
        primary = primary_topic_id
        if primary is None and ints:
            primary = ints[0].topic_id
        return cls(
            plan_id=pid,
            interventions=ints,
            candidates=cands,
            windows=wins,
            total_estimated_minutes=total,
            primary_topic_id=primary,
        )

    @property
    def is_empty(self) -> bool:
        """True when no interventions are planned."""
        return not self.interventions

    @property
    def intervention_count(self) -> int:
        """Number of planned interventions."""
        return len(self.interventions)

    @property
    def topic_ids(self) -> tuple[str, ...]:
        """Ordered topic ids from interventions (skipping None)."""
        return tuple(i.topic_id for i in self.interventions if i.topic_id)


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _non_negative(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a non-negative number")
    numeric = float(value)
    if numeric < 0.0:
        raise ValueError(f"{field_name} must be a non-negative number")
    return numeric
