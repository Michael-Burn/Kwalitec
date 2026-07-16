"""EIP-006 Version 1 Educational State Refinement regression tests.

Version 1 student-facing educational states are only:
  Study Progress, Estimated Knowledge, Educational Guidance.

Competence and Mastery remain educational constructs but must not appear as
Version 1 student-facing educational states without constitutionally sufficient
warrant. Practice-backed ``mastery_score`` is Estimated Knowledge meaning.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest

from app.extensions import db
from app.models.topic_progress import TopicProgress
from app.services.educational_explainability_service import (
    EducationalExplainabilityService,
)
from app.services.planning_service import PlanningService
from app.services.study_plan_service import StudyPlanService

REPO_ROOT = Path(__file__).resolve().parents[1]

# Student-facing HTML / narration templates under review for EIP-006.
_STUDENT_SURFACE_FILES = (
    REPO_ROOT / "app" / "templates" / "dashboard" / "index.html",
    REPO_ROOT / "app" / "templates" / "analytics" / "index.html",
    REPO_ROOT / "app" / "templates" / "mission" / "index.html",
    REPO_ROOT / "app" / "templates" / "study_plan" / "view.html",
    REPO_ROOT / "app" / "templates" / "study_plan" / "wizard_step_4.html",
    REPO_ROOT / "app" / "services" / "educational_explainability_service.py",
    REPO_ROOT / "app" / "services" / "readiness_service.py",
    REPO_ROOT / "app" / "services" / "recommendation_service.py",
    REPO_ROOT / "app" / "settings" / "routes.py",
)

# Phrases that would claim Mastery as a Version 1 student educational state.
_FORBIDDEN_MASTERY_CLAIMS = (
    "Estimated Mastery",
    "estimated mastery",
)


# ═══════════════════════════════════════════════════════════════════════════
# Negative regression
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.usefixtures("ctx")
class TestNegativeNoUnsupportedMasteryClaims:
    def test_student_surfaces_do_not_label_estimated_mastery(self) -> None:
        """V1 student surfaces must not claim Estimated Mastery."""
        for path in _STUDENT_SURFACE_FILES:
            text = path.read_text(encoding="utf-8")
            for phrase in _FORBIDDEN_MASTERY_CLAIMS:
                assert phrase not in text, (
                    f"{path.relative_to(REPO_ROOT)} still claims {phrase!r}"
                )

    def test_coverage_completion_does_not_mint_estimated_knowledge(self, user) -> None:
        """Study Progress alone must not gate Estimated Knowledge display."""
        progress = TopicProgress(
            user_id=user.id,
            topic_id=1,
            completed=True,
            mastery_score=0.0,
            average_accuracy=None,
            current_stage=TopicProgress.STAGE_COMPLETED,
            confidence="High",
        )
        db.session.add(progress)
        db.session.commit()

        assert progress.has_estimated_knowledge is False
        assert progress.has_estimated_mastery is False

    def test_mastered_stage_never_shown_as_mastered_to_students(self) -> None:
        label = EducationalExplainabilityService.student_stage_label("Mastered")
        assert "Mastered" not in label
        assert "mastery" not in label.lower()
        assert "knowledge" in label.lower()

    def test_mission_narrative_does_not_claim_mastery(self) -> None:
        narrative = EducationalExplainabilityService.build_mission_narrative(
            mission_title="Topic A",
            syllabus_coverage_pct=25.0,
            completed_topics=1,
            total_topics=4,
        )
        assert narrative is not None
        joined = " ".join(narrative.estimates)
        assert "Estimated Mastery" not in joined
        assert "Estimated Knowledge" in joined


# ═══════════════════════════════════════════════════════════════════════════
# Positive regression
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.usefixtures("ctx")
class TestPositiveVersion1EducationalStates:
    def test_evidence_gates_estimated_knowledge_alias(self, user) -> None:
        progress = TopicProgress(
            user_id=user.id,
            topic_id=1,
            completed=True,
            mastery_score=72.0,
            average_accuracy=72.0,
            current_stage=TopicProgress.STAGE_PRACTISING,
            confidence="High",
        )
        db.session.add(progress)
        db.session.commit()

        assert progress.has_estimated_knowledge is True
        assert progress.has_estimated_mastery is True  # compatibility alias

    def test_coverage_readiness_names_estimated_knowledge(self) -> None:
        narrative = EducationalExplainabilityService.explain_coverage_readiness(
            readiness_percentage=0.55
        )
        assert "not Estimated Knowledge" in narrative.explanation
        assert "Estimated Mastery" not in narrative.explanation
        assert narrative.is_estimate is False

    def test_dashboard_uses_estimated_knowledge_label(
        self, app, user, logged_in_client
    ) -> None:
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

        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Estimated Mastery" not in body
        # Guidance / coverage story remains present
        lower = body.lower()
        assert (
            "Study Progress" in body
            or "Learning Progress" in body
            or "mission" in lower
        )

    def test_analytics_chart_uses_estimated_knowledge(
        self, app, user, logged_in_client
    ) -> None:
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
        response = logged_in_client.get("/analytics/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Estimated Mastery" not in body
        assert "Estimated Knowledge" in body

    def test_mission_page_explains_estimated_knowledge(
        self, app, user, logged_in_client
    ) -> None:
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

        response = logged_in_client.get("/missions/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Estimated Mastery" not in body
        assert "Estimated Knowledge" in body
        assert "Study Progress" in body

    def test_roadmap_label_is_estimated_knowledge(
        self, app, user, logged_in_client
    ) -> None:
        plan = StudyPlanService.create_study_plan(
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
        response = logged_in_client.get(f"/study-plan/{plan.id}")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Estimated Mastery" not in body
