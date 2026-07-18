"""Shared helpers for curriculum management application tests."""

from __future__ import annotations

from app.application.curriculum_management import CurriculumManagementFacade
from app.application.curriculum_management.dto.version_snapshot import (
    VersionSnapshot,
)


def make_facade() -> CurriculumManagementFacade:
    return CurriculumManagementFacade()


def seed_ready_version(
    facade: CurriculumManagementFacade | None = None,
    *,
    code: str = "CS1",
    title: str = "Core Statistics",
    version_label: str = "2026.1",
    sections: tuple[str, ...] = ("ch1",),
) -> tuple[CurriculumManagementFacade, str, VersionSnapshot]:
    """Create subject+version with syllabus, CMP, and blueprint assignments."""
    facade = facade or make_facade()
    subject = facade.subjects.create_subject(code, title)
    version = facade.versions.create_version(
        subject.subject_id,
        version_label,
        section_refs=sections,
    )
    facade.assets.add_asset(
        version.version_id,
        "syllabus",
        f"s3://bucket/{code.lower()}-syllabus",
        "Syllabus",
    )
    facade.assets.add_asset(
        version.version_id,
        "cmp",
        f"s3://bucket/{code.lower()}-cmp",
        "CMP",
    )
    facade.assets.add_asset(
        version.version_id,
        "learning_objectives",
        f"s3://bucket/{code.lower()}-lo",
        "Learning Objectives",
    )
    for section in sections:
        facade.assignments.assign(
            version.version_id,
            section,
            "profile-concept-mastery",
        )
    return facade, subject.subject_id, facade.versions.get_version(version.version_id)


def advance_to_preview(
    facade: CurriculumManagementFacade,
    version_id: str,
):
    """Validate + preview a ready version."""
    facade.validation.validate(version_id)
    return facade.previews.preview(version_id)


def advance_to_published(
    facade: CurriculumManagementFacade,
    version_id: str,
    *,
    reviewer_id: str = "reviewer-1",
    occurred_at: str = "2026-07-18T10:00:00Z",
):
    """Drive a ready version through preview → approve → publish."""
    advance_to_preview(facade, version_id)
    facade.approvals.approve(version_id, reviewer_id, decided_at=occurred_at)
    return facade.publications.publish(
        version_id,
        actor_id=reviewer_id,
        occurred_at=occurred_at,
    )
