"""AP-002D7 — end-to-end provenance certification."""

from __future__ import annotations

from tests.certification.educational_intelligence.fixtures import (
    ReplayScenario,
    build_fixture,
)
from tests.certification.educational_intelligence.pipeline_harness import (
    EducationalIntelligencePipelineHarness,
)
from tests.certification.educational_intelligence.provenance import (
    REQUIRED_PROVENANCE_KEYS,
)


def test_provenance_chain_complete_for_cold_start() -> None:
    result = EducationalIntelligencePipelineHarness().run_fixture(
        build_fixture(ReplayScenario.COLD_START)
    )
    chain = result.provenance
    assert chain.is_complete, chain.broken_links
    assert chain.assessment_session_id.startswith("sess-")
    assert chain.evidence_bundle_id.startswith("bundle-")
    assert chain.observation_ids
    assert chain.decision_ids
    assert chain.reasoning_request_id
    assert chain.twin_version >= 2
    assert chain.mission_plan_id
    assert chain.explanation_id
    assert chain.correlation_id


def test_every_explanation_section_has_supporting_evidence() -> None:
    result = EducationalIntelligencePipelineHarness().run_fixture(
        build_fixture(ReplayScenario.STRONG_EVIDENCE)
    )
    assert result.explanation.available is True
    expl = result.explanation.explanation
    assert expl.decision_ids
    decision_ids = set(result.decision_set.decisions and result.provenance.decision_ids)
    for decision_id in expl.decision_ids:
        assert decision_id in decision_ids
    assert expl.context.evidence_bundle_id == result.provenance.evidence_bundle_id
    assert expl.context.reasoning_request_id == result.provenance.reasoning_request_id
    for section in expl.sections:
        assert section.body.strip()
        if hasattr(section, "reference") and section.reference is not None:
            ref = section.reference
            assert getattr(ref, "evidence_bundle_id", "") in (
                "",
                result.provenance.evidence_bundle_id,
            )


def test_required_provenance_keys_documented() -> None:
    assert "assessment_session_id" in REQUIRED_PROVENANCE_KEYS
    assert "evidence_bundle_id" in REQUIRED_PROVENANCE_KEYS
    assert "observation_ids" in REQUIRED_PROVENANCE_KEYS
    assert "decision_ids" in REQUIRED_PROVENANCE_KEYS
    assert "reasoning_request_id" in REQUIRED_PROVENANCE_KEYS
    assert "twin_version" in REQUIRED_PROVENANCE_KEYS
    assert "mission_plan_id" in REQUIRED_PROVENANCE_KEYS
    assert "explanation_id" in REQUIRED_PROVENANCE_KEYS
    assert "correlation_id" in REQUIRED_PROVENANCE_KEYS


def test_projection_and_mission_share_decision_lineage() -> None:
    result = EducationalIntelligencePipelineHarness().run_fixture(
        build_fixture(ReplayScenario.CONFLICTING_EVIDENCE)
    )
    decision_ids = set(result.provenance.decision_ids)
    for rel in result.projection.batch.relationships:
        assert rel.decision_id in decision_ids
    selected = result.mission.study_mission_plan.selected_candidate
    assert selected is not None
    if selected.decision_id:
        assert selected.decision_id in decision_ids
