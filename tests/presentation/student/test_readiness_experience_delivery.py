"""EP-006.4 — readiness experience delivery regression tests.

Covers readiness driver delivery, explanation completeness, Home rendering,
and fallback when the readiness surface is incomplete or unavailable.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

from flask import render_template

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.student_experience.dto.readiness_explanation_snapshot import (
    ReadinessExplanationSnapshot,
)
from app.application.student_experience.readiness_explanation import (
    load_home_readiness_explanation,
    readiness_explanation_from_narrative,
)
from app.presentation.intelligence_surface.adapter import (
    RuntimeAPresentationAdapter,
)
from app.presentation.student.view_models import home_vm
from app.services.educational_explainability_service import ReadinessNarrative


def _schema_complete_readiness_surface(**overrides):
    surface = {
        "explanation_schema_complete": True,
        "judgement": "Estimated readiness around 62%",
        "why_this_estimate": (
            "Coverage and practice density support a mid-band estimate."
        ),
        "supporting_evidence": [
            "6 of 10 topics started.",
            "Average Estimated Knowledge on started topics is moderate.",
        ],
        "confidence_level": "Suggested",
        "confidence_basis": "Based on coverage and recent practice density.",
        "expected_benefit": "A focused weak-topic session should raise readiness.",
        "suggested_next_action": "Practise Geometry proofs.",
        "review_point": "Reassess after two more practice sessions.",
        "readiness_drivers": [
            {
                "driver_id": "curriculum_coverage",
                "label": "Curriculum coverage",
                "value": 55.0,
            },
            {
                "driver_id": "knowledge_strength",
                "label": "Knowledge strength",
                "value": 68.0,
            },
            {
                "driver_id": "mission_discipline",
                "label": "Review discipline",
                "value": 70.0,
            },
        ],
        "explanation_schema_version": "1.0",
        "explanation_level": 2,
        "readiness": {"score": 62.0},
    }
    surface.update(overrides)
    return surface


def test_readiness_driver_delivery_from_schema_surface():
    surface = _schema_complete_readiness_surface()
    narrative = RuntimeAPresentationAdapter.readiness_narrative(surface)
    snap = readiness_explanation_from_narrative(
        narrative, schema_complete=True
    )
    assert snap.is_complete is True
    assert len(snap.readiness_drivers) >= 3
    assert any("Curriculum coverage" in d for d in snap.readiness_drivers)
    assert snap.why_this_estimate.startswith("Coverage and practice")
    assert snap.suggested_next_action.startswith("Practise Geometry")
    assert snap.review_point.startswith("Reassess")
    assert snap.confidence_label == "Suggested"
    assert "coverage" in snap.confidence_basis.lower()


def test_explanation_completeness_requires_drivers_why_confidence_next():
    incomplete = readiness_explanation_from_narrative(
        ReadinessNarrative(
            label="Estimated readiness",
            percentage=50.0,
            explanation="Thin estimate.",
            evidence_basis="Limited practice.",
            can_estimate=True,
            is_estimate=True,
            why_this_estimate="Thin estimate.",
            confidence_label="Suggested",
            suggested_next_action="",
            readiness_drivers=(),
        ),
        schema_complete=False,
    )
    assert incomplete.is_complete is False
    assert incomplete.readiness_drivers == ()

    complete = readiness_explanation_from_narrative(
        ReadinessNarrative(
            label="Estimated readiness",
            percentage=62.0,
            explanation="Coverage supports a mid-band estimate.",
            evidence_basis="Coverage and practice.",
            can_estimate=True,
            is_estimate=True,
            why_this_estimate="Coverage supports a mid-band estimate.",
            confidence_label="Suggested",
            confidence_basis="Based on coverage.",
            suggested_next_action="Practise Geometry proofs.",
            review_point="Reassess after two more practice sessions.",
            readiness_drivers=(
                "Curriculum coverage (~55%)",
                "Knowledge strength (~68%)",
            ),
            supporting_evidence=("6 of 10 topics started.",),
        ),
        schema_complete=False,
    )
    assert complete.is_complete is True


def test_home_vm_binds_authored_readiness_mes():
    snap = HomeSnapshot(
        student_id="1",
        greeting="Welcome back",
        examination_label="ACCA AA",
        exam_countdown_days=30,
        exam_readiness=0.62,
        exam_readiness_label="On Track",
        recommendation_title="Cash flow statements",
        recommendation_summary="Focus on cash flow statements next.",
        estimated_study_minutes=25,
        explanation=ExplanationSnapshot(
            summary="Focus on cash flow statements next.",
            why_recommended="Soft recall on cash flow.",
            suggested_next_action="Start cash flow practice.",
            is_complete=True,
        ),
        readiness_explanation=ReadinessExplanationSnapshot(
            why_this_estimate=(
                "Coverage and practice density support a mid-band estimate."
            ),
            confidence_label="Suggested",
            confidence_basis="Based on coverage and recent practice density.",
            suggested_next_action="Practise Geometry proofs.",
            review_point="Reassess after two more practice sessions.",
            readiness_drivers=(
                "Curriculum coverage (~55%)",
                "Knowledge strength (~68%)",
                "Review discipline (~70%)",
            ),
            supporting_evidence=(
                "6 of 10 topics started.",
                "Average Estimated Knowledge on started topics is moderate.",
            ),
            expected_benefit="A focused weak-topic session should raise readiness.",
            can_estimate=True,
            is_complete=True,
        ),
        has_recommendation=True,
    )
    page = home_vm(snap, unified_journey=False)
    assert page.readiness.why_this_estimate.startswith("Coverage and practice")
    # CQ-002 / CR1: hero owns primary Next — readiness next is suppressed.
    assert page.readiness.suggested_next_action == ""
    assert page.readiness.review_point.startswith("Reassess")
    assert len(page.readiness.readiness_drivers) >= 3
    assert page.readiness.confidence_label == "Suggested"
    assert "coverage" in page.readiness.confidence_basis.lower()
    assert page.readiness.has_disclosure is True
    assert page.explanation is not None
    assert "cash flow" in page.explanation.suggested_next_action.lower()


def test_home_template_renders_readiness_drivers_and_review(app, ctx):
    snap = HomeSnapshot(
        student_id="1",
        greeting="Welcome back",
        examination_label="ACCA AA",
        exam_countdown_days=30,
        exam_readiness=0.62,
        exam_readiness_label="On Track",
        recommendation_title="Cash flow statements",
        recommendation_summary="Focus on cash flow.",
        estimated_study_minutes=25,
        readiness_explanation=ReadinessExplanationSnapshot(
            why_this_estimate=(
                "Coverage and practice density support a mid-band estimate."
            ),
            confidence_label="Suggested",
            confidence_basis="Based on coverage and recent practice density.",
            suggested_next_action="Practise Geometry proofs.",
            review_point="Reassess after two more practice sessions.",
            readiness_drivers=(
                "Curriculum coverage (~55%)",
                "Knowledge strength (~68%)",
            ),
            supporting_evidence=("6 of 10 topics started.",),
            is_complete=True,
        ),
        has_recommendation=True,
    )
    page_home = home_vm(snap, unified_journey=False)
    page = SimpleNamespace(
        home=page_home,
        shell=SimpleNamespace(active_surface="home", navigation=()),
    )
    with app.test_request_context("/student/"):
        html = render_template("student/home.html", page=page, form=None)
    assert 'data-mes-field="readiness_drivers"' in html
    assert "Curriculum coverage" in html
    assert 'data-mes-field="readiness_next_action"' in html
    assert "Practise Geometry proofs" in html
    assert 'data-mes-field="review_point"' in html
    assert "Reassess after two more" in html
    assert "Why this estimate?" in html
    assert 'data-mes-field="confidence_level"' in html
    assert "Coverage and practice density" in html


def test_fallback_when_readiness_explanation_absent():
    snap = HomeSnapshot(
        student_id="1",
        greeting="Welcome back",
        exam_readiness=0.4,
        exam_readiness_label="Building",
        recommendation_title="Tax",
        explanation=ExplanationSnapshot(
            summary="Focus on Tax.",
            why_recommended="Tax is high value.",
            confidence_label="Suggested",
            confidence_basis="Based on recent practice outcomes.",
            suggested_next_action="Complete one tax scenario set.",
            review_point="Review after the next timed set.",
            evidence_points=("Recent miss on scenario.",),
            is_complete=True,
        ),
        readiness_explanation=None,
        has_recommendation=True,
    )
    page = home_vm(snap, unified_journey=False)
    assert page.readiness.readiness_drivers == ()
    # CQ-002 / CR1: do not duplicate hero Next into the Readiness panel.
    assert page.readiness.suggested_next_action == ""
    assert page.explanation is not None
    assert page.explanation.suggested_next_action.startswith("Complete one tax")
    assert page.readiness.review_point.startswith("Review after")
    assert page.readiness.confidence_basis.startswith("Based on recent")
    assert page.readiness.has_disclosure is True


def test_fallback_when_load_fails_open():
    with patch(
        "app.services.readiness_service.ReadinessService."
        "get_dashboard_readiness_surface",
        side_effect=RuntimeError("surface unavailable"),
    ):
        assert load_home_readiness_explanation("1") is None


def test_fallback_when_student_id_not_numeric():
    assert load_home_readiness_explanation("stu-not-numeric") is None


def test_load_home_readiness_explanation_pass_through():
    surface = _schema_complete_readiness_surface()
    with patch(
        "app.services.readiness_service.ReadinessService."
        "get_dashboard_readiness_surface",
        return_value=surface,
    ):
        snap = load_home_readiness_explanation("42")
    assert snap is not None
    assert snap.is_complete is True
    assert len(snap.readiness_drivers) >= 3
    assert snap.suggested_next_action.startswith("Practise Geometry")
    assert snap.review_point.startswith("Reassess")
