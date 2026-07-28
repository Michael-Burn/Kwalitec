"""AP-002D5 Mission planning from validated Twin decisions."""

from __future__ import annotations

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from app.application.mission_engine.mappers.planning_mapper import map_planning_result
from app.application.mission_engine.planning.mission_planning_service import (
    MissionPlanningService,
)
from app.application.mission_engine.planning.persistence import (
    PlanningPersistenceService,
)
from app.application.mission_engine.planning.validator import PlanningValidator
from app.application.mission_engine.planning.versions import PLANNING_VERSION
from app.domain.mission.planning.errors import (
    DuplicateMissionRequest,
    IncompleteProvenance,
    InvalidDecisionVersion,
    UnsupportedPlanningContract,
)
from app.domain.mission.planning.events import (
    MissionGenerated,
    MissionPlanningCompleted,
    MissionPlanningSkipped,
    MissionPlanningStarted,
)
from app.domain.reasoning.decisions.category import DecisionCategory
from tests.application.mission_engine.conftest_planning import (
    FIXED_AT,
    make_decision,
    make_decision_set,
    make_graph,
    make_twin,
)


def test_mission_generation_from_mastery_decision() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    service = MissionPlanningService()
    result = service.plan(
        twin, decision_set, learning_graph=make_graph(twin=twin), planned_at=FIXED_AT
    )

    assert result.candidate_count == 1
    assert result.generated_count == 1
    assert result.study_mission_plan.mission_id
    assert result.study_mission_plan.selected_candidate is not None
    assert (
        result.study_mission_plan.selected_candidate.concept_id == "concept-bayes"
    )
    kinds = [e.kind.value for e in result.events]
    assert "mission_planning_started" in kinds
    assert "mission_generated" in kinds
    assert "mission_planning_completed" in kinds
    assert isinstance(result.events[0], MissionPlanningStarted)
    assert any(isinstance(e, MissionGenerated) for e in result.events)
    assert isinstance(result.events[-1], MissionPlanningCompleted)


def test_deterministic_planning_identical_inputs() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    service = MissionPlanningService()
    a = service.plan(twin, decision_set, planned_at=FIXED_AT, persist=False)
    b = service.plan(twin, decision_set, planned_at=FIXED_AT, persist=False)
    assert a.plan_id == b.plan_id
    assert a.mission_id == b.mission_id
    assert a.candidate_ids == b.candidate_ids
    assert a.study_mission_plan.goal == b.study_mission_plan.goal
    snap_a = {
        "candidates": [
            (c.candidate_id, c.priority_score, c.concept_id)
            for c in a.batch.candidates
        ],
        "events": [e.kind.value for e in a.events],
    }
    snap_b = {
        "candidates": [
            (c.candidate_id, c.priority_score, c.concept_id)
            for c in b.batch.candidates
        ],
        "events": [e.kind.value for e in b.events],
    }
    assert snap_a == snap_b


def test_duplicate_mission_request_idempotent_skip() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    store = PlanningPersistenceService()
    service = MissionPlanningService(persistence=store)
    first = service.plan(twin, decision_set, planned_at=FIXED_AT)
    second = service.plan(twin, decision_set, planned_at=FIXED_AT)
    assert first.generated_count == 1
    assert second.generated_count == 0
    assert any(
        isinstance(e, MissionPlanningSkipped)
        and e.reason_code == "duplicate_mission_request"
        for e in second.events
    )


def test_duplicate_mission_request_strict_raises() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    store = PlanningPersistenceService()
    service = MissionPlanningService(persistence=store)
    service.plan(twin, decision_set, planned_at=FIXED_AT)
    with pytest.raises(DuplicateMissionRequest):
        service.plan(
            twin,
            decision_set,
            planned_at=FIXED_AT,
            allow_idempotent_skip=False,
        )


def test_soft_decisions_are_skipped() -> None:
    twin = make_twin()
    soft = make_decision(
        decision_id="ed-soft",
        category=DecisionCategory.UNCERTAINTY_PRESERVED,
        concept_reference="concept-bayes",
    )
    decision_set = make_decision_set(twin_id=twin.twin_id, decisions=(soft,))
    result = MissionPlanningService().plan(
        twin, decision_set, planned_at=FIXED_AT, persist=False
    )
    assert result.candidate_count == 0
    assert result.batch.skipped_decision_ids == ("ed-soft",)
    assert any(
        isinstance(e, MissionPlanningSkipped)
        and e.reason_code == "non_plannable_decision"
        for e in result.events
    )


def test_validation_rejects_unsupported_planning_version() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    service = MissionPlanningService()
    result = service.plan(twin, decision_set, planned_at=FIXED_AT, persist=False)
    bad_context = replace(
        result.batch.context, planning_version="AP-002D5.planning.v999"
    )
    bad_candidates = tuple(
        replace(c, planning_version="AP-002D5.planning.v999")
        for c in result.batch.candidates
    )
    bad_batch = replace(
        result.batch,
        context=bad_context,
        planning_version="AP-002D5.planning.v999",
        candidates=bad_candidates,
    )
    with pytest.raises(UnsupportedPlanningContract):
        PlanningValidator().validate(bad_batch)


