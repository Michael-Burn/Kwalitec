"""TeachingIntention aggregate root — educational change sought next.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    Teaching Intention
"""

from __future__ import annotations

from domain.education.foundation.enums import TeachingIntentionType
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
    IntentionRevisionKind,
    IntentionStatus,
)
from domain.education.teaching_intention.events.intention_created import (
    TeachingIntentionCreated,
)
from domain.education.teaching_intention.events.intention_revised import (
    TeachingIntentionRevised,
)
from domain.education.teaching_intention.policies.intention_alignment_policy import (
    IntentionAlignmentPolicy,
)
from domain.education.teaching_intention.policies.intention_validation_policy import (
    IntentionValidationPolicy,
)
from domain.education.teaching_intention.value_objects.expected_outcome import (
    ExpectedOutcome,
)
from domain.education.teaching_intention.value_objects.intention_strength import (
    IntentionStrength,
)

DomainEvent = TeachingIntentionCreated | TeachingIntentionRevised


class TeachingIntention:
    """Aggregate root for teaching intention.

    Owns priority references, diagnosis references, hypothesis references,
    goal, expected educational outcome, instructional scope, constraints, and
    strength. Behaviour is exposed only through methods — no public setters.

    This aggregate answers *what educational change should happen next*. It
    does not choose teaching strategies, construct learning episodes, or
    orchestrate sessions.
    """

    def __init__(
        self,
        intention_id: TeachingIntentionId,
        student_id: str,
        intention_type: TeachingIntentionType,
        goal: IntentionGoal,
        scope: IntentionScope,
        expected_outcome: ExpectedOutcome,
        strength: IntentionStrength,
        priority_references: list[PriorityReference] | tuple[PriorityReference, ...],
        diagnosis_references: list[DiagnosisReference]
        | tuple[DiagnosisReference, ...],
        *,
        hypothesis_references: list[HypothesisReference]
        | tuple[HypothesisReference, ...]
        | None = None,
        constraints: list[IntentionConstraint]
        | tuple[IntentionConstraint, ...]
        | None = None,
        status: IntentionStatus = IntentionStatus.DRAFT,
        retire_reason: str | None = None,
        _record_created: bool = False,
    ) -> None:
        self._intention_id = IntentionValidationPolicy.assert_identity(intention_id)
        self._student_id = IntentionValidationPolicy.assert_student_id(student_id)
        self._intention_type = IntentionValidationPolicy.assert_intention_type(
            intention_type
        )
        self._goal = IntentionValidationPolicy.assert_goal(goal)
        IntentionValidationPolicy.assert_goal_matches_type(
            self._goal, self._intention_type
        )
        self._scope = IntentionValidationPolicy.assert_scope(scope)
        self._expected_outcome = IntentionValidationPolicy.assert_expected_outcome(
            expected_outcome
        )
        self._strength = IntentionValidationPolicy.assert_strength(strength)
        self._priority_references = list(
            IntentionValidationPolicy.assert_priority_references(priority_references)
        )
        self._diagnosis_references = list(
            IntentionValidationPolicy.assert_diagnosis_references(diagnosis_references)
        )
        self._hypothesis_references = list(
            IntentionValidationPolicy.assert_hypothesis_references(
                hypothesis_references or ()
            )
        )
        self._constraints = list(
            IntentionValidationPolicy.assert_constraints(constraints or ())
        )
        IntentionValidationPolicy.assert_constraints_satisfied(
            self._constraints,
            intention_type=self._intention_type,
            strength=self._strength,
            priority_references=self._priority_references,
            diagnosis_references=self._diagnosis_references,
            hypothesis_references=self._hypothesis_references,
            expected_outcome=self._expected_outcome,
        )
        IntentionAlignmentPolicy.assert_priority_not_contradicted(
            self._priority_references,
            self._diagnosis_references,
            self._intention_type,
        )
        self._status = IntentionValidationPolicy.assert_status(status)
        self._retire_reason = IntentionValidationPolicy.assert_retire_reason(
            retire_reason
        )

        self._pending_events: list[DomainEvent] = []
        if _record_created:
            self._pending_events.append(
                TeachingIntentionCreated(
                    intention_id=self._intention_id,
                    student_id=self._student_id,
                    intention_type=self._intention_type,
                    strength_level=self._strength.level,
                    priority_count=len(self._priority_references),
                    diagnosis_count=len(self._diagnosis_references),
                    hypothesis_count=len(self._hypothesis_references),
                )
            )

    @classmethod
    def create(
        cls,
        intention_id: TeachingIntentionId,
        student_id: str,
        intention_type: TeachingIntentionType,
        goal: IntentionGoal,
        scope: IntentionScope,
        expected_outcome: ExpectedOutcome,
        strength: IntentionStrength,
        priority_references: list[PriorityReference] | tuple[PriorityReference, ...],
        diagnosis_references: list[DiagnosisReference]
        | tuple[DiagnosisReference, ...],
        *,
        hypothesis_references: list[HypothesisReference]
        | tuple[HypothesisReference, ...]
        | None = None,
        constraints: list[IntentionConstraint]
        | tuple[IntentionConstraint, ...]
        | None = None,
    ) -> TeachingIntention:
        """Factory: create a draft teaching intention from Priority and Diagnosis."""
        return cls(
            intention_id=intention_id,
            student_id=student_id,
            intention_type=intention_type,
            goal=goal,
            scope=scope,
            expected_outcome=expected_outcome,
            strength=strength,
            priority_references=priority_references,
            diagnosis_references=diagnosis_references,
            hypothesis_references=hypothesis_references,
            constraints=constraints,
            status=IntentionStatus.DRAFT,
            _record_created=True,
        )

    # --- identity / read models (no setters) ---

    @property
    def intention_id(self) -> TeachingIntentionId:
        return self._intention_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def intention_type(self) -> TeachingIntentionType:
        return self._intention_type

    @property
    def goal(self) -> IntentionGoal:
        return self._goal

    @property
    def scope(self) -> IntentionScope:
        return self._scope

    @property
    def expected_outcome(self) -> ExpectedOutcome:
        return self._expected_outcome

    @property
    def strength(self) -> IntentionStrength:
        return self._strength

    @property
    def priority_references(self) -> tuple[PriorityReference, ...]:
        return tuple(self._priority_references)

    @property
    def diagnosis_references(self) -> tuple[DiagnosisReference, ...]:
        return tuple(self._diagnosis_references)

    @property
    def hypothesis_references(self) -> tuple[HypothesisReference, ...]:
        return tuple(self._hypothesis_references)

    @property
    def constraints(self) -> tuple[IntentionConstraint, ...]:
        return tuple(self._constraints)

    @property
    def status(self) -> IntentionStatus:
        return self._status

    @property
    def retire_reason(self) -> str | None:
        return self._retire_reason

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear pending domain events."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    # --- behaviour ---

    def activate(self) -> None:
        """Activate the intention, locking intention type."""
        IntentionValidationPolicy.assert_can_activate(self._status)
        IntentionValidationPolicy.assert_constraints_satisfied(
            self._constraints,
            intention_type=self._intention_type,
            strength=self._strength,
            priority_references=self._priority_references,
            diagnosis_references=self._diagnosis_references,
            hypothesis_references=self._hypothesis_references,
            expected_outcome=self._expected_outcome,
        )
        IntentionAlignmentPolicy.assert_priority_not_contradicted(
            self._priority_references,
            self._diagnosis_references,
            self._intention_type,
        )
        self._status = IntentionStatus.ACTIVE
        self._pending_events.append(
            TeachingIntentionRevised(
                intention_id=self._intention_id,
                student_id=self._student_id,
                intention_type=self._intention_type,
                strength_level=self._strength.level,
                revision_kind=IntentionRevisionKind.ACTIVATED,
            )
        )

    def revise(
        self,
        *,
        intention_type: TeachingIntentionType | None = None,
        goal: IntentionGoal | None = None,
        scope: IntentionScope | None = None,
        expected_outcome: ExpectedOutcome | None = None,
        strength: IntentionStrength | None = None,
        priority_references: list[PriorityReference]
        | tuple[PriorityReference, ...]
        | None = None,
        diagnosis_references: list[DiagnosisReference]
        | tuple[DiagnosisReference, ...]
        | None = None,
        hypothesis_references: list[HypothesisReference]
        | tuple[HypothesisReference, ...]
        | None = None,
        constraints: list[IntentionConstraint]
        | tuple[IntentionConstraint, ...]
        | None = None,
        revision_kind: IntentionRevisionKind | None = None,
    ) -> None:
        """Revise intention detail without selecting strategy or episodes."""
        IntentionValidationPolicy.assert_mutable(self._status, action="revise")

        next_type = (
            IntentionValidationPolicy.assert_intention_type(intention_type)
            if intention_type is not None
            else self._intention_type
        )
        IntentionValidationPolicy.assert_type_change_allowed(
            self._status, self._intention_type, next_type
        )

        next_goal = (
            IntentionValidationPolicy.assert_goal(goal)
            if goal is not None
            else self._goal
        )
        if goal is not None and intention_type is None:
            # Goal carries its own type; amend aggregate type only while draft.
            if next_goal.intention_type is not self._intention_type:
                IntentionValidationPolicy.assert_type_change_allowed(
                    self._status,
                    self._intention_type,
                    next_goal.intention_type,
                )
                next_type = next_goal.intention_type
        IntentionValidationPolicy.assert_goal_matches_type(next_goal, next_type)

        next_scope = (
            IntentionValidationPolicy.assert_scope(scope)
            if scope is not None
            else self._scope
        )
        next_outcome = (
            IntentionValidationPolicy.assert_expected_outcome(expected_outcome)
            if expected_outcome is not None
            else self._expected_outcome
        )
        next_strength = (
            IntentionValidationPolicy.assert_strength(strength)
            if strength is not None
            else self._strength
        )
        next_priorities = (
            list(
                IntentionValidationPolicy.assert_priority_references(
                    priority_references
                )
            )
            if priority_references is not None
            else list(self._priority_references)
        )
        next_diagnoses = (
            list(
                IntentionValidationPolicy.assert_diagnosis_references(
                    diagnosis_references
                )
            )
            if diagnosis_references is not None
            else list(self._diagnosis_references)
        )
        next_hypotheses = (
            list(
                IntentionValidationPolicy.assert_hypothesis_references(
                    hypothesis_references
                )
            )
            if hypothesis_references is not None
            else list(self._hypothesis_references)
        )
        next_constraints = (
            list(IntentionValidationPolicy.assert_constraints(constraints))
            if constraints is not None
            else list(self._constraints)
        )

        IntentionValidationPolicy.assert_constraints_satisfied(
            next_constraints,
            intention_type=next_type,
            strength=next_strength,
            priority_references=next_priorities,
            diagnosis_references=next_diagnoses,
            hypothesis_references=next_hypotheses,
            expected_outcome=next_outcome,
        )
        IntentionAlignmentPolicy.assert_priority_not_contradicted(
            next_priorities,
            next_diagnoses,
            next_type,
        )

        kind = revision_kind or self._infer_revision_kind(
            intention_type=intention_type,
            goal=goal,
            scope=scope,
            expected_outcome=expected_outcome,
            priority_references=priority_references,
            diagnosis_references=diagnosis_references,
            hypothesis_references=hypothesis_references,
            constraints=constraints,
        )

        self._intention_type = next_type
        self._goal = next_goal
        self._scope = next_scope
        self._expected_outcome = next_outcome
        self._strength = next_strength
        self._priority_references = next_priorities
        self._diagnosis_references = next_diagnoses
        self._hypothesis_references = next_hypotheses
        self._constraints = next_constraints
        if self._status is IntentionStatus.DRAFT:
            # Remain draft until activate(); revision of draft keeps DRAFT.
            self._status = IntentionStatus.DRAFT
        else:
            self._status = IntentionStatus.REVISED
        self._pending_events.append(
            TeachingIntentionRevised(
                intention_id=self._intention_id,
                student_id=self._student_id,
                intention_type=self._intention_type,
                strength_level=self._strength.level,
                revision_kind=kind,
            )
        )

    def strengthen(self) -> None:
        """Increase commitment strength of an activated intention."""
        IntentionValidationPolicy.assert_can_strengthen(self._status)
        next_strength = self._strength.strengthened()
        IntentionValidationPolicy.assert_constraints_satisfied(
            self._constraints,
            intention_type=self._intention_type,
            strength=next_strength,
            priority_references=self._priority_references,
            diagnosis_references=self._diagnosis_references,
            hypothesis_references=self._hypothesis_references,
            expected_outcome=self._expected_outcome,
        )
        self._strength = next_strength
        self._status = IntentionStatus.REVISED
        self._pending_events.append(
            TeachingIntentionRevised(
                intention_id=self._intention_id,
                student_id=self._student_id,
                intention_type=self._intention_type,
                strength_level=self._strength.level,
                revision_kind=IntentionRevisionKind.STRENGTHENED,
            )
        )

    def weaken(self) -> None:
        """Decrease commitment strength of an activated intention."""
        IntentionValidationPolicy.assert_can_weaken(self._status)
        next_strength = self._strength.weakened()
        IntentionValidationPolicy.assert_constraints_satisfied(
            self._constraints,
            intention_type=self._intention_type,
            strength=next_strength,
            priority_references=self._priority_references,
            diagnosis_references=self._diagnosis_references,
            hypothesis_references=self._hypothesis_references,
            expected_outcome=self._expected_outcome,
        )
        self._strength = next_strength
        self._status = IntentionStatus.REVISED
        self._pending_events.append(
            TeachingIntentionRevised(
                intention_id=self._intention_id,
                student_id=self._student_id,
                intention_type=self._intention_type,
                strength_level=self._strength.level,
                revision_kind=IntentionRevisionKind.WEAKENED,
            )
        )

    def retire(self, reason: str | None = None) -> None:
        """Retire the teaching intention (terminal)."""
        IntentionValidationPolicy.assert_can_retire(self._status)
        self._retire_reason = IntentionValidationPolicy.assert_retire_reason(reason)
        self._status = IntentionStatus.RETIRED
        self._pending_events.append(
            TeachingIntentionRevised(
                intention_id=self._intention_id,
                student_id=self._student_id,
                intention_type=self._intention_type,
                strength_level=self._strength.level,
                revision_kind=IntentionRevisionKind.RETIRED,
            )
        )

    # --- queries ---

    def is_draft(self) -> bool:
        return self._status is IntentionStatus.DRAFT

    def is_active(self) -> bool:
        return self._status is IntentionStatus.ACTIVE

    def is_revised(self) -> bool:
        return self._status is IntentionStatus.REVISED

    def is_retired(self) -> bool:
        return self._status is IntentionStatus.RETIRED

    def is_activated(self) -> bool:
        return self._status in {
            IntentionStatus.ACTIVE,
            IntentionStatus.REVISED,
        }

    def priority_count(self) -> int:
        return len(self._priority_references)

    def diagnosis_count(self) -> int:
        return len(self._diagnosis_references)

    def hypothesis_count(self) -> int:
        return len(self._hypothesis_references)

    def constraint_count(self) -> int:
        return len(self._constraints)

    def has_priority(self, priority_id: object) -> bool:
        return any(
            ref.priority_id == priority_id for ref in self._priority_references
        )

    def has_diagnosis(self, diagnosis_id: object) -> bool:
        return any(
            ref.diagnosis_id == diagnosis_id for ref in self._diagnosis_references
        )

    def has_hypothesis(self, hypothesis_id: object) -> bool:
        return any(
            ref.hypothesis_id == hypothesis_id for ref in self._hypothesis_references
        )

    @staticmethod
    def _infer_revision_kind(
        *,
        intention_type: TeachingIntentionType | None,
        goal: IntentionGoal | None,
        scope: IntentionScope | None,
        expected_outcome: ExpectedOutcome | None,
        priority_references: object,
        diagnosis_references: object,
        hypothesis_references: object,
        constraints: object,
    ) -> IntentionRevisionKind:
        if goal is not None and all(
            x is None
            for x in (
                intention_type,
                scope,
                expected_outcome,
                priority_references,
                diagnosis_references,
                hypothesis_references,
                constraints,
            )
        ):
            return IntentionRevisionKind.GOAL_AMENDED
        if expected_outcome is not None and all(
            x is None
            for x in (
                intention_type,
                goal,
                scope,
                priority_references,
                diagnosis_references,
                hypothesis_references,
                constraints,
            )
        ):
            return IntentionRevisionKind.OUTCOME_AMENDED
        if scope is not None and all(
            x is None
            for x in (
                intention_type,
                goal,
                expected_outcome,
                priority_references,
                diagnosis_references,
                hypothesis_references,
                constraints,
            )
        ):
            return IntentionRevisionKind.SCOPE_AMENDED
        if constraints is not None and all(
            x is None
            for x in (
                intention_type,
                goal,
                scope,
                expected_outcome,
                priority_references,
                diagnosis_references,
                hypothesis_references,
            )
        ):
            return IntentionRevisionKind.CONSTRAINTS_REPLACED
        if any(
            x is not None
            for x in (
                priority_references,
                diagnosis_references,
                hypothesis_references,
            )
        ) and all(
            x is None
            for x in (intention_type, goal, scope, expected_outcome, constraints)
        ):
            return IntentionRevisionKind.REFERENCES_UPDATED
        return IntentionRevisionKind.GENERAL

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, TeachingIntention):
            return NotImplemented
        return self._intention_id == other._intention_id

    def __hash__(self) -> int:
        return hash((type(self), self._intention_id))

    def __repr__(self) -> str:
        return (
            f"TeachingIntention(intention_id={self._intention_id!r}, "
            f"type={self._intention_type!r}, status={self._status!r})"
        )
