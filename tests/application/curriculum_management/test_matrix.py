"""Parametrized service matrix and regression coverage."""

from __future__ import annotations

import pytest

from app.application.curriculum_management.exceptions import (
    AssetNotFound,
    PolicyViolation,
    PreviewError,
    SubjectNotFound,
    ValidationFailed,
    VersionNotFound,
)
from app.domain.curriculum_management.curriculum_asset import AssetKind
from app.domain.curriculum_management.publication_state import (
    PublicationState,
    PublicationTransitionEvent,
)
from tests.application.curriculum_management.helpers import (
    advance_to_preview,
    advance_to_published,
    make_facade,
    seed_ready_version,
)

ASSET_KINDS = [
    AssetKind.CMP,
    AssetKind.SYLLABUS,
    AssetKind.LEARNING_OBJECTIVES,
    AssetKind.FORMULA_SHEET,
    AssetKind.SUPPORTING_DOCUMENT,
]


@pytest.mark.parametrize("kind", ASSET_KINDS)
def test_add_each_asset_kind(kind):
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    version = facade.versions.create_version(subject.subject_id, "2026.1")
    updated = facade.assets.add_asset(
        version.version_id,
        kind,
        f"s3://bucket/{kind.value}",
        kind.value,
    )
    assert kind.value in updated.asset_kinds
    assert updated.publication_state == "uploaded"


@pytest.mark.parametrize(
    "label",
    [f"2026.{n}" for n in range(1, 13)]
    + [f"2027.{n}" for n in range(1, 6)],
)
def test_version_labels_accepted(label):
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    snap = facade.versions.create_version(subject.subject_id, label)
    assert snap.version_label == label


@pytest.mark.parametrize(
    "code,title",
    [
        ("CS1", "Core Statistics 1"),
        ("CM1", "Core Mathematics 1"),
        ("CB2", "Core Business 2"),
        ("FS1", "Further Stats 1"),
        ("FM1", "Further Maths 1"),
        ("CP1", "Core Pure 1"),
        ("CP2", "Core Pure 2"),
        ("MEI1", "MEI Mechanics"),
    ],
)
def test_create_many_subjects(code, title):
    facade = make_facade()
    snap = facade.subjects.create_subject(code, title, tags=["exam", code.lower()])
    assert snap.code == code
    assert snap.title == title
    assert code.lower() in snap.tags


@pytest.mark.parametrize(
    "section",
    [f"ch{i}" for i in range(1, 21)],
)
def test_assign_many_sections(section):
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    version = facade.versions.create_version(subject.subject_id, "2026.1")
    facade.assets.add_asset(version.version_id, "syllabus", "s3://s", "S")
    updated = facade.assignments.assign(
        version.version_id,
        section,
        "profile-concept-mastery",
    )
    assert updated.assignment_count == 1


@pytest.mark.parametrize(
    "event,from_state",
    [
        (PublicationTransitionEvent.MARK_UPLOADED, PublicationState.DRAFT),
        (PublicationTransitionEvent.REVERT_TO_DRAFT, PublicationState.UPLOADED),
        (
            PublicationTransitionEvent.MARK_VALIDATED,
            PublicationState.UPLOADED,
        ),
        (
            PublicationTransitionEvent.REVERT_TO_UPLOADED,
            PublicationState.VALIDATED,
        ),
        (
            PublicationTransitionEvent.MARK_BLUEPRINT_ASSIGNED,
            PublicationState.VALIDATED,
        ),
        (
            PublicationTransitionEvent.REVERT_TO_VALIDATED,
            PublicationState.BLUEPRINT_ASSIGNED,
        ),
        (
            PublicationTransitionEvent.MARK_PREVIEW_READY,
            PublicationState.BLUEPRINT_ASSIGNED,
        ),
        (
            PublicationTransitionEvent.REVERT_TO_BLUEPRINT_ASSIGNED,
            PublicationState.PREVIEW_READY,
        ),
        (
            PublicationTransitionEvent.MARK_APPROVED,
            PublicationState.PREVIEW_READY,
        ),
        (
            PublicationTransitionEvent.REVERT_TO_PREVIEW_READY,
            PublicationState.APPROVED,
        ),
        (
            PublicationTransitionEvent.MARK_PUBLISHED,
            PublicationState.APPROVED,
        ),
        (
            PublicationTransitionEvent.MARK_ARCHIVED,
            PublicationState.PUBLISHED,
        ),
    ],
)
def test_explicit_publication_transitions(event, from_state):
    """Drive to from_state then apply event via PublicationService.transition."""
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    version = facade.versions.create_version(subject.subject_id, "2026.1")
    # Force state by successive lawful forward transitions as needed.
    order = [
        PublicationState.DRAFT,
        PublicationState.UPLOADED,
        PublicationState.VALIDATED,
        PublicationState.BLUEPRINT_ASSIGNED,
        PublicationState.PREVIEW_READY,
        PublicationState.APPROVED,
        PublicationState.PUBLISHED,
    ]
    target_idx = (
        order.index(from_state) if from_state in order else -1
    )
    forwards = [
        PublicationTransitionEvent.MARK_UPLOADED,
        PublicationTransitionEvent.MARK_VALIDATED,
        PublicationTransitionEvent.MARK_BLUEPRINT_ASSIGNED,
        PublicationTransitionEvent.MARK_PREVIEW_READY,
        PublicationTransitionEvent.MARK_APPROVED,
        PublicationTransitionEvent.MARK_PUBLISHED,
    ]
    for i in range(target_idx):
        facade.publications.transition(version.version_id, forwards[i])
    snap = facade.publications.transition(version.version_id, event)
    assert snap.state in {s.value for s in PublicationState}


