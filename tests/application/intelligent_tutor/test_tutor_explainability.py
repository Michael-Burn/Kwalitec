"""AP-002D6 Tutor explainability from validated educational provenance."""

from __future__ import annotations

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from app.application.intelligent_tutor.explainability.persistence import (
    ExplanationPersistenceService,
)
from app.application.intelligent_tutor.explainability.tutor_explanation_service import (
    TutorExplanationService,
)
from app.application.intelligent_tutor.explainability.validator import (
    ExplanationValidator,
)
from app.application.intelligent_tutor.explainability.versions import (
    EXPLANATION_VERSION,
)
from app.application.intelligent_tutor.intelligent_tutor_service import (
    IntelligentTutorService,
)
from app.application.intelligent_tutor.mappers.explanation_mapper import (
    map_explanation_result,
)
from app.application.mission_engine.planning.mission_planning_service import (
    MissionPlanningService,
)
from app.domain.intelligent_tutor.explainability.errors import (
    DuplicateExplanationRequest,
    IncompleteProvenance,
    InvalidDecisionVersion,
    MissionVersionMismatch,
    TwinVersionMismatch,
    UnsupportedExplanationContract,
)
from app.domain.intelligent_tutor.explainability.events import (
    TutorExplanationGenerated,
    TutorExplanationRequested,
    TutorExplanationUnavailable,
)
from app.domain.intelligent_tutor.explainability.section import (
    ExplanationSectionKind,
)
from app.domain.reasoning.decisions.category import DecisionCategory
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from tests.application.intelligent_tutor.conftest_explainability import (
    EXPLAIN_FIXED_AT,
    make_study_mission_plan,
)
from tests.application.mission_engine.conftest_planning import (
    make_decision,
    make_decision_set,
    make_graph,
    make_twin,
)


def test_explanation_generation_from_mastery_decision() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    plan = make_study_mission_plan(twin=twin)
    result = TutorExplanationService().explain(
        twin,
        decision_set,
        study_mission_plan=plan,
        learning_graph=make_graph(twin=twin),
        explained_at=EXPLAIN_FIXED_AT,
        persist=False,
    )

    assert result.available is True
    assert result.generated_count == 1
    assert result.section_count >= 4
    kinds = {s.kind for s in result.explanation.sections}
    assert ExplanationSectionKind.DECISION in kinds
    assert ExplanationSectionKind.EVIDENCE in kinds
    assert ExplanationSectionKind.CONCEPT in kinds
    assert ExplanationSectionKind.MISSION in kinds
    assert ExplanationSectionKind.LEARNING_OBJECTIVE in kinds
    event_kinds = [e.kind.value for e in result.events]
    assert "tutor_explanation_requested" in event_kinds
    assert "tutor_explanation_generated" in event_kinds
    assert isinstance(result.events[0], TutorExplanationRequested)
    assert any(isinstance(e, TutorExplanationGenerated) for e in result.events)


def test_traceability_on_every_section() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = TutorExplanationService().explain(
        twin, decision_set, explained_at=EXPLAIN_FIXED_AT, persist=False
    )
    for section in result.explanation.sections:
        ref = section.reference
        assert ref.decision_id
        assert ref.evidence_bundle_id
        assert ref.educational_observation_ids
        assert ref.reasoning_request_id
        assert ref.assessment_session_id
        assert ref.correlation_id
        assert ref.twin_version == twin.version
        assert ref.explanation_version == EXPLANATION_VERSION
        for key in (
            "decision_id",
            "evidence_bundle_id",
            "educational_observation_ids",
            "reasoning_request_id",
            "assessment_session_id",
            "correlation_id",
            "twin_version",
            "explanation_version",
        ):
            assert key in section.provenance


def test_deterministic_explanation_identical_inputs() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    plan = make_study_mission_plan(twin=twin)
    service = TutorExplanationService()
    a = service.explain(
        twin,
        decision_set,
        study_mission_plan=plan,
        explained_at=EXPLAIN_FIXED_AT,
        persist=False,
    )
    b = service.explain(
        twin,
        decision_set,
        study_mission_plan=plan,
        explained_at=EXPLAIN_FIXED_AT,
        persist=False,
    )
    assert a.explanation_id == b.explanation_id
    assert a.section_ids == b.section_ids
    assert a.explanation.summary == b.explanation.summary
    assert [s.body for s in a.explanation.sections] == [
        s.body for s in b.explanation.sections
    ]


