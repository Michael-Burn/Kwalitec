"""PTP-004 Information Architecture regression tests.

Dashboard must answer student decisions in order:
1. What to study (Today's Study Session + primary CTA)
2. Whether on track (single Progress / Syllabus coverage story)
3. Estimated Knowledge (separate from coverage)
4. Attention / recommendations
5. Secondary exploration

No competing coverage percentages. Navigation unchanged.
"""

from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

from app.services.planning_service import PlanningService
from app.services.study_plan_service import StudyPlanService

REPO_ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_TEMPLATE = REPO_ROOT / "app" / "templates" / "dashboard" / "index.html"
PTP004_DOC = (
    REPO_ROOT / "knowledge" / "product" / "PTP-004_INFORMATION_ARCHITECTURE.md"
)
SIDEBAR = REPO_ROOT / "app" / "templates" / "partials" / "sidebar.html"

# Competing / removed Dashboard chrome (must not reappear as section titles)
FORBIDDEN_DASHBOARD_LABELS = (
    "Curriculum Coverage",
    "Weighted Coverage",
    "Curriculum Roadmap",
    "Quick Actions",
    "Daily Briefing",
    "Decision Journal",
)

# Card title retired by PTP-004 (honesty phrases may still say "Learning Progress")
FORBIDDEN_CARD_TITLE = 'command-card-title">Learning Progress'

REQUIRED_SLOTS = (
    'data-ptp004-slot="primary-session"',
    'data-ptp004-slot="progress"',
    'data-ptp004-slot="estimated-knowledge"',
    'data-ptp004-slot="attention"',
    'data-ptp004-slot="secondary"',
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


# ─────────────────────────────────────────────────────────────────────────────
# Documentation deliverable
# ─────────────────────────────────────────────────────────────────────────────


class TestPtp004Documentation:
    def test_standard_document_exists(self):
        assert PTP004_DOC.is_file()
        text = PTP004_DOC.read_text(encoding="utf-8")
        assert "PTP-004" in text
        assert "Dashboard Information Audit" in text
        assert "Information Hierarchy" in text
        assert "Removal Justification" in text
        assert "Migration Plan" in text

    def test_template_declares_decision_slots(self):
        html = DASHBOARD_TEMPLATE.read_text(encoding="utf-8")
        for slot in REQUIRED_SLOTS:
            assert slot in html, f"Missing IA slot marker: {slot}"
        assert 'data-ptp004-cta="primary"' in html
        assert 'data-ptp004-metric="syllabus-coverage"' in html


# ─────────────────────────────────────────────────────────────────────────────
# Hierarchy / no duplicate metrics
# ─────────────────────────────────────────────────────────────────────────────


class TestPtp004DashboardHierarchy:
    def test_primary_cta_and_session_first(self, app, user, logged_in_client):
        _create_plan_and_mission(user)
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)

        assert "Today's Study Session" in body
        assert 'data-ptp004-cta="primary"' in body
        assert (
            "Start Study Session" in body
            or "Resume Study Session" in body
            or "Review Today's Session" in body
        )

        session_idx = body.find('data-ptp004-slot="primary-session"')
        progress_idx = body.find('data-ptp004-slot="progress"')
        knowledge_idx = body.find('data-ptp004-slot="estimated-knowledge"')
        attention_idx = body.find('data-ptp004-slot="attention"')
        secondary_idx = body.find('data-ptp004-slot="secondary"')
        assert session_idx >= 0
        assert progress_idx > session_idx
        assert knowledge_idx > progress_idx
        assert attention_idx > knowledge_idx
        assert secondary_idx > attention_idx

    def test_no_competing_coverage_percentages(self, app, user, logged_in_client):
        _create_plan_and_mission(user)
        response = logged_in_client.get("/dashboard/")
        body = response.get_data(as_text=True)

        for label in FORBIDDEN_DASHBOARD_LABELS:
            assert label not in body, f"Removed IA element still present: {label}"
        assert FORBIDDEN_CARD_TITLE not in body

        # At most one authoritative syllabus-coverage hero metric
        assert body.count('data-ptp004-metric="syllabus-coverage"') <= 1
        assert "Curriculum Coverage" not in body
        assert "Weighted Coverage" not in body

    def test_single_authoritative_progress_story(self, app, user, logged_in_client):
        _create_plan_and_mission(user)
        response = logged_in_client.get("/dashboard/")
        body = response.get_data(as_text=True)

        assert "Progress through Study Plan" in body
        assert body.count('data-ptp004-metric="syllabus-coverage"') <= 1

    def test_estimated_knowledge_separated_from_progress(
        self, app, user, logged_in_client
    ):
        _create_plan_and_mission(user)
        response = logged_in_client.get("/dashboard/")
        body = response.get_data(as_text=True)

        assert 'data-ptp004-slot="estimated-knowledge"' in body
        assert "Estimated Knowledge" in body
        # Progress card must not use Estimated Knowledge as its hero label
        progress_block = re.search(
            r'data-ptp004-slot="progress".*?data-ptp004-slot="estimated-knowledge"',
            body,
            re.DOTALL,
        )
        assert progress_block is not None
        assert "Avg. Estimated Knowledge" not in progress_block.group(0)

    def test_ten_second_decision_questions_surface(
        self, app, user, logged_in_client
    ):
        """Page chrome answers the three PTP-004 decision questions."""
        _create_plan_and_mission(user)
        response = logged_in_client.get("/dashboard/")
        body = response.get_data(as_text=True)

        assert "What to study" in body or "Today's Study Session" in body
        assert "Progress through Study Plan" in body
        assert (
            "Topics needing more practice" in body
            or "Today's Recommendation" in body
            or "Recommendations needing attention" in body
            or "Estimated Knowledge" in body
        )


# ─────────────────────────────────────────────────────────────────────────────
# Navigation unchanged
# ─────────────────────────────────────────────────────────────────────────────


class TestPtp004NavigationUnchanged:
    def test_sidebar_nav_endpoints_preserved(self):
        html = SIDEBAR.read_text(encoding="utf-8")
        for endpoint in (
            "dashboard.index",
            "mission.missions",
            "study_plan.index",
            "analytics.index",
            "settings.index",
        ):
            assert endpoint in html

    def test_dashboard_route_still_serves_student_home(
        self, logged_in_client
    ):
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        assert b"Dashboard" in response.data