def test_set_section_refs():
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    version = facade.versions.create_version(subject.subject_id, "2026.1")
    updated = facade.versions.set_section_refs(
        version.version_id,
        ["a", "b", "c"],
    )
    assert updated.section_refs == ("a", "b", "c")
    assert updated.section_count == 3


def test_set_section_refs_locked_when_approved():
    facade, _, version = seed_ready_version()
    advance_to_preview(facade, version.version_id)
    facade.approvals.approve(version.version_id, "rev")
    with pytest.raises(PolicyViolation):
        facade.versions.set_section_refs(version.version_id, ["x"])


def test_remove_missing_asset():
    facade, _, version = seed_ready_version()
    with pytest.raises(AssetNotFound):
        facade.assets.remove_asset(version.version_id, "missing")


def test_validation_latest_none():
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    version = facade.versions.create_version(subject.subject_id, "2026.1")
    assert facade.validation.latest(version.version_id) is None


def test_approval_latest_none():
    facade, _, version = seed_ready_version()
    assert facade.approvals.latest(version.version_id) is None


def test_list_assignments():
    facade, _, version = seed_ready_version()
    assignments = facade.assignments.list_assignments(version.version_id)
    assert len(assignments) >= 1


def test_publication_history_accumulates():
    facade, _, version = seed_ready_version()
    advance_to_published(facade, version.version_id)
    pub = facade.publications.get_publication(version.version_id)
    assert pub.history_count >= 4
    assert pub.is_published


def test_preview_without_package_raises():
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    version = facade.versions.create_version(subject.subject_id, "2026.1")
    # Force validated without package via raw transition
    facade.publications.transition(
        version.version_id,
        PublicationTransitionEvent.MARK_UPLOADED,
    )
    facade.publications.transition(
        version.version_id,
        PublicationTransitionEvent.MARK_VALIDATED,
    )
    with pytest.raises(PreviewError):
        facade.previews.preview(version.version_id)


def test_subject_set_active_unknown_version():
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    with pytest.raises(SubjectNotFound):
        facade.subjects.set_active_version(subject.subject_id, "nope")


def test_version_for_missing_subject():
    facade = make_facade()
    with pytest.raises(SubjectNotFound):
        facade.versions.create_version("missing", "2026.1")


@pytest.mark.parametrize("missing_id", ["v-missing", "nope", "version-999"])
def test_services_version_not_found(missing_id):
    facade = make_facade()
    with pytest.raises(VersionNotFound):
        facade.assets.add_asset(missing_id, "syllabus", "s3://x", "S")
    with pytest.raises(VersionNotFound):
        facade.validation.validate(missing_id)
    with pytest.raises(VersionNotFound):
        facade.approvals.approve(missing_id, "r")
    with pytest.raises(VersionNotFound):
        facade.previews.preview(missing_id)
    with pytest.raises(VersionNotFound):
        facade.publications.publish(missing_id)
    with pytest.raises(VersionNotFound):
        facade.releases.get_release(missing_id)


def test_immutable_validation_reports_accumulate():
    facade, _, version = seed_ready_version()
    facade.validation.validate(version.version_id)
    # Mutate package then re-validate without advancing
    ids = facade.assets.list_asset_ids(version.version_id)
    facade.assets.remove_asset(version.version_id, ids[0])
    with pytest.raises(ValidationFailed):
        facade.validation.validate(version.version_id, advance_state=False)
    domain_version = facade.catalogue.get_version(version.version_id)
    assert domain_version is not None
    assert len(domain_version.validation_reports) == 2


def test_regression_education_platform_untouched():
    """Ensure EducationPlatform source still exists and is unchanged by imports."""
    from pathlib import Path

    path = Path("app/application/education_platform/platform.py")
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "class EducationPlatform" in text
    assert "curriculum_management" not in text


@pytest.mark.parametrize(
    "text",
    [
        "Added prerequisite links.",
        "Updated blueprint assignments.",
        "Improved session estimates.",
        "Clarified syllabus reference.",
        "Aligned formula sheet.",
    ],
)
def test_release_note_entries(text):
    facade, _, version = seed_ready_version()
    snap = facade.releases.add_entry(version.version_id, text)
    assert text in snap.entries
