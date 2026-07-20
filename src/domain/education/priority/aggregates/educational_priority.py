"""EducationalPriority aggregate root — instructional ordering of educational work.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Educational Priority
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import PriorityId
from domain.education.priority.entities.priority_constraint import PriorityConstraint
from domain.education.priority.entities.priority_factor import PriorityFactor
from domain.education.priority.entities.priority_references import (
    DiagnosisReference,
    HypothesisReference,
)
from domain.education.priority.entities.priority_scope import PriorityScope
from domain.education.priority.enums import PriorityRevisionKind, PriorityStatus
from domain.education.priority.events.priority_assigned import PriorityAssigned
from domain.education.priority.events.priority_revised import PriorityRevised
from domain.education.priority.policies.priority_calculation_policy import (
    PriorityCalculationPolicy,
)
from domain.education.priority.policies.priority_validation_policy import (
    PriorityValidationPolicy,
)
from domain.education.priority.value_objects.instructional_impact import (
    InstructionalImpact,
)
from domain.education.priority.value_objects.priority_score import PriorityScore
from domain.education.priority.value_objects.urgency import Urgency

DomainEvent = PriorityAssigned | PriorityRevised


class EducationalPriority:
    """Aggregate root for educational priority.

    Owns diagnosis references, hypothesis references, priority factors,
    priority score, urgency, instructional impact, and constraints.
    Behaviour is exposed only through methods — no public setters.

    This aggregate answers *what the tutor should address first*. It does
    not diagnose, explain why a deficiency exists, or choose teaching
    strategies. Severity (learner condition) is never conflated with
    priority (instructional ordering).
    """

    def __init__(
        self,
        priority_id: PriorityId,
        student_id: str,
        scope: PriorityScope,
        diagnosis_references: list[DiagnosisReference]
        | tuple[DiagnosisReference, ...],
        hypothesis_references: list[HypothesisReference]
        | tuple[HypothesisReference, ...],
        factors: list[PriorityFactor] | tuple[PriorityFactor, ...],
        score: PriorityScore,
        urgency: Urgency,
        instructional_impact: InstructionalImpact,
        *,
        constraints: list[PriorityConstraint]
        | tuple[PriorityConstraint, ...]
        | None = None,
        status: PriorityStatus = PriorityStatus.ASSIGNED,
        stabilisation_reason: str | None = None,
        _record_assigned: bool = False,
    ) -> None:
        self._priority_id = PriorityValidationPolicy.assert_identity(priority_id)
        self._student_id = PriorityValidationPolicy.assert_student_id(student_id)
        self._scope = PriorityValidationPolicy.assert_scope(scope)
        self._diagnosis_references = list(
            PriorityValidationPolicy.assert_diagnosis_references(
                diagnosis_references
            )
        )
        self._hypothesis_references = list(
            PriorityValidationPolicy.assert_hypothesis_references(
                hypothesis_references
            )
        )
        self._factors = list(PriorityValidationPolicy.assert_factors(factors))
        PriorityValidationPolicy.assert_recalculable(self._factors)
        self._score = PriorityValidationPolicy.assert_score(score)
        self._urgency = PriorityValidationPolicy.assert_urgency(urgency)
        self._instructional_impact = (
            PriorityValidationPolicy.assert_instructional_impact(
                instructional_impact
            )
        )
        self._constraints = list(
            PriorityValidationPolicy.assert_constraints(constraints or ())
        )
        PriorityValidationPolicy.assert_constraints_satisfied(
            self._constraints,
            self._factors,
            self._score,
            self._urgency,
        )
        self._status = PriorityValidationPolicy.assert_status(status)
        self._stabilisation_reason = (
            PriorityValidationPolicy.assert_stabilisation_reason(
                stabilisation_reason
            )
        )

        self._pending_events: list[DomainEvent] = []
        if _record_assigned:
            self._pending_events.append(
                PriorityAssigned(
                    priority_id=self._priority_id,
                    student_id=self._student_id,
                    score_band=self._score.band,
                    urgency_level=self._urgency.level,
                    impact_level=self._instructional_impact.level,
                    factor_count=len(self._factors),
                    diagnosis_count=len(self._diagnosis_references),
                    hypothesis_count=len(self._hypothesis_references),
                )
            )

    @classmethod
    def assign(
        cls,
        priority_id: PriorityId,
        student_id: str,
        scope: PriorityScope,
        diagnosis_references: list[DiagnosisReference]
        | tuple[DiagnosisReference, ...],
        hypothesis_references: list[HypothesisReference]
        | tuple[HypothesisReference, ...],
        factors: list[PriorityFactor] | tuple[PriorityFactor, ...],
        *,
        constraints: list[PriorityConstraint]
        | tuple[PriorityConstraint, ...]
        | None = None,
        score: PriorityScore | None = None,
        urgency: Urgency | None = None,
        instructional_impact: InstructionalImpact | None = None,
        rationale: str | None = None,
    ) -> EducationalPriority:
        """Factory: assign instructional ordering from diagnosis and hypothesis.

        When score/urgency/impact are omitted, they are calculated from factors
        via PriorityCalculationPolicy so the priority remains recalculable.
        """
        validated_factors = PriorityValidationPolicy.assert_factors(factors)
        if score is None or urgency is None or instructional_impact is None:
            calculated_score, calculated_urgency, calculated_impact = (
                PriorityCalculationPolicy.calculate(
                    validated_factors,
                    rationale=rationale,
                )
            )
            score = score or calculated_score
            urgency = urgency or calculated_urgency
            instructional_impact = instructional_impact or calculated_impact

        return cls(
            priority_id=priority_id,
            student_id=student_id,
            scope=scope,
            diagnosis_references=diagnosis_references,
            hypothesis_references=hypothesis_references,
            factors=validated_factors,
            score=score,
            urgency=urgency,
            instructional_impact=instructional_impact,
            constraints=constraints,
            status=PriorityStatus.ASSIGNED,
            _record_assigned=True,
        )

    # --- identity / read models (no setters) ---

    @property
    def priority_id(self) -> PriorityId:
        return self._priority_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def scope(self) -> PriorityScope:
        return self._scope

    @property
    def diagnosis_references(self) -> tuple[DiagnosisReference, ...]:
        return tuple(self._diagnosis_references)

    @property
    def hypothesis_references(self) -> tuple[HypothesisReference, ...]:
        return tuple(self._hypothesis_references)

    @property
    def factors(self) -> tuple[PriorityFactor, ...]:
        return tuple(self._factors)

    @property
    def score(self) -> PriorityScore:
        return self._score

    @property
    def urgency(self) -> Urgency:
        return self._urgency

    @property
    def instructional_impact(self) -> InstructionalImpact:
        return self._instructional_impact

    @property
    def constraints(self) -> tuple[PriorityConstraint, ...]:
        return tuple(self._constraints)

    @property
    def status(self) -> PriorityStatus:
        return self._status

    @property
    def stabilisation_reason(self) -> str | None:
        return self._stabilisation_reason

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear pending domain events."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    # --- behaviour ---

    def recalculate(
        self,
        *,
        factors: list[PriorityFactor] | tuple[PriorityFactor, ...] | None = None,
        constraints: list[PriorityConstraint]
        | tuple[PriorityConstraint, ...]
        | None = None,
        rationale: str | None = None,
    ) -> None:
        """Recompute score, urgency, and impact from factors.

        Recalculation is always lawful — including from STABILISED — so that
        priority remains recalculable. Optional factor/constraint replacement
        is validated for duplicates and constraint contradictions.
        """
        PriorityValidationPolicy.assert_mutable(
            self._status, action="recalculate"
        )
        next_factors = (
            list(PriorityValidationPolicy.assert_factors(factors))
            if factors is not None
            else list(self._factors)
        )
        PriorityValidationPolicy.assert_recalculable(next_factors)
        next_constraints = (
            list(PriorityValidationPolicy.assert_constraints(constraints))
            if constraints is not None
            else list(self._constraints)
        )
        next_score, next_urgency, next_impact = PriorityCalculationPolicy.calculate(
            next_factors,
            rationale=rationale,
        )
        PriorityValidationPolicy.assert_constraints_satisfied(
            next_constraints,
            next_factors,
            next_score,
            next_urgency,
        )

        revision_kind = (
            PriorityRevisionKind.FACTORS_REPLACED
            if factors is not None
            else PriorityRevisionKind.RECALCULATED
        )
        self._factors = next_factors
        self._constraints = next_constraints
        self._score = next_score
        self._urgency = next_urgency
        self._instructional_impact = next_impact
        self._status = PriorityStatus.REVISED
        self._stabilisation_reason = None
        self._pending_events.append(
            PriorityRevised(
                priority_id=self._priority_id,
                student_id=self._student_id,
                score_band=self._score.band,
                urgency_level=self._urgency.level,
                impact_level=self._instructional_impact.level,
                revision_kind=revision_kind,
            )
        )

    def promote(self) -> None:
        """Raise instructional ordering by one band (not severity)."""
        PriorityValidationPolicy.assert_mutable(self._status, action="promote")
        next_score, next_urgency = PriorityCalculationPolicy.promote(
            self._score, self._urgency
        )
        PriorityValidationPolicy.assert_constraints_satisfied(
            self._constraints,
            self._factors,
            next_score,
            next_urgency,
        )
        self._score = next_score
        self._urgency = next_urgency
        self._status = PriorityStatus.REVISED
        self._pending_events.append(
            PriorityRevised(
                priority_id=self._priority_id,
                student_id=self._student_id,
                score_band=self._score.band,
                urgency_level=self._urgency.level,
                impact_level=self._instructional_impact.level,
                revision_kind=PriorityRevisionKind.PROMOTED,
            )
        )

    def demote(self) -> None:
        """Lower instructional ordering by one band (not severity)."""
        PriorityValidationPolicy.assert_mutable(self._status, action="demote")
        next_score, next_urgency = PriorityCalculationPolicy.demote(
            self._score, self._urgency
        )
        PriorityValidationPolicy.assert_constraints_satisfied(
            self._constraints,
            self._factors,
            next_score,
            next_urgency,
        )
        self._score = next_score
        self._urgency = next_urgency
        self._status = PriorityStatus.REVISED
        self._pending_events.append(
            PriorityRevised(
                priority_id=self._priority_id,
                student_id=self._student_id,
                score_band=self._score.band,
                urgency_level=self._urgency.level,
                impact_level=self._instructional_impact.level,
                revision_kind=PriorityRevisionKind.DEMOTED,
            )
        )

    def stabilise(self, reason: str | None = None) -> None:
        """Lock the current instructional ordering until recalculation."""
        PriorityValidationPolicy.assert_mutable(self._status, action="stabilise")
        PriorityValidationPolicy.assert_recalculable(self._factors)
        PriorityValidationPolicy.assert_constraints_satisfied(
            self._constraints,
            self._factors,
            self._score,
            self._urgency,
        )
        self._stabilisation_reason = (
            PriorityValidationPolicy.assert_stabilisation_reason(reason)
        )
        self._status = PriorityStatus.STABILISED
        self._pending_events.append(
            PriorityRevised(
                priority_id=self._priority_id,
                student_id=self._student_id,
                score_band=self._score.band,
                urgency_level=self._urgency.level,
                impact_level=self._instructional_impact.level,
                revision_kind=PriorityRevisionKind.STABILISED,
            )
        )

    # --- queries ---

    def is_assigned(self) -> bool:
        return self._status is PriorityStatus.ASSIGNED

    def is_revised(self) -> bool:
        return self._status is PriorityStatus.REVISED

    def is_stabilised(self) -> bool:
        return self._status is PriorityStatus.STABILISED

    def factor_count(self) -> int:
        return len(self._factors)

    def constraint_count(self) -> int:
        return len(self._constraints)

    def diagnosis_count(self) -> int:
        return len(self._diagnosis_references)

    def hypothesis_count(self) -> int:
        return len(self._hypothesis_references)

    def has_factor_kind(self, kind: object) -> bool:
        return any(factor.kind is kind for factor in self._factors)

    def has_diagnosis(self, diagnosis_id: object) -> bool:
        return any(
            ref.diagnosis_id == diagnosis_id for ref in self._diagnosis_references
        )

    def has_hypothesis(self, hypothesis_id: object) -> bool:
        return any(
            ref.hypothesis_id == hypothesis_id for ref in self._hypothesis_references
        )

    def peak_factor(self) -> PriorityFactor:
        """Return the factor with the highest ordering weight."""
        if not self._factors:
            raise EducationalInvariantViolation(
                "priority has no factors",
                invariant="EducationalPriority.peak_factor.empty",
            )
        return max(
            self._factors,
            key=PriorityCalculationPolicy.factor_ordering_weight,
        )

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, EducationalPriority):
            return NotImplemented
        return self._priority_id == other._priority_id

    def __hash__(self) -> int:
        return hash((type(self), self._priority_id))

    def __repr__(self) -> str:
        return (
            f"EducationalPriority(priority_id={self._priority_id!r}, "
            f"score={self._score.band!r}, status={self._status!r})"
        )
