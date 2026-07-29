"""RC-2026.07.29-06 — Home examination identity from active Study Plan."""

from __future__ import annotations

from typing import Any

from app.application.student_experience.examination_identity import (
    exam_label_from_active_plan,
)
from app.application.student_experience.home_service import HomeService
from app.presentation.student.view_models import home_vm
from tests.application.student_experience.helpers import (
    FakeAdaptivePort,
    FakeMissionPort,
    FakeTwinPort,
)


class _EmptyExamTwin(FakeTwinPort):
    """Twin with blank examination_label (post-wizard Experience gap)."""

    def get_learner_summary(self, student_id: str) -> dict[str, Any] | None:
        summary = super().get_learner_summary(student_id)
        assert summary is not None
        summary = dict(summary)
        summary["examination_label"] = ""
        return summary

    def get_readiness_summary(self, student_id: str) -> dict[str, Any] | None:
        readiness = super().get_readiness_summary(student_id)
        assert readiness is not None
        readiness = dict(readiness)
        readiness["examination_label"] = ""
        return readiness


class _EmptyRecommendationAdaptive(FakeAdaptivePort):
    def get_todays_recommendation(self, student_id: str) -> dict[str, Any] | None:
        self.calls.append(f"recommend:{student_id}")
        return {}


def test_exam_label_from_active_plan(ctx, study_plan):
    assert exam_label_from_active_plan(str(study_plan.user_id)) == study_plan.exam_name
    assert exam_label_from_active_plan("not-an-id") == ""


def test_home_service_uses_active_plan_when_twin_exam_blank(ctx, study_plan):
    twin = _EmptyExamTwin(student_id=str(study_plan.user_id))
    adaptive = FakeAdaptivePort()
    mission = FakeMissionPort()
    home = HomeService(
        student_twin=twin,
        adaptive_decision=adaptive,
        mission=mission,
    ).home(str(study_plan.user_id))
    assert home.examination_label == study_plan.exam_name == "IFoA CM1"
    assert home.has_recommendation
    assert home.can_start_session


def test_home_service_uses_session_topic_when_recommendation_blank(ctx, study_plan):
    twin = _EmptyExamTwin(student_id=str(study_plan.user_id))
    home = HomeService(
        student_twin=twin,
        adaptive_decision=_EmptyRecommendationAdaptive(),
        mission=FakeMissionPort(),
    ).home(str(study_plan.user_id))
    assert home.examination_label == "IFoA CM1"
    assert home.recommendation_title == "Equity method"
    assert home.has_recommendation


def test_home_vm_examination_label_agrees_with_active_study_plan(ctx, study_plan):
    from app.application.student_experience.dto.home_snapshot import HomeSnapshot

    snap = HomeSnapshot(
        student_id=str(study_plan.user_id),
        greeting="Welcome back",
        examination_label="",
        has_recommendation=True,
        recommendation_title="Topic",
        can_start_session=True,
    )
    vm = home_vm(snap, unified_journey=False)
    assert vm.examination_label == study_plan.exam_name == "IFoA CM1"