def test_validation_rejects_invalid_decision_version() -> None:
    twin = make_twin()
    soft = make_decision(
        decision_id="ed-prov",
        category=DecisionCategory.PROVENANCE_RECORDED,
        decision_version="AP-002D3.decision.v999",
    )
    from tests.application.mission_engine.conftest_planning import (
        make_decision_context,
    )

    ctx = make_decision_context(decision_version="AP-002D3.decision.v999")
    decision_set = make_decision_set(
        twin_id=twin.twin_id, decisions=(soft,), context=ctx
    )
    with pytest.raises(InvalidDecisionVersion):
        MissionPlanningService().plan(
            twin, decision_set, planned_at=FIXED_AT, persist=False
        )


def test_validation_rejects_incomplete_provenance() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = MissionPlanningService().plan(
        twin, decision_set, planned_at=FIXED_AT, persist=False
    )
    cand = result.batch.candidates[0]
    broken = replace(cand, provenance={"decision_id": cand.decision_id})
    bad_batch = replace(result.batch, candidates=(broken,))
    with pytest.raises(IncompleteProvenance):
        PlanningValidator().validate(bad_batch)


def test_version_compatibility_planning_contract() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = MissionPlanningService().plan(
        twin, decision_set, planned_at=FIXED_AT, persist=False
    )
    assert result.context.planning_version == PLANNING_VERSION
    assert result.context.decision_version == "AP-002D3.decision.v1"
    assert result.batch.candidates[0].planning_version == PLANNING_VERSION


def test_traceability_chain_on_candidate() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = MissionPlanningService().plan(
        twin, decision_set, planned_at=FIXED_AT, persist=False
    )
    cand = result.batch.candidates[0]
    ref = cand.reference
    assert ref.decision_id
    assert ref.evidence_bundle_id == "bundle-plan-1"
    assert ref.educational_observation_ids == ("obs-plan-1",)
    assert ref.reasoning_request_id == "rr-plan-1"
    assert ref.assessment_session_id == "sess-plan-1"
    assert ref.correlation_id == "corr-plan-1"
    assert cand.provenance["evidence_bundle_id"] == ref.evidence_bundle_id
    plan_prov = result.study_mission_plan.provenance
    assert plan_prov["decision_set_id"] == decision_set.set_id
    assert plan_prov["selected_decision_id"] == cand.decision_id


def test_replay_consistency() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    service = MissionPlanningService()
    first = service.plan(twin, decision_set, planned_at=FIXED_AT)
    replayed = service.replay(twin, decision_set, planned_at=FIXED_AT)
    assert first.plan_id == replayed.plan_id
    assert first.mission_id == replayed.mission_id
    assert first.candidate_ids == replayed.candidate_ids
    assert [e.kind.value for e in first.events] == [
        e.kind.value for e in replayed.events
    ]


def test_dto_mapping() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = MissionPlanningService().plan(
        twin, decision_set, planned_at=FIXED_AT, persist=False
    )
    dto = map_planning_result(result)
    assert dto.plan_id == result.plan_id
    assert dto.mission_id == result.mission_id
    assert dto.candidate_count == 1
    assert dto.events[0].kind == "mission_planning_started"
    assert dto.candidates[0].concept_id == "concept-bayes"


def test_adaptive_mission_service_plan_from_decisions(ctx) -> None:
    from app.application.adaptive_mission.adaptive_mission_service import (
        AdaptiveMissionService,
    )

    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    service = AdaptiveMissionService(
        planning_persistence=PlanningPersistenceService()
    )
    result = service.plan_from_decisions(
        twin, decision_set, planned_at=FIXED_AT, persist=True
    )
    assert result.generated_count == 1
    assert result.study_mission_plan.selected_candidate is not None


def test_student_reasoning_service_untouched_by_planning_imports() -> None:
    path = (
        Path(__file__).resolve().parents[3]
        / "app"
        / "application"
        / "student_digital_twin"
        / "student_reasoning_service.py"
    )
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    assert not any("mission_engine.planning" in m for m in imported)
    text = path.read_text(encoding="utf-8")
    assert "MissionPlanningService" not in text
    assert "plan_from_decisions" not in text


def test_prioritisation_ranking_prefers_higher_score() -> None:
    twin = make_twin()
    low = make_decision(
        decision_id="ed-low",
        concept_reference="concept-low",
        subject_ref="concept-low",
        value=0.8,
    )
    high = make_decision(
        decision_id="ed-high",
        concept_reference="concept-high",
        subject_ref="concept-high",
        value=0.2,
        payload={
            "mastery_id": "mst-high",
            "misconception_tags": ["misconception-x"],
        },
    )
    decision_set = make_decision_set(
        twin_id=twin.twin_id, decisions=(low, high)
    )
    result = MissionPlanningService().plan(
        twin, decision_set, planned_at=FIXED_AT, persist=False
    )
    assert result.candidate_count == 2
    selected = result.study_mission_plan.selected_candidate
    assert selected is not None
    assert selected.concept_id == result.batch.candidates[0].concept_id
    scores = [c.priority_score for c in result.batch.candidates]
    assert scores == sorted(scores, reverse=True)
