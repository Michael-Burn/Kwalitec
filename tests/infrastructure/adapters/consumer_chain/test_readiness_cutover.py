"""EP-002.6 Readiness Intelligence gated HTTP cutover tests."""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.consumer_chain import (
    assess_readiness_semantic_alignment,
    build_consumer_chain_telemetry,
    build_readiness_cutover_health_metrics,
    has_readiness_blocking_limitation,
    is_readiness_intelligence_cutover_eligible,
    project_readiness_intelligence_to_surface,
    run_readiness_intelligence_http_cutover,
    set_consumer_chain_telemetry,
    set_readiness_cutover_health_metrics,
)
from app.infrastructure.adapters.consumer_chain.readiness_cutover import (
    ALIGNMENT_ALIGNED,
    ALIGNMENT_LIMITATION_FALLBACK,
    ALIGNMENT_MISMATCHED,
    ALIGNMENT_TWIN_UNAVAILABLE,
    FALLBACK_BLOCKING_LIMITATION,
    FALLBACK_CUTOVER_FLAG_OFF,
    FALLBACK_PRODUCTION_ENV,
    FALLBACK_TWIN_EXCEPTION,
    FALLBACK_TWIN_OFF,
)
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry
from app.services.readiness_service import ReadinessService


@pytest.fixture
def telemetry():
    sink = build_consumer_chain_telemetry(
        structured=StructuredLogger("test.consumer_chain.readiness_cutover"),
        events=EventRegistry(),
    )
    previous = set_consumer_chain_telemetry(sink)
    yield sink
    set_consumer_chain_telemetry(previous)


@pytest.fixture
def cutover_metrics():
    metrics = build_readiness_cutover_health_metrics()
    previous = set_readiness_cutover_health_metrics(metrics)
    yield metrics
    set_readiness_cutover_health_metrics(previous)


def _eligible_environ(**extra: str) -> dict[str, str]:
    env = {
        "KWALITEC_DIGITAL_TWIN": "1",
        "KWALITEC_DIGITAL_TWIN_AUTHORITY": "0",
        "KWALITEC_READINESS_INTELLIGENCE_CUTOVER": "1",
        "APP_ENV": "development",
        "FLASK_ENV": "development",
    }
    env.update(extra)
    return env


def _legacy_readiness() -> dict[str, Any]:
    return {
        "score": 60.0,
        "coverage_pct": 50.0,
        "avg_mastery": 70.0,
        "review_discipline": 80.0,
        "total_topics": 10,
        "topics_started": 5,
        "topics_mastered": 2,
    }


def _legacy_weak() -> list[dict[str, Any]]:
    return [
        {
            "topic_id": "fractions",
            "topic_name": "Fractions",
            "mastery_score": 40.0,
            "stage": "learning",
            "revision_count": 2,
        }
    ]


def _legacy_strong() -> list[dict[str, Any]]:
    return [
        {
            "topic_id": "algebra",
            "topic_name": "Algebra",
            "mastery_score": 90.0,
            "stage": "mastered",
            "revision_count": 5,
        }
    ]


def _twin_payload(
    *, score: float = 62.0, topic_id: str = "fractions"
) -> dict[str, Any]:
    return {
        "readiness_score": score,
        "confidence_level": "medium",
        "availability": "available",
        "weakest_areas": [
            {
                "topic_id": topic_id,
                "topic_name": "Fractions",
                "mastery_score": 41.0,
                "reason": "Needs reinforcement",
            }
        ],
        "strongest_areas": [
            {
                "topic_id": "algebra",
                "topic_name": "Algebra",
                "mastery_score": 91.0,
                "reason": "Strong evidence",
            }
        ],
        "readiness_drivers": [
            {
                "driver_id": "curriculum_coverage",
                "label": "Coverage",
                "influence": "mixed",
                "value": 52.0,
                "source": "cls",
                "rationale": "Coverage 52%",
            },
            {
                "driver_id": "knowledge_strength",
                "label": "Knowledge",
                "influence": "supportive",
                "value": 71.0,
                "source": "cls",
                "rationale": "Mastery 71%",
            },
            {
                "driver_id": "mission_discipline",
                "label": "Discipline",
                "influence": "supportive",
                "value": 82.0,
                "source": "cls",
                "rationale": "Discipline 82%",
            },
        ],
        "recommended_next_actions": [],
        "limitations_codes": [],
        "explainability": {},
    }


