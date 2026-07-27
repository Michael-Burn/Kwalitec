"""Educational explanation for why a mission was selected."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MissionReason:
    """Explainable educational rationale for the daily mission.

    Every mission must cite decisions already produced by Educational Reasoning
    (recommendations / gaps) and optionally Learning Graph recovery structure.
    """

    summary: str
    educational_explanation: str
    decision_references: tuple[str, ...] = ()
    recommendation_ids: tuple[str, ...] = ()
    gap_ids: tuple[str, ...] = ()
    recovery_path_concept_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    graph_influence: str = ""

    def __post_init__(self) -> None:
        if not (self.summary or "").strip():
            raise ValueError("mission reason summary is required")
        if not (self.educational_explanation or "").strip():
            raise ValueError("educational_explanation is required")
        object.__setattr__(
            self, "decision_references", tuple(self.decision_references or ())
        )
        object.__setattr__(
            self, "recommendation_ids", tuple(self.recommendation_ids or ())
        )
        object.__setattr__(self, "gap_ids", tuple(self.gap_ids or ()))
        object.__setattr__(
            self,
            "recovery_path_concept_ids",
            tuple(self.recovery_path_concept_ids or ()),
        )
        object.__setattr__(self, "evidence_ids", tuple(self.evidence_ids or ()))
