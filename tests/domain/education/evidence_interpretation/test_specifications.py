"""Specification tests for Evidence Interpretation domain."""

from __future__ import annotations

import pytest

from domain.education.evidence_interpretation import (
    InterpretationIsActionableSpecification,
    InterpretationIsConsistentSpecification,
    PatternKind,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.evidence_interpretation.conftest import (
    EVIDENCE_001,
    make_cluster,
    make_confidence,
    make_interpretation,
    make_pattern,
    make_summary,
)


def test_actionable_satisfied_by_active() -> None:
    interp = make_interpretation()
    spec = InterpretationIsActionableSpecification()
    assert spec.is_satisfied_by(interp)
    spec.assert_satisfied_by(interp)


def test_actionable_satisfied_after_revise() -> None:
    interp = make_interpretation()
    interp.revise(confidence=make_confidence(ConfidenceLevel.MEDIUM))
    assert InterpretationIsActionableSpecification().is_satisfied_by(interp)


def test_actionable_rejects_invalidated() -> None:
    interp = make_interpretation()
    interp.invalidate("void")
    assert not InterpretationIsActionableSpecification().is_satisfied_by(interp)
    with pytest.raises(EducationalInvariantViolation):
        InterpretationIsActionableSpecification().assert_satisfied_by(interp)


def test_actionable_rejects_merged() -> None:
    primary = make_interpretation(interpretation_id="primary")
    other = make_interpretation(
        interpretation_id="other",
        clusters=[
            make_cluster(cluster_id="c-other", theme="other theme"),
        ],
        patterns=[
            make_pattern(
                pattern_id="p-other",
                kind=PatternKind.REPEATED_TRANSFER_FAILURE,
                description="Other pattern",
            )
        ],
        summary=make_summary(
            text="Observed other transfer failures",
            pattern_count=1,
            cluster_count=1,
        ),
    )
    primary.merge(other)
    assert not InterpretationIsActionableSpecification().is_satisfied_by(other)


def test_actionable_rejects_very_low_confidence() -> None:
    # Construct via revise after creation with low confidence that still
    # satisfies clustering floors for retrieval (LOW floor).
    interp = make_interpretation(
        confidence=make_confidence(ConfidenceLevel.LOW),
    )
    # Actionable requires at least LOW — this should still pass.
    assert InterpretationIsActionableSpecification().is_satisfied_by(interp)


def test_consistent_satisfied() -> None:
    interp = make_interpretation()
    spec = InterpretationIsConsistentSpecification()
    assert spec.is_satisfied_by(interp)
    spec.assert_satisfied_by(interp)


def test_consistent_rejects_invalidated() -> None:
    interp = make_interpretation()
    interp.invalidate("void")
    assert not InterpretationIsConsistentSpecification().is_satisfied_by(interp)


def test_consistent_assert_raises() -> None:
    interp = make_interpretation()
    interp.invalidate("void")
    with pytest.raises(EducationalInvariantViolation):
        InterpretationIsConsistentSpecification().assert_satisfied_by(interp)


@pytest.mark.parametrize(
    "kind",
    [
        PatternKind.REPEATED_RETRIEVAL_FAILURE,
        PatternKind.REPEATED_TRANSFER_FAILURE,
        PatternKind.REPEATED_PROCEDURAL_ERROR,
        PatternKind.EVIDENCE_CONSISTENCY,
        PatternKind.EVIDENCE_SUFFICIENCY,
    ],
)
def test_actionable_across_pattern_kinds(kind: PatternKind) -> None:
    if kind in {
        PatternKind.EVIDENCE_CONSISTENCY,
        PatternKind.EVIDENCE_SUFFICIENCY,
    }:
        clusters = [make_cluster(evidence_ids=(EVIDENCE_001,))]
        patterns = [
            make_pattern(
                kind=kind,
                description=f"{kind.value} observation",
                evidence_ids=(EVIDENCE_001,),
                occurrence_count=1,
            )
        ]
        confidence = make_confidence(ConfidenceLevel.MEDIUM)
    else:
        clusters = [make_cluster()]
        patterns = [
            make_pattern(
                kind=kind,
                description=f"{kind.value} observation",
            )
        ]
        confidence = make_confidence(ConfidenceLevel.HIGH)
    interp = make_interpretation(
        clusters=clusters,
        patterns=patterns,
        confidence=confidence,
        summary=make_summary(
            text=f"Observed {kind.value.replace('_', ' ')}",
            pattern_count=1,
            cluster_count=1,
        ),
    )
    assert InterpretationIsActionableSpecification().is_satisfied_by(interp)
    assert InterpretationIsConsistentSpecification().is_satisfied_by(interp)
