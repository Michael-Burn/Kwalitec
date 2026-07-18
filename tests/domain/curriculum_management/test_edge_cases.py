"""Additional domain edge cases and package export coverage."""

from __future__ import annotations

import pytest

from app.domain.curriculum_management import (
    AssetKind,
    PublicationState,
    Subject,
    SubjectIdentifier,
    SubjectMetadata,
    SubjectVersion,
    resolve_asset_kind,
)
from app.domain.curriculum_management.curriculum_asset import CurriculumAsset
from app.domain.curriculum_management.curriculum_package import CurriculumPackage
from app.domain.curriculum_management.publication import Publication
from app.domain.curriculum_management.release_notes import ReleaseNoteEntry
from app.domain.curriculum_management.validation_report import (
    ValidationIssue,
    ValidationIssueCode,
    ValidationSeverity,
)


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("CMP", AssetKind.CMP),
        ("Syllabus", AssetKind.SYLLABUS),
        ("learning-objectives", AssetKind.LEARNING_OBJECTIVES),
        ("supporting", AssetKind.SUPPORTING_DOCUMENT),
        ("support", AssetKind.SUPPORTING_DOCUMENT),
        ("document", AssetKind.SUPPORTING_DOCUMENT),
        ("formula", AssetKind.FORMULA_SHEET),
    ],
)
def test_resolve_asset_kind_variants(raw, expected):
    assert resolve_asset_kind(raw) is expected


def test_resolve_asset_kind_unknown():
    with pytest.raises(ValueError):
        resolve_asset_kind("unknown-kind")


@pytest.mark.parametrize(
    "code,message,severity,blocking",
    [
        (
            ValidationIssueCode.MISSING_SYLLABUS,
            "Missing syllabus",
            ValidationSeverity.ERROR,
            True,
        ),
        (
            ValidationIssueCode.MISSING_CMP,
            "Missing CMP",
            ValidationSeverity.WARNING,
            False,
        ),
        (
            ValidationIssueCode.PUBLICATION_BLOCKED,
            "Blocked",
            ValidationSeverity.ERROR,
            True,
        ),
        (
            ValidationIssueCode.DUPLICATE_TOPIC,
            "Dup",
            ValidationSeverity.ERROR,
            False,
        ),
        (
            ValidationIssueCode.INVALID_REFERENCE,
            "Bad ref",
            ValidationSeverity.INFO,
            False,
        ),
        (
            ValidationIssueCode.EMPTY_PACKAGE,
            "Empty",
            ValidationSeverity.BLOCKING,
            True,
        ),
        (
            ValidationIssueCode.MISSING_BLUEPRINT_ASSIGNMENT,
            "No BP",
            ValidationSeverity.ERROR,
            True,
        ),
        (
            ValidationIssueCode.MISSING_LEARNING_OBJECTIVES,
            "No LO",
            ValidationSeverity.WARNING,
            False,
        ),
        (
            ValidationIssueCode.DUPLICATE_SECTION,
            "Dup section",
            ValidationSeverity.ERROR,
            False,
        ),
        (
            ValidationIssueCode.OTHER,
            "Other",
            ValidationSeverity.INFO,
            False,
        ),
    ],
)
def test_validation_issue_blocking_matrix(code, message, severity, blocking):
    issue = ValidationIssue.create(code, message, severity=severity)
    assert issue.is_blocking is blocking


@pytest.mark.parametrize(
    "state",
    [
        PublicationState.DRAFT,
        PublicationState.UPLOADED,
        PublicationState.VALIDATED,
        PublicationState.BLUEPRINT_ASSIGNED,
        PublicationState.PREVIEW_READY,
        PublicationState.APPROVED,
        PublicationState.PUBLISHED,
        PublicationState.ARCHIVED,
    ],
)
def test_publication_create_in_each_state(state):
    pub = Publication.create("p1", "v1", state=state)
    assert pub.state is state
    if state is PublicationState.PUBLISHED:
        assert pub.published_at is not None
    if state is PublicationState.ARCHIVED:
        assert pub.archived_at is not None


@pytest.mark.parametrize(
    "category",
    [
        "structure",
        "blueprint",
        "planning",
        "general",
        "assets",
        "validation",
    ],
)
def test_release_note_categories(category):
    entry = ReleaseNoteEntry.create("e1", "Change", category=category)
    assert entry.category == category


@pytest.mark.parametrize(
    "media_type",
    [
        "application/pdf",
        "application/json",
        "text/plain",
        "application/vnd.kwalitec.cmp+json",
    ],
)
def test_asset_media_types(media_type):
    asset = CurriculumAsset.create(
        "a1",
        AssetKind.SUPPORTING_DOCUMENT,
        "s3://bucket/doc",
        "Doc",
        media_type=media_type,
        checksum="abc",
    )
    assert asset.media_type == media_type
    assert asset.checksum == "abc"


@pytest.mark.parametrize("n", range(1, 16))
def test_package_many_assets(n):
    assets = [
        CurriculumAsset.create(
            f"a{i}",
            AssetKind.SUPPORTING_DOCUMENT,
            f"s3://bucket/{i}",
            f"Doc {i}",
        )
        for i in range(n)
    ]
    package = CurriculumPackage.create("p1", "v1", assets=assets)
    assert package.asset_count == n


@pytest.mark.parametrize(
    "year,minor",
    [(y, m) for y in (2025, 2026, 2027, 2028) for m in (1, 2, 3)],
)
def test_subject_version_labels_matrix(year, minor):
    label = f"{year}.{minor}"
    version = SubjectVersion.create("v1", "s1", label)
    assert version.version_label == label


@pytest.mark.parametrize("locale", ["en-GB", "en-US", "fr-FR", "de-DE"])
def test_metadata_locales(locale):
    md = SubjectMetadata.create("T", locale=locale)
    assert md.locale == locale


def test_package_exports():
    assert SubjectIdentifier.create("CS1").code == "CS1"
    subject = Subject.create(
        "s1",
        "CS1",
        SubjectMetadata.create("Core Stats"),
    )
    assert subject.code == "CS1"


def test_asset_by_id_blank_returns_none():
    package = CurriculumPackage.create("p1", "v1")
    assert package.asset_by_id("") is None
    assert package.asset_by_id("  ") is None
