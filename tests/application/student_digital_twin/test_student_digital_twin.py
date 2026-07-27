"""SDT-001 Student Digital Twin foundation tests."""

from __future__ import annotations

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from app.application.student_digital_twin.knowledge_gap_service import (
    KnowledgeGapService,
)
from app.application.student_digital_twin.observation_service import ObservationService
from app.application.student_digital_twin.persistence import TwinPersistenceService
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_digital_twin.student_reasoning_service import (
    StudentReasoningService,
)
from app.domain.curriculum_retrieval.intent import QueryIntent
from app.domain.curriculum_retrieval.profile import RetrievalProfile
from app.domain.curriculum_retrieval.query import RetrievalQuery
from app.domain.curriculum_retrieval.ranking import RankingBreakdown
from app.domain.curriculum_retrieval.result import (
    EvidenceItem,
    RankedEvidence,
    RetrievalResult,
)
from app.domain.student_digital_twin.knowledge_gap import KnowledgeGap
from app.domain.student_digital_twin.observation import ObservationKind
from app.domain.student_digital_twin.student import Student
from app.models.student_digital_twin import SdtObservation
from tests.presentation.curriculum_studio.helpers import login_founder


def _fixed_now() -> datetime:
    return datetime(2026, 7, 27, 12, 0, 0)


def _ranking() -> RankingBreakdown:
    return RankingBreakdown(
        semantic_similarity=0.5,
        graph_proximity=0.8,
        confidence=0.9,
        founder_verification=1.0,
        document_version=0.5,
        entity_freshness=0.5,
        relationship_strength=0.7,
        evidence_count=0.5,
        rank_score=0.88,
    )


def _make_retrieval_stub(*, concept_id: str = "concept-bayes") -> MagicMock:
    """Stub CurriculumRetrievalService returning evidence-backed results."""
    stub = MagicMock()
    evidence = (
        EvidenceItem(
            evidence_id="ev-1",
            role="definition",
            excerpt="Bayes theorem definition",
            entity_id=concept_id,
        ),
    )
    ranked = RankedEvidence(
        entity_id=concept_id,
        kind="concept",
        title="Bayes Theorem",
        body="definition",
        document_id=1,
        version_label="2026",
        confidence=0.9,
        confidence_band="high",
        verified=True,
        provenance_id="prov-1",
        rank_score=0.88,
        ranking=_ranking(),
        evidence=evidence,
        prerequisites=("concept-conditional",),
        related_concepts=(),
        supporting_formulae=(),
        worked_examples=(),
        practice_questions=(),
        learning_objectives=(),
        graph_distance=1,
    )
    stub.retrieve.return_value = RetrievalResult(
        query_text="Bayes",
        intent=QueryIntent.DEFINITION,
        profile=RetrievalProfile.STUDENT_DIGITAL_TWIN,
        results=(ranked,),
        concept_ids=(concept_id,),
        learning_objective_ids=(),
        definition_ids=(),
        formula_ids=(),
        example_ids=(),
        practice_question_ids=(),
        prerequisite_ids=("concept-conditional",),
        related_concept_ids=(),
        retrieval_log_id="ret-log-1",
    )
    return stub


def _seed_observations(twin):
    obs_svc = ObservationService()
    twin, _ = obs_svc.record(
        twin,
        kind=ObservationKind.QUESTION_ANSWERED,
        curriculum_entity_id="concept-bayes",
        curriculum_entity_kind="concept",
        evidence_reference="quiz-2-q1",
        provenance="test",
        metadata={"correct": False, "concept_title": "Bayes Theorem"},
        recorded_at=_fixed_now(),
        observation_id="obs-1",
        persist=True,
    )
    twin, _ = obs_svc.record(
        twin,
        kind=ObservationKind.QUESTION_ANSWERED,
        curriculum_entity_id="concept-bayes",
        curriculum_entity_kind="concept",
        evidence_reference="quiz-2-q2",
        provenance="test",
        metadata={"correct": False, "concept_title": "Bayes Theorem"},
        recorded_at=_fixed_now(),
        observation_id="obs-2",
        persist=True,
    )
    twin, _ = obs_svc.record(
        twin,
        kind=ObservationKind.QUIZ_COMPLETED,
        curriculum_entity_id="concept-bayes",
        curriculum_entity_kind="concept",
        evidence_reference="quiz-2",
        provenance="test",
        metadata={"score": 0.3, "concept_title": "Bayes Theorem"},
        recorded_at=_fixed_now(),
        observation_id="obs-3",
        persist=True,
    )
    return twin


