"""Subject version — a specific educational product release."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.domain.curriculum_management.approval import Approval
from app.domain.curriculum_management.blueprint_assignment import BlueprintAssignment
from app.domain.curriculum_management.curriculum_package import CurriculumPackage
from app.domain.curriculum_management.publication import Publication
from app.domain.curriculum_management.publication_state import PublicationState
from app.domain.curriculum_management.release_notes import ReleaseNotes
from app.domain.curriculum_management.validation_report import ValidationReport

_VERSION_LABEL_RE = re.compile(r"^\d{4}\.\d+$")


@dataclass(frozen=True)
class SubjectVersion:
    """Specific release of a curriculum subject product.

    Examples: CS1 2026.1, CS1 2027.1.

    Owns: package, blueprint assignments, validation reports,
    publication status, and release notes.
    """

    version_id: str
    subject_id: str
    version_label: str
    package: CurriculumPackage | None = None
    assignments: tuple[BlueprintAssignment, ...] = field(default_factory=tuple)
    validation_reports: tuple[ValidationReport, ...] = field(default_factory=tuple)
    publication: Publication | None = None
    release_notes: ReleaseNotes | None = None
    approvals: tuple[Approval, ...] = field(default_factory=tuple)
    section_refs: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        version_id: str,
        subject_id: str,
        version_label: str,
        *,
        package: CurriculumPackage | None = None,
        assignments: (
            list[BlueprintAssignment] | tuple[BlueprintAssignment, ...] | None
        ) = None,
        validation_reports: (
            list[ValidationReport] | tuple[ValidationReport, ...] | None
        ) = None,
        publication: Publication | None = None,
        release_notes: ReleaseNotes | None = None,
        approvals: list[Approval] | tuple[Approval, ...] | None = None,
        section_refs: list[str] | tuple[str, ...] | None = None,
    ) -> SubjectVersion:
        """Construct a SubjectVersion after validating invariants."""
        vid = _require_non_empty(version_id, "version_id")
        sid = _require_non_empty(subject_id, "subject_id")
        label = _require_non_empty(version_label, "version_label")
        if not _VERSION_LABEL_RE.match(label):
            raise ValueError(
                "version_label must match YYYY.N (e.g. 2026.1); "
                f"got {version_label!r}"
            )
        if package is not None and package.version_id != vid:
            raise ValueError("package version_id must match subject version")
        pub = publication or Publication.create(f"pub-{vid}", vid)
        if pub.version_id != vid:
            raise ValueError("publication version_id must match subject version")
        notes = release_notes
        if notes is not None and notes.version_id != vid:
            raise ValueError("release_notes version_id must match subject version")
        assign_t = tuple(assignments or ())
        seen_a: set[str] = set()
        for assignment in assign_t:
            if assignment.assignment_id in seen_a:
                raise ValueError(
                    f"duplicate assignment_id: {assignment.assignment_id!r}"
                )
            seen_a.add(assignment.assignment_id)
            if assignment.version_id != vid:
                raise ValueError("assignment version_id must match subject version")
        reports_t = tuple(validation_reports or ())
        for report in reports_t:
            if report.version_id != vid:
                raise ValueError("validation report version_id must match")
        approvals_t = tuple(approvals or ())
        for approval in approvals_t:
            if approval.version_id != vid:
                raise ValueError("approval version_id must match subject version")
        sections = tuple(
            _require_non_empty(s, "section_ref") for s in (section_refs or ())
        )
        if len(sections) != len(set(sections)):
            raise ValueError("duplicate section_ref within version")
        return cls(
            version_id=vid,
            subject_id=sid,
            version_label=label,
            package=package,
            assignments=assign_t,
            validation_reports=reports_t,
            publication=pub,
            release_notes=notes,
            approvals=approvals_t,
            section_refs=sections,
        )

    @property
    def state(self) -> PublicationState:
        """Current publication state."""
        if self.publication is None:
            return PublicationState.DRAFT
        return self.publication.state

    @property
    def display_name(self) -> str:
        """Human-facing version token (subject version_id + label)."""
        return f"{self.subject_id} {self.version_label}"

    @property
    def latest_validation(self) -> ValidationReport | None:
        """Most recent validation report, or None."""
        if not self.validation_reports:
            return None
        return self.validation_reports[-1]

    @property
    def latest_approval(self) -> Approval | None:
        """Most recent approval record, or None."""
        if not self.approvals:
            return None
        return self.approvals[-1]

    def with_package(self, package: CurriculumPackage) -> SubjectVersion:
        """Return a copy with replacement package."""
        return SubjectVersion.create(
            self.version_id,
            self.subject_id,
            self.version_label,
            package=package,
            assignments=self.assignments,
            validation_reports=self.validation_reports,
            publication=self.publication,
            release_notes=self.release_notes,
            approvals=self.approvals,
            section_refs=self.section_refs,
        )

    def with_publication(self, publication: Publication) -> SubjectVersion:
        """Return a copy with replacement publication."""
        return SubjectVersion.create(
            self.version_id,
            self.subject_id,
            self.version_label,
            package=self.package,
            assignments=self.assignments,
            validation_reports=self.validation_reports,
            publication=publication,
            release_notes=self.release_notes,
            approvals=self.approvals,
            section_refs=self.section_refs,
        )

    def with_assignment(self, assignment: BlueprintAssignment) -> SubjectVersion:
        """Return a copy with an appended blueprint assignment."""
        return SubjectVersion.create(
            self.version_id,
            self.subject_id,
            self.version_label,
            package=self.package,
            assignments=(*self.assignments, assignment),
            validation_reports=self.validation_reports,
            publication=self.publication,
            release_notes=self.release_notes,
            approvals=self.approvals,
            section_refs=self.section_refs,
        )

    def with_validation_report(self, report: ValidationReport) -> SubjectVersion:
        """Return a copy with an appended immutable validation report."""
        return SubjectVersion.create(
            self.version_id,
            self.subject_id,
            self.version_label,
            package=self.package,
            assignments=self.assignments,
            validation_reports=(*self.validation_reports, report),
            publication=self.publication,
            release_notes=self.release_notes,
            approvals=self.approvals,
            section_refs=self.section_refs,
        )

    def with_approval(self, approval: Approval) -> SubjectVersion:
        """Return a copy with an appended approval record."""
        return SubjectVersion.create(
            self.version_id,
            self.subject_id,
            self.version_label,
            package=self.package,
            assignments=self.assignments,
            validation_reports=self.validation_reports,
            publication=self.publication,
            release_notes=self.release_notes,
            approvals=(*self.approvals, approval),
            section_refs=self.section_refs,
        )

    def with_release_notes(self, notes: ReleaseNotes) -> SubjectVersion:
        """Return a copy with replacement release notes."""
        return SubjectVersion.create(
            self.version_id,
            self.subject_id,
            self.version_label,
            package=self.package,
            assignments=self.assignments,
            validation_reports=self.validation_reports,
            publication=self.publication,
            release_notes=notes,
            approvals=self.approvals,
            section_refs=self.section_refs,
        )

    def with_section_refs(
        self,
        section_refs: list[str] | tuple[str, ...],
    ) -> SubjectVersion:
        """Return a copy with replacement section references."""
        return SubjectVersion.create(
            self.version_id,
            self.subject_id,
            self.version_label,
            package=self.package,
            assignments=self.assignments,
            validation_reports=self.validation_reports,
            publication=self.publication,
            release_notes=self.release_notes,
            approvals=self.approvals,
            section_refs=section_refs,
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
