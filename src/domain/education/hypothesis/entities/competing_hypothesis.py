"""Competing hypothesis — alternative educational explanation.

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    Competing Hypothesis
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.hypothesis.enums import HypothesisKind
from domain.education.hypothesis.value_objects.plausibility import Plausibility


@dataclass(frozen=True, slots=True)
class CompetingHypothesisId(EducationalValueObject):
    """Identity of a competing hypothesis within an EducationalHypothesis."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "CompetingHypothesisId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class CompetingHypothesis(EducationalEntity):
    """Alternative educational explanation competing with the primary one.

    Competitors must be educationally distinct — not rewordings of one idea.
    They do not select teaching strategy or replace diagnosis.
    """

    competing_id: CompetingHypothesisId
    hypothesis_kind: HypothesisKind
    explanation: str
    plausibility: Plausibility | None = None

    @property
    def entity_id(self) -> CompetingHypothesisId:
        return self.competing_id

    def _validate(self) -> None:
        if not isinstance(self.competing_id, CompetingHypothesisId):
            raise EducationalInvariantViolation(
                "competing_id must be a CompetingHypothesisId",
                invariant="CompetingHypothesis.competing_id.type",
            )
        if not isinstance(self.hypothesis_kind, HypothesisKind):
            raise EducationalInvariantViolation(
                "hypothesis_kind must be a HypothesisKind",
                invariant="CompetingHypothesis.hypothesis_kind.type",
            )
        object.__setattr__(
            self,
            "explanation",
            require_non_empty_text(self.explanation, "explanation"),
        )
        if self.plausibility is not None and not isinstance(
            self.plausibility, Plausibility
        ):
            raise EducationalInvariantViolation(
                "plausibility must be a Plausibility when provided",
                invariant="CompetingHypothesis.plausibility.type",
            )
        self._reject_how_to_smuggling(self.explanation)

    @staticmethod
    def _reject_how_to_smuggling(explanation: str) -> None:
        lowered = explanation.casefold()
        forbidden_fragments = (
            "therefore teach",
            "therefore use",
            "recommend strategy",
            "select strategy",
            "we should drill",
            "priority is",
        )
        for fragment in forbidden_fragments:
            if fragment in lowered:
                raise EducationalInvariantViolation(
                    "competing hypothesis must not encode teaching strategy "
                    "or priority",
                    invariant="CompetingHypothesis.no_how_to_smuggling",
                )

    def competitor_signature(self) -> tuple[str, str]:
        """Structural fingerprint used to reject duplicate competitors."""
        return (self.hypothesis_kind.value, self.explanation.casefold())

    def with_explanation(self, explanation: str) -> CompetingHypothesis:
        """Return a copy with an amended explanation."""
        return CompetingHypothesis(
            competing_id=self.competing_id,
            hypothesis_kind=self.hypothesis_kind,
            explanation=explanation,
            plausibility=self.plausibility,
        )
