"""RecommendationSetValidator — structural checks (FOS-006).

Validates unique ids, priority values, template existence, evidence
references, and snapshot version presence.
"""

from __future__ import annotations

from datetime import datetime

from app.founder.recommendations.config import ALL_TEMPLATE_IDS, PRIORITY_ORDER
from app.founder.recommendations.dto.validation import (
    ValidationIssue,
    ValidationReport,
)
from app.founder.recommendations.models import RecommendationSet
from app.founder.recommendations.providers import TemplateProvider


class RecommendationSetValidator:
    """Validate an assembled RecommendationSet for structural integrity."""

    def __init__(
        self,
        *,
        templates: TemplateProvider | None = None,
        allowed_priorities: tuple[str, ...] = PRIORITY_ORDER,
    ) -> None:
        self._templates = templates or TemplateProvider()
        self._allowed_priorities = frozenset(allowed_priorities)

    def validate(self, recommendation_set: RecommendationSet) -> ValidationReport:
        """Return an explicit validation report for ``recommendation_set``.

        Args:
            recommendation_set: Assembled recommendation cargo.

        Returns:
            ValidationReport with ok=False when any hard error is present.
        """
        issues: list[ValidationIssue] = []
        issues.extend(self._check_snapshot_metadata(recommendation_set))
        issues.extend(self._check_unique_ids(recommendation_set))
        issues.extend(self._check_priorities(recommendation_set))
        issues.extend(self._check_templates(recommendation_set))
        issues.extend(self._check_evidence(recommendation_set))
        issues.extend(self._check_overall_status(recommendation_set))
        return ValidationReport(ok=len(issues) == 0, issues=tuple(issues))

    def _check_snapshot_metadata(
        self, recommendation_set: RecommendationSet
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if not str(recommendation_set.snapshot_version or "").strip():
            issues.append(
                ValidationIssue(
                    code="missing_snapshot_version",
                    message="snapshot_version must be a non-empty string",
                    field="snapshot_version",
                )
            )
        if not isinstance(recommendation_set.generated_at, datetime):
            issues.append(
                ValidationIssue(
                    code="missing_generated_at",
                    message="generated_at must be a datetime",
                    field="generated_at",
                )
            )
        return issues

    def _check_unique_ids(
        self, recommendation_set: RecommendationSet
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        seen: dict[str, int] = {}
        for index, recommendation in enumerate(recommendation_set.recommendations):
            rid = recommendation.id
            if not str(rid or "").strip():
                issues.append(
                    ValidationIssue(
                        code="empty_recommendation_id",
                        message=f"Recommendation at index {index} has empty id",
                        field=f"recommendations[{index}].id",
                    )
                )
                continue
            if rid in seen:
                issues.append(
                    ValidationIssue(
                        code="duplicate_recommendation_id",
                        message=(
                            f"Recommendation id {rid!r} is duplicated "
                            f"(indices {seen[rid]} and {index})"
                        ),
                        field="recommendations",
                    )
                )
            else:
                seen[rid] = index
        return issues

    def _check_priorities(
        self, recommendation_set: RecommendationSet
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for index, recommendation in enumerate(recommendation_set.recommendations):
            if recommendation.priority not in self._allowed_priorities:
                issues.append(
                    ValidationIssue(
                        code="invalid_priority",
                        message=(
                            f"priority {recommendation.priority!r} is not in "
                            f"{sorted(self._allowed_priorities)}"
                        ),
                        field=f"recommendations[{index}].priority",
                    )
                )
        return issues

    def _check_templates(
        self, recommendation_set: RecommendationSet
    ) -> list[ValidationIssue]:
        """Recommendation ids are template ids in Version 1."""
        issues: list[ValidationIssue] = []
        known = self._templates.known_ids() or ALL_TEMPLATE_IDS
        for index, recommendation in enumerate(recommendation_set.recommendations):
            if recommendation.id and recommendation.id not in known:
                issues.append(
                    ValidationIssue(
                        code="unknown_template",
                        message=(
                            f"Recommendation id {recommendation.id!r} does not "
                            "match a registered template"
                        ),
                        field=f"recommendations[{index}].id",
                    )
                )
            if not str(recommendation.title or "").strip():
                issues.append(
                    ValidationIssue(
                        code="empty_title",
                        message=f"Recommendation {recommendation.id!r} has empty title",
                        field=f"recommendations[{index}].title",
                    )
                )
            if not str(recommendation.explanation or "").strip():
                issues.append(
                    ValidationIssue(
                        code="empty_explanation",
                        message=(
                            f"Recommendation {recommendation.id!r} has "
                            "empty explanation"
                        ),
                        field=f"recommendations[{index}].explanation",
                    )
                )
            if not str(recommendation.rationale or "").strip():
                issues.append(
                    ValidationIssue(
                        code="empty_rationale",
                        message=(
                            f"Recommendation {recommendation.id!r} has empty rationale"
                        ),
                        field=f"recommendations[{index}].rationale",
                    )
                )
        return issues

    def _check_evidence(
        self, recommendation_set: RecommendationSet
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for index, recommendation in enumerate(recommendation_set.recommendations):
            if not recommendation.evidence:
                issues.append(
                    ValidationIssue(
                        code="missing_evidence",
                        message=(
                            f"Recommendation {recommendation.id!r} has no evidence"
                        ),
                        field=f"recommendations[{index}].evidence",
                    )
                )
                continue
            for e_index, evidence in enumerate(recommendation.evidence):
                field_prefix = (
                    f"recommendations[{index}].evidence[{e_index}]"
                )
                if not str(evidence.source or "").strip():
                    issues.append(
                        ValidationIssue(
                            code="invalid_evidence_source",
                            message="Evidence source must be non-empty",
                            field=f"{field_prefix}.source",
                        )
                    )
                if not str(evidence.metric or "").strip():
                    issues.append(
                        ValidationIssue(
                            code="invalid_evidence_metric",
                            message="Evidence metric must be non-empty",
                            field=f"{field_prefix}.metric",
                        )
                    )
                if evidence.value is None:
                    issues.append(
                        ValidationIssue(
                            code="invalid_evidence_value",
                            message="Evidence value must not be None",
                            field=f"{field_prefix}.value",
                        )
                    )
        return issues

    def _check_overall_status(
        self, recommendation_set: RecommendationSet
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if not str(recommendation_set.overall_status or "").strip():
            issues.append(
                ValidationIssue(
                    code="missing_overall_status",
                    message="overall_status must be a non-empty string",
                    field="overall_status",
                )
            )
        return issues
