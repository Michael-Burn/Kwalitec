"""Progress evaluation engine tests (EDU-003).

Covers: trend calculation, velocity calculation, regression detection,
intervention thresholds, determinism, and architecture purity.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from domain.education.digital_twin import RetentionBand
from domain.education.evidence import EvidenceItemKind
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.progress_evaluation import (
    InterventionUrgency,
    ProgressEvaluator,
    ProgressReport,
    RevisionEffectivenessBand,
    StabilityBand,
    TrendDirection,
    VelocityBand,
    active_misconception_threshold,
    trend_delta_threshold,
)
from tests.domain.education.digital_twin.conftest import make_archived_twin
from tests.domain.education.evidence.conftest import (
    make_item,
    make_record,
    make_timestamp,
)
from tests.domain.progress_evaluation.conftest import (
    evaluate_progress,
    make_completed_mission,
    make_evidence_batch,
    make_progress_twin,
)
from tests.domain.study_planning.conftest import make_availability, plan_study

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3] / "src" / "domain" / "progress_evaluation"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
        "alembic",
        "jinja2",
        "wtforms",
        "requests",
        "httpx",
        "celery",
        "redis",
        "boto3",
        "openai",
        "anthropic",
        "random",
        "secrets",
        "uuid",
        "matplotlib",
        "plotly",
        "seaborn",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "app.",
    "openai.",
    "anthropic.",
    "matplotlib.",
    "plotly.",
)


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_package_exports_required_types() -> None:
    from domain import progress_evaluation as package

    for name in (
        "ProgressReport",
        "ProgressMetric",
        "MasteryTrend",
        "ConfidenceTrend",
        "LearningVelocity",
        "RevisionEffectiveness",
        "InterventionSignal",
        "ProgressEvaluator",
        "CompletedMission",
    ):
        assert hasattr(package, name), name


@pytest.mark.parametrize(
    "path",
    sorted(PACKAGE_ROOT.glob("*.py")),
    ids=lambda p: p.name,
)
def test_no_forbidden_infrastructure_or_ai_imports(path: Path) -> None:
    imported = _imported_modules(path)
    for name in imported:
        assert name not in FORBIDDEN_MODULES, f"{path.name} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in FORBIDDEN_PREFIXES
        ), f"{path.name} imports {name}"


def test_evaluator_source_has_no_randomness_or_visualization() -> None:
    source = (PACKAGE_ROOT / "progress_evaluator.py").read_text(encoding="utf-8")
    for token in (
        "import random",
        "from random",
        "import uuid",
        "from uuid",
        "import secrets",
        "from secrets",
        "datetime.now",
        "time.time",
        "matplotlib",
        "plotly",
        "seaborn",
    ):
        assert token not in source


def test_evaluate_returns_complete_progress_report() -> None:
    report = evaluate_progress()

    assert isinstance(report, ProgressReport)
    assert report.student_id == "student-ada"
    assert report.twin_id.value == "twin-001"
    assert report.mastery_trend.sample_size >= 1
    assert report.learning_velocity.window_days >= 1
    assert report.knowledge_stability in {
        StabilityBand.STABLE,
        StabilityBand.DURABLE,
        StabilityBand.FRAGILE,
        StabilityBand.UNSTABLE,
        StabilityBand.UNKNOWN,
    }
    assert report.confidence_level is ConfidenceLevel.MEDIUM
    assert len(report.metrics) >= 7
    assert "Progress report for student" in report.educational_explanation
    assert report.intervention_required == report.intervention_signal.required


def test_evaluate_rejects_student_mismatch_on_evidence() -> None:
    twin = make_progress_twin()
    evidence = make_evidence_batch(student_id="student-other")
    with pytest.raises(EducationalInvariantViolation, match="student_id"):
        ProgressEvaluator.evaluate(
            twin,
            evidence,
            (make_completed_mission(),),
            (plan_study(),),
        )


def test_evaluate_rejects_archived_twin() -> None:
    twin = make_archived_twin()
    with pytest.raises(EducationalInvariantViolation, match="archived"):
        ProgressEvaluator.evaluate(
            twin,
            make_evidence_batch(),
            (make_completed_mission(),),
            (plan_study(),),
        )


def test_evaluate_rejects_duplicate_missions() -> None:
    twin = make_progress_twin()
    mission = make_completed_mission()
    with pytest.raises(EducationalInvariantViolation, match="unique"):
        ProgressEvaluator.evaluate(
            twin,
            make_evidence_batch(),
            (mission, mission),
            (plan_study(),),
        )


# --- trend calculation ------------------------------------------------------


def test_mastery_trend_improving_when_later_evidence_stronger() -> None:
    evidence = make_evidence_batch(
        strengths=("weak", "weak", "very_strong", "very_strong")
    )
    report = evaluate_progress(evidence=evidence, completed_missions=())

    assert report.mastery_trend.direction is TrendDirection.IMPROVING
    assert report.mastery_trend.delta_millipoints >= trend_delta_threshold()
    assert not report.mastery_trend.regression_detected


def test_mastery_trend_stable_within_threshold() -> None:
    evidence = make_evidence_batch(
        strengths=("strong", "strong", "strong", "strong")
    )
    report = evaluate_progress(evidence=evidence, completed_missions=())

    assert report.mastery_trend.direction is TrendDirection.STABLE
    assert abs(report.mastery_trend.delta_millipoints) < trend_delta_threshold()


def test_mastery_trend_insufficient_data_with_single_signal() -> None:
    evidence = make_evidence_batch(strengths=("strong",))
    report = evaluate_progress(evidence=evidence, completed_missions=())

    assert report.mastery_trend.direction is TrendDirection.INSUFFICIENT_DATA
    assert report.mastery_trend.delta_millipoints == 0


def test_confidence_trend_improving_from_evidence_confidence() -> None:
    from domain.education.evidence import ConfidenceMeasure
    from tests.domain.education.evidence.conftest import make_strength

    low = make_record(
        evidence_id="evidence-low",
        confidence=ConfidenceMeasure.of(ConfidenceLevel.LOW, ratio=0.25),
        strength=make_strength(level="weak"),
        timestamp=make_timestamp(day=1),
    )
    high = make_record(
        evidence_id="evidence-high",
        confidence=ConfidenceMeasure.of(ConfidenceLevel.VERY_HIGH, ratio=0.95),
        strength=make_strength(level="very_strong"),
        timestamp=make_timestamp(day=2),
    )
    report = evaluate_progress(
        evidence=(low, high),
        completed_missions=(),
    )
    assert report.confidence_trend.direction is TrendDirection.IMPROVING
    assert report.confidence_trend.delta_millipoints >= trend_delta_threshold()


# --- velocity calculation ---------------------------------------------------


def test_learning_velocity_uses_evidence_window_days() -> None:
    evidence = make_evidence_batch(
        strengths=("moderate", "moderate", "moderate", "moderate"),
        start_day=1,
    )
    report = evaluate_progress(evidence=evidence, completed_missions=())

    assert report.learning_velocity.window_days == 4
    assert report.learning_velocity.events_per_day_millipoints == 1000
    assert report.learning_velocity.band is VelocityBand.MODERATE


def test_learning_velocity_fast_for_dense_same_day_burst() -> None:
    evidence = (
        make_record(
            evidence_id="evidence-a",
            timestamp=make_timestamp(day=5, hour=9),
        ),
        make_record(
            evidence_id="evidence-b",
            items=[make_item(item_id="item-b")],
            timestamp=make_timestamp(day=5, hour=10),
        ),
        make_record(
            evidence_id="evidence-c",
            items=[make_item(item_id="item-c")],
            timestamp=make_timestamp(day=5, hour=11),
        ),
    )
    report = evaluate_progress(evidence=evidence, completed_missions=())

    assert report.learning_velocity.window_days == 1
    assert report.learning_velocity.events_per_day_millipoints == 3000
    assert report.learning_velocity.band is VelocityBand.FAST


def test_learning_velocity_unknown_without_evidence() -> None:
    report = evaluate_progress(
        evidence=(),
        completed_missions=(make_completed_mission(),),
    )
    assert report.learning_velocity.band is VelocityBand.UNKNOWN
    assert report.learning_velocity.window_days == 0
    assert report.learning_velocity.missions_completed == 1


# --- regression detection ---------------------------------------------------


def test_regression_detected_when_mastery_declines() -> None:
    evidence = make_evidence_batch(
        strengths=("very_strong", "very_strong", "weak", "weak")
    )
    report = evaluate_progress(evidence=evidence, completed_missions=())

    assert report.mastery_trend.direction is TrendDirection.DECLINING
    assert report.mastery_trend.regression_detected is True
    assert report.mastery_trend.delta_millipoints <= -trend_delta_threshold()


def test_regression_triggers_critical_intervention() -> None:
    evidence = make_evidence_batch(
        strengths=("very_strong", "very_strong", "weak", "weak")
    )
    report = evaluate_progress(evidence=evidence, completed_missions=())

    assert report.intervention_signal.required is True
    assert report.intervention_signal.urgency is InterventionUrgency.CRITICAL
    assert any(
        "mastery_regression" in reason
        for reason in report.intervention_signal.reasons
    )


# --- intervention thresholds ------------------------------------------------


def test_active_misconception_triggers_elevated_intervention() -> None:
    twin = make_progress_twin(with_misconception=True)
    evidence = make_evidence_batch(strengths=("strong", "strong"))
    report = evaluate_progress(
        twin=twin,
        evidence=evidence,
        completed_missions=(),
    )

    assert active_misconception_threshold() == 1
    assert report.intervention_signal.required is True
    assert report.intervention_signal.urgency in {
        InterventionUrgency.ELEVATED,
        InterventionUrgency.CRITICAL,
    }
    assert any(
        reason.startswith("active_misconceptions:")
        for reason in report.intervention_signal.reasons
    )


def test_fading_retention_marks_unstable_and_intervention() -> None:
    twin = make_progress_twin(retention_band=RetentionBand.FADING)
    evidence = make_evidence_batch(strengths=("strong", "strong"))
    report = evaluate_progress(
        twin=twin,
        evidence=evidence,
        completed_missions=(),
        study_plans=(plan_study(),),
    )

    assert report.knowledge_stability is StabilityBand.UNSTABLE
    assert report.intervention_signal.required is True
    assert "knowledge_unstable" in report.intervention_signal.reasons
    assert (
        report.revision_effectiveness.band
        is RevisionEffectivenessBand.INEFFECTIVE
    )


def test_low_confidence_triggers_advisory_intervention() -> None:
    twin = make_progress_twin(confidence_level=ConfidenceLevel.LOW)
    evidence = make_evidence_batch(strengths=("strong", "strong"))
    report = evaluate_progress(
        twin=twin,
        evidence=evidence,
        completed_missions=(),
    )

    assert report.confidence_level is ConfidenceLevel.LOW
    assert report.intervention_signal.required is True
    assert report.intervention_signal.urgency in {
        InterventionUrgency.ADVISORY,
        InterventionUrgency.ELEVATED,
        InterventionUrgency.CRITICAL,
    }
    assert any(
        reason.startswith("low_confidence:")
        for reason in report.intervention_signal.reasons
    )


def test_healthy_progress_requires_no_intervention() -> None:
    twin = make_progress_twin(
        retention_band=RetentionBand.DURABLE,
        confidence_level=ConfidenceLevel.HIGH,
    )
    evidence = make_evidence_batch(
        strengths=("moderate", "strong", "strong", "very_strong")
    )
    report = evaluate_progress(
        twin=twin,
        evidence=evidence,
        completed_missions=(make_completed_mission(),),
    )

    assert report.mastery_trend.direction in {
        TrendDirection.IMPROVING,
        TrendDirection.STABLE,
    }
    assert report.intervention_signal.required is False
    assert report.intervention_signal.urgency is InterventionUrgency.NONE
    assert report.intervention_signal.reasons == ()


def test_revision_effectiveness_inapplicable_without_reviews() -> None:
    twin = make_progress_twin(retention_band=RetentionBand.STABLE)
    report = evaluate_progress(
        twin=twin,
        evidence=make_evidence_batch(strengths=("strong", "strong")),
        completed_missions=(),
        study_plans=(),
    )
    assert report.revision_effectiveness.band is (
        RevisionEffectivenessBand.INAPPLICABLE
    )
    assert report.revision_effectiveness.review_session_count == 0


def test_revision_effectiveness_counts_retrieval_probes() -> None:
    evidence = make_evidence_batch(
        strengths=("strong", "strong"),
        kind=EvidenceItemKind.RETRIEVAL_ATTEMPT,
    )
    report = evaluate_progress(
        evidence=evidence,
        completed_missions=(),
        study_plans=(plan_study(),),
    )
    assert report.revision_effectiveness.retention_probe_count == 2
    assert report.revision_effectiveness.review_session_count >= 1


# --- determinism ------------------------------------------------------------


def test_same_inputs_always_generate_same_report() -> None:
    twin = make_progress_twin()
    evidence = make_evidence_batch(
        strengths=("weak", "moderate", "strong", "very_strong")
    )
    missions = (make_completed_mission(),)
    plans = (plan_study(availability=make_availability(day_count=12)),)

    first = ProgressEvaluator.evaluate(twin, evidence, missions, plans)
    second = ProgressEvaluator.evaluate(twin, evidence, missions, plans)

    assert first == second
    assert first.report_id == second.report_id
    assert first.mastery_trend == second.mastery_trend
    assert first.learning_velocity == second.learning_velocity
    assert first.intervention_signal == second.intervention_signal
    assert first.educational_explanation == second.educational_explanation


def test_repeated_evaluation_is_stable_across_many_runs() -> None:
    twin = make_progress_twin(with_misconception=True)
    evidence = make_evidence_batch(
        strengths=("very_strong", "strong", "moderate", "weak")
    )
    missions = (
        make_completed_mission(mission_id="mission-a", completion_sequence=1),
        make_completed_mission(
            mission_id="mission-b",
            completion_sequence=2,
            outcome_millipoints=700,
        ),
    )
    plans = (plan_study(),)
    reports = [
        ProgressEvaluator.evaluate(twin, evidence, missions, plans)
        for _ in range(20)
    ]
    assert all(report == reports[0] for report in reports)


def test_report_id_is_deterministic_from_inputs() -> None:
    report = evaluate_progress()
    assert report.report_id.value.startswith("progress-twin-001-")


def test_evidence_order_does_not_change_result() -> None:
    twin = make_progress_twin()
    evidence = make_evidence_batch(
        strengths=("weak", "moderate", "strong", "very_strong")
    )
    reversed_evidence = tuple(reversed(evidence))
    missions = (make_completed_mission(),)
    plans = (plan_study(),)

    first = ProgressEvaluator.evaluate(twin, evidence, missions, plans)
    second = ProgressEvaluator.evaluate(twin, reversed_evidence, missions, plans)

    assert first.mastery_trend == second.mastery_trend
    assert first.learning_velocity == second.learning_velocity
    assert first.report_id == second.report_id
