"""Stateless compilation rules for Instructional Blueprints.

Applies structural bookends, activity constraints, and effort estimation.
Never generates questions, explanations, or syllabus prose.
"""

from __future__ import annotations

from app.domain.instructional_blueprint.blueprint import InstructionalBlueprint
from app.domain.instructional_blueprint.blueprint_rule import (
    BlueprintRule,
    BlueprintRuleKind,
)
from app.domain.instructional_blueprint.blueprint_step import BlueprintStep
from app.domain.instructional_blueprint.effort_band import (
    EffortBand,
    effort_rank,
    effort_units_for,
)

PRACTICE_KINDS = frozenset(
    {
        "guided_practice",
        "independent_practice",
        "worked_example",
        "knowledge_check",
        "spaced_recall",
        "review",
    }
)

THEORY_KINDS = frozenset(
    {
        "introduction",
        "concept_learning",
        "summary",
        "reflection",
        "next_intention",
    }
)

_INTRODUCTION = "introduction"
_SUMMARY = "summary"
_REFLECTION = "reflection"


class CompilationPolicy:
    """Instructional blueprint compilation rules (stateless, deterministic)."""

    @staticmethod
    def practice_kinds() -> frozenset[str]:
        return PRACTICE_KINDS

    @staticmethod
    def theory_kinds() -> frozenset[str]:
        return THEORY_KINDS

    @staticmethod
    def is_practice(activity_kind: str) -> bool:
        return (activity_kind or "").strip().lower() in PRACTICE_KINDS

    @staticmethod
    def is_theory(activity_kind: str) -> bool:
        return (activity_kind or "").strip().lower() in THEORY_KINDS

    @staticmethod
    def practice_ratio(steps: list[BlueprintStep] | tuple[BlueprintStep, ...]) -> float:
        items = tuple(steps or ())
        if not items:
            return 0.0
        practice = sum(
            1
            for step in items
            if CompilationPolicy.is_practice(step.activity_kind)
        )
        return practice / len(items)

    @staticmethod
    def theory_ratio(steps: list[BlueprintStep] | tuple[BlueprintStep, ...]) -> float:
        items = tuple(steps or ())
        if not items:
            return 0.0
        theory = sum(
            1 for step in items if CompilationPolicy.is_theory(step.activity_kind)
        )
        return theory / len(items)

    @staticmethod
    def apply_bookends(
        steps: list[BlueprintStep] | tuple[BlueprintStep, ...],
        rules: list[BlueprintRule] | tuple[BlueprintRule, ...] | None = None,
    ) -> tuple[BlueprintStep, ...]:
        """Optionally prepend/append structural bookend steps from rules."""
        items = list(steps or ())
        rule_kinds = {rule.kind for rule in (rules or ())}

        if (
            BlueprintRuleKind.BOOKEND_INTRODUCTION in rule_kinds
            and not any(s.activity_kind == _INTRODUCTION for s in items)
        ):
            items.insert(
                0,
                BlueprintStep.create(
                    "bookend-introduction",
                    _INTRODUCTION,
                    sequence_index=0,
                    role="warm_up",
                    effort_weight=1,
                    required=True,
                    metadata=("bookend",),
                ),
            )

        if (
            BlueprintRuleKind.BOOKEND_REFLECTION in rule_kinds
            and not any(s.activity_kind == _REFLECTION for s in items)
        ):
            items.append(
                BlueprintStep.create(
                    "bookend-reflection",
                    _REFLECTION,
                    sequence_index=len(items),
                    role="consolidate",
                    effort_weight=1,
                    required=True,
                    metadata=("bookend",),
                )
            )

        if (
            BlueprintRuleKind.BOOKEND_SUMMARY in rule_kinds
            and not any(s.activity_kind == _SUMMARY for s in items)
        ):
            items.append(
                BlueprintStep.create(
                    "bookend-summary",
                    _SUMMARY,
                    sequence_index=len(items),
                    role="consolidate",
                    effort_weight=1,
                    required=True,
                    metadata=("bookend",),
                )
            )

        return CompilationPolicy.reindex(items)

    @staticmethod
    def reindex(
        steps: list[BlueprintStep] | tuple[BlueprintStep, ...],
    ) -> tuple[BlueprintStep, ...]:
        """Return steps with contiguous 0-based sequence_index values."""
        return tuple(
            step.with_index(index) for index, step in enumerate(steps or ())
        )

    @staticmethod
    def enforce_required_activities(
        steps: list[BlueprintStep] | tuple[BlueprintStep, ...],
        rules: list[BlueprintRule] | tuple[BlueprintRule, ...] | None = None,
    ) -> tuple[BlueprintStep, ...]:
        """Append missing required activity kinds from REQUIRE_ACTIVITY rules."""
        items = list(steps or ())
        present = {step.activity_kind for step in items}
        for rule in rules or ():
            if rule.kind != BlueprintRuleKind.REQUIRE_ACTIVITY:
                continue
            kind = rule.parameter("activity_kind") or rule.parameter("kind")
            if not kind:
                continue
            token = kind.strip().lower().replace("-", "_").replace(" ", "_")
            if token in present:
                continue
            items.append(
                BlueprintStep.create(
                    f"required-{token}",
                    token,
                    sequence_index=len(items),
                    role="required",
                    effort_weight=1,
                    required=True,
                    metadata=("required_by_rule", rule.rule_id),
                )
            )
            present.add(token)
        return CompilationPolicy.reindex(items)

    @staticmethod
    def estimate_effort_band(
        blueprint: InstructionalBlueprint,
        steps: list[BlueprintStep] | tuple[BlueprintStep, ...] | None = None,
    ) -> EffortBand:
        """Estimate effort band from profile intensity and step weights."""
        base = blueprint.default_effort_band
        items = tuple(steps if steps is not None else blueprint.steps)
        weight_sum = sum(step.effort_weight for step in items)
        intensity = blueprint.profile.intensity if blueprint.profile else 3

        # Deterministic uplift: many weighted steps or high intensity.
        rank = effort_rank(base)
        if weight_sum >= 10 or intensity >= 5 or len(items) >= 8:
            rank = min(4, rank + 1)
        elif weight_sum <= 2 and intensity <= 2 and len(items) <= 3:
            rank = max(1, rank - 1)

        for band, value in (
            (EffortBand.LOW, 1),
            (EffortBand.MEDIUM, 2),
            (EffortBand.HIGH, 3),
            (EffortBand.EXTENSIVE, 4),
        ):
            if value == rank:
                return band
        return EffortBand.MEDIUM

    @staticmethod
    def estimate_effort_units(
        blueprint: InstructionalBlueprint,
        steps: list[BlueprintStep] | tuple[BlueprintStep, ...] | None = None,
    ) -> int:
        """Estimate relative effort units (not study content duration)."""
        items = tuple(steps if steps is not None else blueprint.steps)
        band = CompilationPolicy.estimate_effort_band(blueprint, items)
        base = effort_units_for(band)
        weight_sum = sum(max(1, step.effort_weight) for step in items) if items else 0
        return base + weight_sum

    @staticmethod
    def applied_rule_ids(
        rules: list[BlueprintRule] | tuple[BlueprintRule, ...] | None,
    ) -> tuple[str, ...]:
        """Stable ordered rule identities considered during compilation."""
        return tuple(rule.rule_id for rule in (rules or ()))

    @staticmethod
    def rejects_content_generation() -> bool:
        return True

    @staticmethod
    def rejects_ai() -> bool:
        return True
