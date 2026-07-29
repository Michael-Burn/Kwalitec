"""RR-002.1 — Navigation & educational consistency remediation.

Closes RP-002 Open PC findings PC-001–PC-004 (RP002-NCR-001–004)
without changing algorithms, schema, curriculum, or feature flags.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from flask import render_template

from app.application.student_experience.dto.commitment_reflection_snapshot import (
    CommitmentReflectionSnapshot,
)
from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.student_experience.dto.recommendation_commitment_snapshot import (
    RecommendationCommitmentSnapshot,
)
from app.application.student_experience.recommendation_commitment import (
    CONTINUITY_REFLECTION,
    WHAT_WAS_LEARNED_HUMBLE,
)
from app.presentation.student.view_models import home_vm
from app.services.alpha_onboarding_service import AlphaOnboardingService

ROOT = Path(__file__).resolve().parents[3]


def test_pc001_settings_and_help_use_product_check_in_label():
    """PC-001 / UX-003 — Product Check-in canon via settings.share_feedback."""
    settings = (ROOT / "app/templates/settings/index.html").read_text(encoding="utf-8")
    profile = (ROOT / "app/templates/student/profile.html").read_text(encoding="utf-8")
    help_page = (ROOT / "app/templates/alpha/help.html").read_text(encoding="utf-8")
    assert "Product Check-in" in settings
    assert "Share Feedback" not in settings
    assert "Product Check-in" in profile
    assert "Product Check-in" in help_page
    assert "Share Feedback" not in help_page
    assert "settings.share_feedback" in settings
    assert "settings.share_feedback" in profile
    assert "research.checkin" in help_page or "url_for('research.checkin'" in help_page


def test_pc002_commitment_reflection_names_system_authority(app, ctx):
    """PC-002 / SOP-001 — commitment reflection chrome is not hosted on Home."""
    from tests.presentation.student.helpers import render_student_home

    reflection = CommitmentReflectionSnapshot(
        what_you_did="Completed: Cash flow statements",
        what_changed="Reassess after tonight's practice set.",
        why_it_mattered="Strengthen exam readiness on cash flow analysis.",
        what_was_learned=WHAT_WAS_LEARNED_HUMBLE,
        what_happens_next="Return Home for the next Mission.",
    )
    commitment = RecommendationCommitmentSnapshot(
        state="completed",
        title="Cash flow statements",
        continuity_line=CONTINUITY_REFLECTION,
        reflection=reflection,
    )
    snap = HomeSnapshot(
        student_id="stu-rr021",
        greeting="Welcome back",
        examination_label="ACCA AA",
        exam_countdown_days=30,
        exam_readiness=0.62,
        exam_readiness_label="Exam Readiness",
        recommendation_title="Cash flow statements",
        recommendation_summary="Focus on cash flow statements next.",
        estimated_study_minutes=25,
        expected_readiness_improvement=0.03,
        explanation=ExplanationSnapshot(
            summary="Focus on cash flow statements next.",
            why_recommended="Soft recall on cash flow statements.",
            evidence_points=("Recent practice below topic average.",),
            expected_benefit="Strengthen cash flow analysis.",
            confidence_label="Suggested",
            suggested_next_action="Start a 25-minute practice Session.",
            review_point="Reassess after tonight's practice.",
            confidence_basis="Based on recent practice outcomes.",
            is_complete=True,
        ),
        has_recommendation=True,
        can_start_session=False,
        commitment=commitment,
    )
    page_home = home_vm(snap, unified_journey=False)
    reflection_form = SimpleNamespace(
        hidden_tag=lambda: "",
        recommendation_key=lambda: "",
    )
    html = render_student_home(app, page_home, reflection_form=reflection_form)
    assert "What we updated" not in html
    assert 'data-reflection-field="what_was_learned"' not in html
    assert "ds-os-home" in html
    assert "Mission" in WHAT_WAS_LEARNED_HUMBLE


def test_pc003_onboarding_header_count_matches_steps(app, ctx):
    """PC-003 — orientation count matches ONBOARDING_STEPS (four ideas)."""
    steps = AlphaOnboardingService.steps()
    assert len(steps) == 4
    with app.test_request_context("/alpha/onboarding"):
        html = render_template(
            "alpha/onboarding.html",
            steps=steps,
            internal_alpha_label="Internal Alpha",
        )
    assert f"Step 1 of {len(steps)}" in html
    assert f"Step {len(steps)} of {len(steps)}" in html
    assert "Step 1 of 6" not in html


def test_pc004_learning_check_attributes_support_to_study_sensei():
    """PC-004 / RP002-NCR-004 — Learning Check support speech is Sensei."""
    entry = (ROOT / "app/templates/student/assessment/entry.html").read_text(
        encoding="utf-8"
    )
    assert "help Study Sensei" in entry
    assert "understand how to support you" in entry
    assert "help Kwalitec" not in entry
    assert "Learning Check" in entry
