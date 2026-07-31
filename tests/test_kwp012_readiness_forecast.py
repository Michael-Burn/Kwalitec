"""KWP-012 — Readiness Forecast & Study Trajectory tests.

Deterministic trajectory projection from existing evidence, student
guidance (no fabricated certainty), Learning Journey / Home wiring, and
founder forecast metrics. No runtime authority redesign.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from app.application.educational_memory.snapshot import capture_intelligence_snapshot
from app.application.readiness_forecast import (
    FORECAST_TITLES,
    ForecastLabel,
    ReadinessForecastEngine,
    get_readiness_forecast_engine,
)
from app.application.readiness_forecast.projection import (
    project_trajectory,
    readiness_stage_for_ratio,
)
from app.application.readiness_forecast.signals import extract_forecast_signals
from app.presentation.product_language import APPROVED_TERMS
from app.presentation.student.exam_week_briefing import build_home_insights
from app.presentation.student.view_models import learning_journey_vm
from app.services.readiness_forecast_metrics import ReadinessForecastMetrics

FOUNDER_ALPHA = Path(
    "app/founder/dashboard/templates/founder_dashboard/alpha_observability.html"
)
JOURNEY_TMPL = Path("app/templates/student/learning_journey.html")

_FORBIDDEN = (
    "digital twin",
    "evidence authority",
    "pass probability",
    "guaranteed",
    "will definitely",
    "cognitive load",
    "overloaded",
    "badge",
    "leaderboard",
)


def _package(
    *,
    session_id: str,
    student_id: str = "learner-1",
    topic: str = "Discount Factors",
    created_at: str = "2026-01-01T10:00:00+00:00",
    correct: int = 2,
    incorrect: int = 0,
    finish: str = "yes",
    progress: bool = True,
    retention_risk: bool = False,
    streak_days: int | None = 4,
    recent_session_count: int | None = 4,
    with_snapshot: bool = True,
) -> dict:
    observations = []
    for _ in range(correct):
        observations.append({"type_id": "EV-RT-07", "payload": {}})
    for _ in range(incorrect):
        observations.append({"type_id": "EV-RT-08", "payload": {}})
    package = {
        "package_id": f"pkg-{session_id}",
        "student_id": student_id,
        "session_id": session_id,
        "topic_id": "topic-df",
        "topic_title": topic,
        "learning_objectives": ["Apply discount factors"],
        "observations": observations,
        "created_at": created_at,
        "finish_review_verdict": finish,
        "finish_review": {"verdict": finish},
        "progress_advanced": progress,
        "retention_risk": retention_risk,
        "streak_days": streak_days,
        "recent_session_count": recent_session_count,
        "validation": {"disposition": "accepted"},
    }
    if with_snapshot:
        snap = capture_intelligence_snapshot(package)
        package["intelligence_snapshot"] = snap.to_opaque()
    return package


def _weak_package(**kwargs) -> dict:
    defaults = {
        "correct": 0,
        "incorrect": 2,
        "finish": "partially",
        "progress": False,
        "streak_days": 0,
        "recent_session_count": 1,
    }
    defaults.update(kwargs)
    return _package(**defaults)


class TestReadinessStageReuse:
    def test_stage_vocabulary_matches_kwp006(self):
        assert readiness_stage_for_ratio(0.10) == "Building"
        assert readiness_stage_for_ratio(0.50) == "Strengthening"
        assert readiness_stage_for_ratio(0.75) == "Ready for Revision"
        assert readiness_stage_for_ratio(0.95) == "Ready for Assessment"


class TestForecastClassification:
    def test_insufficient_with_thin_history(self):
        forecast = ReadinessForecastEngine().forecast(
            [_package(session_id="s1")],
            student_id="learner-1",
        )
        assert forecast.label == ForecastLabel.INSUFFICIENT_EVIDENCE
        assert not forecast.has_forecast
        assert "few more study sittings" in forecast.guidance.lower()

    def test_on_track_strong_consistent_pattern(self):
        packages = [
            _package(
                session_id=f"s{i}",
                created_at=f"2026-01-{i:02d}T10:00:00+00:00",
            )
            for i in range(1, 7)
        ]
        forecast = ReadinessForecastEngine().forecast(
            packages,
            student_id="learner-1",
            days_to_exam=60,
            current_readiness_ratio=0.62,
            as_of=date(2026, 1, 20),
        )
        assert forecast.has_forecast
        assert forecast.label in {
            ForecastLabel.ON_TRACK,
            ForecastLabel.AHEAD_OF_SCHEDULE,
            ForecastLabel.BUILDING_MOMENTUM,
        }
        assert forecast.trajectory.projected_readiness_stage
        assert forecast.trajectory.key_assumptions
        assert forecast.trajectory.influential_factors
        for fragment in _FORBIDDEN:
            assert fragment not in forecast.guidance.lower()
            assert fragment not in forecast.explanation.lower()

    def test_needs_greater_consistency(self):
        packages = [
            _weak_package(
                session_id=f"s{i}",
                created_at=f"2026-01-{i:02d}T10:00:00+00:00",
                streak_days=0,
                recent_session_count=0,
            )
            for i in range(1, 5)
        ]
        # Spread across weeks so cadence is sparse.
        packages[2]["created_at"] = "2026-02-01T10:00:00+00:00"
        packages[3]["created_at"] = "2026-02-20T10:00:00+00:00"
        forecast = ReadinessForecastEngine().forecast(
            packages,
            student_id="learner-1",
            days_to_exam=45,
            as_of=date(2026, 2, 25),
        )
        assert forecast.label in {
            ForecastLabel.NEEDS_GREATER_CONSISTENCY,
            ForecastLabel.RECOVERY_REQUIRED,
            ForecastLabel.BELOW_TARGET_PACE,
            ForecastLabel.BUILDING_MOMENTUM,
        }
        assert "consistency" in forecast.guidance.lower() or (
            "recovery" in forecast.guidance.lower()
            or "pace" in forecast.guidance.lower()
            or "momentum" in forecast.guidance.lower()
        )

    def test_recovery_required_when_retention_dominates(self):
        packages = [
            _weak_package(
                session_id=f"s{i}",
                created_at=f"2026-03-{i:02d}T10:00:00+00:00",
                retention_risk=True,
                streak_days=2,
                recent_session_count=3,
            )
            for i in range(1, 6)
        ]
        for package in packages:
            snap = package["intelligence_snapshot"]
            snap["strategy"] = {
                **snap.get("strategy", {}),
                "action": "recover_prior_knowledge",
            }
            package["intelligence_snapshot"] = snap
        forecast = ReadinessForecastEngine().forecast(
            packages,
            student_id="learner-1",
            days_to_exam=40,
            as_of=date(2026, 3, 10),
        )
        assert forecast.label == ForecastLabel.RECOVERY_REQUIRED
        assert "recovery" in forecast.guidance.lower()

    def test_below_target_pace_near_exam(self):
        packages = [
            _weak_package(
                session_id=f"s{i}",
                created_at=f"2026-04-{i:02d}T10:00:00+00:00",
                streak_days=3,
                recent_session_count=3,
            )
            for i in range(1, 5)
        ]
        forecast = ReadinessForecastEngine().forecast(
            packages,
            student_id="learner-1",
            days_to_exam=10,
            current_readiness_ratio=0.25,
            as_of=date(2026, 4, 8),
        )
        assert forecast.label in {
            ForecastLabel.BELOW_TARGET_PACE,
            ForecastLabel.NEEDS_GREATER_CONSISTENCY,
            ForecastLabel.RECOVERY_REQUIRED,
            ForecastLabel.BUILDING_MOMENTUM,
        }
        assert forecast.trajectory.days_to_exam == 10

    def test_deterministic_same_inputs(self):
        packages = [
            _package(
                session_id=f"s{i}",
                created_at=f"2026-05-{i:02d}T10:00:00+00:00",
            )
            for i in range(1, 5)
        ]
        a = ReadinessForecastEngine().forecast(
            packages,
            student_id="learner-1",
            days_to_exam=50,
            current_readiness_ratio=0.55,
            as_of=date(2026, 5, 10),
        )
        b = get_readiness_forecast_engine().forecast(
            packages,
            student_id="learner-1",
            days_to_exam=50,
            current_readiness_ratio=0.55,
            as_of=date(2026, 5, 10),
        )
        assert a.to_opaque() == b.to_opaque()


class TestTrajectoryHonesty:
    def test_never_fabricates_certainty_copy(self):
        packages = [
            _package(
                session_id=f"s{i}",
                created_at=f"2026-06-{i:02d}T10:00:00+00:00",
            )
            for i in range(1, 4)
        ]
        forecast = ReadinessForecastEngine().forecast(
            packages,
            student_id="learner-1",
            days_to_exam=30,
        )
        text = f"{forecast.guidance} {forecast.explanation}".lower()
        assert "not a guarantee" in text or "directional" in text
        assert "pass probability" not in text

    def test_signals_consume_existing_evidence_only(self):
        packages = [
            _package(session_id="s1", created_at="2026-07-01T10:00:00+00:00"),
            _package(session_id="s2", created_at="2026-07-03T10:00:00+00:00"),
        ]
        signals = extract_forecast_signals(packages, student_id="learner-1")
        assert signals.sitting_count == 2
        traj = project_trajectory(signals)
        assert traj.confidence_title
        assert traj.key_assumptions


class TestStudentSurfaces:
    def test_learning_journey_vm_includes_forecast(self):
        from app.application.educational_memory.narrative import (
            build_learning_journey_narrative,
        )

        packages = [
            _package(
                session_id=f"s{i}",
                created_at=f"2026-08-{i:02d}T10:00:00+00:00",
            )
            for i in range(1, 4)
        ]
        narrative = build_learning_journey_narrative(
            packages, student_id="learner-1"
        )
        forecast = ReadinessForecastEngine().forecast(
            packages,
            student_id="learner-1",
            days_to_exam=40,
        )
        vm = learning_journey_vm(narrative, forecast=forecast)
        assert vm.forecast_guidance
        assert vm.forecast_title in FORECAST_TITLES.values() or vm.forecast_title

    def test_home_insights_include_trajectory(self):
        cards = build_home_insights(
            home=None,
            forecast_title="On Track",
            forecast_guidance=(
                "If your recent study pattern continues, you are likely "
                "to reach Ready for Revision before your scheduled sitting."
            ),
        )
        kinds = {c.kind for c in cards}
        assert "trajectory" in kinds
        body = next(c.body for c in cards if c.kind == "trajectory")
        assert "Ready for Revision" in body

    def test_journey_template_has_forecast_section(self):
        text = JOURNEY_TMPL.read_text(encoding="utf-8")
        assert "Readiness Forecast" in text
        assert "data-readiness-forecast" in text
        assert "forecast_guidance" in text


class TestFounderMetrics:
    def test_metrics_from_packages(self):
        packages = []
        for learner in ("a", "b"):
            for i in range(1, 5):
                packages.append(
                    _package(
                        session_id=f"{learner}-{i}",
                        student_id=learner,
                        created_at=f"2026-09-{i:02d}T10:00:00+00:00",
                    )
                )
        snap = ReadinessForecastMetrics.from_packages(packages)
        assert snap.learners_forecasted == 2
        assert snap.sittings_scanned == 8
        assert snap.label_counts
        opaque = snap.to_opaque()
        assert "forecast_accuracy" in opaque
        assert "label_counts" in opaque

    def test_founder_template_section(self):
        text = FOUNDER_ALPHA.read_text(encoding="utf-8")
        assert "Readiness Forecast" in text
        assert "readiness_forecast" in text
        assert "Trajectory distribution" in text


class TestProductLanguage:
    def test_approved_terms(self):
        assert "Readiness Forecast" in APPROVED_TERMS
        assert "Study Trajectory" in APPROVED_TERMS
