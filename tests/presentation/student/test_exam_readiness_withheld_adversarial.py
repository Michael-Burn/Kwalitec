"""Adversarial regression fixtures: Exam Readiness withhold (Phase 3).

Named fixtures from the Phase 3 critical review. Each asserts the semantic
contract behaviour that coverage alone (or any Phase 3 competing engine input)
must never mint a confident-looking Exam Readiness percentage on learner
surfaces, and that the withdrawn "not yet assessable" state is what displays.

Does not choose a canonical coverage implementation. Does not touch
Progression Readiness, Twin internals, Policy V1, numeric assessment, or
arbitration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from app.presentation.intelligence_surface.adapter import RuntimeAPresentationAdapter
from app.presentation.student.exam_readiness_withheld import (
    EXAM_READINESS_NOT_YET_ASSESSABLE,
    EXAM_READINESS_NOT_YET_ASSESSABLE_SHORT,
    assert_no_confident_exam_readiness_percent,
    student_facing_exam_readiness_claim,
    student_facing_exam_readiness_percentage,
)
from app.services.educational_explainability_service import (
    EducationalExplainabilityService,
)
from app.services.readiness_service import ReadinessService


@dataclass(frozen=True)
class ExamReadinessAdversarialFixture:
    """Named adversarial state for Exam Readiness withhold regression."""

    name: str
    description: str
    # Inputs that historically tempted engines to mint a % (coverage / overall).
    coverage_pct: float
    overall_score: float
    avg_mastery: float
    review_discipline: float
    topics_completed: int
    total_topics: int
    topics_with_ek_evidence: int
    demonstrated_evidence_present: bool
    assessment_evidence_present: bool
    outside_current_syllabus: bool
    conflicting_evidence: bool
    stale_curriculum_version: bool


# Exact Phase 3 S7-shaped case: high coverage, thin demonstrated evidence.
HIGH_COVERAGE_LOW_EVIDENCE = ExamReadinessAdversarialFixture(
    name="HIGH_COVERAGE_LOW_EVIDENCE",
    description=(
        "Phase 3 state S7 shape: ~85.7% coverage with thin demonstrated "
        "evidence. Coverage alone must never mint Exam Readiness %."
    ),
    coverage_pct=85.7,
    overall_score=61.2,
    avg_mastery=0.0,
    review_discipline=0.0,
    topics_completed=12,
    total_topics=14,
    topics_with_ek_evidence=0,
    demonstrated_evidence_present=False,
    assessment_evidence_present=False,
    outside_current_syllabus=False,
    conflicting_evidence=False,
    stale_curriculum_version=False,
)

LOW_COVERAGE_HIGH_DEMONSTRATED_EVIDENCE = ExamReadinessAdversarialFixture(
    name="LOW_COVERAGE_HIGH_DEMONSTRATED_EVIDENCE",
    description=(
        "Low Study Progress coverage with strong demonstrated practice "
        "evidence. Still withheld until evidence architecture is reconciled."
    ),
    coverage_pct=14.3,
    overall_score=48.0,
    avg_mastery=88.0,
    review_discipline=90.0,
    topics_completed=2,
    total_topics=14,
    topics_with_ek_evidence=8,
    demonstrated_evidence_present=True,
    assessment_evidence_present=True,
    outside_current_syllabus=False,
    conflicting_evidence=False,
    stale_curriculum_version=False,
)

HIGH_COVERAGE_HIGH_DEMONSTRATED_EVIDENCE = ExamReadinessAdversarialFixture(
    name="HIGH_COVERAGE_HIGH_DEMONSTRATED_EVIDENCE",
    description=(
        "High coverage and strong demonstrated evidence. Numerical claim "
        "still withheld while architecture is incomplete."
    ),
    coverage_pct=92.0,
    overall_score=88.0,
    avg_mastery=91.0,
    review_discipline=95.0,
    topics_completed=13,
    total_topics=14,
    topics_with_ek_evidence=13,
    demonstrated_evidence_present=True,
    assessment_evidence_present=True,
    outside_current_syllabus=False,
    conflicting_evidence=False,
    stale_curriculum_version=False,
)

HIGH_COVERAGE_NO_ASSESSMENT_EVIDENCE = ExamReadinessAdversarialFixture(
    name="HIGH_COVERAGE_NO_ASSESSMENT_EVIDENCE",
    description=(
        "High coverage with zero assessment evidence. Coverage must not "
        "stand in for Exam Readiness."
    ),
    coverage_pct=85.7,
    overall_score=55.0,
    avg_mastery=0.0,
    review_discipline=40.0,
    topics_completed=12,
    total_topics=14,
    topics_with_ek_evidence=0,
    demonstrated_evidence_present=False,
    assessment_evidence_present=False,
    outside_current_syllabus=False,
    conflicting_evidence=False,
    stale_curriculum_version=False,
)

LOW_COVERAGE_NO_EVIDENCE = ExamReadinessAdversarialFixture(
    name="LOW_COVERAGE_NO_EVIDENCE",
    description="Empty / near-empty account. Withheld, not 'unprepared'.",
    coverage_pct=0.0,
    overall_score=0.0,
    avg_mastery=0.0,
    review_discipline=0.0,
    topics_completed=0,
    total_topics=14,
    topics_with_ek_evidence=0,
    demonstrated_evidence_present=False,
    assessment_evidence_present=False,
    outside_current_syllabus=False,
    conflicting_evidence=False,
    stale_curriculum_version=False,
)

COVERAGE_DATA_PRESENT_BUT_OUTSIDE_CURRENT_SYLLABUS = ExamReadinessAdversarialFixture(
    name="COVERAGE_DATA_PRESENT_BUT_OUTSIDE_CURRENT_SYLLABUS",
    description=(
        "Progress rows exist for topics outside the active plan syllabus "
        "universe. Must not mint a confident sitting-preparedness %."
    ),
    coverage_pct=100.0,
    overall_score=70.0,
    avg_mastery=60.0,
    review_discipline=50.0,
    topics_completed=20,
    total_topics=20,
    topics_with_ek_evidence=5,
    demonstrated_evidence_present=True,
    assessment_evidence_present=False,
    outside_current_syllabus=True,
    conflicting_evidence=False,
    stale_curriculum_version=False,
)

CONFLICTING_EVIDENCE = ExamReadinessAdversarialFixture(
    name="CONFLICTING_EVIDENCE",
    description=(
        "Coverage engines and overall/Twin-shaped scores disagree. Honest "
        "posture is withhold, not pick a theatrical number."
    ),
    coverage_pct=85.7,
    overall_score=35.0,
    avg_mastery=90.0,
    review_discipline=10.0,
    topics_completed=12,
    total_topics=14,
    topics_with_ek_evidence=3,
    demonstrated_evidence_present=True,
    assessment_evidence_present=True,
    outside_current_syllabus=False,
    conflicting_evidence=True,
    stale_curriculum_version=False,
)

STALE_CURRICULUM_VERSION = ExamReadinessAdversarialFixture(
    name="STALE_CURRICULUM_VERSION",
    description=(
        "Evidence recorded against a prior curriculum version. Must not "
        "mint a confident Exam Readiness percentage."
    ),
    coverage_pct=78.0,
    overall_score=66.0,
    avg_mastery=70.0,
    review_discipline=65.0,
    topics_completed=11,
    total_topics=14,
    topics_with_ek_evidence=6,
    demonstrated_evidence_present=True,
    assessment_evidence_present=True,
    outside_current_syllabus=False,
    conflicting_evidence=False,
    stale_curriculum_version=True,
)

NAMED_ADVERSARIAL_FIXTURES: tuple[ExamReadinessAdversarialFixture, ...] = (
    HIGH_COVERAGE_LOW_EVIDENCE,
    LOW_COVERAGE_HIGH_DEMONSTRATED_EVIDENCE,
    HIGH_COVERAGE_HIGH_DEMONSTRATED_EVIDENCE,
    HIGH_COVERAGE_NO_ASSESSMENT_EVIDENCE,
    LOW_COVERAGE_NO_EVIDENCE,
    COVERAGE_DATA_PRESENT_BUT_OUTSIDE_CURRENT_SYLLABUS,
    CONFLICTING_EVIDENCE,
    STALE_CURRICULUM_VERSION,
)


def _overall_shaped_dict(fx: ExamReadinessAdversarialFixture) -> dict[str, Any]:
    return {
        "score": fx.overall_score,
        "coverage_pct": fx.coverage_pct,
        "avg_mastery": fx.avg_mastery,
        "review_discipline": fx.review_discipline,
        "topics_completed": fx.topics_completed,
        "total_topics": fx.total_topics,
        "topics_started": fx.topics_completed,
        "topics_with_ek_evidence": fx.topics_with_ek_evidence,
    }


def _assert_withheld_display(claim: str, percentage: Any) -> None:
    assert percentage is None
    assert claim == EXAM_READINESS_NOT_YET_ASSESSABLE
    assert "not yet assessable" in claim.lower()
    assert "unprepared" not in claim.lower()
    assert_no_confident_exam_readiness_percent(claim)


@pytest.mark.parametrize(
    "fx",
    NAMED_ADVERSARIAL_FIXTURES,
    ids=[f.name for f in NAMED_ADVERSARIAL_FIXTURES],
)
def test_adversarial_fixture_student_facing_claim_withheld(
    fx: ExamReadinessAdversarialFixture,
) -> None:
    """No named fixture may produce a confident Exam Readiness % display."""
    claim = student_facing_exam_readiness_claim(
        coverage_pct=fx.coverage_pct,
        overall_score=fx.overall_score,
        avg_mastery=fx.avg_mastery,
        demonstrated=fx.demonstrated_evidence_present,
        assessment=fx.assessment_evidence_present,
        outside_syllabus=fx.outside_current_syllabus,
        conflicting=fx.conflicting_evidence,
        stale=fx.stale_curriculum_version,
    )
    percentage = student_facing_exam_readiness_percentage(
        coverage_pct=fx.coverage_pct,
        overall_score=fx.overall_score,
    )
    _assert_withheld_display(claim, percentage)


@pytest.mark.parametrize(
    "fx",
    NAMED_ADVERSARIAL_FIXTURES,
    ids=[f.name for f in NAMED_ADVERSARIAL_FIXTURES],
)
def test_adversarial_fixture_explain_composite_withheld(
    fx: ExamReadinessAdversarialFixture,
) -> None:
    narrative = EducationalExplainabilityService.explain_composite_readiness(
        _overall_shaped_dict(fx)
    )
    assert narrative.can_estimate is False
    assert narrative.percentage is None
    assert narrative.explanation == EXAM_READINESS_NOT_YET_ASSESSABLE
    assert_no_confident_exam_readiness_percent(narrative.explanation)


@pytest.mark.parametrize(
    "fx",
    NAMED_ADVERSARIAL_FIXTURES,
    ids=[f.name for f in NAMED_ADVERSARIAL_FIXTURES],
)
def test_adversarial_fixture_presentation_adapter_withheld(
    fx: ExamReadinessAdversarialFixture,
) -> None:
    surface = {
        "readiness": _overall_shaped_dict(fx),
        "source_authority": "legacy",
    }
    narrative = RuntimeAPresentationAdapter.readiness_narrative(surface)
    assert narrative.can_estimate is False
    assert narrative.percentage is None
    assert narrative.explanation == EXAM_READINESS_NOT_YET_ASSESSABLE
    assert_no_confident_exam_readiness_percent(narrative.explanation)


def test_high_coverage_low_evidence_matches_phase3_s7_shape() -> None:
    """Pin the exact 85.7% coverage / thin-evidence S7 shape from Phase 3."""
    fx = HIGH_COVERAGE_LOW_EVIDENCE
    assert fx.coverage_pct == pytest.approx(85.7)
    assert fx.topics_completed == 12
    assert fx.total_topics == 14
    assert fx.topics_with_ek_evidence == 0
    assert fx.demonstrated_evidence_present is False
    # Historical overall-from-coverage temptation (~61.2) must still withhold.
    claim = student_facing_exam_readiness_claim(overall_score=fx.overall_score)
    assert claim == EXAM_READINESS_NOT_YET_ASSESSABLE
    assert student_facing_exam_readiness_percentage(fx.overall_score) is None


def test_calculate_readiness_is_not_exam_readiness_authority() -> None:
    """Revoked helper may still compute coverage-shaped numbers for history.

    It must not be treated as a student-facing Exam Readiness claim.
    """

    class _Summary:
        weighted_completed_percentage = 0.857
        weighted_remaining_percentage = 0.143
        completed_topic_count = 12
        total_topic_count = 14
        remaining_topic_count = 2
        estimated_hours_remaining = 10.0

    summary = ReadinessService.calculate_readiness(_Summary())
    assert summary is not None
    # Historical coverage rename still returns a number internally...
    assert summary.readiness_percentage == pytest.approx(0.857)
    # ...but student-facing claim path must ignore it.
    claim = student_facing_exam_readiness_claim(
        calculate_readiness_percentage=summary.readiness_percentage
    )
    assert claim == EXAM_READINESS_NOT_YET_ASSESSABLE
    assert_no_confident_exam_readiness_percent(claim)
    assert EXAM_READINESS_NOT_YET_ASSESSABLE_SHORT in claim


def test_named_fixture_inventory_is_complete() -> None:
    names = {fx.name for fx in NAMED_ADVERSARIAL_FIXTURES}
    expected = {
        "HIGH_COVERAGE_LOW_EVIDENCE",
        "LOW_COVERAGE_HIGH_DEMONSTRATED_EVIDENCE",
        "HIGH_COVERAGE_HIGH_DEMONSTRATED_EVIDENCE",
        "HIGH_COVERAGE_NO_ASSESSMENT_EVIDENCE",
        "LOW_COVERAGE_NO_EVIDENCE",
        "COVERAGE_DATA_PRESENT_BUT_OUTSIDE_CURRENT_SYLLABUS",
        "CONFLICTING_EVIDENCE",
        "STALE_CURRICULUM_VERSION",
    }
    assert names == expected
    assert len(NAMED_ADVERSARIAL_FIXTURES) == 8
