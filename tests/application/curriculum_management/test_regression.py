"""End-to-end regression scenarios for Curriculum Management."""

from __future__ import annotations

import pytest

from app.application.curriculum_management import CurriculumManagementFacade
from app.application.curriculum_management.exceptions import (
    PolicyViolation,
    ValidationFailed,
)
from app.domain.curriculum_management.publication_state import PublicationState
from tests.application.curriculum_management.helpers import (
    advance_to_published,
    make_facade,
    seed_ready_version,
)


@pytest.mark.parametrize(
    "code,label",
    [
        ("CS1", "2026.1"),
        ("CS1", "2027.1"),
        ("CM1", "2026.1"),
        ("CB2", "2026.2"),
    ],
)
def test_publish_multiple_products(code, label):
    facade, subject_id, version = seed_ready_version(
        code=code,
        version_label=label,
        sections=("ch1", "ch2"),
    )
    advance_to_published(facade, version.version_id)
    subject = facade.subjects.get_subject(subject_id)
    assert subject.active_version_id == version.version_id
    assert (
        facade.versions.get_version(version.version_id).publication_state
        == PublicationState.PUBLISHED.value
    )


def test_cannot_mutate_archived_assets():
    facade, _, version = seed_ready_version()
    advance_to_published(facade, version.version_id)
    facade.publications.archive(version.version_id)
    with pytest.raises(PolicyViolation):
        facade.assets.add_asset(
            version.version_id,
            "supporting_document",
            "s3://x",
            "Extra",
        )


def test_preview_never_sets_published():
    facade, _, version = seed_ready_version()
    facade.validation.validate(version.version_id)
    for _ in range(3):
        preview = facade.previews.preview(version.version_id)
        assert preview.publication_state != "published"
        assert facade.versions.get_version(version.version_id).publication_state != (
            "published"
        )


def test_catalogue_clear():
    facade = make_facade()
    facade.subjects.create_subject("CS1", "S")
    facade.catalogue.clear()
    assert facade.subjects.list_subjects() == ()


def test_services_share_catalogue():
    facade = CurriculumManagementFacade()
    subject = facade.subjects.create_subject("CS1", "S")
    version = facade.versions.create_version(subject.subject_id, "2026.1")
    assert facade.subjects.catalogue is facade.catalogue
    assert facade.catalogue.get_subject(subject.subject_id) is not None
    assert facade.catalogue.get_version(version.version_id) is not None
    facade.assets.add_asset(version.version_id, "syllabus", "s3://x", "S")
    assert facade.catalogue.get_version(version.version_id).package is not None


def test_validation_failed_still_stores_report():
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    version = facade.versions.create_version(subject.subject_id, "2026.1")
    with pytest.raises(ValidationFailed):
        facade.validation.validate(version.version_id)
    assert facade.validation.latest(version.version_id) is not None


@pytest.mark.parametrize("n_sections", [1, 2, 3, 5, 8])
def test_preview_ready_for_approval_with_sections(n_sections):
    sections = tuple(f"s{i}" for i in range(n_sections))
    facade, _, version = seed_ready_version(sections=sections)
    facade.validation.validate(version.version_id)
    preview = facade.previews.preview(version.version_id)
    assert preview.assignment_count == n_sections
    assert preview.ready_for_approval


def test_release_snapshot_after_publish():
    facade, _, version = seed_ready_version()
    facade.releases.set_notes(
        version.version_id,
        headline="Release",
        entries=[("Added prerequisite links.", "structure")],
    )
    advance_to_published(facade, version.version_id, occurred_at="2026-07-18")
    release = facade.releases.get_release(version.version_id)
    assert release.is_published
    assert release.published_at == "2026-07-18"
    assert release.headline == "Release"
