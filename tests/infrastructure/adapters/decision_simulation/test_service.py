"""DecisionSimulationService + feature-flag isolation tests (P2-MS011)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.decision_simulation import (
    DecisionSimulationContext,
    DecisionSimulationService,
    SimulatedRecommendation,
    build_decision_simulation_service,
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
    }


def test_decision_simulation_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_DECISION_SIMULATION is False
    dual = build_dual_run_status(flags=flags)
    assert dual.decision_simulation is False


def test_decision_simulation_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_DECISION_SIMULATION": "1"}
    )
    assert flags.ENABLE_DECISION_SIMULATION is True
    dual = build_dual_run_status(flags=flags)
    assert dual.decision_simulation is True


def test_flag_isolation_from_all_prior_flags():
    simulation_only = resolve_v2_feature_flags(
        environ={"KWALITEC_DECISION_SIMULATION": "1"}
    )
    assert simulation_only.ENABLE_DECISION_SIMULATION is True
    assert simulation_only.ENABLE_RECOVERY_PLANNER is False
    assert simulation_only.ENABLE_EVIDENCE_ADVISORY is False
    assert simulation_only.ENABLE_EXPERIENCE_FEEDBACK is False
    assert simulation_only.ENABLE_EVIDENCE_PLATFORM is False
    assert simulation_only.ENABLE_STRATEGY_ENGINE is False
    assert simulation_only.ENABLE_ADAPTIVE_ENGINE is False

    others_only = resolve_v2_feature_flags(
        environ={
            "KWALITEC_RECOVERY_PLANNER": "1",
            "KWALITEC_EVIDENCE_ADVISORY": "1",
            "KWALITEC_EXPERIENCE_FEEDBACK": "1",
            "KWALITEC_EVIDENCE_PLATFORM": "1",
            "KWALITEC_STRATEGY_ENGINE": "1",
            "KWALITEC_ADAPTIVE_ENGINE": "1",
        }
    )
    assert others_only.ENABLE_DECISION_SIMULATION is False


def test_simulate_mirrors_priority_and_annotates_advisory():
    service = DecisionSimulationService(enabled=True)
    context = service.build_context(
        production_recommendation=_production(),
        evidence_advisory={"advisory_id": "evadv-9"},
        recovery_candidates=(
            {"candidate_id": "rcv-cand-9", "advisory_only": True},
        ),
        student_id="7",
        generated_at="2026-08-07T12:00:00+00:00",
    )
    result = service.simulate(context)
    assert result.ok is True
    assert isinstance(result.simulated, SimulatedRecommendation)
    simulated = result.simulated
    assert simulated.simulation_only is True
    assert simulated.simulated_priority == "High"
    assert simulated.simulated_title == "Review weakest topic: Algebra"
    assert "evidence_advisory" in simulated.advisory_sources
    assert "recovery_candidate:rcv-cand-9" in simulated.advisory_sources
    assert "advisory sources considered" in simulated.simulated_rationale.lower()
    assert simulated.differs_from_runtime is True  # rationale annotation
    assert result.comparison is not None
    assert result.comparison.operational_only is True
    assert result.comparison.advisory_sources_considered
    assert any(d.field_name == "rationale" for d in result.comparison.differences)
    assert simulated.provenance["mode"] == "structural_mirror_with_advisory_annotation"


def test_simulate_without_advisory_still_simulation_only():
    service = DecisionSimulationService(enabled=True)
    context = service.build_context(
        production_recommendation=_production(),
        student_id="7",
    )
    result = service.simulate(context)
    assert result.ok is True
    assert result.simulated is not None
    assert result.simulated.simulation_only is True
    assert result.simulated.advisory_sources == ()
    assert "no advisory inputs" in result.simulated.simulated_rationale.lower()


def test_simulate_never_mutates_production_mapping():
    service = DecisionSimulationService(enabled=True)
    production = _production()
    original = dict(production)
    context = service.build_context(
        production_recommendation=production,
        evidence_advisory={"advisory_id": "evadv-1"},
        student_id="3",
    )
    service.simulate(context)
    assert production == original


def test_simulate_is_deterministic():
    service = DecisionSimulationService(enabled=True)
    context = DecisionSimulationContext(
        simulation_id="sim-fixed",
        recommendation_id="Review weakest topic: Algebra",
        evidence_advisory={"advisory_id": "evadv-1"},
        runtime_inputs={"production_recommendation": _production()},
        generated_at="2026-08-07T12:00:00+00:00",
        student_id="7",
    )
    first = service.simulate(context)
    second = service.simulate(context)
    assert first.ok and second.ok
    assert first.simulated is not None and second.simulated is not None
    assert first.simulated.serialize() == second.simulated.serialize()
    assert first.comparison is not None and second.comparison is not None
    assert first.comparison.serialize() == second.comparison.serialize()


def test_disabled_service_rejects():
    service = DecisionSimulationService(enabled=False)
    result = service.simulate(
        service.build_context(production_recommendation=_production())
    )
    assert result.ok is False
    assert result.error_code == "UNAVAILABLE"


def test_simulate_after_recommendations_preserves_input_list():
    service = DecisionSimulationService(enabled=True)
    recommendations = [_production()]
    snapshot = [dict(recommendations[0])]
    records = service.simulate_after_recommendations(
        student_id=11,
        production_recommendations=recommendations,
        evidence_advisory={"advisory_id": "evadv-2"},
    )
    assert len(records) == 1
    assert recommendations == snapshot
    assert records[0].simulated_recommendation is not None
    assert records[0].simulated_recommendation.simulation_only is True


def test_composition_wires_simulation_when_flag_on():
    flags_off = resolve_v2_feature_flags(environ={})
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.decision_simulation is None

    flags_on = resolve_v2_feature_flags(
        environ={"KWALITEC_DECISION_SIMULATION": "1"}
    )
    composition_on, _ = build_production_experience(flags=flags_on)
    assert isinstance(
        composition_on.decision_simulation, DecisionSimulationService
    )


def test_build_helper_respects_enabled_gate():
    assert build_decision_simulation_service(enabled=False) is None
    service = build_decision_simulation_service(enabled=True)
    assert isinstance(service, DecisionSimulationService)
