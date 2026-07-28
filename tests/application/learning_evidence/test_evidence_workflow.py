"""Application tests for Learning Evidence Engine (EI-005)."""

from __future__ import annotations

import ast
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from app.application.curriculum_extraction.dto import ExtractionRequest
from app.application.curriculum_extraction.extraction_engine import (
    CurriculumExtractionEngine,
)
from app.application.curriculum_publishing.editorial_operations_service import (
    EditorialOperationsService,
)
from app.application.curriculum_publishing.publication_engine import (
    PublicationEngine,
)
from app.application.learning_evidence.exceptions import (
    EvidenceGateError,
    EvidenceNotFoundError,
)
from app.application.learning_evidence.query_service import EvidenceQueryService
from app.application.learning_evidence.recording_service import (
    EvidenceRecordingService,
)
from app.application.student_curriculum_binding.binding_service import (
    StudentCurriculumBindingService,
)
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.domain.learning_evidence.evidence_type import EvidenceSource, EvidenceType
from app.models.curriculum_knowledge_graph import (
    CkgGraphEdition,
    CkgLearningObjective,
)
from app.models.learning_evidence import LeeEvidenceEvent
from app.models.student_curriculum_binding import SciCurriculumNodeState
from tests.application.curriculum_extraction.helpers import (
    cmp_document,
    syllabus_document,
)
from tests.conftest import _make_user

FOUNDER = "founder@kwalitec.test"


def _publish_and_bind(*, job_id: str = "job-ei005-1") -> tuple[int, str, str]:
    user = _make_user()
    engine = CurriculumExtractionEngine()
    result = engine.extract(
        ExtractionRequest(
            job_id=job_id,
            subject_code="CS1",
            edition_label="2026",
            subject_title="Actuarial Statistics",
            cmp_document=cmp_document(),
            syllabus_document=syllabus_document(),
            persist=True,
        )
    )
    assert result.persisted is True
    assert result.edition_id is not None
    edition_id = result.edition_id

    EditorialOperationsService().approve_edition(edition_id, actor=FOUNDER)
    PublicationEngine().publish(
        edition_id,
        publisher=FOUNDER,
        rationale="EI-005 test published edition",
    )
    edition = CkgGraphEdition.query.filter_by(edition_id=edition_id).first()
    assert edition is not None
    assert edition.publication_state == PublicationState.PUBLISHED.value

    binding = StudentCurriculumBindingService().create_instance(
        student_id=user.id,
        edition_id=edition_id,
    )
    lo = CkgLearningObjective.query.first()
    assert lo is not None
    return user.id, binding.instance.instance_id, lo.stable_id


def test_record_and_query_chronological_history(app, db, ctx) -> None:
    student_id, instance_id, node_id = _publish_and_bind()
    recorder = EvidenceRecordingService()
    query = EvidenceQueryService()

    t0 = datetime(2026, 7, 1, 10, 0, 0)
    t1 = datetime(2026, 7, 2, 11, 0, 0)
    t2 = datetime(2026, 7, 3, 12, 0, 0)

    first = recorder.record_evidence(
        instance_id=instance_id,
        node_stable_id=node_id,
        evidence_type=EvidenceType.READING_COMPLETED,
        source=EvidenceSource.STUDENT_RUNTIME,
        occurred_at=t1,
        metadata={"duration_minutes": 20},
    )
    recorder.record_evidence(
        instance_id=instance_id,
        node_stable_id=node_id,
        evidence_type=EvidenceType.PRACTICE_ATTEMPT,
        source=EvidenceSource.SESSION_RUNTIME,
        occurred_at=t0,
        metadata={"correct": False, "item_id": "q-1"},
    )
    recorder.record_evidence(
        instance_id=instance_id,
        node_stable_id=node_id,
        evidence_type=EvidenceType.STUDY_SESSION,
        source=EvidenceSource.SESSION_RUNTIME,
        occurred_at=t2,
        metadata={"duration_minutes": 45, "session_id": "sess-1"},
    )

    history = query.get_chronological_history(instance_id)
    assert len(history.events) == 3
    assert [e.evidence_type for e in history.events] == [
        "practice_attempt",
        "reading_completed",
        "study_session",
    ]
    assert history.events[0].occurred_at == t0

    by_node = query.get_by_node(instance_id, node_id)
    assert len(by_node.events) == 3

    by_type = query.filter_by_type(instance_id, EvidenceType.PRACTICE_ATTEMPT)
    assert len(by_type.events) == 1
    assert by_type.events[0].metadata["item_id"] == "q-1"

    by_student = query.get_by_student(student_id)
    assert len(by_student.events) == 3

    summary = query.summarise_counts(instance_id, node_stable_id=node_id)
    assert summary.summary.total == 3
    assert summary.summary.to_dict()["by_type"]["practice_attempt"] == 1

    state = SciCurriculumNodeState.query.filter_by(
        instance_id=instance_id,
        node_stable_id=node_id,
    ).first()
    assert state is not None
    assert state.evidence_count == 3
    assert state.last_interaction_at == t2
    # Mastery / confidence untouched (no inference).
    assert state.mastery == 0.0
    assert state.confidence == 0.0

    assert LeeEvidenceEvent.query.count() == 3
    assert first.event.evidence_id.startswith("lee-")


