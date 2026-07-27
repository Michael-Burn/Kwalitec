"""Shared helpers for PI-001D platform certification tests."""

from __future__ import annotations

from datetime import date, timedelta

from app.application.curriculum_studio_foundation.service import (
    CurriculumStudioFoundationService,
)
from app.application.educational_runtime_engine import (
    EducationalRuntimeEngineService,
)
from app.extensions import db
from app.models.user import User


def make_certified_user(email: str = "cert@example.com") -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    user.alpha_onboarding_completed = True
    db.session.add(user)
    db.session.commit()
    return user


STANDARD_STRUCTURE = {
    "entries": [
        {
            "entry_id": "s1",
            "entry_type": "section",
            "text": "Fundamentals",
            "number": "1",
        },
        {
            "entry_id": "t1",
            "entry_type": "topic",
            "text": "Core concepts",
            "number": "1.1",
            "parent_ref": "s1",
        },
        {
            "entry_id": "o1",
            "entry_type": "objective",
            "text": "Explain core concepts",
            "number": "1.1.1",
            "parent_ref": "t1",
        },
        {
            "entry_id": "s2",
            "entry_type": "section",
            "text": "Applications",
            "number": "2",
        },
        {
            "entry_id": "t2",
            "entry_type": "topic",
            "text": "Applied methods",
            "number": "2.1",
            "parent_ref": "s2",
            "attributes": {"prerequisites": "t1"},
        },
        {
            "entry_id": "o2",
            "entry_type": "objective",
            "text": "Apply methods in context",
            "number": "2.1.1",
            "parent_ref": "t2",
        },
        {
            "entry_id": "s3",
            "entry_type": "section",
            "text": "Advanced",
            "number": "3",
        },
        {
            "entry_id": "t3",
            "entry_type": "topic",
            "text": "Advanced analysis",
            "number": "3.1",
            "parent_ref": "s3",
            "attributes": {"prerequisites": "t2"},
        },
        {
            "entry_id": "o3",
            "entry_type": "objective",
            "text": "Perform advanced analysis",
            "number": "3.1.1",
            "parent_ref": "t3",
        },
    ],
}


def publish_certified_subject(
    subject_code: str = "CERT1",
    *,
    version_label: str = "2027.1",
    title: str = "Certification Subject",
    structure: dict | None = None,
) -> str:
    """Publish a subject through the full founder lifecycle."""
    foundation = CurriculumStudioFoundationService()
    foundation.create_subject(subject_code, title=title, actor_id="founder")
    version = foundation.create_version(
        subject_code, version_label, actor_id="founder"
    )
    struct = structure or STANDARD_STRUCTURE
    foundation.upload_document(
        version.version_id,
        kind="cmp",
        reference=f"ref://cmp/{subject_code.lower()}",
        structure=struct,
        actor_id="founder",
    )
    foundation.upload_document(
        version.version_id,
        kind="syllabus",
        reference=f"ref://syllabus/{subject_code.lower()}",
        structure=struct,
        actor_id="founder",
    )
    foundation.process_curriculum(version.version_id, actor_id="founder")
    foundation.validate_curriculum(version.version_id, actor_id="founder")
    foundation.founder_review(version.version_id, actor_id="founder")
    foundation.publish_curriculum(version.version_id, actor_id="founder")
    return subject_code.upper()


def run_full_journey(
    user: User,
    subject_code: str,
    *,
    start_date: date | None = None,
) -> dict:
    """Execute a complete learning journey and return summary."""
    runtime = EducationalRuntimeEngineService()
    journey = runtime.enrol_student(user_id=user.id, subject_code=subject_code)

    day = start_date or date(2026, 8, 1)
    missions_completed = []
    topic_sequence = []

    while not journey.progress.syllabus_complete:
        mission = runtime.generate_daily_mission(
            user_id=user.id,
            subject_code=subject_code,
            mission_date=day,
        )
        topic_sequence.append(mission.topic_id)
        journey = runtime.complete_mission(
            user_id=user.id,
            mission_instance_id=mission.mission_instance_id,
        )
        missions_completed.append(mission.mission_instance_id)
        day += timedelta(days=1)

    events = runtime.list_events(user_id=user.id, subject_code=subject_code)
    return {
        "journey": journey,
        "missions_completed": missions_completed,
        "topic_sequence": topic_sequence,
        "events": events,
        "days_elapsed": len(missions_completed),
    }
