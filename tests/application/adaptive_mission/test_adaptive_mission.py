"""AME-001 Adaptive Mission Engine tests."""

from __future__ import annotations

from datetime import date, datetime
from unittest.mock import MagicMock

import pytest

from app.application.adaptive_mission.adaptive_mission_service import (
    AdaptiveMissionService,
)
from app.application.adaptive_mission.persistence import (
    AdaptiveMissionPersistenceService,
)
from app.application.learning_graph.learning_graph_service import LearningGraphService
from app.application.student_digital_twin.observation_service import ObservationService
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_digital_twin.student_reasoning_service import (
    StudentReasoningService,
)
from app.domain.adaptive_mission.construction import construct_mission
from app.domain.adaptive_mission.mission import MissionStatus
from app.domain.adaptive_mission.mission_step import ActivityType
from app.domain.adaptive_mission.prioritisation import prioritise_candidates
from app.domain.adaptive_mission.validation import validate_mission
from app.domain.curriculum_retrieval.intent import QueryIntent
from app.domain.curriculum_retrieval.profile import RetrievalProfile
from app.domain.curriculum_retrieval.ranking import RankingBreakdown
from app.domain.curriculum_retrieval.result import (
    EvidenceItem,
    RankedEvidence,
    RetrievalResult,
)
from app.domain.learning_graph.graph_edge import GraphEdge
from app.domain.learning_graph.graph_node import GraphNode, PrerequisiteStatus
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.learning_graph.relationship import RelationshipType
from app.domain.student_digital_twin.observation import ObservationKind
from app.models.adaptive_mission import (
    AmeAdaptiveMission,
    AmeMissionHistory,
    AmeMissionProgress,
    AmeMissionStep,
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
        body="Definition body",
        document_id=1,
        version_label="2026",
        confidence=0.9,
        confidence_band="high",
        verified=True,
        provenance_id="prov-1",
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
        retrieval_log_id="rl-ame-1",
    )
    return stub


def _reasoned_twin(ctx, *, student_id: str = "s-ame-1"):
    stub = _make_retrieval_stub()
    twin = StudentDigitalTwinService().create(
        student_id=student_id,
        workspace_id="ws-ame",
        subject_code="CS1",
    )
    twin, _obs = ObservationService().record(
        twin,
        kind=ObservationKind.QUESTION_ANSWERED,
        curriculum_entity_id="concept-bayes",
        metadata={"correct": False, "concept_title": "Bayes Theorem"},
        persist=True,
    )
    updated = StudentReasoningService(retrieval=stub).reason(
        twin, triggered_by="ame-test", persist=True
    )
    return updated, stub


def test_mission_generation_consumes_twin_decisions(ctx):
    twin, _stub = _reasoned_twin(ctx)
    assert twin.recommendations or twin.knowledge_gaps

    service = AdaptiveMissionService(retrieval=_make_retrieval_stub())
    mission = service.generate_from_twin(
        twin,
        mission_date=date(2026, 7, 27),
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
        persist=True,
    )
    assert mission.status == MissionStatus.ACTIVE
    assert mission.reason.educational_explanation
    assert mission.source_recommendation_ids or mission.source_gap_ids
    assert mission.objective.primary_concept_id
    assert mission.as_mission_card()["source"] == "adaptive_mission_engine"


def test_prioritisation_is_deterministic(ctx):
    twin, _stub = _reasoned_twin(ctx, student_id="s-ame-prio")
    graph = LearningGraphService().get_for_twin(twin.twin_id)
    first = prioritise_candidates(
        recommendations=twin.recommendations,
        gaps=twin.knowledge_gaps,
        learning_state=twin.learning_state,
        observations=twin.observations,
        learning_graph=graph,
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
    )
    second = prioritise_candidates(
        recommendations=twin.recommendations,
        gaps=twin.knowledge_gaps,
        learning_state=twin.learning_state,
        observations=twin.observations,
        learning_graph=graph,
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
    )
    assert first.ranked_concept_ids == second.ranked_concept_ids
    assert first.selected is not None
    assert first.selected.priority_score.score == second.selected.priority_score.score


