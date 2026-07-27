"""Rule registry — pluggable execution of educational reasoning rules."""

from __future__ import annotations

from app.domain.educational_reasoning.confidence_update import ConfidenceAdjustmentRule
from app.domain.educational_reasoning.consistency_rule import ConsistencyRule
from app.domain.educational_reasoning.gap_analysis import (
    KnowledgeGapDetectionRule,
    PrerequisiteAnalysisRule,
)
from app.domain.educational_reasoning.mastery_update import MasteryUpdateRule
from app.domain.educational_reasoning.momentum_rule import LearningMomentumRule
from app.domain.educational_reasoning.readiness_rule import ReadinessContributionRule
from app.domain.educational_reasoning.reasoning_context import ReasoningContext
from app.domain.educational_reasoning.reasoning_rule import ReasoningRule, RuleExecution
from app.domain.educational_reasoning.recommendation_rule import RecommendationRule


class RuleRegistry:
    """Ordered registry of educational reasoning rules.

    New rules are pluggable without modifying existing rule implementations.
    StudentReasoningService delegates educational logic to this registry.
    """

    def __init__(self, rules: list[ReasoningRule] | None = None) -> None:
        self._rules: list[ReasoningRule] = list(rules or [])
        self._by_code: dict[str, ReasoningRule] = {
            r.code: r for r in self._rules if r.code
        }

    def register(self, rule: ReasoningRule, *, after: str | None = None) -> None:
        """Register a rule. Optionally insert after an existing rule code."""
        if not rule.code:
            raise ValueError("rule.code is required")
        if rule.code in self._by_code:
            raise ValueError(f"rule {rule.code!r} is already registered")
        if after is None:
            self._rules.append(rule)
        else:
            idx = next(
                (i for i, r in enumerate(self._rules) if r.code == after), None
            )
            if idx is None:
                raise ValueError(f"anchor rule {after!r} not found")
            self._rules.insert(idx + 1, rule)
        self._by_code[rule.code] = rule

    def get(self, code: str) -> ReasoningRule | None:
        return self._by_code.get(code)

    def list_rules(self) -> tuple[dict[str, str], ...]:
        return tuple(
            {
                "code": r.code,
                "name": r.name,
                "description": r.description,
            }
            for r in self._rules
        )

    @property
    def rules(self) -> tuple[ReasoningRule, ...]:
        return tuple(self._rules)

    def execute(
        self, context: ReasoningContext
    ) -> tuple[RuleExecution, ReasoningContext]:
        """Run all registered rules in order, merging outputs into context.

        Returns the list of executions and the final accumulated context.
        """
        executions: list[RuleExecution] = []
        current = context
        for rule in self._rules:
            execution = rule.apply(current)
            executions.append(execution)
            current = _merge(current, execution)
        return tuple(executions), current


def _merge(context: ReasoningContext, execution: RuleExecution) -> ReasoningContext:
    updates: dict = {}
    if execution.mastery is not None:
        updates["mastery"] = execution.mastery
    if execution.confidence is not None:
        updates["confidence"] = execution.confidence
    if execution.knowledge is not None:
        updates["knowledge"] = execution.knowledge
    if execution.retention is not None:
        updates["retention"] = execution.retention
    if execution.consistency is not None:
        updates["consistency"] = execution.consistency
    if execution.momentum is not None:
        updates["momentum"] = execution.momentum
    if execution.exam_readiness is not None:
        updates["exam_readiness"] = execution.exam_readiness
    if execution.gaps is not None:
        updates["gaps"] = execution.gaps
    if execution.recommendations is not None:
        updates["recommendations"] = execution.recommendations
    if not updates:
        return context
    return context.with_updates(**updates)


def build_default_registry() -> RuleRegistry:
    """Default educational rule set for SDT-002.

    Order encodes educational dependencies:
    mastery → confidence / momentum / consistency → readiness →
    gaps → prerequisites → recommendations.
    """
    registry = RuleRegistry(
        [
            MasteryUpdateRule(),
            ConfidenceAdjustmentRule(),
            LearningMomentumRule(),
            ConsistencyRule(),
            ReadinessContributionRule(),
            KnowledgeGapDetectionRule(),
            PrerequisiteAnalysisRule(),
            RecommendationRule(),
        ]
    )
    return registry
