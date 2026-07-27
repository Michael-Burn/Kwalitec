"""AP-001 Assessment & Learning Feedback Pipeline tests."""

from __future__ import annotations

from datetime import date, datetime
from unittest.mock import MagicMock

import pytest

from app.application.adaptive_mission.adaptive_mission_service import (
    AdaptiveMissionService,
)
from app.application.assessment_pipeline.assessment_pipeline_service import (
    AssessmentPipelineService,
)
from app.application.assessment_pipeline.persistence import (
    AssessmentPipelinePersistenceService,
)
from app.application.student_digital_twin.observation_service import ObservationService
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_digital_twin.student_reasoning_service import (
    StudentReasoningService,
)
from app.domain.assessment_pipeline.assessment_event import (
    AssessmentEvent,
    AssessmentEventType,
)
from app.domain.assessment_pipeline.assessment_pipeline import (
    build_learning_feedback,
    build_observation_from_event,
    performance_label_for_event,
    prepare_pipeline_artifacts,
)
from app.domain.assessment_pipeline.feedback_validator import (
    validate_assessment_event,
)
from app.domain.curriculum_retrieval.intent import QueryIntent
from app.domain.curriculum_retrieval.profile import RetrievalProfile
from app.domain.curriculum_retrieval.ranking import RankingBreakdown
from app.domain.curriculum_retrieval.result import (
    EvidenceItem,
    RankedEvidence,
    RetrievalResult,
)
from app.domain.student_digital_twin.observation import ObservationKind
from app.models.assessment_pipeline import (
    ApAssessmentEvent,
    ApAssessmentResult,
    ApLearningFeedback,
    ApMissionAssessmentLink,
)
from tests.presentation.curriculum_studio.helpers import login_founder


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


def _make_retrieval_stub(
    *,
    concept_id: str = "concept-bayes",
    prerequisites: tuple[str, ...] = ("concept-conditional",),
) -> MagicMock:
    stub = MagicMock()
    evidence = (
        EvidenceItem(
            evidence_id="ev-ap-1",
            role="definition",
            excerpt="Bayes theorem definition",
            entity_id=concept_id,
        ),
    )
    ranked = RankedEvidence(
        entity_id=concept_id,
        kind="concept",
        title="Bayes Theorem",
        body="Definition body",
        document_id=1,
        version_label="2026",
        confidence=0.9,
        confidence_band="high",
        verified=True,
        provenance_id="prov-ap-1",
        rank_score=0.88,
        ranking=_ranking(),
        evidence=evidence,
        prerequisites=prerequisites,
        related_concepts=(),
        supporting_formulae=(),
        worked_examples=(),
        practice_questions=(),
        learning_objectives=(),
    )
    stub.retrieve.return_value = RetrievalResult(
        query_text=concept_id,
        intent=QueryIntent.DEFINITION,
        profile=RetrievalProfile.MISSION_ENGINE,
        results=(ranked,),
        concept_ids=(concept_id,),
        learning_objective_ids=(),
        definition_ids=(),
        formula_ids=(),
        example_ids=(),
        practice_question_ids=(),
        prerequisite_ids=prerequisites,
        related_concept_ids=(),
        retrieval_log_id="rl-ap-1",
    )
    return stub


def _twin(ctx, *, student_id: str = "s-ap-1"):
    return StudentDigitalTwinService().create(
        student_id=student_id,
        workspace_id="ws-ap",
        subject_code="CS1",
    )


def _reasoned_twin(ctx, *, student_id: str = "s-ap-reasoned"):
    stub = _make_retrieval_stub()
    twin = _twin(ctx, student_id=student_id)
    twin, _obs = ObservationService().record(
        twin,
        kind=ObservationKind.QUESTION_ANSWERED,
        curriculum_entity_id="concept-bayes",
        metadata={"correct": False, "concept_title": "Bayes Theorem"},
        persist=True,
    )
    updated = StudentReasoningService(retrieval=stub).reason(
        twin, triggered_by="ap-setup", persist=True
    )
    return updated, stub


def _pipeline(stub: MagicMock | None = None) -> AssessmentPipelineService:
    retrieval = stub or _make_retrieval_stub()
    return AssessmentPipelineService(
        reasoning=StudentReasoningService(retrieval=retrieval),
    )


def test_assessment_event_creation_is_immutable(ctx):
    twin = _twin(ctx, student_id="s-ap-evt")
    event = AssessmentEvent.create(
        event_id="aev-1",
        event_type=AssessmentEventType.QUESTION_ATTEMPT,
        twin_id=twin.twin_id,
        student_id=twin.student.student_id,
        occurred_at=datetime(2026, 7, 27, 10, 0, 0),
        curriculum_entity_id="concept-bayes",
        concept_ids=("concept-bayes",),
        correct=True,
        score=1.0,
    )
    assert event.event_type == AssessmentEventType.QUESTION_ATTEMPT
    with pytest.raises(Exception):
        event.correct = False  # type: ignore[misc]


