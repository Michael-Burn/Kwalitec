"""Mission — one executable learning activity."""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_generation.enums import (
    MissionRecurrenceBand,
    MissionType,
)
from application.education.mission_generation.errors import MissionInvariantViolation
from application.education.mission_generation.ids import MissionId
from application.education.mission_generation.models.mission_constraint import (
    MissionConstraint,
)
from application.education.mission_generation.models.mission_estimate import (
    MissionEstimate,
)
from application.education.mission_generation.models.mission_objective import (
    MissionObjective,
)
from application.education.mission_generation.models.mission_ordering import (
    MissionOrdering,
)
from application.education.mission_generation.models.mission_step import MissionStep


@dataclass(frozen=True, slots=True)
class Mission:
    """Immutable executable learning mission derived from recommendations.

    A Mission is learning work — never an educational recommendation, never
    a mastery estimate, and never a mutation of student educational state.
    """

    mission_id: MissionId
    mission_type: MissionType
    objective: MissionObjective
    estimate: MissionEstimate
    ordering: MissionOrdering
    steps: tuple[MissionStep, ...] = ()
    constraints: tuple[MissionConstraint, ...] = ()
    source_recommendation_ids: tuple[str, ...] = ()
    subject_id: str | None = None
    competency_id: str | None = None
    recurrence: MissionRecurrenceBand = MissionRecurrenceBand.NORMAL
    chunk_index: int = 1
    chunk_count: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.mission_id, MissionId):
            raise MissionInvariantViolation(
                "mission_id must be a MissionId",
                invariant="Mission.mission_id.type",
            )
        if not isinstance(self.mission_type, MissionType):
            raise MissionInvariantViolation(
                "mission_type must be a MissionType",
                invariant="Mission.mission_type.type",
            )
        if not isinstance(self.objective, MissionObjective):
            raise MissionInvariantViolation(
                "objective must be a MissionObjective",
                invariant="Mission.objective.type",
            )
        if not isinstance(self.estimate, MissionEstimate):
            raise MissionInvariantViolation(
                "estimate must be a MissionEstimate",
                invariant="Mission.estimate.type",
            )
        if not isinstance(self.ordering, MissionOrdering):
            raise MissionInvariantViolation(
                "ordering must be a MissionOrdering",
                invariant="Mission.ordering.type",
            )
        if not isinstance(self.recurrence, MissionRecurrenceBand):
            raise MissionInvariantViolation(
                "recurrence must be a MissionRecurrenceBand",
                invariant="Mission.recurrence.type",
            )
        object.__setattr__(self, "steps", tuple(self.steps))
        for step in self.steps:
            if not isinstance(step, MissionStep):
                raise MissionInvariantViolation(
                    "steps must contain MissionStep values",
                    invariant="Mission.steps.type",
                )
        object.__setattr__(self, "constraints", tuple(self.constraints))
        for constraint in self.constraints:
            if not isinstance(constraint, MissionConstraint):
                raise MissionInvariantViolation(
                    "constraints must contain MissionConstraint values",
                    invariant="Mission.constraints.type",
                )
        source_ids = tuple(
            sid.strip()
            for sid in self.source_recommendation_ids
            if isinstance(sid, str) and sid.strip()
        )
        object.__setattr__(self, "source_recommendation_ids", source_ids)
        subject_id = (self.subject_id or "").strip() or None
        object.__setattr__(self, "subject_id", subject_id)
        competency_id = (self.competency_id or "").strip() or None
        object.__setattr__(self, "competency_id", competency_id)
        if isinstance(self.chunk_index, bool) or not isinstance(self.chunk_index, int):
            raise MissionInvariantViolation(
                "chunk_index must be an integer",
                invariant="Mission.chunk_index.type",
            )
        if self.chunk_index < 1:
            raise MissionInvariantViolation(
                "chunk_index must be >= 1",
                invariant="Mission.chunk_index.positive",
            )
        if isinstance(self.chunk_count, bool) or not isinstance(self.chunk_count, int):
            raise MissionInvariantViolation(
                "chunk_count must be an integer",
                invariant="Mission.chunk_count.type",
            )
        if self.chunk_count < 1:
            raise MissionInvariantViolation(
                "chunk_count must be >= 1",
                invariant="Mission.chunk_count.positive",
            )
        if self.chunk_index > self.chunk_count:
            raise MissionInvariantViolation(
                "chunk_index must be <= chunk_count",
                invariant="Mission.chunk_index.range",
            )

    def with_ordering(self, ordering: MissionOrdering) -> Mission:
        """Return a new Mission carrying an updated ordering."""
        return Mission(
            mission_id=self.mission_id,
            mission_type=self.mission_type,
            objective=self.objective,
            estimate=self.estimate,
            ordering=ordering,
            steps=self.steps,
            constraints=self.constraints,
            source_recommendation_ids=self.source_recommendation_ids,
            subject_id=self.subject_id,
            competency_id=self.competency_id,
            recurrence=self.recurrence,
            chunk_index=self.chunk_index,
            chunk_count=self.chunk_count,
        )

    def correlation_key(self) -> str:
        return (
            f"{self.mission_type.value}:"
            f"{self.subject_id or '-'}:"
            f"{self.competency_id or '-'}"
        )

    def is_prerequisite(self) -> bool:
        return self.mission_type is MissionType.REVISE_PREREQUISITE

    def is_lightweight(self) -> bool:
        return self.mission_type is MissionType.MAINTENANCE_REVIEW
