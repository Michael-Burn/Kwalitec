"""ProjectionContext — immutable context for one Twin→Graph projection cycle."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProjectionContext:
    """Shared identifiers for a ProjectionBatch."""

    twin_id: str
    student_id: str
    graph_id: str
    reasoning_request_id: str
    evidence_bundle_id: str
    session_id: str
    correlation_id: str
    projection_version: str
    decision_version: str
    twin_version: int
    decision_set_id: str

    def __post_init__(self) -> None:
        for field_name in (
            "twin_id",
            "student_id",
            "graph_id",
            "reasoning_request_id",
            "evidence_bundle_id",
            "session_id",
            "correlation_id",
            "projection_version",
            "decision_version",
            "decision_set_id",
        ):
            if not (getattr(self, field_name) or "").strip():
                raise ValueError(f"{field_name} is required")
        if self.twin_version < 1:
            raise ValueError("twin_version must be >= 1")
