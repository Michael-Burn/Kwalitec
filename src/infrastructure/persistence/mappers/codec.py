"""Pure conversion helpers for persistence mappers.

No educational reasoning. No validation beyond structural reconstruction.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from domain.education.foundation.ids import (
    ConceptId,
    LearningObjectiveId,
    MisconceptionId,
)
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
    MisconceptionReference,
)
from infrastructure.persistence.dto.common import (
    ConceptReferenceDTO,
    LearningObjectiveReferenceDTO,
    MisconceptionReferenceDTO,
)


def enum_value(member: Enum) -> str:
    return member.value


def optional_enum_value(member: Enum | None) -> str | None:
    return None if member is None else member.value


def id_value(identity: Any) -> str:
    return identity.value


def optional_id_value(identity: Any | None) -> str | None:
    return None if identity is None else identity.value


def datetime_to_iso(value: datetime) -> str:
    return value.isoformat()


def iso_to_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def sorted_id_values(identities: Any) -> tuple[str, ...]:
    return tuple(sorted(identity.value for identity in identities))


def sorted_strings(values: Any) -> tuple[str, ...]:
    return tuple(sorted(values))


def concept_ref_to_dto(ref: ConceptReference) -> ConceptReferenceDTO:
    return ConceptReferenceDTO(concept_id=ref.concept_id.value, label=ref.label)


def concept_ref_from_dto(dto: ConceptReferenceDTO) -> ConceptReference:
    return ConceptReference(concept_id=ConceptId(dto.concept_id), label=dto.label)


def objective_ref_to_dto(
    ref: LearningObjectiveReference,
) -> LearningObjectiveReferenceDTO:
    return LearningObjectiveReferenceDTO(
        objective_id=ref.objective_id.value,
        label=ref.label,
    )


def objective_ref_from_dto(
    dto: LearningObjectiveReferenceDTO,
) -> LearningObjectiveReference:
    return LearningObjectiveReference(
        objective_id=LearningObjectiveId(dto.objective_id),
        label=dto.label,
    )


def misconception_ref_to_dto(
    ref: MisconceptionReference,
) -> MisconceptionReferenceDTO:
    return MisconceptionReferenceDTO(
        misconception_id=ref.misconception_id.value,
        related_concept_id=optional_id_value(ref.related_concept_id),
        label=ref.label,
    )


def misconception_ref_from_dto(
    dto: MisconceptionReferenceDTO,
) -> MisconceptionReference:
    related = (
        ConceptId(dto.related_concept_id)
        if dto.related_concept_id is not None
        else None
    )
    return MisconceptionReference(
        misconception_id=MisconceptionId(dto.misconception_id),
        related_concept_id=related,
        label=dto.label,
    )
