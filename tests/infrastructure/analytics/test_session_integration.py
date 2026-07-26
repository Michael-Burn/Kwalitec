"""Integration + negative tests — Study Session analytics instrumentation.

Educational lifecycle must succeed even when analytics fails or is disabled.
"""

from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import patch

import pytest

from app.extensions import db
from app.infrastructure.analytics.dispatcher import AnalyticsEventDispatcher
from app.infrastructure.analytics.feature_flag import AnalyticsFeatureFlag
from app.infrastructure.analytics.outbox import MemoryOutboxSink
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.session_events import (
    COMPLETION_ABANDONED_AFTER_START,
    COMPLETION_COMPLETED,
    SESSION_COMPLETED,
    SESSION_STARTED,
)
from app.infrastructure.analytics.validator import (
    AnalyticsEventValidator,
    ValidationResult,
)
from app.models.curriculum import Curriculum, Topic
from app.models.mission import Mission, MissionTask
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.services.study_session_service import (
    COMPLETION_NO,
    COMPLETION_PARTIAL,
    COMPLETION_YES,
    StudySessionService,
)


def _make_curriculum(
    exam_name: str, topic_names: list[str]
) -> tuple[Curriculum, list[Topic]]:
    curriculum = Curriculum(exam_name=exam_name, version="2025", active=True)
    db.session.add(curriculum)
    db.session.flush()
    topics: list[Topic] = []
    for index, name in enumerate(topic_names, start=1):
        topic = Topic(
            name=name,
            curriculum_id=curriculum.id,
            order=index,
            recommended_minutes=60,
            active=True,
        )
        db.session.add(topic)
        topics.append(topic)
    db.session.flush()
    return curriculum, topics


def _make_active_plan(
    user_id: int,
    *,
    exam_name: str,
    curriculum: Curriculum,
) -> StudyPlan:
    plan = StudyPlan(
        user_id=user_id,
        curriculum_id=curriculum.id,
        curriculum_version=curriculum.version,
        exam_name=exam_name,
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=90,
        weekend_study_minutes=120,
        current_stage="Chapter 1",
        study_preference="Mixed",
        target_grade="A",
        preferred_session_minutes=60,
        active=True,
        curriculum_topic_code=None,
    )
    db.session.add(plan)
    db.session.flush()
    week = WeekPlan(
        study_plan_id=plan.id,
        week_number=1,
        start_date=date.today() - timedelta(days=2),
        end_date=date.today() + timedelta(days=4),
    )
    db.session.add(week)
    db.session.commit()
    return plan


def _make_mission_for_topic(
    user_id: int,
    *,
    topic: Topic,
    study_plan_id: int | None = None,
    status: str = "Pending",
) -> Mission:
    subject = Subject(user_id=user_id, name="Exam Paper")
    db.session.add(subject)
    db.session.flush()
    mission = Mission(
        user_id=user_id,
        subject_id=subject.id,
        study_plan_id=study_plan_id,
        mission_date=date.today(),
        title=f"Study {topic.name}",
        status=status,
    )
    mission.tasks.append(MissionTask(title="Focus study", order=0, completed=False))
    mission.tasks.append(MissionTask(title="Practice", order=1, completed=False))
    db.session.add(mission)
    db.session.commit()
    return mission


def _enabled_dispatcher(
    outbox: MemoryOutboxSink | None = None,
) -> AnalyticsEventDispatcher:
    sink = outbox if outbox is not None else MemoryOutboxSink()
    return AnalyticsEventDispatcher(
        feature_flag=AnalyticsFeatureFlag(events_v1=True),
        outbox=sink,
        registry=AnalyticsEventRegistry.phase_b_default(),
    )


