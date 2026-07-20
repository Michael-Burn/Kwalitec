"""High-volume matrices exercising Educational Decision domain surface area."""

from __future__ import annotations

import pytest

from domain.education.decision import (
    DecisionIsExecutableSpecification,
    DecisionOutcome,
    DecisionPolicy,
    DecisionRevisionKind,
    DecisionStatus,
    ExecutionConstraintKind,
    InterventionIsReadySpecification,
    ReadinessBand,
    ReadinessIndicatorKind,
    ReadinessPolicy,
)
from domain.education.foundation.enums import (
    ConfidenceLevel,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.decision.conftest import (
    make_approved_decision,
    make_confidence,
    make_constraint,
    make_decision,
    make_indicator,
    make_intention_ref,
    make_priority_ref,
    make_readiness,
    make_ready_indicators,
    make_reason,
    make_strategy_ref,
)

INTENTION_TYPES = list(TeachingIntentionType)
STRATEGY_TYPES = list(TeachingStrategyType)
INDICATOR_KINDS = list(ReadinessIndicatorKind)
OUTCOMES = list(DecisionOutcome)
NON_TEACH_OUTCOMES = [o for o in OUTCOMES if o is not DecisionOutcome.TEACH_NOW]
READINESS_BANDS = list(ReadinessBand)
CONFIDENCE_LEVELS = [
    ConfidenceLevel.VERY_LOW,
    ConfidenceLevel.LOW,
    ConfidenceLevel.MEDIUM,
    ConfidenceLevel.HIGH,
    ConfidenceLevel.VERY_HIGH,
]
CONSTRAINT_KINDS = list(ExecutionConstraintKind)
STUDENTS = tuple(f"student-{i}" for i in range(1, 9))
ACTIONS = ("approve", "delay", "reject", "refresh_readiness")
SUPPORTING_KINDS = [
    ReadinessIndicatorKind.PREREQUISITE_SATISFIED,
    ReadinessIndicatorKind.EVIDENCE_SUFFICIENT,
    ReadinessIndicatorKind.CAPACITY_ADEQUATE,
    ReadinessIndicatorKind.INTENTION_ALIGNED,
    ReadinessIndicatorKind.STRATEGY_APPLICABLE,
]
BLOCKING_KINDS = [
    ReadinessIndicatorKind.PREREQUISITE_MISSING,
    ReadinessIndicatorKind.EVIDENCE_INSUFFICIENT,
    ReadinessIndicatorKind.CAPACITY_INSUFFICIENT,
    ReadinessIndicatorKind.REMEDIATION_REQUIRED,
    ReadinessIndicatorKind.AFFECTIVE_BLOCK,
    ReadinessIndicatorKind.SESSION_CONSTRAINT,
    ReadinessIndicatorKind.CONFLICTING_SIGNAL,
]


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
def test_create_per_intention_and_strategy(
    intention_type: TeachingIntentionType, strategy_type: TeachingStrategyType
) -> None:
    decision = make_decision(
        decision_id=f"dec-{intention_type.value}-{strategy_type.value}",
        intention_type=intention_type,
        strategy_type=strategy_type,
    )
    assert decision.intention_references[0].intention_type is intention_type
    assert decision.strategy_references[0].strategy_type is strategy_type
    assert decision.is_pending()


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
@pytest.mark.parametrize("student", STUDENTS)
def test_approve_per_strategy_and_student(
    strategy_type: TeachingStrategyType, student: str
) -> None:
    decision = make_decision(
        decision_id=f"dec-appr-{strategy_type.value}-{student}",
        student_id=student,
        strategy_type=strategy_type,
    )
    decision.approve(reasons=[make_reason(reason_id=f"r-{student}")])
    assert decision.teaches_now()
    assert DecisionIsExecutableSpecification().is_satisfied_by(decision)


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("student", STUDENTS)
def test_pending_ready_per_intention_and_student(
    intention_type: TeachingIntentionType, student: str
) -> None:
    decision = make_decision(
        decision_id=f"dec-ready-{intention_type.value}-{student}",
        student_id=student,
        intention_type=intention_type,
    )
    assert InterventionIsReadySpecification().is_satisfied_by(decision)


@pytest.mark.parametrize("kind", INDICATOR_KINDS)
@pytest.mark.parametrize("student", STUDENTS[:6])
def test_indicator_kind_and_student_matrix(
    kind: ReadinessIndicatorKind, student: str
) -> None:
    supporting = kind in SUPPORTING_KINDS
    indicators = [
        make_indicator(
            indicator_id=f"ind-{kind.value}-{student}",
            kind=kind,
            supports_readiness=supporting,
            weight=0.7,
        )
    ]
    if supporting:
        # Keep at least one supporting companion for assess paths.
        for companion in SUPPORTING_KINDS:
            if companion is kind:
                continue
            indicators.append(
                make_indicator(
                    indicator_id=f"ind-c-{companion.value}-{student}",
                    kind=companion,
                    weight=0.8,
                )
            )
            break
    band = ReadinessBand.READY if supporting else ReadinessBand.BLOCKED
    if kind in {
        ReadinessIndicatorKind.EVIDENCE_INSUFFICIENT,
        ReadinessIndicatorKind.CAPACITY_INSUFFICIENT,
        ReadinessIndicatorKind.CONFLICTING_SIGNAL,
    }:
        band = ReadinessBand.NOT_READY
    decision = make_decision(
        decision_id=f"dec-ind-{kind.value}-{student}",
        student_id=student,
        indicators=indicators,
        readiness=make_readiness(band),
        confidence=make_confidence(ConfidenceLevel.MEDIUM),
    )
    assert decision.has_indicator_kind(kind)


@pytest.mark.parametrize("band", READINESS_BANDS)
@pytest.mark.parametrize("level", CONFIDENCE_LEVELS)
def test_readiness_confidence_matrix(
    band: ReadinessBand, level: ConfidenceLevel
) -> None:
    indicators = make_ready_indicators()
    if band is ReadinessBand.BLOCKED:
        indicators = [
            make_indicator(
                kind=ReadinessIndicatorKind.AFFECTIVE_BLOCK,
                supports_readiness=False,
            )
        ]
    elif band is ReadinessBand.NOT_READY:
        indicators = [
            make_indicator(
                kind=ReadinessIndicatorKind.EVIDENCE_INSUFFICIENT,
                supports_readiness=False,
            ),
            make_indicator(
                indicator_id="ind-cap",
                kind=ReadinessIndicatorKind.CAPACITY_ADEQUATE,
                weight=0.4,
            ),
        ]
    elif band is ReadinessBand.PARTIALLY_READY:
        indicators = [
            make_indicator(
                kind=ReadinessIndicatorKind.EVIDENCE_INSUFFICIENT,
                supports_readiness=False,
                weight=0.3,
            ),
            make_indicator(
                indicator_id="ind-prereq",
                kind=ReadinessIndicatorKind.PREREQUISITE_SATISFIED,
                weight=0.9,
            ),
            make_indicator(
                indicator_id="ind-int",
                kind=ReadinessIndicatorKind.INTENTION_ALIGNED,
                weight=0.9,
            ),
        ]
    decision = make_decision(
        decision_id=f"dec-{band.value}-{level.value}",
        indicators=indicators,
        readiness=make_readiness(band),
        confidence=make_confidence(level),
    )
    assert decision.readiness.band is band
    assert decision.confidence.level is level


@pytest.mark.parametrize("outcome", NON_TEACH_OUTCOMES)
@pytest.mark.parametrize("student", STUDENTS)
def test_delay_matrix(outcome: DecisionOutcome, student: str) -> None:
    decision = make_decision(
        decision_id=f"dec-delay-{outcome.value}-{student}",
        student_id=student,
    )
    decision.delay(outcome, reasons=[make_reason(reason_id=f"rd-{student}")])
    assert decision.is_delayed()
    assert decision.outcome is outcome


@pytest.mark.parametrize("outcome", NON_TEACH_OUTCOMES)
@pytest.mark.parametrize("student", STUDENTS[:5])
def test_reject_matrix(outcome: DecisionOutcome, student: str) -> None:
    decision = make_decision(
        decision_id=f"dec-rej-{outcome.value}-{student}",
        student_id=student,
    )
    decision.reject(outcome, reasons=[make_reason(reason_id=f"rj-{student}")])
    assert decision.is_rejected()
    assert decision.outcome is outcome


@pytest.mark.parametrize("action", ACTIONS)
@pytest.mark.parametrize("student", STUDENTS[:5])
def test_mutation_matrix(action: str, student: str) -> None:
    decision = make_decision(
        decision_id=f"dec-mut-{action}-{student}",
        student_id=student,
    )
    if action == "approve":
        decision.approve(reasons=[make_reason()])
        assert decision.is_approved()
    elif action == "delay":
        decision.delay(DecisionOutcome.DELAY)
        assert decision.is_delayed()
    elif action == "reject":
        decision.reject(DecisionOutcome.REQUIRE_ADDITIONAL_EVIDENCE)
        assert decision.is_rejected()
    else:
        decision.refresh_readiness()
        assert decision.is_pending()


@pytest.mark.parametrize("kind", CONSTRAINT_KINDS)
@pytest.mark.parametrize("student", STUDENTS[:4])
def test_protective_constraints_matrix(
    kind: ExecutionConstraintKind, student: str
) -> None:
    kwargs: dict = {
        "constraint_id": f"c-{kind.value}-{student}",
        "kind": kind,
    }
    if kind is ExecutionConstraintKind.REQUIRE_MINIMUM_READINESS:
        kwargs["min_readiness"] = ReadinessBand.PARTIALLY_READY
    elif kind is ExecutionConstraintKind.REQUIRE_MINIMUM_CONFIDENCE:
        kwargs["min_confidence"] = ConfidenceLevel.LOW
    elif kind is ExecutionConstraintKind.REQUIRE_INDICATOR:
        kwargs["related_indicator_kind"] = ReadinessIndicatorKind.CAPACITY_ADEQUATE
    elif kind is ExecutionConstraintKind.FORBID_INDICATOR:
        kwargs["related_indicator_kind"] = ReadinessIndicatorKind.AFFECTIVE_BLOCK
    elif kind is ExecutionConstraintKind.FORBID_OUTCOME:
        kwargs["forbidden_outcome"] = DecisionOutcome.REQUIRE_REMEDIATION

    decision = make_decision(
        decision_id=f"dec-c-{kind.value}-{student}",
        student_id=student,
        constraints=[make_constraint(**kwargs)],
    )
    assert decision.constraint_count() == 1
    assert decision.has_constraint_kind(kind)


@pytest.mark.parametrize("kind", BLOCKING_KINDS)
def test_blocking_indicator_assessment(kind: ReadinessIndicatorKind) -> None:
    readiness = ReadinessPolicy.assess(
        [make_indicator(kind=kind, supports_readiness=False, weight=0.9)]
    )
    assert readiness.band in {
        ReadinessBand.BLOCKED,
        ReadinessBand.NOT_READY,
        ReadinessBand.PARTIALLY_READY,
    }


@pytest.mark.parametrize("kind", SUPPORTING_KINDS)
def test_supporting_indicator_duplicate_rejected(kind: ReadinessIndicatorKind) -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_decision(
            indicators=[
                make_indicator(indicator_id="a", kind=kind),
                make_indicator(indicator_id="b", kind=kind),
            ]
        )


@pytest.mark.parametrize("i", range(24))
def test_reconsider_volume(i: int) -> None:
    decision = make_approved_decision(decision_id=f"dec-rec-{i}")
    decision.pull_events()
    decision.reconsider(f"reconsider-{i}")
    assert decision.is_reconsidered()
    decision.delay(NON_TEACH_OUTCOMES[i % len(NON_TEACH_OUTCOMES)])
    assert decision.status in {DecisionStatus.DELAYED, DecisionStatus.REJECTED} or (
        decision.is_delayed()
    )


@pytest.mark.parametrize("i", range(16))
def test_approve_reconsider_approve_roundtrip(i: int) -> None:
    decision = make_decision(decision_id=f"dec-round-{i}")
    decision.approve(reasons=[make_reason(reason_id=f"r1-{i}")])
    decision.reconsider(f"roundtrip-{i}")
    decision.approve(reasons=[make_reason(reason_id=f"r2-{i}")])
    assert decision.teaches_now()
    assert decision.revision_kind_for_status() is DecisionRevisionKind.APPROVED


@pytest.mark.parametrize("status", list(DecisionStatus))
def test_status_enum_values(status: DecisionStatus) -> None:
    assert isinstance(status.value, str)
    assert DecisionPolicy.assert_status(status) is status


@pytest.mark.parametrize("outcome", OUTCOMES)
def test_outcome_enum_values(outcome: DecisionOutcome) -> None:
    assert isinstance(outcome.value, str)
    assert DecisionPolicy.assert_outcome(outcome) is outcome


@pytest.mark.parametrize(
    "pair",
    [
        (a, b)
        for i, a in enumerate(SUPPORTING_KINDS)
        for b in SUPPORTING_KINDS[i:]
    ],
)
def test_pairwise_supporting_indicators_assignable(
    pair: tuple[ReadinessIndicatorKind, ReadinessIndicatorKind],
) -> None:
    left, right = pair
    if left is right:
        companion_kind = SUPPORTING_KINDS[
            (SUPPORTING_KINDS.index(left) + 1) % len(SUPPORTING_KINDS)
        ]
        indicators = [
            make_indicator(indicator_id="solo", kind=left),
            make_indicator(
                indicator_id="companion",
                kind=companion_kind,
            ),
        ]
    else:
        indicators = [
            make_indicator(indicator_id="left", kind=left),
            make_indicator(indicator_id="right", kind=right),
        ]
        # Pad to ready assessment if assessing.
        for kind in SUPPORTING_KINDS:
            if kind not in {left, right}:
                indicators.append(
                    make_indicator(indicator_id=f"pad-{kind.value}", kind=kind)
                )
                if len(indicators) >= 4:
                    break
    decision = make_decision(
        decision_id=f"dec-pair-{left.value}-{right.value}",
        indicators=indicators,
        readiness=make_readiness(ReadinessBand.READY),
    )
    assert decision.indicator_count() >= 2


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("band", READINESS_BANDS)
def test_intention_readiness_matrix(
    intention_type: TeachingIntentionType, band: ReadinessBand
) -> None:
    indicators = make_ready_indicators()
    if band is ReadinessBand.BLOCKED:
        indicators = [
            make_indicator(
                kind=ReadinessIndicatorKind.REMEDIATION_REQUIRED,
                supports_readiness=False,
            )
        ]
    elif band is not ReadinessBand.READY:
        indicators = [
            make_indicator(
                kind=ReadinessIndicatorKind.EVIDENCE_INSUFFICIENT,
                supports_readiness=False,
                weight=0.5,
            ),
            make_indicator(
                indicator_id="ind-al",
                kind=ReadinessIndicatorKind.INTENTION_ALIGNED,
                weight=0.9,
            ),
        ]
    decision = make_decision(
        decision_id=f"dec-ir-{intention_type.value}-{band.value}",
        intention_type=intention_type,
        indicators=indicators,
        readiness=make_readiness(band),
    )
    assert decision.intention_references[0].intention_type is intention_type
    assert decision.readiness.band is band


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
@pytest.mark.parametrize("outcome", NON_TEACH_OUTCOMES)
def test_strategy_deferral_matrix(
    strategy_type: TeachingStrategyType, outcome: DecisionOutcome
) -> None:
    decision = make_decision(
        decision_id=f"dec-sd-{strategy_type.value}-{outcome.value}",
        strategy_type=strategy_type,
    )
    decision.delay(outcome)
    assert decision.strategy_references[0].strategy_type is strategy_type
    assert decision.outcome is outcome


@pytest.mark.parametrize("level", CONFIDENCE_LEVELS)
@pytest.mark.parametrize("student", STUDENTS[:4])
def test_confidence_student_matrix(level: ConfidenceLevel, student: str) -> None:
    decision = make_decision(
        decision_id=f"dec-cf-{level.value}-{student}",
        student_id=student,
        confidence=make_confidence(level),
    )
    assert decision.confidence.level is level
    if level is ConfidenceLevel.VERY_LOW:
        with pytest.raises(EducationalInvariantViolation):
            decision.approve()
    else:
        decision.approve(reasons=[make_reason(reason_id=f"r-{student}-{level.value}")])
        assert decision.is_approved()


@pytest.mark.parametrize("i", range(20))
def test_multi_reference_volume(i: int) -> None:
    decision = make_decision(
        decision_id=f"dec-refs-{i}",
        priority_references=[
            make_priority_ref(priority_id=f"prio-{i}-a"),
            make_priority_ref(priority_id=f"prio-{i}-b"),
        ],
        intention_references=[
            make_intention_ref(
                intention_id=f"int-{i}",
                intention_type=INTENTION_TYPES[i % len(INTENTION_TYPES)],
            )
        ],
        strategy_references=[
            make_strategy_ref(
                strategy_id=f"str-{i}",
                strategy_type=STRATEGY_TYPES[i % len(STRATEGY_TYPES)],
            )
        ],
    )
    assert decision.priority_count() == 2
    assert decision.intention_count() == 1
    assert decision.strategy_count() == 1


@pytest.mark.parametrize("strategy_type", STRATEGY_TYPES)
@pytest.mark.parametrize("level", CONFIDENCE_LEVELS)
def test_strategy_confidence_matrix(
    strategy_type: TeachingStrategyType, level: ConfidenceLevel
) -> None:
    decision = make_decision(
        decision_id=f"dec-sc-{strategy_type.value}-{level.value}",
        strategy_type=strategy_type,
        confidence=make_confidence(level),
    )
    assert decision.strategy_references[0].strategy_type is strategy_type
    if level is not ConfidenceLevel.VERY_LOW:
        assert InterventionIsReadySpecification().is_satisfied_by(decision)


@pytest.mark.parametrize("intention_type", INTENTION_TYPES)
@pytest.mark.parametrize("outcome", NON_TEACH_OUTCOMES)
def test_intention_reject_matrix(
    intention_type: TeachingIntentionType, outcome: DecisionOutcome
) -> None:
    decision = make_decision(
        decision_id=f"dec-irj-{intention_type.value}-{outcome.value}",
        intention_type=intention_type,
    )
    decision.reject(outcome)
    assert decision.is_rejected()
    assert decision.outcome is outcome


@pytest.mark.parametrize("kind", BLOCKING_KINDS)
@pytest.mark.parametrize("student", STUDENTS[:4])
def test_blocking_then_delay_matrix(
    kind: ReadinessIndicatorKind, student: str
) -> None:
    decision = make_decision(
        decision_id=f"dec-bd-{kind.value}-{student}",
        student_id=student,
        indicators=[
            make_indicator(kind=kind, supports_readiness=False, weight=0.85)
        ],
        readiness=make_readiness(
            ReadinessBand.BLOCKED
            if kind
            in {
                ReadinessIndicatorKind.PREREQUISITE_MISSING,
                ReadinessIndicatorKind.REMEDIATION_REQUIRED,
                ReadinessIndicatorKind.AFFECTIVE_BLOCK,
                ReadinessIndicatorKind.SESSION_CONSTRAINT,
            }
            else ReadinessBand.NOT_READY
        ),
    )
    outcome = decision.suggested_deferral_outcome()
    decision.delay(outcome)
    assert decision.is_delayed()
    assert outcome is not DecisionOutcome.TEACH_NOW


@pytest.mark.parametrize("i", range(12))
def test_assess_readiness_volume(i: int) -> None:
    decision = make_decision(
        decision_id=f"dec-assess-{i}",
        assess_readiness=True,
        indicators=make_ready_indicators(),
    )
    assert decision.readiness.band is ReadinessBand.READY
    assert decision.is_pending()
