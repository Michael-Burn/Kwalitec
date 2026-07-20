"""Core educational reference value objects.

References are lightweight, immutable citations of educational knowledge
artefacts. They do not load aggregates, persist state, or encode transport
DTOs.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import (
    DependencyKind,
    RepresentationKind,
    TransferLevel,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    ConceptId,
    LearningObjectiveId,
    MisconceptionId,
)


@dataclass(frozen=True, slots=True)
class LearningObjectiveReference(EducationalValueObject):
    """Citation of a curriculum-grounded learning objective."""

    objective_id: LearningObjectiveId
    label: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.objective_id, LearningObjectiveId):
            raise EducationalInvariantViolation(
                "objective_id must be a LearningObjectiveId",
                invariant="LearningObjectiveReference.objective_id.type",
            )
        if self.label is not None:
            object.__setattr__(
                self,
                "label",
                require_non_empty_text(self.label, "label"),
            )


@dataclass(frozen=True, slots=True)
class ConceptReference(EducationalValueObject):
    """Citation of a teachable concept."""

    concept_id: ConceptId
    label: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId",
                invariant="ConceptReference.concept_id.type",
            )
        if self.label is not None:
            object.__setattr__(
                self,
                "label",
                require_non_empty_text(self.label, "label"),
            )


@dataclass(frozen=True, slots=True)
class MisconceptionReference(EducationalValueObject):
    """Citation of a stable incorrect mental model."""

    misconception_id: MisconceptionId
    related_concept_id: ConceptId | None = None
    label: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.misconception_id, MisconceptionId):
            raise EducationalInvariantViolation(
                "misconception_id must be a MisconceptionId",
                invariant="MisconceptionReference.misconception_id.type",
            )
        if self.related_concept_id is not None and not isinstance(
            self.related_concept_id, ConceptId
        ):
            raise EducationalInvariantViolation(
                "related_concept_id must be a ConceptId when provided",
                invariant="MisconceptionReference.related_concept_id.type",
            )
        if self.label is not None:
            object.__setattr__(
                self,
                "label",
                require_non_empty_text(self.label, "label"),
            )


@dataclass(frozen=True, slots=True)
class RepresentationReference(EducationalValueObject):
    """Citation of an educational representation of a concept."""

    representation_id: str
    kind: RepresentationKind
    concept_id: ConceptId | None = None
    label: str | None = None

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "representation_id",
            require_identity_value(self.representation_id, "representation_id"),
        )
        if not isinstance(self.kind, RepresentationKind):
            raise EducationalInvariantViolation(
                "kind must be a RepresentationKind",
                invariant="RepresentationReference.kind.type",
            )
        if self.concept_id is not None and not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId when provided",
                invariant="RepresentationReference.concept_id.type",
            )
        if self.label is not None:
            object.__setattr__(
                self,
                "label",
                require_non_empty_text(self.label, "label"),
            )


@dataclass(frozen=True, slots=True)
class DependencyReference(EducationalValueObject):
    """Citation of an educational dependency between knowledge entities.

    ``source_id`` is the upstream entity; ``target_id`` leans on the source
    (except for ``PARALLEL``, where order is permissive).
    """

    source_id: str
    target_id: str
    kind: DependencyKind
    label: str | None = None

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "source_id",
            require_identity_value(self.source_id, "source_id"),
        )
        object.__setattr__(
            self,
            "target_id",
            require_identity_value(self.target_id, "target_id"),
        )
        if not isinstance(self.kind, DependencyKind):
            raise EducationalInvariantViolation(
                "kind must be a DependencyKind",
                invariant="DependencyReference.kind.type",
            )
        if self.source_id == self.target_id:
            raise EducationalInvariantViolation(
                "dependency source_id and target_id must differ",
                invariant="DependencyReference.no_self_dependency",
            )
        if self.label is not None:
            object.__setattr__(
                self,
                "label",
                require_non_empty_text(self.label, "label"),
            )


@dataclass(frozen=True, slots=True)
class TransferContextReference(EducationalValueObject):
    """Citation of a transfer context with controlled surface variation."""

    context_id: str
    transfer_level: TransferLevel
    base_application_context_id: str | None = None
    label: str | None = None

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "context_id",
            require_identity_value(self.context_id, "context_id"),
        )
        if not isinstance(self.transfer_level, TransferLevel):
            raise EducationalInvariantViolation(
                "transfer_level must be a TransferLevel",
                invariant="TransferContextReference.transfer_level.type",
            )
        if self.transfer_level is TransferLevel.NONE:
            raise EducationalInvariantViolation(
                "transfer contexts require NEAR or FAR transfer_level "
                "(NONE denotes clone competence, not transfer)",
                invariant="TransferContextReference.transfer_level.not_none",
            )
        if self.base_application_context_id is not None:
            object.__setattr__(
                self,
                "base_application_context_id",
                require_identity_value(
                    self.base_application_context_id,
                    "base_application_context_id",
                ),
            )
        if self.label is not None:
            object.__setattr__(
                self,
                "label",
                require_non_empty_text(self.label, "label"),
            )


@dataclass(frozen=True, slots=True)
class ApplicationContextReference(EducationalValueObject):
    """Citation of a reusable application situation type."""

    context_id: str
    task_demand: str
    label: str | None = None

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "context_id",
            require_identity_value(self.context_id, "context_id"),
        )
        object.__setattr__(
            self,
            "task_demand",
            require_non_empty_text(self.task_demand, "task_demand"),
        )
        if self.label is not None:
            object.__setattr__(
                self,
                "label",
                require_non_empty_text(self.label, "label"),
            )
