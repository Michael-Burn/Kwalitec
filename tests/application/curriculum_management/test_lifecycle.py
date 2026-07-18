"""Application service lifecycle and happy-path tests."""

from __future__ import annotations

import pytest

from app.application.curriculum_management.exceptions import (
    AssetError,
    BlueprintAssignmentError,
    PolicyViolation,
    PreviewError,
    PublicationError,
    SubjectAlreadyExists,
    SubjectNotFound,
    ValidationFailed,
    VersionAlreadyExists,
    VersionNotFound,
)
from app.domain.curriculum_management.publication_state import PublicationState
from tests.application.curriculum_management.helpers import (
    advance_to_preview,
    advance_to_published,
    make_facade,
    seed_ready_version,
)


def test_full_publication_lifecycle():
    facade, subject_id, version = seed_ready_version()
    assert version.publication_state == PublicationState.UPLOADED.value
    advance_to_published(facade, version.version_id)
    snap = facade.versions.get_version(version.version_id)
    assert snap.publication_state == PublicationState.PUBLISHED.value
    subject = facade.subjects.get_subject(subject_id)
    assert subject.active_version_id == version.version_id
    archived = facade.publications.archive(version.version_id)
    assert archived.state == PublicationState.ARCHIVED.value


def test_create_subject_duplicate_code():
    facade = make_facade()
    facade.subjects.create_subject("CS1", "A")
    with pytest.raises(SubjectAlreadyExists):
        facade.subjects.create_subject("CS1", "B")


def test_get_subject_by_code():
    facade = make_facade()
    created = facade.subjects.create_subject("CM1", "Core Maths")
    found = facade.subjects.get_subject_by_code("cm1")
    assert found.subject_id == created.subject_id


def test_subject_not_found():
    facade = make_facade()
    with pytest.raises(SubjectNotFound):
        facade.subjects.get_subject("missing")


def test_list_subjects_ordered():
    facade = make_facade()
    facade.subjects.create_subject("CS1", "S")
    facade.subjects.create_subject("CB2", "B")
    facade.subjects.create_subject("CM1", "M")
    codes = [s.code for s in facade.subjects.list_subjects()]
    assert codes == ["CB2", "CM1", "CS1"]


def test_update_metadata():
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "Old")
    updated = facade.subjects.update_metadata(
        subject.subject_id,
        title="New",
        tags=["exam"],
    )
    assert updated.title == "New"
    assert updated.tags == ("exam",)


def test_create_version_and_duplicate_label():
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    facade.versions.create_version(subject.subject_id, "2026.1")
    with pytest.raises(VersionAlreadyExists):
        facade.versions.create_version(subject.subject_id, "2026.1")


def test_version_not_found():
    facade = make_facade()
    with pytest.raises(VersionNotFound):
        facade.versions.get_version("missing")


def test_add_asset_advances_to_uploaded():
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    version = facade.versions.create_version(subject.subject_id, "2026.1")
    assert version.publication_state == "draft"
    updated = facade.assets.add_asset(
        version.version_id,
        "syllabus",
        "s3://x/s",
        "Syllabus",
    )
    assert updated.publication_state == "uploaded"
    assert updated.asset_count == 1


def test_add_asset_rejects_data_uri():
    facade, _, version = seed_ready_version()
    with pytest.raises(AssetError):
        facade.assets.add_asset(
            version.version_id,
            "supporting_document",
            "data:text/plain,hi",
            "Bad",
        )


def test_remove_asset():
    facade, _, version = seed_ready_version()
    ids = facade.assets.list_asset_ids(version.version_id)
    assert ids
    updated = facade.assets.remove_asset(version.version_id, ids[0])
    assert updated.asset_count == version.asset_count - 1


def test_validation_fails_without_syllabus():
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    version = facade.versions.create_version(subject.subject_id, "2026.1")
    facade.assets.add_asset(version.version_id, "cmp", "s3://x/c", "CMP")
    with pytest.raises(ValidationFailed):
        facade.validation.validate(version.version_id)
    latest = facade.validation.latest(version.version_id)
    assert latest is not None
    assert latest.blocks_publication


def test_validation_requires_assignments():
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    version = facade.versions.create_version(subject.subject_id, "2026.1")
    facade.assets.add_asset(version.version_id, "syllabus", "s3://x/s", "S")
    with pytest.raises(ValidationFailed):
        facade.validation.validate(version.version_id)


def test_assign_duplicate_section():
    facade, _, version = seed_ready_version()
    with pytest.raises(BlueprintAssignmentError):
        facade.assignments.assign(
            version.version_id,
            "ch1",
            "profile-other",
        )


def test_preview_rejects_draft():
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    version = facade.versions.create_version(subject.subject_id, "2026.1")
    with pytest.raises(PreviewError):
        facade.previews.preview(version.version_id)


def test_preview_is_immutable_and_does_not_publish():
    facade, _, version = seed_ready_version()
    facade.validation.validate(version.version_id)
    preview = facade.previews.preview(version.version_id)
    assert preview.publication_state == "preview_ready"
    assert facade.versions.get_version(version.version_id).publication_state != (
        "published"
    )
    # Second preview does not mutate further
    preview2 = facade.previews.preview(version.version_id, advance_state=False)
    assert preview2.preview_id != preview.preview_id


def test_approve_requires_preview_ready():
    facade, _, version = seed_ready_version()
    with pytest.raises(PolicyViolation):
        facade.approvals.approve(version.version_id, "rev")


def test_reject_does_not_advance():
    facade, _, version = seed_ready_version()
    advance_to_preview(facade, version.version_id)
    rejected = facade.approvals.reject(
        version.version_id,
        "rev",
        rationale="needs work",
    )
    assert rejected.decision == "rejected"
    assert (
        facade.versions.get_version(version.version_id).publication_state
        == "preview_ready"
    )


def test_publish_requires_approved():
    facade, _, version = seed_ready_version()
    facade.validation.validate(version.version_id)
    with pytest.raises(PolicyViolation):
        facade.publications.publish(version.version_id)


def test_archive_requires_published():
    facade, _, version = seed_ready_version()
    with pytest.raises(PublicationError):
        facade.publications.archive(version.version_id)


def test_release_notes():
    facade, _, version = seed_ready_version()
    snap = facade.releases.set_notes(
        version.version_id,
        headline="2026.1",
        entries=[
            ("Added prerequisite links.", "structure"),
            ("Updated blueprint assignments.", "blueprint"),
            ("Improved session estimates.", "planning"),
        ],
    )
    assert snap.entry_count == 3
    assert "Added prerequisite links." in snap.entries
    added = facade.releases.add_entry(
        version.version_id,
        "Clarified formula sheet reference.",
    )
    assert added.entry_count == 4


def test_two_versions_independent():
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    v1 = facade.versions.create_version(subject.subject_id, "2026.1")
    v2 = facade.versions.create_version(subject.subject_id, "2027.1")
    facade.assets.add_asset(v1.version_id, "syllabus", "s3://a", "S")
    assert facade.versions.get_version(v2.version_id).asset_count == 0
    assert facade.versions.get_version(v1.version_id).asset_count == 1


@pytest.mark.parametrize("code", ["CS1", "CM1", "CB2"])
def test_subject_codes_roundtrip(code):
    facade = make_facade()
    snap = facade.subjects.create_subject(code, f"Title {code}")
    assert snap.code == code
