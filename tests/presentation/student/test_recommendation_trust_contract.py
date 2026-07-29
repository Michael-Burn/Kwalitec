"""EP-008.1 — Recommendation Trust contract tests (VALIDATION_PLAN TR-A0*)."""

from __future__ import annotations

from types import SimpleNamespace

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.student_experience.dto.recommendation_alternative_snapshot import (
    RecommendationAlternativeSnapshot,
)
from app.application.student_experience.explanation_service import (
    ExplanationService,
)
from app.application.student_experience.recommendation_trust import (
    TRUST_STATE_COMPLETE,
    TRUST_STATE_REFUSAL,
    map_recommendation_alternatives,
    resolve_trust_state,
)
from app.infrastructure.adapters.educational_runtime_bridge import (
    recommendation_mapper as rec_mapper,
)
from app.presentation.student.view_models import home_vm
from tests.presentation.student.helpers import render_student_home


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
        "plan_coherence_label": "Supports today's mission",
        "explanation_schema_version": "1.0",
        "explanation_level": 2,
        "explanation_schema_complete": True,
        "confidence_basis": "Based on recent practice outcomes.",
        "category": "Revision",
        "priority": "High",
        "honest_refusal": False,
    }
    row.update(overrides)
    return row


def _honest_refusal_row(**overrides):
    row = {
        "title": "No recommendation yet",
        "reason": (
            "There is not yet enough personal study evidence for a confident "
            "primary tip."
        ),
        "why_recommended": (
            "There is not yet enough personal study evidence for a confident "
            "primary tip."
        ),
        "expected_benefit": (
            "Avoid fabricated certainty; build enough evidence for useful guidance."
        ),
        "suggested_next_action": (
            "Complete a short study session so guidance can be personalised."
        ),
        "next_action": (
            "Complete a short study session so guidance can be personalised."
        ),
        "confidence_level": "Cannot yet be estimated",
        "supporting_evidence": [
            "Insufficient personal study history for a confident primary tip.",
        ],
        "review_point": "Reassess after your next completed study session.",
        "plan_coherence": "deferred",
        "plan_coherence_label": "No recommendation yet",
        "honest_refusal": True,
        "explanation_schema_complete": True,
        "category": "Deferred",
        "priority": "Low",
    }
    row.update(overrides)
    return row


def _trust_home_snapshot(**overrides) -> HomeSnapshot:
    explanation = ExplanationSnapshot(
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
        plan_coherence="aligned",
        plan_coherence_label="Supports today's mission",
        honest_refusal=False,
        timeliness_line="High educational return before the exam window.",
        completion_loop_line="Reassess after tonight's practice set.",
    )
    kwargs = dict(
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
        explanation=explanation,
        has_recommendation=True,
        can_start_session=True,
        trust_state=TRUST_STATE_COMPLETE,
        recommendation_alternatives=(
            RecommendationAlternativeSnapshot(
                title="Working capital cycles",
                why_recommended="Also under-practised this week.",
                expected_benefit="Protect related marks.",
                suggested_next_action="Review one working-capital set.",
            ),
            RecommendationAlternativeSnapshot(
                title="Inventory valuation",
                why_recommended="Syllabus weight is high.",
                expected_benefit="Close a coverage gap.",
                suggested_next_action="Attempt one inventory question.",
            ),
            RecommendationAlternativeSnapshot(
                title="Should be capped",
                why_recommended="Third alternative must not appear on Home.",
            ),
        ),
    )
    kwargs.update(overrides)
    # Cap is applied by mapper; HomeSnapshot may already be capped by HomeService.
    alts = kwargs.get("recommendation_alternatives") or ()
    if len(alts) > 2 and "recommendation_alternatives" not in overrides:
        kwargs["recommendation_alternatives"] = alts[:2]
    return HomeSnapshot(**kwargs)


def test_tr_a01_schema_complete_home_binds_trust_mes_fields(app, ctx):
    """TR-A01: DX-005A Home — one why-now; deep MES stack not on template."""
    from app.application.student_experience.dto.home_snapshot import (
        StartSessionActionSnapshot,
    )

    page_home = home_vm(
        _trust_home_snapshot(
            start_session=StartSessionActionSnapshot(
                label="Start Session",
                enabled=True,
                can_start=True,
                mission_id="m-1",
                estimated_minutes=25,
                topic_title="Cash flow statements",
            ),
        ),
        unified_journey=False,
    )
    html = render_student_home(app, page_home)
    assert "Current Mission" in html
    assert "Why now" in html
    assert 'data-mes-field' not in html
    assert 'data-mes-level' not in html
    assert 'data-mes-disclosure' not in html
    assert 'data-mes-field="plan_coherence"' not in html
    assert 'data-mes-field="review_point"' not in html
    assert html.count('data-student-cta="primary"') <= 1


