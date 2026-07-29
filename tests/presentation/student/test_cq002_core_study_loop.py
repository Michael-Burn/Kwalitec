"""CQ-002 — Core Study Loop Reliability presentation contracts."""

from __future__ import annotations

from types import SimpleNamespace

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.student_experience.dto.readiness_explanation_snapshot import (
    ReadinessExplanationSnapshot,
)
from app.application.student_experience.profile_service import ProfileService
from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.session.navigation import build_session_steps, page_meta
from app.presentation.student.view_models import home_vm
from tests.presentation.student.helpers import render_student_home


def test_empty_home_offers_forward_paths(app, ctx):
    page_home = home_vm(
        HomeSnapshot(
            student_id="1",
            greeting="Welcome",
            has_recommendation=False,
            can_start_session=False,
        ),
        unified_journey=False,
    )
    html = render_student_home(app, page_home)
    assert 'data-student-state="empty"' in html
    assert "Choose Exam" in html
    assert "ds-btn--primary" in html
    assert "/study-plan/" in html
    assert "Review Journey" not in html
    assert "Open Study Plan" not in html


def test_session_chrome_hides_phantom_complete_step():
    steps = build_session_steps(SessionSurface.SUMMARY, session_id="s1")
    assert [s.surface for s in steps] == [
        "overview",
        "activity",
        "reflection",
        "summary",
    ]
    eyebrow, _, _ = page_meta(SessionSurface.SUMMARY)
    assert "Step 4 of 4" in eyebrow


def test_profile_falls_back_to_active_plan_exam(monkeypatch):
    class _Twin:
        def is_available(self):
            return True

        def get_learner_summary(self, student_id):
            return {
                "display_name": "Founder",
                "examination_label": "",
                "preferences": {},
                "account": {},
                "goals": (),
                "statistics": {},
            }

        def get_readiness_summary(self, student_id):
            return {"examination_label": ""}

        def get_learning_insights(self, student_id):
            return {}

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(exam_name="IFoA CM1")

    monkeypatch.setattr(
        "app.services.study_plan_service.StudyPlanService",
        _PlanSvc,
    )
    snap = ProfileService(student_twin=_Twin()).profile("7")
    assert snap.examination_label == "IFoA CM1"


def test_hero_owns_primary_next_when_both_exist():
    page = home_vm(
        HomeSnapshot(
            student_id="1",
            greeting="Welcome",
            has_recommendation=True,
            explanation=ExplanationSnapshot(
                summary="Focus on cash flow.",
                suggested_next_action="Start cash flow practice.",
                is_complete=True,
            ),
            readiness_explanation=ReadinessExplanationSnapshot(
                why_this_estimate="Coverage supports the estimate.",
                confidence_label="Suggested",
                confidence_basis="Based on practice.",
                suggested_next_action="Practise Geometry proofs.",
                review_point="Reassess later.",
                readiness_drivers=("Coverage",),
                supporting_evidence=("Evidence",),
                is_complete=True,
            ),
        ),
        unified_journey=False,
    )
    assert page.explanation is not None
    assert page.explanation.suggested_next_action.startswith("Start cash flow")
    assert page.readiness.suggested_next_action == ""
