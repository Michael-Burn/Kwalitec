"""Application tests for Student Curriculum Binding (EI-004)."""

from __future__ import annotations

import ast
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
from app.application.student_curriculum_binding.binding_service import (
    StudentCurriculumBindingService,
)
from app.application.student_curriculum_binding.educational_state_query_service import (
    EducationalStateQueryService,
)
from app.application.student_curriculum_binding.exceptions import BindingGateError
from app.application.student_curriculum_binding.progress_aggregation_service import (
    ProgressAggregationService,
)
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.domain.student_curriculum_binding.node_state import CompletionStatus
from app.models.curriculum_knowledge_graph import (
    CkgGraphEdition,
    CkgLearningObjective,
    CkgSubject,
)
from app.models.student_curriculum_binding import (
    SciCurriculumNodeState,
    SciStudentCurriculumInstance,
)
from tests.application.curriculum_extraction.helpers import (
    cmp_document,
    syllabus_document,
)
from tests.conftest import _make_user

FOUNDER = "founder@kwalitec.test"


def _publish_edition(*, job_id: str = "job-ei004-1") -> str:
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

    editorial = EditorialOperationsService()
    editorial.approve_edition(edition_id, actor=FOUNDER)
    PublicationEngine().publish(
        edition_id,
        publisher=FOUNDER,
        rationale="EI-004 test published edition",
    )
    edition = CkgGraphEdition.query.filter_by(edition_id=edition_id).first()
    assert edition is not None
    assert edition.publication_state == PublicationState.PUBLISHED.value
    return edition_id


def test_bind_creates_instance_and_node_states(app, db, ctx) -> None:
    user = _make_user()
    edition_id = _publish_edition()

    binding = StudentCurriculumBindingService()
    result = binding.create_instance(student_id=user.id, edition_id=edition_id)

    assert result.created is True
    assert result.instance.student_id == user.id
    assert result.instance.subject_code == "CS1"
    assert result.instance.edition_id == edition_id
    assert result.instance.is_active is True
    assert result.instance.is_completed is False
    assert result.node_states_initialised > 0

    instance = SciStudentCurriculumInstance.query.filter_by(
        instance_id=result.instance.instance_id
    ).first()
    assert instance is not None
    assert instance.enrolled_at is not None

    states = SciCurriculumNodeState.query.filter_by(
        instance_id=result.instance.instance_id
    ).all()
    assert len(states) == result.node_states_initialised
    assert CkgSubject.query.filter_by(graph_edition_id=edition_id).first()
    # Every LO in the published graph has a node state.
    lo_ids = {lo.stable_id for lo in CkgLearningObjective.query.all()}
    state_ids = {s.node_stable_id for s in states}
    assert lo_ids.issubset(state_ids)
    assert all(
        s.completion_status == CompletionStatus.NOT_STARTED.value for s in states
    )
    assert all(s.mastery == 0.0 for s in states)


def test_cannot_bind_to_draft(app, db, ctx) -> None:
    user = _make_user()
    extract = CurriculumExtractionEngine().extract(
        ExtractionRequest(
            job_id="job-ei004-draft",
            subject_code="CS1",
            edition_label="2026",
            subject_title="Actuarial Statistics",
            cmp_document=cmp_document(),
            syllabus_document=syllabus_document(),
            persist=True,
        )
    )
    assert extract.edition_id is not None

    with pytest.raises(BindingGateError):
        StudentCurriculumBindingService().create_instance(
            student_id=user.id,
            edition_id=extract.edition_id,
        )


def test_idempotent_rebind_same_edition(app, db, ctx) -> None:
    user = _make_user()
    edition_id = _publish_edition(job_id="job-ei004-idem")
    binding = StudentCurriculumBindingService()
    first = binding.create_instance(student_id=user.id, edition_id=edition_id)
    second = binding.create_instance(student_id=user.id, edition_id=edition_id)
    assert first.created is True
    assert second.created is False
    assert second.instance.instance_id == first.instance.instance_id
    assert (
        SciStudentCurriculumInstance.query.filter_by(student_id=user.id).count() == 1
    )


def test_query_state_incomplete_completed_and_aggregate(app, db, ctx) -> None:
    user = _make_user()
    edition_id = _publish_edition(job_id="job-ei004-query")
    binding = StudentCurriculumBindingService()
    result = binding.create_instance(student_id=user.id, edition_id=edition_id)
    instance_id = result.instance.instance_id

    query = EducationalStateQueryService()
    state = query.get_educational_state(instance_id)
    assert state.instance.instance_id == instance_id
    assert len(state.node_states) == result.node_states_initialised

    incomplete = query.query_incomplete_curriculum(instance_id)
    assert len(incomplete.nodes) == len(state.node_states)
    assert query.query_completed_curriculum(instance_id).nodes == ()

    # Mark one LO completed to exercise filters (direct state write — not mastery calc).
    lo = CkgLearningObjective.query.first()
    assert lo is not None
    row = SciCurriculumNodeState.query.filter_by(
        instance_id=instance_id,
        node_stable_id=lo.stable_id,
    ).first()
    assert row is not None
    row.completion_status = CompletionStatus.COMPLETED.value
    row.mastery = 0.8
    row.attempts = 3
    row.total_study_time_minutes = 25
    row.evidence_count = 2
    db.session.commit()

    completed = query.query_completed_curriculum(instance_id)
    assert len(completed.nodes) == 1
    assert completed.nodes[0].node_stable_id == lo.stable_id

    incomplete_after = query.query_incomplete_curriculum(instance_id)
    assert len(incomplete_after.nodes) == len(state.node_states) - 1

    agg = ProgressAggregationService()
    subject = agg.aggregate_for_node(instance_id, "CS1")
    assert subject.kind == "subject"
    assert subject.node_count == len(state.node_states)
    assert subject.completed_count == 1
    assert subject.total_attempts == 3
    assert subject.total_study_time_minutes == 25

    levels = agg.aggregate_all_levels(instance_id)
    kinds = {a.kind for a in levels.aggregates}
    assert {"subject", "topic", "section", "subsection"} <= kinds

    # Determinism: same inputs → same aggregates.
    again = agg.aggregate_for_node(instance_id, "CS1")
    assert again == subject


def test_binding_package_purity() -> None:
    """Application binding package must not import Twin / mission / recommendation."""
    root = Path("app/application/student_curriculum_binding")
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
