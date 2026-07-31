"""Runtime C: session-budget LO chunking across multi-objective topics."""

from __future__ import annotations

from datetime import date

from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.domain.educational_runtime_engine.events import EducationalEventType
from tests.certification.pi001d_helpers import (
    make_certified_user,
    publish_certified_subject,
)

MULTI_LO_STRUCTURE = {
    "entries": [
        {
            "entry_id": "s1",
            "entry_type": "section",
            "text": "Modelling",
            "number": "4",
        },
        {
            "entry_id": "t1",
            "entry_type": "topic",
            "text": "Understand and use generalised linear models",
            "number": "4.2",
            "parent_ref": "s1",
        },
        *[
            {
                "entry_id": f"o{i}",
                "entry_type": "objective",
                "text": f"4.2.{i} Objective {i} detail",
                "number": f"4.2.{i}",
                "parent_ref": "t1",
            }
            for i in range(1, 11)
        ],
    ]
}


def test_daily_mission_chunks_objectives_to_session_budget(ctx):
    user = make_certified_user("chunk-1@cert.test")
    subject = publish_certified_subject("CHUNK1", structure=MULTI_LO_STRUCTURE)
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=user.id, subject_code=subject)

    mission = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code=subject,
        mission_date=date(2026, 8, 1),
    )
    assert mission.quality is not None
    assert 1 <= len(mission.quality.objective_ids) <= 3
    assert len(mission.quality.objective_ids) < 10
    assert int(mission.quality.estimated_duration_minutes or 0) <= 60


def test_topic_advances_only_after_all_lo_chunks(ctx):
    user = make_certified_user("chunk-2@cert.test")
    subject = publish_certified_subject("CHUNK2", structure=MULTI_LO_STRUCTURE)
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=user.id, subject_code=subject)

    day = date(2026, 8, 1)
    first = runtime.generate_daily_mission(
        user_id=user.id, subject_code=subject, mission_date=day
    )
    topic_id = first.topic_id
    journey = runtime.complete_mission(
        user_id=user.id, mission_instance_id=first.mission_instance_id
    )
    assert topic_id not in journey.progress.completed_topic_ids
    assert journey.progress.current_topic_id == topic_id

    events = runtime.list_events(user_id=user.id, subject_code=subject)
    assert not any(
        e.event_type == EducationalEventType.TOPIC_COMPLETED.value
        for e in events
    )

    covered = set(first.quality.objective_ids)
    safety = 0
    while topic_id not in journey.progress.completed_topic_ids and safety < 20:
        safety += 1
        day = date(2026, 8, 1 + safety)
        mission = runtime.generate_daily_mission(
            user_id=user.id, subject_code=subject, mission_date=day
        )
        assert mission.topic_id == topic_id
        assert not set(mission.quality.objective_ids) & covered
        covered.update(mission.quality.objective_ids)
        journey = runtime.complete_mission(
            user_id=user.id, mission_instance_id=mission.mission_instance_id
        )

    assert topic_id in journey.progress.completed_topic_ids
    assert len(covered) == 10
