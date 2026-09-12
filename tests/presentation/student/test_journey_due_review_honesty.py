"""A5-1: Journey due-review presentation must not frame calendar-due as weakness."""

from __future__ import annotations

from app.application.student_experience.dto.journey_snapshot import (
    JourneySnapshot,
    JourneyTopicSnapshot,
)
from app.application.student_experience.dto.revision_snapshot import (
    RevisionOptionSnapshot,
    RevisionSnapshot,
)
from app.presentation.student.view_models import (
    StudentPageViewModel,
    StudentShellViewModel,
    journey_vm,
)


def test_journey_due_review_not_framed_as_weakness(app):
    revision = RevisionSnapshot(
        student_id="1",
        has_revision=True,
        option_count=1,
        primary=RevisionOptionSnapshot(
            option_id="pkg-due-1",
            topic_title="Cash Flow Models",
            priority_label="",
            is_primary=True,
            package_id="pkg-due-1",
        ),
    )
    snap = JourneySnapshot(
        student_id="1",
        examination_label="CS1",
        progress_percent=40,
        current_topic=JourneyTopicSnapshot(
            topic_id="t-current",
            title="Current Topic",
            status_label="Current",
        ),
        upcoming_topics=(
            JourneyTopicSnapshot(
                topic_id="t-next",
                title="Next Topic",
                status_label="Upcoming",
            ),
        ),
        completed_count=2,
        upcoming_count=1,
    )
    journey = journey_vm(snap, revision=revision)
    assert journey.needs_attention
    assert journey.needs_attention[0].title == "Cash Flow Models"
    assert journey.needs_attention[0].status_label == "Due for review"
    assert "Strengthen" not in journey.needs_attention[0].status_label
    assert any("due for review" in line.lower() for line in journey.learning_insights)

    page = StudentPageViewModel(
        shell=StudentShellViewModel(
            active_surface="journey",
            active_label="Syllabus",
            navigation=(),
            page_title="Syllabus",
        ),
        journey=journey,
    )
    with app.test_request_context("/student/journey"):
        from flask import render_template

        html = render_template(
            "student/journey.html",
            page=page,
            title="Syllabus",
        )
    assert "Due for review" in html
    assert "Needs Attention" not in html
    assert "Topics to strengthen" not in html
    assert "need strengthening" not in html
    assert "Strengthen" not in html
    assert "Cash Flow Models" in html
    assert "Open Revision" in html
    assert "when you are ready" in html
