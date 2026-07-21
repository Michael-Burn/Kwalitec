"""Shared helpers for Student Twin Initialization tests (BR-003)."""

from __future__ import annotations

from datetime import UTC, datetime

from application.onboarding.results import (
    CompletedOnboarding,
    StudentTwinInitializationRequest,
)
from application.student_initialization import StudentInitializationService
from domain.education.digital_twin import EducationalDigitalTwin
from domain.education.evidence import EvidenceRecord
from tests.education_os.application.fakes import (
    FixedClock,
    InMemoryDigitalTwinRepository,
    InMemoryEventPublisher,
    InMemoryUnitOfWork,
)
from tests.education_os.application.helpers import make_events, make_uow


def fixed_completed_at() -> datetime:
    return datetime(2026, 7, 20, 12, 0, tzinfo=UTC)


def make_declarations(
    *,
    student_id: str = "stu-1",
    onboarding_id: str = "ob-1",
    confidence_band: str = "moderate",
    core_reading: str = "partial",
    exam_paper: str = "CM1",
) -> StudentTwinInitializationRequest:
    return StudentTwinInitializationRequest(
        student_id=student_id,
        onboarding_id=onboarding_id,
        pathway="core_principles",
        exam_paper=exam_paper,
        intended_sitting_label="Apr 2027",
        prior_study="first_time",
        core_reading=core_reading,
        previous_attempts=0,
        sitting_intent="first_sit",
        weekday_minutes=45,
        weekend_minutes=90,
        preferred_session_minutes=30,
        confidence_band=confidence_band,
        confidence_notes="Need steady guidance",
        study_habit_preference="mixed",
        typical_start_time="19:00",
        diagnostic_choice="skipped",
    )


def make_completed(
    *,
    declarations: StudentTwinInitializationRequest | None = None,
    completed_at: datetime | None = None,
) -> CompletedOnboarding:
    decls = declarations or make_declarations()
    return CompletedOnboarding(
        onboarding_id=decls.onboarding_id,
        student_id=decls.student_id,
        completed_at=completed_at or fixed_completed_at(),
        twin_initialization=decls,
    )


def make_service(
    uow: InMemoryUnitOfWork | None = None,
    events: InMemoryEventPublisher | None = None,
    clock: FixedClock | None = None,
) -> StudentInitializationService:
    from application.pipeline.educational_pipeline import EducationalPipeline
    from application.student_initialization.student_initialization_service import (
        EducationalPipelineAdapter,
    )

    return StudentInitializationService(
        uow=uow or make_uow(with_concept=None),
        events=events or make_events(),
        clock=clock or FixedClock(),
        pipeline=EducationalPipelineAdapter(EducationalPipeline()),
    )


class FailingTwinRepository(InMemoryDigitalTwinRepository):
    """Repository that fails on save for transactional failure tests."""

    def __init__(self, *, message: str = "repository save failed") -> None:
        super().__init__()
        self.message = message
        self.save_attempts = 0

    def save(self, twin: EducationalDigitalTwin) -> None:
        self.save_attempts += 1
        raise RuntimeError(self.message)

    def seed(self, twin: EducationalDigitalTwin) -> None:
        super().save(twin)


class StagingUnitOfWork(InMemoryUnitOfWork):
    """In-memory UoW that only publishes staged writes on ``commit``.

    ``rollback`` discards staged Twin and evidence writes so transactional
    failure tests can assert absence of persisted aggregates.
    """

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._staged_twins: list[EducationalDigitalTwin] = []
        self._staged_evidence: list[EvidenceRecord] = []
        self._twin_repo = self._digital_twins
        self._evidence_repo = self._evidence
        self._digital_twins = _StagingTwinRepository(self)  # type: ignore[assignment]
        self._evidence = _StagingEvidenceRepository(self)  # type: ignore[assignment]

    def stage_twin(self, twin: EducationalDigitalTwin) -> None:
        self._staged_twins.append(twin)

    def stage_evidence(self, evidence: EvidenceRecord) -> None:
        self._staged_evidence.append(evidence)

    def commit(self) -> None:
        for twin in self._staged_twins:
            self._twin_repo.save(twin)
        for evidence in self._staged_evidence:
            self._evidence_repo.save(evidence)
        self._staged_twins.clear()
        self._staged_evidence.clear()
        super().commit()

    def rollback(self) -> None:
        self._staged_twins.clear()
        self._staged_evidence.clear()
        super().rollback()


class _StagingTwinRepository(InMemoryDigitalTwinRepository):
    def __init__(self, uow: StagingUnitOfWork) -> None:
        super().__init__()
        self._uow = uow

    def get(self, twin_id):  # noqa: ANN001, ANN201
        key = getattr(twin_id, "value", twin_id)
        staged = next(
            (
                t
                for t in self._uow._staged_twins  # noqa: SLF001
                if t.twin_id.value == key
            ),
            None,
        )
        if staged is not None:
            return staged
        return self._uow._twin_repo.get(twin_id)  # noqa: SLF001

    def get_by_student(self, student_id: str):
        staged = next(
            (
                t
                for t in self._uow._staged_twins  # noqa: SLF001
                if t.student_id == student_id
            ),
            None,
        )
        if staged is not None:
            return staged
        return self._uow._twin_repo.get_by_student(student_id)  # noqa: SLF001

    def save(self, twin: EducationalDigitalTwin) -> None:
        self._uow.stage_twin(twin)


class _StagingEvidenceRepository:
    def __init__(self, uow: StagingUnitOfWork) -> None:
        self._uow = uow

    def get(self, evidence_id):  # noqa: ANN001, ANN201
        from domain.education.foundation.ids import EvidenceId

        key = evidence_id if isinstance(evidence_id, EvidenceId) else EvidenceId(
            str(evidence_id)
        )
        staged = next(
            (
                e
                for e in self._uow._staged_evidence  # noqa: SLF001
                if e.evidence_id == key
            ),
            None,
        )
        if staged is not None:
            return staged
        return self._uow._evidence_repo.get(key)  # noqa: SLF001

    def list_by_student(self, student_id: str):
        committed = self._uow._evidence_repo.list_by_student(student_id)  # noqa: SLF001
        staged = [
            e
            for e in self._uow._staged_evidence  # noqa: SLF001
            if e.student_id == student_id
        ]
        by_id = {e.evidence_id.value: e for e in committed}
        for evidence in staged:
            by_id[evidence.evidence_id.value] = evidence
        return list(by_id.values())

    def save(self, evidence: EvidenceRecord) -> None:
        self._uow.stage_evidence(evidence)


def make_uow_with_failing_twins() -> InMemoryUnitOfWork:
    return InMemoryUnitOfWork(digital_twins=FailingTwinRepository())


def make_staging_uow() -> StagingUnitOfWork:
    return StagingUnitOfWork()


def load_twin(
    uow: InMemoryUnitOfWork, student_id: str
) -> EducationalDigitalTwin | None:
    return uow.digital_twins.get_by_student(student_id)


def load_evidence(
    uow: InMemoryUnitOfWork, evidence_id: str
) -> EvidenceRecord | None:
    from domain.education.foundation.ids import EvidenceId

    return uow.evidence.get(EvidenceId(evidence_id))
