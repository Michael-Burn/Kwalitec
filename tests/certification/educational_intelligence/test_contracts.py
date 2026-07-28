"""AP-002D7 — contract compatibility certification."""

from __future__ import annotations

from dataclasses import replace

import pytest

from app.application.intelligent_tutor.explainability.errors import (
    InvalidDecisionVersion as ExplanationInvalidDecisionVersion,
)
from app.application.intelligent_tutor.explainability.tutor_explanation_service import (
    TutorExplanationService,
)
from app.application.learning_graph.projections.errors import (
    InvalidDecisionVersion as ProjectionInvalidDecisionVersion,
)
from app.application.learning_graph.projections.twin_projection_service import (
    TwinProjectionService,
)
from app.application.mission_engine.planning.errors import (
    InvalidDecisionVersion as PlanningInvalidDecisionVersion,
)
from app.application.mission_engine.planning.mission_planning_service import (
    MissionPlanningService,
)
from app.application.reasoning.decisions.errors import UnsupportedDecisionVersion
from app.application.reasoning.decisions.validator import DecisionValidator
from app.application.reasoning.interpretation.errors import UnsupportedEvidenceSchema
from app.application.reasoning.interpretation.evidence_interpreter import (
    EvidenceInterpreter,
)
from tests.application.mission_engine.conftest_planning import (
    FIXED_AT,
    make_decision_set,
    make_twin,
)
from tests.certification.educational_intelligence.contracts import (
    CERTIFIED_CONTRACTS,
    EXPECTED_DECISION,
    EXPECTED_EXPLANATION,
    EXPECTED_INGRESS,
    EXPECTED_INTERPRETATION,
    EXPECTED_PACKAGING,
    EXPECTED_PLANNING,
    EXPECTED_PROJECTION,
    UNSUPPORTED_VERSION_PROBE,
    assert_certified_contract_matrix,
)
from tests.certification.educational_intelligence.fixtures import (
    ReplayScenario,
    build_fixture,
)


def test_contract_matrix_values() -> None:
    assert_certified_contract_matrix()
    assert CERTIFIED_CONTRACTS["packaging"] == EXPECTED_PACKAGING
    assert CERTIFIED_CONTRACTS["evidence_ingress"] == EXPECTED_INGRESS
    assert CERTIFIED_CONTRACTS["interpretation"] == EXPECTED_INTERPRETATION
    assert CERTIFIED_CONTRACTS["decision"] == EXPECTED_DECISION
    assert CERTIFIED_CONTRACTS["projection"] == EXPECTED_PROJECTION
    assert CERTIFIED_CONTRACTS["planning"] == EXPECTED_PLANNING
    assert CERTIFIED_CONTRACTS["explanation"] == EXPECTED_EXPLANATION


def test_unsupported_packaging_rejected_at_interpretation() -> None:
    fixture = build_fixture(ReplayScenario.VERSION_MISMATCH)
    with pytest.raises(UnsupportedEvidenceSchema):
        EvidenceInterpreter().interpret_bundle(
            fixture.bundle,
            correlation_id=fixture.correlation_id,
            reasoning_request_id=fixture.reasoning_request_id,
            interpreted_at=FIXED_AT,
        )


def test_unsupported_decision_version_rejected() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    bad = decision_set
    object.__setattr__(bad, "decision_version", UNSUPPORTED_VERSION_PROBE)
    object.__setattr__(
        bad,
        "context",
        replace(decision_set.context, decision_version=UNSUPPORTED_VERSION_PROBE),
    )
    with pytest.raises(UnsupportedDecisionVersion):
        DecisionValidator().validate(bad, twin=twin)


def test_projection_rejects_invalid_decision_version() -> None:
    twin = make_twin(version=2)
    decision_set = make_decision_set(twin_id=twin.twin_id)
    bad = decision_set
    object.__setattr__(bad, "decision_version", UNSUPPORTED_VERSION_PROBE)
    object.__setattr__(
        bad,
        "context",
        replace(decision_set.context, decision_version=UNSUPPORTED_VERSION_PROBE),
    )
    with pytest.raises(ProjectionInvalidDecisionVersion):
        TwinProjectionService().project(
            twin, bad, graph_id="lg-ver", projected_at=FIXED_AT, persist=False
        )


def test_planning_rejects_invalid_decision_version() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    bad = decision_set
    object.__setattr__(bad, "decision_version", UNSUPPORTED_VERSION_PROBE)
    object.__setattr__(
        bad,
        "context",
        replace(decision_set.context, decision_version=UNSUPPORTED_VERSION_PROBE),
    )
    with pytest.raises(PlanningInvalidDecisionVersion):
        MissionPlanningService().plan(twin, bad, planned_at=FIXED_AT, persist=False)


def test_explanation_rejects_invalid_decision_version() -> None:
    twin = make_twin()
    decision_set = make_decision_set(twin_id=twin.twin_id)
    service = TutorExplanationService()
    bad = decision_set
    object.__setattr__(bad, "decision_version", UNSUPPORTED_VERSION_PROBE)
    object.__setattr__(
        bad,
        "context",
        replace(decision_set.context, decision_version=UNSUPPORTED_VERSION_PROBE),
    )
    with pytest.raises(ExplanationInvalidDecisionVersion):
        service.explain(twin, bad, explained_at=FIXED_AT, persist=False)
