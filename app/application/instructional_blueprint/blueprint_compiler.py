"""Compile an Instructional Blueprint into executable instructional structure.

Applies structural rules and estimates effort. Never generates educational
content, questions, explanations, or PDFs.
"""

from __future__ import annotations

from app.application.instructional_blueprint.blueprint_validator import (
    BlueprintValidator,
)
from app.application.instructional_blueprint.dto.compiled_blueprint import (
    CompiledBlueprint,
)
from app.application.instructional_blueprint.exceptions import (
    BlueprintCompilationError,
)
from app.application.instructional_blueprint.policies.compilation_policy import (
    CompilationPolicy,
)
from app.domain.instructional_blueprint.blueprint import InstructionalBlueprint
from app.domain.instructional_blueprint.blueprint_step import BlueprintStep
from app.domain.instructional_blueprint.blueprint_type import BlueprintType

_POST_COMPILE_BLOCKING = frozenset(
    {
        "forbidden_activity_present",
        "max_steps_exceeded",
        "min_practice_ratio_not_met",
        "max_theory_ratio_exceeded",
        "duplicate_step_id",
        "index_gap",
        "order_mismatch",
    }
)


_AUTO_FIXED_PRECOMPILE = frozenset(
    {
        "missing_required_activity",
        "min_steps_not_met",  # may be satisfied after bookends / required appends
    }
)


class BlueprintCompiler:
    """Compile Instructional Blueprints into ``CompiledBlueprint`` values."""

    def __init__(self, *, validator: BlueprintValidator | None = None) -> None:
        self._validator = validator or BlueprintValidator()

    def compile(
        self,
        blueprint: InstructionalBlueprint,
        *,
        extra_steps: list[BlueprintStep] | tuple[BlueprintStep, ...] | None = None,
        validate: bool = True,
    ) -> CompiledBlueprint:
        """Compile a blueprint into ordered instructional structure.

        Args:
            blueprint: Source instructional blueprint.
            extra_steps: Optional caller-supplied steps (replace empty CUSTOM
                steps, otherwise appended).
            validate: When True, reject structurally invalid blueprints.

        Returns:
            Immutable CompiledBlueprint.

        Raises:
            BlueprintCompilationError: When compilation cannot proceed.
        """
        if validate:
            self._assert_compilable(blueprint, extra_steps=extra_steps)

        steps = list(blueprint.steps)
        if extra_steps:
            if blueprint.blueprint_type == BlueprintType.CUSTOM and not steps:
                steps = list(extra_steps)
            else:
                steps.extend(extra_steps)
            steps = list(CompilationPolicy.reindex(steps))

        if not steps:
            raise BlueprintCompilationError(
                "Cannot compile blueprint with zero steps"
            )

        steps = list(
            CompilationPolicy.enforce_required_activities(steps, blueprint.rules)
        )
        steps = list(CompilationPolicy.apply_bookends(steps, blueprint.rules))

        if validate:
            probe = blueprint.with_steps(steps)
            post = self._validator.validate(probe)
            blocking = [
                issue
                for issue in post.hard_issues
                if issue.code in _POST_COMPILE_BLOCKING
            ]
            if blocking:
                codes = ", ".join(issue.code for issue in blocking)
                raise BlueprintCompilationError(
                    f"Compiled blueprint violates rules: {codes}"
                )

        effort_band = CompilationPolicy.estimate_effort_band(blueprint, steps)
        effort_units = CompilationPolicy.estimate_effort_units(blueprint, steps)
        practice_ratio = CompilationPolicy.practice_ratio(steps)
        theory_ratio = CompilationPolicy.theory_ratio(steps)
        applied = CompilationPolicy.applied_rule_ids(blueprint.rules)

        rationale = (
            f"blueprint={blueprint.blueprint_id}",
            f"type={blueprint.blueprint_type.value}",
            f"steps={len(steps)}",
            f"effort={effort_band.value}",
            f"practice_ratio={practice_ratio:.2f}",
            f"theory_ratio={theory_ratio:.2f}",
            "no_content_generation",
            "no_ai",
            "no_questions",
            "no_explanations",
            "no_pdfs",
        )

        return CompiledBlueprint(
            blueprint_id=blueprint.blueprint_id,
            blueprint_type=blueprint.blueprint_type,
            steps=tuple(steps),
            applied_rule_ids=applied,
            estimated_effort_band=effort_band,
            estimated_effort_units=effort_units,
            practice_ratio=practice_ratio,
            theory_ratio=theory_ratio,
            rationale_tags=rationale,
            version=blueprint.version,
        )

    def _assert_compilable(
        self,
        blueprint: InstructionalBlueprint,
        *,
        extra_steps: list[BlueprintStep] | tuple[BlueprintStep, ...] | None,
    ) -> None:
        result = self._validator.validate(blueprint)
        if result.is_valid:
            return

        # CUSTOM blueprints may start empty and receive extra_steps.
        if (
            blueprint.blueprint_type == BlueprintType.CUSTOM
            and extra_steps
            and not blueprint.steps
        ):
            soft_or_empty = {
                "min_steps_not_met",
                "empty_steps",
                "zero_profile_weight",
            }
            if set(result.codes) <= soft_or_empty or not result.hard_issues:
                return

        remaining_hard = [
            issue
            for issue in result.hard_issues
            if issue.code not in _AUTO_FIXED_PRECOMPILE
        ]
        if remaining_hard:
            codes = ", ".join(issue.code for issue in remaining_hard)
            raise BlueprintCompilationError(
                f"Cannot compile invalid blueprint: {codes}"
            )
