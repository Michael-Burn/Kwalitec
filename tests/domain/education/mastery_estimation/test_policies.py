"""Unit tests for Mastery Estimation policies."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from domain.education.educational_evidence import EvidenceSource, LearningEnvironment
from domain.education.educational_evidence.aggregates.educational_evidence import (
    EducationalEvidence,
)
from domain.education.educational_evidence.enums import (
    EvidenceType,
    LearningEnvironmentKind,
)
from domain.education.educational_evidence.ids import EvidenceId
from domain.education.educational_evidence.value_objects.evidence_timestamp import (
    EvidenceTimestamp,
)
from domain.education.knowledge_graph.enums import DependencyStrengthBand
from domain.education.knowledge_graph.value_objects.dependency_strength import (
    DependencyStrength,
)
from domain.education.mastery_estimation.enums import (
    KnowledgeGapKind,
    KnowledgeGapSeverity,
)
from domain.education.mastery_estimation.ids import CompetencyId
from domain.education.mastery_estimation.policies.confidence_policy import (
    ConfidencePolicy,
)
from domain.education.mastery_estimation.policies.evidence_weight_policy import (
    EvidenceWeightPolicy,
)
from domain.education.mastery_estimation.policies.mastery_policy import (
    MasteryPolicy,
)
from domain.education.mastery_estimation.policies.prerequisite_influence_policy import (  # noqa: E501
    PrerequisiteInfluencePolicy,
)
from domain.education.mastery_estimation.policies.stability_policy import (
    StabilityPolicy,
)
from domain.education.mastery_estimation.value_objects.confidence_score import (
    ConfidenceScore,
)
from domain.education.mastery_estimation.value_objects.evidence_contribution import (
    EvidenceContribution,
)
from domain.education.mastery_estimation.value_objects.knowledge_gap import (
    KnowledgeGap,
)
from domain.education.mastery_estimation.value_objects.learning_stability import (
    LearningStability,
)
from domain.education.mastery_estimation.value_objects.mastery_confidence import (
    MasteryConfidence,
)
from domain.education.mastery_estimation.value_objects.mastery_score import (
    MasteryScore,
)

AS_OF = datetime(2026, 7, 21, 12, 0, 0, tzinfo=UTC)
STUDENT_ID = "student-001"


def make_evidence(
    *,
    evidence_id: str = "ev-1",
    is_correct: bool = True,
    competency_id: str = "comp-1",
    occurred_at: datetime = AS_OF,
    weight: float | None = None,
) -> EducationalEvidence:
    return EducationalEvidence.record_question_answer(
        EvidenceId(evidence_id),
        STUDENT_ID,
        occurred_at,
        EvidenceSource.student_action("practice-app"),
        learning_environment=LearningEnvironment.of(
            LearningEnvironmentKind.FREE_PRACTICE
        ),
        competency_id=competency_id,
        is_correct=is_correct,
        weight=weight,
    )


def make_confidence_evidence(
    *,
    evidence_id: str = "ev-conf",
    confidence_level: str = "high",
    competency_id: str = "comp-1",
    occurred_at: datetime = AS_OF,
) -> EducationalEvidence:
    return EducationalEvidence.record_confidence(
        EvidenceId(evidence_id),
        STUDENT_ID,
        occurred_at,
        EvidenceSource.self_report("survey"),
        learning_environment=LearningEnvironment.of(
            LearningEnvironmentKind.REFLECTION_PROMPT
        ),
        confidence_level=confidence_level,
        competency_id=competency_id,
    )


def make_contribution(
    *,
    evidence_id: str = "ev-1",
    contribution: float = 1.0,
    weight: float = 0.5,
    occurred_at: datetime = AS_OF,
) -> EvidenceContribution:
    return EvidenceContribution(
        evidence_id=EvidenceId(evidence_id),
        evidence_type=EvidenceType.QUESTION_ANSWERED,
        contribution=contribution,
        weight=weight,
        occurred_at=EvidenceTimestamp.of(occurred_at),
    )


class TestEvidenceWeightPolicy:
    def test_correct_answer_is_positive_signal(self) -> None:
        contribution = EvidenceWeightPolicy.contribution_for(
            make_evidence(is_correct=True)
        )
        assert contribution.is_positive()

    def test_incorrect_answer_is_negative_signal(self) -> None:
        contribution = EvidenceWeightPolicy.contribution_for(
            make_evidence(is_correct=False)
        )
        assert contribution.is_negative()

    def test_polarity_classification_helpers(self) -> None:
        assert EvidenceWeightPolicy.is_positive_signal(EvidenceType.QUESTION_ANSWERED)
        assert EvidenceWeightPolicy.is_negative_signal(
            EvidenceType.QUESTION_INCORRECT
        )
        assert EvidenceWeightPolicy.is_neutral_signal(
            EvidenceType.STUDY_SESSION_STARTED
        )

    def test_unmapped_evidence_type_is_neutral(self) -> None:
        evidence = EducationalEvidence.record_session_start(
            EvidenceId("ev-session"),
            STUDENT_ID,
            AS_OF,
            EvidenceSource.system_observation("app"),
            learning_environment=LearningEnvironment.of(
                LearningEnvironmentKind.STUDY_SESSION
            ),
            learning_episode_id="episode-1",
        )
        contribution = EvidenceWeightPolicy.contribution_for(evidence)
        assert contribution.is_neutral()

    def test_confidence_report_scaled_by_reported_level(self) -> None:
        high = EvidenceWeightPolicy.contribution_for(
            make_confidence_evidence(confidence_level="very_high")
        )
        low = EvidenceWeightPolicy.contribution_for(
            make_confidence_evidence(
                evidence_id="ev-conf-2", confidence_level="very_low"
            )
        )
        assert high.is_positive()
        assert low.is_negative()
        assert abs(high.contribution) < 1.0

    def test_confidence_report_unknown_level_defaults_neutral(self) -> None:
        contribution = EvidenceWeightPolicy.contribution_for(
            make_confidence_evidence(confidence_level="medium")
        )
        assert contribution.is_neutral()


class TestMasteryPolicy:
    def test_no_contributions_is_not_assessed(self) -> None:
        score = MasteryPolicy.aggregate_contributions([])
        assert score.band.value == "not_assessed"
        assert score.evidence_count == 0

    def test_all_positive_contributions_yield_full_magnitude(self) -> None:
        contributions = [
            make_contribution(evidence_id="a", contribution=1.0, weight=0.5),
            make_contribution(evidence_id="b", contribution=1.0, weight=0.5),
        ]
        score = MasteryPolicy.aggregate_contributions(contributions)
        assert score.magnitude == pytest.approx(1.0)
        assert score.evidence_count == 2

    def test_all_negative_contributions_yield_zero_magnitude(self) -> None:
        contributions = [make_contribution(contribution=-1.0, weight=0.5)]
        score = MasteryPolicy.aggregate_contributions(contributions)
        assert score.magnitude == pytest.approx(0.0)

    def test_mixed_contributions_yield_proportional_magnitude(self) -> None:
        contributions = [
            make_contribution(evidence_id="a", contribution=1.0, weight=0.6),
            make_contribution(evidence_id="b", contribution=-1.0, weight=0.4),
        ]
        score = MasteryPolicy.aggregate_contributions(contributions)
        assert score.magnitude == pytest.approx(0.6)

    def test_all_neutral_contributions_yield_default_neutral_magnitude(self) -> None:
        contributions = [make_contribution(contribution=0.0, weight=0.5)]
        score = MasteryPolicy.aggregate_contributions(contributions)
        assert score.magnitude == pytest.approx(0.5)
        assert score.evidence_count == 1

    def test_dampening_noop_without_weak_prerequisites(self) -> None:
        score = MasteryScore(magnitude=0.8, evidence_count=2)
        dampened = MasteryPolicy.apply_prerequisite_dampening(score, [])
        assert dampened == score

    def test_dampening_noop_when_no_evidence(self) -> None:
        score = MasteryScore.not_assessed()
        gap = KnowledgeGap(
            competency_id=CompetencyId("prereq"),
            kind=KnowledgeGapKind.WEAK_PREREQUISITE,
            severity=KnowledgeGapSeverity.SEVERE,
            mastery_score=MasteryScore(magnitude=0.1, evidence_count=1),
            related_competency_id=CompetencyId("dependent"),
            dependency_strength=DependencyStrength.critical(),
        )
        dampened = MasteryPolicy.apply_prerequisite_dampening(score, [gap])
        assert dampened == score

    def test_dampening_reduces_magnitude_when_prerequisite_weak(self) -> None:
        score = MasteryScore(magnitude=0.9, evidence_count=3)
        gap = KnowledgeGap(
            competency_id=CompetencyId("prereq"),
            kind=KnowledgeGapKind.WEAK_PREREQUISITE,
            severity=KnowledgeGapSeverity.SEVERE,
            mastery_score=MasteryScore(magnitude=0.0, evidence_count=2),
            related_competency_id=CompetencyId("dependent"),
            dependency_strength=DependencyStrength.critical(),
        )
        dampened = MasteryPolicy.apply_prerequisite_dampening(score, [gap])
        assert dampened.magnitude < score.magnitude
        assert dampened.evidence_count == score.evidence_count

    def test_aggregate_subject_scores_weighted_by_evidence(self) -> None:
        scores = [
            MasteryScore(magnitude=1.0, evidence_count=1),
            MasteryScore(magnitude=0.0, evidence_count=3),
        ]
        aggregate = MasteryPolicy.aggregate_subject_scores(scores)
        assert aggregate.magnitude == pytest.approx(0.25)
        assert aggregate.evidence_count == 4

    def test_aggregate_subject_scores_ignores_unassessed(self) -> None:
        scores = [
            MasteryScore.not_assessed(),
            MasteryScore(magnitude=0.5, evidence_count=1),
        ]
        aggregate = MasteryPolicy.aggregate_subject_scores(scores)
        assert aggregate.evidence_count == 1

    def test_aggregate_subject_scores_all_unassessed(self) -> None:
        aggregate = MasteryPolicy.aggregate_subject_scores(
            [MasteryScore.not_assessed()]
        )
        assert aggregate.evidence_count == 0

    def test_classify_gap_severity_none_when_no_evidence(self) -> None:
        assert MasteryPolicy.classify_gap_severity(MasteryScore.not_assessed()) is None

    def test_classify_gap_severity_none_when_secure(self) -> None:
        secure = MasteryScore(magnitude=0.70, evidence_count=2)
        assert MasteryPolicy.classify_gap_severity(secure) is None

    def test_classify_gap_severity_bands(self) -> None:
        assert MasteryPolicy.classify_gap_severity(
            MasteryScore(magnitude=0.10, evidence_count=1)
        ) is KnowledgeGapSeverity.SEVERE
        assert MasteryPolicy.classify_gap_severity(
            MasteryScore(magnitude=0.35, evidence_count=1)
        ) is KnowledgeGapSeverity.MODERATE
        assert MasteryPolicy.classify_gap_severity(
            MasteryScore(magnitude=0.50, evidence_count=1)
        ) is KnowledgeGapSeverity.MINOR


class TestPrerequisiteInfluencePolicy:
    def test_no_evidence_prerequisite_is_never_weak(self) -> None:
        assert not PrerequisiteInfluencePolicy.is_weak(MasteryScore.not_assessed())

    def test_low_mastery_prerequisite_is_weak(self) -> None:
        assert PrerequisiteInfluencePolicy.is_weak(
            MasteryScore(magnitude=0.2, evidence_count=1)
        )

    def test_secure_prerequisite_is_not_weak(self) -> None:
        assert not PrerequisiteInfluencePolicy.is_weak(
            MasteryScore(magnitude=0.9, evidence_count=1)
        )

    def test_dampening_factor_is_identity_when_not_weak(self) -> None:
        factor = PrerequisiteInfluencePolicy.dampening_factor(
            DependencyStrength.critical(),
            MasteryScore(magnitude=0.9, evidence_count=1),
        )
        assert factor == 1.0

    def test_dampening_factor_scales_with_band_intensity(self) -> None:
        weak_score = MasteryScore(magnitude=0.0, evidence_count=1)
        critical_factor = PrerequisiteInfluencePolicy.dampening_factor(
            DependencyStrength.critical(), weak_score
        )
        optional_factor = PrerequisiteInfluencePolicy.dampening_factor(
            DependencyStrength.optional(), weak_score
        )
        assert critical_factor < optional_factor

    def test_classify_severity_floor_by_band(self) -> None:
        mild_deficiency = MasteryScore(magnitude=0.55, evidence_count=1)
        assert PrerequisiteInfluencePolicy.classify_severity(
            mild_deficiency, DependencyStrength.optional()
        ) is KnowledgeGapSeverity.MINOR
        assert PrerequisiteInfluencePolicy.classify_severity(
            mild_deficiency, DependencyStrength.important()
        ) is KnowledgeGapSeverity.MODERATE

    def test_classify_severity_escalates_on_large_deficiency(self) -> None:
        severe_deficiency = MasteryScore(magnitude=0.0, evidence_count=1)
        result = PrerequisiteInfluencePolicy.classify_severity(
            severe_deficiency, DependencyStrength.helpful()
        )
        assert result is KnowledgeGapSeverity.MODERATE

    def test_classify_severity_critical_escalation(self) -> None:
        severe_deficiency = MasteryScore(magnitude=0.0, evidence_count=1)
        result = PrerequisiteInfluencePolicy.classify_severity(
            severe_deficiency, DependencyStrength.critical()
        )
        assert result is KnowledgeGapSeverity.CRITICAL

    def test_band_intensity_covers_all_bands(self) -> None:
        weak_score = MasteryScore(magnitude=0.1, evidence_count=1)
        for band in DependencyStrengthBand:
            strength = DependencyStrength(band=band)
            factor = PrerequisiteInfluencePolicy.dampening_factor(strength, weak_score)
            assert 0.0 <= factor <= 1.0


class TestConfidencePolicy:
    def test_no_contributions_yields_zero_confidence(self) -> None:
        confidence = ConfidencePolicy.calculate([], as_of=AS_OF)
        assert confidence.score.magnitude == 0.0
        assert confidence.evidence_count == 0

    def test_contradictory_evidence_reduces_confidence(self) -> None:
        agreeing = [
            make_contribution(evidence_id="a", contribution=1.0, weight=0.5),
            make_contribution(evidence_id="b", contribution=1.0, weight=0.5),
        ]
        conflicting = [
            make_contribution(evidence_id="c", contribution=1.0, weight=0.5),
            make_contribution(evidence_id="d", contribution=-1.0, weight=0.5),
        ]
        agreeing_confidence = ConfidencePolicy.calculate(agreeing, as_of=AS_OF)
        conflicting_confidence = ConfidencePolicy.calculate(conflicting, as_of=AS_OF)
        assert conflicting_confidence.contradiction_ratio > 0.0
        assert (
            conflicting_confidence.score.magnitude
            < agreeing_confidence.score.magnitude
        )

    def test_contradiction_ratio_symmetric_conflict_is_maximal(self) -> None:
        contributions = [
            make_contribution(evidence_id="a", contribution=1.0, weight=0.5),
            make_contribution(evidence_id="b", contribution=-1.0, weight=0.5),
        ]
        ratio = ConfidencePolicy.contradiction_ratio(contributions)
        assert ratio == pytest.approx(1.0)

    def test_contradiction_ratio_zero_when_one_directional(self) -> None:
        contributions = [make_contribution(contribution=1.0, weight=0.5)]
        assert ConfidencePolicy.contradiction_ratio(contributions) == 0.0

    def test_contradiction_ratio_zero_when_no_directional_weight(self) -> None:
        contributions = [make_contribution(contribution=0.0, weight=0.5)]
        assert ConfidencePolicy.contradiction_ratio(contributions) == 0.0

    def test_recency_factor_is_maximal_for_current_evidence(self) -> None:
        contributions = [make_contribution(occurred_at=AS_OF)]
        assert ConfidencePolicy.recency_factor(contributions, as_of=AS_OF) == 1.0

    def test_recency_factor_is_zero_beyond_window(self) -> None:
        stale = AS_OF - timedelta(days=60)
        contributions = [make_contribution(occurred_at=stale)]
        assert ConfidencePolicy.recency_factor(contributions, as_of=AS_OF) == 0.0

    def test_recency_factor_empty_is_zero(self) -> None:
        assert ConfidencePolicy.recency_factor([], as_of=AS_OF) == 0.0

    def test_recency_factor_decays_linearly_within_window(self) -> None:
        halfway = AS_OF - timedelta(days=15)
        contributions = [make_contribution(occurred_at=halfway)]
        factor = ConfidencePolicy.recency_factor(contributions, as_of=AS_OF)
        assert 0.0 < factor < 1.0

    def test_weak_prerequisites_apply_penalty(self) -> None:
        contributions = [make_contribution(contribution=1.0, weight=0.9)]
        gap = KnowledgeGap(
            competency_id=CompetencyId("prereq"),
            kind=KnowledgeGapKind.WEAK_PREREQUISITE,
            severity=KnowledgeGapSeverity.SEVERE,
            mastery_score=MasteryScore(magnitude=0.1, evidence_count=1),
            related_competency_id=CompetencyId("dependent"),
            dependency_strength=DependencyStrength.critical(),
        )
        without_penalty = ConfidencePolicy.calculate(contributions, as_of=AS_OF)
        with_penalty = ConfidencePolicy.calculate(
            contributions, as_of=AS_OF, weak_prerequisites=[gap]
        )
        assert with_penalty.prerequisite_penalty_applied
        assert not without_penalty.prerequisite_penalty_applied
        assert with_penalty.score.magnitude < without_penalty.score.magnitude

    def test_aggregate_subject_confidence_empty_is_zero(self) -> None:
        confidence = ConfidencePolicy.aggregate_subject_confidence([])
        assert confidence.score.magnitude == 0.0

    def test_aggregate_subject_confidence_weighted_by_evidence(self) -> None:
        high = MasteryConfidence(
            score=ConfidenceScore(magnitude=1.0),
            evidence_count=1,
        )
        low = MasteryConfidence(
            score=ConfidenceScore(magnitude=0.0),
            evidence_count=3,
        )
        aggregate = ConfidencePolicy.aggregate_subject_confidence([high, low])
        assert aggregate.score.magnitude == pytest.approx(0.25)
        assert aggregate.evidence_count == 4

    def test_aggregate_subject_confidence_ignores_zero_evidence(self) -> None:
        aggregate = ConfidencePolicy.aggregate_subject_confidence(
            [MasteryConfidence.zero()]
        )
        assert aggregate.evidence_count == 0


class TestStabilityPolicy:
    def test_below_minimum_evidence_is_insufficient(self) -> None:
        stability = StabilityPolicy.calculate([make_contribution()])
        assert stability.band.value == "insufficient_data"

    def test_consistent_contributions_yield_high_stability(self) -> None:
        contributions = [
            make_contribution(evidence_id="a", contribution=0.8, occurred_at=AS_OF),
            make_contribution(
                evidence_id="b",
                contribution=0.8,
                occurred_at=AS_OF + timedelta(days=1),
            ),
        ]
        stability = StabilityPolicy.calculate(contributions)
        assert stability.magnitude == pytest.approx(1.0)
        assert stability.variance == pytest.approx(0.0)

    def test_volatile_contributions_yield_low_stability(self) -> None:
        contributions = [
            make_contribution(evidence_id="a", contribution=1.0, occurred_at=AS_OF),
            make_contribution(
                evidence_id="b",
                contribution=-1.0,
                occurred_at=AS_OF + timedelta(days=1),
            ),
        ]
        stability = StabilityPolicy.calculate(contributions)
        assert stability.variance == pytest.approx(1.0)
        assert stability.magnitude == pytest.approx(0.0)

    def test_aggregate_subject_stability_empty_is_insufficient(self) -> None:
        aggregate = StabilityPolicy.aggregate_subject_stability([])
        assert aggregate.band.value == "insufficient_data"

    def test_aggregate_subject_stability_filters_insufficient_members(self) -> None:
        insufficient = LearningStability.insufficient_data()
        sufficient = LearningStability(magnitude=0.8, evidence_count=2, variance=0.2)
        aggregate = StabilityPolicy.aggregate_subject_stability(
            [insufficient, sufficient]
        )
        assert aggregate.evidence_count == 2
        assert aggregate.magnitude == pytest.approx(0.8)

    def test_aggregate_subject_stability_weighted_by_evidence(self) -> None:
        low = LearningStability(magnitude=0.0, evidence_count=2, variance=1.0)
        high = LearningStability(magnitude=1.0, evidence_count=6, variance=0.0)
        aggregate = StabilityPolicy.aggregate_subject_stability([low, high])
        assert aggregate.evidence_count == 8
        assert aggregate.magnitude == pytest.approx(0.75)