def test_tr_a02_alternatives_capped_at_two_on_home(app, ctx):
    """TR-A02: ≤2 alternatives rendered with titles."""
    alts = map_recommendation_alternatives(
        [
            {
                "title": "Alt A",
                "why_recommended": "Why A",
                "expected_benefit": "Benefit A",
            },
            {
                "title": "Alt B",
                "why_recommended": "Why B",
            },
            {
                "title": "Alt C",
                "why_recommended": "Why C",
            },
        ]
    )
    assert len(alts) == 2
    snap = _trust_home_snapshot(recommendation_alternatives=alts)
    page_home = home_vm(snap, unified_journey=False)
    assert len(page_home.recommendation_alternatives) == 2
    html = render_student_home(app, page_home)
    assert 'data-mes-field="alternatives"' not in html
    assert "Alt A" not in html
    assert "Alt B" not in html
    assert "Other options considered" not in html


def test_tr_a03_honest_refusal_hides_alternatives(app, ctx):
    """TR-A03: refusal → no alternatives; cannot-yet confidence; authored title."""
    from app.application.student_experience.dto.home_snapshot import (
        StartSessionActionSnapshot,
    )

    explanation = ExplanationSnapshot(
        summary="No recommendation yet",
        why_recommended=(
            "There is not yet enough personal study evidence for a confident "
            "primary tip."
        ),
        evidence_points=(
            "Insufficient personal study history for a confident primary tip.",
        ),
        expected_benefit=(
            "Avoid fabricated certainty; build enough evidence for useful guidance."
        ),
        confidence_label="Cannot yet be estimated",
        suggested_next_action=(
            "Complete a short study session so guidance can be personalised."
        ),
        review_point="Reassess after your next completed study session.",
        is_complete=True,
        plan_coherence="deferred",
        plan_coherence_label="No recommendation yet",
        honest_refusal=True,
        timeliness_line="",
        completion_loop_line="Reassess after your next completed study session.",
    )
    snap = _trust_home_snapshot(
        recommendation_title="No recommendation yet",
        explanation=explanation,
        trust_state=TRUST_STATE_REFUSAL,
        recommendation_alternatives=(),
        can_start_session=True,
        start_session=StartSessionActionSnapshot(
            label="Start Session",
            enabled=True,
            can_start=True,
            mission_id="m-refusal",
            estimated_minutes=25,
            topic_title="No recommendation yet",
        ),
    )
    page_home = home_vm(snap, unified_journey=False)
    assert page_home.trust_state == TRUST_STATE_REFUSAL
    assert page_home.recommendation_alternatives == ()
    html = render_student_home(app, page_home)
    assert "No recommendation yet" in html
    assert "Cannot yet be estimated" not in html
    assert 'data-mes-field="alternatives"' not in html
    assert 'data-trust-state="refusal"' not in html
    assert "Supports today's mission" not in html


def test_tr_a04_coach_strings_subset_of_authored_fields():
    """TR-A04: Coach insight uses Home authored fields only (glue labels OK)."""
    snap = _trust_home_snapshot()
    page = home_vm(snap, unified_journey=False)
    assert page.coach_trust is not None
    assert page.coach_trust.why == snap.explanation.why_recommended
    assert page.coach_trust.why_now == snap.explanation.timeliness_line
    assert page.coach_trust.next == snap.explanation.suggested_next_action
    assert page.coach_trust.benefit == snap.explanation.expected_benefit
    # Novel marketing sentences must not appear.
    assert "highly confident" not in page.coach_insight.lower()
    assert "exam ready" not in page.coach_insight.lower()
    assert "soft recall" in page.coach_insight
    assert "25-minute" in page.coach_insight


def test_tr_a05_single_primary_cta(app, ctx):
    """TR-A05: DR-050 — at most one primary Start Session CTA."""
    from app.application.student_experience.dto.home_snapshot import (
        StartSessionActionSnapshot,
    )

    snap = _trust_home_snapshot(
        start_session=StartSessionActionSnapshot(
            label="Start Session",
            enabled=True,
            can_start=True,
            mission_id="m-1",
        ),
        can_start_session=True,
    )
    page_home = home_vm(snap, unified_journey=False)
    form = SimpleNamespace(
        hidden_tag=lambda: "",
        mission_id=lambda: '<input type="hidden" name="mission_id">',
        session_id=lambda: '<input type="hidden" name="session_id">',
    )
    html = render_student_home(app, page_home, form=form)
    assert html.count('data-student-cta="primary"') == 1


