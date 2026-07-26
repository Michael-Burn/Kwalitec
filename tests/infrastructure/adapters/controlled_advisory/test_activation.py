"""Controlled Advisory Activation + Runtime A integration tests (P3-MS001)."""

from __future__ import annotations

from datetime import UTC, datetime

from app.infrastructure.adapters.controlled_advisory import (
    ACTIVATION_KEY,
    REASON_FLAG_OFF,
    REASON_ROLLOUT_EXCLUDED,
    ControlledAdvisoryActivation,
    build_default_advisory_policy,
)
from app.infrastructure.adapters.decision_simulation import (
    DecisionSimulationService,
)
from app.infrastructure.adapters.evidence_platform.contracts import (
    ConsistencySummary,
    EngagementSummary,
    EvidenceAdvisory,
)
from app.services.recommendation_service import RecommendationService
from tests.conftest import _make_user


def _advisory(*, generated_at: str, streak: int = 4) -> EvidenceAdvisory:
    return EvidenceAdvisory(
        advisory_id="evadv-activation",
        student_id="1",
        consistency_summary=ConsistencySummary(
            active_streak=streak,
            source_description="Derived from recorded study activity.",
        ),
        engagement_summary=EngagementSummary(),
        generated_at=generated_at,
        evidence_summary_id="evsum-activation",
        availability="available",
    )


class _StubAdvisoryInjection:
    def __init__(self, advisory: EvidenceAdvisory | None) -> None:
        self.last_advisory = advisory
        self.last_consideration = None

    def prepare_for_recommendation(self, user_id):  # noqa: ANN001
        return None


def test_activation_annotates_reason_when_allowed():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    activation = ControlledAdvisoryActivation(
        enabled=True,
        policy=build_default_advisory_policy(rollout_percentage=100),
        now=now,
    )
    production = [
        {
            "title": "Clear your review backlog",
            "category": "Review",
            "priority": "Critical",
            "reason": "Overdue reviews.",
        }
    ]
    advisory = _advisory(generated_at="2026-07-24T12:00:00+00:00")
    result = activation.apply_to_recommendations(
        "7", production, advisory=advisory
    )
    assert production[0]["reason"] == "Overdue reviews."  # input untouched
    assert "consistency_summary" in result[0]["reason"]
    assert "active streak of 4" in result[0]["reason"]
    assert result[0][ACTIVATION_KEY]["activated"] is True
    assert result[0][ACTIVATION_KEY]["advisory_field_used"] == "consistency_summary"
    assert result[0][ACTIVATION_KEY]["policy_version"]
    assert result[0][ACTIVATION_KEY]["activation_reason"]
    assert result[0][ACTIVATION_KEY]["evidence_provenance"]["advisory_id"] == (
        "evadv-activation"
    )
    # Minimal influence — ranking fields unchanged.
    assert result[0]["priority"] == "Critical"
    assert result[0]["title"] == "Clear your review backlog"


def test_activation_records_rejection_reason():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    activation = ControlledAdvisoryActivation(
        enabled=True,
        policy=build_default_advisory_policy(rollout_percentage=0),
        now=now,
    )
    production = [
        {
            "title": "Clear your review backlog",
            "category": "Review",
            "priority": "Critical",
            "reason": "Overdue reviews.",
        }
    ]
    result = activation.apply_to_recommendations(
        "7",
        production,
        advisory=_advisory(generated_at="2026-07-24T12:00:00+00:00"),
    )
    assert result[0]["reason"] == "Overdue reviews."
    assert result[0][ACTIVATION_KEY]["activated"] is False
    assert result[0][ACTIVATION_KEY]["rejection_reason"] == REASON_ROLLOUT_EXCLUDED


