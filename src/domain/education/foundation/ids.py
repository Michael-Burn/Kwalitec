"""Educational identity value objects.

Opaque, immutable identifiers for educational domain objects. Identities are
not database keys and carry no persistence semantics.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)


@dataclass(frozen=True, slots=True)
class LearningObjectiveId(EducationalValueObject):
    """Identity of a curriculum-grounded learning objective."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "LearningObjectiveId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ConceptId(EducationalValueObject):
    """Identity of a teachable concept."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "ConceptId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class LearningEpisodeId(EducationalValueObject):
    """Identity of a bounded learning episode."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "LearningEpisodeId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class TeachingStrategyId(EducationalValueObject):
    """Identity of a named teaching strategy commitment."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "TeachingStrategyId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class TeachingIntentionId(EducationalValueObject):
    """Identity of a teaching intention."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "TeachingIntentionId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class DiagnosisId(EducationalValueObject):
    """Identity of an educational diagnosis."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "DiagnosisId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class HypothesisId(EducationalValueObject):
    """Identity of an educational hypothesis."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "HypothesisId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class PriorityId(EducationalValueObject):
    """Identity of an educational priority decision."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "PriorityId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class DecisionId(EducationalValueObject):
    """Identity of an educational execution-readiness decision."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "DecisionId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class OrchestratorId(EducationalValueObject):
    """Identity of an educational orchestrator coordination turn."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "OrchestratorId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class DigitalTwinId(EducationalValueObject):
    """Identity of an Educational Digital Twin aggregate."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "DigitalTwinId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class EvidenceId(EducationalValueObject):
    """Identity of an educational evidence observation."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "EvidenceId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ReflectionId(EducationalValueObject):
    """Identity of a student reflection."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "ReflectionId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class StudentKnowledgeId(EducationalValueObject):
    """Identity of a student knowledge estimate / knowledge state slice."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "StudentKnowledgeId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class MisconceptionId(EducationalValueObject):
    """Identity of an authored or diagnosed misconception."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "MisconceptionId"),
        )

    def __str__(self) -> str:
        return self.value
