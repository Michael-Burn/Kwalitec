"""Quality Gate item 7 — claim-to-capability honesty regressions.

Locks the eight approved honest-copy replacements so Help, brand, Sensei
framing, Learning Check, Quick Check bank, session briefing, and login
pairing stay aligned with live mechanisms.
"""

from __future__ import annotations

from pathlib import Path

from app.application.adaptive_assessment.copy_registry import get_copy
from app.application.session_experience.dto.overview_snapshot import (
    BeginSessionActionSnapshot,
    OverviewSnapshot,
)
from app.brand_identity import PRODUCT_DESCRIPTOR
from app.presentation.product_language import HISTORY_EPISTEMOLOGY_BRIDGE
from app.presentation.session.view_models import overview_vm
from app.services.alpha_onboarding_service import SENSEI_HANDOFF_SENTENCE
from app.services.product_communication_service import ProductCommunicationService

ROOT = Path(__file__).resolve().parents[1]
HELP = (ROOT / "app/templates/alpha/help.html").read_text(encoding="utf-8")
MANIFEST = (
    ROOT / "app/static/branding/manifest.webmanifest"
).read_text(encoding="utf-8")
ENTRY = (
    ROOT / "app/templates/student/assessment/entry.html"
).read_text(encoding="utf-8")
WELCOME = (
    ROOT / "app/templates/partials/welcome_modal.html"
).read_text(encoding="utf-8")

QUICK_CHECK_HONEST_DEFAULTS = {
    "session.quick_check.frame": (
        "Quick check. Short practice on today's topic."
    ),
    "session.readiness_check.frame": (
        "Readiness check. Practice for today's topic; it does not "
        "predict your result."
    ),
    "explain.why_body": (
        "This check is short practice inside today's Session. "
        "Your answers are practice evidence, not a grade, and they do not "
        "rewrite today's plan."
    ),
    "feedback.use_to_guide": (
        "This stays as practice evidence from today's check."
    ),
    "readiness.non_guarantee": (
        "This is practice for today's focus. It does not predict your result."
    ),
    "quick_check.completion.uncertain": (
        "Some parts may still feel uncertain, that is expected after a "
        "short check."
    ),
    "quick_check.completion.mission_benefit": (
        "Today's Mission continues as planned. This check was practice "
        "on the same focus."
    ),
    "framing.context.purpose": (
        "This Quick Check is short practice on {focus} inside today's "
        "Mission."
    ),
    "framing.context.benefit": "This is practice evidence, not a grade.",
    "framing.context.why_expanded": (
        "You are seeing this check because today's Mission focus on "
        "{focus} includes a short practice check. Answers are practice "
        "on this topic. They are not a grade, and they do not change "
        "today's Mission choice."
    ),
    "framing.summary.meaning": (
        "That was practice on how the ideas are landing for you. "
        "Today's Mission continues from your plan."
    ),
    "session.deep_check.frame": "Careful check on this topic. No grades.",
}


def test_help_reflection_faq_aligns_with_glossary_no_rerank():
    assert "less signal for Sensei’s next recommendation" not in HELP
    assert "Reflection does not re-rank today’s Mission." in HELP
    assert "Sensei reflection does not re-rank today's Mission." in HELP
    assert "Readiness signal" not in HELP
    assert (
        "Today's Session follows your Study Plan in syllabus order." in HELP
    )


def test_help_revision_glossary_is_spacing_not_mission_support():
    """A5-7: Revision is the spacing board, not Mission support."""
    assert "supports today's Mission" not in HELP
    assert "supports today’s Mission" not in HELP
    assert (
        "Follow-up practice on previously completed material when the "
        "schedule says it is due for review. Distinct from today's Mission, "
        "never a second Mission or competing daily focus."
    ) in HELP


def test_brand_descriptor_and_manifest_match_without_exam_ready():
    assert PRODUCT_DESCRIPTOR == "Study guidance for your exam plan"
    assert "Exam-ready" not in PRODUCT_DESCRIPTOR
    assert PRODUCT_DESCRIPTOR in MANIFEST
    assert "Exam-ready" not in MANIFEST
    assert (
        "Kwalitec — Study guidance for your exam plan. "
        "Know exactly what to study next."
    ) in MANIFEST


def test_sensei_mentor_language_removed_honest_instances_untouched():
    assert "educational mentor" not in HELP
    assert "mentor voice" not in HELP
    assert "mentor narrative" not in HELP
    assert "The Sensei voice across Mission" in HELP
    assert "Kwalitec’s educational voice for focus" in HELP
    assert "Study Sensei’s learning story" in HELP
    assert "learning story" in HISTORY_EPISTEMOLOGY_BRIDGE
    assert "mentor" not in HISTORY_EPISTEMOLOGY_BRIDGE.lower()

    assert (
        "Study Sensei is how Kwalitec guides your daily learning decisions."
        in WELCOME
    )
    assert "mentor" not in WELCOME.lower()
    assert SENSEI_HANDOFF_SENTENCE == (
        "Study Sensei is how Kwalitec guides your daily learning decisions."
    )
    assert "What does Study Sensei do?" in HELP
    assert (
        "Study Sensei is how Kwalitec guides your daily learning decisions. "
        "Sensei prepares today’s Mission"
    ) in HELP


def test_learning_check_entry_does_not_claim_sensei_support():
    assert "help Study Sensei" not in ENTRY
    assert "understand how to support you" not in ENTRY
    assert "Practice on this topic to support" in ENTRY
    assert "today’s Session." in ENTRY
    assert "that practice stays with this check." in ENTRY
    assert "It does not change Sensei’s Mission choice" in ENTRY
    assert "it does not rank you." in ENTRY
    assert "we use what you shared to support learning" not in ENTRY


def test_quick_check_copy_bank_matches_honest_replacements():
    for key, expected in QUICK_CHECK_HONEST_DEFAULTS.items():
        assert get_copy(key).default == expected, key


def test_session_briefing_uses_coverage_and_display_estimate():
    with_estimate = overview_vm(
        OverviewSnapshot(
            experience_session_id="es-1",
            student_id="stu-1",
            session_id="sess-1",
            objective="Coverage practice",
            estimated_minutes=30,
            activity_count=3,
            expected_readiness_improvement=0.12,
            can_begin=True,
            begin_action=BeginSessionActionSnapshot(
                can_begin=True, session_id="sess-1"
            ),
        )
    )
    assert "coverage movement" in with_estimate.expected_improvement_label
    assert "display estimate only" in with_estimate.expected_improvement_label
    assert "readiness movement" not in with_estimate.expected_improvement_label

    without_estimate = overview_vm(
        OverviewSnapshot(
            experience_session_id="es-1",
            student_id="stu-1",
            session_id="sess-1",
            objective="Coverage practice",
            estimated_minutes=30,
            activity_count=3,
            expected_readiness_improvement=None,
            can_begin=True,
            begin_action=BeginSessionActionSnapshot(
                can_begin=True, session_id="sess-1"
            ),
        )
    )
    assert (
        "advances coverage on today's topic"
        in without_estimate.expected_improvement_label
    )
    assert "strengthen readiness" not in without_estimate.expected_improvement_label
    assert "readiness movement" not in without_estimate.expected_improvement_label


def test_login_readiness_pairing_uses_shown_not_insights():
    assert (
        ProductCommunicationService.LOGIN_ANALYTICS_FEATURE
        == "Estimated readiness shown"
    )
    assert "insights" not in ProductCommunicationService.LOGIN_ANALYTICS_FEATURE
