"""A5-2: Consolidation narration must not claim weakness from absent EK."""

from __future__ import annotations

from app.services.educational_explainability_service import (
    EducationalExplainabilityService,
)


def test_consolidation_narration_absent_ek_is_not_yet_assessed():
    narrative = EducationalExplainabilityService.build_mission_narrative(
        mission_title="Consolidate Cash Flow Models",
        mission_status="Pending",
        exam_name="IFoA CS1",
        completed_topics=3,
        total_topics=10,
        syllabus_coverage_pct=30.0,
        estimated_knowledge=None,
    )
    assert narrative is not None
    joined = " ".join(narrative.estimates)
    assert "not yet assessed" in joined.lower()
    assert "still weak" not in joined.lower()
    purpose = narrative.educational_purpose.lower()
    reason = narrative.reason_for_selection.lower()
    position = narrative.educational_position.lower()
    assert "weak covered" not in purpose
    assert "weakest covered" not in reason
    assert "weak covered" not in position


def test_consolidation_narration_low_ek_is_developing_not_absent():
    narrative = EducationalExplainabilityService.build_mission_narrative(
        mission_title="Consolidate Cash Flow Models",
        mission_status="Pending",
        exam_name="IFoA CS1",
        completed_topics=3,
        total_topics=10,
        syllabus_coverage_pct=30.0,
        estimated_knowledge=22.0,
    )
    assert narrative is not None
    joined = " ".join(narrative.estimates)
    assert "still developing" in joined.lower()
    assert "not yet assessed" not in joined.lower()
    assert "still weak" not in joined.lower()
