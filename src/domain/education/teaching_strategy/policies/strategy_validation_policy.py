"""Policy governing TeachingStrategy construction and integrity.

Architecture Source
    STRATEGY_INVARIANTS.md
    TEACHING_STRATEGY_ARCHITECTURE.md
Concept
    Strategy Validation Policy
"""

from __future__ import annotations

from domain.education.foundation.base import (
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import (
    DiagnosisType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import TeachingStrategyId
from domain.education.teaching_strategy.entities.strategy_constraint import (
    StrategyConstraint,
)
from domain.education.teaching_strategy.entities.strategy_goal import StrategyGoal
from domain.education.teaching_strategy.entities.strategy_rationale import (
    StrategyRationale,
)
from domain.education.teaching_strategy.entities.strategy_reference import (
    DiagnosisReference,
    HypothesisReference,
    IntentionReference,
    SecondaryStrategyReference,
)
from domain.education.teaching_strategy.enums import (
    ComplexityLevel,
    StrategyConstraintKind,
    StrategyStatus,
)
from domain.education.teaching_strategy.policies.strategy_composition_policy import (
    StrategyCompositionPolicy,
)
from domain.education.teaching_strategy.policies.strategy_selection_policy import (
    StrategySelectionPolicy,
)
from domain.education.teaching_strategy.value_objects.instructional_complexity import (
    InstructionalComplexity,
)
from domain.education.teaching_strategy.value_objects.strategy_effectiveness import (
    StrategyEffectiveness,
)

_COMPLEXITY_ORDER: tuple[ComplexityLevel, ...] = (
    ComplexityLevel.LOW,
    ComplexityLevel.MODERATE,
    ComplexityLevel.HIGH,
    ComplexityLevel.VERY_HIGH,
)

_MUTABLE_STATUSES = frozenset(
    {
        StrategyStatus.DRAFT,
        StrategyStatus.SELECTED,
        StrategyStatus.REVISED,
    }
)

_COMMITTED_STATUSES = frozenset(
    {
        StrategyStatus.SELECTED,
        StrategyStatus.REVISED,
    }
)


class StrategyValidationPolicy:
    """Enforces TeachingStrategy identity, ownership, and lifecycle invariants."""

    @staticmethod
    def assert_identity(strategy_id: TeachingStrategyId) -> TeachingStrategyId:
        if not isinstance(strategy_id, TeachingStrategyId):
            raise EducationalInvariantViolation(
                "teaching strategy must possess a TeachingStrategyId identity",
                invariant="TeachingStrategy.identity.required",
            )
        return strategy_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_primary_strategy(
        strategy_type: TeachingStrategyType,
    ) -> TeachingStrategyType:
        if not isinstance(strategy_type, TeachingStrategyType):
            raise EducationalInvariantViolation(
                "teaching strategy must identify one primary strategy",
                invariant="TeachingStrategy.primary_strategy.required",
            )
        if not StrategySelectionPolicy.is_catalogue_strategy(strategy_type):
            raise EducationalInvariantViolation(
                "primary strategy must be a catalogue strategy",
                invariant="TeachingStrategy.primary_strategy.catalogue",
            )
        return strategy_type

    @staticmethod
    def assert_goal(goal: StrategyGoal) -> StrategyGoal:
        if not isinstance(goal, StrategyGoal):
            raise EducationalInvariantViolation(
                "teaching strategy must possess a goal",
                invariant="TeachingStrategy.goal.required",
            )
        if not goal.statement.strip():
            raise EducationalInvariantViolation(
                "teaching strategy must possess a goal",
                invariant="TeachingStrategy.goal.statement.required",
            )
        return goal

    @staticmethod
    def assert_goal_matches_primary(
        goal: StrategyGoal,
        primary: TeachingStrategyType,
    ) -> None:
        if goal.strategy_type is not primary:
            raise EducationalInvariantViolation(
                "strategy goal type must match aggregate primary strategy",
                invariant="TeachingStrategy.goal.type_match",
            )

    @staticmethod
    def assert_rationale(rationale: StrategyRationale) -> StrategyRationale:
        if not isinstance(rationale, StrategyRationale):
            raise EducationalInvariantViolation(
                "teaching strategy must include rationale",
                invariant="TeachingStrategy.rationale.required",
            )
        if not rationale.statement.strip():
            raise EducationalInvariantViolation(
                "teaching strategy must include rationale",
                invariant="TeachingStrategy.rationale.statement.required",
            )
        return rationale

    @staticmethod
    def assert_effectiveness(
        effectiveness: StrategyEffectiveness,
    ) -> StrategyEffectiveness:
        if not isinstance(effectiveness, StrategyEffectiveness):
            raise EducationalInvariantViolation(
                "teaching strategy must possess effectiveness estimate",
                invariant="TeachingStrategy.effectiveness.required",
            )
        return effectiveness

    @staticmethod
    def assert_complexity(
        complexity: InstructionalComplexity,
    ) -> InstructionalComplexity:
        if not isinstance(complexity, InstructionalComplexity):
            raise EducationalInvariantViolation(
                "teaching strategy must possess instructional complexity",
                invariant="TeachingStrategy.complexity.required",
            )
        return complexity

    @staticmethod
    def assert_status(status: StrategyStatus) -> StrategyStatus:
        if not isinstance(status, StrategyStatus):
            raise EducationalInvariantViolation(
                "status must be a StrategyStatus",
                invariant="TeachingStrategy.status.type",
            )
        return status

    @staticmethod
    def assert_mutable(status: StrategyStatus, *, action: str) -> None:
        if status is StrategyStatus.RETIRED:
            raise EducationalInvariantViolation(
                f"cannot {action} a retired teaching strategy",
                invariant="TeachingStrategy.status.mutable",
            )
        if status not in _MUTABLE_STATUSES:
            raise EducationalInvariantViolation(
                f"cannot {action} teaching strategy in status {status.value}",
                invariant="TeachingStrategy.status.mutable",
            )

    @staticmethod
    def assert_can_select(status: StrategyStatus) -> None:
        if status is StrategyStatus.RETIRED:
            raise EducationalInvariantViolation(
                "cannot select a retired teaching strategy",
                invariant="TeachingStrategy.select.retired",
            )
        if status in _COMMITTED_STATUSES:
            raise EducationalInvariantViolation(
                "teaching strategy is already selected",
                invariant="TeachingStrategy.select.already",
            )
        if status is not StrategyStatus.DRAFT:
            raise EducationalInvariantViolation(
                "only draft teaching strategies can be selected",
                invariant="TeachingStrategy.select.draft",
            )

    @staticmethod
    def assert_can_retire(status: StrategyStatus) -> None:
        if status is StrategyStatus.RETIRED:
            raise EducationalInvariantViolation(
                "teaching strategy is already retired",
                invariant="TeachingStrategy.retire.already",
            )

    @staticmethod
    def assert_primary_change_allowed(
        status: StrategyStatus,
        current: TeachingStrategyType,
        proposed: TeachingStrategyType,
    ) -> None:
        if current is proposed:
            return
        if status in _COMMITTED_STATUSES:
            raise EducationalInvariantViolation(
                "cannot change primary strategy after selection",
                invariant="TeachingStrategy.primary.immutable_after_selection",
            )

    @staticmethod
    def assert_intention_references(
        references: tuple[IntentionReference, ...] | list[IntentionReference],
    ) -> tuple[IntentionReference, ...]:
        collected = tuple(references)
        if not collected:
            raise EducationalInvariantViolation(
                "teaching strategy must reference Teaching Intention",
                invariant="TeachingStrategy.intention_references.min_one",
            )
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, IntentionReference):
                raise EducationalInvariantViolation(
                    "intention_references must be IntentionReference values",
                    invariant="TeachingStrategy.intention_references.type",
                )
            if ref.intention_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate intention reference is not allowed",
                    invariant="TeachingStrategy.intention_references.no_duplicate",
                )
            seen.add(ref.intention_id.value)
        return collected

    @staticmethod
    def assert_diagnosis_references(
        references: tuple[DiagnosisReference, ...] | list[DiagnosisReference],
    ) -> tuple[DiagnosisReference, ...]:
        collected = tuple(references)
        if not collected:
            raise EducationalInvariantViolation(
                "teaching strategy must reference diagnosis",
                invariant="TeachingStrategy.diagnosis_references.min_one",
            )
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, DiagnosisReference):
                raise EducationalInvariantViolation(
                    "diagnosis_references must be DiagnosisReference values",
                    invariant="TeachingStrategy.diagnosis_references.type",
                )
            if ref.diagnosis_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate diagnosis reference is not allowed",
                    invariant="TeachingStrategy.diagnosis_references.no_duplicate",
                )
            seen.add(ref.diagnosis_id.value)
        return collected

    @staticmethod
    def assert_hypothesis_references(
        references: tuple[HypothesisReference, ...] | list[HypothesisReference],
    ) -> tuple[HypothesisReference, ...]:
        collected = tuple(references)
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, HypothesisReference):
                raise EducationalInvariantViolation(
                    "hypothesis_references must be HypothesisReference values",
                    invariant="TeachingStrategy.hypothesis_references.type",
                )
            if ref.hypothesis_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate hypothesis reference is not allowed",
                    invariant="TeachingStrategy.hypothesis_references.no_duplicate",
                )
            seen.add(ref.hypothesis_id.value)
        return collected

    @staticmethod
    def assert_constraints(
        constraints: tuple[StrategyConstraint, ...] | list[StrategyConstraint],
    ) -> tuple[StrategyConstraint, ...]:
        collected = tuple(constraints)
        seen_ids: set[str] = set()
        seen_signatures: set[tuple[str, str | None, str | None]] = set()
        for constraint in collected:
            if not isinstance(constraint, StrategyConstraint):
                raise EducationalInvariantViolation(
                    "constraints must be StrategyConstraint entities",
                    invariant="TeachingStrategy.constraints.type",
                )
            if constraint.constraint_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate strategy constraint identity is not allowed",
                    invariant="TeachingStrategy.constraints.no_duplicate_id",
                )
            signature = constraint.constraint_signature()
            if signature in seen_signatures:
                raise EducationalInvariantViolation(
                    "cannot duplicate constraints",
                    invariant="TeachingStrategy.constraints.no_identical_duplicate",
                )
            seen_ids.add(constraint.constraint_id.value)
            seen_signatures.add(signature)
        return collected

    @staticmethod
    def assert_secondary_strategies(
        primary: TeachingStrategyType,
        secondaries: tuple[SecondaryStrategyReference, ...]
        | list[SecondaryStrategyReference],
    ) -> tuple[SecondaryStrategyReference, ...]:
        return StrategyCompositionPolicy.assert_secondaries(primary, secondaries)

    @staticmethod
    def assert_constraints_satisfied(
        constraints: tuple[StrategyConstraint, ...] | list[StrategyConstraint],
        *,
        primary: TeachingStrategyType,
        complexity: InstructionalComplexity,
        intention_references: tuple[IntentionReference, ...]
        | list[IntentionReference],
        diagnosis_references: tuple[DiagnosisReference, ...]
        | list[DiagnosisReference],
        hypothesis_references: tuple[HypothesisReference, ...]
        | list[HypothesisReference],
        rationale: StrategyRationale,
        effectiveness: StrategyEffectiveness,
        secondaries: tuple[SecondaryStrategyReference, ...]
        | list[SecondaryStrategyReference],
    ) -> None:
        """Reject strategies that contradict educational constraints."""
        for constraint in constraints:
            kind = constraint.kind
            if kind is StrategyConstraintKind.REQUIRE_INTENTION_REFERENCE:
                if not intention_references:
                    raise EducationalInvariantViolation(
                        "constraint requires an intention reference",
                        invariant="TeachingStrategy.constraints.require_intention",
                    )
            elif kind is StrategyConstraintKind.REQUIRE_DIAGNOSIS_REFERENCE:
                if not diagnosis_references:
                    raise EducationalInvariantViolation(
                        "constraint requires a diagnosis reference",
                        invariant="TeachingStrategy.constraints.require_diagnosis",
                    )
            elif kind is StrategyConstraintKind.REQUIRE_HYPOTHESIS_REFERENCE:
                if not hypothesis_references:
                    raise EducationalInvariantViolation(
                        "constraint requires a hypothesis reference",
                        invariant="TeachingStrategy.constraints.require_hypothesis",
                    )
            elif kind is StrategyConstraintKind.REQUIRE_RATIONALE:
                if not rationale.statement.strip():
                    raise EducationalInvariantViolation(
                        "constraint requires educational rationale",
                        invariant="TeachingStrategy.constraints.require_rationale",
                    )
            elif kind is StrategyConstraintKind.REQUIRE_EFFECTIVENESS:
                if effectiveness is None:
                    raise EducationalInvariantViolation(
                        "constraint requires effectiveness estimate",
                        invariant="TeachingStrategy.constraints.require_effectiveness",
                    )
            elif kind is StrategyConstraintKind.REQUIRE_INTENTION_AFFINITY:
                StrategySelectionPolicy.assert_serves_intention(
                    primary,
                    intention_references,
                    require_affinity=True,
                )
            elif kind is StrategyConstraintKind.FORBID_MASTERY_CLAIM:
                lowered = (
                    f"{rationale.statement} {effectiveness.rationale or ''}"
                ).casefold()
                if any(
                    token in lowered
                    for token in (
                        "mastered",
                        "achieve mastery",
                        "declare mastery",
                        "full mastery",
                    )
                ):
                    raise EducationalInvariantViolation(
                        "constraint forbids mastery claim",
                        invariant="TeachingStrategy.constraints.forbid_mastery",
                    )
            elif kind is StrategyConstraintKind.FORBID_COEQUAL_PRIMARIES:
                StrategyCompositionPolicy.assert_no_coequal_primaries(
                    primary, secondaries
                )
            elif kind is StrategyConstraintKind.PROTECT_ATOMICITY:
                # One primary strategy is enforced by aggregate identity.
                continue
            elif kind is StrategyConstraintKind.FORBID_STRATEGY_TYPE:
                forbidden = constraint.forbidden_strategy_type
                if forbidden is not None and (
                    primary is forbidden
                    or any(ref.strategy_type is forbidden for ref in secondaries)
                ):
                    raise EducationalInvariantViolation(
                        f"constraint forbids strategy type {forbidden.value}",
                        invariant="TeachingStrategy.constraints.forbid_type",
                    )
            elif kind is StrategyConstraintKind.CAP_COMPLEXITY:
                cap = constraint.max_complexity
                if cap is not None and _COMPLEXITY_ORDER.index(
                    complexity.level
                ) > _COMPLEXITY_ORDER.index(cap):
                    raise EducationalInvariantViolation(
                        "instructional complexity exceeds constraint cap",
                        invariant="TeachingStrategy.constraints.cap_complexity",
                    )
            elif kind is StrategyConstraintKind.REQUIRE_MISCONCEPTION_STRATEGY:
                StrategySelectionPolicy.assert_misconception_duty(
                    primary, intention_references, diagnosis_references
                )
            elif kind is StrategyConstraintKind.FORBID_EXAM_OVER_MISCONCEPTION:
                StrategySelectionPolicy.assert_not_exam_over_misconception(
                    primary, diagnosis_references
                )
                for ref in secondaries:
                    StrategySelectionPolicy.assert_not_exam_over_misconception(
                        ref.strategy_type, diagnosis_references
                    )

    @staticmethod
    def assert_educational_integrity(
        *,
        primary: TeachingStrategyType,
        intention_references: tuple[IntentionReference, ...]
        | list[IntentionReference],
        diagnosis_references: tuple[DiagnosisReference, ...]
        | list[DiagnosisReference],
        require_affinity: bool = False,
    ) -> None:
        StrategySelectionPolicy.assert_serves_intention(
            primary,
            intention_references,
            require_affinity=require_affinity,
        )
        intention_types = {ref.intention_type for ref in intention_references}
        diagnosis_types = {ref.diagnosis_type for ref in diagnosis_references}
        if (
            TeachingIntentionType.REPAIR_MISCONCEPTION in intention_types
            or DiagnosisType.MISCONCEPTION in diagnosis_types
        ):
            StrategySelectionPolicy.assert_misconception_duty(
                primary, intention_references, diagnosis_references
            )
        StrategySelectionPolicy.assert_not_exam_over_misconception(
            primary, diagnosis_references
        )

    @staticmethod
    def assert_retire_reason(reason: str | None) -> str | None:
        if reason is None:
            return None
        return require_non_empty_text(reason, "retire_reason")
