"""Mastery link — pointer from a graph node to Twin mastery (no duplication)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MasteryLink:
    """Reference from a Learning Graph node to a Twin mastery record.

    The Student Digital Twin remains the canonical store of mastery scores.
    The Learning Graph only stores this link so nodes can resolve Twin state
    without copying inference rows.
    """

    link_id: str
    graph_id: str
    concept_id: str
    mastery_id: str
    twin_id: str

    def __post_init__(self) -> None:
        if not (self.link_id or "").strip():
            raise ValueError("link_id is required")
        if not (self.concept_id or "").strip():
            raise ValueError("concept_id is required")
        if not (self.mastery_id or "").strip():
            raise ValueError("mastery_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