def test_rollback_when_flag_disabled_leaves_output_unchanged():
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    activation = ControlledAdvisoryActivation(
        enabled=False,
        policy=build_default_advisory_policy(rollout_percentage=100),
        now=now,
    )
    production = [
        {
            "title": "Clear your review backlog",
            "category": "Review",
            "priority": "Critical",
            "reason": "Overdue reviews.",
        }
    ]
    result = activation.apply_to_recommendations(
        "7",
        production,
        advisory=_advisory(generated_at="2026-07-24T12:00:00+00:00"),
    )
    assert result == production
    assert ACTIVATION_KEY not in result[0]
    decision = activation.evaluate(
        "7", advisory=_advisory(generated_at="2026-07-24T12:00:00+00:00")
    )
    assert decision.reason == REASON_FLAG_OFF


def test_recommendation_service_applies_controlled_advisory(ctx):
    user = _make_user()
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    activation = ControlledAdvisoryActivation(
        enabled=True,
        policy=build_default_advisory_policy(rollout_percentage=100),
        now=now,
    )
    advisory = _advisory(generated_at="2026-07-24T12:00:00+00:00")
    injection = _StubAdvisoryInjection(advisory)

    baseline = RecommendationService.generate_recommendations(user.id, limit=5)
    activated = RecommendationService.generate_recommendations(
        user.id,
        limit=5,
        advisory_injection=injection,
        controlled_advisory=activation,
    )
    assert activation.last_decision is not None
    assert activation.last_decision.allowed is True
    if activated:
        assert activated[0][ACTIVATION_KEY]["activated"] is True
        assert "consistency_summary" in activated[0]["reason"]
        # Titles / priorities remain the production ranking.
        assert [r["title"] for r in activated] == [r["title"] for r in baseline]
        assert [r["priority"] for r in activated] == [
            r["priority"] for r in baseline
        ]


def test_simulation_comparison_remains_available(ctx):
    user = _make_user()
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    activation = ControlledAdvisoryActivation(
        enabled=True,
        policy=build_default_advisory_policy(rollout_percentage=100),
        now=now,
    )
    advisory = _advisory(generated_at="2026-07-24T12:00:00+00:00")
    injection = _StubAdvisoryInjection(advisory)
    simulation = DecisionSimulationService(enabled=True)

    production = RecommendationService.generate_recommendations(
        user.id,
        limit=5,
        advisory_injection=injection,
        controlled_advisory=activation,
        simulation_service=simulation,
    )
    if production:
        assert len(simulation.comparisons) >= 1
        record = simulation.comparisons[0]
        assert record.operational_only is True
        assert record.simulated_recommendation is not None
        assert record.simulated_recommendation.simulation_only is True
        # Policy-driven production carries activation explainability.
        assert production[0][ACTIVATION_KEY]["activated"] is True
        # Simulation still compares against the (possibly annotated) production.
        assert record.production_recommendation.get("title") == production[0]["title"]


def test_other_advisory_fields_ignored():
    """Only consistency_summary may influence; engagement is ignored."""
    now = datetime(2026, 7, 25, 12, 0, tzinfo=UTC)
    activation = ControlledAdvisoryActivation(
        enabled=True,
        policy=build_default_advisory_policy(rollout_percentage=100),
        now=now,
    )
    advisory = EvidenceAdvisory(
        advisory_id="evadv-other",
        student_id="7",
        consistency_summary=ConsistencySummary(active_streak=2),
        engagement_summary=EngagementSummary(
            completed_missions=99,
            study_sessions=99,
            completed_reflections=99,
            source_description="must not appear",
        ),
        generated_at="2026-07-24T12:00:00+00:00",
        evidence_summary_id="evsum-other",
        availability="available",
    )
    result = activation.apply_to_recommendations(
        "7",
        [{"title": "t", "category": "c", "priority": "High", "reason": "base"}],
        advisory=advisory,
    )
    assert "must not appear" not in result[0]["reason"]
    assert "consistency_summary" in result[0]["reason"]
    assert result[0][ACTIVATION_KEY]["advisory_field_used"] == "consistency_summary"
