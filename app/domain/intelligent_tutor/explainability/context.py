"""ExplanationContext — immutable context for one Tutor explanation cycle."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExplanationContext:
    """Shared identifiers for a TutorExplanation / ExplanationResult."""

    twin_id: str
    student_id: str
    reasoning_request_id: str
    evidence_bundle_id: str
    session_id: str
    correlation_id: str
    explanation_version: str
    decision_version: str
    twin_version: int
    decision_set_id: str
    mission_plan_id: str = ""
    mission_id: str = ""
    planning_version: str = ""
    explanation_request_id: str = ""

    def __post_init__(self) -> None:
        for field_name in (
            "twin_id",
            "student_id",
            "reasoning_request_id",
            "evidence_bundle_id",
            "session_id",
            "correlation_id",
            "explanation_version",
            "decision_version",
            "decision_set_id",
        ):
            if not (getattr(self, field_name) or "").strip():
                raise ValueError(f"{field_name} is required")
        if self.twin_version < 1:
            raise ValueError("twin_version must be >= 1")
        if not (self.explanation_request_id or "").strip():
            object.__setattr__(
                self,
                "explanation_request_id",
                (
                    f"xreq:{self.reasoning_request_id}:"
                    f"{self.evidence_bundle_id}:v{self.twin_version}"
                    f":{self.mission_plan_id or 'no-plan'}"
                ),
            )
