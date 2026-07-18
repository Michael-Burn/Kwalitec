"""Structural validation for Instructional Blueprints.

Ensures step integrity, rule consistency, and profile bounds.
Never validates educational content (there is none).
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.instructional_blueprint.exceptions import (
    BlueprintValidationError,
)
from app.application.instructional_blueprint.policies.compilation_policy import (
    CompilationPolicy,
)
from app.domain.instructional_blueprint.blueprint import InstructionalBlueprint
from app.domain.instructional_blueprint.blueprint_rule import BlueprintRuleKind
from app.domain.instructional_blueprint.blueprint_type import BlueprintType


@dataclass(frozen=True)
class ValidationIssue:
    """One structural validation finding."""

    code: str
    message: str
    severity: str = "hard"


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of validating an Instructional Blueprint."""

    is_valid: bool
    issues: tuple[ValidationIssue, ...]

    @property
    def codes(self) -> tuple[str, ...]:
        """Stable issue codes."""
        return tuple(issue.code for issue in self.issues)

    @property
    def hard_issues(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "hard")

    @property
    def soft_issues(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "soft")


class BlueprintValidator:
    """Validate Instructional Blueprint structural integrity invariants."""

    def validate(self, blueprint: InstructionalBlueprint) -> ValidationResult:
        """Validate blueprint structure without mutating state."""
        issues: list[ValidationIssue] = []

        if not blueprint.blueprint_id or not blueprint.blueprint_id.strip():
            issues.append(
                ValidationIssue("empty_blueprint_id", "blueprint_id must be non-empty")
            )
        if not blueprint.name or not blueprint.name.strip():
            issues.append(ValidationIssue("empty_name", "name must be non-empty"))

        if (
            not blueprint.steps
            and blueprint.blueprint_type != BlueprintType.CUSTOM
        ):
            issues.append(
                ValidationIssue(
                    "empty_steps",
                    "non-custom blueprints must define at least one step",
                )
            )

        step_ids: list[str] = []
        indices: list[int] = []
        for step in blueprint.steps:
            if step.step_id in step_ids:
                issues.append(
                    ValidationIssue(
                        "duplicate_step_id",
                        f"duplicate step identity: {step.step_id!r}",
                    )
                )
            step_ids.append(step.step_id)
            if step.sequence_index in indices:
                issues.append(
                    ValidationIssue(
                        "duplicate_index",
                        f"duplicate sequence_index: {step.sequence_index}",
                    )
                )
            indices.append(step.sequence_index)
            if not step.activity_kind or not step.activity_kind.strip():
                issues.append(
                    ValidationIssue(
                        "empty_activity_kind",
                        f"step {step.step_id!r} has empty activity_kind",
                    )
                )
            if step.effort_weight < 0:
                issues.append(
                    ValidationIssue(
                        "negative_effort_weight",
                        f"step {step.step_id!r} has negative effort_weight",
                    )
                )

        if indices and sorted(indices) != list(range(len(indices))):
            issues.append(
                ValidationIssue(
                    "index_gap",
                    "sequence_index values must be contiguous from 0",
                )
            )
        ordered = [step.sequence_index for step in blueprint.steps]
        if ordered != sorted(ordered):
            issues.append(
                ValidationIssue(
                    "order_mismatch",
                    "steps must be ordered by ascending sequence_index",
                )
            )

        rule_ids: list[str] = []
        for rule in blueprint.rules:
            if rule.rule_id in rule_ids:
                issues.append(
                    ValidationIssue(
                        "duplicate_rule_id",
                        f"duplicate rule identity: {rule.rule_id!r}",
                    )
                )
            rule_ids.append(rule.rule_id)

        if blueprint.profile is not None:
            if blueprint.profile.total_weight == 0:
                issues.append(
                    ValidationIssue(
                        "zero_profile_weight",
                        "profile weights must not all be zero",
                        severity="soft",
                    )
                )
            for name, value in (
                ("theory_weight", blueprint.profile.theory_weight),
                ("practice_weight", blueprint.profile.practice_weight),
                ("revision_weight", blueprint.profile.revision_weight),
                ("assessment_weight", blueprint.profile.assessment_weight),
            ):
                if value < 0 or value > 100:
                    issues.append(
                        ValidationIssue(
                            "profile_weight_range",
                            f"{name} must be in 0..100",
                        )
                    )
            if blueprint.profile.intensity < 1 or blueprint.profile.intensity > 5:
                issues.append(
                    ValidationIssue(
                        "intensity_range",
                        "intensity must be in 1..5",
                    )
                )

        issues.extend(self._validate_rules(blueprint))

        hard = [issue for issue in issues if issue.severity == "hard"]
        return ValidationResult(is_valid=not hard, issues=tuple(issues))

    def assert_valid(self, blueprint: InstructionalBlueprint) -> None:
        """Raise BlueprintValidationError when the blueprint is invalid."""
        result = self.validate(blueprint)
        if not result.is_valid:
            codes = ", ".join(result.codes)
            raise BlueprintValidationError(
                f"Blueprint validation failed: {codes}"
            )

    def _validate_rules(
        self, blueprint: InstructionalBlueprint
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        kinds = {step.activity_kind for step in blueprint.steps}
        practice_ratio = CompilationPolicy.practice_ratio(blueprint.steps)
        theory_ratio = CompilationPolicy.theory_ratio(blueprint.steps)

        for rule in blueprint.rules:
            severity = rule.severity
            if rule.kind == BlueprintRuleKind.REQUIRE_ACTIVITY:
                required = rule.parameter("activity_kind") or rule.parameter("kind")
                if required and required not in kinds:
                    issues.append(
                        ValidationIssue(
                            "missing_required_activity",
                            f"required activity {required!r} is absent",
                            severity=severity,
                        )
                    )
            elif rule.kind == BlueprintRuleKind.FORBID_ACTIVITY:
                forbidden = rule.parameter("activity_kind") or rule.parameter("kind")
                if forbidden and forbidden in kinds:
                    issues.append(
                        ValidationIssue(
                            "forbidden_activity_present",
                            f"forbidden activity {forbidden!r} is present",
                            severity=severity,
                        )
                    )
            elif rule.kind == BlueprintRuleKind.MAX_STEPS:
                raw = rule.parameter("count", "0") or "0"
                try:
                    maximum = int(raw)
                except ValueError:
                    issues.append(
                        ValidationIssue(
                            "invalid_rule_parameter",
                            f"rule {rule.rule_id!r} has non-integer max_steps",
                            severity=severity,
                        )
                    )
                    continue
                if len(blueprint.steps) > maximum:
                    issues.append(
                        ValidationIssue(
                            "max_steps_exceeded",
                            f"step count {len(blueprint.steps)} exceeds max {maximum}",
                            severity=severity,
                        )
                    )
            elif rule.kind == BlueprintRuleKind.MIN_STEPS:
                raw = rule.parameter("count", "0") or "0"
                try:
                    minimum = int(raw)
                except ValueError:
                    issues.append(
                        ValidationIssue(
                            "invalid_rule_parameter",
                            f"rule {rule.rule_id!r} has non-integer min_steps",
                            severity=severity,
                        )
                    )
                    continue
                if len(blueprint.steps) < minimum:
                    issues.append(
                        ValidationIssue(
                            "min_steps_not_met",
                            f"step count {len(blueprint.steps)} below min {minimum}",
                            severity=severity,
                        )
                    )
            elif rule.kind == BlueprintRuleKind.MIN_PRACTICE_RATIO:
                raw = rule.parameter("ratio", "0") or "0"
                try:
                    minimum = float(raw)
                except ValueError:
                    issues.append(
                        ValidationIssue(
                            "invalid_rule_parameter",
                            f"rule {rule.rule_id!r} has non-float min_practice_ratio",
                            severity=severity,
                        )
                    )
                    continue
                if practice_ratio + 1e-9 < minimum:
                    issues.append(
                        ValidationIssue(
                            "min_practice_ratio_not_met",
                            f"practice ratio {practice_ratio:.2f} below {minimum}",
                            severity=severity,
                        )
                    )
            elif rule.kind == BlueprintRuleKind.MAX_THEORY_RATIO:
                raw = rule.parameter("ratio", "1") or "1"
                try:
                    maximum = float(raw)
                except ValueError:
                    issues.append(
                        ValidationIssue(
                            "invalid_rule_parameter",
                            f"rule {rule.rule_id!r} has non-float max_theory_ratio",
                            severity=severity,
                        )
                    )
                    continue
                if theory_ratio - 1e-9 > maximum:
                    issues.append(
                        ValidationIssue(
                            "max_theory_ratio_exceeded",
                            f"theory ratio {theory_ratio:.2f} exceeds {maximum}",
                            severity=severity,
                        )
                    )
        return issues
