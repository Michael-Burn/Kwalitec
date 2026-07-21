"""EvidenceUpdateService — store captured evidence as Educational OS records.

Validates captured evidence, transforms it into ``EvidenceRecord`` aggregates,
persists through repository ports inside a unit of work, optionally appends
Twin evidence history, and returns an auditable update summary.

Never diagnoses, recommends, prioritises, plans study, generates missions,
or invokes AI.
"""

from __future__ import annotations

from application.errors import ApplicationError, ConflictError, NotFoundError
from application.events.evidence import EvidenceRecordedApplicationEvent
from application.evidence_capture.captured_evidence import CapturedEvidence
from application.evidence_update.evidence_transformer import (
    EvidenceTransformer,
    EvidenceTransformError,
)
from application.evidence_update.evidence_update_request import (
    EvidenceUpdateRequest,
)
from application.evidence_update.evidence_update_result import (
    EvidenceUpdateAuditEntry,
    EvidenceUpdateOutcome,
    EvidenceUpdateResult,
)
from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.unit_of_work import UnitOfWork
from domain.education.evidence import EvidenceRecord
from domain.education.foundation.enums import EvidenceType
from domain.education.foundation.errors import EducationalDomainError
from domain.education.foundation.ids import DigitalTwinId, EvidenceId, LearningEpisodeId


class EvidenceUpdateError(ApplicationError):
    """Base error for Educational Evidence Update failures."""


