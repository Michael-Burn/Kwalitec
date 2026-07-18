"""DTO projection helpers for Curriculum Management."""

from __future__ import annotations

from app.application.curriculum_management.dto.approval_snapshot import (
    ApprovalSnapshot,
)
from app.application.curriculum_management.dto.publication_snapshot import (
    PublicationSnapshot,
)
from app.application.curriculum_management.dto.release_snapshot import (
    ReleaseSnapshot,
)
from app.application.curriculum_management.dto.subject_snapshot import (
    SubjectSnapshot,
)
from app.application.curriculum_management.dto.subject_summary import (
    SubjectSummary,
)
from app.application.curriculum_management.dto.validation_snapshot import (
    ValidationIssueSnapshot,
    ValidationSnapshot,
)
from app.application.curriculum_management.dto.version_snapshot import (
    VersionSnapshot,
)
from app.domain.curriculum_management.approval import Approval
from app.domain.curriculum_management.publication import Publication
from app.domain.curriculum_management.subject import Subject
from app.domain.curriculum_management.subject_version import SubjectVersion
from app.domain.curriculum_management.validation_report import ValidationReport


def subject_snapshot(subject: Subject) -> SubjectSnapshot:
    """Project a Subject into an immutable snapshot."""
    return SubjectSnapshot(
        subject_id=subject.subject_id,
        code=subject.code,
        title=subject.title,
        description=subject.metadata.description,
        exam_board=subject.metadata.exam_board,
        academic_year=subject.metadata.academic_year,
        locale=subject.metadata.locale,
        tags=subject.metadata.tags,
        version_ids=subject.version_ids,
        active_version_id=subject.active_version_id,
        version_count=subject.version_count,
    )


def subject_summary(
    subject: Subject,
    *,
    active_version: SubjectVersion | None = None,
) -> SubjectSummary:
    """Project a Subject into a compact summary row."""
    state = None
    label = None
    if active_version is not None:
        state = active_version.state.value
        label = active_version.version_label
    return SubjectSummary(
        subject_id=subject.subject_id,
        code=subject.code,
        title=subject.title,
        version_count=subject.version_count,
        active_version_id=subject.active_version_id,
        active_version_label=label,
        publication_state=state,
    )


def version_snapshot(version: SubjectVersion) -> VersionSnapshot:
    """Project a SubjectVersion into an immutable snapshot."""
    package = version.package
    latest_val = version.latest_validation
    latest_apr = version.latest_approval
    kinds = tuple(sorted({a.kind.value for a in (package.assets if package else ())}))
    return VersionSnapshot(
        version_id=version.version_id,
        subject_id=version.subject_id,
        version_label=version.version_label,
        display_name=version.display_name,
        publication_state=version.state.value,
        asset_count=package.asset_count if package else 0,
        assignment_count=len(version.assignments),
        section_count=len(version.section_refs),
        validation_passed=None if latest_val is None else latest_val.passed,
        approval_decision=(
            None if latest_apr is None else latest_apr.decision.value
        ),
        package_id=None if package is None else package.package_id,
        publication_id=(
            None if version.publication is None else version.publication.publication_id
        ),
        has_release_notes=version.release_notes is not None,
        section_refs=version.section_refs,
        asset_kinds=kinds,
    )


def publication_snapshot(publication: Publication) -> PublicationSnapshot:
    """Project a Publication into an immutable snapshot."""
    history = publication.history
    events = tuple(e.event.value for e in (history.entries if history else ()))
    latest = history.latest() if history else None
    return PublicationSnapshot(
        publication_id=publication.publication_id,
        version_id=publication.version_id,
        state=publication.state.value,
        is_published=publication.is_published,
        is_archived=publication.is_archived,
        is_terminal=publication.is_terminal,
        published_at=publication.published_at,
        archived_at=publication.archived_at,
        history_count=history.entry_count if history else 0,
        latest_event=None if latest is None else latest.event.value,
        history_events=events,
    )


def validation_snapshot(report: ValidationReport) -> ValidationSnapshot:
    """Project a ValidationReport into an immutable snapshot."""
    issues = tuple(
        ValidationIssueSnapshot(
            code=i.code.value,
            message=i.message,
            severity=i.severity.value,
            section_ref=i.section_ref,
            is_blocking=i.is_blocking,
        )
        for i in report.issues
    )
    return ValidationSnapshot(
        report_id=report.report_id,
        version_id=report.version_id,
        passed=report.passed,
        summary=report.summary,
        issue_count=report.issue_count,
        blocking_count=len(report.blocking_issues),
        blocks_publication=report.blocks_publication,
        issues=issues,
    )


def approval_snapshot(approval: Approval) -> ApprovalSnapshot:
    """Project an Approval into an immutable snapshot."""
    return ApprovalSnapshot(
        approval_id=approval.approval_id,
        version_id=approval.version_id,
        reviewer_id=approval.reviewer_id,
        decision=approval.decision.value,
        rationale=approval.rationale,
        decided_at=approval.decided_at,
        is_approved=approval.is_approved,
    )


def release_snapshot(version: SubjectVersion) -> ReleaseSnapshot:
    """Project version release notes into an immutable snapshot."""
    notes = version.release_notes
    return ReleaseSnapshot(
        version_id=version.version_id,
        subject_id=version.subject_id,
        version_label=version.version_label,
        display_name=version.display_name,
        publication_state=version.state.value,
        notes_id=None if notes is None else notes.notes_id,
        headline="" if notes is None else notes.headline,
        entry_count=0 if notes is None else notes.entry_count,
        entries=() if notes is None else notes.texts(),
        is_published=version.publication.is_published if version.publication else False,
        published_at=(
            version.publication.published_at if version.publication else None
        ),
    )
