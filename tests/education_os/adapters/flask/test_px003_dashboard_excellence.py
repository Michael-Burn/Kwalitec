"""PX-003 Dashboard Excellence — hierarchy, visibility, and XP reuse."""

from __future__ import annotations

from types import SimpleNamespace

from application.pipeline import EducationalPipeline
from presentation.dashboard import DashboardPresenter, XpProjectionMapper
from tests.education_os.application.pipeline.test_educational_pipeline import (
    make_pipeline_request,
)


def test_hierarchy_slots_present_in_html(client) -> None:
    html = client.get("/eos/dashboard/?student_id=student-ada").get_data(as_text=True)
    assert 'data-dashboard-slot="primary"' in html
    assert 'data-dashboard-slot="secondary"' in html
    assert 'data-dashboard-slot="tertiary"' in html
    assert 'data-dashboard-panel="readiness"' in html
    assert 'data-dashboard-panel="journey"' in html
    assert 'data-dashboard-panel="coach"' in html
    assert 'data-dashboard-panel="milestones"' in html
    assert 'data-dashboard-panel="quick-actions"' in html


def test_metric_grids_removed_from_dashboard(client) -> None:
    html = client.get("/eos/dashboard/?student_id=student-ada").get_data(as_text=True)
    assert "Learning statistics" not in html
    assert 'aria-label="Achievements"' not in html
    assert "eos-hero" in html


def test_focus_visibility_and_reduced_motion_in_base(client) -> None:
    html = client.get("/eos/dashboard/?student_id=student-ada").get_data(as_text=True)
    assert "focus-visible" in html
    assert "prefers-reduced-motion" in html


def test_xp_mapper_prefers_experience_over_pipeline() -> None:
    result = EducationalPipeline().run(make_pipeline_request())
    experience = SimpleNamespace(
        home=SimpleNamespace(
            todays_focus=SimpleNamespace(
                headline="Continue",
                mission_title="XP Mission",
                estimated_duration_minutes=20,
                study_objective="Purpose from XP",
                reason="Resume",
                primary_action_label="Resume Mission",
                primary_action_kind=SimpleNamespace(value="resume_session"),
            ),
            exam_readiness=SimpleNamespace(
                available=True,
                readiness_label="Building readiness",
                readiness_percent=55.0,
                trend=SimpleNamespace(value="steady"),
                trend_message="Holding steady.",
            ),
            progress=SimpleNamespace(
                mastery_message="Progress message.",
                weekly_growth_message="Growth message.",
            ),
            momentum=SimpleNamespace(momentum_message="Momentum message."),
            learning_insights=SimpleNamespace(insights=()),
            upcoming_milestone=SimpleNamespace(
                title="Next checkpoint",
                detail="Soon",
                days_until=3,
                has_milestone=True,
            ),
            quick_actions=SimpleNamespace(actions=()),
        ),
        home_snapshot=SimpleNamespace(
            focus_headline="Continue",
            focus_mission_title="XP Mission",
            focus_action_label="Resume Mission",
        ),
        journey_snapshot=SimpleNamespace(
            trajectory_message="Yesterday you completed a revision session.",
            consistency_message="Your readiness improved.",
        ),
        readiness_snapshot=SimpleNamespace(
            readiness_available=True,
            readiness_percent=55.0,
            readiness_label="Building readiness",
            direction_message="Steady",
            journey_trajectory_message="Reason for state.",
        ),
        coach_snapshot=SimpleNamespace(
            focus_headline="One coach insight.",
            journey_message="Journey note.",
        ),
        next_action=SimpleNamespace(
            label="Resume Mission",
            action_key="resume_session",
            detail="",
        ),
    )
    assert XpProjectionMapper.has_experience_cargo(experience)
    view = DashboardPresenter.present(result, experience=experience)
    assert view.hero.mission_title == "XP Mission"
    assert view.hero.purpose == "Purpose from XP"
    assert view.learning_statistics == ()
    assert "revision" in view.journey.story.lower()
