"""Mission execution-context value object.

Goals capacity, Constraints, session window, committed work, and optional
journal / Behaviour refs bound how Decision(s) fit into *now* — never a second
selection authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.domain.decision.constraints import Constraints, IntensityPosture


@dataclass(frozen=True)
class MissionExecutionContext:
    """Feasibility bounds for one Mission composition evaluation.

    Attributes:
        session_window_id: Temporal container identity for this session/day.
        session_date: Calendar day of the session window when known.
        goals_capacity_minutes: Committed Goals capacity bound (optional).
        constraints: Session Constraints (time / intensity / sustainability).
        already_committed_minutes: Capacity already booked in this window.
        max_tasks: Explicit structural task-count ceiling (optional).
        journal_history_refs: Decision Journal refs (preference — not mastery).
        prior_completion_refs: Prior Completion / Failure refs (feasibility only).
        twin_snapshot_ref: Optional Twin snapshot identity for regeneration.
        curriculum_id: Curriculum identity when known (must match Decision).
        note_tags: Structural execution-context tags.
    """

    session_window_id: str | None = None
    session_date: date | None = None
    goals_capacity_minutes: int | None = None
    constraints: Constraints | None = None
    already_committed_minutes: int = 0
    max_tasks: int | None = None
    journal_history_refs: tuple[str, ...] = ()
    prior_completion_refs: tuple[str, ...] = ()
    twin_snapshot_ref: str | None = None
    curriculum_id: str | None = None
    note_tags: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        *,
        session_window_id: str | None = None,
        session_date: date | None = None,
        goals_capacity_minutes: int | None = None,
        constraints: Constraints | None = None,
        already_committed_minutes: int = 0,
        max_tasks: int | None = None,
        journal_history_refs: list[str] | tuple[str, ...] | None = None,
        prior_completion_refs: list[str] | tuple[str, ...] | None = None,
        twin_snapshot_ref: str | None = None,
        curriculum_id: str | None = None,
        note_tags: list[str] | tuple[str, ...] | None = None,
    ) -> MissionExecutionContext:
        """Construct MissionExecutionContext.

        Raises:
            ValueError: If minute / max_tasks fields are negative.
        """
        if already_committed_minutes < 0:
            raise ValueError("already_committed_minutes must be non-negative")
        if goals_capacity_minutes is not None and goals_capacity_minutes < 0:
            raise ValueError("goals_capacity_minutes must be non-negative")
        if max_tasks is not None and max_tasks < 0:
            raise ValueError("max_tasks must be non-negative")
        return cls(
            session_window_id=session_window_id,
            session_date=session_date,
            goals_capacity_minutes=goals_capacity_minutes,
            constraints=constraints,
            already_committed_minutes=already_committed_minutes,
            max_tasks=max_tasks,
            journal_history_refs=tuple(journal_history_refs or ()),
            prior_completion_refs=tuple(prior_completion_refs or ()),
            twin_snapshot_ref=twin_snapshot_ref,
            curriculum_id=curriculum_id,
            note_tags=tuple(note_tags or ()),
        )

    @classmethod
    def ample(cls, **overrides: object) -> MissionExecutionContext:
        """Convenience: ample capacity execution context."""
        defaults: dict[str, object] = {
            "session_window_id": "session-ample",
            "constraints": Constraints.create(
                available_minutes=60,
                intensity=IntensityPosture.AMPLE,
            ),
        }
        defaults.update(overrides)
        return cls.create(**defaults)  # type: ignore[arg-type]

    @property
    def remaining_available_minutes(self) -> int | None:
        """Remaining session minutes after already-committed work."""
        if self.constraints is None or self.constraints.available_minutes is None:
            if self.goals_capacity_minutes is None:
                return None
            return max(0, self.goals_capacity_minutes - self.already_committed_minutes)
        return max(
            0, self.constraints.available_minutes - self.already_committed_minutes
        )

    @property
    def protect_intensity(self) -> bool:
        """True when Constraints demand sustainability protection."""
        return self.constraints is not None and self.constraints.protect_intensity

    @property
    def scarce_capacity(self) -> bool:
        """True when remaining minutes are structurally scarce (< 25)."""
        remaining = self.remaining_available_minutes
        return remaining is not None and remaining < 25
