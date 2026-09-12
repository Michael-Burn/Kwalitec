"""Journey / Home coverage honesty: verified vs prior-knowledge claims."""

from __future__ import annotations

from app.application.educational_experience.dto import (
    CurriculumPositionSnapshot,
    EducationalExperienceSnapshot,
    JourneyEducationSnapshot,
    PacingEducationSnapshot,
)
from app.presentation.student.educational_view_models import (
    educational_vm,
    page_from_educational_experience,
)


def _snap(
    *,
    verified_percent: int = 20,
    completed_topics: tuple[tuple[str, str], ...] = (
        ("t-verified", "Verified Topic"),
        ("t-claimed", "Claimed Topic"),
    ),
    claimed_ids: tuple[str, ...] = ("t-claimed",),
) -> EducationalExperienceSnapshot:
    return EducationalExperienceSnapshot(
        student_id="1",
        enrolment_id="enr-1",
        subject_code="CS1",
        curriculum_identity="CS1:test",
        runtime_authority="runtime_c",
        is_runtime_c=True,
        greeting="Hello",
        examination_label="CS1",
        curriculum_position=CurriculumPositionSnapshot(
            subject_code="CS1",
            subject_title="CS1",
            version_label="2026",
            section_title="Section 1",
            topic_id="t-next",
            topic_code="T3",
            topic_title="Next Topic",
            position_index=3,
            topic_count=5,
            position_label=f"Topic 3 of 5 · {verified_percent // 20} complete",
            coverage_ratio=verified_percent / 100.0,
            coverage_percent=verified_percent,
            journey_stage="in_progress",
        ),
        mission=None,
        journey=JourneyEducationSnapshot(
            why_today="Next in syllabus order.",
            why_previous_complete="",
            unlocks_next="",
            supporting_evidence=(),
            current_topic_title="Next Topic",
            completed_topics=completed_topics,
            upcoming_topics=(("t-next", "Next Topic"),),
            prior_knowledge_claimed_topic_ids=claimed_ids,
        ),
        pacing=PacingEducationSnapshot(
            exam_date=None,
            exam_date_label="No exam date set",
            exam_date_aware=False,
            first_pass_minutes=0,
            revision_minutes=0,
            total_required_minutes=0,
            feasible=None,
            shortfall_minutes=None,
            pacing_summary="",
            feasibility_label="",
        ),
    )


def test_journey_labels_verified_and_claimed_topics_differently(app):
    snap = _snap()
    edu = educational_vm(snap)
    assert edu is not None
    assert edu.progress_percent == 20
    assert edu.progress_label == "20% of syllabus completed"
    page = page_from_educational_experience(snap, surface="journey")
    journey = page.journey
    assert journey is not None
    assert journey.completed_count == 1
    assert journey.prior_knowledge_claimed_count == 1
    assert journey.prior_knowledge_claim_label == "1 already knew coming in"
    by_id = {t.topic_id: t for t in journey.completed}
    assert by_id["t-verified"].status_label == "Completed"
    assert by_id["t-claimed"].status_label == "Already knew coming in"
    with app.test_request_context("/student/journey"):
        from flask import render_template

        html = render_template(
            "student/journey.html",
            page=page,
            title="Syllabus",
        )
    assert "Topics completed" in html
    assert "Already knew coming in" in html
    assert 'data-journey-prior-knowledge="true"' in html
    assert "20% of syllabus completed" in html


def test_journey_omits_claim_row_when_no_prior_knowledge(app):
    snap = _snap(
        verified_percent=40,
        completed_topics=(("t-verified", "Verified Topic"),),
        claimed_ids=(),
    )
    page = page_from_educational_experience(snap, surface="journey")
    journey = page.journey
    assert journey is not None
    assert journey.completed_count == 1
    assert journey.prior_knowledge_claimed_count == 0
    assert journey.prior_knowledge_claim_label == ""
    assert journey.completed[0].status_label == "Completed"
    with app.test_request_context("/student/journey"):
        from flask import render_template

        html = render_template(
            "student/journey.html",
            page=page,
            title="Syllabus",
        )
    assert "Already knew coming in" not in html
    assert 'data-journey-prior-knowledge="true"' not in html
