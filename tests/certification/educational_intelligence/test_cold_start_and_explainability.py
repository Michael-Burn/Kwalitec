"""AP-002D7 — cold-start honesty and explainability audit."""

from __future__ import annotations

from app.domain.reasoning.decisions.category import DecisionCategory
from tests.certification.educational_intelligence.fixtures import (
    ReplayScenario,
    build_fixture,
)
from tests.certification.educational_intelligence.pipeline_harness import (
    EducationalIntelligencePipelineHarness,
)


def test_cold_start_never_fabricates_perfect_mastery() -> None:
    harness = EducationalIntelligencePipelineHarness()
    twin = harness.make_cold_start_twin(
        twin_id="twin-cold-honesty",
        student_id="student-cold-honesty",
    )
    assert twin.mastery.records == ()
    assert twin.confidence.score == 0.0

    result = harness.run_fixture(build_fixture(ReplayScenario.COLD_START), twin=twin)
    record = result.twin.mastery.get("concept-bayes")
    assert record is not None
    assert 0.0 < record.mastery_score < 1.0
    assert record.confidence < 0.95
    assert result.explanation.available is True


def test_weak_and_partial_evidence_preserve_uncertainty() -> None:
    harness = EducationalIntelligencePipelineHarness()
    for scenario in (ReplayScenario.WEAK_EVIDENCE, ReplayScenario.PARTIAL_EVIDENCE):
        result = harness.run_fixture(build_fixture(scenario))
        categories = {d.category for d in result.decision_set.decisions}
        mastery = result.twin.mastery.get("concept-bayes")
        if DecisionCategory.MASTERY_BELIEF_UPDATE in categories:
            assert mastery is not None
            assert mastery.mastery_score < 0.95
            assert mastery.confidence < 0.95
        else:
            assert DecisionCategory.UNCERTAINTY_PRESERVED in categories
        assert result.explanation.available is True
        assert result.certified


def test_no_explanation_without_supporting_decisions() -> None:
    result = EducationalIntelligencePipelineHarness().run_fixture(
        build_fixture(ReplayScenario.STRONG_EVIDENCE)
    )
    expl = result.explanation.explanation
    assert expl.decision_ids
    known = set(result.provenance.decision_ids)
    assert set(expl.decision_ids).issubset(known)
    assert expl.context.evidence_bundle_id == result.provenance.evidence_bundle_id
    assert result.provenance.is_complete


def test_conflicting_evidence_does_not_overstate_mastery() -> None:
    result = EducationalIntelligencePipelineHarness().run_fixture(
        build_fixture(ReplayScenario.CONFLICTING_EVIDENCE)
    )
    mastery = result.twin.mastery.get("concept-bayes")
    assert mastery is not None
    assert mastery.mastery_score < 0.9
    assert mastery.confidence < 0.95
    assert result.explanation.available is True