def test_twin_creation(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="student-1",
        display_name="Ada",
        subject_code="CS1",
        workspace_id="ws-1",
        twin_id="twin-fixed-1",
        created_at=_fixed_now(),
    )
    assert twin.twin_id == "twin-fixed-1"
    assert twin.student.student_id == "student-1"
    assert twin.observation_count == 0
    assert twin.learning_state.knowledge == 0.0

    again = StudentDigitalTwinService().create(
        student_id="student-1",
        subject_code="CS1",
        workspace_id="ws-1",
    )
    assert again.twin_id == "twin-fixed-1"


def test_observation_recording_and_immutability(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-obs",
        workspace_id="ws",
        twin_id="twin-obs",
    )
    twin, obs = ObservationService().record(
        twin,
        kind=ObservationKind.CHAPTER_COMPLETED,
        curriculum_entity_id="ch-4",
        evidence_reference="chapter-4",
        observation_id="obs-imm-1",
        persist=True,
    )
    assert twin.observation_count == 1
    assert obs.kind is ObservationKind.CHAPTER_COMPLETED

    with pytest.raises(ValueError, match="already recorded"):
        twin.append_observation(obs)

    with pytest.raises(ValueError, match="immutable"):
        ObservationService().record(
            twin,
            kind=ObservationKind.CHAPTER_COMPLETED,
            observation_id="obs-imm-1",
            persist=True,
        )

    with pytest.raises(Exception):
        obs.kind = ObservationKind.FORMULA_REVIEWED  # type: ignore[misc]


def test_mastery_and_learning_state_updates(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-mast",
        workspace_id="ws",
        twin_id="twin-mast",
    )
    twin = _seed_observations(twin)
    twin = StudentReasoningService(retrieval=_make_retrieval_stub()).reason(
        twin, triggered_by="test", persist=True
    )

    mastery = twin.mastery.get("concept-bayes")
    assert mastery is not None
    assert mastery.mastery_score < 0.55
    assert mastery.evidence_count >= 2
    assert mastery.supporting_evidence

    state = twin.learning_state
    assert state.snapshot_id
    assert 0.0 <= state.knowledge <= 1.0
    assert 0.0 <= state.exam_readiness <= 1.0
    assert state.evidence_count == 3
    assert set(state.as_dict()) == {
        "knowledge",
        "confidence",
        "retention",
        "consistency",
        "momentum",
        "exam_readiness",
    }


def test_knowledge_gap_requires_retrieval_evidence(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-gap",
        workspace_id="ws-gap",
        subject_code="CS1",
        twin_id="twin-gap",
    )
    twin = _seed_observations(twin)

    empty = MagicMock()
    empty.retrieve.return_value = RetrievalResult(
        query_text="x",
        intent=QueryIntent.GENERAL,
        profile=RetrievalProfile.STUDENT_DIGITAL_TWIN,
        results=(),
        concept_ids=(),
        learning_objective_ids=(),
        definition_ids=(),
        formula_ids=(),
        example_ids=(),
        practice_question_ids=(),
        prerequisite_ids=(),
        related_concept_ids=(),
    )
    mastery = StudentReasoningService(retrieval=empty)._mastery.recompute(
        twin_id=twin.twin_id, observations=twin.observations
    )
    gaps = KnowledgeGapService(retrieval=empty).identify(
        twin_id=twin.twin_id,
        mastery=mastery,
        workspace_id="ws-gap",
    )
    assert gaps == ()

    with pytest.raises(ValueError, match="supporting evidence"):
        KnowledgeGap(
            gap_id="g1",
            twin_id=twin.twin_id,
            concept_id="concept-bayes",
            supporting_evidence=(),
        )


def test_recommendation_and_prediction_scaffolding(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-rec",
        workspace_id="ws-rec",
        twin_id="twin-rec",
    )
    twin = _seed_observations(twin)
    twin = StudentReasoningService(retrieval=_make_retrieval_stub()).reason(
        twin, triggered_by="test", persist=True
    )

    assert twin.knowledge_gaps
    assert twin.recommendations
    rec = twin.recommendations[0]
    assert rec.supporting_evidence
    assert rec.confidence > 0

    kinds = {p.kind.value for p in twin.predictions}
    assert "estimated_readiness" in kinds
    assert "likelihood_of_goal_completion" in kinds
    assert "expected_mastery_growth" in kinds
    assert all(p.algorithm_version == "sdt001.scaffold_v1" for p in twin.predictions)


