"""TeachingStrategy aggregate root — instructional approach commitment.

Architecture Source
    TEACHING_STRATEGY_ARCHITECTURE.md
    TEACHING_STRATEGY_CATALOGUE.md
    STRATEGY_COMPOSITION_MODEL.md
Concept
    Teaching Strategy
"""

from __future__ import annotations

from domain.education.foundation.enums import TeachingStrategyType
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
    CompositionPattern,
    StrategyRevisionKind,
    StrategyStatus,
)
from domain.education.teaching_strategy.events.strategy_revised import (
    TeachingStrategyRevised,
)
from domain.education.teaching_strategy.events.strategy_selected import (
    TeachingStrategySelected,
)
from domain.education.teaching_strategy.policies.strategy_composition_policy import (
    StrategyCompositionPolicy,
)
from domain.education.teaching_strategy.policies.strategy_validation_policy import (
    StrategyValidationPolicy,
)
from domain.education.teaching_strategy.value_objects.instructional_complexity import (
    InstructionalComplexity,
)
from domain.education.teaching_strategy.value_objects.strategy_effectiveness import (
    StrategyEffectiveness,
)

DomainEvent = TeachingStrategySelected | TeachingStrategyRevised


class TeachingStrategy:
    """Aggregate root for teaching strategy.

    Owns Teaching Intention references, Diagnosis references, Hypothesis
    references, selected primary strategy type, educational rationale,
    expected effectiveness, instructional complexity, secondary composition
    members, and constraints.

    Behaviour is exposed only through methods — no public setters.

    This aggregate answers *how the tutor intends to produce the desired
    educational change*. It does not enact learning episodes, score twins,
    or prescribe prompts/screens.
    """

    def __init__(
        self,
        strategy_id: TeachingStrategyId,
        student_id: str,
        primary_strategy: TeachingStrategyType,
        goal: StrategyGoal,
        rationale: StrategyRationale,
        effectiveness: StrategyEffectiveness,
        complexity: InstructionalComplexity,
        intention_references: list[IntentionReference]
        | tuple[IntentionReference, ...],
        diagnosis_references: list[DiagnosisReference]
        | tuple[DiagnosisReference, ...],
        *,
        hypothesis_references: list[HypothesisReference]
        | tuple[HypothesisReference, ...]
        | None = None,
        secondary_strategies: list[SecondaryStrategyReference]
        | tuple[SecondaryStrategyReference, ...]
        | None = None,
        constraints: list[StrategyConstraint]
        | tuple[StrategyConstraint, ...]
        | None = None,
        composition_pattern: CompositionPattern | None = None,
        status: StrategyStatus = StrategyStatus.DRAFT,
        retire_reason: str | None = None,
    ) -> None:
        self._strategy_id = StrategyValidationPolicy.assert_identity(strategy_id)
        self._student_id = StrategyValidationPolicy.assert_student_id(student_id)
        self._primary_strategy = StrategyValidationPolicy.assert_primary_strategy(
            primary_strategy
        )
        self._goal = StrategyValidationPolicy.assert_goal(goal)
        StrategyValidationPolicy.assert_goal_matches_primary(
            self._goal, self._primary_strategy
        )
        self._rationale = StrategyValidationPolicy.assert_rationale(rationale)
        self._effectiveness = StrategyValidationPolicy.assert_effectiveness(
            effectiveness
        )
        self._complexity = StrategyValidationPolicy.assert_complexity(complexity)
        self._intention_references = list(
            StrategyValidationPolicy.assert_intention_references(intention_references)
        )
        self._diagnosis_references = list(
            StrategyValidationPolicy.assert_diagnosis_references(diagnosis_references)
        )
        self._hypothesis_references = list(
            StrategyValidationPolicy.assert_hypothesis_references(
                hypothesis_references or ()
            )
        )
        self._secondary_strategies = list(
            StrategyValidationPolicy.assert_secondary_strategies(
                self._primary_strategy, secondary_strategies or ()
            )
        )
        self._constraints = list(
            StrategyValidationPolicy.assert_constraints(constraints or ())
        )
        self._composition_pattern = composition_pattern
        if self._composition_pattern is not None and not isinstance(
            self._composition_pattern, CompositionPattern
        ):
            from domain.education.foundation.errors import EducationalInvariantViolation

            raise EducationalInvariantViolation(
                "composition_pattern must be a CompositionPattern when provided",
                invariant="TeachingStrategy.composition_pattern.type",
            )
        StrategyValidationPolicy.assert_educational_integrity(
            primary=self._primary_strategy,
            intention_references=self._intention_references,
            diagnosis_references=self._diagnosis_references,
        )
        StrategyValidationPolicy.assert_constraints_satisfied(
            self._constraints,
            primary=self._primary_strategy,
            complexity=self._complexity,
            intention_references=self._intention_references,
            diagnosis_references=self._diagnosis_references,
            hypothesis_references=self._hypothesis_references,
            rationale=self._rationale,
            effectiveness=self._effectiveness,
            secondaries=self._secondary_strategies,
        )
        self._status = StrategyValidationPolicy.assert_status(status)
        self._retire_reason = StrategyValidationPolicy.assert_retire_reason(
            retire_reason
        )
        self._pending_events: list[DomainEvent] = []

    @classmethod
    def create(
        cls,
        strategy_id: TeachingStrategyId,
        student_id: str,
        primary_strategy: TeachingStrategyType,
        goal: StrategyGoal,
        rationale: StrategyRationale,
        effectiveness: StrategyEffectiveness,
        complexity: InstructionalComplexity,
        intention_references: list[IntentionReference]
        | tuple[IntentionReference, ...],
        diagnosis_references: list[DiagnosisReference]
        | tuple[DiagnosisReference, ...],
        *,
        hypothesis_references: list[HypothesisReference]
        | tuple[HypothesisReference, ...]
        | None = None,
        secondary_strategies: list[SecondaryStrategyReference]
        | tuple[SecondaryStrategyReference, ...]
        | None = None,
        constraints: list[StrategyConstraint]
        | tuple[StrategyConstraint, ...]
        | None = None,
        composition_pattern: CompositionPattern | None = None,
    ) -> TeachingStrategy:
        """Factory: create a draft teaching strategy from Teaching Intention."""
        return cls(
            strategy_id=strategy_id,
            student_id=student_id,
            primary_strategy=primary_strategy,
            goal=goal,
            rationale=rationale,
            effectiveness=effectiveness,
            complexity=complexity,
            intention_references=intention_references,
            diagnosis_references=diagnosis_references,
            hypothesis_references=hypothesis_references,
            secondary_strategies=secondary_strategies,
            constraints=constraints,
            composition_pattern=composition_pattern,
            status=StrategyStatus.DRAFT,
        )

    # --- identity / read models (no setters) ---

    @property
    def strategy_id(self) -> TeachingStrategyId:
        return self._strategy_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def primary_strategy(self) -> TeachingStrategyType:
        return self._primary_strategy

    @property
    def goal(self) -> StrategyGoal:
        return self._goal

    @property
    def rationale(self) -> StrategyRationale:
        return self._rationale

    @property
    def effectiveness(self) -> StrategyEffectiveness:
        return self._effectiveness

    @property
    def complexity(self) -> InstructionalComplexity:
        return self._complexity

    @property
    def intention_references(self) -> tuple[IntentionReference, ...]:
        return tuple(self._intention_references)

    @property
    def diagnosis_references(self) -> tuple[DiagnosisReference, ...]:
        return tuple(self._diagnosis_references)

    @property
    def hypothesis_references(self) -> tuple[HypothesisReference, ...]:
        return tuple(self._hypothesis_references)

    @property
    def secondary_strategies(self) -> tuple[SecondaryStrategyReference, ...]:
        return tuple(self._secondary_strategies)

    @property
    def constraints(self) -> tuple[StrategyConstraint, ...]:
        return tuple(self._constraints)

    @property
    def composition_pattern(self) -> CompositionPattern | None:
        return self._composition_pattern

    @property
    def status(self) -> StrategyStatus:
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

    def select(self) -> None:
        """Commit the draft strategy as the selected instructional approach."""
        StrategyValidationPolicy.assert_can_select(self._status)
        StrategyValidationPolicy.assert_educational_integrity(
            primary=self._primary_strategy,
            intention_references=self._intention_references,
            diagnosis_references=self._diagnosis_references,
        )
        StrategyValidationPolicy.assert_constraints_satisfied(
            self._constraints,
            primary=self._primary_strategy,
            complexity=self._complexity,
            intention_references=self._intention_references,
            diagnosis_references=self._diagnosis_references,
            hypothesis_references=self._hypothesis_references,
            rationale=self._rationale,
            effectiveness=self._effectiveness,
            secondaries=self._secondary_strategies,
        )
        self._status = StrategyStatus.SELECTED
        self._pending_events.append(
            TeachingStrategySelected(
                strategy_id=self._strategy_id,
                student_id=self._student_id,
                primary_strategy=self._primary_strategy,
                effectiveness_level=self._effectiveness.level,
                intention_count=len(self._intention_references),
                diagnosis_count=len(self._diagnosis_references),
                hypothesis_count=len(self._hypothesis_references),
                secondary_count=len(self._secondary_strategies),
            )
        )

    def revise(
        self,
        *,
        primary_strategy: TeachingStrategyType | None = None,
        goal: StrategyGoal | None = None,
        rationale: StrategyRationale | None = None,
        effectiveness: StrategyEffectiveness | None = None,
        complexity: InstructionalComplexity | None = None,
        intention_references: list[IntentionReference]
        | tuple[IntentionReference, ...]
        | None = None,
        diagnosis_references: list[DiagnosisReference]
        | tuple[DiagnosisReference, ...]
        | None = None,
        hypothesis_references: list[HypothesisReference]
        | tuple[HypothesisReference, ...]
        | None = None,
        secondary_strategies: list[SecondaryStrategyReference]
        | tuple[SecondaryStrategyReference, ...]
        | None = None,
        constraints: list[StrategyConstraint]
        | tuple[StrategyConstraint, ...]
        | None = None,
        composition_pattern: CompositionPattern | None = None,
        revision_kind: StrategyRevisionKind | None = None,
    ) -> None:
        """Revise strategy detail without enacting episodes."""
        StrategyValidationPolicy.assert_mutable(self._status, action="revise")

        next_primary = (
            StrategyValidationPolicy.assert_primary_strategy(primary_strategy)
            if primary_strategy is not None
            else self._primary_strategy
        )
        StrategyValidationPolicy.assert_primary_change_allowed(
            self._status, self._primary_strategy, next_primary
        )

        next_goal = (
            StrategyValidationPolicy.assert_goal(goal)
            if goal is not None
            else self._goal
        )
        if goal is not None and primary_strategy is None:
            if next_goal.strategy_type is not self._primary_strategy:
                StrategyValidationPolicy.assert_primary_change_allowed(
                    self._status,
                    self._primary_strategy,
                    next_goal.strategy_type,
                )
                next_primary = next_goal.strategy_type
        StrategyValidationPolicy.assert_goal_matches_primary(next_goal, next_primary)

        next_rationale = (
            StrategyValidationPolicy.assert_rationale(rationale)
            if rationale is not None
            else self._rationale
        )
        next_effectiveness = (
            StrategyValidationPolicy.assert_effectiveness(effectiveness)
            if effectiveness is not None
            else self._effectiveness
        )
        next_complexity = (
            StrategyValidationPolicy.assert_complexity(complexity)
            if complexity is not None
            else self._complexity
        )
        next_intentions = (
            list(
                StrategyValidationPolicy.assert_intention_references(
                    intention_references
                )
            )
            if intention_references is not None
            else list(self._intention_references)
        )
        next_diagnoses = (
            list(
                StrategyValidationPolicy.assert_diagnosis_references(
                    diagnosis_references
                )
            )
            if diagnosis_references is not None
            else list(self._diagnosis_references)
        )
        next_hypotheses = (
            list(
                StrategyValidationPolicy.assert_hypothesis_references(
                    hypothesis_references
                )
            )
            if hypothesis_references is not None
            else list(self._hypothesis_references)
        )
        next_secondaries = (
            list(
                StrategyValidationPolicy.assert_secondary_strategies(
                    next_primary, secondary_strategies
                )
            )
            if secondary_strategies is not None
            else list(self._secondary_strategies)
        )
        next_constraints = (
            list(StrategyValidationPolicy.assert_constraints(constraints))
            if constraints is not None
            else list(self._constraints)
        )
        next_pattern = (
            composition_pattern
            if composition_pattern is not None
            else self._composition_pattern
        )

        StrategyValidationPolicy.assert_educational_integrity(
            primary=next_primary,
            intention_references=next_intentions,
            diagnosis_references=next_diagnoses,
        )
        StrategyValidationPolicy.assert_constraints_satisfied(
            next_constraints,
            primary=next_primary,
            complexity=next_complexity,
            intention_references=next_intentions,
            diagnosis_references=next_diagnoses,
            hypothesis_references=next_hypotheses,
            rationale=next_rationale,
            effectiveness=next_effectiveness,
            secondaries=next_secondaries,
        )

        kind = revision_kind or self._infer_revision_kind(
            primary_strategy=primary_strategy,
            goal=goal,
            rationale=rationale,
            effectiveness=effectiveness,
            complexity=complexity,
            intention_references=intention_references,
            diagnosis_references=diagnosis_references,
            hypothesis_references=hypothesis_references,
            secondary_strategies=secondary_strategies,
            constraints=constraints,
        )

        self._primary_strategy = next_primary
        self._goal = next_goal
        self._rationale = next_rationale
        self._effectiveness = next_effectiveness
        self._complexity = next_complexity
        self._intention_references = next_intentions
        self._diagnosis_references = next_diagnoses
        self._hypothesis_references = next_hypotheses
        self._secondary_strategies = next_secondaries
        self._constraints = next_constraints
        self._composition_pattern = next_pattern
        if self._status is StrategyStatus.DRAFT:
            self._status = StrategyStatus.DRAFT
        else:
            self._status = StrategyStatus.REVISED
        self._pending_events.append(
            TeachingStrategyRevised(
                strategy_id=self._strategy_id,
                student_id=self._student_id,
                primary_strategy=self._primary_strategy,
                effectiveness_level=self._effectiveness.level,
                revision_kind=kind,
                secondary_count=len(self._secondary_strategies),
            )
        )

    def compose(
        self,
        secondary_types: list[TeachingStrategyType]
        | tuple[TeachingStrategyType, ...],
        *,
        composition_pattern: CompositionPattern | None = None,
    ) -> None:
        """Attach ordered secondary strategies under composition rules."""
        StrategyValidationPolicy.assert_mutable(self._status, action="compose")
        refs = StrategyCompositionPolicy.assert_compose_types(
            self._primary_strategy, secondary_types
        )
        StrategyCompositionPolicy.assert_no_coequal_primaries(
            self._primary_strategy, refs
        )
        pattern = composition_pattern
        if pattern is None:
            pattern = StrategyCompositionPolicy.matches_canonical_prefix(
                self._primary_strategy,
                [ref.strategy_type for ref in refs],
            )
        StrategyValidationPolicy.assert_constraints_satisfied(
            self._constraints,
            primary=self._primary_strategy,
            complexity=self._complexity,
            intention_references=self._intention_references,
            diagnosis_references=self._diagnosis_references,
            hypothesis_references=self._hypothesis_references,
            rationale=self._rationale,
            effectiveness=self._effectiveness,
            secondaries=refs,
        )
        self._secondary_strategies = list(refs)
        self._composition_pattern = pattern
        if self._status is not StrategyStatus.DRAFT:
            self._status = StrategyStatus.REVISED
        self._pending_events.append(
            TeachingStrategyRevised(
                strategy_id=self._strategy_id,
                student_id=self._student_id,
                primary_strategy=self._primary_strategy,
                effectiveness_level=self._effectiveness.level,
                revision_kind=StrategyRevisionKind.SECONDARIES_COMPOSED,
                secondary_count=len(self._secondary_strategies),
            )
        )

    def decompose(
        self,
        *,
        remove_strategy: TeachingStrategyType | None = None,
    ) -> None:
        """Remove secondary composition members (all, or one named type)."""
        StrategyValidationPolicy.assert_mutable(self._status, action="decompose")
        if not self._secondary_strategies:
            from domain.education.foundation.errors import EducationalInvariantViolation

            raise EducationalInvariantViolation(
                "cannot decompose a strategy with no secondary composition",
                invariant="TeachingStrategy.decompose.empty",
            )
        if remove_strategy is None:
            remaining: list[SecondaryStrategyReference] = []
        else:
            remaining = [
                ref
                for ref in self._secondary_strategies
                if ref.strategy_type is not remove_strategy
            ]
            if len(remaining) == len(self._secondary_strategies):
                from domain.education.foundation.errors import (
                    EducationalInvariantViolation,
                )

                raise EducationalInvariantViolation(
                    f"secondary strategy {remove_strategy.value} is not composed",
                    invariant="TeachingStrategy.decompose.missing",
                )
            remaining = list(
                StrategyCompositionPolicy.assert_compose_types(
                    self._primary_strategy,
                    [ref.strategy_type for ref in remaining],
                )
            )
        self._secondary_strategies = remaining
        self._composition_pattern = (
            StrategyCompositionPolicy.matches_canonical_prefix(
                self._primary_strategy,
                [ref.strategy_type for ref in remaining],
            )
            if remaining
            else None
        )
        if self._status is not StrategyStatus.DRAFT:
            self._status = StrategyStatus.REVISED
        self._pending_events.append(
            TeachingStrategyRevised(
                strategy_id=self._strategy_id,
                student_id=self._student_id,
                primary_strategy=self._primary_strategy,
                effectiveness_level=self._effectiveness.level,
                revision_kind=StrategyRevisionKind.SECONDARIES_DECOMPOSED,
                secondary_count=len(self._secondary_strategies),
            )
        )

    def retire(self, reason: str | None = None) -> None:
        """Retire the teaching strategy (terminal)."""
        StrategyValidationPolicy.assert_can_retire(self._status)
        self._retire_reason = StrategyValidationPolicy.assert_retire_reason(reason)
        self._status = StrategyStatus.RETIRED
        self._pending_events.append(
            TeachingStrategyRevised(
                strategy_id=self._strategy_id,
                student_id=self._student_id,
                primary_strategy=self._primary_strategy,
                effectiveness_level=self._effectiveness.level,
                revision_kind=StrategyRevisionKind.RETIRED,
                secondary_count=len(self._secondary_strategies),
            )
        )

    # --- queries ---

    def is_draft(self) -> bool:
        return self._status is StrategyStatus.DRAFT

    def is_selected(self) -> bool:
        return self._status is StrategyStatus.SELECTED

    def is_revised(self) -> bool:
        return self._status is StrategyStatus.REVISED

    def is_retired(self) -> bool:
        return self._status is StrategyStatus.RETIRED

    def is_committed(self) -> bool:
        return self._status in {
            StrategyStatus.SELECTED,
            StrategyStatus.REVISED,
        }

    def intention_count(self) -> int:
        return len(self._intention_references)

    def diagnosis_count(self) -> int:
        return len(self._diagnosis_references)

    def hypothesis_count(self) -> int:
        return len(self._hypothesis_references)

    def secondary_count(self) -> int:
        return len(self._secondary_strategies)

    def constraint_count(self) -> int:
        return len(self._constraints)

    def has_intention(self, intention_id: object) -> bool:
        return any(
            ref.intention_id == intention_id for ref in self._intention_references
        )

    def has_diagnosis(self, diagnosis_id: object) -> bool:
        return any(
            ref.diagnosis_id == diagnosis_id for ref in self._diagnosis_references
        )

    def has_hypothesis(self, hypothesis_id: object) -> bool:
        return any(
            ref.hypothesis_id == hypothesis_id for ref in self._hypothesis_references
        )

    def has_secondary(self, strategy_type: TeachingStrategyType) -> bool:
        return any(
            ref.strategy_type is strategy_type for ref in self._secondary_strategies
        )

    def composition_sequence(self) -> tuple[TeachingStrategyType, ...]:
        return (
            self._primary_strategy,
            *(ref.strategy_type for ref in self._secondary_strategies),
        )

    @staticmethod
    def _infer_revision_kind(
        *,
        primary_strategy: TeachingStrategyType | None,
        goal: StrategyGoal | None,
        rationale: StrategyRationale | None,
        effectiveness: StrategyEffectiveness | None,
        complexity: InstructionalComplexity | None,
        intention_references: object,
        diagnosis_references: object,
        hypothesis_references: object,
        secondary_strategies: object,
        constraints: object,
    ) -> StrategyRevisionKind:
        if primary_strategy is not None and all(
            x is None
            for x in (
                goal,
                rationale,
                effectiveness,
                complexity,
                intention_references,
                diagnosis_references,
                hypothesis_references,
                secondary_strategies,
                constraints,
            )
        ):
            return StrategyRevisionKind.PRIMARY_CHANGED
        if secondary_strategies is not None and all(
            x is None
            for x in (
                primary_strategy,
                goal,
                rationale,
                effectiveness,
                complexity,
                intention_references,
                diagnosis_references,
                hypothesis_references,
                constraints,
            )
        ):
            return StrategyRevisionKind.SECONDARIES_COMPOSED
        if rationale is not None and all(
            x is None
            for x in (
                primary_strategy,
                goal,
                effectiveness,
                complexity,
                intention_references,
                diagnosis_references,
                hypothesis_references,
                secondary_strategies,
                constraints,
            )
        ):
            return StrategyRevisionKind.RATIONALE_AMENDED
        if effectiveness is not None and all(
            x is None
            for x in (
                primary_strategy,
                goal,
                rationale,
                complexity,
                intention_references,
                diagnosis_references,
                hypothesis_references,
                secondary_strategies,
                constraints,
            )
        ):
            return StrategyRevisionKind.EFFECTIVENESS_AMENDED
        if goal is not None and all(
            x is None
            for x in (
                primary_strategy,
                rationale,
                effectiveness,
                complexity,
                intention_references,
                diagnosis_references,
                hypothesis_references,
                secondary_strategies,
                constraints,
            )
        ):
            return StrategyRevisionKind.GOAL_AMENDED
        if complexity is not None and all(
            x is None
            for x in (
                primary_strategy,
                goal,
                rationale,
                effectiveness,
                intention_references,
                diagnosis_references,
                hypothesis_references,
                secondary_strategies,
                constraints,
            )
        ):
            return StrategyRevisionKind.COMPLEXITY_AMENDED
        if constraints is not None and all(
            x is None
            for x in (
                primary_strategy,
                goal,
                rationale,
                effectiveness,
                complexity,
                intention_references,
                diagnosis_references,
                hypothesis_references,
                secondary_strategies,
            )
        ):
            return StrategyRevisionKind.CONSTRAINTS_REPLACED
        if any(
            x is not None
            for x in (
                intention_references,
                diagnosis_references,
                hypothesis_references,
            )
        ) and all(
            x is None
            for x in (
                primary_strategy,
                goal,
                rationale,
                effectiveness,
                complexity,
                secondary_strategies,
                constraints,
            )
        ):
            return StrategyRevisionKind.REFERENCES_UPDATED
        return StrategyRevisionKind.GENERAL

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, TeachingStrategy):
            return NotImplemented
        return self._strategy_id == other._strategy_id

    def __hash__(self) -> int:
        return hash((type(self), self._strategy_id))

    def __repr__(self) -> str:
        return (
            f"TeachingStrategy(strategy_id={self._strategy_id!r}, "
            f"primary={self._primary_strategy!r}, status={self._status!r})"
        )
