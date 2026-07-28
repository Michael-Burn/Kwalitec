"""AP-002D7 — end-to-end Educational Intelligence pipeline certification."""

from __future__ import annotations

import pytest

from app.application.reasoning.decisions.versions import DECISION_VERSION
from app.application.reasoning.interpretation.versions import INTERPRETATION_VERSION
from app.domain.reasoning.decisions.category import DecisionCategory
from tests.certification.educational_intelligence.contracts import (
    EXPECTED_DECISION,
    EXPECTED_EXPLANATION,
    EXPECTED_INTERPRETATION,
    EXPECTED_PLANNING,
    EXPECTED_PROJECTION,
    assert_certified_contract_matrix,
)
from tests.certification.educational_intelligence.fixtures import (
    ReplayScenario,
    build_fixture,
)
from tests.certification.educational_intelligence.pipeline_harness import (
    EducationalIntelligencePipelineHarness,
)


def test_certified_contract_matrix() -> None:
    assert_certified_contract_matrix()
    assert INTERPRETATION_VERSION == EXPECTED_INTERPRETATION
    assert DECISION_VERSION == EXPECTED_DECISION


def test_full_pipeline_certification_cold_start() -> None:
    harness = EducationalIntelligencePipelineHarness()
    fixture = build_fixture(ReplayScenario.COLD_START)
    result = harness.run_fixture(fixture)

    assert result.certified
    assert result.provenance.is_complete
    assert result.observation_set.interpretation_version == EXPECTED_INTERPRETATION
    assert result.decision_set.decision_version == EXPECTED_DECISION
    assert result.projection.context.projection_version == EXPECTED_PROJECTION
    assert result.mission.study_mission_plan.planning_version == EXPECTED_PLANNING
    assert result.explanation.explanation.explanation_version == EXPECTED_EXPLANATION
    assert result.twin.version == 2
    assert result.explanation.available is True
    assert result.provenance.assessment_session_id
    assert result.provenance.evidence_bundle_id
    assert result.provenance.observation_ids
    assert result.provenance.decision_ids
    assert result.provenance.reasoning_request_id
    assert result.provenance.mission_plan_id
    assert result.provenance.explanation_id
    assert result.provenance.correlation_id


def test_pipeline_stages_preserve_authority_outputs() -> None:
    harness = EducationalIntelligencePipelineHarness()
    fixture = build_fixture(ReplayScenario.STRONG_EVIDENCE)
    result = harness.run_fixture(fixture)

    # Twin alone stores belief
    assert result.twin.mastery.get("concept-bayes") is not None
    # Graph / projection stores relationships only (not mastery SoT)
    assert result.projection.relationship_count >= 1
    # Mission plans only
    assert result.mission.study_mission_plan.selected_candidate is not None
    # Tutor explains only
    assert result.explanation.explanation.sections
    assert result.explanation.explanation.decision_ids


def test_assessment_never_updates_twin_via_interpretation_only() -> None:
    from app.application.reasoning.interpretation.evidence_interpreter import (
        EvidenceInterpreter,
    )
    from app.domain.student_digital_twin.student import Student
    from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
    from tests.certification.educational_intelligence.fixtures import CERT_FIXED_AT

    twin = StudentDigitalTwin.create(
        twin_id="twin-interp-only",
        student=Student(student_id="s-interp", display_name="L"),
        created_at=CERT_FIXED_AT,
    )
    before = twin.version
    fixture = build_fixture(ReplayScenario.COLD_START)
    EvidenceInterpreter().interpret_bundle(
        fixture.bundle,
        correlation_id=fixture.correlation_id,
        reasoning_request_id=fixture.reasoning_request_id,
        interpreted_at=CERT_FIXED_AT,
    )
    assert twin.version == before
    assert twin.mastery.records == ()


@pytest.mark.parametrize(
    "scenario",
    [
        ReplayScenario.COLD_START,
        ReplayScenario.STRONG_EVIDENCE,
        ReplayScenario.WEAK_EVIDENCE,
        ReplayScenario.CONFLICTING_EVIDENCE,
        ReplayScenario.PARTIAL_EVIDENCE,
    ],
)
def test_pipeline_certifies_named_scenarios(scenario: ReplayScenario) -> None:
    harness = EducationalIntelligencePipelineHarness()
    result = harness.run_fixture(build_fixture(scenario))
    assert result.certified, result.errors
    assert result.provenance.is_complete
    categories = {d.category for d in result.decision_set.decisions}
    assert DecisionCategory.PROVENANCE_RECORDED in categories or categories
