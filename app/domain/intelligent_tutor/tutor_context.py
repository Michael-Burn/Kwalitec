"""Tutor context — snapshot of educational intelligence for one interaction.

Assembled from existing platform services. Contains no inferred educational
decisions of its own.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any


def _freeze(metadata: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(metadata or {}))


@dataclass(frozen=True)
class TutorContext:
    """Immutable educational context for one Tutor turn.

    Fields reference Twin / Reasoning / Graph / Mission / Assessment /
    Curriculum artefacts already produced elsewhere.
    """

    context_id: str
    twin_id: str
    student_id: str
    question_kind: str
    question_text: str
    active_mission_id: str = ""
    active_mission_goal: str = ""
    active_mission_reason: str = ""
    primary_concept_id: str = ""
    concept_ids: tuple[str, ...] = ()
    recommendation_summaries: tuple[str, ...] = ()
    knowledge_gap_summaries: tuple[str, ...] = ()
    recovery_path: tuple[str, ...] = ()
    prerequisite_ids: tuple[str, ...] = ()
    related_concept_ids: tuple[str, ...] = ()
    mastery_notes: tuple[str, ...] = ()
    confidence_notes: tuple[str, ...] = ()
    assessment_feedback_summaries: tuple[str, ...] = ()
    curriculum_evidence_ids: tuple[str, ...] = ()
    curriculum_excerpts: tuple[str, ...] = ()
    reasoning_run_id: str = ""
    learning_state_summary: str = ""
    conversation_concept_ids: tuple[str, ...] = ()
    assembled_at: datetime | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not (self.context_id or "").strip():
            raise ValueError("context_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        for attr in (
            "concept_ids",
            "recommendation_summaries",
            "knowledge_gap_summaries",
            "recovery_path",
            "prerequisite_ids",
            "related_concept_ids",
            "mastery_notes",
            "confidence_notes",
            "assessment_feedback_summaries",
            "curriculum_evidence_ids",
            "curriculum_excerpts",
            "conversation_concept_ids",
        ):
            object.__setattr__(self, attr, tuple(getattr(self, attr) or ()))
        when = self.assembled_at
        if when is not None and when.tzinfo is not None:
            object.__setattr__(
                self, "assembled_at", when.astimezone(UTC).replace(tzinfo=None)
            )
        object.__setattr__(self, "metadata", _freeze(self.metadata))
