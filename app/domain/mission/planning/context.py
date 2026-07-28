"""PlanningContext — immutable context for one Twin→Mission planning cycle."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlanningContext:
    """Shared identifiers for a PlanningBatch / StudyMissionPlan."""

    twin_id: str
    student_id: str
    reasoning_request_id: str
    evidence_bundle_id: str
    session_id: str
    correlation_id: str
    planning_version: str
    decision_version: str
    twin_version: int
    decision_set_id: str
    available_minutes: int = 45
    curriculum_position: str = ""
    mission_request_id: str = ""

    def __post_init__(self) -> None:
        for field_name in (
            "twin_id",
            "student_id",
            "reasoning_request_id",
            "evidence_bundle_id",
            "session_id",
            "correlation_id",
            "planning_version",
            "decision_version",
            "decision_set_id",
        ):
            if not (getattr(self, field_name) or "").strip():
                raise ValueError(f"{field_name} is required")
        if self.twin_version < 1:
            raise ValueError("twin_version must be >= 1")
        if self.available_minutes < 1:
            raise ValueError("available_minutes must be >= 1")
        if not (self.mission_request_id or "").strip():
            object.__setattr__(
                self,
                "mission_request_id",
                (
                    f"mreq:{self.reasoning_request_id}:"
                    f"{self.evidence_bundle_id}:v{self.twin_version}"
                ),
            )