def test_flag_requires_twin():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_READINESS_INTELLIGENCE_CUTOVER": "1"}
    )
    assert flags.ENABLE_READINESS_INTELLIGENCE_CUTOVER is False
    flags_on = resolve_v2_feature_flags(
        environ={
            "KWALITEC_DIGITAL_TWIN": "1",
            "KWALITEC_READINESS_INTELLIGENCE_CUTOVER": "1",
        }
    )
    assert flags_on.ENABLE_READINESS_INTELLIGENCE_CUTOVER is True


def test_eligibility_matrix():
    assert is_readiness_intelligence_cutover_eligible(
        environ=_eligible_environ()
    )
    assert not is_readiness_intelligence_cutover_eligible(
        environ=_eligible_environ(KWALITEC_DIGITAL_TWIN="0")
    )
    assert not is_readiness_intelligence_cutover_eligible(
        environ=_eligible_environ(KWALITEC_READINESS_INTELLIGENCE_CUTOVER="0")
    )
    assert not is_readiness_intelligence_cutover_eligible(
        environ=_eligible_environ(APP_ENV="production")
    )
    assert not is_readiness_intelligence_cutover_eligible(
        environ=_eligible_environ(APP_ENV="prod")
    )


def test_projection_maps_score_and_areas():
    projected = project_readiness_intelligence_to_surface(
        _twin_payload(),
        legacy_surface={
            "readiness": _legacy_readiness(),
            "weakest_topics": _legacy_weak(),
            "strongest_topics": _legacy_strong(),
        },
        weak_limit=3,
        strong_limit=3,
    )
    assert projected is not None
    assert projected["source_authority"] == "readiness_intelligence"
    assert projected["readiness"]["score"] == 62.0
    assert projected["readiness"]["coverage_pct"] == 52.0
    assert projected["readiness"]["total_topics"] == 10
    assert projected["weakest_topics"][0]["topic_id"] == "fractions"
    assert projected["strongest_topics"][0]["topic_id"] == "algebra"
    assert projected["confidence_level"] == "medium"


def test_blocking_limitation_codes():
    assert has_readiness_blocking_limitation(
        {"readiness_score": 50, "limitations_codes": ["twin_foundation_flag_off"]}
    )
    assert has_readiness_blocking_limitation(
        {"readiness_score": None, "limitations_codes": []}
    )
    assert has_readiness_blocking_limitation(
        {
            "readiness_score": 50,
            "availability": "unavailable",
            "limitations_codes": [],
        }
    )
    assert not has_readiness_blocking_limitation(_twin_payload())
    assert not has_readiness_blocking_limitation(
        {
            **_twin_payload(),
            "limitations_codes": ["planner_outputs_unavailable"],
        }
    )


@pytest.mark.parametrize(
    ("environ_extra", "expected_reason"),
    [
        ({"KWALITEC_DIGITAL_TWIN": "0"}, FALLBACK_TWIN_OFF),
        ({"KWALITEC_READINESS_INTELLIGENCE_CUTOVER": "0"}, FALLBACK_CUTOVER_FLAG_OFF),
        ({"APP_ENV": "production"}, FALLBACK_PRODUCTION_ENV),
    ],
)
def test_fallback_ineligible(
    telemetry, cutover_metrics, environ_extra, expected_reason
):
    from app.infrastructure.adapters.consumer_chain.readiness_cutover import (
        readiness_cutover_ineligibility_reason,
    )

    assert (
        readiness_cutover_ineligibility_reason(
            environ=_eligible_environ(**environ_extra)
        )
        == expected_reason
    )
    surface = run_readiness_intelligence_http_cutover(
        1,
        environ=_eligible_environ(**environ_extra),
        get_overall_readiness=lambda _uid: _legacy_readiness(),
        get_weakest_topics=lambda _uid, limit=5: _legacy_weak(),
        get_strongest_topics=lambda _uid, limit=5: _legacy_strong(),
        build_readiness_intelligence=lambda _uid: _twin_payload(),
        skip_request_dedupe=True,
    )
    assert surface["source_authority"] == "legacy"
    assert surface["readiness"]["score"] == 60.0
    assert cutover_metrics.snapshot().eligible_requests == 0


