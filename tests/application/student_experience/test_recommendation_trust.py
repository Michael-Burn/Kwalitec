"""EP-008.1 — Application-layer trust mapping tests."""

from __future__ import annotations

from app.application.student_experience.explanation_service import (
    ExplanationService,
)
from app.application.student_experience.recommendation_trust import (
    TRUST_STATE_COMPLETE,
    TRUST_STATE_INCOMPLETE,
    TRUST_STATE_REFUSAL,
    compose_timeliness_line,
    map_recommendation_alternatives,
    resolve_trust_state,
)


def test_compose_timeliness_prefers_distinct_reason():
    line = compose_timeliness_line(
        reason="High educational return before the exam window.",
        why_recommended="Soft recall on cash flow.",
        category="Revision",
        plan_coherence_label="Supports today's mission",
        plan_coherence="aligned",
        exam_countdown_days=30,
    )
    assert line == "High educational return before the exam window."


def test_compose_timeliness_skips_duplicate_reason():
    why = "Not enough evidence yet."
    line = compose_timeliness_line(
        reason=why,
        why_recommended=why,
        category="Deferred",
        plan_coherence="deferred",
        plan_coherence_label="No recommendation yet",
        honest_refusal=True,
    )
    assert line == ""


def test_compose_timeliness_advisory_coherence():
    line = compose_timeliness_line(
        reason="",
        why_recommended="Why text",
        plan_coherence="advisory",
        plan_coherence_label="Advisory — does not replace Today's Mission",
    )
    assert "Advisory" in line


def test_compose_timeliness_category_countdown():
    line = compose_timeliness_line(
        reason="",
        why_recommended="Why text",
        category="Revision",
        exam_countdown_days=12,
    )
    assert line == "Revision priority with 12 days to exam."


def test_map_alternatives_cap_and_refusal():
    raw = [
        {"title": "A", "why_recommended": "wa"},
        {"title": "B", "reason": "wb"},
        {"title": "C", "why_recommended": "wc"},
    ]
    assert len(map_recommendation_alternatives(raw)) == 2
    assert map_recommendation_alternatives(raw, honest_refusal=True) == ()


def test_resolve_trust_state_vocabulary():
    assert resolve_trust_state(honest_refusal=True, is_complete=True) == (
        TRUST_STATE_REFUSAL
    )
    assert resolve_trust_state(honest_refusal=False, is_complete=True) == (
        TRUST_STATE_COMPLETE
    )
    assert resolve_trust_state(honest_refusal=False, is_complete=False) == (
        TRUST_STATE_INCOMPLETE
    )


def test_explanation_service_maps_trust_fields():
    domain = ExplanationService().from_opaque(
        {
            "title": "Cash flow",
            "reason": "Exam window urgency.",
            "why_recommended": "Soft recall on cash flow.",
            "expected_benefit": "Strengthen analysis.",
            "suggested_next_action": "Start a short session.",
            "review_point": "Reassess tomorrow.",
            "confidence_level": "Suggested",
            "supporting_evidence": ["Evidence one."],
            "plan_coherence": "advisory",
            "plan_coherence_label": (
                "Advisory — does not replace Today's Mission"
            ),
            "honest_refusal": False,
            "category": "Revision",
        },
        exam_countdown_days=20,
    )
    assert domain.timeliness_line == "Exam window urgency."
    assert domain.plan_coherence == "advisory"
    assert "Advisory" in domain.plan_coherence_label
    assert domain.completion_loop_line == "Reassess tomorrow."
    assert domain.honest_refusal is False
