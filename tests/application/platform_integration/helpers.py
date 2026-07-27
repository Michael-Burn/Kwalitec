"""Helpers for PI-002A Founder → Student bridge tests."""

from __future__ import annotations

from app.application.curriculum_studio_foundation.service import (
    CurriculumStudioFoundationService,
)
from app.application.platform_integration.flags import FounderStudentBridgeFlags
from app.extensions import db
from app.models.user import User

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
    ],
}


def make_user(email: str = "bridge@example.com") -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    user.alpha_onboarding_completed = True
    db.session.add(user)
    db.session.commit()
    return user


def publish_subject(
    subject_code: str = "BRG1",
    *,
    title: str = "Bridge Subject",
    version_label: str = "2027.1",
) -> str:
    foundation = CurriculumStudioFoundationService()
    foundation.create_subject(subject_code, title=title, actor_id="founder")
    version = foundation.create_version(
        subject_code, version_label, actor_id="founder"
    )
    foundation.upload_document(
        version.version_id,
        kind="cmp",
        reference=f"ref://cmp/{subject_code.lower()}",
        structure=STANDARD_STRUCTURE,
        actor_id="founder",
    )
    foundation.upload_document(
        version.version_id,
        kind="syllabus",
        reference=f"ref://syllabus/{subject_code.lower()}",
        structure=STANDARD_STRUCTURE,
        actor_id="founder",
    )
    foundation.process_curriculum(version.version_id, actor_id="founder")
    foundation.validate_curriculum(version.version_id, actor_id="founder")
    foundation.founder_review(version.version_id, actor_id="founder")
    foundation.publish_curriculum(version.version_id, actor_id="founder")
    return subject_code.upper()


def bridge_flags(
    *,
    discovery: bool = True,
    enrolment: bool = True,
    allowlist: frozenset[str] | None = None,
) -> FounderStudentBridgeFlags:
    return FounderStudentBridgeFlags(
        ENABLE_PUBLISHED_SUBJECT_DISCOVERY=discovery,
        ENABLE_RUNTIME_C_ENROLMENT=enrolment,
        RUNTIME_C_SUBJECT_ALLOWLIST=allowlist or frozenset(),
    )
