"""Baseline seed writes PRIOR_KNOWLEDGE_CLAIM; continue-from still positions."""

from __future__ import annotations

from datetime import date

import pytest

from app.application.educational_runtime_engine import EducationalRuntimeEngineService
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.models.educational_runtime_engine import RuntimeEducationalEvent
from tests.application.educational_runtime_engine.helpers import (
    make_user,
    publish_subject,
)


def test_seed_declared_position_emits_prior_knowledge_claim_not_topic_completed(
    ctx,
):
    user = make_user("prior-claim@example.com")
    subject = publish_subject("PKC1")
    runtime = EducationalRuntimeEngineService()
    journey = runtime.enrol_student(user_id=user.id, subject_code=subject)
    first_topic = journey.progress.current_topic_id
    assert first_topic is not None

    # Continue from second leaf (2.1): prior leaf becomes a claim.
    seeded = runtime.seed_declared_position(
        user_id=user.id,
        subject_code=subject,
        curriculum_topic_code="2.1",
        realign_today_mission=True,
    )
    assert seeded is not None
    assert seeded.current_topic_id is not None
    assert seeded.current_topic_id != first_topic
    assert first_topic in seeded.progressed_topic_ids
    assert first_topic in seeded.prior_knowledge_claimed_topic_ids
    assert first_topic not in seeded.verified_completed_topic_ids
    assert seeded.verified_coverage_ratio == 0.0
    # Progressed ratio still positions continue-from honestly for presentation.
    assert seeded.coverage_ratio > 0.0
    assert first_topic in seeded.completed_topic_ids

    claim_rows = RuntimeEducationalEvent.query.filter_by(
        user_id=user.id,
        event_type=EducationalEventType.PRIOR_KNOWLEDGE_CLAIM.value,
        topic_id=first_topic,
    ).all()
    assert len(claim_rows) >= 1
    payload = claim_rows[0].payload_json or ""
    assert "baseline_self_declared" in payload

    verified_rows = RuntimeEducationalEvent.query.filter_by(
        user_id=user.id,
        event_type=EducationalEventType.TOPIC_COMPLETED.value,
        topic_id=first_topic,
    ).all()
    assert verified_rows == []


def test_mission_completion_still_advances_verified_coverage(ctx):
    user = make_user("verified-cov@example.com")
    subject = publish_subject("VCOV1")
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    mission = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code=subject,
        mission_date=date(2026, 9, 12),
    )
    journey = runtime.complete_mission(
        user_id=user.id,
        mission_instance_id=mission.mission_instance_id,
    )
    assert mission.topic_id in journey.progress.verified_completed_topic_ids
    assert mission.topic_id in journey.progress.progressed_topic_ids
    assert mission.topic_id not in (
        journey.progress.prior_knowledge_claimed_topic_ids
    )
    assert journey.progress.verified_coverage_ratio == pytest.approx(0.5)
    assert journey.progress.current_topic_id != mission.topic_id
