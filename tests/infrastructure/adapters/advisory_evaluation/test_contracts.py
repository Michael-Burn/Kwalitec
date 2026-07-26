"""Advisory Evaluation DTO contract tests (P2-MS012)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.advisory_evaluation.contracts import (
    AUTHORITY_ADVISORY_EVALUATION,
    DIFFERENCE_RATIONALE_ANNOTATION,
    DIFFERENCE_UNCHANGED,
    EVALUATION_VERSION,
    DomainReviewExport,
    EvaluationMetrics,
    EvaluationSummary,
    RecommendationComparison,
)


def test_recommendation_comparison_is_frozen():
    comparison = RecommendationComparison(
        comparison_id="adveval-1",
        production_recommendation={"title": "A", "priority": "High"},
        simulated_recommendation={"title": "A", "priority": "High"},
        differs=False,
        difference_type=DIFFERENCE_UNCHANGED,
        generated_at="2026-08-07T12:00:00+00:00",
    )
    with pytest.raises(Exception):
        comparison.comparison_id = "mutated"  # type: ignore[misc]


def test_recommendation_comparison_has_no_student_identifier_field():
    comparison = RecommendationComparison(
        comparison_id="adveval-1",
        production_recommendation={"title": "A", "student_id": "should-remain-in-map"},
        differs=False,
    )
    payload = comparison.to_canonical_dict()
    assert "student_id" not in payload
    assert payload["authority"] == AUTHORITY_ADVISORY_EVALUATION
    assert payload["evaluation_version"] == EVALUATION_VERSION
    assert payload["operational_only"] is True


def test_recommendation_comparison_coerces_differs_false_to_unchanged():
    comparison = RecommendationComparison(
        comparison_id="adveval-1",
        differs=False,
        difference_type=DIFFERENCE_RATIONALE_ANNOTATION,
    )
    assert comparison.difference_type == DIFFERENCE_UNCHANGED


def test_recommendation_comparison_coerces_differs_true_away_from_unchanged():
    comparison = RecommendationComparison(
        comparison_id="adveval-1",
        differs=True,
        difference_type=DIFFERENCE_UNCHANGED,
    )
    assert comparison.difference_type == "structural"


def test_evaluation_metrics_clamp_rates_and_freeze():
    metrics = EvaluationMetrics(
        comparison_count=10,
        difference_rate=1.5,
        unchanged_rate=-0.2,
        advisory_usage_frequency=0.4,
        explainability_completeness=0.9,
        difference_type_counts={"rationale_annotation": 4},
    )
    assert metrics.difference_rate == 1.0
    assert metrics.unchanged_rate == 0.0
    assert metrics.operational_only is True
    with pytest.raises(Exception):
        metrics.comparison_count = 99  # type: ignore[misc]
    payload = metrics.to_canonical_dict()
    assert payload["comparison_count"] == 10
    assert payload["advisory_usage_frequency"] == 0.4
    assert payload["difference_type_counts"]["rationale_annotation"] == 4


def test_domain_review_export_forces_review_only_not_student_facing():
    export = DomainReviewExport(
        export_id="advexp-1",
        comparison_id="adveval-1",
        production_rationale="Observed weak coverage.",
        simulated_rationale="Observed weak coverage. | advisory annotation",
        provenance={"source_service": "advisory_evaluation"},
        explanation="Rationale annotation only.",
        review_only=False,
        student_facing=True,
    )
    assert export.review_only is True
    assert export.student_facing is False
    payload = export.to_canonical_dict()
    assert payload["production_rationale"]
    assert payload["simulated_rationale"]
    assert payload["provenance"]["source_service"] == "advisory_evaluation"
    assert payload["explanation"]
    assert payload["student_facing"] is False


def test_evaluation_summary_requires_typed_collections():
    comparison = RecommendationComparison(comparison_id="adveval-1", differs=False)
    metrics = EvaluationMetrics(comparison_count=1, unchanged_rate=1.0)
    summary = EvaluationSummary(
        summary_id="advsum-1",
        metrics=metrics,
        comparisons=(comparison,),
        notes=("Operational only.",),
    )
    assert summary.operational_only is True
    assert summary.to_canonical_dict()["metrics"]["comparison_count"] == 1
    with pytest.raises(TypeError):
        EvaluationSummary(
            summary_id="bad",
            comparisons=("not-a-comparison",),  # type: ignore[arg-type]
        )
