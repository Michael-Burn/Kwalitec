"""PTP-001 Supported Subject Integrity regression tests.

Covers support-state resolution, wizard gating, student messaging,
navigation, and refusal of hollow plan creation.
"""

from __future__ import annotations

from datetime import date, timedelta

from app.models.study_plan import StudyPlan
from app.services.subject_support_service import (
    SubjectSupportService,
    SupportStatus,
)

# ─────────────────────────────────────────────────────────────────────────────
# Service — support-state model
# ─────────────────────────────────────────────────────────────────────────────


class TestSubjectSupportResolution:
    def test_supported_cs1(self):
        info = SubjectSupportService.resolve("IFoA", "CS1")
        assert info.status is SupportStatus.SUPPORTED
        assert info.label == "Ready"
        assert info.allows_plan_creation is True
        assert "json" not in info.explanation.lower()
        assert "loader" not in info.explanation.lower()
        assert "verified" in info.explanation.lower() or "ready" in info.title.lower()

    def test_supported_cm1_and_cb2(self):
        for paper in ("CM1", "CB2"):
            info = SubjectSupportService.resolve("IFoA", paper)
            assert info.status is SupportStatus.SUPPORTED
            assert info.allows_plan_creation is True

    def test_coming_soon_cm2(self):
        info = SubjectSupportService.resolve("IFoA", "CM2")
        assert info.status is SupportStatus.COMING_SOON
        assert info.label == "Coming Soon"
        assert info.allows_plan_creation is False
        assert "coming soon" in info.title.lower()
        assert info.alternatives
        assert any("CS1" in label or "CM1" in label for _k, label in info.alternatives)

    def test_not_supported_cfa(self):
        info = SubjectSupportService.resolve("CFA", "Level I")
        assert info.status is SupportStatus.NOT_SUPPORTED
        assert info.label == "Unavailable"
        assert info.allows_plan_creation is False
        assert "unavailable" in info.title.lower()

    def test_not_supported_free_text(self):
        info = SubjectSupportService.resolve(
            "University", "Actuarial Science", free_text_subject=True
        )
        assert info.status is SupportStatus.NOT_SUPPORTED
        assert info.allows_plan_creation is False

    def test_list_supported_includes_version1_papers(self):
        supported = SubjectSupportService.list_supported_examinations()
        papers = {(o.upper(), p.upper()) for o, p in supported}
        assert ("IFOA", "CS1") in papers
        assert ("IFOA", "CM1") in papers
        assert ("IFOA", "CB2") in papers

    def test_category_summary_ifoa_partial(self):
        summary = SubjectSupportService.category_summary("IFoA")
        assert summary.status is SupportStatus.SUPPORTED
        assert (
            "CS1" in summary.supported_paper_codes
            or "CM1" in summary.supported_paper_codes
        )
        assert "Partially" in summary.label or summary.label == "Ready"

    def test_category_summary_cfa_not_supported(self):
        summary = SubjectSupportService.category_summary("CFA")
        assert summary.status is SupportStatus.NOT_SUPPORTED


# ─────────────────────────────────────────────────────────────────────────────
# Wizard — messaging and gating
# ─────────────────────────────────────────────────────────────────────────────


class TestWizardSupportSurface:
    def test_step1_shows_catalogue_availability(self, logged_in_client):
        response = logged_in_client.get("/study-plan/wizard/1")
        assert response.status_code == 200
        body = response.data
        assert b"Ready" in body
        assert b"Coming Soon" in body or b"Coming soon" in body
        assert b"Ready to begin" in body
        assert b"Subject Catalogue" in body or b"Choose Exam" in body or b"exam" in body.lower()

    def test_ready_subject_advances(self, logged_in_client):
        response = logged_in_client.post(
            "/study-plan/wizard/1",
            data={"subject_key": "IFoA:CS1"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert "/study-plan/wizard/2" in response.headers["Location"]

    def test_coming_soon_not_selectable(self, logged_in_client):
        response = logged_in_client.get("/study-plan/wizard/1")
        assert response.status_code == 200
        body = response.data.decode("utf-8")
        assert "Coming Soon" in body
        assert 'value="IFoA:CM2"' not in body
        assert "under preparation" in body.lower()

    def test_coming_soon_cannot_reach_exam_date(self, logged_in_client):
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CM2",
            }
        response = logged_in_client.get(
            "/study-plan/wizard/2", follow_redirects=False
        )
        assert response.status_code == 302
        assert "/study-plan/wizard/1" in response.headers["Location"]


# ─────────────────────────────────────────────────────────────────────────────
# No hollow plans
# ─────────────────────────────────────────────────────────────────────────────


class TestNoHollowPlans:
    def test_review_post_refuses_coming_soon(self, logged_in_client):
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "IFoA",
                "exam_paper": "CM2",
                "exam_sitting": "April 2027",
                "exam_date": (
                    date.today() + timedelta(days=180)
                ).isoformat(),
                "weekday_study_minutes": 90,
                "weekend_study_minutes": 120,
                "current_position": "not_started",
                "study_preference": "Mixed",
                "target_grade": "Pass",
                "preferred_session_minutes": 60,
            }
        before = StudyPlan.query.count()
        response = logged_in_client.post(
            "/study-plan/review",
            data={"confirm": "yes"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert "/study-plan/wizard/1" in response.headers["Location"]
        assert StudyPlan.query.count() == before

    def test_review_post_refuses_unsupported(self, logged_in_client):
        with logged_in_client.session_transaction() as sess:
            sess["wizard_data"] = {
                "exam_category": "ACCA",
                "exam_paper": "FR",
                "exam_sitting": "June 2027",
                "exam_date": (
                    date.today() + timedelta(days=180)
                ).isoformat(),
                "weekday_study_minutes": 90,
                "weekend_study_minutes": 120,
                "current_position": "not_started",
                "study_preference": "Mixed",
                "target_grade": "Pass",
                "preferred_session_minutes": 60,
            }
        before = StudyPlan.query.count()
        response = logged_in_client.post(
            "/study-plan/review",
            data={"confirm": "yes"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert StudyPlan.query.count() == before
        assert b"Unavailable" in response.data or b"unavailable" in response.data or b"not available" in response.data.lower()

    def test_supported_messaging_avoids_implementation_terms(self):
        info = SubjectSupportService.resolve("IFoA", "CS1")
        forbidden = ("json", "loader", "disk", "engine", "curriculum_version", "v2")
        blob = f"{info.title} {info.explanation}".lower()
        for term in forbidden:
            assert term not in blob