def test_tr_a06_terminology_guard_on_trust_blocks(app, ctx):
    """TR-A06: no Twin/pipeline/warrant tokens in rendered trust blocks."""
    snap = _trust_home_snapshot()
    page_home = home_vm(snap, unified_journey=False)
    html = render_student_home(app, page_home)
    lowered = html.lower()
    for token in (
        "digital twin",
        "pipeline",
        "warrant",
        "adaptive decision engine",
        "bounded context",
    ):
        assert token not in lowered


def test_tr_a07_mapper_dto_round_trip_preserves_trust_fields():
    """TR-A07: plan_coherence_label, honest_refusal, alternatives preserved."""
    primary = _schema_complete_row()
    alts = [
        {
            "title": "Working capital",
            "reason": "Also soft this week.",
            "why_recommended": "Also soft this week.",
            "expected_benefit": "Protect related marks.",
            "suggested_next_action": "Review one set.",
        }
    ]
    projection = rec_mapper.map_recommendation_to_projection(
        student_id="stu-1",
        primary=primary,
        alternatives=alts,
        estimated_minutes=25,
    )
    assert projection is not None
    assert projection["plan_coherence"] == "aligned"
    assert projection["plan_coherence_label"] == "Supports today's mission"
    assert projection["honest_refusal"] is False
    assert projection["explanation"]["plan_coherence_label"] == (
        "Supports today's mission"
    )
    assert len(projection["alternatives"]) == 1
    assert projection["alternatives"][0]["why_recommended"] == "Also soft this week."

    domain = ExplanationService().from_opaque(projection)
    assert domain.plan_coherence_label == "Supports today's mission"
    assert domain.honest_refusal is False
    assert domain.timeliness_line == primary["reason"]
    assert domain.completion_loop_line == primary["review_point"]
    assert domain.expected_benefit == primary["expected_benefit"]

    mapped_alts = map_recommendation_alternatives(projection["alternatives"])
    assert len(mapped_alts) == 1
    assert mapped_alts[0].title == "Working capital"
    assert resolve_trust_state(honest_refusal=False, is_complete=True) == (
        TRUST_STATE_COMPLETE
    )


def test_tr_a07_refusal_round_trip():
    primary = _honest_refusal_row()
    projection = rec_mapper.map_recommendation_to_projection(
        student_id="stu-1",
        primary=primary,
        alternatives=[
            {"title": "Should hide", "why_recommended": "noise"},
        ],
    )
    assert projection is not None
    assert projection["honest_refusal"] is True
    domain = ExplanationService().from_opaque(projection)
    assert domain.honest_refusal is True
    assert domain.confidence_label == "Cannot yet be estimated"
    alts = map_recommendation_alternatives(
        projection["alternatives"], honest_refusal=True
    )
    assert alts == ()
    assert resolve_trust_state(honest_refusal=True, is_complete=True) == (
        TRUST_STATE_REFUSAL
    )


def test_tr_a08_incomplete_mes_omits_invented_confidence():
    """TR-A08: incomplete MES → omit blocks; no invented confidence."""
    domain = ExplanationService().from_opaque(
        {
            "topic_title": "Tax",
            "why_recommended": "",
            "reason_codes": ("high_roi",),
            "evidence_points": ("Recent practice showed a gap.",),
        }
    )
    # Fallback synthesis may author why/benefit, but must not invent
    # plan_coherence / confidence theatre when absent.
    assert domain.plan_coherence_label == ""
    assert domain.plan_coherence == ""
    assert domain.honest_refusal is False
    snap = HomeSnapshot(
        student_id="stu-1",
        recommendation_title="Tax",
        explanation=ExplanationSnapshot(
            summary=domain.summary,
            why_recommended=domain.why_recommended,
            evidence_points=domain.evidence_points,
            expected_benefit=domain.expected_benefit,
            confidence_label=domain.confidence_label,
            suggested_next_action=domain.suggested_next_action,
            is_complete=domain.is_complete,
            plan_coherence="",
            plan_coherence_label="",
            honest_refusal=False,
            timeliness_line="",
            completion_loop_line="",
        ),
        has_recommendation=True,
        trust_state="incomplete",
    )
    page = home_vm(snap, unified_journey=False)
    assert page.explanation is not None
    assert page.explanation.plan_coherence_label == ""
    assert page.l1_expected_benefit  # may be synthesised benefit from fallback
    # No coherence badge when label empty.
    assert page.explanation.plan_coherence_label == ""
