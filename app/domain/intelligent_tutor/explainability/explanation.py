"""TutorExplanation — immutable explanation artefact for one Tutor cycle."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from app.domain.intelligent_tutor.explainability.context import ExplanationContext
from app.domain.intelligent_tutor.explainability.section import ExplanationSection


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


@dataclass(frozen=True)
class TutorExplanation:
    """Immutable learner-facing explanation grounded in educational provenance.

    Represents explanations only — never learner state, mastery estimates,
    or independent recommendations.
    """

    explanation_id: str
    twin_id: str
    student_id: str
    context: ExplanationContext
    sections: tuple[ExplanationSection, ...]
    explanation_version: str
    twin_version: int
    created_at: datetime
    summary: str = ""
    decision_ids: tuple[str, ...] = ()
    concept_ids: tuple[str, ...] = ()
    learning_objective_ids: tuple[str, ...] = ()
    mission_plan_id: str = ""
    mission_id: str = ""
    uncertainty_notes: tuple[str, ...] = ()
    validation_passed: bool = True
    validation_summary: str = ""
    available: bool = True
    provenance: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not (self.explanation_id or "").strip():
            raise ValueError("explanation_id is required")
        if not isinstance(self.context, ExplanationContext):
            raise TypeError("context must be ExplanationContext")
        if self.context.twin_id != self.twin_id:
            raise ValueError("twin_id mismatch with context")
        if self.context.explanation_version != self.explanation_version:
            raise ValueError("explanation_version mismatch with context")
        if self.twin_version < 1:
            raise ValueError("twin_version must be >= 1")
        if self.available and not (self.summary or "").strip():
            raise ValueError("summary is required when explanation is available")

        when = self.created_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )

        if not isinstance(self.sections, tuple):
            object.__setattr__(self, "sections", tuple(self.sections))
        object.__setattr__(self, "decision_ids", tuple(self.decision_ids or ()))
        object.__setattr__(self, "concept_ids", tuple(self.concept_ids or ()))
        object.__setattr__(
            self,
            "learning_objective_ids",
            tuple(self.learning_objective_ids or ()),
        )
        object.__setattr__(
            self, "uncertainty_notes", tuple(self.uncertainty_notes or ())
        )
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))

        seen: set[str] = set()
        for section in self.sections:
            if not isinstance(section, ExplanationSection):
                raise TypeError("sections must be ExplanationSection")
            if section.section_id in seen:
                from app.domain.intelligent_tutor.explainability.errors import (
                    InvalidExplanationSchema,
                )

                raise InvalidExplanationSchema(
                    f"duplicate section: {section.section_id!r}"
                )
            seen.add(section.section_id)
            if section.reference.twin_id != self.twin_id:
                raise ValueError("section twin_id mismatch")

    @property
    def section_ids(self) -> tuple[str, ...]:
        return tuple(s.section_id for s in self.sections)

    def __len__(self) -> int:
        return len(self.sections)