def test_deterministic_reasoning(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-det",
        workspace_id="ws-det",
        twin_id="twin-det",
    )
    twin = _seed_observations(twin)
    retrieval = _make_retrieval_stub()

    a = StudentReasoningService(retrieval=retrieval).reason(
        twin, triggered_by="a", persist=False
    )
    b = StudentReasoningService(retrieval=retrieval).reason(
        twin, triggered_by="b", persist=False
    )

    assert a.mastery.get("concept-bayes").mastery_score == b.mastery.get(
        "concept-bayes"
    ).mastery_score
    assert a.learning_state.as_dict() == b.learning_state.as_dict()
    assert [g.concept_id for g in a.knowledge_gaps] == [
        g.concept_id for g in b.knowledge_gaps
    ]
    assert [r.title for r in a.recommendations] == [r.title for r in b.recommendations]
    assert [p.value for p in a.predictions] == [p.value for p in b.predictions]


def test_persistence_round_trip(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-pers",
        workspace_id="ws-pers",
        twin_id="twin-pers",
    )
    twin = _seed_observations(twin)
    twin = StudentReasoningService(retrieval=_make_retrieval_stub()).reason(
        twin, triggered_by="persist", persist=True
    )

    loaded = TwinPersistenceService().load_twin("twin-pers")
    assert loaded is not None
    assert loaded.observation_count == 3
    assert loaded.mastery.get("concept-bayes") is not None
    assert loaded.knowledge_gaps
    assert loaded.recommendations
    assert loaded.predictions
    assert loaded.reasoning_history
    assert SdtObservation.query.filter_by(twin_id="twin-pers").count() == 3


def test_curriculum_retrieval_integration_contract(ctx):
    """Gaps must call CurriculumRetrievalService with Twin profile — never bypass."""
    twin = StudentDigitalTwinService().create(
        student_id="s-cip",
        workspace_id="ws-cip",
        subject_code="CS1",
        twin_id="twin-cip",
    )
    twin = _seed_observations(twin)
    retrieval = _make_retrieval_stub()
    StudentReasoningService(retrieval=retrieval).reason(
        twin, triggered_by="cip", persist=True
    )

    assert retrieval.retrieve.called
    query: RetrievalQuery = retrieval.retrieve.call_args.args[0]
    assert isinstance(query, RetrievalQuery)
    assert query.workspace_id == "ws-cip"
    assert query.profile is RetrievalProfile.STUDENT_DIGITAL_TWIN
    assert query.seed_entity_id == "concept-bayes"


def test_founder_diagnostics_endpoints(client, app, ctx):
    login_founder(client, app)

    create = client.post(
        "/founder/twin/",
        json={
            "student_id": "diag-student",
            "workspace_id": "ws-diag",
            "subject_code": "CS1",
            "display_name": "Diag",
        },
    )
    assert create.status_code == 201
    twin_id = create.get_json()["twin"]["twin_id"]

    obs = client.post(
        f"/founder/twin/{twin_id}/observations",
        json={
            "kind": "question_answered",
            "curriculum_entity_id": "concept-bayes",
            "curriculum_entity_kind": "concept",
            "evidence_reference": "quiz-1",
            "metadata": {"correct": False, "concept_title": "Bayes Theorem"},
            "reason": False,
        },
    )
    assert obs.status_code == 201

    twin = StudentDigitalTwinService().get(twin_id)
    assert twin is not None
    StudentReasoningService(retrieval=_make_retrieval_stub()).reason(
        twin, triggered_by="diag", persist=True
    )

    detail = client.get(f"/founder/twin/{twin_id}")
    assert detail.status_code == 200
    assert detail.get_json()["twin"]["twin_id"] == twin_id

    for path in (
        "history",
        "mastery",
        "gaps",
        "recommendations",
        "predictions",
        "reasoning",
    ):
        resp = client.get(f"/founder/twin/{twin_id}/{path}")
        assert resp.status_code == 200, path
        assert resp.get_json()["ok"] is True


def test_observations_never_overwritten_on_reasoning(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-ow",
        workspace_id="ws-ow",
        twin_id="twin-ow",
    )
    twin = _seed_observations(twin)
    before = [o.observation_id for o in twin.observations]
    twin = StudentReasoningService(retrieval=_make_retrieval_stub()).reason(
        twin, triggered_by="ow", persist=True
    )
    after = [o.observation_id for o in twin.observations]
    assert before == after
    assert SdtObservation.query.filter_by(twin_id="twin-ow").count() == 3


def test_student_domain_requires_id():
    with pytest.raises(ValueError):
        Student(student_id="")
