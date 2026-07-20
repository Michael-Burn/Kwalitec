"""AssessmentApplicationService — evidence recording and history queries."""

from __future__ import annotations

from application.commands.record_evidence import RecordEvidence
from application.dto.evidence import EvidenceHistoryDTO, EvidenceRecordDTO
from application.errors import ConflictError, NotFoundError
from application.events.evidence import EvidenceRecordedApplicationEvent
from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.unit_of_work import UnitOfWork
from application.queries.get_evidence_history import GetEvidenceHistory
from application.services.mappers import (
    to_evidence_history_dto,
    to_evidence_record_dto,
)
from domain.education.evidence import (
    ConfidenceMeasure,
    EvidenceContext,
    EvidenceContextId,
    EvidenceItem,
    EvidenceItemId,
    EvidenceItemKind,
    EvidenceRecord,
    EvidenceSource,
    EvidenceSourceId,
    EvidenceSourceKind,
    EvidenceStrength,
    EvidenceStrengthLevel,
    EvidenceTimestamp,
)
from domain.education.foundation.enums import (
    ConfidenceLevel,
    EvidenceType,
    LearningDimension,
)
from domain.education.foundation.errors import EducationalDomainError
from domain.education.foundation.ids import (
    ConceptId,
    DigitalTwinId,
    EvidenceId,
    LearningEpisodeId,
)
from domain.education.foundation.references import ConceptReference


class AssessmentApplicationService:
    """Coordinates evidence recording and history retrieval.

    Does not diagnose, interpret, or prioritise. Optionally appends Twin
    evidence history when ``twin_id`` is supplied on the command.
    """

    def __init__(
        self,
        uow: UnitOfWork,
        events: ApplicationEventPublisher,
        clock: Clock,
    ) -> None:
        self._uow = uow
        self._events = events
        self._clock = clock

    def record_evidence(self, command: RecordEvidence) -> EvidenceRecordDTO:
        """Construct EvidenceRecord via domain factory, commit, publish."""
        with self._uow:
            try:
                record = self._build_record(command)
            except EducationalDomainError as exc:
                raise ConflictError(str(exc)) from exc
            self._uow.evidence.save(record)

            if command.twin_id:
                self._append_twin_history(command)

            if command.learning_episode_ids:
                self._attach_to_episodes(command)

            self._uow.commit()

        self._events.publish(
            EvidenceRecordedApplicationEvent.create(
                evidence_id=record.evidence_id.value,
                student_id=record.student_id,
                occurred_at=self._clock.now(),
            )
        )
        return to_evidence_record_dto(record)

    def get_evidence_history(self, query: GetEvidenceHistory) -> EvidenceHistoryDTO:
        with self._uow:
            records = self._uow.evidence.list_by_student(query.student_id)
        return to_evidence_history_dto(query.student_id, records)

    def _build_record(self, command: RecordEvidence) -> EvidenceRecord:
        if not command.items:
            raise ConflictError("RecordEvidence requires at least one evidence item")
        concept_ids = tuple(ConceptId(cid) for cid in command.concept_ids)
        episode_ids = tuple(
            LearningEpisodeId(eid) for eid in command.learning_episode_ids
        )
        items = [
            EvidenceItem(
                item_id=EvidenceItemId(spec.item_id),
                kind=EvidenceItemKind(spec.kind),
                observation=spec.summary,
                concept_id=ConceptId(spec.concept_id) if spec.concept_id else None,
                learning_episode_id=(
                    LearningEpisodeId(spec.learning_episode_id)
                    if spec.learning_episode_id
                    else None
                ),
            )
            for spec in command.items
        ]
        concept_refs = tuple(
            ConceptReference(concept_id=cid) for cid in concept_ids
        )
        return EvidenceRecord.record(
            evidence_id=EvidenceId(command.evidence_id),
            student_id=command.student_id,
            items=items,
            source=EvidenceSource(
                source_id=EvidenceSourceId(command.source_id),
                kind=EvidenceSourceKind(command.source_kind),
                label=command.source_label,
            ),
            context=EvidenceContext(
                context_id=EvidenceContextId(command.context_id),
                situation=command.context_summary,
                learning_dimension=LearningDimension(command.context_dimension),
                concept_references=concept_refs,
                learning_episode_ids=episode_ids,
            ),
            confidence=ConfidenceMeasure.of(
                ConfidenceLevel(command.confidence_level),
                ratio=command.confidence_ratio,
            ),
            strength=EvidenceStrength(level=EvidenceStrengthLevel(command.strength_level)),
            timestamp=EvidenceTimestamp(occurred_at=command.occurred_at),
            known_concept_ids=frozenset(concept_ids) if concept_ids else None,
            known_episode_ids=frozenset(episode_ids) if episode_ids else None,
            concept_references=list(concept_refs),
            learning_episode_ids=list(episode_ids),
        )

    def _append_twin_history(self, command: RecordEvidence) -> None:
        assert command.twin_id is not None
        twin = self._uow.digital_twins.get(DigitalTwinId(command.twin_id))
        if twin is None:
            raise NotFoundError("EducationalDigitalTwin", command.twin_id)
        evidence_type = EvidenceType(
            command.evidence_type_for_twin or EvidenceType.PERFORMANCE.value
        )
        concept_id = command.concept_ids[0] if command.concept_ids else None
        try:
            twin.record_evidence(
                command.evidence_id,
                evidence_type,
                concept_id=concept_id,
            )
        except EducationalDomainError as exc:
            raise ConflictError(str(exc)) from exc
        self._uow.digital_twins.save(twin)

    def _attach_to_episodes(self, command: RecordEvidence) -> None:
        for episode_key in command.learning_episode_ids:
            episode = self._uow.episodes.get(LearningEpisodeId(episode_key))
            if episode is None:
                raise NotFoundError("LearningEpisode", episode_key)
            try:
                episode.attach_evidence(EvidenceId(command.evidence_id))
            except EducationalDomainError as exc:
                raise ConflictError(str(exc)) from exc
            self._uow.episodes.save(episode)
