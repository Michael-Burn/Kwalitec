"""Shared helpers for Educational Evidence Update tests (V3-007)."""

from __future__ import annotations

from datetime import UTC, datetime

from application.evidence_capture import (
    CapturedEvidence,
    CompletionStatus,
    EvidenceCaptureService,
    LearningSessionOutcome,
)
from application.evidence_update import EvidenceUpdateRequest
from domain.education.evidence import EvidenceRecord
from domain.education.foundation.ids import EvidenceId
from tests.education_os.application.fakes import (
    InMemoryEvidenceRepository,
    InMemoryUnitOfWork,
)
from tests.education_os.application.helpers import make_twin, make_uow


def fixed_captured_at() -> datetime:
    return datetime(2026, 7, 20, 14, 25, 30, tzinfo=UTC)


def make_outcome(
    *,
    student_id: str = "student-ada",
    mission_id: str = "mission-001",
    session_id: str = "session-evidence-1",
    confidence: str = "confident",
    difficulty: str = "hard",
    weak_concept: str = "Conditional probability",
    student_notes: str = "Need another worked example.",
    reflection_summary: str = "Completed guided practice",
    mission_title: str = "Select vs ultimate",
) -> LearningSessionOutcome:
    return LearningSessionOutcome(
        student_id=student_id,
        mission_id=mission_id,
        session_id=session_id,
        session_started=datetime(2026, 7, 20, 14, 0, 0, tzinfo=UTC),
        session_completed=datetime(2026, 7, 20, 14, 25, 0, tzinfo=UTC),
        actual_duration_seconds=1500,
        completion_status=CompletionStatus.COMPLETED,
        confidence=confidence,
        difficulty=difficulty,
        weak_concept=weak_concept,
        student_notes=student_notes,
        reflection_summary=reflection_summary,
        mission_title=mission_title,
    )


def make_captured(
    *,
    evidence_id: str = "evidence-session-001",
    outcome: LearningSessionOutcome | None = None,
    captured_at: datetime | None = None,
    provenance: str = "study_session_reflection",
) -> CapturedEvidence:
    return EvidenceCaptureService.from_outcome(
        outcome or make_outcome(),
        evidence_id=evidence_id,
        captured_at=captured_at or fixed_captured_at(),
        provenance=provenance,
    )


def make_request(
    captured: CapturedEvidence | None = None,
    **kwargs: object,
) -> EvidenceUpdateRequest:
    return EvidenceUpdateRequest(
        captured=captured or make_captured(),
        **kwargs,  # type: ignore[arg-type]
    )


class FailingEvidenceRepository(InMemoryEvidenceRepository):
    """Repository that fails on save for transactional failure tests."""

    def __init__(self, *, message: str = "repository save failed") -> None:
        super().__init__()
        self.message = message
        self.save_attempts = 0

    def save(self, evidence: EvidenceRecord) -> None:
        self.save_attempts += 1
        raise RuntimeError(self.message)

    def seed(self, evidence: EvidenceRecord) -> None:
        super().save(evidence)


def make_uow_with_failing_evidence() -> InMemoryUnitOfWork:
    return InMemoryUnitOfWork(evidence=FailingEvidenceRepository())


def make_uow_with_twin(
    *,
    student_id: str = "student-ada",
    twin_id: str = "twin-001",
) -> InMemoryUnitOfWork:
    uow = make_uow()
    make_twin(uow, twin_id=twin_id, student_id=student_id)
    return uow


def load_evidence(
    uow: InMemoryUnitOfWork, evidence_id: str
) -> EvidenceRecord | None:
    return uow.evidence.get(EvidenceId(evidence_id))
