"""Policy governing EducationalPriority construction and integrity.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Priority Validation Policy
"""

from __future__ import annotations

from domain.education.foundation.base import (
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import PriorityId
from domain.education.priority.entities.priority_constraint import PriorityConstraint
from domain.education.priority.entities.priority_factor import PriorityFactor
from domain.education.priority.entities.priority_references import (
    DiagnosisReference,
    HypothesisReference,
)
from domain.education.priority.entities.priority_scope import PriorityScope
from domain.education.priority.enums import (
    PriorityConstraintKind,
    PriorityFactorKind,
    PriorityScoreBand,
    PriorityStatus,
    UrgencyLevel,
)
from domain.education.priority.value_objects.instructional_impact import (
    InstructionalImpact,
)
from domain.education.priority.value_objects.priority_score import PriorityScore
from domain.education.priority.value_objects.urgency import Urgency

_TERMINAL_FOR_MUTATION = frozenset({PriorityStatus.STABILISED})

_SCORE_ORDER: tuple[PriorityScoreBand, ...] = (
    PriorityScoreBand.NEGLIGIBLE,
    PriorityScoreBand.LOW,
    PriorityScoreBand.MEDIUM,
    PriorityScoreBand.HIGH,
    PriorityScoreBand.CRITICAL,
)

_URGENCY_ORDER: tuple[UrgencyLevel, ...] = (
    UrgencyLevel.DEFERRED,
    UrgencyLevel.ROUTINE,
    UrgencyLevel.ELEVATED,
    UrgencyLevel.IMMEDIATE,
    UrgencyLevel.CRITICAL,
)


class PriorityValidationPolicy:
    """Enforces EducationalPriority identity, ownership, and ordering invariants."""

    @staticmethod
    def assert_identity(priority_id: PriorityId) -> PriorityId:
        if not isinstance(priority_id, PriorityId):
            raise EducationalInvariantViolation(
                "priority must possess a PriorityId identity",
                invariant="EducationalPriority.identity.required",
            )
        return priority_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_scope(scope: PriorityScope) -> PriorityScope:
        if not isinstance(scope, PriorityScope):
            raise EducationalInvariantViolation(
                "priority must identify educational scope",
                invariant="EducationalPriority.scope.required",
            )
        if not scope.statement.strip():
            raise EducationalInvariantViolation(
                "priority must identify educational scope",
                invariant="EducationalPriority.scope.statement.required",
            )
        return scope

    @staticmethod
    def assert_score(score: PriorityScore) -> PriorityScore:
        if not isinstance(score, PriorityScore):
            raise EducationalInvariantViolation(
                "priority must possess score",
                invariant="EducationalPriority.score.required",
            )
        return score

    @staticmethod
    def assert_urgency(urgency: Urgency) -> Urgency:
        if not isinstance(urgency, Urgency):
            raise EducationalInvariantViolation(
                "priority must possess urgency",
                invariant="EducationalPriority.urgency.required",
            )
        return urgency

    @staticmethod
    def assert_instructional_impact(
        impact: InstructionalImpact,
    ) -> InstructionalImpact:
        if not isinstance(impact, InstructionalImpact):
            raise EducationalInvariantViolation(
                "priority must identify instructional impact",
                invariant="EducationalPriority.instructional_impact.required",
            )
        if not impact.statement.strip():
            raise EducationalInvariantViolation(
                "priority must identify instructional impact",
                invariant="EducationalPriority.instructional_impact.statement",
            )
        return impact

    @staticmethod
    def assert_status(status: PriorityStatus) -> PriorityStatus:
        if not isinstance(status, PriorityStatus):
            raise EducationalInvariantViolation(
                "status must be a PriorityStatus",
                invariant="EducationalPriority.status.type",
            )
        return status

    @staticmethod
    def assert_mutable(status: PriorityStatus, *, action: str) -> None:
        if status in _TERMINAL_FOR_MUTATION and action != "recalculate":
            raise EducationalInvariantViolation(
                f"cannot {action} a stabilised priority "
                "(recalculate first to reopen ordering)",
                invariant="EducationalPriority.status.mutable",
            )

    @staticmethod
    def assert_diagnosis_references(
        references: tuple[DiagnosisReference, ...] | list[DiagnosisReference],
    ) -> tuple[DiagnosisReference, ...]:
        collected = tuple(references)
        if not collected:
            raise EducationalInvariantViolation(
                "priority must reference diagnosis",
                invariant="EducationalPriority.diagnosis_references.min_one",
            )
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, DiagnosisReference):
                raise EducationalInvariantViolation(
                    "diagnosis_references must be DiagnosisReference values",
                    invariant="EducationalPriority.diagnosis_references.type",
                )
            if ref.diagnosis_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate diagnosis reference is not allowed",
                    invariant=(
                        "EducationalPriority.diagnosis_references.no_duplicate"
                    ),
                )
            seen.add(ref.diagnosis_id.value)
        return collected

    @staticmethod
    def assert_hypothesis_references(
        references: tuple[HypothesisReference, ...] | list[HypothesisReference],
    ) -> tuple[HypothesisReference, ...]:
        collected = tuple(references)
        if not collected:
            raise EducationalInvariantViolation(
                "priority must reference hypothesis",
                invariant="EducationalPriority.hypothesis_references.min_one",
            )
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, HypothesisReference):
                raise EducationalInvariantViolation(
                    "hypothesis_references must be HypothesisReference values",
                    invariant="EducationalPriority.hypothesis_references.type",
                )
            if ref.hypothesis_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate hypothesis reference is not allowed",
                    invariant=(
                        "EducationalPriority.hypothesis_references.no_duplicate"
                    ),
                )
            seen.add(ref.hypothesis_id.value)
        return collected

    @staticmethod
    def assert_factors(
        factors: tuple[PriorityFactor, ...] | list[PriorityFactor],
    ) -> tuple[PriorityFactor, ...]:
        collected = tuple(factors)
        if not collected:
            raise EducationalInvariantViolation(
                "priority must possess at least one priority factor "
                "to remain recalculable",
                invariant="EducationalPriority.factors.min_one",
            )
        seen_ids: set[str] = set()
        seen_kinds: set[PriorityFactorKind] = set()
        for factor in collected:
            if not isinstance(factor, PriorityFactor):
                raise EducationalInvariantViolation(
                    "factors must be PriorityFactor entities",
                    invariant="EducationalPriority.factors.type",
                )
            if factor.factor_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate priority factor identity is not allowed",
                    invariant="EducationalPriority.factors.no_duplicate_id",
                )
            if factor.kind in seen_kinds:
                raise EducationalInvariantViolation(
                    "cannot contain duplicate factors "
                    f"(factor kind {factor.kind.value} already present)",
                    invariant="EducationalPriority.factors.no_duplicate_kind",
                )
            seen_ids.add(factor.factor_id.value)
            seen_kinds.add(factor.kind)
        return collected

    @staticmethod
    def assert_factor_not_duplicate(
        existing: tuple[PriorityFactor, ...] | list[PriorityFactor],
        candidate: PriorityFactor,
    ) -> None:
        for factor in existing:
            if factor.factor_id == candidate.factor_id:
                raise EducationalInvariantViolation(
                    "duplicate priority factor identity is not allowed",
                    invariant="EducationalPriority.factors.no_duplicate_id",
                )
            if factor.kind is candidate.kind:
                raise EducationalInvariantViolation(
                    "cannot contain duplicate factors "
                    f"(factor kind {candidate.kind.value} already present)",
                    invariant="EducationalPriority.factors.no_duplicate_kind",
                )

    @staticmethod
    def assert_constraints(
        constraints: tuple[PriorityConstraint, ...] | list[PriorityConstraint],
    ) -> tuple[PriorityConstraint, ...]:
        collected = tuple(constraints)
        seen_ids: set[str] = set()
        seen_signatures: set[
            tuple[str, str | None, str | None, str | None]
        ] = set()
        for constraint in collected:
            if not isinstance(constraint, PriorityConstraint):
                raise EducationalInvariantViolation(
                    "constraints must be PriorityConstraint entities",
                    invariant="EducationalPriority.constraints.type",
                )
            if constraint.constraint_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate priority constraint identity is not allowed",
                    invariant="EducationalPriority.constraints.no_duplicate_id",
                )
            signature = constraint.constraint_signature()
            if signature in seen_signatures:
                raise EducationalInvariantViolation(
                    "identical priority constraints must not be duplicated",
                    invariant=(
                        "EducationalPriority.constraints.no_identical_duplicate"
                    ),
                )
            seen_ids.add(constraint.constraint_id.value)
            seen_signatures.add(signature)
        return collected

    @staticmethod
    def assert_constraints_satisfied(
        constraints: tuple[PriorityConstraint, ...] | list[PriorityConstraint],
        factors: tuple[PriorityFactor, ...] | list[PriorityFactor],
        score: PriorityScore,
        urgency: Urgency,
    ) -> None:
        """Reject orderings that contradict educational constraints."""
        factor_kinds = {factor.kind for factor in factors}
        factor_by_kind = {factor.kind: factor for factor in factors}

        for constraint in constraints:
            if constraint.kind is PriorityConstraintKind.REQUIRE_FACTOR:
                required = constraint.related_factor_kind
                if required is not None and required not in factor_kinds:
                    raise EducationalInvariantViolation(
                        f"constraint requires factor kind {required.value}",
                        invariant="EducationalPriority.constraints.require_factor",
                    )
            elif constraint.kind is PriorityConstraintKind.FORBID_FACTOR:
                forbidden = constraint.related_factor_kind
                if forbidden is not None and forbidden in factor_kinds:
                    raise EducationalInvariantViolation(
                        f"constraint forbids factor kind {forbidden.value}",
                        invariant="EducationalPriority.constraints.forbid_factor",
                    )
            elif constraint.kind is PriorityConstraintKind.CAP_URGENCY:
                cap = constraint.max_urgency
                if cap is not None and _URGENCY_ORDER.index(
                    urgency.level
                ) > _URGENCY_ORDER.index(cap):
                    raise EducationalInvariantViolation(
                        "urgency exceeds constraint cap",
                        invariant="EducationalPriority.constraints.cap_urgency",
                    )
            elif constraint.kind is PriorityConstraintKind.CAP_SCORE:
                cap = constraint.max_score_band
                if cap is not None and _SCORE_ORDER.index(
                    score.band
                ) > _SCORE_ORDER.index(cap):
                    raise EducationalInvariantViolation(
                        "priority score exceeds constraint cap",
                        invariant="EducationalPriority.constraints.cap_score",
                    )
            elif (
                constraint.kind
                is PriorityConstraintKind.PROTECT_PREREQUISITE_OVER_EXTENSION
            ):
                PriorityValidationPolicy._assert_factor_dominance(
                    factor_by_kind,
                    dominant=PriorityFactorKind.PREREQUISITE_IMPORTANCE,
                    subordinate=PriorityFactorKind.EXAM_RELEVANCE,
                    invariant=(
                        "EducationalPriority.constraints.protect_prerequisite"
                    ),
                    message=(
                        "prerequisite importance must outrank exam relevance "
                        "when both contribute"
                    ),
                )
                PriorityValidationPolicy._assert_factor_dominance(
                    factor_by_kind,
                    dominant=PriorityFactorKind.LEARNING_DEPENDENCY_DEPTH,
                    subordinate=PriorityFactorKind.EXAM_RELEVANCE,
                    invariant=(
                        "EducationalPriority.constraints.protect_dependency"
                    ),
                    message=(
                        "learning dependency depth must outrank exam relevance "
                        "when both contribute"
                    ),
                )
            elif (
                constraint.kind
                is PriorityConstraintKind.PROTECT_MISCONCEPTION_OVER_PRACTICE
            ):
                PriorityValidationPolicy._assert_factor_dominance(
                    factor_by_kind,
                    dominant=PriorityFactorKind.MISCONCEPTION_PERSISTENCE,
                    subordinate=PriorityFactorKind.EXAM_RELEVANCE,
                    invariant=(
                        "EducationalPriority.constraints.protect_misconception"
                    ),
                    message=(
                        "misconception persistence must outrank exam relevance "
                        "when both contribute"
                    ),
                )
            elif (
                constraint.kind
                is PriorityConstraintKind.PROTECT_UNDERSTANDING_OVER_SPEED
            ):
                PriorityValidationPolicy._assert_factor_dominance(
                    factor_by_kind,
                    dominant=PriorityFactorKind.CONCEPT_CENTRALITY,
                    subordinate=PriorityFactorKind.EXAM_RELEVANCE,
                    invariant=(
                        "EducationalPriority.constraints.protect_understanding"
                    ),
                    message=(
                        "concept centrality must outrank exam relevance "
                        "when both contribute"
                    ),
                )
            elif (
                constraint.kind
                is PriorityConstraintKind.EXAM_MUST_NOT_SKIP_CONCEPTUAL_REPAIR
            ):
                if (
                    PriorityFactorKind.EXAM_RELEVANCE in factor_by_kind
                    and PriorityFactorKind.MISCONCEPTION_PERSISTENCE
                    in factor_by_kind
                    and factor_by_kind[
                        PriorityFactorKind.EXAM_RELEVANCE
                    ].contribution
                    >= factor_by_kind[
                        PriorityFactorKind.MISCONCEPTION_PERSISTENCE
                    ].contribution
                ):
                    raise EducationalInvariantViolation(
                        "exam relevance must not outrank misconception repair",
                        invariant=(
                            "EducationalPriority.constraints.exam_not_skip_repair"
                        ),
                    )
            elif (
                constraint.kind
                is PriorityConstraintKind.FORBID_ENGAGEMENT_ORDERING
            ):
                # Engagement metrics are not lawful priority factors. This
                # constraint is satisfied whenever ordering rests only on the
                # educational factor catalogue (already enforced by factor
                # validation). Kept as an explicit protective posture.
                continue
            elif (
                constraint.kind
                is PriorityConstraintKind.PROTECT_DURABLE_LEARNING_OVER_THEATRE
            ):
                PriorityValidationPolicy._assert_factor_dominance(
                    factor_by_kind,
                    dominant=PriorityFactorKind.EDUCATIONAL_LEVERAGE,
                    subordinate=PriorityFactorKind.EXAM_RELEVANCE,
                    invariant=(
                        "EducationalPriority.constraints.protect_durable_learning"
                    ),
                    message=(
                        "educational leverage must outrank exam relevance "
                        "when both contribute"
                    ),
                    allow_missing_dominant=True,
                )

    @staticmethod
    def _assert_factor_dominance(
        factor_by_kind: dict[PriorityFactorKind, PriorityFactor],
        *,
        dominant: PriorityFactorKind,
        subordinate: PriorityFactorKind,
        invariant: str,
        message: str,
        allow_missing_dominant: bool = False,
    ) -> None:
        if dominant not in factor_by_kind or subordinate not in factor_by_kind:
            if (
                subordinate in factor_by_kind
                and dominant not in factor_by_kind
                and not allow_missing_dominant
            ):
                # Only enforce when both are present unless explicitly required.
                return
            return
        if (
            factor_by_kind[subordinate].contribution
            > factor_by_kind[dominant].contribution
        ):
            raise EducationalInvariantViolation(message, invariant=invariant)

    @staticmethod
    def assert_recalculable(
        factors: tuple[PriorityFactor, ...] | list[PriorityFactor],
    ) -> None:
        if not factors:
            raise EducationalInvariantViolation(
                "priority must remain recalculable "
                "(at least one factor required)",
                invariant="EducationalPriority.recalculable",
            )

    @staticmethod
    def assert_stabilisation_reason(reason: str | None) -> str | None:
        if reason is None:
            return None
        return require_non_empty_text(reason, "stabilisation_reason")