def test_fallback_twin_none(telemetry, cutover_metrics):
    surface = run_readiness_intelligence_http_cutover(
        1,
        environ=_eligible_environ(),
        get_overall_readiness=lambda _uid: _legacy_readiness(),
        get_weakest_topics=lambda _uid, limit=5: _legacy_weak(),
        get_strongest_topics=lambda _uid, limit=5: _legacy_strong(),
        build_readiness_intelligence=lambda _uid: None,
        skip_request_dedupe=True,
    )
    assert surface["source_authority"] == "legacy"
    snap = cutover_metrics.snapshot()
    assert snap.eligible_requests == 1
    assert snap.legacy_fallback_count == 1
    assert snap.cutover_served_count == 0


def test_fallback_twin_exception(telemetry, cutover_metrics):
    def _boom(_uid: int) -> dict[str, Any]:
        raise RuntimeError("boom")

    surface = run_readiness_intelligence_http_cutover(
        1,
        environ=_eligible_environ(),
        get_overall_readiness=lambda _uid: _legacy_readiness(),
        get_weakest_topics=lambda _uid, limit=5: _legacy_weak(),
        get_strongest_topics=lambda _uid, limit=5: _legacy_strong(),
        build_readiness_intelligence=_boom,
        skip_request_dedupe=True,
    )
    assert surface["source_authority"] == "legacy"
    alignment = assess_readiness_semantic_alignment(
        legacy_surface=surface,
        twin_payload=None,
        served_twin=False,
        fallback_reason=FALLBACK_TWIN_EXCEPTION,
    )
    assert alignment["alignment_status"] == ALIGNMENT_TWIN_UNAVAILABLE


def test_fallback_blocking_limitation(telemetry, cutover_metrics):
    twin = {
        **_twin_payload(),
        "limitations_codes": ["canonical_learner_state_unavailable"],
    }
    surface = run_readiness_intelligence_http_cutover(
        1,
        environ=_eligible_environ(),
        get_overall_readiness=lambda _uid: _legacy_readiness(),
        get_weakest_topics=lambda _uid, limit=5: _legacy_weak(),
        get_strongest_topics=lambda _uid, limit=5: _legacy_strong(),
        build_readiness_intelligence=lambda _uid: twin,
        skip_request_dedupe=True,
    )
    assert surface["source_authority"] == "legacy"
    snap = cutover_metrics.snapshot()
    assert snap.limitation_fallback_count == 1
    alignment = assess_readiness_semantic_alignment(
        legacy_surface={
            "readiness": _legacy_readiness(),
            "weakest_topics": _legacy_weak(),
            "strongest_topics": _legacy_strong(),
        },
        twin_payload=twin,
        served_twin=False,
        fallback_reason=FALLBACK_BLOCKING_LIMITATION,
    )
    assert alignment["alignment_status"] == ALIGNMENT_LIMITATION_FALLBACK


def test_eligible_serves_twin_projection(telemetry, cutover_metrics):
    surface = run_readiness_intelligence_http_cutover(
        9,
        environ=_eligible_environ(),
        get_overall_readiness=lambda _uid: _legacy_readiness(),
        get_weakest_topics=lambda _uid, limit=5: _legacy_weak(),
        get_strongest_topics=lambda _uid, limit=5: _legacy_strong(),
        build_readiness_intelligence=lambda _uid: _twin_payload(score=63.0),
        skip_request_dedupe=True,
    )
    assert surface["source_authority"] == "readiness_intelligence"
    assert surface["readiness"]["score"] == 63.0
    assert surface["readiness"]["source_authority"] == "readiness_intelligence"
    assert surface["weakest_topics"][0]["topic_id"] == "fractions"
    snap = cutover_metrics.snapshot()
    assert snap.eligible_requests == 1
    assert snap.cutover_served_count == 1
    assert snap.twin_success_rate == 1.0
    assert snap.alignment_rate == 1.0
    assert snap.behavioural_regressions == 0
    assert snap.ownership_violations == 0
    assert snap.overall_cutover_readiness == "ready_for_ep002_7_planning"


