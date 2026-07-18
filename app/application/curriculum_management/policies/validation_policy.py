"""Stateless validation policy for curriculum packages and assignments."""

from __future__ import annotations

from app.domain.curriculum_management.curriculum_asset import AssetKind
from app.domain.curriculum_management.subject_version import SubjectVersion
from app.domain.curriculum_management.validation_report import (
    ValidationIssue,
    ValidationIssueCode,
    ValidationSeverity,
)


class ValidationPolicy:
    """Deterministic readiness checks (stateless). No PDF parsing."""

    @staticmethod
    def collect_issues(version: SubjectVersion) -> tuple[ValidationIssue, ...]:
        """Inspect version structural readiness; return immutable findings."""
        issues: list[ValidationIssue] = []
        package = version.package
        if package is None or package.asset_count == 0:
            issues.append(
                ValidationIssue.create(
                    ValidationIssueCode.EMPTY_PACKAGE,
                    "Curriculum package is empty",
                    severity=ValidationSeverity.BLOCKING,
                )
            )
        else:
            if not package.has_kind(AssetKind.SYLLABUS):
                issues.append(
                    ValidationIssue.create(
                        ValidationIssueCode.MISSING_SYLLABUS,
                        "Missing syllabus asset reference",
                        severity=ValidationSeverity.BLOCKING,
                    )
                )
            if not package.has_kind(AssetKind.CMP):
                issues.append(
                    ValidationIssue.create(
                        ValidationIssueCode.MISSING_CMP,
                        "Missing CMP asset reference",
                        severity=ValidationSeverity.WARNING,
                    )
                )
            if not package.has_kind(AssetKind.LEARNING_OBJECTIVES):
                issues.append(
                    ValidationIssue.create(
                        ValidationIssueCode.MISSING_LEARNING_OBJECTIVES,
                        "Missing learning objectives asset reference",
                        severity=ValidationSeverity.WARNING,
                    )
                )

        if not version.assignments:
            issues.append(
                ValidationIssue.create(
                    ValidationIssueCode.MISSING_BLUEPRINT_ASSIGNMENT,
                    "No blueprint assignments recorded",
                    severity=ValidationSeverity.ERROR,
                )
            )
        else:
            seen_sections: set[str] = set()
            for assignment in version.assignments:
                if assignment.section_ref in seen_sections:
                    issues.append(
                        ValidationIssue.create(
                            ValidationIssueCode.DUPLICATE_SECTION,
                            f"Duplicate blueprint assignment for "
                            f"{assignment.section_ref}",
                            severity=ValidationSeverity.ERROR,
                            section_ref=assignment.section_ref,
                        )
                    )
                seen_sections.add(assignment.section_ref)

        # Declared section_refs without assignment → missing assignment signal
        assigned = {a.section_ref for a in version.assignments}
        for section in version.section_refs:
            if section not in assigned:
                issues.append(
                    ValidationIssue.create(
                        ValidationIssueCode.MISSING_BLUEPRINT_ASSIGNMENT,
                        f"Section {section} has no blueprint assignment",
                        severity=ValidationSeverity.ERROR,
                        section_ref=section,
                    )
                )

        # Duplicate topic-like tokens in section_refs
        seen_topics: set[str] = set()
        for section in version.section_refs:
            token = section.lower()
            if token in seen_topics:
                issues.append(
                    ValidationIssue.create(
                        ValidationIssueCode.DUPLICATE_TOPIC,
                        f"Duplicate topic/section ref: {section}",
                        severity=ValidationSeverity.ERROR,
                        section_ref=section,
                    )
                )
            seen_topics.add(token)

        return tuple(issues)

    @staticmethod
    def is_ready_for_validation_gate(version: SubjectVersion) -> bool:
        """True when collected issues contain no blocking/error findings."""
        issues = ValidationPolicy.collect_issues(version)
        return not any(i.is_blocking for i in issues)
