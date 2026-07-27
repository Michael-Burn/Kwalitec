"""Helpers shared by Educational Runtime Engine application tests."""

from __future__ import annotations

from app.application.curriculum_studio_foundation.service import (
    CurriculumStudioFoundationService,
)
from app.models.user import User


def make_user(email: str = "runtime-student@example.com") -> User:
    user = User(email=email)
    user.set_password("password123")
    from app.extensions import db

    db.session.add(user)
    db.session.commit()
    return user


def publish_subject(
    subject_code: str = "LAW9",
    *,
    version_label: str = "2027.1",
    title: str = "Published Law Subject",
) -> str:
    """Publish a minimal two-topic subject and return the subject code."""
    foundation = CurriculumStudioFoundationService()
    foundation.create_subject(subject_code, title=title, actor_id="founder")
    version = foundation.create_version(
        subject_code, version_label, actor_id="founder"
    )
    structure = {
        "entries": [
            {
                "entry_id": "s1",
                "entry_type": "section",
                "text": "Foundations",
                "number": "1",
            },
            {
                "entry_id": "t1",
                "entry_type": "topic",
                "text": "Offer and acceptance",
                "number": "1.1",
                "parent_ref": "s1",
            },
            {
                "entry_id": "o1",
                "entry_type": "objective",
                "text": "Explain formation basics",
                "number": "1.1.1",
                "parent_ref": "t1",
            },
            {
                "entry_id": "s2",
                "entry_type": "section",
                "text": "Remedies",
                "number": "2",
            },
            {
                "entry_id": "t2",
                "entry_type": "topic",
                "text": "Damages",
                "number": "2.1",
                "parent_ref": "s2",
                "attributes": {"prerequisites": "t1"},
            },
            {
                "entry_id": "o2",
                "entry_type": "objective",
                "text": "Apply damages principles",
                "number": "2.1.1",
                "parent_ref": "t2",
            },
        ]
    }
    foundation.upload_document(
        version.version_id,
        kind="cmp",
        reference=f"ref://cmp/{subject_code.lower()}",
        structure=structure,
        actor_id="founder",
    )
    foundation.upload_document(
        version.version_id,
        kind="syllabus",
        reference=f"ref://syllabus/{subject_code.lower()}",
        structure=structure,
        actor_id="founder",
    )
    foundation.process_curriculum(version.version_id, actor_id="founder")
    foundation.validate_curriculum(version.version_id, actor_id="founder")
    foundation.founder_review(version.version_id, actor_id="founder")
    foundation.publish_curriculum(version.version_id, actor_id="founder")
    return subject_code.upper()
