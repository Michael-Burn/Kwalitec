"""EP-002.5 Study Insights gated HTTP cutover tests.

Covers cutover eligibility, fail-open fallback, alignment, feature flags,
regression (bridges still legacy), and dashboard HTTP integration.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.consumer_chain import (
    assess_semantic_alignment,
    build_consumer_chain_telemetry,
    build_study_insights_cutover_health_metrics,
    has_blocking_limitation,
    is_study_insights_cutover_eligible,
    project_study_insights_to_recommendations,
    run_study_insights_http_cutover,
    set_consumer_chain_telemetry,
    set_study_insights_cutover_health_metrics,
)
from app.infrastructure.adapters.consumer_chain.cutover import (
    ALIGNMENT_ALIGNED,
    ALIGNMENT_LIMITATION_FALLBACK,
    ALIGNMENT_MISMATCHED,
    ALIGNMENT_TWIN_UNAVAILABLE,
    FALLBACK_BLOCKING_LIMITATION,
    FALLBACK_CUTOVER_FLAG_OFF,
    FALLBACK_PRODUCTION_ENV,
    FALLBACK_TWIN_EXCEPTION,
    FALLBACK_TWIN_OFF,
    FALLBACK_TWIN_UNAVAILABLE,
)
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import CONSUMER_CHAIN_CUTOVER
from app.services.recommendation_service import RecommendationService


@pytest.fixture
def telemetry():
    sink = build_consumer_chain_telemetry(
        structured=StructuredLogger("test.consumer_chain.cutover"),
        events=EventRegistry(),
    )
    previous = set_consumer_chain_telemetry(sink)
    yield sink
    set_consumer_chain_telemetry(previous)


@pytest.fixture
def cutover_metrics():
    metrics = build_study_insights_cutover_health_metrics()
    previous = set_study_insights_cutover_health_metrics(metrics)
    yield metrics
    set_study_insights_cutover_health_metrics(previous)


def _eligible_environ(**extra: str) -> dict[str, str]:
    env = {
        "KWALITEC_DIGITAL_TWIN": "1",
        "KWALITEC_DIGITAL_TWIN_AUTHORITY": "0",
        "KWALITEC_STUDY_INSIGHTS_CUTOVER": "1",
        "APP_ENV": "development",
        "FLASK_ENV": "development",
    }
    env.update(extra)
    return env


def _legacy_rows() -> list[dict[str, Any]]:
    return [
        {
            "title": "Review Fractions",
            "category": "Review",
            "priority": "High",
            "reason": "Due for review on Fractions",
            "expected_benefit": "Keep retention",
        },
        {
            "title": "Strengthen Algebra",
            "category": "Weak Topic",
            "priority": "Critical",
            "reason": "Low mastery Algebra",
            "expected_benefit": "Improve score",
        },
    ]


def _twin_payload(*, topic_id: str = "Fractions") -> dict[str, Any]:
    return {
        "todays_key_focus": {
            "field_id": "todays_key_focus",
            "title": "Focus on Fractions",
            "message": "Spend today's session on Fractions.",
            "topic_id": topic_id,
            "source": "readiness_intelligence",
        },
        "recommended_next_action": {
            "field_id": "recommended_next_action",
            "title": "Practise Fractions",
            "message": "Complete a short Fractions practice set.",
            "topic_id": topic_id,
            "source": "readiness_intelligence",
        },
        "greatest_risk": {
            "field_id": "greatest_risk",
            "title": "Risk: Algebra drift",
            "message": "Algebra may fade without review.",
            "topic_id": "Algebra",
            "source": "readiness_intelligence",
        },
        "strongest_area": None,
        "workload_explanation": None,
        "readiness_explanation": None,
        "motivational_progress_summary": None,
        "limitations_codes": ["sparse_evidence"],
        "confidence_level": "medium",
    }


# ── Feature flags ──────────────────────────────────────────────────────────


def test_cutover_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_STUDY_INSIGHTS_CUTOVER is False


def test_cutover_flag_requires_twin():
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_STUDY_INSIGHTS_CUTOVER": "1",
            "KWALITEC_DIGITAL_TWIN": "0",
        }
    )
    assert flags.ENABLE_DIGITAL_TWIN is False
    assert flags.ENABLE_STUDY_INSIGHTS_CUTOVER is False


def test_cutover_flag_on_with_twin():
    flags = resolve_v2_feature_flags(environ=_eligible_environ())
    assert flags.ENABLE_DIGITAL_TWIN is True
    assert flags.ENABLE_STUDY_INSIGHTS_CUTOVER is True


@pytest.mark.parametrize(
    ("environ", "expected"),
    [
        (_eligible_environ(), True),
        (_eligible_environ(KWALITEC_DIGITAL_TWIN="0"), False),
        (_eligible_environ(KWALITEC_STUDY_INSIGHTS_CUTOVER="0"), False),
        (_eligible_environ(APP_ENV="production"), False),
        (_eligible_environ(APP_ENV="prod"), False),
        (
            {
                "KWALITEC_DIGITAL_TWIN": "1",
                "KWALITEC_STUDY_INSIGHTS_CUTOVER": "1",
                "APP_ENV": "staging",
            },
            True,
        ),
    ],
)
def test_cutover_eligibility_matrix(environ: dict[str, str], expected: bool):
    assert is_study_insights_cutover_eligible(environ=environ) is expected


# ── Projection / blocking / alignment ───────────────────────────────────────


def test_project_study_insights_rows():
    rows = project_study_insights_to_recommendations(_twin_payload(), limit=5)
    assert rows
    assert rows[0]["source_authority"] == "study_insights"
    assert rows[0]["category"] == "Study Focus"
    assert rows[0]["topic_id"] == "Fractions"
    assert "sparse_evidence" in rows[0]["limitations_codes"]


def test_blocking_limitation_codes():
    assert has_blocking_limitation(
        {"todays_key_focus": None, "recommended_next_action": None}
    )
    assert has_blocking_limitation(
        {
            "todays_key_focus": {"title": "x", "message": "y"},
            "recommended_next_action": {"title": "a", "message": "b"},
            "limitations_codes": ["canonical_learner_state_unavailable"],
        }
    )
    assert not has_blocking_limitation(_twin_payload())


def test_alignment_aligned_on_topic_id():
    report = assess_semantic_alignment(
        legacy_recommendations=_legacy_rows(),
        twin_payload=_twin_payload(topic_id="Fractions"),
        served_twin=True,
        fallback_reason=None,
    )
    assert report["alignment_status"] == ALIGNMENT_ALIGNED


def test_alignment_mismatched_topic():
    twin = {
        "todays_key_focus": {
            "field_id": "todays_key_focus",
            "title": "Focus on Quantum Topology",
            "message": "Spend today's session on Quantum Topology.",
            "topic_id": "quantum-topology-zzz",
            "source": "readiness_intelligence",
        },
        "recommended_next_action": {
            "field_id": "recommended_next_action",
            "title": "Practise Quantum Topology",
            "message": "Complete a short Quantum Topology set.",
            "topic_id": "quantum-topology-zzz",
            "source": "readiness_intelligence",
        },
        "greatest_risk": None,
        "limitations_codes": [],
        "confidence_level": "medium",
    }
    report = assess_semantic_alignment(
        legacy_recommendations=_legacy_rows(),
        twin_payload=twin,
        served_twin=True,
        fallback_reason=None,
    )
    assert report["alignment_status"] == ALIGNMENT_MISMATCHED


def test_alignment_unavailable_and_limitation():
    unavailable = assess_semantic_alignment(
        legacy_recommendations=_legacy_rows(),
        twin_payload=None,
        served_twin=False,
        fallback_reason=FALLBACK_TWIN_UNAVAILABLE,
    )
    assert unavailable["alignment_status"] == ALIGNMENT_TWIN_UNAVAILABLE

    limited = assess_semantic_alignment(
        legacy_recommendations=_legacy_rows(),
        twin_payload={"limitations_codes": ["twin_foundation_flag_off"]},
        served_twin=False,
        fallback_reason=FALLBACK_BLOCKING_LIMITATION,
    )
    assert limited["alignment_status"] == ALIGNMENT_LIMITATION_FALLBACK


# ── Cutover orchestration ───────────────────────────────────────────────────


def test_cutover_emits_integration_event(telemetry, cutover_metrics):
    run_study_insights_http_cutover(
        11,
        limit=3,
        environ=_eligible_environ(),
        telemetry=telemetry,
        generate_recommendations=lambda user_id, limit=5: _legacy_rows(),
        build_study_insights=lambda user_id: _twin_payload(),
        skip_request_dedupe=True,
    )
    recorded = [
        event
        for event in telemetry._events.published()
        if event.event_type == CONSUMER_CHAIN_CUTOVER
    ]
    assert recorded
    assert cutover_metrics.snapshot().cutover_served_count == 1


def test_cutover_serves_twin_when_eligible(telemetry, cutover_metrics, ctx):
    legacy = _legacy_rows()
    twin = _twin_payload()
    result = run_study_insights_http_cutover(
        42,
        limit=5,
        environ=_eligible_environ(),
        telemetry=telemetry,
        generate_recommendations=lambda user_id, limit=5: legacy,
        build_study_insights=lambda user_id: twin,
        skip_request_dedupe=True,
    )
    assert result
    assert result[0]["source_authority"] == "study_insights"
    assert result[0]["title"] == "Focus on Fractions"
    snap = cutover_metrics.snapshot()
    assert snap.eligible_requests == 1
    assert snap.cutover_served_count == 1
    assert snap.twin_success_rate == 1.0
    recorded = [
        event
        for event in telemetry._events.published()
        if event.event_type == CONSUMER_CHAIN_CUTOVER
    ]
    assert recorded
    assert recorded[0].payload.get("influences_student") is True


def test_cutover_fallback_twin_off(telemetry, cutover_metrics):
    legacy = _legacy_rows()
    twin_calls = {"n": 0}

    def twin(_user_id: int) -> dict[str, Any]:
        twin_calls["n"] += 1
        return _twin_payload()

    result = run_study_insights_http_cutover(
        7,
        limit=5,
        environ=_eligible_environ(KWALITEC_DIGITAL_TWIN="0"),
        telemetry=telemetry,
        generate_recommendations=lambda user_id, limit=5: legacy,
        build_study_insights=twin,
        skip_request_dedupe=True,
    )
    assert result == legacy
    assert twin_calls["n"] == 0
    assert cutover_metrics.snapshot().eligible_requests == 0


def test_cutover_fallback_cutover_flag_off(telemetry, cutover_metrics):
    legacy = _legacy_rows()
    result = run_study_insights_http_cutover(
        7,
        limit=5,
        environ=_eligible_environ(KWALITEC_STUDY_INSIGHTS_CUTOVER="0"),
        telemetry=telemetry,
        generate_recommendations=lambda user_id, limit=5: legacy,
        build_study_insights=lambda user_id: _twin_payload(),
        skip_request_dedupe=True,
    )
    assert result == legacy
    assert result[0].get("source_authority") != "study_insights"


def test_cutover_fallback_production(telemetry):
    legacy = _legacy_rows()
    result = run_study_insights_http_cutover(
        7,
        limit=5,
        environ=_eligible_environ(APP_ENV="production"),
        telemetry=telemetry,
        generate_recommendations=lambda user_id, limit=5: legacy,
        build_study_insights=lambda user_id: _twin_payload(),
        skip_request_dedupe=True,
    )
    assert result == legacy


def test_cutover_fallback_twin_none(telemetry, cutover_metrics):
    legacy = _legacy_rows()
    result = run_study_insights_http_cutover(
        7,
        limit=5,
        environ=_eligible_environ(),
        telemetry=telemetry,
        generate_recommendations=lambda user_id, limit=5: legacy,
        build_study_insights=lambda user_id: None,
        skip_request_dedupe=True,
    )
    assert result == legacy
    snap = cutover_metrics.snapshot()
    assert snap.eligible_requests == 1
    assert snap.legacy_fallback_count == 1


def test_cutover_fallback_twin_exception(telemetry, cutover_metrics):
    legacy = _legacy_rows()

    def boom(_user_id: int) -> dict[str, Any]:
        raise RuntimeError("twin explode")

    result = run_study_insights_http_cutover(
        7,
        limit=5,
        environ=_eligible_environ(),
        telemetry=telemetry,
        generate_recommendations=lambda user_id, limit=5: legacy,
        build_study_insights=boom,
        skip_request_dedupe=True,
    )
    assert result == legacy
    assert cutover_metrics.snapshot().legacy_fallback_count == 1


def test_cutover_fallback_blocking_limitation(telemetry, cutover_metrics):
    legacy = _legacy_rows()
    twin = {
        "todays_key_focus": None,
        "recommended_next_action": None,
        "limitations_codes": ["canonical_learner_state_unavailable"],
    }
    result = run_study_insights_http_cutover(
        7,
        limit=5,
        environ=_eligible_environ(),
        telemetry=telemetry,
        generate_recommendations=lambda user_id, limit=5: legacy,
        build_study_insights=lambda user_id: twin,
        skip_request_dedupe=True,
    )
    assert result == legacy
    snap = cutover_metrics.snapshot()
    assert snap.limitation_fallback_count >= 1


def test_generate_recommendations_unchanged_for_bridges(ctx, monkeypatch):
    """Regression: bridges still receive legacy list, not Twin projection."""
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", "1")
    monkeypatch.setenv("KWALITEC_STUDY_INSIGHTS_CUTOVER", "1")
    monkeypatch.setenv("APP_ENV", "development")

    legacy = _legacy_rows()
    with patch.object(
        RecommendationService,
        "build_study_insights",
        return_value=_twin_payload(),
    ):
        # Force legacy body by patching lifecycle path helpers via return of
        # a controlled list — simplest: patch the dual-run skip path and
        # stub the full generate to ensure identity when cutover not used.
        with patch(
            "app.services.recommendation_service.RecommendationService."
            "_revision_lifecycle_recommendations",
            return_value=[],
        ):
            # Call generate_recommendations — should NOT return study_insights
            # projection even when cutover eligible (dashboard API owns that).
            with patch(
                "app.services.recommendation_service.RecommendationService."
                "_review_backlog_recommendations",
                return_value=legacy[:1],
            ), patch(
                "app.services.recommendation_service.RecommendationService."
                "_weak_topic_recommendations",
                return_value=[],
            ), patch(
                "app.services.recommendation_service.RecommendationService."
                "_curriculum_progression_recommendations",
                return_value=[],
            ), patch(
                "app.services.recommendation_service.RecommendationService."
                "_mock_exam_recommendations",
                return_value=[],
            ), patch(
                "app.services.recommendation_service.RecommendationService."
                "_burnout_recommendations",
                return_value=[],
            ), patch(
                "app.services.recommendation_service.RecommendationService."
                "_revision_phase_recommendations",
                return_value=[],
            ), patch(
                "app.services.recommendation_service.RecommendationService."
                "_exam_technique_recommendations",
                return_value=[],
            ), patch(
                "app.services.learning_lifecycle_service.LearningLifecycleService."
                "resolve",
                return_value=MagicMock(stage="learning"),
            ):
                result = RecommendationService.generate_recommendations(99, limit=5)
    assert result
    assert result[0].get("source_authority") != "study_insights"
    assert result[0]["title"] == "Review Fractions"


def test_dashboard_methods_serve_cutover(ctx, monkeypatch):
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", "1")
    monkeypatch.setenv("KWALITEC_STUDY_INSIGHTS_CUTOVER", "1")
    monkeypatch.setenv("APP_ENV", "development")

    with patch(
        "app.infrastructure.adapters.consumer_chain.cutover."
        "run_study_insights_http_cutover",
        return_value=[
            {
                "title": "Focus on Fractions",
                "category": "Study Focus",
                "priority": "High",
                "reason": "Spend today on Fractions",
                "source_authority": "study_insights",
            }
        ],
    ) as mocked:
        rows = RecommendationService.get_dashboard_recommendations(3, limit=5)
        today = RecommendationService.get_dashboard_today_recommendation(3)
    assert mocked.called
    assert rows[0]["source_authority"] == "study_insights"
    assert today is not None
    assert today["source_authority"] == "study_insights"


# ── HTTP integration ────────────────────────────────────────────────────────


def test_dashboard_http_serves_study_insights(
    logged_in_client, monkeypatch
) -> None:
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", "1")
    monkeypatch.setenv("KWALITEC_STUDY_INSIGHTS_CUTOVER", "1")
    monkeypatch.setenv("APP_ENV", "development")

    projected = [
        {
            "title": "Focus on Fractions",
            "category": "Study Focus",
            "priority": "High",
            "reason": "Spend today's session on Fractions.",
            "expected_benefit": "Follow Twin-grounded study guidance.",
            "next_action": "Complete a short Fractions practice set.",
            "observed_facts": ("Spend today's session on Fractions.",),
            "estimates": (),
            "educational_advice": "Spend today's session on Fractions.",
            "limitations_codes": ["sparse_evidence"],
            "source_authority": "study_insights",
            "generated_at": "2026-07-26T00:00:00",
        }
    ]
    with patch(
        "app.dashboard.routes.resolve_feature_flags",
        return_value=MagicMock(ENABLE_EDUCATIONAL_ORCHESTRATOR=False),
    ), patch.object(
        RecommendationService,
        "get_dashboard_recommendations",
        return_value=projected,
    ), patch.object(
        RecommendationService,
        "get_dashboard_today_recommendation",
        return_value=projected[0],
    ):
        response = logged_in_client.get("/dashboard/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Focus on Fractions" in body
    assert "Study Focus" in body


def test_dashboard_http_legacy_when_cutover_off(
    logged_in_client, monkeypatch
) -> None:
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", "1")
    monkeypatch.setenv("KWALITEC_STUDY_INSIGHTS_CUTOVER", "0")
    monkeypatch.setenv("APP_ENV", "development")

    legacy = [
        {
            "title": "Clear your review backlog (2 overdue)",
            "category": "Review",
            "priority": "Critical",
            "reason": "You have overdue reviews.",
            "expected_benefit": "Restore retention.",
            "generated_at": "2026-07-26T00:00:00",
        }
    ]
    with patch(
        "app.dashboard.routes.resolve_feature_flags",
        return_value=MagicMock(ENABLE_EDUCATIONAL_ORCHESTRATOR=False),
    ), patch.object(
        RecommendationService,
        "get_dashboard_recommendations",
        return_value=legacy,
    ), patch.object(
        RecommendationService,
        "get_dashboard_today_recommendation",
        return_value=legacy[0],
    ):
        response = logged_in_client.get("/dashboard/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Clear your review backlog" in body


def test_cutover_readiness_snapshot(cutover_metrics):
    cutover_metrics.record(
        {
            "cutover_attempted": True,
            "cutover_served": True,
            "alignment_status": "aligned",
            "legacy_latency_ms": 1.5,
            "twin_latency_ms": 2.0,
        }
    )
    snap = cutover_metrics.snapshot()
    assert snap.overall_cutover_readiness == "ready_for_ep002_6_planning"
    assert snap.alignment_rate == 1.0


# Silence unused import warnings for fallback constants used as documentation
_ = (
    FALLBACK_CUTOVER_FLAG_OFF,
    FALLBACK_PRODUCTION_ENV,
    FALLBACK_TWIN_EXCEPTION,
    FALLBACK_TWIN_OFF,
)