def test_replay_consistency() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    plan = make_study_mission_plan(twin=twin)
    service = TutorExplanationService()
    first = service.explain(
        twin,
        decision_set,
        study_mission_plan=plan,
        explained_at=EXPLAIN_FIXED_AT,
    )
    replayed = service.replay(
        twin,
        decision_set,
        study_mission_plan=plan,
        explained_at=EXPLAIN_FIXED_AT,
    )
    assert first.explanation_id == replayed.explanation_id
    assert first.section_ids == replayed.section_ids
    assert first.explanation.summary == replayed.explanation.summary
    assert service.explanation_snapshot(twin_id=twin.twin_id)[
        "explanations"
    ][0]["summary"] == replayed.explanation.summary


def test_duplicate_explanation_request_idempotent_skip() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    store = ExplanationPersistenceService()
    service = TutorExplanationService(persistence=store)
    first = service.explain(twin, decision_set, explained_at=EXPLAIN_FIXED_AT)
    second = service.explain(twin, decision_set, explained_at=EXPLAIN_FIXED_AT)
    assert first.generated_count == 1
    assert second.generated_count == 0
    assert any(
        isinstance(e, TutorExplanationUnavailable)
        and e.reason_code == "duplicate_explanation_request"
        for e in second.events
    )


def test_duplicate_explanation_request_strict_raises() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    store = ExplanationPersistenceService()
    service = TutorExplanationService(persistence=store)
    service.explain(twin, decision_set, explained_at=EXPLAIN_FIXED_AT)
    with pytest.raises(DuplicateExplanationRequest):
        service.explain(
            twin,
            decision_set,
            explained_at=EXPLAIN_FIXED_AT,
            allow_idempotent_skip=False,
        )


def test_soft_decisions_explain_uncertainty_explicitly() -> None:
    twin = make_twin()
    soft = make_decision(
        decision_id="ed-soft",
        category=DecisionCategory.UNCERTAINTY_PRESERVED,
        concept_reference="concept-bayes",
    )
    decision_set = make_decision_set(twin_id=twin.twin_id, decisions=(soft,))
    result = TutorExplanationService().explain(
        twin, decision_set, explained_at=EXPLAIN_FIXED_AT, persist=False
    )
    assert result.available is True
    assert result.generated_count == 1
    kinds = {s.kind for s in result.explanation.sections}
    assert ExplanationSectionKind.UNCERTAINTY in kinds
    assert any("uncertain" in n.lower() or "uncertainty" in n.lower()
               for n in result.explanation.uncertainty_notes)
    assert "mastery" not in result.explanation.summary.lower() or "no" in (
        result.explanation.summary.lower()
    )


def test_empty_decision_set_unavailable() -> None:
    twin = make_twin()
    context = make_decision_set(twin_id=twin.twin_id).context
    empty = EducationalDecisionSet(
        set_id="eds-empty",
        decisions=(),
        context=context,
        decision_version=context.decision_version,
    )
    result = TutorExplanationService().explain(
        twin, empty, explained_at=EXPLAIN_FIXED_AT, persist=False
    )
    assert result.available is False
    assert result.unavailable_count == 1
    assert any(isinstance(e, TutorExplanationUnavailable) for e in result.events)


def test_validation_rejects_unsupported_explanation_version() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    service = TutorExplanationService()
    result = service.explain(
        twin, decision_set, explained_at=EXPLAIN_FIXED_AT, persist=False
    )
    bad = replace(
        result.explanation,
        explanation_version="AP-002D6.explanation.v999",
        context=replace(
            result.explanation.context,
            explanation_version="AP-002D6.explanation.v999",
        ),
    )
    with pytest.raises(UnsupportedExplanationContract):
        ExplanationValidator().validate(bad)


def test_validation_rejects_invalid_decision_version() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = TutorExplanationService().explain(
        twin, decision_set, explained_at=EXPLAIN_FIXED_AT, persist=False
    )
    bad = replace(
        result.explanation,
        context=replace(
            result.explanation.context, decision_version="AP-002D3.decision.v999"
        ),
    )
    with pytest.raises(InvalidDecisionVersion):
        ExplanationValidator().validate(bad)