class EvidenceUpdateService:
    """Update educational evidence from captured session outcomes.

    Input: ``CapturedEvidence`` (via ``EvidenceUpdateRequest``).
    Output: ``EvidenceUpdateResult``.

    Idempotent on ``evidence_id``. Transactional via ``UnitOfWork``.
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

    def update(
        self,
        request: EvidenceUpdateRequest | CapturedEvidence,
    ) -> EvidenceUpdateResult:
        """Validate, transform, store, and summarise an evidence update.

        Args:
            request: ``EvidenceUpdateRequest`` or bare ``CapturedEvidence``.

        Returns:
            ``EvidenceUpdateResult`` describing apply / duplicate outcome.

        Raises:
            EvidenceUpdateError: When validation or transformation fails.
            ConflictError: When Twin / episode attachment conflicts.
        """
        normalised = self._normalise_request(request)
        self._validate_request(normalised)

        evidence_id = EvidenceId(normalised.captured.evidence_id)
        audit: list[EvidenceUpdateAuditEntry] = []

        with self._uow:
            existing = self._uow.evidence.get(evidence_id)
            if existing is not None:
                result = self._duplicate_result(existing, audit)
                self._uow.commit()
                return result

            try:
                record = EvidenceTransformer.transform(normalised)
            except EvidenceTransformError as exc:
                raise EvidenceUpdateError(str(exc)) from exc

            domain_events = record.pull_events()
            for event in domain_events:
                audit.append(
                    EvidenceUpdateAuditEntry(
                        kind=type(event).__name__,
                        detail=(
                            f"student_id={getattr(event, 'student_id', '')}; "
                            f"item_count={getattr(event, 'item_count', '')}"
                        ),
                        evidence_id=record.evidence_id.value,
                    )
                )

            self._uow.evidence.save(record)
            audit.append(
                EvidenceUpdateAuditEntry(
                    kind="evidence_stored",
                    detail="EvidenceRecord saved through EvidenceRepository",
                    evidence_id=record.evidence_id.value,
                )
            )

            twin_updated = False
            if normalised.update_twin:
                twin_updated = self._append_twin_history(normalised, record, audit)

            if normalised.learning_episode_ids:
                self._attach_to_episodes(normalised, record, audit)

            self._uow.commit()

        self._events.publish(
            EvidenceRecordedApplicationEvent.create(
                evidence_id=record.evidence_id.value,
                student_id=record.student_id,
                occurred_at=self._clock.now(),
            )
        )
        audit.append(
            EvidenceUpdateAuditEntry(
                kind="EvidenceRecordedApplicationEvent",
                detail="application event published",
                evidence_id=record.evidence_id.value,
            )
        )

        return EvidenceUpdateResult(
            evidence_id=record.evidence_id.value,
            student_id=record.student_id,
            outcome=EvidenceUpdateOutcome.APPLIED,
            item_count=len(record.items),
            strength_level=record.strength.level.value,
            confidence_level=record.confidence.level.value,
            status=record.status.value,
            twin_updated=twin_updated,
            audit_trail=tuple(audit),
        )

    def _normalise_request(
        self,
        request: EvidenceUpdateRequest | CapturedEvidence,
    ) -> EvidenceUpdateRequest:
        if isinstance(request, EvidenceUpdateRequest):
            return request
        if isinstance(request, CapturedEvidence):
            return EvidenceUpdateRequest(captured=request)
        raise EvidenceUpdateError(
            "request must be EvidenceUpdateRequest or CapturedEvidence"
        )

    def _validate_request(self, request: EvidenceUpdateRequest) -> None:
        captured = request.captured
        if not (captured.evidence_id or "").strip():
            raise EvidenceUpdateError("evidence_id is required")
        if not (captured.outcome.student_id or "").strip():
            raise EvidenceUpdateError("student_id is required on captured evidence")
        if captured.captured_at.tzinfo is None:
            raise EvidenceUpdateError("captured_at must be timezone-aware")

    def _duplicate_result(
        self,
        existing: EvidenceRecord,
        audit: list[EvidenceUpdateAuditEntry],
    ) -> EvidenceUpdateResult:
        audit.append(
            EvidenceUpdateAuditEntry(
                kind="duplicate_skipped",
                detail="evidence_id already present; idempotent no-op",
                evidence_id=existing.evidence_id.value,
            )
        )
        return EvidenceUpdateResult(
            evidence_id=existing.evidence_id.value,
            student_id=existing.student_id,
            outcome=EvidenceUpdateOutcome.DUPLICATE,
            item_count=len(existing.items),
            strength_level=existing.strength.level.value,
            confidence_level=existing.confidence.level.value,
            status=existing.status.value,
            twin_updated=False,
            audit_trail=tuple(audit),
        )

    def _append_twin_history(
        self,
        request: EvidenceUpdateRequest,
        record: EvidenceRecord,
        audit: list[EvidenceUpdateAuditEntry],
    ) -> bool:
        twin = None
        if request.twin_id:
            twin = self._uow.digital_twins.get(DigitalTwinId(request.twin_id))
            if twin is None:
                raise NotFoundError("EducationalDigitalTwin", request.twin_id)
        else:
            twin = self._uow.digital_twins.get_by_student(record.student_id)

        if twin is None:
            audit.append(
                EvidenceUpdateAuditEntry(
                    kind="twin_skipped",
                    detail="no twin available for educational-state update",
                    evidence_id=record.evidence_id.value,
                )
            )
            return False

        if twin.has_evidence(record.evidence_id):
            audit.append(
                EvidenceUpdateAuditEntry(
                    kind="twin_duplicate_skipped",
                    detail="twin already remembers this evidence_id",
                    evidence_id=record.evidence_id.value,
                )
            )
            return False

        concept_id = request.concept_ids[0] if request.concept_ids else None
        try:
            twin.record_evidence(
                record.evidence_id,
                EvidenceType.REFLECTION,
                concept_id=concept_id,
                note="study_session_reflection",
            )
        except EducationalDomainError as exc:
            raise ConflictError(str(exc)) from exc

        self._uow.digital_twins.save(twin)
        audit.append(
            EvidenceUpdateAuditEntry(
                kind="twin_evidence_recorded",
                detail=f"twin_id={twin.twin_id.value}",
                evidence_id=record.evidence_id.value,
            )
        )
        return True

    def _attach_to_episodes(
        self,
        request: EvidenceUpdateRequest,
        record: EvidenceRecord,
        audit: list[EvidenceUpdateAuditEntry],
    ) -> None:
        for episode_key in request.learning_episode_ids:
            episode = self._uow.episodes.get(LearningEpisodeId(episode_key))
            if episode is None:
                raise NotFoundError("LearningEpisode", episode_key)
            try:
                episode.attach_evidence(record.evidence_id)
            except EducationalDomainError as exc:
                raise ConflictError(str(exc)) from exc
            self._uow.episodes.save(episode)
            audit.append(
                EvidenceUpdateAuditEntry(
                    kind="episode_evidence_attached",
                    detail=f"episode_id={episode_key}",
                    evidence_id=record.evidence_id.value,
                )
            )
