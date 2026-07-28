"""DecisionContext — immutable context for one decision-generation cycle."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DecisionContext:
    """Shared identifiers for an EducationalDecisionSet."""

    twin_id: str
    reasoning_request_id: str
    evidence_bundle_id: str
    session_id: str
    correlation_id: str
    decision_version: str
    prior_twin_version: int
    observation_set_id: str

    def __post_init__(self) -> None:
        for field_name in (
            "twin_id",
            "reasoning_request_id",
            "evidence_bundle_id",
            "session_id",
            "correlation_id",
            "decision_version",
            "observation_set_id",
        ):
            if not (getattr(self, field_name) or "").strip():
                raise ValueError(f"{field_name} is required")
        if self.prior_twin_version < 1:
            raise ValueError("prior_twin_version must be >= 1")
