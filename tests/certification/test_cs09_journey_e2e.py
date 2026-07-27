"""CS-09: End-to-end journey progression certification."""

from __future__ import annotations

import pytest

from app.application.educational_engine_foundation.service import (
    EducationalEngineFoundationService,
)
from app.application.educational_runtime_engine.exceptions import (
    SyllabusAlreadyComplete,
)
from app.domain.educational_runtime_engine.events import EducationalEventType
from tests.certification.pi001d_helpers import (
    make_certified_user,
    publish_certified_subject,
    run_full_journey,
)


class TestJourneyProgression:
    """Certify complete syllabus traversal from enrolment to completion."""

    def test_cs09_1_full_syllabus_traversal(self, ctx):
        user = make_certified_user("cs09-1@cert.test")
        subject = publish_certified_subject("CS09A")
        result = run_full_journey(user, subject)

        assert result["journey"].progress.syllabus_complete is True
        assert result["days_elapsed"] == 3
        assert len(set(result["topic_sequence"])) == 3

        snapshot = EducationalEngineFoundationService().derive_active(subject)
        expected_order = [
            str(topic["topic_id"])
            for topic in snapshot.study_plan_template.topic_templates
        ]
        assert result["topic_sequence"] == expected_order

    def test_cs09_2_final_state_correct(self, ctx):
        user = make_certified_user("cs09-2@cert.test")
        subject = publish_certified_subject("CS09B")
        result = run_full_journey(user, subject)

        journey = result["journey"]
        assert journey.enrolment.status == "completed"
        assert journey.study_plan.status == "completed"
        assert journey.progress.coverage_ratio == 1.0
        assert journey.progress.current_topic_id is None

    def test_cs09_3_post_completion_mission_rejected(self, ctx):
        from datetime import date

        from app.application.educational_runtime_engine import (
            EducationalRuntimeEngineService,
        )

        user = make_certified_user("cs09-3@cert.test")
        subject = publish_certified_subject("CS09C")
        run_full_journey(user, subject)

        runtime = EducationalRuntimeEngineService()
        with pytest.raises(SyllabusAlreadyComplete):
            runtime.generate_daily_mission(
                user_id=user.id,
                subject_code=subject,
                mission_date=date(2026, 12, 1),
            )

    def test_cs09_4_event_audit_trail_complete(self, ctx):
        user = make_certified_user("cs09-4@cert.test")
        subject = publish_certified_subject("CS09D")
        result = run_full_journey(user, subject)

        event_types = [e.event_type for e in result["events"]]
        assert EducationalEventType.STUDENT_ENROLLED.value in event_types
        assert EducationalEventType.STUDY_PLAN_INSTANTIATED.value in event_types
        assert event_types.count(EducationalEventType.MISSION_GENERATED.value) == 3
        assert event_types.count(EducationalEventType.MISSION_COMPLETED.value) == 3
        assert event_types.count(EducationalEventType.TOPIC_COMPLETED.value) == 3
        assert event_types.count(EducationalEventType.JOURNEY_ADVANCED.value) == 3
        assert EducationalEventType.SYLLABUS_COMPLETED.value in event_types

        # Events are chronologically ordered
        timestamps = [e.occurred_at for e in result["events"]]
        assert timestamps == sorted(timestamps)
