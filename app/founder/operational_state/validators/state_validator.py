"""OperationalStateValidator — completeness checks for FOS-005 snapshots.

Validates required sections, duplicate-free source versions, snapshot
completeness, and version consistency. Failures are explicit codes.
No scoring or recommendations.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime

from app.founder.operational_state.dto.validation import (
    ValidationIssue,
    ValidationReport,
)
from app.founder.operational_state.models.state import (
    SNAPSHOT_VERSION,
    CapabilityState,
    EngineeringState,
    FounderOperationalState,
    InternalAlphaState,
    KnowledgeState,
    ReleaseState,
    SourceVersions,
)

_REQUIRED_SOURCE_KEYS: tuple[str, ...] = (
    "knowledge",
    "capability_archive",
    "internal_alpha",
)


class OperationalStateValidator:
    """Validate an assembled FounderOperationalState for completeness."""

    def __init__(self, *, expected_snapshot_version: str = SNAPSHOT_VERSION) -> None:
        self._expected_snapshot_version = expected_snapshot_version

    def validate(self, state: FounderOperationalState) -> ValidationReport:
        """Return an explicit validation report for ``state``.

        Args:
            state: Assembled operational snapshot.

        Returns:
            ValidationReport with ok=False when any hard error is present.
        """
        issues: list[ValidationIssue] = []
        issues.extend(self._check_required_sections(state))
        issues.extend(self._check_snapshot_metadata(state))
        issues.extend(self._check_source_versions(state.source_versions))
        issues.extend(self._check_version_consistency(state))
        issues.extend(self._check_non_negative_counts(state))
        issues.extend(self._check_cross_section_consistency(state))
        return ValidationReport(ok=len(issues) == 0, issues=tuple(issues))

    def _check_required_sections(
        self, state: FounderOperationalState
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        checks: tuple[tuple[str, object, type], ...] = (
            ("engineering", state.engineering, EngineeringState),
            ("knowledge", state.knowledge, KnowledgeState),
            ("capability", state.capability, CapabilityState),
            ("internal_alpha", state.internal_alpha, InternalAlphaState),
            ("release", state.release, ReleaseState),
            ("source_versions", state.source_versions, SourceVersions),
        )
        for field, value, expected in checks:
            if value is None:
                issues.append(
                    ValidationIssue(
                        code="missing_section",
                        message=f"Required section {field!r} is missing",
                        field=field,
                    )
                )
            elif not isinstance(value, expected):
                issues.append(
                    ValidationIssue(
                        code="invalid_section_type",
                        message=(
                            f"Section {field!r} must be {expected.__name__}, "
                            f"got {type(value).__name__}"
                        ),
                        field=field,
                    )
                )
        return issues

    def _check_snapshot_metadata(
        self, state: FounderOperationalState
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if not isinstance(state.generated_at, datetime):
            issues.append(
                ValidationIssue(
                    code="missing_generated_at",
                    message="generated_at must be a datetime",
                    field="generated_at",
                )
            )
        if not str(state.snapshot_version or "").strip():
            issues.append(
                ValidationIssue(
                    code="missing_snapshot_version",
                    message="snapshot_version must be a non-empty string",
                    field="snapshot_version",
                )
            )
        return issues

    def _check_source_versions(
        self, versions: SourceVersions
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        mapping = versions.as_mapping()
        seen_values: dict[str, str] = {}

        for key in _REQUIRED_SOURCE_KEYS:
            if key not in mapping:
                issues.append(
                    ValidationIssue(
                        code="missing_source_version",
                        message=f"Missing source version for {key!r}",
                        field=f"source_versions.{key}",
                    )
                )
                continue
            value = str(mapping[key] or "").strip()
            if not value:
                issues.append(
                    ValidationIssue(
                        code="empty_source_version",
                        message=f"Source version for {key!r} must be non-empty",
                        field=f"source_versions.{key}",
                    )
                )
                continue
            # Detect identical version tokens reused across distinct
            # subsystems when they are not intentionally "unwired".
            if value != "unwired" and value in seen_values:
                issues.append(
                    ValidationIssue(
                        code="duplicate_subsystem_data",
                        message=(
                            f"Source version {value!r} appears on both "
                            f"{seen_values[value]!r} and {key!r}"
                        ),
                        field="source_versions",
                    )
                )
            else:
                seen_values[value] = key

        extra = set(mapping) - set(_REQUIRED_SOURCE_KEYS)
        for key in sorted(extra):
            issues.append(
                ValidationIssue(
                    code="unexpected_source_version",
                    message=f"Unexpected source version key {key!r}",
                    field=f"source_versions.{key}",
                )
            )
        return issues

    def _check_version_consistency(
        self, state: FounderOperationalState
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if (
            state.snapshot_version
            and state.snapshot_version != self._expected_snapshot_version
        ):
            issues.append(
                ValidationIssue(
                    code="snapshot_version_mismatch",
                    message=(
                        f"snapshot_version {state.snapshot_version!r} does not "
                        f"match expected {self._expected_snapshot_version!r}"
                    ),
                    field="snapshot_version",
                )
            )
        return issues

    def _check_non_negative_counts(
        self, state: FounderOperationalState
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        numeric_fields: tuple[tuple[str, int], ...] = (
            ("engineering.standards_count", state.engineering.standards_count),
            ("engineering.validation_errors", state.engineering.validation_errors),
            (
                "knowledge.engineering_standards",
                state.knowledge.engineering_standards,
            ),
            (
                "knowledge.architecture_documents",
                state.knowledge.architecture_documents,
            ),
            ("knowledge.research_documents", state.knowledge.research_documents),
            (
                "knowledge.capability_documents",
                state.knowledge.capability_documents,
            ),
            ("knowledge.indexed_artefacts", state.knowledge.indexed_artefacts),
            ("capability.total_count", state.capability.total_count),
            ("capability.completed_count", state.capability.completed_count),
            ("capability.active_count", state.capability.active_count),
            (
                "capability.archive_inconsistencies",
                state.capability.archive_inconsistencies,
            ),
            ("internal_alpha.feedback_count", state.internal_alpha.feedback_count),
            (
                "internal_alpha.duplicate_count",
                state.internal_alpha.duplicate_count,
            ),
            ("release.completed_capabilities", state.release.completed_capabilities),
        )
        for field, value in numeric_fields:
            if value < 0:
                issues.append(
                    ValidationIssue(
                        code="negative_count",
                        message=f"{field} must be >= 0 (got {value})",
                        field=field,
                    )
                )

        if not isinstance(state.internal_alpha.category_counts, Mapping):
            issues.append(
                ValidationIssue(
                    code="invalid_category_counts",
                    message="internal_alpha.category_counts must be a mapping",
                    field="internal_alpha.category_counts",
                )
            )
        else:
            for category, count in state.internal_alpha.category_counts.items():
                if count < 0:
                    issues.append(
                        ValidationIssue(
                            code="negative_count",
                            message=(
                                f"category_counts[{category!r}] must be >= 0 "
                                f"(got {count})"
                            ),
                            field="internal_alpha.category_counts",
                        )
                    )
        return issues

    def _check_cross_section_consistency(
        self, state: FounderOperationalState
    ) -> list[ValidationIssue]:
        """Ensure sections derived from the same subsystem stay consistent."""
        issues: list[ValidationIssue] = []
        if (
            state.engineering.standards_count
            != state.knowledge.engineering_standards
        ):
            issues.append(
                ValidationIssue(
                    code="inconsistent_engineering_standards",
                    message=(
                        "engineering.standards_count must equal "
                        "knowledge.engineering_standards"
                    ),
                    field="engineering.standards_count",
                )
            )
        if (
            state.release.completed_capabilities
            != state.capability.completed_count
        ):
            issues.append(
                ValidationIssue(
                    code="inconsistent_completed_capabilities",
                    message=(
                        "release.completed_capabilities must equal "
                        "capability.completed_count"
                    ),
                    field="release.completed_capabilities",
                )
            )
        if not str(state.release.current_release or "").strip():
            issues.append(
                ValidationIssue(
                    code="missing_current_release",
                    message="release.current_release must be non-empty",
                    field="release.current_release",
                )
            )
        return issues