def test_validation_rejects_missing_provenance_keys() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = TutorExplanationService().explain(
        twin, decision_set, explained_at=EXPLAIN_FIXED_AT, persist=False
    )
    section = result.explanation.sections[0]
    broken_section = replace(
        section,
        provenance={"decision_id": section.reference.decision_id},
    )
    bad = replace(
        result.explanation,
        sections=(broken_section, *result.explanation.sections[1:]),
    )
    with pytest.raises(IncompleteProvenance):
        ExplanationValidator().validate(bad)


def test_twin_version_mismatch_with_mission_plan() -> None:
    twin = make_twin(version=1)
    plan = make_study_mission_plan(twin=twin)
    twin_v2 = replace(twin, version=2)
    decision_set = make_decision_set(twin_id=twin.twin_id)
    with pytest.raises(TwinVersionMismatch):
        TutorExplanationService().explain(
            twin_v2,
            decision_set,
            study_mission_plan=plan,
            explained_at=EXPLAIN_FIXED_AT,
            persist=False,
        )


def test_mission_version_mismatch_rejected() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    plan = make_study_mission_plan(twin=twin)
    bad_plan = replace(
        plan,
        planning_version="AP-002D5.planning.v999",
        context=replace(plan.context, planning_version="AP-002D5.planning.v999"),
    )
    with pytest.raises(MissionVersionMismatch):
        TutorExplanationService().explain(
            twin,
            decision_set,
            study_mission_plan=bad_plan,
            explained_at=EXPLAIN_FIXED_AT,
            persist=False,
        )


def test_dto_mapping() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = TutorExplanationService().explain(
        twin, decision_set, explained_at=EXPLAIN_FIXED_AT, persist=False
    )
    dto = map_explanation_result(result)
    assert dto.explanation_id == result.explanation_id
    assert dto.section_count == result.section_count
    assert dto.available is True
    assert len(dto.sections) == result.section_count
    assert dto.events[0].kind == "tutor_explanation_requested"


def test_intelligent_tutor_service_explain_from_decisions() -> None:
    from unittest.mock import MagicMock

    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    plan = make_study_mission_plan(twin=twin)
    explanations = TutorExplanationService()
    graphs = MagicMock()
    graphs.get_for_twin.return_value = None
    service = IntelligentTutorService(
        twins=MagicMock(),
        graphs=graphs,
        traversal=MagicMock(),
        missions=MagicMock(),
        assessments=MagicMock(),
        explanations=explanations,
    )
    result = service.explain_from_decisions(
        twin,
        decision_set,
        study_mission_plan=plan,
        explained_at=EXPLAIN_FIXED_AT,
        persist=False,
    )
    assert result.available is True
    assert result.generated_count == 1
    assert service.explanations is explanations


def test_student_reasoning_service_untouched_regression() -> None:
    path = (
        Path(__file__).resolve().parents[3]
        / "app"
        / "application"
        / "student_digital_twin"
        / "student_reasoning_service.py"
    )
    # File must exist and not import Tutor explainability (authority boundary).
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "TutorExplanationService" not in text
    assert "AP-002D6" not in text
    tree = ast.parse(text)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
    assert not any(
        name.startswith("app.application.intelligent_tutor.explainability")
        for name in imported
    )


def test_mission_planning_then_tutor_explanation_pipeline() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    planning = MissionPlanningService().plan(
        twin,
        decision_set,
        learning_graph=make_graph(twin=twin),
        planned_at=EXPLAIN_FIXED_AT,
        persist=False,
    )
    explanation = TutorExplanationService().explain(
        twin,
        decision_set,
        study_mission_plan=planning.study_mission_plan,
        learning_graph=make_graph(twin=twin),
        explained_at=EXPLAIN_FIXED_AT,
        persist=False,
    )
    assert planning.generated_count == 1
    assert explanation.generated_count == 1
    assert explanation.explanation.mission_plan_id == planning.plan_id
    mission_sections = [
        s
        for s in explanation.explanation.sections
        if s.kind is ExplanationSectionKind.MISSION
    ]
    assert mission_sections
    assert planning.mission_id in mission_sections[0].body


def test_does_not_predict_exam_outcomes() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    result = TutorExplanationService().explain(
        twin, decision_set, explained_at=EXPLAIN_FIXED_AT, persist=False
    )
    text = " ".join(
        [result.explanation.summary, *[s.body for s in result.explanation.sections]]
    ).lower()
    for banned in (
        "pass probability",
        "you will pass",
        "exam outcome",
        "predicted score",
    ):
        assert banned not in text