def test_alignment_mismatched_when_score_diverges():
    alignment = assess_readiness_semantic_alignment(
        legacy_surface={
            "readiness": _legacy_readiness(),
            "weakest_topics": _legacy_weak(),
            "strongest_topics": _legacy_strong(),
        },
        twin_payload=_twin_payload(score=95.0),
        served_twin=True,
        fallback_reason=None,
    )
    assert alignment["alignment_status"] == ALIGNMENT_MISMATCHED
    assert alignment["readiness_agreement"] is False


def test_alignment_aligned_on_score_and_areas():
    alignment = assess_readiness_semantic_alignment(
        legacy_surface={
            "readiness": _legacy_readiness(),
            "weakest_topics": _legacy_weak(),
            "strongest_topics": _legacy_strong(),
        },
        twin_payload=_twin_payload(score=62.0),
        served_twin=True,
        fallback_reason=None,
    )
    assert alignment["alignment_status"] == ALIGNMENT_ALIGNED
    assert alignment["confidence_agreement"] is True


def test_collector_still_uses_legacy_getter():
    """Regression: Adaptive collector must keep calling get_overall_readiness."""
    from pathlib import Path

    from app.infrastructure.adapters.adaptive_engine import collectors

    text = Path(collectors.__file__).read_text(encoding="utf-8")
    assert "get_overall_readiness" in text
    assert "get_dashboard_readiness_surface" not in text


def test_get_dashboard_readiness_surface_routes_to_cutover(ctx):
    with (
        patch(
            "app.infrastructure.adapters.consumer_chain.readiness_cutover."
            "is_readiness_intelligence_cutover_eligible",
            return_value=True,
        ),
        patch(
            "app.infrastructure.adapters.consumer_chain.readiness_cutover."
            "run_readiness_intelligence_http_cutover",
            return_value={
                "readiness": {"score": 70.0},
                "weakest_topics": [],
                "strongest_topics": [],
                "source_authority": "readiness_intelligence",
            },
        ) as cutover,
    ):
        surface = ReadinessService.get_dashboard_readiness_surface(4)
        assert surface["source_authority"] == "readiness_intelligence"
        cutover.assert_called_once()


def test_dashboard_http_integration(logged_in_client, monkeypatch):
    """Eligible dashboard request receives readiness intelligence projection."""
    from unittest.mock import MagicMock

    projected = {
        "readiness": {
            **_legacy_readiness(),
            "score": 66.0,
            "source_authority": "readiness_intelligence",
            "confidence_level": "medium",
        },
        "weakest_topics": _legacy_weak(),
        "strongest_topics": _legacy_strong(),
        "source_authority": "readiness_intelligence",
        "confidence_level": "medium",
        "limitations_codes": [],
        "readiness_drivers": [],
        "recommended_next_actions": [],
        "explainability": {},
    }
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", "1")
    monkeypatch.setenv("KWALITEC_READINESS_INTELLIGENCE_CUTOVER", "1")
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.setenv("FLASK_ENV", "development")

    with (
        patch(
            "app.dashboard.routes.resolve_feature_flags",
            return_value=MagicMock(ENABLE_EDUCATIONAL_ORCHESTRATOR=False),
        ),
        patch.object(
            ReadinessService,
            "get_dashboard_readiness_surface",
            return_value=projected,
        ),
        patch.object(
            ReadinessService,
            "get_review_backlog",
            return_value={
                "topics_due_today": 0,
                "topics_overdue": 0,
                "total_backlog": 0,
                "next_7_days": [],
            },
        ),
    ):
        response = logged_in_client.get("/dashboard/")
    assert response.status_code == 200
    assert b"66" in response.data


def test_cutover_emits_health_metrics(telemetry, cutover_metrics):
    run_readiness_intelligence_http_cutover(
        2,
        environ=_eligible_environ(),
        get_overall_readiness=lambda _uid: _legacy_readiness(),
        get_weakest_topics=lambda _uid, limit=5: _legacy_weak(),
        get_strongest_topics=lambda _uid, limit=5: _legacy_strong(),
        build_readiness_intelligence=lambda _uid: _twin_payload(),
        skip_request_dedupe=True,
    )
    snap = cutover_metrics.snapshot()
    assert snap.eligible_requests == 1
    assert snap.cutover_served_count == 1
    assert telemetry is not None