def test_rejects_inactive_instance_and_unknown_node(app, db, ctx) -> None:
    _student_id, instance_id, node_id = _publish_and_bind(job_id="job-ei005-gate")
    from app.models.student_curriculum_binding import SciStudentCurriculumInstance

    instance = SciStudentCurriculumInstance.query.filter_by(
        instance_id=instance_id
    ).first()
    assert instance is not None
    instance.is_active = False
    db.session.commit()

    recorder = EvidenceRecordingService()
    with pytest.raises(EvidenceGateError):
        recorder.record_evidence(
            instance_id=instance_id,
            node_stable_id=node_id,
            evidence_type=EvidenceType.STUDY_SESSION,
            source=EvidenceSource.MANUAL_ENTRY,
            occurred_at=datetime(2026, 7, 28, 12, 0, 0),
        )

    # Reactivate to test foreign node.
    instance.is_active = True
    db.session.commit()
    with pytest.raises(EvidenceGateError):
        recorder.record_evidence(
            instance_id=instance_id,
            node_stable_id="CS1.NOT.A.REAL.NODE",
            evidence_type=EvidenceType.READING_COMPLETED,
            source=EvidenceSource.STUDENT_RUNTIME,
            occurred_at=datetime(2026, 7, 28, 12, 0, 0),
        )


def test_correction_is_append_only(app, db, ctx) -> None:
    _student_id, instance_id, node_id = _publish_and_bind(job_id="job-ei005-corr")
    recorder = EvidenceRecordingService()
    original = recorder.record_evidence(
        instance_id=instance_id,
        node_stable_id=node_id,
        evidence_type=EvidenceType.ASSESSMENT_RESULT,
        source=EvidenceSource.SESSION_RUNTIME,
        occurred_at=datetime(2026, 7, 10, 9, 0, 0),
        metadata={"score": 40, "passed": False},
    )
    correction = recorder.record_evidence(
        instance_id=instance_id,
        node_stable_id=node_id,
        evidence_type=EvidenceType.MANUAL_FOUNDER_OVERRIDE,
        source=EvidenceSource.FOUNDER_OVERRIDE,
        occurred_at=datetime(2026, 7, 11, 9, 0, 0),
        metadata={"reason": "Score was entered against wrong LO"},
        corrects_evidence_id=original.event.evidence_id,
    )
    assert correction.event.corrects_evidence_id == original.event.evidence_id
    assert LeeEvidenceEvent.query.count() == 2
    # Original row unchanged.
    prior = LeeEvidenceEvent.query.filter_by(
        evidence_id=original.event.evidence_id
    ).first()
    assert prior is not None
    assert prior.evidence_type == "assessment_result"

    with pytest.raises(EvidenceNotFoundError):
        recorder.record_evidence(
            instance_id=instance_id,
            node_stable_id=node_id,
            evidence_type=EvidenceType.MANUAL_FOUNDER_OVERRIDE,
            source=EvidenceSource.FOUNDER_OVERRIDE,
            occurred_at=datetime(2026, 7, 12, 9, 0, 0),
            metadata={"reason": "missing target"},
            corrects_evidence_id="lee-does-not-exist",
        )


def test_rejects_future_timestamp(app, db, ctx) -> None:
    _student_id, instance_id, node_id = _publish_and_bind(job_id="job-ei005-future")
    with pytest.raises(EvidenceGateError):
        EvidenceRecordingService().record_evidence(
            instance_id=instance_id,
            node_stable_id=node_id,
            evidence_type=EvidenceType.REVISION_SESSION,
            source=EvidenceSource.STUDENT_RUNTIME,
            occurred_at=datetime.now(UTC).replace(tzinfo=None) + timedelta(days=5),
        )


def test_learning_evidence_package_purity() -> None:
    """Application learning evidence package must not import Twin / missions."""
    root = Path("app/application/learning_evidence")
    forbidden = (
        "app.domain.twin",
        "app.application.learning_orchestrator",
        "app.services.recommendation",
        "app.mission",
    )
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for bad in forbidden:
                        assert not alias.name.startswith(bad), path
            elif isinstance(node, ast.ImportFrom) and node.module:
                for bad in forbidden:
                    assert not node.module.startswith(bad), path
