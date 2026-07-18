"""V1SP-001E — Information Architecture & Dashboard Simplification tests."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from app.services.planning_service import PlanningService
from app.services.product_communication_service import ProductCommunicationService
from app.services.study_plan_service import StudyPlanService

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = REPO_ROOT / "app" / "templates"
FOUNDER_TEMPLATES = (
    REPO_ROOT / "app" / "founder" / "dashboard" / "templates" / "founder_dashboard"
)
HELP_PARTIAL = TEMPLATES / "partials" / "contextual_help.html"
DASHBOARD = TEMPLATES / "dashboard" / "index.html"
MISSION = TEMPLATES / "mission" / "index.html"
ANALYTICS = TEMPLATES / "analytics" / "index.html"
RELEASE_DOC = (
    REPO_ROOT
    / "knowledge"
    / "releases"
    / "V1SP-001E_INFORMATION_ARCHITECTURE_SIMPLIFICATION.md"
)


def _create_plan_and_mission(user) -> None:
    StudyPlanService.create_study_plan(
        user_id=user.id,
        exam_name="IFoA CS1",
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=60,
        weekend_study_minutes=120,
        current_stage="Learning",
        study_preference="Mixed",
        target_grade="B",
        curriculum_version="2026",
        curriculum_topic_code="1.1",
    )
    PlanningService.generate_today_mission(user.id)


class TestV1sp001eDeliverables:
    def test_release_document_exists(self):
        assert RELEASE_DOC.is_file()
        text = RELEASE_DOC.read_text(encoding="utf-8")
        assert "V1SP-001E" in text
        assert "Simplification Audit" in text
        assert "Duplicate Actions Removed" in text
        assert "Progressive Disclosure" in text

    def test_contextual_help_partial_exists(self):
        html = HELP_PARTIAL.read_text(encoding="utf-8")
        assert "macro help_tip" in html
        assert "macro learn_more" in html
        assert 'aria-label=' in html
        assert "visually-hidden" in html
        assert "<details" in html


class TestV1sp001eProgressiveDisclosure:
    def test_dashboard_uses_help_patterns(self):
        html = DASHBOARD.read_text(encoding="utf-8")
        assert "contextual_help.html" in html
        assert "help_tip" in html
        assert "learn_more" in html
        assert "Why this recommendation" in html
        # EI recommendation card keeps its own start CTA (educational integration).
        assert "ei_card.primary_action" in html
        assert 'data-ptp004-cta="primary"' in html

    def test_mission_collapses_long_guidance(self):
        html = MISSION.read_text(encoding="utf-8")
        assert "contextual_help.html" in html
        assert "Session guidance" in html or "How today's session is chosen" in html
        assert "Start Study Session" in html

    def test_analytics_honesty_in_help_tips(self):
        html = ANALYTICS.read_text(encoding="utf-8")
        assert ProductCommunicationService.ESTIMATED_KNOWLEDGE_BASIS in html
        assert ProductCommunicationService.ACCURACY_BASIS in html
        assert ProductCommunicationService.ESTIMATED_READINESS_SELF_REPORT in html
        assert "help_tip" in html


class TestV1sp001eDashboardRuntime:
    def test_single_primary_session_cta(self, app, user, logged_in_client):
        _create_plan_and_mission(user)
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)

        assert body.count('data-ptp004-cta="primary"') == 1
        assert "Start Study Session" in body or "Resume Study Session" in body
        # Recommendation must not add a second Start Study Session button.
        assert 'data-ptp004-slot="primary-session"' in body
        assert "ctx-help-trigger" in body or "ctx-learn-more" in body

    def test_page_headers_remain_short(self, logged_in_client, user):
        _create_plan_and_mission(user)
        for path in ("/dashboard/", "/missions/", "/analytics/"):
            response = logged_in_client.get(path)
            assert response.status_code == 200
            body = response.get_data(as_text=True)
            assert "section-title" in body
            assert "section-description" in body


class TestV1sp001eFounderSimplification:
    def test_overview_and_vision_headers_shortened(self):
        overview = (FOUNDER_TEMPLATES / "overview.html").read_text(encoding="utf-8")
        vision = (FOUNDER_TEMPLATES / "vision_journal.html").read_text(encoding="utf-8")
        assert "Operational pulse" in overview
        assert "No Vision entries yet" in overview or "New entry" in overview
        assert "Strategic product ideas" in vision
        assert "No Vision entries yet" in vision

    def test_internal_alpha_uses_learn_more(self):
        html = (FOUNDER_TEMPLATES / "internal_alpha.html").read_text(encoding="utf-8")
        assert "learn_more" in html
        assert "filesystem week pipeline is not wired" in html


class TestV1sp001eStudyPlanHierarchy:
    def test_view_uses_section_header_not_display_6(self):
        html = (TEMPLATES / "study_plan" / "view.html").read_text(encoding="utf-8")
        assert "display-6" not in html
        assert "section-title" in html
        assert "btn-primary" in html
        assert "Edit" in html
        assert "btn-link-tertiary" in html
