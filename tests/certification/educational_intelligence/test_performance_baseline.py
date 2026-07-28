"""AP-002D7 — performance baseline recording (no optimisation)."""

from __future__ import annotations

from tests.certification.educational_intelligence.fixtures import (
    ReplayScenario,
    build_fixture,
)
from tests.certification.educational_intelligence.pipeline_harness import (
    EducationalIntelligencePipelineHarness,
)

# Soft CI budgets (ms). Baselines only — not production SLOs.
PIPELINE_BUDGET_MS = 5_000.0
STAGE_BUDGET_MS = 2_000.0


def test_pipeline_performance_baseline() -> None:
    harness = EducationalIntelligencePipelineHarness()
    result = harness.run_fixture(build_fixture(ReplayScenario.STRONG_EVIDENCE))
    timings = result.timings
    print(
        "[ap-002d7-perf] "
        f"total={timings.total_ms:.2f}ms "
        f"interpretation={timings.interpretation_ms:.2f}ms "
        f"decision={timings.decision_ms:.2f}ms "
        f"twin={timings.twin_ms:.2f}ms "
        f"projection={timings.projection_ms:.2f}ms "
        f"mission={timings.mission_ms:.2f}ms "
        f"explanation={timings.explanation_ms:.2f}ms"
    )
    assert timings.total_ms < PIPELINE_BUDGET_MS
    assert timings.interpretation_ms < STAGE_BUDGET_MS
    assert timings.decision_ms < STAGE_BUDGET_MS
    assert timings.projection_ms < STAGE_BUDGET_MS
    assert timings.mission_ms < STAGE_BUDGET_MS
    assert timings.explanation_ms < STAGE_BUDGET_MS
    assert result.certified


def test_replay_performance_baseline() -> None:
    harness = EducationalIntelligencePipelineHarness()
    fixture = build_fixture(ReplayScenario.DUPLICATE_SUBMISSION)
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
    print(
        "[ap-002d7-perf-replay] "
        f"first={first.timings.total_ms:.2f}ms "
        f"second={second.timings.total_ms:.2f}ms"
    )
    assert first.timings.total_ms < PIPELINE_BUDGET_MS
    assert second.timings.total_ms < PIPELINE_BUDGET_MS
    assert first.fingerprints == second.fingerprints
