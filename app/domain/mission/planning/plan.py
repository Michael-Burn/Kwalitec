"""StudyMissionPlan — immutable planning artefact for one Twin→Mission cycle."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from app.domain.mission.planning.candidate import MissionCandidateProjection
from app.domain.mission.planning.context import PlanningContext


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


@dataclass(frozen=True)
class StudyMissionPlan:
    """Immutable study mission plan derived from Twin decisions.

    Planning only — answers \"what should the learner do next?\".
    Twin remains authoritative for learner belief.
    """

    plan_id: str
    mission_id: str
    twin_id: str
    student_id: str
    context: PlanningContext
    selected_candidate: MissionCandidateProjection | None
    ranked_candidates: tuple[MissionCandidateProjection, ...]
    planning_version: str
    twin_version: int
    created_at: datetime
    goal: str = ""
    educational_explanation: str = ""
    concept_ids: tuple[str, ...] = ()
    decision_ids: tuple[str, ...] = ()
    prior_plan_ids: tuple[str, ...] = ()
    validation_passed: bool = True
    validation_summary: str = ""
    provenance: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not (self.plan_id or "").strip():
            raise ValueError("plan_id is required")
        if not isinstance(self.context, PlanningContext):
            raise TypeError("context must be PlanningContext")
        if self.context.twin_id != self.twin_id:
            raise ValueError("twin_id mismatch with context")
        if self.context.planning_version != self.planning_version:
            raise ValueError("planning_version mismatch with context")
        if self.twin_version < 1:
            raise ValueError("twin_version must be >= 1")

        when = self.created_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )

        if not isinstance(self.ranked_candidates, tuple):
            object.__setattr__(
                self, "ranked_candidates", tuple(self.ranked_candidates)
            )
        object.__setattr__(self, "concept_ids", tuple(self.concept_ids or ()))
        object.__setattr__(self, "decision_ids", tuple(self.decision_ids or ()))
        object.__setattr__(self, "prior_plan_ids", tuple(self.prior_plan_ids or ()))
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))

        seen: set[str] = set()
        for cand in self.ranked_candidates:
            if not isinstance(cand, MissionCandidateProjection):
                raise TypeError("ranked_candidates must be MissionCandidateProjection")
            if cand.candidate_id in seen:
                from app.domain.mission.planning.errors import DuplicateMissionRequest

                raise DuplicateMissionRequest(
                    f"duplicate candidate projection: {cand.candidate_id!r}"
                )
            seen.add(cand.candidate_id)
            if cand.twin_id != self.twin_id:
                raise ValueError("candidate twin_id mismatch")

        if self.selected_candidate is not None:
            if not isinstance(self.selected_candidate, MissionCandidateProjection):
                raise TypeError("selected_candidate must be MissionCandidateProjection")
            if self.selected_candidate.twin_id != self.twin_id:
                raise ValueError("selected_candidate twin_id mismatch")

    @property
    def candidate_ids(self) -> tuple[str, ...]:
        return tuple(c.candidate_id for c in self.ranked_candidates)

    def __len__(self) -> int:
        return len(self.ranked_candidates)
