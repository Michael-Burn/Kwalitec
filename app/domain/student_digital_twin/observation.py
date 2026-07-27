"""Immutable educational observations (facts) — append-only.

Observations are educational FACTS, never inferences. They must never be
mutated or deleted after creation.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any


class ObservationKind(StrEnum):
    """Canonical observation kinds for SDT-001."""

    QUESTION_ANSWERED = "question_answered"
    QUIZ_COMPLETED = "quiz_completed"
    STUDY_SESSION_COMPLETED = "study_session_completed"
    REVISION_COMPLETED = "revision_completed"
    CHAPTER_COMPLETED = "chapter_completed"
    FORMULA_REVIEWED = "formula_reviewed"


def _freeze_metadata(metadata: Mapping[str, Any] | None) -> Mapping[str, Any]:
    raw = dict(metadata or {})
    return MappingProxyType(raw)


@dataclass(frozen=True)
class Observation:
    """One immutable educational fact about a learner.

    Append-only: never overwrite. Curriculum entity references are opaque ids
    resolved through CurriculumRetrievalService when reasoning needs evidence.
    """

    observation_id: str
    kind: ObservationKind
    twin_id: str
    student_id: str
    recorded_at: datetime
    curriculum_entity_id: str = ""
    curriculum_entity_kind: str = ""
    evidence_reference: str = ""
    provenance: str = ""
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not (self.observation_id or "").strip():
            raise ValueError("observation_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        if not (self.student_id or "").strip():
            raise ValueError("student_id is required")
        kind = (
            self.kind
            if isinstance(self.kind, ObservationKind)
            else ObservationKind(str(self.kind))
        )
        object.__setattr__(self, "kind", kind)
        when = self.recorded_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "recorded_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))

    @classmethod
    def create(
        cls,
        *,
        observation_id: str,
        kind: ObservationKind | str,
        twin_id: str,
        student_id: str,
        recorded_at: datetime | None = None,
        curriculum_entity_id: str = "",
        curriculum_entity_kind: str = "",
        evidence_reference: str = "",
        provenance: str = "",
        metadata: Mapping[str, Any] | None = None,
    ) -> Observation:
        """Factory for a new immutable observation."""
        when = recorded_at or datetime.now(UTC).replace(tzinfo=None)
        return cls(
            observation_id=observation_id,
            kind=(
                kind
                if isinstance(kind, ObservationKind)
                else ObservationKind(kind)
            ),
            twin_id=twin_id,
            student_id=student_id,
            recorded_at=when,
            curriculum_entity_id=curriculum_entity_id or "",
            curriculum_entity_kind=curriculum_entity_kind or "",
            evidence_reference=evidence_reference or "",
            provenance=provenance or "",
            metadata=_freeze_metadata(metadata),
        )

    @property
    def is_positive_outcome(self) -> bool | None:
        """Interpret common outcome metadata; None when not applicable."""
        if "correct" in self.metadata:
            return bool(self.metadata["correct"])
        if "score" in self.metadata:
            try:
                return float(self.metadata["score"]) >= 0.7
            except (TypeError, ValueError):
                return None
        if self.kind in {
            ObservationKind.CHAPTER_COMPLETED,
            ObservationKind.FORMULA_REVIEWED,
            ObservationKind.REVISION_COMPLETED,
            ObservationKind.STUDY_SESSION_COMPLETED,
        }:
            return True
        return None
