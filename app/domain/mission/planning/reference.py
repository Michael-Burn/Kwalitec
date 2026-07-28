"""PlanningReference — identity chain from Twin decision to planned mission."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlanningReference:
    """Provenance pointers required for Mission planning explainability."""

    decision_id: str
    decision_version: str
    twin_version: int
    evidence_bundle_id: str
    educational_observation_ids: tuple[str, ...]
    reasoning_request_id: str
    assessment_session_id: str
    correlation_id: str
    planning_version: str
    twin_id: str
    learning_objective_reference: str = ""
    concept_reference: str = ""
    candidate_id: str = ""
    mission_id: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "educational_observation_ids",
            tuple(self.educational_observation_ids or ()),
        )
        for field_name in (
            "decision_id",
            "decision_version",
            "evidence_bundle_id",
            "reasoning_request_id",
            "assessment_session_id",
            "correlation_id",
            "planning_version",
            "twin_id",
        ):
            if not (getattr(self, field_name) or "").strip():
                raise ValueError(f"{field_name} is required")
        if self.twin_version < 1:
            raise ValueError("twin_version must be >= 1")
