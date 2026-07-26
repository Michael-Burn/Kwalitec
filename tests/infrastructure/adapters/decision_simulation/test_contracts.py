"""Decision Simulation DTO contract tests (P2-MS011)."""

from __future__ import annotations

import pytest

from app.infrastructure.adapters.decision_simulation.contracts import (
    AUTHORITY_DECISION_SIMULATION,
    SIMULATION_VERSION,
    DecisionComparisonRecord,
    DecisionDifference,
    DecisionSimulationContext,
    SimulatedRecommendation,
)


def test_decision_simulation_context_is_frozen():
    context = DecisionSimulationContext(
        simulation_id="sim-1",
        recommendation_id="rec-1",
        generated_at="2026-08-07T12:00:00+00:00",
        student_id="42",
    )
    with pytest.raises(Exception):
        context.simulation_id = "mutated"  # type: ignore[misc]


def test_decision_simulation_context_traceable_fields():
    context = DecisionSimulationContext(
        simulation_id="sim-1",
        recommendation_id="rec-1",
        evidence_advisory={
            "advisory_id": "evadv-1",
            "reporting_period": "this_week",
        },
        recovery_candidates=(
            {
                "candidate_id": "rcv-cand-1",
                "advisory_only": True,
            },
        ),
        runtime_inputs={
            "production_recommendation": {
                "title": "Review weakest topic",
                "priority": "High",
                "reason": "Observed weak coverage",
            }
        },
        generated_at="2026-08-07T12:00:00+00:00",
        student_id="42",
    )
    payload = context.to_canonical_dict()
    assert payload["simulation_id"] == "sim-1"
    assert payload["authority"] == AUTHORITY_DECISION_SIMULATION
    assert payload["simulation_version"] == SIMULATION_VERSION
    assert payload["evidence_advisory"]["advisory_id"] == "evadv-1"
    assert payload["recovery_candidates"][0]["candidate_id"] == "rcv-cand-1"
    assert "production_recommendation" in payload["runtime_inputs"]


def test_simulated_recommendation_forces_simulation_only():
    simulated = SimulatedRecommendation(
        simulation_id="sim-1",
        simulated_priority="High",
        simulated_rationale="Annotated",
        advisory_sources=("evidence_advisory",),
        differs_from_runtime=True,
        provenance={"source_service": "decision_simulation"},
        simulation_only=False,  # coerced to True
        recommendation_id="rec-1",
        simulated_title="Review weakest topic",
    )
    assert simulated.simulation_only is True
    with pytest.raises(Exception):
        simulated.simulation_id = "x"  # type: ignore[misc]
    assert simulated.to_canonical_dict()["simulation_only"] is True


def test_comparison_record_is_operational_only():
    simulated = SimulatedRecommendation(
        simulation_id="sim-1",
        simulated_priority="High",
        simulated_rationale="Annotated",
        recommendation_id="rec-1",
    )
    record = DecisionComparisonRecord(
        comparison_id="simcmp-1",
        simulation_id="sim-1",
        recommendation_id="rec-1",
        production_recommendation={"title": "A", "priority": "High"},
        simulated_recommendation=simulated,
        differences=(
            DecisionDifference(
                field_name="rationale",
                production_value="A",
                simulated_value="Annotated",
                explanation="Advisory annotation only.",
            ),
        ),
        advisory_sources_considered=("evidence_advisory",),
        operational_only=False,  # coerced to True
    )
    assert record.operational_only is True
    assert record.differences[0].field_name == "rationale"


def test_decision_difference_requires_field_name():
    with pytest.raises(ValueError, match="field_name"):
        DecisionDifference(field_name="")


def test_no_student_facing_authority_fields():
    forbidden = {
        "student_facing",
        "serve_to_student",
        "replace_production",
        "ranking_override",
    }
    assert set(SimulatedRecommendation.__dataclass_fields__).isdisjoint(forbidden)
    assert set(DecisionComparisonRecord.__dataclass_fields__).isdisjoint(forbidden)
