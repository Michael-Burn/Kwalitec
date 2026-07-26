"""EP-006.2 — dual-home MES parity smoke (Dashboard vs Home).

Until REM-02 consolidates homes, the same day's authored Why / Evidence /
next action must not conflict between Dashboard recommendation rows and the
canonical Home explanation path (P7).
"""

from __future__ import annotations

from app.application.student_experience.explanation_service import (
    ExplanationService,
)
from app.infrastructure.adapters.educational_runtime_bridge import (
    recommendation_mapper as rec_mapper,
)
from app.presentation.intelligence_surface.adapter import (
    RuntimeAPresentationAdapter,
)


def _schema_complete_row():
    return {
        "title": "Cash flow statements",
        "reason": "High educational return before the exam window.",
        "why_recommended": (
            "Your recent practice shows soft recall on cash flow statements."
        ),
        "expected_benefit": "Strengthen exam readiness on cash flow analysis.",
        "next_action": "Start a 25-minute cash flow practice session.",
        "suggested_next_action": "Start a 25-minute cash flow practice session.",
        "confidence_level": "Suggested",
        "supporting_evidence": [
            "Two recent practice attempts scored below your topic average.",
            "Cash flow is on the near-term revision list.",
        ],
        "review_point": "Reassess after tonight's practice set.",
        "decision_ladder_rank": 1,
        "plan_coherence": "aligned",
        "explanation_schema_version": "1.0",
        "explanation_level": 2,
        "explanation_schema_complete": True,
        "category": "Revision",
        "priority": "High",
    }


def test_dashboard_and_home_paths_share_authored_why():
    primary = _schema_complete_row()

    # Legacy Dashboard path — schema-complete rows pass through unchanged.
    today, rows = RuntimeAPresentationAdapter.enrich_recommendations_if_needed(
        [primary],
        today_recommendation=primary,
    )
    assert today is primary
    assert rows[0]["why_recommended"] == primary["why_recommended"]
    assert rows[0]["supporting_evidence"] == primary["supporting_evidence"]
    assert rows[0]["suggested_next_action"] == primary["suggested_next_action"]

    # Canonical Home path — bridge + ExplanationService pass-through.
    projection = rec_mapper.map_recommendation_to_projection(
        student_id="stu-1",
        primary=primary,
        estimated_minutes=25,
    )
    assert projection is not None
    home_expl = ExplanationService().from_opaque(projection)
    assert home_expl.why_recommended == primary["why_recommended"]
    assert list(home_expl.evidence_points) == primary["supporting_evidence"]
    assert home_expl.suggested_next_action == primary["suggested_next_action"]
    assert home_expl.review_point == primary["review_point"]


def test_schema_readiness_narrative_exposes_drivers_and_review_point():
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
    narrative = RuntimeAPresentationAdapter.readiness_narrative(surface)
    assert narrative.can_estimate is True
    assert "Coverage and practice" in narrative.explanation
    assert len(narrative.readiness_drivers) >= 3
    assert any("Curriculum coverage" in d for d in narrative.readiness_drivers)
    assert narrative.review_point.startswith("Reassess")
    assert narrative.suggested_next_action.startswith("Practise")
    assert len(narrative.supporting_evidence) >= 2


def test_schema_mission_narrative_exposes_plan_drivers_and_review_point():
    mission = type(
        "Mission", (), {"title": "Cash flow practice", "status": "pending"}
    )()
    surface = {
        "explanation_schema_complete": True,
        "judgement": "Today's plan: Cash flow practice",
        "why_this_plan": "Recovery focus after a missed session protects retention.",
        "supporting_evidence": [
            "One missed mission in the last three days.",
            "Cash flow remains incomplete on the syllabus.",
        ],
        "confidence_level": "Suggested",
        "expected_benefit": "Restore continuity on cash flow.",
        "suggested_next_action": "Start today's cash flow session.",
        "review_point": "Reassess after tonight's session.",
        "plan_drivers": [
            {
                "driver_id": "adaptive_recovery",
                "label": "Adaptive recovery",
                "value": 1,
            },
            {
                "driver_id": "slot_review",
                "label": "Cash flow statements",
                "value": None,
            },
        ],
        "explanation_schema_version": "1.0",
        "explanation_level": 2,
    }
    narrative = RuntimeAPresentationAdapter.mission_narrative(
        today_mission=mission,
        mission_surface=surface,
    )
    assert narrative is not None
    assert "Recovery focus" in narrative.reason_for_selection
    assert narrative.next_action.startswith("Start today's")
    assert len(narrative.plan_drivers) >= 1
    assert narrative.review_point.startswith("Reassess")
    assert narrative.expected_benefit.startswith("Restore")
