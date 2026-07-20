"""Interpreted pattern — one educational pattern within an Interpretation.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md
Concept
    Interpreted Pattern
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.evidence_interpretation.enums import PatternKind
from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, EvidenceId, LearningEpisodeId

# Pattern kinds that require repeated observations (occurrence ≥ 2).
REPEATED_PATTERN_KINDS = frozenset(
    {
        PatternKind.REPEATED_RETRIEVAL_FAILURE,
        PatternKind.REPEATED_TRANSFER_FAILURE,
        PatternKind.REPEATED_CONFIDENCE_MISMATCH,
        PatternKind.REPEATED_MISCONCEPTION_INDICATOR,
        PatternKind.REPEATED_PROCEDURAL_ERROR,
        PatternKind.REPEATED_REFLECTION_THEME,
    }
)


@dataclass(frozen=True, slots=True)
class InterpretedPatternId(EducationalValueObject):
    """Identity of an interpreted pattern within an Interpretation."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "InterpretedPatternId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class InterpretedPattern(EducationalEntity):
    """Single interpreted educational pattern.

    Records a pattern observed across evidence (e.g. repeated retrieval
    failures). Never stores diagnoses, recommendations, or priority rankings.
    """

    pattern_id: InterpretedPatternId
    kind: PatternKind
    description: str
    evidence_ids: tuple[EvidenceId, ...]
    occurrence_count: int
    concept_id: ConceptId | None = None
    learning_episode_id: LearningEpisodeId | None = None

    @property
    def entity_id(self) -> InterpretedPatternId:
        return self.pattern_id

    def _validate(self) -> None:
        if not isinstance(self.pattern_id, InterpretedPatternId):
            raise EducationalInvariantViolation(
                "pattern_id must be an InterpretedPatternId",
                invariant="InterpretedPattern.pattern_id.type",
            )
        if not isinstance(self.kind, PatternKind):
            raise EducationalInvariantViolation(
                "kind must be a PatternKind",
                invariant="InterpretedPattern.kind.type",
            )
        object.__setattr__(
            self,
            "description",
            require_non_empty_text(self.description, "description"),
        )
        object.__setattr__(
            self,
            "evidence_ids",
            self._validate_evidence_ids(self.evidence_ids),
        )
        if not isinstance(self.occurrence_count, int) or isinstance(
            self.occurrence_count, bool
        ):
            raise EducationalInvariantViolation(
                "occurrence_count must be an integer",
                invariant="InterpretedPattern.occurrence_count.type",
            )
        minimum = 2 if self.kind in REPEATED_PATTERN_KINDS else 1
        if self.occurrence_count < minimum:
            raise EducationalInvariantViolation(
                f"occurrence_count must be at least {minimum} for {self.kind.value}",
                invariant="InterpretedPattern.occurrence_count.min",
            )
        if len(self.evidence_ids) < minimum:
            raise EducationalInvariantViolation(
                f"pattern {self.kind.value} must reference at least "
                f"{minimum} evidence id(s)",
                invariant="InterpretedPattern.evidence_ids.min",
            )
        if self.concept_id is not None and not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId when provided",
                invariant="InterpretedPattern.concept_id.type",
            )
        if self.learning_episode_id is not None and not isinstance(
            self.learning_episode_id, LearningEpisodeId
        ):
            raise EducationalInvariantViolation(
                "learning_episode_id must be a LearningEpisodeId when provided",
                invariant="InterpretedPattern.learning_episode_id.type",
            )

    @staticmethod
    def _validate_evidence_ids(
        evidence_ids: tuple[EvidenceId, ...] | list[EvidenceId],
    ) -> tuple[EvidenceId, ...]:
        items = tuple(evidence_ids)
        if not items:
            raise EducationalInvariantViolation(
                "interpreted pattern must reference evidence",
                invariant="InterpretedPattern.evidence_ids.required",
            )
        seen: set[str] = set()
        for evidence_id in items:
            if not isinstance(evidence_id, EvidenceId):
                raise EducationalInvariantViolation(
                    "evidence_ids must be EvidenceId values",
                    invariant="InterpretedPattern.evidence_ids.type",
                )
            if evidence_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate evidence id is not allowed in a pattern",
                    invariant="InterpretedPattern.evidence_ids.no_duplicate",
                )
            seen.add(evidence_id.value)
        return items

    def pattern_signature(self) -> tuple[str, str, str | None, str | None]:
        """Structural fingerprint used to prevent identical duplicate patterns."""
        return (
            self.kind.value,
            self.description.casefold(),
            None if self.concept_id is None else self.concept_id.value,
            None
            if self.learning_episode_id is None
            else self.learning_episode_id.value,
        )

    def is_repeated_kind(self) -> bool:
        return self.kind in REPEATED_PATTERN_KINDS

    def with_description(self, description: str) -> InterpretedPattern:
        """Return a copy with amended observational description."""
        return InterpretedPattern(
            pattern_id=self.pattern_id,
            kind=self.kind,
            description=description,
            evidence_ids=self.evidence_ids,
            occurrence_count=self.occurrence_count,
            concept_id=self.concept_id,
            learning_episode_id=self.learning_episode_id,
        )

    def with_occurrence_count(self, occurrence_count: int) -> InterpretedPattern:
        """Return a copy with amended occurrence count."""
        return InterpretedPattern(
            pattern_id=self.pattern_id,
            kind=self.kind,
            description=self.description,
            evidence_ids=self.evidence_ids,
            occurrence_count=occurrence_count,
            concept_id=self.concept_id,
            learning_episode_id=self.learning_episode_id,
        )
