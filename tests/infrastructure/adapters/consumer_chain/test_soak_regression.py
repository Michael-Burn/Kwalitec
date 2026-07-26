"""EP-002.3 regression — Twin OFF / HTTP posture unchanged after soak modules."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.services.planning_service import PlanningService
from app.services.readiness_service import ReadinessService
from app.services.recommendation_service import RecommendationService

SOAK_DIR = (
    Path(__file__).resolve().parents[4]
    / "app"
    / "infrastructure"
    / "adapters"
    / "consumer_chain"
)
FORBIDDEN_WRITE_TOKENS = (
    "db.session.commit",
    "db.session.add",
    "StudyPlan(",
    "Mission(",
)


def test_build_apis_none_when_twin_off(monkeypatch) -> None:
    monkeypatch.setattr(
        PlanningService,
        "_resolve_twin_foundation",
        staticmethod(lambda: None),
    )
    monkeypatch.setattr(
        ReadinessService,
        "_resolve_twin_foundation",
        staticmethod(lambda: None),
    )
    monkeypatch.setattr(
        RecommendationService,
        "_resolve_twin_foundation",
        staticmethod(lambda: None),
    )
    assert PlanningService.build_daily_study_plan(1, today=date.today()) is None
    assert ReadinessService.build_readiness_intelligence(1) is None
    assert RecommendationService.build_study_insights(1) is None


def test_defaults_still_fail_open() -> None:
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_DIGITAL_TWIN is False
    assert flags.ENABLE_DIGITAL_TWIN_AUTHORITY is False


def test_soak_modules_do_not_write_runtime_a() -> None:
    soak_files = [
        SOAK_DIR / "soak.py",
        SOAK_DIR / "soak_rollback.py",
        SOAK_DIR / "authority_matrix.py",
        SOAK_DIR / "soak_telemetry.py",
        SOAK_DIR / "soak_health.py",
        SOAK_DIR / "soak_contracts.py",
    ]
    for path in soak_files:
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_WRITE_TOKENS:
            assert token not in text, f"{path.name} contains {token}"


def test_no_new_feature_flags_in_v2_defaults() -> None:
    """EP-002.3 must not introduce new flags — only exercise Twin + Authority."""
    flags = resolve_v2_feature_flags(environ={})
    assert hasattr(flags, "ENABLE_DIGITAL_TWIN")
    assert hasattr(flags, "ENABLE_DIGITAL_TWIN_AUTHORITY")
    # Soak does not add ENABLE_* for consumer chain.
    assert not hasattr(flags, "ENABLE_CONSUMER_CHAIN_SOAK")
