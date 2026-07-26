"""EP-006.2 — MES delivery presentation contract tests.

Asserts that authored Runtime A Meaningful Explanation Schema fields reach
Home / Coach view models and that reason-code re-narration is not used when
schema-complete payloads are present.
"""

from __future__ import annotations

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.student_experience.explanation_service import (
    ExplanationService,
)
from app.infrastructure.adapters.educational_runtime_bridge import (
    recommendation_mapper as rec_mapper,
)
from app.presentation.student.view_models import explanation_vm, home_vm


def _schema_complete_row(**overrides):
    row = {
        "title": "Cash flow statements",
        "reason": "High educational return before the exam window.",
        "why_recommended": (
            "Your recent practice shows soft recall on cash flow statements, "
            "so a focused session will protect what you have already learned."
        ),
        "expected_benefit": "Strengthen exam readiness on cash flow analysis.",
        "next_action": "Start a 25-minute cash flow practice session.",
        "suggested_next_action": "Start a 25-minute cash flow practice session.",
        "confidence_level": "Suggested",
        "supporting_evidence": [
            "Two recent practice attempts scored below your topic average.",
            "Cash flow is on the near-term revision list.",
            "Syllabus coverage for this topic is incomplete.",
        ],
        "review_point": "Reassess after tonight's practice set.",
        "decision_ladder_rank": 1,
        "plan_coherence": "aligned",
        "explanation_schema_version": "1.0",
        "explanation_level": 2,
        "explanation_schema_complete": True,
        "confidence_basis": "Based on recent practice outcomes.",
        "category": "Revision",
        "priority": "High",
    }
    row.update(overrides)
    return row


def test_bridge_mapper_preserves_authored_mes_keys():
    primary = _schema_complete_row()
    projection = rec_mapper.map_recommendation_to_projection(
        student_id="stu-1",
        primary=primary,
        estimated_minutes=25,
    )
    assert projection is not None
    explanation = projection["explanation"]
    assert explanation["why_recommended"] == primary["why_recommended"]
    assert explanation["supporting_evidence"] == primary["supporting_evidence"]
    assert (
        explanation["suggested_next_action"] == primary["suggested_next_action"]
    )
    assert explanation["review_point"] == primary["review_point"]
    assert explanation["confidence_level"] == primary["confidence_level"]
    assert projection["why_recommended"] == primary["why_recommended"]
    assert projection["review_point"] == primary["review_point"]


def test_explanation_service_passes_through_authored_mes():
    svc = ExplanationService()
    primary = _schema_complete_row()
    domain = svc.from_opaque(primary)
    assert domain.why_recommended == primary["why_recommended"]
    assert domain.suggested_next_action == primary["suggested_next_action"]
    assert domain.review_point == primary["review_point"]
    assert list(domain.evidence_points) == primary["supporting_evidence"]
    assert domain.confidence_label == primary["confidence_level"]
    # Must not re-narrate from missing reason codes into a different why.
    assert "highest-value next step" not in domain.why_recommended.lower()


def test_explanation_service_fallback_when_schema_incomplete():
    svc = ExplanationService()
    domain = svc.from_opaque(
        {
            "topic_title": "Tax",
            "reason_codes": ("high_roi",),
            "evidence_points": ("Recent practice showed a gap.",),
            "expected_benefit": "Raise exam readiness",
            "priority_band": "high",
        }
    )
    assert "Tax" in domain.why_recommended or "tax" in domain.why_recommended.lower()
    assert domain.evidence_points


def test_home_vm_carries_mandatory_mes_fields():
    snap = HomeSnapshot(
        student_id="stu-1",
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
            why_recommended=(
                "Your recent practice shows soft recall on cash flow statements."
            ),
            evidence_points=(
                "Two recent practice attempts scored below your topic average.",
                "Cash flow is on the near-term revision list.",
            ),
            expected_benefit="Strengthen exam readiness on cash flow analysis.",
            confidence_label="Suggested",
            suggested_next_action="Start a 25-minute cash flow practice session.",
            review_point="Reassess after tonight's practice set.",
            confidence_basis="Based on recent practice outcomes.",
            is_complete=True,
        ),
        has_recommendation=True,
        can_start_session=True,
    )
    page = home_vm(snap, unified_journey=False)
    assert page.explanation is not None
    assert page.explanation.why_recommended.startswith("Your recent practice")
    assert page.explanation.suggested_next_action.startswith("Start a 25-minute")
    assert page.explanation.review_point.startswith("Reassess")
    assert len(page.explanation.evidence_points) >= 2
    assert page.explanation.has_disclosure is True
    # Coach L1 includes authored why and next; disclosure present → no hard clip loss.
    assert "soft recall" in page.coach_insight
    assert "25-minute" in page.coach_insight
    # EP-008.1 structured coach still carries authored strings.
    if page.coach_trust and page.coach_trust.has_content:
        assert "soft recall" in page.coach_trust.why
        assert "25-minute" in page.coach_trust.next


def test_explanation_vm_preserves_review_point_and_next_action():
    vm = explanation_vm(
        ExplanationSnapshot(
            summary="Focus on Ethics.",
            why_recommended="Ethics is high value with the exam approaching.",
            evidence_points=("Syllabus weight is high.", "Recent miss on scenario."),
            expected_benefit="Protect ethics marks.",
            confidence_label="Estimated",
            suggested_next_action="Complete one ethics scenario set.",
            review_point="Review after the next timed set.",
            confidence_basis="Thin recent evidence.",
            is_complete=True,
        )
    )
    assert vm is not None
    assert vm.suggested_next_action == "Complete one ethics scenario set."
    assert vm.review_point == "Review after the next timed set."
    assert vm.confidence_basis == "Thin recent evidence."
    assert len(vm.evidence_points) == 2
