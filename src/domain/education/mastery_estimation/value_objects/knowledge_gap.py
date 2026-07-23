"""Knowledge gap — a competency where estimated mastery is educationally weak.

Architecture Source
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
    KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    Knowledge Gap
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.value_objects.dependency_strength import (
    DependencyStrength,
)
from domain.education.mastery_estimation.enums import (
    KnowledgeGapKind,
    KnowledgeGapSeverity,
)
from domain.education.mastery_estimation.ids import CompetencyId
from domain.education.mastery_estimation.value_objects.mastery_score import (
    MasteryScore,
)


@dataclass(frozen=True, slots=True)
class KnowledgeGap(EducationalValueObject):
    """Immutable record of one educationally weak competency.

    ``kind`` distinguishes a gap discovered directly from a competency's
    own weak evidence (``WEAK_EVIDENCE``) from one discovered because a
    structural prerequisite of some other, dependent competency is itself
    weak (``WEAK_PREREQUISITE``). Both are surfaced through the same shape
    so callers can reason over gaps uniformly, while still recovering the
    distinction and the structural strength that produced it.
    """

    competency_id: CompetencyId
    kind: KnowledgeGapKind
    severity: KnowledgeGapSeverity
    mastery_score: MasteryScore
    related_competency_id: CompetencyId | None = None
    dependency_strength: DependencyStrength | None = None

    def _validate(self) -> None:
        if not isinstance(self.competency_id, CompetencyId):
            raise EducationalInvariantViolation(
                "competency_id must be a CompetencyId",
                invariant="KnowledgeGap.competency_id.type",
            )
        if not isinstance(self.kind, KnowledgeGapKind):
            raise EducationalInvariantViolation(
                "kind must be a KnowledgeGapKind",
                invariant="KnowledgeGap.kind.type",
            )
        if not isinstance(self.severity, KnowledgeGapSeverity):
            raise EducationalInvariantViolation(
                "severity must be a KnowledgeGapSeverity",
                invariant="KnowledgeGap.severity.type",
            )
        if not isinstance(self.mastery_score, MasteryScore):
            raise EducationalInvariantViolation(
                "mastery_score must be a MasteryScore",
                invariant="KnowledgeGap.mastery_score.type",
            )
        if self.related_competency_id is not None and not isinstance(
            self.related_competency_id, CompetencyId
        ):
            raise EducationalInvariantViolation(
                "related_competency_id must be a CompetencyId when provided",
                invariant="KnowledgeGap.related_competency_id.type",
            )
        if self.dependency_strength is not None and not isinstance(
            self.dependency_strength, DependencyStrength
        ):
            raise EducationalInvariantViolation(
                "dependency_strength must be a DependencyStrength when "
                "provided",
                invariant="KnowledgeGap.dependency_strength.type",
            )
        if self.kind is KnowledgeGapKind.WEAK_PREREQUISITE:
            if self.related_competency_id is None:
                raise EducationalInvariantViolation(
                    "a weak_prerequisite gap must reference the dependent "
                    "competency via related_competency_id",
                    invariant="KnowledgeGap.related_competency_id.required",
                )
            if self.dependency_strength is None:
                raise EducationalInvariantViolation(
                    "a weak_prerequisite gap must carry the structural "
                    "dependency_strength that produced it",
                    invariant="KnowledgeGap.dependency_strength.required",
                )
        if (
            self.related_competency_id is not None
            and self.related_competency_id == self.competency_id
        ):
            raise EducationalInvariantViolation(
                "related_competency_id must differ from competency_id",
                invariant="KnowledgeGap.related_competency_id.distinct",
            )

    def is_prerequisite_gap(self) -> bool:
        return self.kind is KnowledgeGapKind.WEAK_PREREQUISITE

    def is_direct_gap(self) -> bool:
        return self.kind is KnowledgeGapKind.WEAK_EVIDENCE
