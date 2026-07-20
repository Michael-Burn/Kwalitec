"""Map EvidenceRecord ↔ EvidenceRecordDTO."""

from __future__ import annotations

from domain.education.evidence import (
    ConfidenceMeasure,
    EvidenceContext,
    EvidenceContextId,
    EvidenceItem,
    EvidenceItemId,
    EvidenceItemKind,
    EvidenceRecord,
    EvidenceRecordStatus,
    EvidenceSource,
    EvidenceSourceId,
    EvidenceSourceKind,
    EvidenceStrength,
    EvidenceStrengthLevel,
    EvidenceTimestamp,
)
from domain.education.foundation.enums import ConfidenceLevel, LearningDimension
from domain.education.foundation.ids import ConceptId, EvidenceId, LearningEpisodeId
from infrastructure.persistence.dto.evidence import (
    ConfidenceMeasureDTO,
    EvidenceContextDTO,
    EvidenceItemDTO,
    EvidenceRecordDTO,
    EvidenceSourceDTO,
    EvidenceStrengthDTO,
)
from infrastructure.persistence.mappers.codec import (
    concept_ref_from_dto,
    concept_ref_to_dto,
    datetime_to_iso,
    enum_value,
    id_value,
    iso_to_datetime,
    objective_ref_from_dto,
    objective_ref_to_dto,
    optional_enum_value,
    optional_id_value,
    sorted_id_values,
)


class EvidenceMapper:
    """Pure structural mapper for EvidenceRecord."""

    @staticmethod
    def to_persistence(record: EvidenceRecord) -> EvidenceRecordDTO:
        return EvidenceRecordDTO(
            evidence_id=id_value(record.evidence_id),
            student_id=record.student_id,
            items=tuple(_item_to_dto(item) for item in record.items),
            source=EvidenceSourceDTO(
                source_id=id_value(record.source.source_id),
                kind=enum_value(record.source.kind),
                label=record.source.label,
                channel=record.source.channel,
            ),
            context=EvidenceContextDTO(
                context_id=id_value(record.context.context_id),
                situation=record.context.situation,
                learning_dimension=optional_enum_value(
                    record.context.learning_dimension
                ),
                concept_references=tuple(
                    concept_ref_to_dto(ref)
                    for ref in record.context.concept_references
                ),
                learning_objective_references=tuple(
                    objective_ref_to_dto(ref)
                    for ref in record.context.learning_objective_references
                ),
                learning_episode_ids=tuple(
                    id_value(eid) for eid in record.context.learning_episode_ids
                ),
            ),
            confidence=ConfidenceMeasureDTO(
                level=enum_value(record.confidence.level),
                ratio=record.confidence.ratio,
            ),
            strength=EvidenceStrengthDTO(level=enum_value(record.strength.level)),
            timestamp=datetime_to_iso(record.timestamp.occurred_at),
            known_concept_ids=sorted_id_values(record.known_concept_ids),
            known_episode_ids=sorted_id_values(record.known_episode_ids),
            concept_references=tuple(
                concept_ref_to_dto(ref) for ref in record.concept_references
            ),
            learning_episode_ids=tuple(
                id_value(eid) for eid in record.learning_episode_ids
            ),
            status=enum_value(record.status),
            invalidation_reason=record.invalidation_reason,
        )

    @staticmethod
    def to_domain(dto: EvidenceRecordDTO) -> EvidenceRecord:
        dimension = (
            LearningDimension(dto.context.learning_dimension)
            if dto.context.learning_dimension is not None
            else None
        )
        return EvidenceRecord(
            evidence_id=EvidenceId(dto.evidence_id),
            student_id=dto.student_id,
            items=tuple(_item_from_dto(item) for item in dto.items),
            source=EvidenceSource(
                source_id=EvidenceSourceId(dto.source.source_id),
                kind=EvidenceSourceKind(dto.source.kind),
                label=dto.source.label,
                channel=dto.source.channel,
            ),
            context=EvidenceContext(
                context_id=EvidenceContextId(dto.context.context_id),
                situation=dto.context.situation,
                learning_dimension=dimension,
                concept_references=tuple(
                    concept_ref_from_dto(ref)
                    for ref in dto.context.concept_references
                ),
                learning_objective_references=tuple(
                    objective_ref_from_dto(ref)
                    for ref in dto.context.learning_objective_references
                ),
                learning_episode_ids=tuple(
                    LearningEpisodeId(eid)
                    for eid in dto.context.learning_episode_ids
                ),
            ),
            confidence=ConfidenceMeasure(
                level=ConfidenceLevel(dto.confidence.level),
                ratio=dto.confidence.ratio,
            ),
            strength=EvidenceStrength(level=EvidenceStrengthLevel(dto.strength.level)),
            timestamp=EvidenceTimestamp.of(iso_to_datetime(dto.timestamp)),
            known_concept_ids=frozenset(
                ConceptId(cid) for cid in dto.known_concept_ids
            ),
            known_episode_ids=frozenset(
                LearningEpisodeId(eid) for eid in dto.known_episode_ids
            ),
            concept_references=tuple(
                concept_ref_from_dto(ref) for ref in dto.concept_references
            ),
            learning_episode_ids=tuple(
                LearningEpisodeId(eid) for eid in dto.learning_episode_ids
            ),
            status=EvidenceRecordStatus(dto.status),
            invalidation_reason=dto.invalidation_reason,
        )


def _item_to_dto(item: EvidenceItem) -> EvidenceItemDTO:
    return EvidenceItemDTO(
        item_id=id_value(item.item_id),
        kind=enum_value(item.kind),
        observation=item.observation,
        concept_id=optional_id_value(item.concept_id),
        learning_episode_id=optional_id_value(item.learning_episode_id),
    )


def _item_from_dto(dto: EvidenceItemDTO) -> EvidenceItem:
    return EvidenceItem(
        item_id=EvidenceItemId(dto.item_id),
        kind=EvidenceItemKind(dto.kind),
        observation=dto.observation,
        concept_id=ConceptId(dto.concept_id) if dto.concept_id else None,
        learning_episode_id=(
            LearningEpisodeId(dto.learning_episode_id)
            if dto.learning_episode_id
            else None
        ),
    )