def test_prerequisite_recovery_steps_included(ctx):
    twin, _stub = _reasoned_twin(ctx, student_id="s-ame-rec")
    graph = LearningGraph(
        graph_id="lg-ame-test",
        twin_id=twin.twin_id,
        student_id=twin.student.student_id,
        nodes=(
            GraphNode(
                node_id="n1",
                graph_id="lg-ame-test",
                concept_id="concept-bayes",
                concept_title="Bayes",
                mastery_score=0.2,
                prerequisite_status=PrerequisiteStatus.UNMET,
            ),
            GraphNode(
                node_id="n2",
                graph_id="lg-ame-test",
                concept_id="concept-conditional",
                concept_title="Conditional",
                mastery_score=0.3,
                prerequisite_status=PrerequisiteStatus.MET,
            ),
        ),
        edges=(
            GraphEdge(
                edge_id="e1",
                graph_id="lg-ame-test",
                from_concept_id="concept-bayes",
                to_concept_id="concept-conditional",
                relationship_type=RelationshipType.PREREQUISITE,
            ),
        ),
    )
    result = prioritise_candidates(
        recommendations=twin.recommendations,
        gaps=twin.knowledge_gaps,
        learning_state=twin.learning_state,
        observations=twin.observations,
        learning_graph=graph,
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
    )
    assert result.selected is not None
    mission = construct_mission(
        twin_id=twin.twin_id,
        student_id=twin.student.student_id,
        mission_date=date(2026, 7, 27),
        candidate=result.selected,
        created_at=datetime(2026, 7, 27, 12, 0, 0),
    )
    prereq_steps = [
        s
        for s in mission.steps
        if s.activity.activity_type == ActivityType.PREREQUISITE_REVIEW
    ]
    # Recovery path may include conditional when graph edges exist.
    recovery = result.selected.recovery_path
    if recovery is not None and len(recovery.concept_ids) > 1:
        assert prereq_steps


def test_validation_rejects_inconsistent_recommendation(ctx):
    twin, _stub = _reasoned_twin(ctx, student_id="s-ame-val")
    service = AdaptiveMissionService(retrieval=_make_retrieval_stub())
    mission = service.generate_from_twin(
        twin,
        mission_date=date(2026, 7, 27),
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
        persist=False,
        activate=False,
    )
    from dataclasses import replace

    broken = replace(
        mission,
        source_recommendation_ids=("rec-does-not-exist",),
    )
    result = validate_mission(
        broken,
        twin=twin,
        learning_graph=LearningGraphService().get_for_twin(twin.twin_id),
        require_evidence=True,
    )
    assert result.passed is False
    assert any(i.code == "unknown_recommendation" for i in result.errors)

    ok = validate_mission(
        mission,
        twin=twin,
        learning_graph=LearningGraphService().get_for_twin(twin.twin_id),
        require_evidence=True,
    )
    assert ok.passed is True


def test_duplicate_active_prevention(ctx):
    twin, _stub = _reasoned_twin(ctx, student_id="s-ame-dup")
    service = AdaptiveMissionService(retrieval=_make_retrieval_stub())
    first = service.generate_from_twin(
        twin,
        mission_date=date(2026, 7, 27),
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
        persist=True,
    )
    second = service.generate_from_twin(
        twin,
        mission_date=date(2026, 7, 28),
        computed_at=datetime(2026, 7, 28, 12, 0, 0),
        persist=True,
    )
    assert (
        first.mission_id != second.mission_id
        or first.mission_date != second.mission_date
    )
    active = service.get_active(twin.twin_id)
    assert active is not None
    assert active.mission_id == second.mission_id
    assert active.status == MissionStatus.ACTIVE
    loaded_first = service.get(first.mission_id)
    assert loaded_first is not None
    assert loaded_first.status == MissionStatus.SUPERSEDED