def test_observation_generation_from_event(ctx):
    twin = _twin(ctx, student_id="s-ap-obs")
    event = AssessmentEvent.create(
        event_id="aev-obs",
        event_type=AssessmentEventType.QUIZ_SUBMISSION,
        twin_id=twin.twin_id,
        student_id=twin.student.student_id,
        curriculum_entity_id="concept-bayes",
        concept_ids=("concept-bayes",),
        score=0.8,
    )
    observation = build_observation_from_event(event, observation_id="obs-ap-1")
    assert observation.kind == ObservationKind.QUIZ_COMPLETED
    assert observation.provenance.startswith("assessment_pipeline:")
    assert observation.metadata["assessment_event_id"] == "aev-obs"
    assert observation.is_positive_outcome is True


def test_validation_rejects_mission_completion_without_mission_id(ctx):
    twin = _twin(ctx, student_id="s-ap-val")
    event = AssessmentEvent.create(
        event_id="aev-bad",
        event_type=AssessmentEventType.MISSION_COMPLETION,
        twin_id=twin.twin_id,
        student_id=twin.student.student_id,
        mission_id="",
    )
    result = validate_assessment_event(event)
    assert result.passed is False
    assert any(i.code == "missing_mission_id" for i in result.errors)


def test_feedback_generation_is_deterministic(ctx):
    twin = _twin(ctx, student_id="s-ap-fb")
    event = AssessmentEvent.create(
        event_id="aev-fb",
        event_type=AssessmentEventType.QUESTION_ATTEMPT,
        twin_id=twin.twin_id,
        student_id=twin.student.student_id,
        curriculum_entity_id="concept-bayes",
        concept_ids=("concept-bayes",),
        correct=False,
        occurred_at=datetime(2026, 7, 27, 11, 0, 0),
    )
    _val, obs, result, feedback = prepare_pipeline_artifacts(
        event,
        observation_id="obs-fb",
        result_id="asr-fb",
        feedback_id="lfb-fb",
    )
    assert obs is not None and result is not None and feedback is not None
    again = build_learning_feedback(event, result, feedback_id="lfb-fb")
    assert feedback.performance == again.performance == "incorrect"
    assert feedback.suggested_next_action == again.suggested_next_action
    assert "recovery" in feedback.suggested_next_action.lower()
    assert performance_label_for_event(event) == "incorrect"


def test_pipeline_updates_twin_via_reasoning(ctx):
    twin = _twin(ctx, student_id="s-ap-pipe")
    stub = _make_retrieval_stub()
    before = len(twin.observations)
    run = _pipeline(stub).ingest(
        twin_id=twin.twin_id,
        event_type=AssessmentEventType.QUESTION_ATTEMPT,
        curriculum_entity_id="concept-bayes",
        concept_ids=["concept-bayes"],
        correct=False,
        persist=True,
        reason=True,
    )
    assert run.ok is True
    assert run.observation is not None
    assert run.result is not None
    assert run.feedback is not None
    assert run.twin is not None
    assert len(run.twin.observations) == before + 1
    assert run.twin.reasoning_history
    assert ApAssessmentEvent.query.filter_by(event_id=run.event.event_id).count() == 1
    assert (
        ApAssessmentResult.query.filter_by(result_id=run.result.result_id).count() == 1
    )
    assert (
        ApLearningFeedback.query.filter_by(feedback_id=run.feedback.feedback_id).count()
        == 1
    )


def test_mission_completion_produces_assessment_evidence(ctx):
    twin, stub = _reasoned_twin(ctx, student_id="s-ap-mission")
    mission_service = AdaptiveMissionService(retrieval=stub)
    mission = mission_service.generate_from_twin(
        twin,
        mission_date=date(2026, 7, 27),
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
        persist=True,
    )
    completed = mission_service.complete(
        mission.mission_id,
        reflection_response="Understood Bayes better",
        outcome_achieved=True,
        emit_assessment=True,
        refresh_mission=False,
    )
    assert completed.status.value == "completed"
    events = AssessmentPipelinePersistenceService().list_events_for_twin(twin.twin_id)
    assert any(
        e.event_type == AssessmentEventType.MISSION_COMPLETION
        and e.mission_id == mission.mission_id
        for e in events
    )
    links = AssessmentPipelinePersistenceService().list_mission_links(
        mission_id=mission.mission_id
    )
    assert links
    assert ApMissionAssessmentLink.query.filter_by(
        mission_id=mission.mission_id
    ).count() >= 1


