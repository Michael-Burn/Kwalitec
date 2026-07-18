"""Shared helpers for curriculum management domain tests."""

from __future__ import annotations

from app.domain.curriculum_management.approval import Approval, ApprovalDecision
from app.domain.curriculum_management.blueprint_assignment import (
    BlueprintAssignment,
)
from app.domain.curriculum_management.curriculum_asset import (
    AssetKind,
    CurriculumAsset,
)
from app.domain.curriculum_management.curriculum_package import CurriculumPackage
from app.domain.curriculum_management.publication import Publication
from app.domain.curriculum_management.publication_history import (
    PublicationHistory,
)
from app.domain.curriculum_management.publication_state import PublicationState
from app.domain.curriculum_management.release_notes import (
    ReleaseNoteEntry,
    ReleaseNotes,
)
from app.domain.curriculum_management.subject import Subject
from app.domain.curriculum_management.subject_identifier import SubjectIdentifier
from app.domain.curriculum_management.subject_metadata import SubjectMetadata
from app.domain.curriculum_management.subject_version import SubjectVersion
from app.domain.curriculum_management.validation_report import (
    ValidationIssue,
    ValidationIssueCode,
    ValidationReport,
    ValidationSeverity,
)


def make_identifier(code: str = "CS1") -> SubjectIdentifier:
    return SubjectIdentifier.create(code)


def make_metadata(title: str = "Core Statistics") -> SubjectMetadata:
    return SubjectMetadata.create(title)


def make_subject(
    subject_id: str = "sub-1",
    code: str = "CS1",
    title: str = "Core Statistics",
    *,
    version_ids: tuple[str, ...] = (),
    active_version_id: str | None = None,
) -> Subject:
    return Subject.create(
        subject_id,
        code,
        make_metadata(title),
        version_ids=version_ids,
        active_version_id=active_version_id,
    )


def make_asset(
    asset_id: str = "asset-1",
    kind: AssetKind | str = AssetKind.SYLLABUS,
    reference: str = "s3://bucket/syllabus.pdf",
    label: str = "Syllabus",
) -> CurriculumAsset:
    return CurriculumAsset.create(asset_id, kind, reference, label)


def make_package(
    package_id: str = "pkg-1",
    version_id: str = "ver-1",
    *,
    with_syllabus: bool = True,
    with_cmp: bool = False,
) -> CurriculumPackage:
    assets: list[CurriculumAsset] = []
    if with_syllabus:
        assets.append(make_asset("a-syllabus", AssetKind.SYLLABUS))
    if with_cmp:
        assets.append(
            make_asset("a-cmp", AssetKind.CMP, "s3://bucket/cmp.json", "CMP")
        )
    return CurriculumPackage.create(package_id, version_id, assets=assets)


def make_assignment(
    assignment_id: str = "asg-1",
    version_id: str = "ver-1",
    section_ref: str = "ch1",
    blueprint_profile_id: str = "profile-concept-mastery",
    *,
    notes: str = "",
) -> BlueprintAssignment:
    return BlueprintAssignment.create(
        assignment_id,
        version_id,
        section_ref,
        blueprint_profile_id,
        notes=notes,
    )


def make_version(
    version_id: str = "ver-1",
    subject_id: str = "sub-1",
    version_label: str = "2026.1",
    *,
    package: CurriculumPackage | None = None,
    assignments: tuple[BlueprintAssignment, ...] = (),
    state: PublicationState = PublicationState.DRAFT,
    section_refs: tuple[str, ...] = (),
) -> SubjectVersion:
    publication = Publication.create(
        f"pub-{version_id}",
        version_id,
        state=state,
    )
    return SubjectVersion.create(
        version_id,
        subject_id,
        version_label,
        package=package,
        assignments=assignments,
        publication=publication,
        section_refs=section_refs,
    )


def make_issue(
    code: ValidationIssueCode = ValidationIssueCode.MISSING_SYLLABUS,
    message: str = "missing",
    *,
    severity: ValidationSeverity = ValidationSeverity.ERROR,
) -> ValidationIssue:
    return ValidationIssue.create(code, message, severity=severity)


def make_report(
    report_id: str = "rep-1",
    version_id: str = "ver-1",
    *,
    issues: tuple[ValidationIssue, ...] = (),
) -> ValidationReport:
    return ValidationReport.create(report_id, version_id, issues=issues)


def make_approval(
    approval_id: str = "apr-1",
    version_id: str = "ver-1",
    reviewer_id: str = "rev-1",
    decision: ApprovalDecision = ApprovalDecision.APPROVED,
) -> Approval:
    return Approval.create(approval_id, version_id, reviewer_id, decision)


def make_notes(
    notes_id: str = "notes-1",
    version_id: str = "ver-1",
    texts: tuple[str, ...] = ("Added prerequisite links.",),
) -> ReleaseNotes:
    entries = tuple(
        ReleaseNoteEntry.create(f"e{i}", text)
        for i, text in enumerate(texts, start=1)
    )
    return ReleaseNotes.create(notes_id, version_id, entries=entries)


def make_history(
    history_id: str = "hist-1",
    version_id: str = "ver-1",
) -> PublicationHistory:
    return PublicationHistory.create(history_id, version_id)