@pytest.mark.usefixtures("ctx")
class TestSessionInstrumentationIntegration:
    def test_start_emits_session_started_when_flag_on(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["EoV"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=curriculum
        )
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.session_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            updated = StudySessionService.start_session(mission.id, user.id)

        assert updated.status == "In Progress"
        assert len(outbox.pending()) == 1
        assert outbox.pending()[0].event_type == SESSION_STARTED

    def test_start_idempotent_no_second_emit(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["EoV"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=curriculum
        )
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.session_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            StudySessionService.start_session(mission.id, user.id)
            StudySessionService.start_session(mission.id, user.id)

        assert len(outbox.pending()) == 1

    def test_finish_yes_emits_completed(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["EoV"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=curriculum
        )
        mission = _make_mission_for_topic(
            user.id,
            topic=topics[0],
            study_plan_id=plan.id,
            status="In Progress",
        )
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.session_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            result = StudySessionService.finish_session(
                mission.id,
                user.id,
                COMPLETION_YES,
                topic_id=topics[0].id,
            )

        assert result.mission_completed is True
        assert len(outbox.pending()) == 1
        record = outbox.pending()[0]
        assert record.event_type == SESSION_COMPLETED
        assert COMPLETION_COMPLETED in record.payload_json
        assert f'"topic_id":{topics[0].id}' in record.payload_json.replace(" ", "")

    def test_finish_no_emits_abandoned_after_start(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["EoV"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=curriculum
        )
        mission = _make_mission_for_topic(
            user.id,
            topic=topics[0],
            study_plan_id=plan.id,
            status="In Progress",
        )
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.session_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            result = StudySessionService.finish_session(
                mission.id,
                user.id,
                COMPLETION_NO,
            )

        assert result.mission_completed is False
        db.session.refresh(mission)
        assert mission.status != "Completed"
        assert len(outbox.pending()) == 1
        assert COMPLETION_ABANDONED_AFTER_START in outbox.pending()[0].payload_json

    def test_finish_partial_emits_completed(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["EoV"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=curriculum
        )
        mission = _make_mission_for_topic(
            user.id,
            topic=topics[0],
            study_plan_id=plan.id,
            status="In Progress",
        )
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.session_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            result = StudySessionService.finish_session(
                mission.id,
                user.id,
                COMPLETION_PARTIAL,
            )

        assert result.mission_completed is True
        assert COMPLETION_COMPLETED in outbox.pending()[0].payload_json

    def test_practice_outcome_emits_completed(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["EoV"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=curriculum
        )
        mission = _make_mission_for_topic(
            user.id,
            topic=topics[0],
            study_plan_id=plan.id,
            status="In Progress",
        )
        outbox = MemoryOutboxSink()
        dispatcher = _enabled_dispatcher(outbox)

        with patch(
            "app.infrastructure.analytics.session_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            result = StudySessionService.record_practice_outcome(
                mission.id,
                user.id,
                questions_attempted=10,
                questions_correct=7,
                duration_minutes=45,
                topic_id=topics[0].id,
            )

        assert result.mission_completed is True
        assert len(outbox.pending()) == 1
        payload = outbox.pending()[0].payload_json
        assert '"completion_status":"completed"' in payload.replace(" ", "")
        assert '"duration_seconds":2700' in payload.replace(" ", "")

    def test_flag_off_session_succeeds_without_outbox_writes(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["EoV"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=curriculum
        )
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )
        outbox = MemoryOutboxSink()
        dispatcher = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=False),
            outbox=outbox,
        )

        with patch(
            "app.infrastructure.analytics.session_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            started = StudySessionService.start_session(mission.id, user.id)
            assert started.status == "In Progress"
            finished = StudySessionService.finish_session(
                mission.id,
                user.id,
                COMPLETION_YES,
                topic_id=topics[0].id,
            )

        assert finished.mission_completed is True
        assert outbox.pending() == ()


@pytest.mark.usefixtures("ctx")
class TestSessionInstrumentationNegative:
    def test_dispatcher_unavailable_session_still_succeeds(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["EoV"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=curriculum
        )
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        class BoomDispatcher:
            def dispatch(self, event):
                raise RuntimeError("dispatcher unavailable")

        with patch(
            "app.infrastructure.analytics.session_events.AnalyticsEventDispatcher",
            return_value=BoomDispatcher(),
        ):
            updated = StudySessionService.start_session(mission.id, user.id)

        assert updated.status == "In Progress"

    def test_registry_reject_does_not_break_finish(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["EoV"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=curriculum
        )
        mission = _make_mission_for_topic(
            user.id,
            topic=topics[0],
            study_plan_id=plan.id,
            status="In Progress",
        )
        dispatcher = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=True),
            outbox=MemoryOutboxSink(),
            registry=AnalyticsEventRegistry.phase_a_default(),
        )

        with patch(
            "app.infrastructure.analytics.session_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            result = StudySessionService.finish_session(
                mission.id,
                user.id,
                COMPLETION_YES,
            )

        assert result.mission_completed is True
        assert dispatcher.outbox.pending() == ()

    def test_validation_failure_does_not_break_finish(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["EoV"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=curriculum
        )
        mission = _make_mission_for_topic(
            user.id,
            topic=topics[0],
            study_plan_id=plan.id,
            status="In Progress",
        )

        class RejectingValidator(AnalyticsEventValidator):
            def validate(self, event):
                return ValidationResult.failure("forced validation failure")

        registry = AnalyticsEventRegistry.phase_b_default()
        dispatcher = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=True),
            outbox=MemoryOutboxSink(),
            registry=registry,
            validator=RejectingValidator(registry),
        )

        with patch(
            "app.infrastructure.analytics.session_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            result = StudySessionService.finish_session(
                mission.id,
                user.id,
                COMPLETION_NO,
            )

        assert result.mission_completed is False
        db.session.refresh(mission)
        assert mission.status != "Completed"

    def test_outbox_unavailable_session_still_succeeds(self, db, user):
        curriculum, topics = _make_curriculum("IFoA CM1", ["EoV"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=curriculum
        )
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        class BoomOutbox(MemoryOutboxSink):
            def enqueue(self, event, *, payload_json: str = ""):
                raise RuntimeError("outbox unavailable")

        dispatcher = AnalyticsEventDispatcher(
            feature_flag=AnalyticsFeatureFlag(events_v1=True),
            outbox=BoomOutbox(),
            registry=AnalyticsEventRegistry.phase_b_default(),
        )

        with patch(
            "app.infrastructure.analytics.session_events.AnalyticsEventDispatcher",
            return_value=dispatcher,
        ):
            updated = StudySessionService.start_session(mission.id, user.id)
            assert updated.status == "In Progress"
            finished = StudySessionService.finish_session(
                mission.id,
                user.id,
                COMPLETION_YES,
            )

        assert finished.mission_completed is True

    def test_analytics_disabled_default_path(self, db, user):
        """Production default: flag off → educational behaviour unchanged."""
        curriculum, topics = _make_curriculum("IFoA CM1", ["EoV"])
        plan = _make_active_plan(
            user.id, exam_name="IFoA CM1", curriculum=curriculum
        )
        mission = _make_mission_for_topic(
            user.id, topic=topics[0], study_plan_id=plan.id
        )

        updated = StudySessionService.start_session(mission.id, user.id)
        assert updated.status == "In Progress"
        finished = StudySessionService.finish_session(
            mission.id,
            user.id,
            COMPLETION_YES,
            topic_id=topics[0].id,
        )
        assert finished.mission_completed is True
