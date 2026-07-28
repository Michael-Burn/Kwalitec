"""Immutable explanation section kinds and section objects (AP-002D6).

Sections narrate validated educational provenance only.
They never invent mastery, predictions, or independent recommendations.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any

from app.domain.intelligent_tutor.explainability.reference import ExplanationReference


class ExplanationSectionKind(StrEnum):
    """Approved Tutor explanation section catalogue."""

    MISSION = "mission"
    DECISION = "decision"
    EVIDENCE = "evidence"
    CONCEPT = "concept"
    LEARNING_OBJECTIVE = "learning_objective"
    UNCERTAINTY = "uncertainty"
    SUMMARY = "summary"


KNOWN_EXPLANATION_SECTION_KINDS: frozenset[str] = frozenset(
    kind.value for kind in ExplanationSectionKind
)


def parse_section_kind(value: str | ExplanationSectionKind) -> ExplanationSectionKind:
    """Parse a section kind or raise for unknown values (never invent)."""
    if isinstance(value, ExplanationSectionKind):
        return value
    normalised = (value or "").strip()
    if normalised not in KNOWN_EXPLANATION_SECTION_KINDS:
        from app.domain.intelligent_tutor.explainability.errors import (
            UnknownExplanationSchema,
        )

        raise UnknownExplanationSchema(f"unknown explanation section kind: {value!r}")
    return ExplanationSectionKind(normalised)


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


@dataclass(frozen=True)
class ExplanationSection:
    """One immutable, provenance-backed explanation section."""

    section_id: str
    kind: ExplanationSectionKind
    title: str
    body: str
    reference: ExplanationReference
    concept_ids: tuple[str, ...] = ()
    learning_objective_ids: tuple[str, ...] = ()
    decision_ids: tuple[str, ...] = ()
    uncertainty_notes: tuple[str, ...] = ()
    provenance: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not (self.section_id or "").strip():
            raise ValueError("section_id is required")
        if not (self.title or "").strip():
            raise ValueError("section title is required")
        if not (self.body or "").strip():
            raise ValueError("section body is required")
        if not isinstance(self.reference, ExplanationReference):
            raise TypeError("reference must be ExplanationReference")
        kind = parse_section_kind(self.kind)
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "concept_ids", tuple(self.concept_ids or ()))
        object.__setattr__(
            self, "learning_objective_ids", tuple(self.learning_objective_ids or ())
        )
        object.__setattr__(self, "decision_ids", tuple(self.decision_ids or ()))
        object.__setattr__(
            self, "uncertainty_notes", tuple(self.uncertainty_notes or ())
        )
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))


@dataclass(frozen=True)
class MissionExplanation(ExplanationSection):
    """Narrates why a StudyMissionPlan was selected (planning provenance only)."""

    mission_plan_id: str = ""
    mission_id: str = ""
    mission_goal: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", ExplanationSectionKind.MISSION)
        super().__post_init__()


@dataclass(frozen=True)
class DecisionExplanation(ExplanationSection):
    """Narrates a validated EducationalDecision (never re-reasons)."""

    decision_category: str = ""
    decision_summary: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", ExplanationSectionKind.DECISION)
        super().__post_init__()


@dataclass(frozen=True)
class EvidenceExplanation(ExplanationSection):
    """Narrates which evidence bundle / observation ids contributed.

    Does not consume raw assessment responses or evidence bundles as authority.
    """

    observation_count: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", ExplanationSectionKind.EVIDENCE)
        object.__setattr__(self, "observation_count", int(self.observation_count))
        super().__post_init__()


@dataclass(frozen=True)
class ConceptExplanation(ExplanationSection):
    """Narrates which concepts influenced the explanation / mission."""

    primary_concept_id: str = ""
    related_concept_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", ExplanationSectionKind.CONCEPT)
        object.__setattr__(
            self, "related_concept_ids", tuple(self.related_concept_ids or ())
        )
        super().__post_init__()
        if not (self.primary_concept_id or "").strip() and not self.concept_ids:
            from app.domain.intelligent_tutor.explainability.errors import (
                BrokenConceptReference,
            )

            raise BrokenConceptReference(
                f"broken concept reference on {self.section_id!r}"
            )


@dataclass(frozen=True)
class LearningObjectiveExplanation(ExplanationSection):
    """Narrates which learning objectives are involved."""

    primary_learning_objective_id: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", ExplanationSectionKind.LEARNING_OBJECTIVE)
        super().__post_init__()
        lo = (self.primary_learning_objective_id or "").strip()
        if not lo and not self.learning_objective_ids:
            from app.domain.intelligent_tutor.explainability.errors import (
                BrokenLearningObjectiveReference,
            )

            raise BrokenLearningObjectiveReference(
                f"missing learning objective on {self.section_id!r}"
            )
