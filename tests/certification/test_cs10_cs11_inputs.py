"""CS-10 and CS-11: Readiness and Estimated Knowledge inputs certification."""

from __future__ import annotations

from datetime import date

import pytest

from app.application.educational_runtime_engine import (
    EducationalRuntimeEngineService,
)
from tests.certification.pi001d_helpers import (
    make_certified_user,
    publish_certified_subject,
)


class TestReadinessInputs:
    """CS-10: Readiness inputs certification."""

    def test_cs10_1_readiness_derives_from_progress(self, ctx):
        user = make_certified_user("cs10-1@cert.test")
        subject = publish_certified_subject("CS10A")
        runtime = EducationalRuntimeEngineService()
        runtime.enrol_student(user_id=user.id, subject_code=subject)

        mission = runtime.generate_daily_mission(
            user_id=user.id, subject_code=subject, mission_date=date(2026, 8, 1)
        )
        runtime.complete_mission(
            user_id=user.id, mission_instance_id=mission.mission_instance_id
        )

        readiness = runtime.get_readiness_inputs(
            user_id=user.id, subject_code=subject
        )
        assert len(readiness.topic_ids) == 3
        assert len(readiness.completed_topic_ids) == 1
        assert readiness.coverage_ratio == pytest.approx(1.0 / 3.0)
        assert readiness.current_topic_id is not None
        assert readiness.syllabus_complete is False


class TestEstimatedKnowledgeInputs:
    """CS-11: Estimated Knowledge inputs certification."""

    def test_cs11_1_ek_derives_from_progress(self, ctx):
        user = make_certified_user("cs11-1@cert.test")
        subject = publish_certified_subject("CS11A")
        runtime = EducationalRuntimeEngineService()
        runtime.enrol_student(user_id=user.id, subject_code=subject)

        mission = runtime.generate_daily_mission(
            user_id=user.id, subject_code=subject, mission_date=date(2026, 8, 1)
        )
        runtime.complete_mission(
            user_id=user.id, mission_instance_id=mission.mission_instance_id
        )

        ek = runtime.get_estimated_knowledge_inputs(
            user_id=user.id, subject_code=subject
        )
        assert len(ek.topic_ids) == 3
        assert len(ek.completed_topic_ids) == 1

        completed_set = set(ek.completed_topic_ids)
        for topic in ek.topics:
            if topic["topic_id"] in completed_set:
                assert topic["completed"] is True
            else:
                assert topic["completed"] is False

    def test_cs11_2_no_phantom_knowledge(self, ctx):
        user = make_certified_user("cs11-2@cert.test")
        subject = publish_certified_subject("CS11B")
        runtime = EducationalRuntimeEngineService()
        runtime.enrol_student(user_id=user.id, subject_code=subject)

        ek = runtime.get_estimated_knowledge_inputs(
            user_id=user.id, subject_code=subject
        )
        for topic in ek.topics:
            assert topic["has_estimated_knowledge"] is False
            assert topic["mastery_score"] is None
