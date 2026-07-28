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


def test_pc001_sidebar_and_settings_use_product_check_in_label():
    """PC-001 / RP002-NCR-001 — nav entry matches Product Check-in canon."""
    sidebar = (ROOT / "app/templates/partials/sidebar.html").read_text(
        encoding="utf-8"
    )
    settings = (ROOT / "app/templates/settings/index.html").read_text(
        encoding="utf-8"
    )
    assert "Product Check-in" in sidebar
    assert "Share Feedback" not in sidebar
    assert "Product Check-in" in settings
    assert "Share Feedback" not in settings
    assert "research.checkin" in sidebar or "url_for('research.checkin'" in sidebar


def test_pc002_commitment_reflection_names_system_authority(app, ctx):
    """PC-002 / RP002-NCR-002 — update field names System, not unnamed we."""
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
    page = SimpleNamespace(
        home=page_home,
        shell=SimpleNamespace(active_surface="home", navigation=()),
    )
    reflection_form = SimpleNamespace(
        hidden_tag=lambda: "",
        recommendation_key=lambda: "",
    )
    with app.test_request_context("/student/"):
        html = render_template(
            "student/home.html",
            page=page,
            form=None,
            reflection_form=reflection_form,
        )
    assert "What the system updated" in html
    assert "What we updated" not in html
    assert 'data-reflection-field="what_was_learned"' in html


def test_pc003_onboarding_header_count_matches_steps(app, ctx):
    """PC-003 / RP002-NCR-003 — orientation count matches ONBOARDING_STEPS."""
    steps = AlphaOnboardingService.steps()
    assert len(steps) == 6
    with app.test_request_context("/alpha/onboarding"):
        html = render_template(
            "alpha/onboarding.html",
            steps=steps,
            internal_alpha_label="Internal Alpha",
        )
    assert f"{len(steps)} ideas" in html
    assert "five ideas" not in html
    assert "Step 1 of 6" in html
    assert "Step 6 of 6" in html


def test_pc004_learning_check_attributes_support_to_study_sensei():
    """PC-004 / RP002-NCR-004 — Learning Check support speech is Sensei."""
    entry = (ROOT / "app/templates/student/assessment/entry.html").read_text(
        encoding="utf-8"
    )
    assert "help Study Sensei" in entry
    assert "understand how to support you" in entry
    assert "help Kwalitec" not in entry
    assert "Learning Check" in entry
