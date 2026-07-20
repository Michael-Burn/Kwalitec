"""Policy governing TeachingIntention construction and integrity.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    Intention Validation Policy
"""

from __future__ import annotations

from domain.education.foundation.base import (
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import DiagnosisType, TeachingIntentionType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import TeachingIntentionId
from domain.education.teaching_intention.entities.intention_constraint import (
    IntentionConstraint,
)
from domain.education.teaching_intention.entities.intention_goal import IntentionGoal
from domain.education.teaching_intention.entities.intention_reference import (
    DiagnosisReference,
    HypothesisReference,
    PriorityReference,
)
from domain.education.teaching_intention.entities.intention_scope import IntentionScope
from domain.education.teaching_intention.enums import (
    IntentionConstraintKind,
    IntentionStatus,
    IntentionStrengthLevel,
)
from domain.education.teaching_intention.value_objects.expected_outcome import (
    ExpectedOutcome,
)
from domain.education.teaching_intention.value_objects.intention_strength import (
    IntentionStrength,
)

_STRENGTH_ORDER: tuple[IntentionStrengthLevel, ...] = (
    IntentionStrengthLevel.TENTATIVE,
    IntentionStrengthLevel.MODERATE,
    IntentionStrengthLevel.FIRM,
    IntentionStrengthLevel.COMMITTED,
)

_MUTABLE_STATUSES = frozenset(
    {
        IntentionStatus.DRAFT,
        IntentionStatus.ACTIVE,
        IntentionStatus.REVISED,
    }
)

_ACTIVATED_STATUSES = frozenset(
    {
        IntentionStatus.ACTIVE,
        IntentionStatus.REVISED,
    }
)


class IntentionValidationPolicy:
    """Enforces TeachingIntention identity, ownership, and lifecycle invariants."""

    @staticmethod
    def assert_identity(intention_id: TeachingIntentionId) -> TeachingIntentionId:
        if not isinstance(intention_id, TeachingIntentionId):
            raise EducationalInvariantViolation(
                "teaching intention must possess a TeachingIntentionId identity",
                invariant="TeachingIntention.identity.required",
            )
        return intention_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_intention_type(
        intention_type: TeachingIntentionType,
    ) -> TeachingIntentionType:
        if not isinstance(intention_type, TeachingIntentionType):
            raise EducationalInvariantViolation(
                "teaching intention must identify one intention type",
                invariant="TeachingIntention.intention_type.required",
            )
        return intention_type

    @staticmethod
    def assert_goal(goal: IntentionGoal) -> IntentionGoal:
        if not isinstance(goal, IntentionGoal):
            raise EducationalInvariantViolation(
                "teaching intention must possess a goal",
                invariant="TeachingIntention.goal.required",
            )
        if not goal.statement.strip():
            raise EducationalInvariantViolation(
                "teaching intention must possess a goal",
                invariant="TeachingIntention.goal.statement.required",
            )
        return goal

    @staticmethod
    def assert_goal_matches_type(
        goal: IntentionGoal,
        intention_type: TeachingIntentionType,
    ) -> None:
        if goal.intention_type is not intention_type:
            raise EducationalInvariantViolation(
                "intention goal type must match aggregate intention type",
                invariant="TeachingIntention.goal.type_match",
            )

    @staticmethod
    def assert_scope(scope: IntentionScope) -> IntentionScope:
        if not isinstance(scope, IntentionScope):
            raise EducationalInvariantViolation(
                "teaching intention must possess instructional scope",
                invariant="TeachingIntention.scope.required",
            )
        if not scope.statement.strip():
            raise EducationalInvariantViolation(
                "teaching intention must possess instructional scope",
                invariant="TeachingIntention.scope.statement.required",
            )
        return scope

    @staticmethod
    def assert_expected_outcome(outcome: ExpectedOutcome) -> ExpectedOutcome:
        if not isinstance(outcome, ExpectedOutcome):
            raise EducationalInvariantViolation(
                "teaching intention must possess expected outcome",
                invariant="TeachingIntention.expected_outcome.required",
            )
        if not outcome.statement.strip() or not outcome.success_evidence.strip():
            raise EducationalInvariantViolation(
                "teaching intention must possess expected outcome",
                invariant="TeachingIntention.expected_outcome.complete",
            )
        return outcome

    @staticmethod
    def assert_strength(strength: IntentionStrength) -> IntentionStrength:
        if not isinstance(strength, IntentionStrength):
            raise EducationalInvariantViolation(
                "teaching intention must possess strength",
                invariant="TeachingIntention.strength.required",
            )
        return strength

    @staticmethod
    def assert_status(status: IntentionStatus) -> IntentionStatus:
        if not isinstance(status, IntentionStatus):
            raise EducationalInvariantViolation(
                "status must be an IntentionStatus",
                invariant="TeachingIntention.status.type",
            )
        return status

    @staticmethod
    def assert_mutable(status: IntentionStatus, *, action: str) -> None:
        if status is IntentionStatus.RETIRED:
            raise EducationalInvariantViolation(
                f"cannot {action} a retired teaching intention",
                invariant="TeachingIntention.status.mutable",
            )
        if status not in _MUTABLE_STATUSES:
            raise EducationalInvariantViolation(
                f"cannot {action} teaching intention in status {status.value}",
                invariant="TeachingIntention.status.mutable",
            )

    @staticmethod
    def assert_can_strengthen(status: IntentionStatus) -> None:
        if status is IntentionStatus.RETIRED:
            raise EducationalInvariantViolation(
                "retired intentions cannot be strengthened",
                invariant="TeachingIntention.strengthen.retired",
            )
        if status not in _ACTIVATED_STATUSES:
            raise EducationalInvariantViolation(
                "only activated teaching intentions can be strengthened",
                invariant="TeachingIntention.strengthen.activation",
            )

    @staticmethod
    def assert_can_weaken(status: IntentionStatus) -> None:
        if status is IntentionStatus.RETIRED:
            raise EducationalInvariantViolation(
                "retired intentions cannot be weakened",
                invariant="TeachingIntention.weaken.retired",
            )
        if status not in _ACTIVATED_STATUSES:
            raise EducationalInvariantViolation(
                "only activated teaching intentions can be weakened",
                invariant="TeachingIntention.weaken.activation",
            )

    @staticmethod
    def assert_can_activate(status: IntentionStatus) -> None:
        if status is IntentionStatus.RETIRED:
            raise EducationalInvariantViolation(
                "cannot activate a retired teaching intention",
                invariant="TeachingIntention.activate.retired",
            )
        if status in _ACTIVATED_STATUSES:
            raise EducationalInvariantViolation(
                "teaching intention is already activated",
                invariant="TeachingIntention.activate.already",
            )
        if status is not IntentionStatus.DRAFT:
            raise EducationalInvariantViolation(
                "only draft teaching intentions can be activated",
                invariant="TeachingIntention.activate.draft",
            )

    @staticmethod
    def assert_can_retire(status: IntentionStatus) -> None:
        if status is IntentionStatus.RETIRED:
            raise EducationalInvariantViolation(
                "teaching intention is already retired",
                invariant="TeachingIntention.retire.already",
            )

    @staticmethod
    def assert_type_change_allowed(
        status: IntentionStatus,
        current: TeachingIntentionType,
        proposed: TeachingIntentionType,
    ) -> None:
        if current is proposed:
            return
        if status in _ACTIVATED_STATUSES:
            raise EducationalInvariantViolation(
                "cannot change intention type after activation",
                invariant="TeachingIntention.intention_type.immutable_after_activation",
            )

    @staticmethod
    def assert_priority_references(
        references: tuple[PriorityReference, ...] | list[PriorityReference],
    ) -> tuple[PriorityReference, ...]:
        collected = tuple(references)
        if not collected:
            raise EducationalInvariantViolation(
                "teaching intention must reference a Priority",
                invariant="TeachingIntention.priority_references.min_one",
            )
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, PriorityReference):
                raise EducationalInvariantViolation(
                    "priority_references must be PriorityReference values",
                    invariant="TeachingIntention.priority_references.type",
                )
            if ref.priority_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate priority reference is not allowed",
                    invariant="TeachingIntention.priority_references.no_duplicate",
                )
            seen.add(ref.priority_id.value)
        return collected

    @staticmethod
    def assert_diagnosis_references(
        references: tuple[DiagnosisReference, ...] | list[DiagnosisReference],
    ) -> tuple[DiagnosisReference, ...]:
        collected = tuple(references)
        if not collected:
            raise EducationalInvariantViolation(
                "teaching intention must reference diagnosis",
                invariant="TeachingIntention.diagnosis_references.min_one",
            )
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, DiagnosisReference):
                raise EducationalInvariantViolation(
                    "diagnosis_references must be DiagnosisReference values",
                    invariant="TeachingIntention.diagnosis_references.type",
                )
            if ref.diagnosis_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate diagnosis reference is not allowed",
                    invariant="TeachingIntention.diagnosis_references.no_duplicate",
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
                    invariant="TeachingIntention.hypothesis_references.type",
                )
            if ref.hypothesis_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate hypothesis reference is not allowed",
                    invariant="TeachingIntention.hypothesis_references.no_duplicate",
                )
            seen.add(ref.hypothesis_id.value)
        return collected

    @staticmethod
    def assert_constraints(
        constraints: tuple[IntentionConstraint, ...] | list[IntentionConstraint],
    ) -> tuple[IntentionConstraint, ...]:
        collected = tuple(constraints)
        seen_ids: set[str] = set()
        seen_signatures: set[tuple[str, str | None, str | None]] = set()
        for constraint in collected:
            if not isinstance(constraint, IntentionConstraint):
                raise EducationalInvariantViolation(
                    "constraints must be IntentionConstraint entities",
                    invariant="TeachingIntention.constraints.type",
                )
            if constraint.constraint_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate intention constraint identity is not allowed",
                    invariant="TeachingIntention.constraints.no_duplicate_id",
                )
            signature = constraint.constraint_signature()
            if signature in seen_signatures:
                raise EducationalInvariantViolation(
                    "cannot duplicate constraints",
                    invariant="TeachingIntention.constraints.no_identical_duplicate",
                )
            seen_ids.add(constraint.constraint_id.value)
            seen_signatures.add(signature)
        return collected

    @staticmethod
    def assert_constraints_satisfied(
        constraints: tuple[IntentionConstraint, ...] | list[IntentionConstraint],
        *,
        intention_type: TeachingIntentionType,
        strength: IntentionStrength,
        priority_references: tuple[PriorityReference, ...] | list[PriorityReference],
        diagnosis_references: tuple[DiagnosisReference, ...]
        | list[DiagnosisReference],
        hypothesis_references: tuple[HypothesisReference, ...]
        | list[HypothesisReference],
        expected_outcome: ExpectedOutcome,
    ) -> None:
        """Reject intentions that contradict educational constraints."""
        for constraint in constraints:
            if constraint.kind is IntentionConstraintKind.REQUIRE_PRIORITY_REFERENCE:
                if not priority_references:
                    raise EducationalInvariantViolation(
                        "constraint requires a priority reference",
                        invariant="TeachingIntention.constraints.require_priority",
                    )
            elif constraint.kind is IntentionConstraintKind.REQUIRE_DIAGNOSIS_ALIGNMENT:
                if not diagnosis_references:
                    raise EducationalInvariantViolation(
                        "constraint requires diagnosis references for alignment",
                        invariant=(
                            "TeachingIntention.constraints.require_diagnosis_alignment"
                        ),
                    )
            elif (
                constraint.kind
                is IntentionConstraintKind.REQUIRE_HYPOTHESIS_REFERENCE
            ):
                if not hypothesis_references:
                    raise EducationalInvariantViolation(
                        "constraint requires a hypothesis reference",
                        invariant="TeachingIntention.constraints.require_hypothesis",
                    )
            elif constraint.kind is IntentionConstraintKind.FORBID_MASTERY_CLAIM:
                lowered = (
                    f"{expected_outcome.statement} "
                    f"{expected_outcome.success_evidence}"
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
                        "constraint forbids mastery claim in expected outcome",
                        invariant="TeachingIntention.constraints.forbid_mastery",
                    )
            elif constraint.kind is IntentionConstraintKind.FORBID_STRATEGY_SELECTION:
                # Strategy selection is structurally outside this aggregate;
                # constraint records protective posture.
                continue
            elif constraint.kind is IntentionConstraintKind.REQUIRE_EVALUABLE_OUTCOME:
                if not expected_outcome.evaluable:
                    raise EducationalInvariantViolation(
                        "constraint requires evaluable expected outcome",
                        invariant="TeachingIntention.constraints.require_evaluable",
                    )
            elif constraint.kind is IntentionConstraintKind.PROTECT_ATOMICITY:
                # One primary intention type is enforced by aggregate identity.
                continue
            elif (
                constraint.kind
                is IntentionConstraintKind.PROTECT_CONCEPTUAL_HONESTY_OVER_EXAM
            ):
                diagnosis_types = {ref.diagnosis_type for ref in diagnosis_references}
                if (
                    intention_type is TeachingIntentionType.PREPARE_FOR_EXAMINATION
                    and DiagnosisType.MISCONCEPTION in diagnosis_types
                ):
                    raise EducationalInvariantViolation(
                        "exam preparation must not skip misconception repair",
                        invariant=(
                            "TeachingIntention.constraints.protect_conceptual_honesty"
                        ),
                    )
            elif constraint.kind is IntentionConstraintKind.CAP_STRENGTH:
                cap = constraint.max_strength
                if cap is not None and _STRENGTH_ORDER.index(
                    strength.level
                ) > _STRENGTH_ORDER.index(cap):
                    raise EducationalInvariantViolation(
                        "intention strength exceeds constraint cap",
                        invariant="TeachingIntention.constraints.cap_strength",
                    )
            elif constraint.kind is IntentionConstraintKind.FORBID_INTENTION_TYPE:
                forbidden = constraint.forbidden_intention_type
                if forbidden is not None and intention_type is forbidden:
                    raise EducationalInvariantViolation(
                        f"constraint forbids intention type {forbidden.value}",
                        invariant="TeachingIntention.constraints.forbid_type",
                    )

    @staticmethod
    def assert_retire_reason(reason: str | None) -> str | None:
        if reason is None:
            return None
        return require_non_empty_text(reason, "retire_reason")
