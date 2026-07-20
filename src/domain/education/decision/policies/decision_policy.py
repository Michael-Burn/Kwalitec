"""Policy governing EducationalDecision construction and transitions.

Architecture Source
    EDUCATIONAL_DECISION_POINTS.md
Concept
    Decision Policy
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
    DecisionStatus,
    ExecutionConstraintKind,
    ReadinessBand,
    ReadinessIndicatorKind,
)
from domain.education.decision.policies.readiness_policy import ReadinessPolicy
from domain.education.decision.value_objects.decision_confidence import (
    DecisionConfidence,
)
from domain.education.decision.value_objects.readiness_level import ReadinessLevel
from domain.education.foundation.base import (
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DecisionId

_COMMITTED = frozenset(
    {
        DecisionStatus.APPROVED,
        DecisionStatus.DELAYED,
        DecisionStatus.REJECTED,
    }
)

_MUTABLE = frozenset(
    {
        DecisionStatus.PENDING,
        DecisionStatus.RECONSIDERED,
    }
)

_NON_TEACH_OUTCOMES = frozenset(
    {
        DecisionOutcome.DELAY,
        DecisionOutcome.REQUIRE_REMEDIATION,
        DecisionOutcome.REQUIRE_PREREQUISITE_WORK,
        DecisionOutcome.REQUIRE_ADDITIONAL_EVIDENCE,
    }
)


class DecisionPolicy:
    """Enforces EducationalDecision identity, ownership, and transition law."""

    @staticmethod
    def assert_identity(decision_id: DecisionId) -> DecisionId:
        if not isinstance(decision_id, DecisionId):
            raise EducationalInvariantViolation(
                "decision must possess a DecisionId identity",
                invariant="EducationalDecision.identity.required",
            )
        return decision_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_confidence(confidence: DecisionConfidence) -> DecisionConfidence:
        if not isinstance(confidence, DecisionConfidence):
            raise EducationalInvariantViolation(
                "decision must possess confidence",
                invariant="EducationalDecision.confidence.required",
            )
        return confidence

    @staticmethod
    def assert_readiness(readiness: ReadinessLevel) -> ReadinessLevel:
        if not isinstance(readiness, ReadinessLevel):
            raise EducationalInvariantViolation(
                "decision must possess readiness",
                invariant="EducationalDecision.readiness.required",
            )
        return readiness

    @staticmethod
    def assert_status(status: DecisionStatus) -> DecisionStatus:
        if not isinstance(status, DecisionStatus):
            raise EducationalInvariantViolation(
                "status must be a DecisionStatus",
                invariant="EducationalDecision.status.type",
            )
        return status

    @staticmethod
    def assert_outcome(
        outcome: DecisionOutcome | None,
    ) -> DecisionOutcome | None:
        if outcome is None:
            return None
        if not isinstance(outcome, DecisionOutcome):
            raise EducationalInvariantViolation(
                "outcome must be a DecisionOutcome when provided",
                invariant="EducationalDecision.outcome.type",
            )
        return outcome

    @classmethod
    def assert_mutable(cls, status: DecisionStatus, *, action: str) -> None:
        if status not in _MUTABLE:
            raise EducationalInvariantViolation(
                f"cannot {action} a decision in status {status.value}; "
                "reconsider first to reopen",
                invariant="EducationalDecision.status.mutable",
            )

    @classmethod
    def assert_reconsiderable(cls, status: DecisionStatus) -> None:
        if status in _COMMITTED:
            return
        if status is DecisionStatus.PENDING:
            raise EducationalInvariantViolation(
                "cannot reconsider a pending decision that has not been made",
                invariant="EducationalDecision.reconsider.not_made",
            )
        raise EducationalInvariantViolation(
            "can only reconsider an approved, delayed, or rejected decision",
            invariant="EducationalDecision.reconsider.committed",
        )

    @staticmethod
    def assert_priority_references(
        references: tuple[PriorityReference, ...] | list[PriorityReference],
    ) -> tuple[PriorityReference, ...]:
        collected = tuple(references)
        if not collected:
            raise EducationalInvariantViolation(
                "decision must reference Priority",
                invariant="EducationalDecision.priority_references.min_one",
            )
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, PriorityReference):
                raise EducationalInvariantViolation(
                    "priority_references must be PriorityReference values",
                    invariant="EducationalDecision.priority_references.type",
                )
            if ref.priority_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate priority reference is not allowed",
                    invariant="EducationalDecision.priority_references.no_duplicate",
                )
            seen.add(ref.priority_id.value)
        return collected

    @staticmethod
    def assert_intention_references(
        references: tuple[IntentionReference, ...] | list[IntentionReference],
    ) -> tuple[IntentionReference, ...]:
        collected = tuple(references)
        if not collected:
            raise EducationalInvariantViolation(
                "decision must reference Teaching Intention",
                invariant="EducationalDecision.intention_references.min_one",
            )
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, IntentionReference):
                raise EducationalInvariantViolation(
                    "intention_references must be IntentionReference values",
                    invariant="EducationalDecision.intention_references.type",
                )
            if ref.intention_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate intention reference is not allowed",
                    invariant="EducationalDecision.intention_references.no_duplicate",
                )
            seen.add(ref.intention_id.value)
        return collected

    @staticmethod
    def assert_strategy_references(
        references: tuple[StrategyReference, ...] | list[StrategyReference],
    ) -> tuple[StrategyReference, ...]:
        collected = tuple(references)
        if not collected:
            raise EducationalInvariantViolation(
                "decision must reference Strategy",
                invariant="EducationalDecision.strategy_references.min_one",
            )
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, StrategyReference):
                raise EducationalInvariantViolation(
                    "strategy_references must be StrategyReference values",
                    invariant="EducationalDecision.strategy_references.type",
                )
            if ref.strategy_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate strategy reference is not allowed",
                    invariant="EducationalDecision.strategy_references.no_duplicate",
                )
            seen.add(ref.strategy_id.value)
        return collected

    @staticmethod
    def assert_indicators(
        indicators: tuple[ReadinessIndicator, ...] | list[ReadinessIndicator],
    ) -> tuple[ReadinessIndicator, ...]:
        collected = tuple(indicators)
        if not collected:
            raise EducationalInvariantViolation(
                "decision must possess at least one readiness indicator",
                invariant="EducationalDecision.indicators.min_one",
            )
        seen_ids: set[str] = set()
        seen_signatures: set[tuple[str, bool]] = set()
        for indicator in collected:
            if not isinstance(indicator, ReadinessIndicator):
                raise EducationalInvariantViolation(
                    "indicators must be ReadinessIndicator values",
                    invariant="EducationalDecision.indicators.type",
                )
            if indicator.indicator_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate readiness indicator identity is not allowed",
                    invariant="EducationalDecision.indicators.no_duplicate_id",
                )
            signature = indicator.indicator_signature()
            if signature in seen_signatures:
                raise EducationalInvariantViolation(
                    "duplicate readiness indicator kind polarity is not allowed",
                    invariant="EducationalDecision.indicators.no_duplicate_kind",
                )
            seen_ids.add(indicator.indicator_id.value)
            seen_signatures.add(signature)
        return collected

    @staticmethod
    def assert_indicator_not_duplicate(
        existing: list[ReadinessIndicator] | tuple[ReadinessIndicator, ...],
        candidate: ReadinessIndicator,
    ) -> None:
        for indicator in existing:
            if indicator.indicator_id == candidate.indicator_id:
                raise EducationalInvariantViolation(
                    "duplicate readiness indicator identity is not allowed",
                    invariant="EducationalDecision.indicators.no_duplicate_id",
                )
            if indicator.indicator_signature() == candidate.indicator_signature():
                raise EducationalInvariantViolation(
                    "duplicate readiness indicator kind polarity is not allowed",
                    invariant="EducationalDecision.indicators.no_duplicate_kind",
                )

    @staticmethod
    def assert_reasons(
        reasons: tuple[DecisionReason, ...] | list[DecisionReason],
    ) -> tuple[DecisionReason, ...]:
        collected = tuple(reasons)
        seen_ids: set[str] = set()
        seen_signatures: set[tuple[str, str | None]] = set()
        for reason in collected:
            if not isinstance(reason, DecisionReason):
                raise EducationalInvariantViolation(
                    "reasons must be DecisionReason values",
                    invariant="EducationalDecision.reasons.type",
                )
            if reason.reason_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate decision reason identity is not allowed",
                    invariant="EducationalDecision.reasons.no_duplicate_id",
                )
            signature = reason.reason_signature()
            if signature in seen_signatures:
                raise EducationalInvariantViolation(
                    "duplicate decision reason statement is not allowed",
                    invariant="EducationalDecision.reasons.no_duplicate_statement",
                )
            seen_ids.add(reason.reason_id.value)
            seen_signatures.add(signature)
        return collected

    @staticmethod
    def assert_reason_not_duplicate(
        existing: list[DecisionReason] | tuple[DecisionReason, ...],
        candidate: DecisionReason,
    ) -> None:
        for reason in existing:
            if reason.reason_id == candidate.reason_id:
                raise EducationalInvariantViolation(
                    "duplicate decision reason identity is not allowed",
                    invariant="EducationalDecision.reasons.no_duplicate_id",
                )
            if reason.reason_signature() == candidate.reason_signature():
                raise EducationalInvariantViolation(
                    "duplicate decision reason statement is not allowed",
                    invariant="EducationalDecision.reasons.no_duplicate_statement",
                )

    @staticmethod
    def assert_constraints(
        constraints: tuple[ExecutionConstraint, ...] | list[ExecutionConstraint],
    ) -> tuple[ExecutionConstraint, ...]:
        collected = tuple(constraints)
        seen_ids: set[str] = set()
        seen_signatures: set[
            tuple[str, str | None, str | None, str | None, str | None]
        ] = set()
        for constraint in collected:
            if not isinstance(constraint, ExecutionConstraint):
                raise EducationalInvariantViolation(
                    "constraints must be ExecutionConstraint values",
                    invariant="EducationalDecision.constraints.type",
                )
            if constraint.constraint_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate execution constraint identity is not allowed",
                    invariant="EducationalDecision.constraints.no_duplicate_id",
                )
            signature = constraint.constraint_signature()
            if signature in seen_signatures:
                raise EducationalInvariantViolation(
                    "duplicate execution constraint signature is not allowed",
                    invariant="EducationalDecision.constraints.no_duplicate_kind",
                )
            seen_ids.add(constraint.constraint_id.value)
            seen_signatures.add(signature)
        DecisionPolicy._assert_no_contradictory_constraint_pair(collected)
        return collected

    @staticmethod
    def _assert_no_contradictory_constraint_pair(
        constraints: tuple[ExecutionConstraint, ...],
    ) -> None:
        require_kinds = {
            c.related_indicator_kind
            for c in constraints
            if c.kind is ExecutionConstraintKind.REQUIRE_INDICATOR
        }
        forbid_kinds = {
            c.related_indicator_kind
            for c in constraints
            if c.kind is ExecutionConstraintKind.FORBID_INDICATOR
        }
        overlap = require_kinds & forbid_kinds
        if overlap:
            raise EducationalInvariantViolation(
                "cannot both require and forbid the same readiness indicator",
                invariant="EducationalDecision.constraints.contradictory_indicator",
            )

    @classmethod
    def assert_constraints_satisfied(
        cls,
        constraints: tuple[ExecutionConstraint, ...] | list[ExecutionConstraint],
        *,
        indicators: tuple[ReadinessIndicator, ...] | list[ReadinessIndicator],
        readiness: ReadinessLevel,
        confidence: DecisionConfidence,
        outcome: DecisionOutcome | None = None,
        approving: bool = False,
    ) -> None:
        """Enforce execution constraints; reject contradictory approval."""
        indicator_kinds = {indicator.kind for indicator in indicators}
        for constraint in constraints:
            cls._assert_one_constraint(
                constraint,
                indicator_kinds=indicator_kinds,
                readiness=readiness,
                confidence=confidence,
                outcome=outcome,
                approving=approving,
            )

    @classmethod
    def _assert_one_constraint(
        cls,
        constraint: ExecutionConstraint,
        *,
        indicator_kinds: set[ReadinessIndicatorKind],
        readiness: ReadinessLevel,
        confidence: DecisionConfidence,
        outcome: DecisionOutcome | None,
        approving: bool,
    ) -> None:
        kind = constraint.kind
        if kind is ExecutionConstraintKind.FORBID_TEACH_WITHOUT_PREREQUISITE:
            if (
                approving
                and ReadinessIndicatorKind.PREREQUISITE_MISSING in indicator_kinds
            ):
                raise EducationalInvariantViolation(
                    "cannot approve while prerequisite is missing",
                    invariant="EducationalDecision.constraints.prerequisite",
                )
        elif kind is ExecutionConstraintKind.FORBID_TEACH_WITHOUT_EVIDENCE:
            if (
                approving
                and ReadinessIndicatorKind.EVIDENCE_INSUFFICIENT in indicator_kinds
            ):
                raise EducationalInvariantViolation(
                    "cannot approve without sufficient evidence",
                    invariant="EducationalDecision.constraints.evidence",
                )
        elif kind is ExecutionConstraintKind.REQUIRE_REMEDIATION_FIRST:
            if (
                approving
                and ReadinessIndicatorKind.REMEDIATION_REQUIRED in indicator_kinds
            ):
                raise EducationalInvariantViolation(
                    "cannot approve while remediation is required first",
                    invariant="EducationalDecision.constraints.remediation",
                )
        elif kind is ExecutionConstraintKind.REQUIRE_MINIMUM_READINESS:
            assert constraint.min_readiness is not None
            if not readiness.is_at_least(constraint.min_readiness):
                raise EducationalInvariantViolation(
                    "readiness does not meet required minimum",
                    invariant="EducationalDecision.constraints.min_readiness",
                )
        elif kind is ExecutionConstraintKind.REQUIRE_MINIMUM_CONFIDENCE:
            assert constraint.min_confidence is not None
            if not confidence.is_at_least(constraint.min_confidence):
                raise EducationalInvariantViolation(
                    "confidence does not meet required minimum",
                    invariant="EducationalDecision.constraints.min_confidence",
                )
        elif kind is ExecutionConstraintKind.FORBID_APPROVAL_WHEN_BLOCKED:
            if approving and readiness.band is ReadinessBand.BLOCKED:
                raise EducationalInvariantViolation(
                    "cannot approve a blocked intervention",
                    invariant="EducationalDecision.constraints.blocked",
                )
        elif kind is ExecutionConstraintKind.PROTECT_CAPACITY:
            if (
                approving
                and ReadinessIndicatorKind.CAPACITY_INSUFFICIENT in indicator_kinds
            ):
                raise EducationalInvariantViolation(
                    "cannot approve when capacity is insufficient",
                    invariant="EducationalDecision.constraints.capacity",
                )
        elif kind is ExecutionConstraintKind.REQUIRE_INDICATOR:
            assert constraint.related_indicator_kind is not None
            if constraint.related_indicator_kind not in indicator_kinds:
                raise EducationalInvariantViolation(
                    "required readiness indicator is missing",
                    invariant="EducationalDecision.constraints.require_indicator",
                )
        elif kind is ExecutionConstraintKind.FORBID_INDICATOR:
            assert constraint.related_indicator_kind is not None
            if constraint.related_indicator_kind in indicator_kinds:
                raise EducationalInvariantViolation(
                    "forbidden readiness indicator is present",
                    invariant="EducationalDecision.constraints.forbid_indicator",
                )
        elif kind is ExecutionConstraintKind.FORBID_OUTCOME:
            assert constraint.forbidden_outcome is not None
            if outcome is constraint.forbidden_outcome:
                raise EducationalInvariantViolation(
                    f"outcome {outcome.value} is forbidden by constraint",
                    invariant="EducationalDecision.constraints.forbid_outcome",
                )

    @classmethod
    def assert_approval_lawful(
        cls,
        *,
        readiness: ReadinessLevel,
        confidence: DecisionConfidence,
        indicators: tuple[ReadinessIndicator, ...] | list[ReadinessIndicator],
        constraints: tuple[ExecutionConstraint, ...] | list[ExecutionConstraint],
    ) -> None:
        ReadinessPolicy.assert_permits_approval(readiness)
        ReadinessPolicy.assert_consistent_with_indicators(readiness, indicators)
        if confidence.level in {ConfidenceLevel.VERY_LOW}:
            raise EducationalInvariantViolation(
                "cannot approve with VERY_LOW decision confidence",
                invariant="EducationalDecision.approve.confidence.floor",
            )
        cls.assert_constraints_satisfied(
            constraints,
            indicators=indicators,
            readiness=readiness,
            confidence=confidence,
            outcome=DecisionOutcome.TEACH_NOW,
            approving=True,
        )

    @classmethod
    def assert_deferral_outcome(cls, outcome: DecisionOutcome) -> DecisionOutcome:
        if outcome not in _NON_TEACH_OUTCOMES:
            raise EducationalInvariantViolation(
                "delay/reject outcome must not be TEACH_NOW",
                invariant="EducationalDecision.deferral.outcome.non_teach",
            )
        return outcome

    @classmethod
    def assert_rejection_outcome(cls, outcome: DecisionOutcome) -> DecisionOutcome:
        return cls.assert_deferral_outcome(outcome)

    @staticmethod
    def assert_reconsideration_reason(reason: str) -> str:
        return require_non_empty_text(reason, "reconsideration_reason")

    @staticmethod
    def status_for_approval() -> DecisionStatus:
        return DecisionStatus.APPROVED

    @staticmethod
    def status_for_delay() -> DecisionStatus:
        return DecisionStatus.DELAYED

    @staticmethod
    def status_for_rejection() -> DecisionStatus:
        return DecisionStatus.REJECTED
