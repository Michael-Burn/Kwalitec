"""Capability 4.7 — Educational KPI status integrity tests.

Verifies schedule/pace labels are educationally honest: derived only from
calendar + TimeEngine evidence, never from a fictional expected-coverage
curve or unsupported “Critically Behind” / risk claims.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.services.educational_kpi_status import (
    CODE_COMFORTABLE_PACE,
    CODE_CURRICULUM_COMPLETE,
    CODE_EXAM_PERIOD,
    CODE_HIGH_REMAINING_WORKLOAD,
    CODE_LIMITED_TIME,
    CODE_PACE_MATCHES_PLAN,
    CODE_PLAN_ACTIVE,
    CODE_SCHEDULE_TIGHT,
    EducationalKpiStatusService,
)


@dataclass(frozen=True)
class _FakeTimeSummary:
    hours_surplus_or_deficit: float
    remaining_hours: float = 40.0
    available_study_hours: float = 60.0


class TestEducationalKpiStatusHonesty:
    """Labels must match available evidence only."""

    def test_high_coverage_many_days_never_critically_behind(self) -> None:
        """Regression: 92% coverage + 67 days must not imply critical failure."""
        status = EducationalKpiStatusService.from_time_summary(
            _FakeTimeSummary(
                hours_surplus_or_deficit=30.0,
                remaining_hours=20.0,
                available_study_hours=50.0,
            ),
            days_remaining=67,
            coverage_pct=92.0,
        )
        assert status.label not in {
            "Critically Behind",
            "Slightly Behind",
            "Behind Schedule",
            "Ahead of Schedule",
            "On Track",
        }
        assert status.code == CODE_COMFORTABLE_PACE
        assert status.label == "Comfortable Pace"
        assert status.risk is None
        assert status.readiness is None
        assert status.predicted_completion is None

    def test_high_remaining_workload_label(self) -> None:
        status = EducationalKpiStatusService.from_time_balance(
            days_remaining=67,
            hours_surplus_or_deficit=-45.0,
            remaining_hours=90.0,
            available_study_hours=45.0,
            coverage_pct=30.0,
        )
        assert status.code == CODE_HIGH_REMAINING_WORKLOAD
        assert status.label == "High Remaining Workload"
        assert status.severity == "urgent"

    def test_schedule_tight_label(self) -> None:
        status = EducationalKpiStatusService.from_time_balance(
            days_remaining=40,
            hours_surplus_or_deficit=-10.0,
            remaining_hours=50.0,
            available_study_hours=40.0,
        )
        assert status.code == CODE_SCHEDULE_TIGHT
        assert status.label == "Schedule Tight"

    def test_pace_matches_plan(self) -> None:
        status = EducationalKpiStatusService.from_time_balance(
            days_remaining=90,
            hours_surplus_or_deficit=5.0,
            remaining_hours=40.0,
            available_study_hours=45.0,
        )
        assert status.code == CODE_PACE_MATCHES_PLAN
        assert status.label == "Pace Matches Plan"

    def test_limited_time_with_deficit(self) -> None:
        status = EducationalKpiStatusService.from_time_balance(
            days_remaining=10,
            hours_surplus_or_deficit=-5.0,
            remaining_hours=20.0,
            available_study_hours=15.0,
        )
        assert status.code == CODE_LIMITED_TIME
        assert status.label == "Limited Time Remaining"

    def test_exam_period(self) -> None:
        status = EducationalKpiStatusService.from_time_balance(
            days_remaining=0,
            hours_surplus_or_deficit=0.0,
        )
        assert status.code == CODE_EXAM_PERIOD
        assert status.label == "Exam Period"

    def test_curriculum_complete(self) -> None:
        status = EducationalKpiStatusService.from_time_balance(
            days_remaining=30,
            hours_surplus_or_deficit=-100.0,
            coverage_pct=100.0,
        )
        assert status.code == CODE_CURRICULUM_COMPLETE
        assert status.label == "Curriculum Complete"

    def test_calendar_fallback_no_behind_claim(self) -> None:
        status = EducationalKpiStatusService.from_days_remaining(67)
        assert status.code == CODE_PLAN_ACTIVE
        assert status.label == "Plan Active"
        assert "Behind" not in status.label
        assert "Ahead" not in status.label

    def test_calendar_fallback_limited_time(self) -> None:
        status = EducationalKpiStatusService.from_days_remaining(7)
        assert status.code == CODE_LIMITED_TIME
        assert status.label == "Limited Time Remaining"

    def test_future_slots_remain_none(self) -> None:
        status = EducationalKpiStatusService.from_days_remaining(50)
        assert status.readiness is None
        assert status.risk is None
        assert status.study_velocity is None
        assert status.predicted_completion is None

    def test_symbol_not_colour_only(self) -> None:
        comfortable = EducationalKpiStatusService.from_time_balance(
            days_remaining=60,
            hours_surplus_or_deficit=25.0,
        )
        urgent = EducationalKpiStatusService.from_time_balance(
            days_remaining=60,
            hours_surplus_or_deficit=-40.0,
        )
        assert comfortable.symbol != urgent.symbol
        assert comfortable.symbol
        assert urgent.symbol

    def test_to_dict_includes_legacy_status_alias(self) -> None:
        status = EducationalKpiStatusService.from_days_remaining(20)
        payload = status.to_dict()
        assert payload["status"] == status.code
        assert payload["label"] == status.label
        assert payload["symbol"] == status.symbol


class TestExamTimelineStatusIntegrity:
    """ExamTimeline must not emit legacy unsupported labels."""

    def test_determine_status_uses_honest_service(self, app, db, user) -> None:
        from unittest.mock import MagicMock

        from app.services.exam_timeline import ExamTimeline

        plan = MagicMock()
        plan.curriculum_id = None
        plan.curriculum_version = None

        status = ExamTimeline._determine_status(
            days_remaining=67,
            coverage_pct=92.0,
            active_plan=plan,
        )
        assert status.label not in {
            "Critically Behind",
            "Slightly Behind",
            "On Track",
            "Ahead of Schedule",
        }
        assert status.code == CODE_PLAN_ACTIVE

    def test_low_coverage_few_days_limited_or_workload(
        self, app, db, user
    ) -> None:
        from unittest.mock import MagicMock, patch

        from app.services.exam_timeline import ExamTimeline
        from app.services.time_engine_service import TimeSummary

        plan = MagicMock()
        fake = TimeSummary(
            total_curriculum_hours=100.0,
            completed_hours=10.0,
            remaining_hours=90.0,
            available_study_hours=20.0,
            hours_surplus_or_deficit=-70.0,
        )
        with patch(
            "app.services.exam_timeline.TimeEngineService.calculate_time_summary",
            return_value=fake,
        ):
            status = ExamTimeline._determine_status(
                days_remaining=10,
                coverage_pct=10.0,
                active_plan=plan,
            )
        assert status.code == CODE_LIMITED_TIME
        assert "Behind" not in status.label

    def test_completed_curriculum_status(self, app, db, user) -> None:
        from unittest.mock import MagicMock, patch

        from app.services.exam_timeline import ExamTimeline
        from app.services.time_engine_service import TimeSummary

        plan = MagicMock()
        fake = TimeSummary(
            total_curriculum_hours=100.0,
            completed_hours=100.0,
            remaining_hours=0.0,
            available_study_hours=40.0,
            hours_surplus_or_deficit=40.0,
        )
        with patch(
            "app.services.exam_timeline.TimeEngineService.calculate_time_summary",
            return_value=fake,
        ):
            status = ExamTimeline._determine_status(
                days_remaining=30,
                coverage_pct=100.0,
                active_plan=plan,
            )
        assert status.code == CODE_CURRICULUM_COMPLETE


class TestForbiddenLegacyLabelsAbsent:
    """Source-level guard: unsupported labels must not remain in status module."""

    def test_educational_kpi_module_has_no_legacy_labels(self) -> None:
        from pathlib import Path

        src = Path("app/services/educational_kpi_status.py").read_text(
            encoding="utf-8"
        )
        for forbidden in (
            "Critically Behind",
            "Slightly Behind",
            "Behind Schedule",
            "Ahead of Schedule",
            "On Track",
        ):
            assert forbidden not in src

    def test_exam_timeline_has_no_legacy_status_labels(self) -> None:
        from pathlib import Path

        src = Path("app/services/exam_timeline.py").read_text(encoding="utf-8")
        for forbidden in (
            "Critically Behind",
            "Slightly Behind",
            "Ahead of Schedule",
            "On Track",
        ):
            assert forbidden not in src

    def test_no_fictional_180_day_curve(self) -> None:
        from pathlib import Path

        src = Path("app/services/exam_timeline.py").read_text(encoding="utf-8")
        assert "typical_total" not in src
        assert "expected_coverage" not in src