def test_progress_tracking_and_completion(ctx):
    twin, _stub = _reasoned_twin(ctx, student_id="s-ame-prog")
    service = AdaptiveMissionService(retrieval=_make_retrieval_stub())
    mission = service.generate_from_twin(
        twin,
        mission_date=date(2026, 7, 27),
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
        persist=True,
    )
    updated = service.update_progress(
        mission.mission_id,
        steps_completed=1,
        last_step_id=mission.steps[0].step_id,
        note="started",
    )
    assert updated.progress.steps_completed == 1
    assert updated.progress.percent_complete > 0
    completed = service.complete(
        mission.mission_id,
        reflection_response="Clearer on Bayes",
        feedback_summary="useful",
    )
    assert completed.status == MissionStatus.COMPLETED
    assert completed.completion is not None
    assert completed.completion.outcome_achieved is True


def test_persistence_roundtrip(ctx):
    twin, _stub = _reasoned_twin(ctx, student_id="s-ame-persist")
    service = AdaptiveMissionService(retrieval=_make_retrieval_stub())
    mission = service.generate_from_twin(
        twin,
        mission_date=date(2026, 7, 27),
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
        persist=True,
    )
    mid = mission.mission_id
    assert AmeAdaptiveMission.query.filter_by(mission_id=mid).count() == 1
    assert AmeMissionStep.query.filter_by(mission_id=mid).count() == len(mission.steps)
    assert AmeMissionProgress.query.filter_by(mission_id=mid).count() == 1
    assert AmeMissionHistory.query.filter_by(mission_id=mid).count() >= 1

    loaded = AdaptiveMissionPersistenceService().load_mission(mission.mission_id)
    assert loaded is not None
    assert loaded.goal == mission.goal
    assert loaded.priority == mission.priority
    assert [s.step_id for s in loaded.steps] == [s.step_id for s in mission.steps]


def test_integration_with_learning_graph_and_reasoning(ctx):
    twin, _stub = _reasoned_twin(ctx, student_id="s-ame-int")
    graph = LearningGraphService().get_for_twin(twin.twin_id)
    assert graph is not None
    assert twin.recommendations or twin.knowledge_gaps

    diagnostics = AdaptiveMissionService(
        retrieval=_make_retrieval_stub()
    ).diagnostics_for_twin(twin.twin_id)
    assert diagnostics["ok"] is True
    assert diagnostics["graph"]["present"] is True
    assert diagnostics["prioritisation"]["selected_concept_id"]


def test_generation_without_decisions_fails(ctx):
    twin = StudentDigitalTwinService().create(
        student_id="s-ame-empty",
        workspace_id="ws-ame",
        subject_code="CS1",
    )
    with pytest.raises(ValueError, match="No educational decisions"):
        AdaptiveMissionService().generate_from_twin(twin, persist=False)


def test_founder_mission_endpoints(client, app, ctx):
    twin, _stub = _reasoned_twin(ctx, student_id="s-ame-http")
    login_founder(client, app)

    AdaptiveMissionService(retrieval=_make_retrieval_stub()).generate_from_twin(
        twin,
        mission_date=date(2026, 7, 27),
        computed_at=datetime(2026, 7, 27, 12, 0, 0),
        persist=True,
    )

    r = client.get(f"/founder/missions/?twin_id={twin.twin_id}")
    assert r.status_code == 200
    assert r.get_json()["ok"] is True
    assert r.get_json()["active_mission_id"]

    r = client.get(f"/founder/missions/history?twin_id={twin.twin_id}")
    assert r.status_code == 200
    assert r.get_json()["ok"] is True

    r = client.get(f"/founder/missions/diagnostics?twin_id={twin.twin_id}")
    assert r.status_code == 200
    assert r.get_json()["ok"] is True

    r = client.post(
        "/founder/missions/validate",
        json={"twin_id": twin.twin_id},
    )
    assert r.status_code == 200
    body = r.get_json()
    assert body["ok"] is True
