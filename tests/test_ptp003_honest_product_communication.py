"""PTP-003 Honest Product Communication regression tests.

Covers claim taxonomy phrases, estimated-value labelling, unavailable
explanations, self-reported practice honesty, and empty-state clarity on
Version 1 student surfaces — without redesigning educational cores.
"""

from __future__ import annotations

from pathlib import Path

from app.services.educational_explainability_service import (
    EducationalExplainabilityService,
)
from app.services.product_communication_service import (
    ClaimCategory,
    ProductCommunicationService,
)
from app.services.subject_support_service import SubjectSupportService

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = REPO_ROOT / "app" / "templates"
STANDARD_DOC = (
    REPO_ROOT / "knowledge" / "product" / "PRODUCT_COMMUNICATION_STANDARD.md"
)

STUDENT_TEMPLATE_DIRS = (
    "dashboard",
    "mission",
    "analytics",
    "study_plan",
    "auth",
)


def _read_templates(*relative_dirs: str) -> str:
    chunks: list[str] = []
    for relative in relative_dirs:
        root = TEMPLATE_ROOT / relative
        if not root.exists():
            continue
        for path in root.rglob("*.html"):
            chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)


# ─────────────────────────────────────────────────────────────────────────────
# Service — taxonomy and canonical phrases
# ─────────────────────────────────────────────────────────────────────────────


class TestProductCommunicationPhrases:
    def test_standard_document_exists(self):
        assert STANDARD_DOC.is_file()
        text = STANDARD_DOC.read_text(encoding="utf-8")
        assert "PTP-003" in text
        assert "Observed Fact" in text
        assert "Estimated Value" in text
        assert "Unavailable" in text

    def test_estimated_knowledge_labelled_and_based(self):
        claim = ProductCommunicationService.estimated_knowledge()
        assert claim.category is ClaimCategory.ESTIMATED_VALUE
        assert "Estimated" in claim.label
        assert claim.basis == "Based on your recorded practice outcomes."

    def test_readiness_unavailable_explains_gap(self):
        claim = ProductCommunicationService.estimated_readiness_unavailable()
        assert claim.category is ClaimCategory.UNAVAILABLE
        assert claim.basis == (
            "We need more recorded practice before this estimate becomes available."
        )

    def test_practice_results_self_report(self):
        claim = ProductCommunicationService.practice_results()
        assert claim.category is ClaimCategory.OBSERVED_FACT
        assert "you recorded" in claim.basis.lower()
        assert "today's study session" in claim.basis.lower()

    def test_accuracy_self_report(self):
        claim = ProductCommunicationService.accuracy()
        assert claim.category is ClaimCategory.DERIVED_FACT
        assert "you recorded" in claim.basis.lower()
        assert "verified exam" in claim.basis.lower()


# ─────────────────────────────────────────────────────────────────────────────
# Explainability — readiness narration uses PTP-003 speech
# ─────────────────────────────────────────────────────────────────────────────


class TestReadinessCommunication:
    def test_unavailable_readiness_uses_canonical_phrase(self):
        narrative = EducationalExplainabilityService.explain_composite_readiness(None)
        assert narrative.can_estimate is False
        assert narrative.is_estimate is True
        assert narrative.explanation == (
            ProductCommunicationService.READINESS_UNAVAILABLE
        )
        assert "practice" in narrative.evidence_basis.lower()

    def test_empty_started_topics_uses_canonical_unavailable(self):
        narrative = EducationalExplainabilityService.explain_composite_readiness(
            {
                "total_topics": 10,
                "topics_started": 0,
                "score": 0,
                "coverage_pct": 0,
                "avg_mastery": 0,
                "review_discipline": 0,
            }
        )
        assert narrative.can_estimate is False
        assert narrative.explanation == (
            ProductCommunicationService.READINESS_UNAVAILABLE
        )

    def test_available_readiness_states_self_report_limit(self):
        narrative = EducationalExplainabilityService.explain_composite_readiness(
            {
                "total_topics": 10,
                "topics_started": 3,
                "score": 42.0,
                "coverage_pct": 30.0,
                "avg_mastery": 55.0,
                "review_discipline": 40.0,
            }
        )
        assert narrative.can_estimate is True
        assert narrative.label == "Estimated readiness"
        assert "Estimated" in narrative.explanation
        assert "recorded" in narrative.evidence_basis.lower()
        assert "not independently verified" in narrative.evidence_basis.lower()

    def test_practice_feedback_states_recorded_results(self):
        narrative = EducationalExplainabilityService._feedback_practice_recorded(
            topic="Probability",
            questions_attempted=7,
            questions_correct=5,
            duration_minutes=20,
        )
        observed = " ".join(narrative.what_observed)
        conclusions = " ".join(narrative.honest_conclusions)
        assert ProductCommunicationService.PRACTICE_RESULTS_BASIS in observed
        assert "recorded practice outcomes" in conclusions.lower()


