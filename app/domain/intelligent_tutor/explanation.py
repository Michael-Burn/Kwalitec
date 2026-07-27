"""Structured educational explanations produced by the Tutor."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class ExplanationKind(StrEnum):
    MISSION = "mission"
    GAP = "gap"
    WEAK_CONCEPT = "weak_concept"
    PREREQUISITE = "prerequisite"
    LEARNING_PATH = "learning_path"
    RECOVERY = "recovery"
    STRATEGY = "strategy"
    CONFIDENCE = "confidence"
    MASTERY = "mastery"
    ASSESSMENT = "assessment"
    GENERAL = "general"


@dataclass(frozen=True)
class Explanation:
    """Traceable educational explanation grounded in assembled evidence."""

    explanation_id: str
    twin_id: str
    kind: ExplanationKind
    summary: str
    detail: str
    evidence_ids: tuple[str, ...] = ()
    concept_ids: tuple[str, ...] = ()
    reasoning_run_id: str = ""
    mission_id: str = ""
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        if not (self.explanation_id or "").strip():
            raise ValueError("explanation_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        if not (self.summary or "").strip():
            raise ValueError("explanation summary is required")
        kind = (
            self.kind
            if isinstance(self.kind, ExplanationKind)
            else ExplanationKind(str(self.kind))
        )
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "evidence_ids", tuple(self.evidence_ids or ()))
        object.__setattr__(self, "concept_ids", tuple(self.concept_ids or ()))
        when = self.created_at
        if when is not None and when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )
