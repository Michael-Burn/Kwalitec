"""MissionCandidateProjection — one immutable planning candidate from a Twin decision.

Planning only. Never stores independent mastery authority.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from app.domain.mission.planning.activity_type import (
    PlanningActivityType,
    parse_planning_activity_type,
)
from app.domain.mission.planning.reference import PlanningReference


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


@dataclass(frozen=True)
class MissionCandidateProjection:
    """One immutable mission candidate projected from a Twin decision.

    Concept / LO refs are opaque educational identifiers. Mastery scores are
    never authoritative here — only Twin decision references and planning rank.
    """

    candidate_id: str
    activity_type: PlanningActivityType
    concept_id: str
    concept_title: str
    twin_id: str
    reference: PlanningReference
    planning_version: str
    created_at: datetime
    decision_id: str
    priority_score: float
    priority_band: str
    learning_objective_id: str = ""
    twin_decision_ref: str = ""
    recommendation_id: str = ""
    gap_id: str = ""
    recovery_path_concept_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    priority_explanation: str = ""
    provenance: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not (self.candidate_id or "").strip():
            raise ValueError("candidate_id is required")
        if not (self.concept_id or "").strip():
            raise ValueError("concept_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        if not (self.decision_id or "").strip():
            raise ValueError("decision_id is required")
        if not (self.planning_version or "").strip():
            raise ValueError("planning_version is required")
        if not isinstance(self.reference, PlanningReference):
            raise TypeError("reference must be PlanningReference")

        activity = parse_planning_activity_type(self.activity_type)
        object.__setattr__(self, "activity_type", activity)

        when = self.created_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )

        object.__setattr__(
            self,
            "recovery_path_concept_ids",
            tuple(self.recovery_path_concept_ids or ()),
        )
        object.__setattr__(self, "evidence_ids", tuple(self.evidence_ids or ()))
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(self, "payload", _freeze_mapping(self.payload))
        if not (self.twin_decision_ref or "").strip():
            object.__setattr__(self, "twin_decision_ref", self.decision_id)
        if not (self.concept_title or "").strip():
            object.__setattr__(self, "concept_title", self.concept_id)
        object.__setattr__(self, "priority_score", float(self.priority_score))