def test_mission_step_progress_emits_assessment(ctx):
    twin, stub = _reasoned_twin(ctx, student_id="s-ap-step")
    mission_service = AdaptiveMissionService(retrieval=stub)
    mission = mission_service.generate_from_twin(
        twin,
        mission_date=date(2026, 7, 27),
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
        persist=True,
    )
    mission_service.update_progress(
        mission.mission_id,
        steps_completed=1,
        last_step_id=mission.steps[0].step_id,
        emit_assessment=True,
    )
    events = AssessmentPipelinePersistenceService().list_events_for_twin(twin.twin_id)
    assert any(
        e.event_type == AssessmentEventType.MISSION_STEP_COMPLETION
        and e.step_id == mission.steps[0].step_id
        for e in events
    )


def test_performance_summary_from_evidence(ctx):
    twin = _twin(ctx, student_id="s-ap-sum")
    stub = _make_retrieval_stub()
    pipe = _pipeline(stub)
    pipe.ingest(
        twin_id=twin.twin_id,
        event_type=AssessmentEventType.QUESTION_ATTEMPT,
        curriculum_entity_id="concept-bayes",
        concept_ids=["concept-bayes"],
        correct=True,
        score=1.0,
        reason=False,
    )
    pipe.ingest(
        twin_id=twin.twin_id,
        event_type=AssessmentEventType.QUESTION_ATTEMPT,
        curriculum_entity_id="concept-bayes",
        concept_ids=["concept-bayes"],
        correct=False,
        score=0.0,
        reason=False,
    )
    summary = pipe.summarise_performance(twin.twin_id, persist=True)
    assert summary.event_count == 2
    assert summary.correct_count == 1
    assert summary.incorrect_count == 1
    assert summary.accuracy == 0.5


def test_no_duplicated_twin_state_in_assessment_tables(ctx):
    twin = _twin(ctx, student_id="s-ap-nodup")
    stub = _make_retrieval_stub()
    run = _pipeline(stub).ingest(
        twin_id=twin.twin_id,
        event_type=AssessmentEventType.STUDY_SESSION_COMPLETION,
        curriculum_entity_id="concept-bayes",
        concept_ids=["concept-bayes"],
        reason=True,
    )
    assert run.ok
    # Assessment tables store evidence metadata only — Twin inferences remain on Twin.
    assert run.twin is not None
    assert run.twin.mastery or run.twin.learning_state
    row = ApAssessmentResult.query.filter_by(event_id=run.event.event_id).first()
    assert row is not None
    assert "mastery" not in row.metadata_json.lower()


def test_founder_assessment_endpoints(client, app, ctx):
    twin = _twin(ctx, student_id="s-ap-http")
    stub = _make_retrieval_stub()
    _pipeline(stub).ingest(
        twin_id=twin.twin_id,
        event_type=AssessmentEventType.FORMULA_RECALL,
        curriculum_entity_id="concept-bayes",
        concept_ids=["concept-bayes"],
        correct=True,
        reason=True,
    )
    login_founder(client, app)

    r = client.get(f"/founder/assessment/events?twin_id={twin.twin_id}")
    assert r.status_code == 200
    assert r.get_json()["ok"] is True
    assert r.get_json()["events"]

    r = client.get(f"/founder/assessment/results?twin_id={twin.twin_id}")
    assert r.status_code == 200
    assert r.get_json()["ok"] is True

    r = client.get(f"/founder/assessment/feedback?twin_id={twin.twin_id}")
    assert r.status_code == 200
    assert r.get_json()["ok"] is True

    r = client.get("/founder/assessment/pipeline")
    assert r.status_code == 200
    assert "StudentReasoningService" in r.get_json()["pipeline"]

    r = client.post(
        "/founder/assessment/pipeline",
        json={
            "twin_id": twin.twin_id,
            "event_type": "revision_session",
            "concept_ids": ["concept-bayes"],
            "curriculum_entity_id": "concept-bayes",
            "reason": True,
        },
    )
    assert r.status_code == 200
    assert r.get_json()["ok"] is True

    r = client.get(f"/founder/assessment/diagnostics?twin_id={twin.twin_id}")
    assert r.status_code == 200
    body = r.get_json()
    assert body["ok"] is True
    assert body["duplicates_twin_state"] is False
    assert body["delegates_reasoning_to"] == "StudentReasoningService"


def test_regression_ame_and_sdt_still_load(ctx):
    """Smoke that AME + SDT packages remain operable alongside AP-001."""
    twin, stub = _reasoned_twin(ctx, student_id="s-ap-reg")
    assert twin.recommendations or twin.knowledge_gaps
    mission = AdaptiveMissionService(retrieval=stub).generate_from_twin(
        twin,
        mission_date=date(2026, 7, 27),
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
        persist=True,
    )
    assert mission.mission_id
    diag = AssessmentPipelineService(
        reasoning=StudentReasoningService(retrieval=stub)
    ).diagnostics_for_twin(twin.twin_id)
    assert diag["ok"] is True
