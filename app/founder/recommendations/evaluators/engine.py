"""RecommendationEngine — run rules, render templates, sort (FOS-006)."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from datetime import UTC, datetime

from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.config import (
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_RANK,
    STATUS_ADVISORY,
    STATUS_ATTENTION,
    STATUS_CRITICAL,
    STATUS_HEALTHY,
)
from app.founder.recommendations.dto import RuleOutcome
from app.founder.recommendations.models import Recommendation, RecommendationSet
from app.founder.recommendations.providers import TemplateProvider
from app.founder.recommendations.rules import RecommendationRule, default_rules


class RecommendationEngine:
    """Execute registered rules and assemble a sorted RecommendationSet."""

    def __init__(
        self,
        *,
        rules: Sequence[RecommendationRule] | None = None,
        templates: TemplateProvider | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._rules: tuple[RecommendationRule, ...] = tuple(
            rules if rules is not None else default_rules()
        )
        self._templates = templates or TemplateProvider()
        self._clock = clock or (lambda: datetime.now(UTC))

    @property
    def rules(self) -> tuple[RecommendationRule, ...]:
        return self._rules

    def evaluate(self, state: FounderOperationalState) -> RecommendationSet:
        """Run every rule, render templates, sort by priority, return set.

        Args:
            state: Immutable FounderOperationalState snapshot (sole input).

        Returns:
            Immutable RecommendationSet sorted Critical → Low.

        Raises:
            UnknownTemplateError: When a rule emits an unregistered template.
        """
        generated_at = self._clock()
        outcomes: list[RuleOutcome] = []
        for rule in self._rules:
            outcome = rule.evaluate(state)
            if outcome is not None:
                outcomes.append(outcome)

        recommendations = tuple(
            self._render(outcome, created_at=generated_at)
            for outcome in self._sort_outcomes(outcomes)
        )
        return RecommendationSet(
            snapshot_version=state.snapshot_version,
            generated_at=generated_at,
            recommendations=recommendations,
            overall_status=self._overall_status(recommendations),
        )

    def _render(
        self, outcome: RuleOutcome, *, created_at: datetime
    ) -> Recommendation:
        template = self._templates.get(outcome.template_id)
        return Recommendation(
            id=outcome.template_id,
            category=outcome.category,
            priority=outcome.priority,
            title=template.title,
            explanation=template.explanation,
            rationale=template.rationale,
            evidence=outcome.evidence,
            created_at=created_at,
        )

    @staticmethod
    def _sort_outcomes(outcomes: list[RuleOutcome]) -> list[RuleOutcome]:
        return sorted(
            outcomes,
            key=lambda o: (
                PRIORITY_RANK.get(o.priority, 99),
                o.template_id,
            ),
        )

    @staticmethod
    def _overall_status(recommendations: tuple[Recommendation, ...]) -> str:
        if not recommendations:
            return STATUS_HEALTHY
        priorities = {r.priority for r in recommendations}
        if PRIORITY_CRITICAL in priorities:
            return STATUS_CRITICAL
        if PRIORITY_HIGH in priorities:
            return STATUS_ATTENTION
        return STATUS_ADVISORY
