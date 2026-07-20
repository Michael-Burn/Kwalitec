"""TwinApplicationService — Digital Twin memory coordination and queries."""

from __future__ import annotations

from application.commands.update_digital_twin import TwinUpdateKind, UpdateDigitalTwin
from application.dto.learner import LearnerStateDTO
from application.dto.trajectory import LearningTrajectoryDTO
from application.dto.twin import DigitalTwinSummaryDTO
from application.errors import ApplicationError, ConflictError, NotFoundError
from application.events.twin import DigitalTwinUpdatedApplicationEvent
from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.unit_of_work import UnitOfWork
from application.queries.get_learner_state import GetLearnerState
from application.queries.get_learning_trajectory import GetLearningTrajectory
from application.services.mappers import (
    to_learner_state_dto,
    to_learning_trajectory_dto,
    to_twin_summary_dto,
)
from domain.education.digital_twin import (
    ConfidenceProfile,
    EducationalDigitalTwin,
    LearnerActivityStatus,
    MasteryBand,
    MasteryState,
    RetentionBand,
    RetentionState,
)
from domain.education.foundation.enums import ConfidenceLevel, EvidenceType
from domain.education.foundation.errors import EducationalDomainError
from domain.education.foundation.ids import DigitalTwinId


class TwinApplicationService:
    """Coordinates Digital Twin load / update / query workflows.

    Applies supplied memory values only. Does not calculate mastery, retention,
    confidence, or educational priorities.
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

    def update_digital_twin(self, command: UpdateDigitalTwin) -> DigitalTwinSummaryDTO:
        """Load Twin, apply the requested memory update, commit, publish."""
        with self._uow:
            twin = self._require_twin(command.twin_id)
            try:
                self._apply_update(twin, command)
            except EducationalDomainError as exc:
                raise ConflictError(str(exc)) from exc
            self._uow.digital_twins.save(twin)
            self._uow.commit()
        kind = command.update_kind.value
        self._events.publish(
            DigitalTwinUpdatedApplicationEvent.create(
                twin_id=twin.twin_id.value,
                student_id=twin.student_id,
                update_kind=kind,
                occurred_at=self._clock.now(),
            )
        )
        return to_twin_summary_dto(twin, update_kind=kind)

    def get_learner_state(self, query: GetLearnerState) -> LearnerStateDTO:
        with self._uow:
            twin = self._resolve_twin(
                twin_id=query.twin_id, student_id=query.student_id
            )
        return to_learner_state_dto(twin)

    def get_learning_trajectory(
        self, query: GetLearningTrajectory
    ) -> LearningTrajectoryDTO:
        with self._uow:
            twin = self._resolve_twin(
                twin_id=query.twin_id, student_id=query.student_id
            )
        return to_learning_trajectory_dto(twin)

    def _require_twin(self, twin_id: str) -> EducationalDigitalTwin:
        twin = self._uow.digital_twins.get(DigitalTwinId(twin_id))
        if twin is None:
            raise NotFoundError("EducationalDigitalTwin", twin_id)
        return twin

    def _resolve_twin(
        self, *, twin_id: str | None, student_id: str | None
    ) -> EducationalDigitalTwin:
        if twin_id:
            return self._require_twin(twin_id)
        if student_id:
            twin = self._uow.digital_twins.get_by_student(student_id)
            if twin is None:
                raise NotFoundError("EducationalDigitalTwin", student_id)
            return twin
        raise ApplicationError("query requires twin_id or student_id")

    def _apply_update(
        self, twin: EducationalDigitalTwin, command: UpdateDigitalTwin
    ) -> None:
        kind = command.update_kind
        if kind is TwinUpdateKind.RECORD_EVIDENCE:
            if not command.evidence_id or not command.evidence_type:
                raise ApplicationError(
                    "record_evidence requires evidence_id and evidence_type"
                )
            twin.record_evidence(
                command.evidence_id,
                EvidenceType(command.evidence_type),
                concept_id=command.concept_id,
                note=command.note,
            )
            return
        if kind is TwinUpdateKind.UPDATE_MASTERY:
            if not command.concept_id or not command.mastery_band:
                raise ApplicationError(
                    "update_mastery requires concept_id and mastery_band"
                )
            twin.update_mastery(
                command.concept_id,
                MasteryState.of(
                    MasteryBand(command.mastery_band),
                    ratio=command.mastery_ratio,
                ),
            )
            return
        if kind is TwinUpdateKind.UPDATE_RETENTION:
            if not command.retention_band:
                raise ApplicationError("update_retention requires retention_band")
            twin.update_retention(
                RetentionState.of(
                    RetentionBand(command.retention_band),
                    ratio=command.retention_ratio,
                ),
                concept_id=command.concept_id,
            )
            return
        if kind is TwinUpdateKind.UPDATE_CONFIDENCE:
            if not command.confidence_level:
                raise ApplicationError("update_confidence requires confidence_level")
            twin.update_confidence(
                ConfidenceProfile.of(
                    ConfidenceLevel(command.confidence_level),
                    ratio=command.confidence_ratio,
                )
            )
            return
        if kind is TwinUpdateKind.UPDATE_ACTIVITY:
            if not command.activity_status:
                raise ApplicationError("update_activity requires activity_status")
            twin.update_learner_activity(LearnerActivityStatus(command.activity_status))
            return
        raise ApplicationError(f"unsupported twin update kind: {kind}")
