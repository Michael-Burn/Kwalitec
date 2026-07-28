"""PlanningBatch — ordered immutable set of mission candidate projections."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.mission.planning.candidate import MissionCandidateProjection
from app.domain.mission.planning.context import PlanningContext


@dataclass(frozen=True)
class PlanningBatch:
    """Ordered, immutable batch of mission candidates for one planning cycle."""

    batch_id: str
    candidates: tuple[MissionCandidateProjection, ...]
    context: PlanningContext
    planning_version: str
    skipped_decision_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not (self.batch_id or "").strip():
            raise ValueError("batch_id is required")
        if not (self.planning_version or "").strip():
            raise ValueError("planning_version is required")
        if not isinstance(self.context, PlanningContext):
            raise TypeError("context must be PlanningContext")
        if self.context.planning_version != self.planning_version:
            raise ValueError("planning_version mismatch between context and batch")
        if not isinstance(self.candidates, tuple):
            object.__setattr__(self, "candidates", tuple(self.candidates))
        object.__setattr__(
            self, "skipped_decision_ids", tuple(self.skipped_decision_ids or ())
        )

        seen: set[str] = set()
        for cand in self.candidates:
            if not isinstance(cand, MissionCandidateProjection):
                raise TypeError(
                    "PlanningBatch accepts MissionCandidateProjection only"
                )
            if cand.candidate_id in seen:
                from app.domain.mission.planning.errors import DuplicateMissionRequest

                raise DuplicateMissionRequest(
                    f"duplicate candidate: {cand.candidate_id!r}"
                )
            seen.add(cand.candidate_id)
            if cand.twin_id != self.context.twin_id:
                raise ValueError("candidate twin_id mismatch with context")
            if cand.planning_version != self.planning_version:
                raise ValueError("planning_version mismatch within batch")

    @property
    def candidate_ids(self) -> tuple[str, ...]:
        return tuple(c.candidate_id for c in self.candidates)

    @property
    def decision_ids(self) -> tuple[str, ...]:
        ids: list[str] = []
        seen: set[str] = set()
        for cand in self.candidates:
            if cand.decision_id not in seen:
                seen.add(cand.decision_id)
                ids.append(cand.decision_id)
        return tuple(ids)

    def __len__(self) -> int:
        return len(self.candidates)
