"""Runtime A Decision Simulation integration tests (P2-MS011)."""

from __future__ import annotations

from app.infrastructure.adapters.decision_simulation import (
    DecisionSimulationService,
)
from app.services.recommendation_service import RecommendationService
from tests.conftest import _make_user


def test_recommendation_output_unchanged_with_simulation(ctx):
    user = _make_user()
    service = DecisionSimulationService(enabled=True)

    without = RecommendationService.generate_recommendations(user.id, limit=5)
    with_sim = RecommendationService.generate_recommendations(
        user.id, limit=5, simulation_service=service
    )
    assert without == with_sim
    # Simulation may produce zero comparisons when no recommendations exist,
    # but when recommendations exist they must remain identical.
    if with_sim:
        assert len(service.comparisons) >= 1
        for record in service.comparisons:
            assert record.operational_only is True
            assert record.simulated_recommendation is not None
            assert record.simulated_recommendation.simulation_only is True


def test_simulation_explainability_metadata_present(ctx):
    user = _make_user()
    service = DecisionSimulationService(enabled=True)
    production = {
        "title": "Clear your review backlog",
        "category": "Review",
        "priority": "Critical",
        "reason": "Overdue reviews.",
    }
    records = service.simulate_after_recommendations(
        student_id=user.id,
        production_recommendations=[production],
        evidence_advisory={
            "advisory_id": "evadv-meta",
            "source_description": "Derived from recorded study activity.",
        },
        recovery_candidates=(
            {
                "candidate_id": "rcv-cand-meta",
                "advisory_only": True,
                "rationale": "Structural placeholder",
            },
        ),
        generated_at="2026-08-07T12:00:00+00:00",
    )
    assert len(records) == 1
    record = records[0]
    assert "evidence_advisory" in record.advisory_sources_considered
    assert any(
        item.startswith("recovery_candidate:")
        for item in record.advisory_sources_considered
    )
    simulated = record.simulated_recommendation
    assert simulated is not None
    assert simulated.simulation_only is True
    assert simulated.provenance["authority_chain"]["production"] == "runtime_a"
    assert simulated.provenance["authority_chain"]["simulation"] == (
        "decision_simulation"
    )
    assert any(d.explanation for d in record.differences)
    # Production mapping untouched.
    assert production["reason"] == "Overdue reviews."
