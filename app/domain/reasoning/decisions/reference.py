"""DecisionReference — identity chain from evidence to decision."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DecisionReference:
    """Provenance pointers required for Twin explainability."""

    evidence_bundle_id: str
    educational_observation_ids: tuple[str, ...]
    reasoning_request_id: str
    assessment_session_id: str
    correlation_id: str
    learning_objective_reference: str
    concept_reference: str = ""
    decision_id: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "educational_observation_ids",
            tuple(self.educational_observation_ids or ()),
        )
        for field_name in (
            "evidence_bundle_id",
            "reasoning_request_id",
            "assessment_session_id",
            "correlation_id",
            "learning_objective_reference",
        ):
            if not (getattr(self, field_name) or "").strip():
                raise ValueError(f"{field_name} is required")
