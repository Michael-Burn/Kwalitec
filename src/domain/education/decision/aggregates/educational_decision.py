"""EducationalDecision aggregate root — readiness to execute a planned intervention.

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
    EDUCATIONAL_ORCHESTRATION_MODEL.md
Concept
    Educational Decision
"""

from __future__ import annotations

from domain.education.decision.entities.decision_reason import DecisionReason
from domain.education.decision.entities.decision_references import (
    IntentionReference,
    PriorityReference,
    StrategyReference,
)
from domain.education.decision.entities.execution_constraint import ExecutionConstraint
from domain.education.decision.entities.readiness_indicator import ReadinessIndicator
from domain.education.decision.enums import (
    DecisionOutcome,
    DecisionRevisionKind,
    DecisionStatus,
)
from domain.education.decision.events.decision_made import DecisionMade
from domain.education.decision.events.decision_reconsidered import DecisionReconsidered
from domain.education.decision.policies.decision_policy import DecisionPolicy
from domain.education.decision.policies.readiness_policy import ReadinessPolicy
from domain.education.decision.value_objects.decision_confidence import (
    DecisionConfidence,
)
from domain.education.decision.value_objects.readiness_level import ReadinessLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DecisionId

DomainEvent = DecisionMade | DecisionReconsidered


class EducationalDecision:
    """Aggregate root for educational execution decisions.

    Owns Priority references, Teaching Intention references, Teaching Strategy
    references, readiness indicators, execution constraints, decision
    confidence, and readiness level.

    Behaviour is exposed only through methods — no public setters.

    This aggregate answers whether a planned educational intervention should
    proceed *now*. It does not create strategies, diagnose deficiencies, or
    orchestrate sessions.
    """

    def __init__(
        self,
        decision_id: DecisionId,
        student_id: str,
        priority_references: list[PriorityReference] | tuple[PriorityReference, ...],
        intention_references: list[IntentionReference]
        | tuple[IntentionReference, ...],
        strategy_references: list[StrategyReference] | tuple[StrategyReference, ...],
        indicators: list[ReadinessIndicator] | tuple[ReadinessIndicator, ...],
        confidence: DecisionConfidence,
        readiness: ReadinessLevel,
        *,
        constraints: list[ExecutionConstraint]
        | tuple[ExecutionConstraint, ...]
        | None = None,
        reasons: list[DecisionReason] | tuple[DecisionReason, ...] | None = None,
        status: DecisionStatus = DecisionStatus.PENDING,
        outcome: DecisionOutcome | None = None,
        reconsideration_reason: str | None = None,
        _record_created: bool = False,
    ) -> None:
        self._decision_id = DecisionPolicy.assert_identity(decision_id)
        self._student_id = DecisionPolicy.assert_student_id(student_id)
        self._priority_references = list(
            DecisionPolicy.assert_priority_references(priority_references)
        )
        self._intention_references = list(
            DecisionPolicy.assert_intention_references(intention_references)
        )
        self._strategy_references = list(
            DecisionPolicy.assert_strategy_references(strategy_references)
        )
        self._indicators = list(DecisionPolicy.assert_indicators(indicators))
        self._confidence = DecisionPolicy.assert_confidence(confidence)
        self._readiness = DecisionPolicy.assert_readiness(readiness)
        ReadinessPolicy.assert_consistent_with_indicators(
            self._readiness, self._indicators
        )
        self._constraints = list(
            DecisionPolicy.assert_constraints(constraints or ())
        )
        DecisionPolicy.assert_constraints_satisfied(
            self._constraints,
            indicators=self._indicators,
            readiness=self._readiness,
            confidence=self._confidence,
            outcome=outcome,
            approving=False,
        )
        self._reasons = list(DecisionPolicy.assert_reasons(reasons or ()))
        self._status = DecisionPolicy.assert_status(status)
        self._outcome = DecisionPolicy.assert_outcome(outcome)
        self._reconsideration_reason = (
            DecisionPolicy.assert_reconsideration_reason(reconsideration_reason)
            if reconsideration_reason is not None
            else None
        )
        self._pending_events: list[DomainEvent] = []
        if _record_created:
            # Creation establishes an evaluated pending posture; commitment
            # events fire on approve/delay/reject.
            pass

    @classmethod
    def create(
        cls,
        decision_id: DecisionId,
        student_id: str,
        priority_references: list[PriorityReference] | tuple[PriorityReference, ...],
        intention_references: list[IntentionReference]
        | tuple[IntentionReference, ...],
        strategy_references: list[StrategyReference] | tuple[StrategyReference, ...],
        indicators: list[ReadinessIndicator] | tuple[ReadinessIndicator, ...],
        confidence: DecisionConfidence,
        *,
        readiness: ReadinessLevel | None = None,
        constraints: list[ExecutionConstraint]
        | tuple[ExecutionConstraint, ...]
        | None = None,
        reasons: list[DecisionReason] | tuple[DecisionReason, ...] | None = None,
        rationale: str | None = None,
    ) -> EducationalDecision:
        """Factory: evaluate readiness for a planned educational intervention.

        When readiness is omitted, ReadinessPolicy derives it from indicators
        so the decision remains recalculable from its readiness signals.
        """
        validated_indicators = DecisionPolicy.assert_indicators(indicators)
        resolved_readiness = readiness or ReadinessPolicy.assess(
            validated_indicators,
            rationale=rationale,
        )
        return cls(
            decision_id=decision_id,
            student_id=student_id,
            priority_references=priority_references,
            intention_references=intention_references,
            strategy_references=strategy_references,
            indicators=validated_indicators,
            confidence=confidence,
            readiness=resolved_readiness,
            constraints=constraints,
            reasons=reasons,
            status=DecisionStatus.PENDING,
            outcome=None,
            _record_created=True,
        )

    # --- identity / read models (no setters) ---

    @property
    def decision_id(self) -> DecisionId:
        return self._decision_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def priority_references(self) -> tuple[PriorityReference, ...]:
        return tuple(self._priority_references)

    @property
    def intention_references(self) -> tuple[IntentionReference, ...]:
        return tuple(self._intention_references)

    @property
    def strategy_references(self) -> tuple[StrategyReference, ...]:
        return tuple(self._strategy_references)

    @property
    def indicators(self) -> tuple[ReadinessIndicator, ...]:
        return tuple(self._indicators)

    @property
    def constraints(self) -> tuple[ExecutionConstraint, ...]:
        return tuple(self._constraints)

    @property
    def reasons(self) -> tuple[DecisionReason, ...]:
        return tuple(self._reasons)

    @property
    def confidence(self) -> DecisionConfidence:
        return self._confidence

    @property
    def readiness(self) -> ReadinessLevel:
        return self._readiness

    @property
    def status(self) -> DecisionStatus:
        return self._status

    @property
    def outcome(self) -> DecisionOutcome | None:
        return self._outcome

    @property
    def reconsideration_reason(self) -> str | None:
        return self._reconsideration_reason

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear pending domain events."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    # --- behaviour ---

    def approve(
        self,
        *,
        reasons: list[DecisionReason] | tuple[DecisionReason, ...] | None = None,
    ) -> None:
        """Approve teaching now when readiness and constraints permit."""
        DecisionPolicy.assert_mutable(self._status, action="approve")
        DecisionPolicy.assert_approval_lawful(
            readiness=self._readiness,
            confidence=self._confidence,
            indicators=self._indicators,
            constraints=self._constraints,
        )
        next_reasons = (
            list(DecisionPolicy.assert_reasons(reasons))
            if reasons is not None
            else list(self._reasons)
        )
        self._reasons = next_reasons
        self._outcome = DecisionOutcome.TEACH_NOW
        self._status = DecisionPolicy.status_for_approval()
        self._reconsideration_reason = None
        self._pending_events.append(self._make_decision_made_event())

    def delay(
        self,
        outcome: DecisionOutcome = DecisionOutcome.DELAY,
        *,
        reasons: list[DecisionReason] | tuple[DecisionReason, ...] | None = None,
    ) -> None:
        """Delay execution; outcome must be a non-teach deferral."""
        DecisionPolicy.assert_mutable(self._status, action="delay")
        resolved = DecisionPolicy.assert_deferral_outcome(outcome)
        DecisionPolicy.assert_constraints_satisfied(
            self._constraints,
            indicators=self._indicators,
            readiness=self._readiness,
            confidence=self._confidence,
            outcome=resolved,
            approving=False,
        )
        next_reasons = (
            list(DecisionPolicy.assert_reasons(reasons))
            if reasons is not None
            else list(self._reasons)
        )
        self._reasons = next_reasons
        self._outcome = resolved
        self._status = DecisionPolicy.status_for_delay()
        self._reconsideration_reason = None
        self._pending_events.append(self._make_decision_made_event())

    def reject(
        self,
        outcome: DecisionOutcome = DecisionOutcome.DELAY,
        *,
        reasons: list[DecisionReason] | tuple[DecisionReason, ...] | None = None,
    ) -> None:
        """Reject execution now; outcome must be a non-teach deferral class."""
        DecisionPolicy.assert_mutable(self._status, action="reject")
        resolved = DecisionPolicy.assert_rejection_outcome(outcome)
        DecisionPolicy.assert_constraints_satisfied(
            self._constraints,
            indicators=self._indicators,
            readiness=self._readiness,
            confidence=self._confidence,
            outcome=resolved,
            approving=False,
        )
        next_reasons = (
            list(DecisionPolicy.assert_reasons(reasons))
            if reasons is not None
            else list(self._reasons)
        )
        self._reasons = next_reasons
        self._outcome = resolved
        self._status = DecisionPolicy.status_for_rejection()
        self._reconsideration_reason = None
        self._pending_events.append(self._make_decision_made_event())

    def reconsider(
        self,
        reason: str,
        *,
        indicators: list[ReadinessIndicator]
        | tuple[ReadinessIndicator, ...]
        | None = None,
        constraints: list[ExecutionConstraint]
        | tuple[ExecutionConstraint, ...]
        | None = None,
        confidence: DecisionConfidence | None = None,
        readiness: ReadinessLevel | None = None,
        rationale: str | None = None,
    ) -> None:
        """Reopen a committed decision for fresh readiness evaluation."""
        DecisionPolicy.assert_reconsiderable(self._status)
        if self._outcome is None:
            raise EducationalInvariantViolation(
                "committed decision must possess an outcome to reconsider",
                invariant="EducationalDecision.reconsider.outcome.required",
            )
        previous_outcome = self._outcome
        previous_status = self._status
        reconsideration_reason = DecisionPolicy.assert_reconsideration_reason(reason)

        next_indicators = (
            list(DecisionPolicy.assert_indicators(indicators))
            if indicators is not None
            else list(self._indicators)
        )
        next_constraints = (
            list(DecisionPolicy.assert_constraints(constraints))
            if constraints is not None
            else list(self._constraints)
        )
        next_confidence = (
            DecisionPolicy.assert_confidence(confidence)
            if confidence is not None
            else self._confidence
        )
        if readiness is not None:
            next_readiness = DecisionPolicy.assert_readiness(readiness)
        elif indicators is not None:
            next_readiness = ReadinessPolicy.assess(
                next_indicators,
                rationale=rationale,
            )
        else:
            next_readiness = self._readiness

        ReadinessPolicy.assert_consistent_with_indicators(
            next_readiness, next_indicators
        )
        DecisionPolicy.assert_constraints_satisfied(
            next_constraints,
            indicators=next_indicators,
            readiness=next_readiness,
            confidence=next_confidence,
            outcome=None,
            approving=False,
        )

        self._indicators = next_indicators
        self._constraints = next_constraints
        self._confidence = next_confidence
        self._readiness = next_readiness
        self._outcome = None
        self._status = DecisionStatus.RECONSIDERED
        self._reconsideration_reason = reconsideration_reason
        self._pending_events.append(
            DecisionReconsidered(
                decision_id=self._decision_id,
                student_id=self._student_id,
                previous_outcome=previous_outcome,
                previous_status=previous_status,
                reason=reconsideration_reason,
            )
        )

    def refresh_readiness(
        self,
        *,
        indicators: list[ReadinessIndicator]
        | tuple[ReadinessIndicator, ...]
        | None = None,
        rationale: str | None = None,
    ) -> None:
        """Recompute readiness from indicators while decision remains mutable."""
        DecisionPolicy.assert_mutable(self._status, action="refresh_readiness")
        next_indicators = (
            list(DecisionPolicy.assert_indicators(indicators))
            if indicators is not None
            else list(self._indicators)
        )
        next_readiness = ReadinessPolicy.assess(
            next_indicators,
            rationale=rationale,
        )
        ReadinessPolicy.assert_consistent_with_indicators(
            next_readiness, next_indicators
        )
        DecisionPolicy.assert_constraints_satisfied(
            self._constraints,
            indicators=next_indicators,
            readiness=next_readiness,
            confidence=self._confidence,
            outcome=None,
            approving=False,
        )
        self._indicators = next_indicators
        self._readiness = next_readiness

    # --- queries ---

    def is_pending(self) -> bool:
        return self._status is DecisionStatus.PENDING

    def is_approved(self) -> bool:
        return self._status is DecisionStatus.APPROVED

    def is_delayed(self) -> bool:
        return self._status is DecisionStatus.DELAYED

    def is_rejected(self) -> bool:
        return self._status is DecisionStatus.REJECTED

    def is_reconsidered(self) -> bool:
        return self._status is DecisionStatus.RECONSIDERED

    def teaches_now(self) -> bool:
        return (
            self._status is DecisionStatus.APPROVED
            and self._outcome is DecisionOutcome.TEACH_NOW
        )

    def indicator_count(self) -> int:
        return len(self._indicators)

    def constraint_count(self) -> int:
        return len(self._constraints)

    def reason_count(self) -> int:
        return len(self._reasons)

    def priority_count(self) -> int:
        return len(self._priority_references)

    def intention_count(self) -> int:
        return len(self._intention_references)

    def strategy_count(self) -> int:
        return len(self._strategy_references)

    def has_indicator_kind(self, kind: object) -> bool:
        return any(indicator.kind is kind for indicator in self._indicators)

    def has_constraint_kind(self, kind: object) -> bool:
        return any(constraint.kind is kind for constraint in self._constraints)

    def has_priority(self, priority_id: object) -> bool:
        return any(
            ref.priority_id == priority_id for ref in self._priority_references
        )

    def has_intention(self, intention_id: object) -> bool:
        return any(
            ref.intention_id == intention_id for ref in self._intention_references
        )

    def has_strategy(self, strategy_id: object) -> bool:
        return any(
            ref.strategy_id == strategy_id for ref in self._strategy_references
        )

    def suggested_deferral_outcome(self) -> DecisionOutcome:
        """Map dominant blocking indicators to a lawful non-teach outcome."""
        suggestion = ReadinessPolicy.suggested_deferral_outcome(self._indicators)
        return DecisionOutcome(suggestion)

    def revision_kind_for_status(self) -> DecisionRevisionKind:
        mapping = {
            DecisionStatus.APPROVED: DecisionRevisionKind.APPROVED,
            DecisionStatus.DELAYED: DecisionRevisionKind.DELAYED,
            DecisionStatus.REJECTED: DecisionRevisionKind.REJECTED,
            DecisionStatus.RECONSIDERED: DecisionRevisionKind.RECONSIDERED,
        }
        return mapping.get(self._status, DecisionRevisionKind.GENERAL)

    def _make_decision_made_event(self) -> DecisionMade:
        assert self._outcome is not None
        return DecisionMade(
            decision_id=self._decision_id,
            student_id=self._student_id,
            outcome=self._outcome,
            status=self._status,
            readiness_band=self._readiness.band.value,
            confidence_level=self._confidence.level,
            indicator_count=len(self._indicators),
            constraint_count=len(self._constraints),
            reason_count=len(self._reasons),
        )

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, EducationalDecision):
            return NotImplemented
        return self._decision_id == other._decision_id

    def __hash__(self) -> int:
        return hash((type(self), self._decision_id))

    def __repr__(self) -> str:
        return (
            f"EducationalDecision(decision_id={self._decision_id!r}, "
            f"status={self._status!r}, outcome={self._outcome!r})"
        )
