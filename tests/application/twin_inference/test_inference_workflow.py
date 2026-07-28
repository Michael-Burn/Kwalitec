"""Application tests for Twin Inference Engine (EI-006)."""

from __future__ import annotations

import ast
from datetime import datetime
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
from app.application.learning_evidence.recording_service import (
    EvidenceRecordingService,
)
from app.application.student_curriculum_binding.binding_service import (
    StudentCurriculumBindingService,
)
from app.application.twin_inference.exceptions import (
    BeliefNotFoundError,
    NodeNotFoundError,
)
from app.application.twin_inference.inference_service import BeliefInferenceService
from app.application.twin_inference.query_service import BeliefQueryService
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.domain.learning_evidence.evidence_type import EvidenceSource, EvidenceType
from app.domain.twin_inference.version import INFERENCE_VERSION
from app.models.curriculum_knowledge_graph import (
    CkgGraphEdition,
    CkgLearningObjective,
)
from app.models.learning_evidence import LeeEvidenceEvent
from app.models.student_curriculum_binding import SciCurriculumNodeState
from app.models.twin_inference import TieNodeBelief
from tests.application.curriculum_extraction.helpers import (
    cmp_document,
    syllabus_document,
)
from tests.conftest import _make_user

FOUNDER = "founder@kwalitec.test"
AS_OF = datetime(2026, 7, 28, 12, 0, 0)


def _publish_and_bind(*, job_id: str = "job-ei006-1") -> tuple[int, str, str]:
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
        rationale="EI-006 test published edition",
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


def _seed_evidence(instance_id: str, node_id: str) -> None:
    recorder = EvidenceRecordingService()
    recorder.record_evidence(
        instance_id=instance_id,
        node_stable_id=node_id,
        evidence_type=EvidenceType.READING_COMPLETED,
        source=EvidenceSource.STUDENT_RUNTIME,
        occurred_at=datetime(2026, 7, 10, 10, 0, 0),
        metadata={"duration_minutes": 25},
    )
    recorder.record_evidence(
        instance_id=instance_id,
        node_stable_id=node_id,
        evidence_type=EvidenceType.PRACTICE_ATTEMPT,
        source=EvidenceSource.SESSION_RUNTIME,
        occurred_at=datetime(2026, 7, 12, 11, 0, 0),
        metadata={"correct": True, "item_id": "q-1"},
    )
    recorder.record_evidence(
        instance_id=instance_id,
        node_stable_id=node_id,
        evidence_type=EvidenceType.ASSESSMENT_RESULT,
        source=EvidenceSource.SESSION_RUNTIME,
        occurred_at=datetime(2026, 7, 15, 9, 0, 0),
        metadata={"score": 75, "passed": True},
    )
    recorder.record_evidence(
        instance_id=instance_id,
        node_stable_id=node_id,
        evidence_type=EvidenceType.REVISION_SESSION,
        source=EvidenceSource.STUDENT_RUNTIME,
        occurred_at=datetime(2026, 7, 20, 14, 0, 0),
        metadata={"duration_minutes": 20},
    )


def test_infer_node_belief_persists_and_projects(app, db, ctx) -> None:
    _student_id, instance_id, node_id = _publish_and_bind()
    _seed_evidence(instance_id, node_id)

    service = BeliefInferenceService()
    view = service.infer_node_belief(instance_id, node_id, as_of=AS_OF)

    assert view.belief.inference_version == INFERENCE_VERSION
    assert view.belief.mastery_level > 0
    assert view.belief.supporting_evidence_ids
    assert view.explanation.contributing_rules
    assert view.explanation.inference_rationale

    row = TieNodeBelief.query.filter_by(
        instance_id=instance_id, node_stable_id=node_id
    ).first()
    assert row is not None
    assert row.rationale_summary

    state = SciCurriculumNodeState.query.filter_by(
        instance_id=instance_id, node_stable_id=node_id
    ).first()
    assert state is not None
    assert state.mastery == view.belief.mastery_level
    assert state.confidence == view.belief.confidence_score

    # Evidence untouched.
    assert LeeEvidenceEvent.query.filter_by(instance_id=instance_id).count() == 4


def test_rebuild_is_deterministic_and_full(app, db, ctx) -> None:
    _student_id, instance_id, node_id = _publish_and_bind(job_id="job-ei006-rebuild")
    _seed_evidence(instance_id, node_id)

    service = BeliefInferenceService()
    first = service.rebuild_beliefs(instance_id, as_of=AS_OF)
    assert first.belief_count > 0
    node_view = next(
        v for v in first.beliefs if v.belief.node_stable_id == node_id
    )
    mastery_1 = node_view.belief.mastery_level

    second = service.rebuild_beliefs(instance_id, as_of=AS_OF)
    node_view_2 = next(
        v for v in second.beliefs if v.belief.node_stable_id == node_id
    )
    assert node_view_2.belief.mastery_level == mastery_1
    assert node_view_2.belief.confidence_score == node_view.belief.confidence_score
    assert node_view_2.belief.learning_state == node_view.belief.learning_state
    # One belief row per SCI node after rebuild.
    assert (
        TieNodeBelief.query.filter_by(instance_id=instance_id).count()
        == first.belief_count
    )
    # Evidence still immutable.
    assert LeeEvidenceEvent.query.filter_by(instance_id=instance_id).count() == 4


def test_query_explainable_summary_and_knowledge_state(app, db, ctx) -> None:
    _student_id, instance_id, node_id = _publish_and_bind(job_id="job-ei006-query")
    _seed_evidence(instance_id, node_id)
    BeliefInferenceService().rebuild_beliefs(instance_id, as_of=AS_OF)

    query = BeliefQueryService()
    summary = query.get_explainable_summary(instance_id, node_id)
    assert summary["node_stable_id"] == node_id
    assert summary["supporting_evidence_ids"]
    assert summary["contributing_rule_ids"]
    assert summary["confidence_calculation"]["formula"]
    assert summary["inference_version"] == INFERENCE_VERSION

    ks = query.get_knowledge_state(instance_id)
    assert ks.state.instance_id == instance_id
    assert ks.state.node_belief_count > 0
    assert ks.state.rationale_summary

    with pytest.raises(BeliefNotFoundError):
        query.get_node_belief(instance_id, "CS1.NOT.A.NODE")


def test_infer_rejects_unknown_node(app, db, ctx) -> None:
    _student_id, instance_id, _node_id = _publish_and_bind(job_id="job-ei006-gate")
    with pytest.raises(NodeNotFoundError):
        BeliefInferenceService().infer_node_belief(
            instance_id, "CS1.NOT.A.REAL.NODE", as_of=AS_OF
        )


def test_subject_knowledge_state_service(app, db, ctx) -> None:
    _student_id, instance_id, node_id = _publish_and_bind(job_id="job-ei006-ks")
    _seed_evidence(instance_id, node_id)
    view = BeliefInferenceService().infer_subject_knowledge_state(
        instance_id, as_of=AS_OF
    )
    assert view.state.subject_code == "CS1"
    assert view.state.node_belief_count > 0
    assert view.node_summaries


def test_twin_inference_packages_do_not_import_missions_or_recommendations() -> None:
    roots = (
        Path("app/domain/twin_inference"),
        Path("app/application/twin_inference"),
    )
    forbidden = (
        "app.application.learning_orchestrator",
        "app.services.recommendation",
        "app.mission",
        "app.domain.adaptive_mission",
    )
    for root in roots:
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
