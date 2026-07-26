"""EP-002.7 Daily Plan gated HTTP cutover tests."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.consumer_chain import (
    assess_daily_plan_semantic_alignment,
    build_consumer_chain_telemetry,
    build_daily_plan_cutover_health_metrics,
    has_daily_plan_blocking_limitation,
    is_daily_plan_cutover_eligible,
    project_daily_plan_to_mission_surface,
    run_daily_plan_http_cutover,
    set_consumer_chain_telemetry,
    set_daily_plan_cutover_health_metrics,
)
from app.infrastructure.adapters.consumer_chain.daily_plan_cutover import (
    ALIGNMENT_ALIGNED,
    ALIGNMENT_LIMITATION_FALLBACK,
    ALIGNMENT_MISMATCHED,
    ALIGNMENT_TWIN_UNAVAILABLE,
    FALLBACK_BLOCKING_LIMITATION,
    FALLBACK_CUTOVER_FLAG_OFF,
    FALLBACK_PRODUCTION_ENV,
    FALLBACK_TWIN_EXCEPTION,
    FALLBACK_TWIN_OFF,
    SOURCE_AUTHORITY_DAILY_STUDY_PLAN,
)
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry
from app.services.planning_service import PlanningService


@pytest.fixture
def telemetry():
    sink = build_consumer_chain_telemetry(
        structured=StructuredLogger("test.consumer_chain.daily_plan_cutover"),
        events=EventRegistry(),
    )
    previous = set_consumer_chain_telemetry(sink)
    yield sink
    set_consumer_chain_telemetry(previous)


@pytest.fixture
def cutover_metrics():
    metrics = build_daily_plan_cutover_health_metrics()
    previous = set_daily_plan_cutover_health_metrics(metrics)
    yield metrics
    set_daily_plan_cutover_health_metrics(previous)


def _eligible_environ(**extra: str) -> dict[str, str]:
    env = {
        "KWALITEC_DIGITAL_TWIN": "1",
        "KWALITEC_DIGITAL_TWIN_AUTHORITY": "0",
        "KWALITEC_DAILY_PLAN_CUTOVER": "1",
        "APP_ENV": "development",
        "FLASK_ENV": "development",
    }
    env.update(extra)
    return env


def _legacy_mission(*, title: str = "Study Fractions") -> Any:
    return SimpleNamespace(
        id=42,
        title=title,
        status="Pending",
        tasks=[SimpleNamespace(title="Read Fractions", description="")],
        mission_date=None,
    )


def _twin_plan(
    *,
    topic_id: str = "fractions",
    topic_name: str = "Fractions",
    available: bool = True,
) -> dict[str, Any]:
    return {
        "availability": "available" if available else "unavailable",
        "today_missions": [
            {
                "slot": "progression",
                "topic_id": topic_id,
                "topic_name": topic_name,
                "reason": "Next incomplete syllabus leaf",
                "priority": 1,
                "expected_benefit": "Progress",
            }
        ],
        "recommended_workload": {
            "available_study_minutes": 60,
            "recommended_minutes": 45,
            "rationale": "weekday",
            "authority": "adaptive_study_planner",
        },
        "topic_ordering": [
            {
                "position": 1,
                "topic_id": topic_id,
                "topic_name": topic_name,
                "completed": False,
            }
        ],
        "revision_priorities": [],
        "limitations_codes": [],
        "explainability": {"summary": "planner-owned"},
    }


def test_flag_defaults_and_requires_twin():
    assert resolve_v2_feature_flags(environ={}).ENABLE_DAILY_PLAN_CUTOVER is False
    assert (
        resolve_v2_feature_flags(
            environ={"KWALITEC_DAILY_PLAN_CUTOVER": "1"}
        ).ENABLE_DAILY_PLAN_CUTOVER
        is False
    )
    assert (
        resolve_v2_feature_flags(
            environ={
                "KWALITEC_DIGITAL_TWIN": "1",
                "KWALITEC_DAILY_PLAN_CUTOVER": "1",
            }
        ).ENABLE_DAILY_PLAN_CUTOVER
        is True
    )


@pytest.mark.parametrize(
    ("environ", "expected"),
    [
        ({}, False),
        (_eligible_environ(KWALITEC_DIGITAL_TWIN="0"), False),
        (_eligible_environ(KWALITEC_DAILY_PLAN_CUTOVER="0"), False),
        (_eligible_environ(APP_ENV="production", FLASK_ENV="production"), False),
        (_eligible_environ(), True),
    ],
)
def test_eligibility_matrix(environ, expected):
    assert is_daily_plan_cutover_eligible(environ=environ) is expected


def test_blocking_limitations():
    assert has_daily_plan_blocking_limitation(None) is True
    assert has_daily_plan_blocking_limitation({"availability": "unavailable"}) is True
    assert (
        has_daily_plan_blocking_limitation(
            {
                "availability": "available",
                "today_missions": [],
                "limitations_codes": [],
            }
        )
        is True
    )
    assert (
        has_daily_plan_blocking_limitation(
            {
                "availability": "available",
                "today_missions": [{"slot": "progression", "topic_id": "a"}],
                "limitations_codes": ["canonical_learner_state_unavailable"],
            }
        )
        is True
    )
    assert has_daily_plan_blocking_limitation(_twin_plan()) is False


def test_projection_overlays_title_without_orm_write():
    legacy = {"today_mission": _legacy_mission(title="Study Algebra")}
    projected = project_daily_plan_to_mission_surface(
        _twin_plan(topic_name="Fractions"),
        legacy_surface=legacy,
    )
    assert projected is not None
    assert projected["source_authority"] == SOURCE_AUTHORITY_DAILY_STUDY_PLAN
    assert projected["today_mission"].title == "Study Fractions"
    assert projected["today_mission"].id == 42
    assert projected["today_mission"].status == "Pending"
    # Underlying ORM title unchanged
    assert legacy["today_mission"].title == "Study Algebra"


def test_projection_empty_without_legacy_mission():
    assert (
        project_daily_plan_to_mission_surface(
            _twin_plan(), legacy_surface={"today_mission": None}
        )
        is None
    )


def test_semantic_alignment_aligned():
    legacy = {"today_mission": _legacy_mission(title="Study Fractions")}
    alignment = assess_daily_plan_semantic_alignment(
        legacy_surface=legacy,
        twin_payload=_twin_plan(),
        served_twin=True,
        fallback_reason=None,
    )
    assert alignment["alignment_status"] == ALIGNMENT_ALIGNED
    assert alignment["topic_agreement"] is True
    assert alignment["workload_agreement"] is True


def test_semantic_alignment_mismatched():
    legacy = {
        "today_mission": SimpleNamespace(
            id=7,
            title="Study Calculus",
            status="Pending",
            tasks=[SimpleNamespace(title="Derivatives practice", description="")],
        )
    }
    twin = _twin_plan(topic_id="fractions", topic_name="Fractions")
    twin["today_missions"][0]["reason"] = ""
    twin["topic_ordering"] = [
        {"position": 1, "topic_id": "fractions", "topic_name": "Fractions"}
    ]
    alignment = assess_daily_plan_semantic_alignment(
        legacy_surface=legacy,
        twin_payload=twin,
        served_twin=True,
        fallback_reason=None,
    )
    assert alignment["alignment_status"] == ALIGNMENT_MISMATCHED
    assert alignment["topic_agreement"] is False


def test_cutover_serves_twin_when_eligible(telemetry, cutover_metrics):
    mission = _legacy_mission()
    surface = run_daily_plan_http_cutover(
        9,
        environ=_eligible_environ(),
        build_daily_study_plan=lambda *_a, **_k: _twin_plan(),
        generate_today_mission=lambda *_a, **_k: mission,
        get_today_mission=lambda *_a, **_k: mission,
        skip_request_dedupe=True,
    )
    assert surface["source_authority"] == SOURCE_AUTHORITY_DAILY_STUDY_PLAN
    assert surface["today_mission"].title == "Study Fractions"
    snap = cutover_metrics.snapshot()
    assert snap.eligible_requests == 1
    assert snap.cutover_served_count == 1
    assert snap.overall_cutover_readiness == "ready_for_ep002_8_presentation"


@pytest.mark.parametrize(
    ("environ", "reason"),
    [
        (_eligible_environ(KWALITEC_DIGITAL_TWIN="0"), FALLBACK_TWIN_OFF),
        (
            _eligible_environ(KWALITEC_DAILY_PLAN_CUTOVER="0"),
            FALLBACK_CUTOVER_FLAG_OFF,
        ),
        (
            _eligible_environ(APP_ENV="production", FLASK_ENV="production"),
            FALLBACK_PRODUCTION_ENV,
        ),
    ],
)
def test_cutover_fail_open_pre_attempt(environ, reason, telemetry, cutover_metrics):
    mission = _legacy_mission(title="Legacy Title")
    surface = run_daily_plan_http_cutover(
        2,
        environ=environ,
        build_daily_study_plan=lambda *_a, **_k: _twin_plan(),
        generate_today_mission=lambda *_a, **_k: mission,
        skip_request_dedupe=True,
    )
    assert surface["source_authority"] == "legacy"
    assert surface["today_mission"].title == "Legacy Title"


def test_cutover_fail_open_twin_none(telemetry, cutover_metrics):
    mission = _legacy_mission()
    surface = run_daily_plan_http_cutover(
        4,
        environ=_eligible_environ(),
        build_daily_study_plan=lambda *_a, **_k: None,
        generate_today_mission=lambda *_a, **_k: mission,
        skip_request_dedupe=True,
    )
    assert surface["source_authority"] == "legacy"
    snap = cutover_metrics.snapshot()
    assert snap.legacy_fallback_count == 1


def test_cutover_fail_open_twin_exception(telemetry, cutover_metrics):
    mission = _legacy_mission()

    def boom(*_a, **_k):
        raise RuntimeError("boom")

    surface = run_daily_plan_http_cutover(
        5,
        environ=_eligible_environ(),
        build_daily_study_plan=boom,
        generate_today_mission=lambda *_a, **_k: mission,
        skip_request_dedupe=True,
    )
    assert surface["source_authority"] == "legacy"
    alignment = assess_daily_plan_semantic_alignment(
        legacy_surface=surface,
        twin_payload=None,
        served_twin=False,
        fallback_reason=FALLBACK_TWIN_EXCEPTION,
    )
    assert alignment["alignment_status"] == ALIGNMENT_TWIN_UNAVAILABLE


def test_cutover_fail_open_blocking(telemetry, cutover_metrics):
    mission = _legacy_mission()
    blocked = _twin_plan(available=False)
    surface = run_daily_plan_http_cutover(
        6,
        environ=_eligible_environ(),
        build_daily_study_plan=lambda *_a, **_k: blocked,
        generate_today_mission=lambda *_a, **_k: mission,
        skip_request_dedupe=True,
    )
    assert surface["source_authority"] == "legacy"
    alignment = assess_daily_plan_semantic_alignment(
        legacy_surface=surface,
        twin_payload=blocked,
        served_twin=False,
        fallback_reason=FALLBACK_BLOCKING_LIMITATION,
    )
    assert alignment["alignment_status"] == ALIGNMENT_LIMITATION_FALLBACK


def test_generate_today_mission_unchanged_for_bridges():
    """Experience / sync callers keep direct generate_today_mission authority."""
    import inspect

    source = inspect.getsource(PlanningService.generate_today_mission)
    assert "run_daily_plan_http_cutover" not in source
    assert "MissionOptimizer" not in source


def test_mission_optimizer_quarantine_preserved():
    import app.infrastructure.adapters.consumer_chain.daily_plan_cutover as mod

    source = open(mod.__file__, encoding="utf-8").read()
    assert "from app.services.mission_optimizer" not in source
    assert "import mission_optimizer" not in source
    assert "generate_balanced_mission" not in source


def test_controlled_bench_metrics(telemetry, cutover_metrics):
    mission = _legacy_mission()
    scenarios = (
        [("ok", _twin_plan())] * 38
        + [("none", None)] * 6
        + [("block", _twin_plan(available=False))] * 4
        + [("exc", "exc")] * 2
    )
    assert len(scenarios) == 50

    for idx, (kind, payload) in enumerate(scenarios):
        if kind == "exc":

            def boom(*_a, **_k):
                raise RuntimeError("x")

            builder = boom
        else:
            builder = (lambda p: (lambda *_a, **_k: p))(payload)
        run_daily_plan_http_cutover(
            100 + idx,
            environ=_eligible_environ(),
            build_daily_study_plan=builder,
            generate_today_mission=lambda *_a, **_k: mission,
            skip_request_dedupe=True,
        )

    snap = cutover_metrics.snapshot()
    assert snap.eligible_requests == 50
    assert snap.cutover_served_count == 38
    assert snap.legacy_fallback_count == 12
    assert snap.behavioural_regressions == 0
    assert snap.ownership_violations == 0
    assert snap.overall_cutover_readiness == "ready_for_ep002_8_presentation"


def test_dashboard_facade_uses_cutover_when_eligible():
    mission = _legacy_mission()
    with patch.dict("os.environ", _eligible_environ(), clear=False):
        with patch(
            "app.infrastructure.adapters.consumer_chain.daily_plan_cutover.run_daily_plan_http_cutover",
            return_value={
                "today_mission": mission,
                "source_authority": SOURCE_AUTHORITY_DAILY_STUDY_PLAN,
            },
        ) as cutover:
            surface = PlanningService.get_dashboard_mission_surface(11)
            cutover.assert_called_once()
            assert surface["source_authority"] == SOURCE_AUTHORITY_DAILY_STUDY_PLAN
