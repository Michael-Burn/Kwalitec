"""FounderWeeklyBriefValidator — structural checks (FOS-007).

Validates required sections, section ordering, metadata completeness,
recommendation references, snapshot version, and report version.
"""

from __future__ import annotations

from datetime import datetime

from app.founder.briefing.config import (
    REPORT_VERSION,
    REQUIRED_SECTION_TITLES,
    SECTION_SPECS,
)
from app.founder.briefing.dto.validation import ValidationIssue, ValidationReport
from app.founder.briefing.models import BriefMetadata, BriefSection, FounderWeeklyBrief
from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.models import RecommendationSet


class FounderWeeklyBriefValidator:
    """Validate an assembled FounderWeeklyBrief for structural integrity."""

    def __init__(
        self,
        *,
        expected_report_version: str = REPORT_VERSION,
        required_titles: tuple[str, ...] = REQUIRED_SECTION_TITLES,
        section_specs: tuple[tuple[int, str], ...] = SECTION_SPECS,
    ) -> None:
        self._expected_report_version = expected_report_version
        self._required_titles = required_titles
        self._section_specs = section_specs

    def validate(
        self,
        brief: FounderWeeklyBrief,
        *,
        state: FounderOperationalState | None = None,
        recommendation_set: RecommendationSet | None = None,
    ) -> ValidationReport:
        """Return an explicit validation report for ``brief``.

        Args:
            brief: Assembled weekly briefing.
            state: Optional source state for cross-checks.
            recommendation_set: Optional source recommendations for cross-checks.

        Returns:
            ValidationReport with ok=False when any hard error is present.
        """
        issues: list[ValidationIssue] = []
        issues.extend(self._check_metadata(brief))
        issues.extend(self._check_required_sections(brief))
        issues.extend(self._check_section_ordering(brief))
        issues.extend(self._check_snapshot_version(brief, state))
        issues.extend(self._check_report_version(brief))
        issues.extend(self._check_recommendation_references(brief, recommendation_set))
        return ValidationReport(ok=len(issues) == 0, issues=tuple(issues))

    def _check_metadata(self, brief: FounderWeeklyBrief) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if not str(brief.week or "").strip():
            issues.append(
                ValidationIssue(
                    code="missing_week",
                    message="week must be a non-empty string",
                    field="week",
                )
            )
        if not isinstance(brief.generated_at, datetime):
            issues.append(
                ValidationIssue(
                    code="missing_generated_at",
                    message="generated_at must be a datetime",
                    field="generated_at",
                )
            )
        if not str(brief.snapshot_version or "").strip():
            issues.append(
                ValidationIssue(
                    code="missing_snapshot_version",
                    message="snapshot_version must be a non-empty string",
                    field="snapshot_version",
                )
            )
        if not str(brief.recommendation_version or "").strip():
            issues.append(
                ValidationIssue(
                    code="missing_recommendation_version",
                    message="recommendation_version must be a non-empty string",
                    field="recommendation_version",
                )
            )
        if not isinstance(brief.metadata, BriefMetadata):
            issues.append(
                ValidationIssue(
                    code="missing_metadata",
                    message="metadata must be a BriefMetadata instance",
                    field="metadata",
                )
            )
            return issues

        meta = brief.metadata
        if not isinstance(meta.generated_at, datetime):
            issues.append(
                ValidationIssue(
                    code="missing_metadata_generated_at",
                    message="metadata.generated_at must be a datetime",
                    field="metadata.generated_at",
                )
            )
        if not str(meta.snapshot_version or "").strip():
            issues.append(
                ValidationIssue(
                    code="missing_metadata_snapshot_version",
                    message="metadata.snapshot_version must be a non-empty string",
                    field="metadata.snapshot_version",
                )
            )
        if not str(meta.report_version or "").strip():
            issues.append(
                ValidationIssue(
                    code="missing_metadata_report_version",
                    message="metadata.report_version must be a non-empty string",
                    field="metadata.report_version",
                )
            )
        if (
            isinstance(brief.generated_at, datetime)
            and isinstance(meta.generated_at, datetime)
            and brief.generated_at != meta.generated_at
        ):
            issues.append(
                ValidationIssue(
                    code="metadata_generated_at_mismatch",
                    message="metadata.generated_at must match brief.generated_at",
                    field="metadata.generated_at",
                )
            )
        if (
            brief.snapshot_version
            and meta.snapshot_version
            and brief.snapshot_version != meta.snapshot_version
        ):
            issues.append(
                ValidationIssue(
                    code="metadata_snapshot_version_mismatch",
                    message=(
                        "metadata.snapshot_version must match brief.snapshot_version"
                    ),
                    field="metadata.snapshot_version",
                )
            )
        return issues

    def _check_required_sections(
        self, brief: FounderWeeklyBrief
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        sections = brief.ordered_sections()
        present_titles = {section.title for section in sections}
        for title in self._required_titles:
            if title not in present_titles:
                issues.append(
                    ValidationIssue(
                        code="missing_section",
                        message=f"Required section {title!r} is missing",
                        field="sections",
                    )
                )
        for index, section in enumerate(sections):
            if not isinstance(section, BriefSection):
                issues.append(
                    ValidationIssue(
                        code="invalid_section_type",
                        message=f"Section at index {index} is not a BriefSection",
                        field=f"sections[{index}]",
                    )
                )
                continue
            if not str(section.title or "").strip():
                issues.append(
                    ValidationIssue(
                        code="empty_section_title",
                        message=f"Section at index {index} has empty title",
                        field=f"sections[{index}].title",
                    )
                )
            if not str(section.content or "").strip():
                issues.append(
                    ValidationIssue(
                        code="empty_section_content",
                        message=f"Section {section.title!r} has empty content",
                        field=f"sections[{index}].content",
                    )
                )
        return issues

    def _check_section_ordering(
        self, brief: FounderWeeklyBrief
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        sections = brief.ordered_sections()
        expected_orders = [order for order, _ in self._section_specs]
        actual_orders = [section.order for section in sections]
        if actual_orders != sorted(actual_orders):
            issues.append(
                ValidationIssue(
                    code="section_order_unsorted",
                    message="ordered_sections() must return ascending order values",
                    field="sections",
                )
            )
        if actual_orders != expected_orders:
            issues.append(
                ValidationIssue(
                    code="section_order_mismatch",
                    message=(
                        f"section orders {actual_orders} do not match "
                        f"expected {list(expected_orders)}"
                    ),
                    field="sections",
                )
            )
        for (expected_order, expected_title), section in zip(
            self._section_specs, sections, strict=False
        ):
            if section.order == expected_order and section.title != expected_title:
                issues.append(
                    ValidationIssue(
                        code="section_title_mismatch",
                        message=(
                            f"section order {expected_order} has title "
                            f"{section.title!r}, expected {expected_title!r}"
                        ),
                        field=f"sections[{expected_order - 1}].title",
                    )
                )
        seen_orders: dict[int, str] = {}
        for section in sections:
            if section.order in seen_orders:
                issues.append(
                    ValidationIssue(
                        code="duplicate_section_order",
                        message=(
                            f"order {section.order} duplicated by "
                            f"{seen_orders[section.order]!r} and {section.title!r}"
                        ),
                        field="sections",
                    )
                )
            else:
                seen_orders[section.order] = section.title
        return issues

    def _check_snapshot_version(
        self,
        brief: FounderWeeklyBrief,
        state: FounderOperationalState | None,
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if state is not None and brief.snapshot_version != state.snapshot_version:
            issues.append(
                ValidationIssue(
                    code="snapshot_version_mismatch",
                    message=(
                        f"brief snapshot_version {brief.snapshot_version!r} does not "
                        f"match state snapshot_version {state.snapshot_version!r}"
                    ),
                    field="snapshot_version",
                )
            )
        if state is not None and brief.week != state.internal_alpha.current_week:
            issues.append(
                ValidationIssue(
                    code="week_mismatch",
                    message=(
                        f"brief week {brief.week!r} does not match "
                        f"state internal_alpha.current_week "
                        f"{state.internal_alpha.current_week!r}"
                    ),
                    field="week",
                )
            )
        return issues

    def _check_report_version(
        self, brief: FounderWeeklyBrief
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if brief.metadata.report_version != self._expected_report_version:
            issues.append(
                ValidationIssue(
                    code="report_version_mismatch",
                    message=(
                        f"report_version {brief.metadata.report_version!r} does not "
                        f"match expected {self._expected_report_version!r}"
                    ),
                    field="metadata.report_version",
                )
            )
        return issues

    def _check_recommendation_references(
        self,
        brief: FounderWeeklyBrief,
        recommendation_set: RecommendationSet | None,
    ) -> list[ValidationIssue]:
        """Ensure the Recommendations section cites every recommendation id."""
        if recommendation_set is None:
            return []

        issues: list[ValidationIssue] = []
        for item in recommendation_set.recommendations:
            if item.id not in brief.recommendations.content:
                issues.append(
                    ValidationIssue(
                        code="missing_recommendation_reference",
                        message=(
                            f"Recommendation id {item.id!r} is not referenced "
                            "in the Recommendations section"
                        ),
                        field="recommendations.content",
                    )
                )
        return issues