# ─────────────────────────────────────────────────────────────────────────────
# Templates — estimated values labelled; empty states explained
# ─────────────────────────────────────────────────────────────────────────────


class TestStudentFacingCommunicationSurfaces:
    def test_estimated_knowledge_basis_on_dashboard_and_analytics(self):
        text = _read_templates("dashboard", "analytics")
        assert ProductCommunicationService.ESTIMATED_KNOWLEDGE_BASIS in text
        assert 'title="Based on your recorded practice outcomes."' in text
        # Legacy ambiguous hover copy must not remain
        assert "Estimated Knowledge from practice results" not in text

    def test_practice_outcome_capture_states_self_report(self):
        path = TEMPLATE_ROOT / "mission" / "session_practice_outcome.html"
        text = path.read_text(encoding="utf-8")
        assert ProductCommunicationService.PRACTICE_RESULTS_BASIS in text
        assert ProductCommunicationService.PRACTICE_RESULTS_NOT_MASTERY in text

    def test_study_plan_estimated_knowledge_has_visible_basis(self):
        path = TEMPLATE_ROOT / "study_plan" / "view.html"
        text = path.read_text(encoding="utf-8")
        assert "Estimated Knowledge" in text
        assert ProductCommunicationService.ESTIMATED_KNOWLEDGE_BASIS in text
        assert ProductCommunicationService.LEARNING_OUTCOMES_UNAVAILABLE in text

    def test_analytics_accuracy_and_coverage_honesty(self):
        path = TEMPLATE_ROOT / "analytics" / "index.html"
        text = path.read_text(encoding="utf-8")
        assert "Syllabus coverage" in text
        assert ProductCommunicationService.ACCURACY_BASIS in text
        assert ProductCommunicationService.ACCURACY_EMPTY in text
        assert ProductCommunicationService.ESTIMATED_READINESS_SELF_REPORT in text

    def test_dashboard_unavailable_and_legacy_readiness_explained(self):
        path = TEMPLATE_ROOT / "dashboard" / "index.html"
        text = path.read_text(encoding="utf-8")
        assert (
            ProductCommunicationService.READINESS_UNAVAILABLE in text
            or "pcs.READINESS_UNAVAILABLE" in text
        )
        assert (
            "not independently verified exam performance" in text
            or "pcs.ESTIMATED_READINESS_SELF_REPORT" in text
            or "readiness_narrative.evidence_basis" in text
        )

    def test_login_does_not_overclaim_exam_readiness_analytics(self):
        path = TEMPLATE_ROOT / "auth" / "login.html"
        text = path.read_text(encoding="utf-8")
        assert "Exam Readiness Analytics" not in text
        assert (
            ProductCommunicationService.LOGIN_ANALYTICS_FEATURE in text
            or "pcs.LOGIN_ANALYTICS_FEATURE" in text
        )

    def test_no_unexplained_blank_learning_outcomes(self):
        path = TEMPLATE_ROOT / "study_plan" / "view.html"
        text = path.read_text(encoding="utf-8")
        assert "roadmap-outcomes-placeholder" in text
        assert ">—</span>" not in text
        assert ProductCommunicationService.LEARNING_OUTCOMES_UNAVAILABLE in text

    def test_unsupported_papers_still_owned_by_ptp001(self):
        info = SubjectSupportService.resolve("IFoA", "CM2")
        assert info.label == "Coming Soon"
        assert info.allows_plan_creation is False
        assert info.explanation
