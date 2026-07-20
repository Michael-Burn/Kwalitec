"""ExplanationSection — one four-question section of an EducationalExplanation.

Architecture Source
    EDU-005 Educational Explainability Engine
    EDUCATIONAL_EXPLAINABILITY_STANDARD.md (EIP-003)
Concept
    Explanation Section
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.explainability.enums import ExplanationSectionKind
from domain.explainability.ids import EvidenceReferenceId, ExplanationSectionId


@dataclass(frozen=True, slots=True)
class ExplanationSection(EducationalValueObject):
    """One educational explanation section answering a framework question.

    Sections narrate authorised Educational OS state. They must not invent
    mastery, expose engineering theatre, or mutate decisions.
    """

    section_id: ExplanationSectionId
    kind: ExplanationSectionKind
    title: str
    body: str
    sequence: int
    evidence_reference_ids: tuple[EvidenceReferenceId, ...] = ()

    def _validate(self) -> None:
        if not isinstance(self.section_id, ExplanationSectionId):
            raise EducationalInvariantViolation(
                "section_id must be an ExplanationSectionId",
                invariant="ExplanationSection.section_id.type",
            )
        if not isinstance(self.kind, ExplanationSectionKind):
            raise EducationalInvariantViolation(
                "kind must be an ExplanationSectionKind",
                invariant="ExplanationSection.kind.type",
            )
        object.__setattr__(
            self,
            "title",
            require_non_empty_text(self.title, "title"),
        )
        object.__setattr__(
            self,
            "body",
            require_non_empty_text(self.body, "body"),
        )
        if len(self.body) < 12:
            raise EducationalInvariantViolation(
                "section body must be educationally substantive",
                invariant="ExplanationSection.body.substantive",
            )
        if not isinstance(self.sequence, int) or isinstance(self.sequence, bool):
            raise EducationalInvariantViolation(
                "sequence must be an integer",
                invariant="ExplanationSection.sequence.type",
            )
        if self.sequence < 1:
            raise EducationalInvariantViolation(
                "sequence must be a positive integer",
                invariant="ExplanationSection.sequence.positive",
            )
        if not isinstance(self.evidence_reference_ids, tuple):
            raise EducationalInvariantViolation(
                "evidence_reference_ids must be a tuple",
                invariant="ExplanationSection.evidence_reference_ids.type",
            )
        seen: set[str] = set()
        for reference_id in self.evidence_reference_ids:
            if not isinstance(reference_id, EvidenceReferenceId):
                raise EducationalInvariantViolation(
                    "evidence_reference_ids must contain EvidenceReferenceId values",
                    invariant="ExplanationSection.evidence_reference_ids.item_type",
                )
            if reference_id.value in seen:
                raise EducationalInvariantViolation(
                    "evidence_reference_ids must be unique within a section",
                    invariant="ExplanationSection.evidence_reference_ids.unique",
                )
            seen.add(reference_id.value)
