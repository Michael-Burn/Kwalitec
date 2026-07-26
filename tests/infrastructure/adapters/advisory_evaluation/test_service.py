"""AdvisoryEvaluationService + feature-flag isolation tests (P2-MS012)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.advisory_evaluation import (
    DIFFERENCE_MULTI_FIELD,
    DIFFERENCE_RATIONALE_ANNOTATION,
    DIFFERENCE_UNCHANGED,
    AdvisoryEvaluationService,
    RecommendationComparison,
    build_advisory_evaluation_service,
    classify_difference_type,
)
from app.infrastructure.adapters.decision_simulation import (
    DecisionComparisonRecord,
    DecisionDifference,
    DecisionSimulationService,
    SimulatedRecommendation,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status


def _production() -> dict:
    return {
        "title": "Review weakest topic: Algebra",
        "category": "Weak Topic",
        "priority": "High",
        "reason": "Observed weak coverage on Algebra.",
        "expected_benefit": "Strengthen estimated knowledge.",
        "student_id": "should-be-stripped",
    }


def _simulation_record(*, with_advisory: bool = True) -> DecisionComparisonRecord:
    service = DecisionSimulationService(enabled=True)
    context = service.build_context(
        production_recommendation=_production(),
        evidence_advisory=(
            {"advisory_id": "evadv-9"} if with_advisory else None
        ),
        recovery_candidates=(
            ({"candidate_id": "rcv-cand-9", "advisory_only": True},)
            if with_advisory
            else ()
        ),
        student_id="7",
        generated_at="2026-08-07T12:00:00+00:00",
    )
    result = service.simulate(context)
    assert result.ok and result.comparison is not None
    return result.comparison


def test_advisory_evaluation_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_ADVISORY_EVALUATION is False
    dual = build_dual_run_status(flags=flags)
    assert dual.advisory_evaluation is False


def test_advisory_evaluation_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_ADVISORY_EVALUATION": "1"}
    )
    assert flags.ENABLE_ADVISORY_EVALUATION is True
    dual = build_dual_run_status(flags=flags)
    assert dual.advisory_evaluation is True


def test_flag_isolation_from_all_prior_flags():
    evaluation_only = resolve_v2_feature_flags(
        environ={"KWALITEC_ADVISORY_EVALUATION": "1"}
    )
    assert evaluation_only.ENABLE_ADVISORY_EVALUATION is True
    assert evaluation_only.ENABLE_DECISION_SIMULATION is False
    assert evaluation_only.ENABLE_RECOVERY_PLANNER is False
    assert evaluation_only.ENABLE_EVIDENCE_ADVISORY is False
    assert evaluation_only.ENABLE_EXPERIENCE_FEEDBACK is False
    assert evaluation_only.ENABLE_EVIDENCE_PLATFORM is False
    assert evaluation_only.ENABLE_STRATEGY_ENGINE is False
    assert evaluation_only.ENABLE_ADAPTIVE_ENGINE is False

    others_only = resolve_v2_feature_flags(
        environ={
            "KWALITEC_DECISION_SIMULATION": "1",
            "KWALITEC_RECOVERY_PLANNER": "1",
            "KWALITEC_EVIDENCE_ADVISORY": "1",
            "KWALITEC_EXPERIENCE_FEEDBACK": "1",
            "KWALITEC_EVIDENCE_PLATFORM": "1",
            "KWALITEC_STRATEGY_ENGINE": "1",
            "KWALITEC_ADAPTIVE_ENGINE": "1",
        }
    )
    assert others_only.ENABLE_ADVISORY_EVALUATION is False


def test_classify_difference_type_taxonomy():
    assert classify_difference_type(differs=False) == DIFFERENCE_UNCHANGED
    assert (
        classify_difference_type(differs=True, field_names=("rationale",))
        == DIFFERENCE_RATIONALE_ANNOTATION
    )
    assert (
        classify_difference_type(differs=True, field_names=("priority", "title"))
        == DIFFERENCE_MULTI_FIELD
    )


def test_ingest_simulation_builds_comparison_without_student_id():
    service = AdvisoryEvaluationService(enabled=True)
    record = _simulation_record(with_advisory=True)
    result = service.ingest_simulation(record)
    assert result.ok is True
    comparison = result.comparison
    assert isinstance(comparison, RecommendationComparison)
    assert comparison.operational_only is True
    assert comparison.differs is True
    assert comparison.difference_type == DIFFERENCE_RATIONALE_ANNOTATION
    assert "evidence_advisory" in comparison.advisory_sources
    assert "student_id" not in comparison.to_canonical_dict()
    assert "student_id" not in comparison.production_recommendation
    assert "student_id" not in comparison.simulated_recommendation


def test_aggregate_metrics_from_mixed_cohort():
    service = AdvisoryEvaluationService(enabled=True)
    with_adv = service.ingest_simulation(_simulation_record(with_advisory=True))
    without = service.ingest_simulation(_simulation_record(with_advisory=False))
    assert with_adv.ok and without.ok
    metrics_result = service.aggregate_metrics(
        generated_at="2026-08-07T12:00:00+00:00"
    )
    assert metrics_result.ok is True
    metrics = metrics_result.metrics
    assert metrics is not None
    assert metrics.comparison_count == 2
    assert metrics.difference_rate == 1.0
    assert metrics.unchanged_rate == 0.0
    assert metrics.advisory_usage_frequency == 0.5
    assert metrics.explainability_completeness == 1.0
    assert metrics.operational_only is True
    assert metrics.difference_type_counts[DIFFERENCE_RATIONALE_ANNOTATION] == 2


def test_generate_export_contains_rationales_provenance_explanation():
    service = AdvisoryEvaluationService(enabled=True)
    ingest = service.ingest_simulation(_simulation_record(with_advisory=True))
    assert ingest.comparison is not None
    export_result = service.generate_export(ingest.comparison)
    assert export_result.ok is True
    export = export_result.export
    assert export is not None
    assert export.review_only is True
    assert export.student_facing is False
    assert export.production_rationale
    assert export.simulated_rationale
    assert export.provenance
    assert export.explanation
    assert "review" in export.explanation.lower() or "authoritative" in (
        export.explanation.lower()
    )


def test_generate_summary_includes_metrics_and_exports():
    service = AdvisoryEvaluationService(enabled=True)
    summary_result = service.evaluate_simulation_batch(
        (
            _simulation_record(with_advisory=True),
            _simulation_record(with_advisory=False),
        ),
        include_exports=True,
        generated_at="2026-08-07T12:00:00+00:00",
    )
    assert summary_result.ok is True
    summary = summary_result.summary
    assert summary is not None
    assert summary.metrics is not None
    assert summary.metrics.comparison_count == 2
    assert len(summary.comparisons) == 2
    assert len(summary.exports) == 2
    assert summary.operational_only is True
    assert any("Runtime A" in note for note in summary.notes)


def test_evaluation_is_deterministic():
    service = AdvisoryEvaluationService(enabled=True)
    record = DecisionComparisonRecord(
        comparison_id="simcmp-fixed",
        simulation_id="sim-fixed",
        recommendation_id="rec-fixed",
        production_recommendation=_production(),
        simulated_recommendation=SimulatedRecommendation(
            simulation_id="sim-fixed",
            recommendation_id="rec-fixed",
            simulated_priority="High",
            simulated_title="Review weakest topic: Algebra",
            simulated_rationale="Annotated rationale",
            advisory_sources=("evidence_advisory",),
            differs_from_runtime=True,
            provenance={"mode": "structural_mirror_with_advisory_annotation"},
            simulation_only=True,
            student_id="7",
        ),
        differences=(
            DecisionDifference(
                field_name="rationale",
                production_value="Observed weak coverage on Algebra.",
                simulated_value="Annotated rationale",
                explanation="Advisory annotation only.",
            ),
        ),
        advisory_sources_considered=("evidence_advisory",),
        provenance={"operational_only": True},
        generated_at="2026-08-07T12:00:00+00:00",
        student_id="7",
        operational_only=True,
    )
    first = service.ingest_simulation(record)
    service.clear_comparisons()
    second = service.ingest_simulation(record)
    assert first.ok and second.ok
    assert first.comparison is not None and second.comparison is not None
    assert first.comparison.serialize() == second.comparison.serialize()


def test_disabled_service_rejects():
    service = AdvisoryEvaluationService(enabled=False)
    result = service.ingest_simulation(_simulation_record())
    assert result.ok is False
    assert result.error_code == "UNAVAILABLE"
    assert service.aggregate_metrics().ok is False
    assert service.evaluate_simulation_batch((_simulation_record(),)).ok is False


def test_build_helper_respects_enabled_flag():
    assert build_advisory_evaluation_service(enabled=False) is None
    service = build_advisory_evaluation_service(enabled=True)
    assert isinstance(service, AdvisoryEvaluationService)
    assert service.is_enabled() is True


def test_composition_wires_advisory_evaluation_only_when_flag_on():
    composition_off, _ = build_production_experience(
        flags=resolve_v2_feature_flags(environ={})
    )
    assert composition_off.advisory_evaluation is None

    composition_on, _ = build_production_experience(
        flags=resolve_v2_feature_flags(
            environ={"KWALITEC_ADVISORY_EVALUATION": "1"}
        )
    )
    assert composition_on.advisory_evaluation is not None
    assert composition_on.advisory_evaluation.is_enabled() is True


def test_ingest_never_mutates_simulation_record():
    service = AdvisoryEvaluationService(enabled=True)
    record = _simulation_record(with_advisory=True)
    before = record.serialize()
    service.ingest_simulation(record)
    assert record.serialize() == before


def test_empty_cohort_metrics_are_zero():
    service = AdvisoryEvaluationService(enabled=True)
    result = service.aggregate_metrics(())
    assert result.ok is True
    metrics = result.metrics
    assert metrics is not None
    assert metrics.comparison_count == 0
    assert metrics.difference_rate == 0.0
    assert metrics.unchanged_rate == 0.0
    assert metrics.advisory_usage_frequency == 0.0
    assert metrics.explainability_completeness == 0.0
