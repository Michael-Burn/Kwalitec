"""Map EducationalDigitalTwin ↔ DigitalTwinDTO."""

from __future__ import annotations

from domain.education.digital_twin import (
    ConceptState,
    ConceptStateId,
    ConfidenceProfile,
    EducationalDigitalTwin,
    EvidenceHistoryEntry,
    EvidenceHistoryEntryId,
    InterventionHistoryEntry,
    InterventionHistoryEntryId,
    LearnerActivityStatus,
    LearnerState,
    LearnerStateId,
    LearningTrajectory,
    MasteryBand,
    MasteryState,
    MisconceptionPresence,
    MisconceptionState,
    MisconceptionStateId,
    RetentionBand,
    RetentionState,
    TrajectoryPoint,
    TrajectoryPointKind,
    TwinStatus,
)
from domain.education.foundation.enums import (
    ConfidenceLevel,
    EvidenceType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.ids import (
    ConceptId,
    DigitalTwinId,
    EvidenceId,
    MisconceptionId,
)
from infrastructure.persistence.dto.digital_twin import (
    ConceptStateDTO,
    ConfidenceProfileDTO,
    DigitalTwinDTO,
    EvidenceHistoryEntryDTO,
    InterventionHistoryEntryDTO,
    LearnerStateDTO,
    LearningTrajectoryDTO,
    MasteryStateDTO,
    MisconceptionStateDTO,
    RetentionStateDTO,
    TrajectoryPointDTO,
)
from infrastructure.persistence.mappers.codec import (
    enum_value,
    id_value,
    optional_enum_value,
    optional_id_value,
)


class DigitalTwinMapper:
    """Pure structural mapper for EducationalDigitalTwin."""

    @staticmethod
    def to_persistence(twin: EducationalDigitalTwin) -> DigitalTwinDTO:
        return DigitalTwinDTO(
            twin_id=id_value(twin.twin_id),
            student_id=twin.student_id,
            learner_state=_learner_to_dto(twin.learner_state),
            concept_states=tuple(
                _concept_state_to_dto(state) for state in twin.concept_states
            ),
            misconception_states=tuple(
                _misconception_state_to_dto(state)
                for state in twin.misconception_states
            ),
            evidence_history=tuple(
                _evidence_entry_to_dto(entry) for entry in twin.evidence_history
            ),
            intervention_history=tuple(
                _intervention_entry_to_dto(entry)
                for entry in twin.intervention_history
            ),
            retention=_retention_to_dto(twin.retention),
            confidence=_confidence_to_dto(twin.confidence),
            trajectory=_trajectory_to_dto(twin.trajectory),
            status=enum_value(twin.status),
        )

    @staticmethod
    def to_domain(dto: DigitalTwinDTO) -> EducationalDigitalTwin:
        return EducationalDigitalTwin(
            twin_id=DigitalTwinId(dto.twin_id),
            student_id=dto.student_id,
            learner_state=_learner_from_dto(dto.learner_state),
            concept_states=tuple(
                _concept_state_from_dto(state) for state in dto.concept_states
            ),
            misconception_states=tuple(
                _misconception_state_from_dto(state)
                for state in dto.misconception_states
            ),
            evidence_history=tuple(
                _evidence_entry_from_dto(entry) for entry in dto.evidence_history
            ),
            intervention_history=tuple(
                _intervention_entry_from_dto(entry)
                for entry in dto.intervention_history
            ),
            retention=_retention_from_dto(dto.retention),
            confidence=_confidence_from_dto(dto.confidence),
            trajectory=_trajectory_from_dto(dto.trajectory),
            status=TwinStatus(dto.status),
        )


def _mastery_to_dto(mastery: MasteryState) -> MasteryStateDTO:
    return MasteryStateDTO(band=enum_value(mastery.band), ratio=mastery.ratio)


def _mastery_from_dto(dto: MasteryStateDTO) -> MasteryState:
    return MasteryState(band=MasteryBand(dto.band), ratio=dto.ratio)


def _retention_to_dto(retention: RetentionState) -> RetentionStateDTO:
    return RetentionStateDTO(band=enum_value(retention.band), ratio=retention.ratio)


def _retention_from_dto(dto: RetentionStateDTO) -> RetentionState:
    return RetentionState(band=RetentionBand(dto.band), ratio=dto.ratio)


def _confidence_to_dto(confidence: ConfidenceProfile) -> ConfidenceProfileDTO:
    return ConfidenceProfileDTO(
        overall=enum_value(confidence.overall),
        ratio=confidence.ratio,
    )


def _confidence_from_dto(dto: ConfidenceProfileDTO) -> ConfidenceProfile:
    return ConfidenceProfile(
        overall=ConfidenceLevel(dto.overall),
        ratio=dto.ratio,
    )


def _trajectory_to_dto(trajectory: LearningTrajectory) -> LearningTrajectoryDTO:
    return LearningTrajectoryDTO(
        points=tuple(
            TrajectoryPointDTO(
                sequence=point.sequence,
                kind=enum_value(point.kind),
                label=point.label,
            )
            for point in trajectory.points
        )
    )


def _trajectory_from_dto(dto: LearningTrajectoryDTO) -> LearningTrajectory:
    return LearningTrajectory(
        points=tuple(
            TrajectoryPoint(
                sequence=point.sequence,
                kind=TrajectoryPointKind(point.kind),
                label=point.label,
            )
            for point in dto.points
        )
    )


def _learner_to_dto(state: LearnerState) -> LearnerStateDTO:
    return LearnerStateDTO(
        learner_state_id=id_value(state.learner_state_id),
        student_id=state.student_id,
        activity_status=enum_value(state.activity_status),
    )


def _learner_from_dto(dto: LearnerStateDTO) -> LearnerState:
    return LearnerState(
        learner_state_id=LearnerStateId(dto.learner_state_id),
        student_id=dto.student_id,
        activity_status=LearnerActivityStatus(dto.activity_status),
    )


def _concept_state_to_dto(state: ConceptState) -> ConceptStateDTO:
    return ConceptStateDTO(
        concept_state_id=id_value(state.concept_state_id),
        concept_id=id_value(state.concept_id),
        mastery=_mastery_to_dto(state.mastery),
        retention=_retention_to_dto(state.retention),
        evidence_count=state.evidence_count,
    )


def _concept_state_from_dto(dto: ConceptStateDTO) -> ConceptState:
    return ConceptState(
        concept_state_id=ConceptStateId(dto.concept_state_id),
        concept_id=ConceptId(dto.concept_id),
        mastery=_mastery_from_dto(dto.mastery),
        retention=_retention_from_dto(dto.retention),
        evidence_count=dto.evidence_count,
    )


def _misconception_state_to_dto(state: MisconceptionState) -> MisconceptionStateDTO:
    return MisconceptionStateDTO(
        misconception_state_id=id_value(state.misconception_state_id),
        misconception_id=id_value(state.misconception_id),
        presence=enum_value(state.presence),
        related_concept_id=optional_id_value(state.related_concept_id),
    )


def _misconception_state_from_dto(dto: MisconceptionStateDTO) -> MisconceptionState:
    related = (
        ConceptId(dto.related_concept_id)
        if dto.related_concept_id is not None
        else None
    )
    return MisconceptionState(
        misconception_state_id=MisconceptionStateId(dto.misconception_state_id),
        misconception_id=MisconceptionId(dto.misconception_id),
        presence=MisconceptionPresence(dto.presence),
        related_concept_id=related,
    )


def _evidence_entry_to_dto(entry: EvidenceHistoryEntry) -> EvidenceHistoryEntryDTO:
    return EvidenceHistoryEntryDTO(
        entry_id=id_value(entry.entry_id),
        evidence_id=id_value(entry.evidence_id),
        evidence_type=enum_value(entry.evidence_type),
        sequence=entry.sequence,
        concept_id=optional_id_value(entry.concept_id),
        note=entry.note,
    )


def _evidence_entry_from_dto(dto: EvidenceHistoryEntryDTO) -> EvidenceHistoryEntry:
    concept = ConceptId(dto.concept_id) if dto.concept_id is not None else None
    return EvidenceHistoryEntry(
        entry_id=EvidenceHistoryEntryId(dto.entry_id),
        evidence_id=EvidenceId(dto.evidence_id),
        evidence_type=EvidenceType(dto.evidence_type),
        sequence=dto.sequence,
        concept_id=concept,
        note=dto.note,
    )


def _intervention_entry_to_dto(
    entry: InterventionHistoryEntry,
) -> InterventionHistoryEntryDTO:
    return InterventionHistoryEntryDTO(
        entry_id=id_value(entry.entry_id),
        intervention_ref=entry.intervention_ref,
        sequence=entry.sequence,
        strategy_type=optional_enum_value(entry.strategy_type),
        intention_type=optional_enum_value(entry.intention_type),
        concept_id=optional_id_value(entry.concept_id),
        note=entry.note,
    )


def _intervention_entry_from_dto(
    dto: InterventionHistoryEntryDTO,
) -> InterventionHistoryEntry:
    strategy = (
        TeachingStrategyType(dto.strategy_type)
        if dto.strategy_type is not None
        else None
    )
    intention = (
        TeachingIntentionType(dto.intention_type)
        if dto.intention_type is not None
        else None
    )
    concept = ConceptId(dto.concept_id) if dto.concept_id is not None else None
    return InterventionHistoryEntry(
        entry_id=InterventionHistoryEntryId(dto.entry_id),
        intervention_ref=dto.intervention_ref,
        sequence=dto.sequence,
        strategy_type=strategy,
        intention_type=intention,
        concept_id=concept,
        note=dto.note,
    )
