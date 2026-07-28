"""AP-002D7 — deterministic replay certification."""

from __future__ import annotations

import pytest

from app.application.reasoning.interpretation.errors import UnsupportedEvidenceSchema
from app.domain.reasoning.decisions.category import DecisionCategory
from tests.certification.educational_intelligence.fixtures import (
    ReplayScenario,
    all_replay_fixtures,
    build_fixture,
)
from tests.certification.educational_intelligence.pipeline_harness import (
    EducationalIntelligencePipelineHarness,
)


@pytest.mark.parametrize(
    "scenario",
    [
        ReplayScenario.COLD_START,
        ReplayScenario.RETURNING,
        ReplayScenario.STRONG_EVIDENCE,
        ReplayScenario.WEAK_EVIDENCE,
        ReplayScenario.CONFLICTING_EVIDENCE,
        ReplayScenario.DUPLICATE_SUBMISSION,
        ReplayScenario.PARTIAL_EVIDENCE,
    ],
)
def test_identical_evidence_replays_identically(scenario: ReplayScenario) -> None:
    fixture = build_fixture(scenario)
    harness = EducationalIntelligencePipelineHarness()
    first = harness.run_fixture(fixture)
    twin_seed = harness.make_cold_start_twin(
        twin_id=fixture.twin_id,
        student_id=fixture.student_id,
    )
    second = harness.replay(
        twin_seed,
        fixture.bundle,
        correlation_id=fixture.correlation_id,
        reasoning_request_id=fixture.reasoning_request_id,
        graph_id=f"lg-{fixture.scenario.value}",
    )

    assert first.fingerprints.observation == second.fingerprints.observation
    assert first.fingerprints.decision == second.fingerprints.decision
    assert first.fingerprints.twin == second.fingerprints.twin
    assert first.fingerprints.projection == second.fingerprints.projection
    assert first.fingerprints.mission == second.fingerprints.mission
    assert first.fingerprints.explanation == second.fingerprints.explanation
    assert first.certified and second.certified


def test_returning_learner_accumulates_without_nondeterminism() -> None:
    harness = EducationalIntelligencePipelineHarness()
    cold = build_fixture(ReplayScenario.COLD_START)
    first = harness.run_fixture(cold)
    returning = build_fixture(ReplayScenario.RETURNING)
    # Reuse belief state from first cycle with a distinct evidence bundle.
    second = harness.run(
        first.twin,
        returning.bundle,
        correlation_id=returning.correlation_id,
        reasoning_request_id=returning.reasoning_request_id,
        graph_id="lg-returning-accum",
        persist=False,
    )
    score_1 = first.twin.mastery.get("concept-bayes").mastery_score
    score_2 = second.twin.mastery.get("concept-bayes").mastery_score
    assert score_2 != score_1 or second.twin.version > first.twin.version
    # Replay the returning cycle from the post-cold twin seed for identity.
    seed = first.twin
    replay_a = harness.run(
        seed,
        returning.bundle,
        correlation_id=returning.correlation_id,
        reasoning_request_id=returning.reasoning_request_id,
        graph_id="lg-returning-replay-a",
        persist=False,
    )
    replay_b = harness.run(
        seed,
        returning.bundle,
        correlation_id=returning.correlation_id,
        reasoning_request_id=returning.reasoning_request_id,
        graph_id="lg-returning-replay-b",
        persist=False,
    )
    assert replay_a.fingerprints.decision == replay_b.fingerprints.decision
    assert replay_a.fingerprints.twin == replay_b.fingerprints.twin


def test_version_mismatch_rejected() -> None:
    fixture = build_fixture(ReplayScenario.VERSION_MISMATCH)
    harness = EducationalIntelligencePipelineHarness()
    with pytest.raises(UnsupportedEvidenceSchema):
        harness.run_fixture(fixture)


def test_duplicate_submission_is_bitwise_identical() -> None:
    fixture = build_fixture(ReplayScenario.DUPLICATE_SUBMISSION)
    harness = EducationalIntelligencePipelineHarness()
    a = harness.run_fixture(fixture)
    b = harness.run_fixture(fixture)
    assert a.fingerprints == b.fingerprints


def test_all_replay_fixtures_are_registered() -> None:
    fixtures = all_replay_fixtures()
    names = {f.scenario for f in fixtures}
    assert names == set(ReplayScenario)


def test_weak_evidence_preserves_uncertainty() -> None:
    harness = EducationalIntelligencePipelineHarness()
    result = harness.run_fixture(build_fixture(ReplayScenario.WEAK_EVIDENCE))
    categories = {d.category for d in result.decision_set.decisions}
    mastery = result.twin.mastery.get("concept-bayes")
    if DecisionCategory.MASTERY_BELIEF_UPDATE in categories:
        assert mastery is not None
        assert mastery.mastery_score < 0.95
        assert mastery.confidence < 0.95
    # Cold honesty: never fabricate perfect mastery from thin evidence.
    if mastery is not None:
        assert mastery.mastery_score < 1.0
        assert mastery.confidence < 0.99
    assert result.explanation.available is True
    assert result.certified
