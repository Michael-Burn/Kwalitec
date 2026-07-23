"""Recommendation Engine identity value objects.

Opaque, immutable identifiers scoped to this bounded context. Identities are
not database keys and carry no persistence semantics.

``SubjectId`` and ``CompetencyId`` intentionally reuse the same string
values as the corresponding identities in ``student_state``,
``educational_evidence``, ``knowledge_graph``, and ``mastery_estimation`` —
this engine's whole purpose is to correlate reasoning across those bounded
contexts. The correlation is a same-string-value convention, not a claim
that the Python types are interchangeable: every read from another
bounded context's aggregate goes through an explicit, narrow coercion at
the boundary (see ``engines/recommendation_engine.py``).
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)


@dataclass(frozen=True, slots=True)
class RecommendationSetId(EducationalValueObject):
    """Identity of a single RecommendationSet produced by the engine."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "RecommendationSetId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class RecommendationId(EducationalValueObject):
    """Identity of a single Recommendation within a RecommendationSet."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "RecommendationId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class SubjectId(EducationalValueObject):
    """Identity of a subject scoped to a recommendation."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "SubjectId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class CompetencyId(EducationalValueObject):
    """Identity of a competency scoped to a recommendation."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self, "value", require_identity_value(self.value, "CompetencyId")
        )

    def __str__(self) -> str:
        return self.value
