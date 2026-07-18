"""DTO immutability and projection tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.curriculum_management._snapshots import (
    approval_snapshot,
    publication_snapshot,
    release_snapshot,
    subject_snapshot,
    subject_summary,
    validation_snapshot,
    version_snapshot,
)
from app.application.curriculum_management.dto import (
    ApprovalSnapshot,
    PreviewSnapshot,
    PublicationSnapshot,
    ReleaseSnapshot,
    SubjectSnapshot,
    SubjectSummary,
    ValidationIssueSnapshot,
    ValidationSnapshot,
    VersionSnapshot,
)
from app.domain.curriculum_management.publication import Publication
from app.domain.curriculum_management.publication_state import PublicationState
from tests.application.curriculum_management.helpers import (
    make_facade,
    seed_ready_version,
)
from tests.domain.curriculum_management.helpers import (
    make_approval,
    make_package,
    make_report,
    make_subject,
    make_version,
)


@pytest.mark.parametrize(
    "cls,kwargs",
    [
        (
            SubjectSnapshot,
            {
                "subject_id": "s",
                "code": "CS1",
                "title": "T",
            },
        ),
        (
            SubjectSummary,
            {"subject_id": "s", "code": "CS1", "title": "T"},
        ),
        (
            VersionSnapshot,
            {
                "version_id": "v",
                "subject_id": "s",
                "version_label": "2026.1",
                "display_name": "s 2026.1",
                "publication_state": "draft",
            },
        ),
        (
            PublicationSnapshot,
            {
                "publication_id": "p",
                "version_id": "v",
                "state": "draft",
            },
        ),
        (
            ValidationSnapshot,
            {
                "report_id": "r",
                "version_id": "v",
                "passed": True,
                "summary": "ok",
            },
        ),
        (
            ValidationIssueSnapshot,
            {
                "code": "missing_syllabus",
                "message": "m",
                "severity": "error",
            },
        ),
        (
            ApprovalSnapshot,
            {
                "approval_id": "a",
                "version_id": "v",
                "reviewer_id": "r",
                "decision": "approved",
            },
        ),
        (
            PreviewSnapshot,
            {
                "preview_id": "p",
                "version_id": "v",
                "subject_id": "s",
                "version_label": "2026.1",
                "display_name": "s 2026.1",
                "publication_state": "preview_ready",
            },
        ),
        (
            ReleaseSnapshot,
            {
                "version_id": "v",
                "subject_id": "s",
                "version_label": "2026.1",
                "display_name": "s 2026.1",
                "publication_state": "draft",
            },
        ),
    ],
)
def test_dto_frozen(cls, kwargs):
    dto = cls(**kwargs)
    field = next(iter(kwargs))
    with pytest.raises(FrozenInstanceError):
        setattr(dto, field, kwargs[field])


def test_subject_snapshot_projection():
    subject = make_subject(version_ids=("v1",), active_version_id="v1")
    snap = subject_snapshot(subject)
    assert snap.code == "CS1"
    assert snap.version_count == 1
    assert snap.active_version_id == "v1"


def test_subject_summary_with_active():
    subject = make_subject(version_ids=("ver-1",), active_version_id="ver-1")
    version = make_version(
        version_id="ver-1",
        state=PublicationState.PUBLISHED,
    )
    summary = subject_summary(subject, active_version=version)
    assert summary.publication_state == "published"
    assert summary.active_version_label == "2026.1"


def test_version_snapshot_projection():
    version = make_version(package=make_package(with_cmp=True))
    snap = version_snapshot(version)
    assert snap.asset_count == 2
    assert "syllabus" in snap.asset_kinds
    assert "cmp" in snap.asset_kinds


def test_publication_snapshot_projection():
    pub = Publication.create("p1", "v1")
    from app.domain.curriculum_management.publication_state import (
        PublicationTransitionEvent,
    )

    pub = pub.transition(PublicationTransitionEvent.MARK_UPLOADED)
    snap = publication_snapshot(pub)
    assert snap.history_count == 1
    assert snap.latest_event == "mark_uploaded"
    assert snap.history_events == ("mark_uploaded",)


def test_validation_and_approval_snapshots():
    report = make_report()
    vs = validation_snapshot(report)
    assert vs.passed
    apr = approval_snapshot(make_approval())
    assert apr.is_approved


def test_release_snapshot_empty_notes():
    snap = release_snapshot(make_version())
    assert snap.entry_count == 0
    assert snap.notes_id is None


def test_preview_snapshot_from_service():
    facade, _, version = seed_ready_version()
    facade.validation.validate(version.version_id)
    preview = facade.previews.preview(version.version_id)
    assert isinstance(preview, PreviewSnapshot)
    with pytest.raises(FrozenInstanceError):
        preview.asset_count = 99  # type: ignore[misc]


def test_dto_package_exports():
    from app.application.curriculum_management import dto as dto_pkg

    assert dto_pkg.SubjectSnapshot is SubjectSnapshot
    assert "VersionSnapshot" in dir(dto_pkg)


def test_facade_list_and_get_snapshots():
    facade = make_facade()
    subject = facade.subjects.create_subject("CS1", "S")
    version = facade.versions.create_version(subject.subject_id, "2026.1")
    assert facade.versions.list_versions(subject_id=subject.subject_id)
    pub = facade.publications.get_publication(version.version_id)
    assert pub.state == "draft"
    assert facade.releases.get_release(version.version_id).version_id == (
        version.version_id
    )
