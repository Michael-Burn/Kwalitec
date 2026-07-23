"""Targeted tests closing remaining branch-coverage gaps.

Covers type-guard rejection branches, ``__str__`` representations, and a
handful of engine branches (advisory-edge skipping, strong-negative-evidence
and volatile-performance reasons) not exercised by the primary test files.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from domain.education.educational_evidence.enums import EvidenceType
from domain.education.educational_evidence.ids import EvidenceId
from domain.education.educational_evidence.value_objects.evidence_timestamp import (
    EvidenceTimestamp,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph import (
    DependencyStrength,
    KnowledgeGraph,
    KnowledgeGraphId,
    KnowledgeNode,
    KnowledgeNodeId,
    KnowledgeNodeKind,
    RelationshipType,
)
from domain.education.mastery_estimation.engines.mastery_estimator import (
    MasteryEstimator,
)
from domain.education.mastery_estimation.enums import (
    AssessmentReasonCode,
    KnowledgeGapKind,
    KnowledgeGapSeverity,
)
from domain.education.mastery_estimation.ids import (
    AssessmentId,
    CompetencyId,
    SubjectId,
)
from domain.education.mastery_estimation.policies.assessment_validation_policy import (  # noqa: E501
    AssessmentValidationPolicy,
)
from domain.education.mastery_estimation.value_objects.assessment_reason import (
    AssessmentReason,
)
from domain.education.mastery_estimation.value_objects.assessment_snapshot import (
    AssessmentSnapshot,
)
from domain.education.mastery_estimation.value_objects.competency_assessment import (
    CompetencyAssessment,
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
from domain.education.mastery_estimation.value_objects.subject_assessment import (
    SubjectAssessment,
)

AS_OF = datetime(2026, 7, 21, 12, 0, 0, tzinfo=UTC)


class TestIdentityStringRepresentations:
    def test_ids_str_returns_value(self) -> None:
        assert str(AssessmentId("assessment-1")) == "assessment-1"
        assert str(SubjectId("algebra")) == "algebra"
        assert str(CompetencyId("comp-1")) == "comp-1"


class TestValueObjectStringRepresentations:
    def test_mastery_score_str(self) -> None:
        score = MasteryScore(magnitude=0.5, evidence_count=2)
        assert str(score) == f"{score.magnitude:.4f}:{score.band.value}"

    def test_confidence_score_str(self) -> None:
        score = ConfidenceScore(magnitude=0.5)
        assert str(score) == f"{score.magnitude:.4f}:{score.band.value}"

    def test_learning_stability_str(self) -> None:
        stability = LearningStability(magnitude=0.9, evidence_count=3, variance=0.1)
        assert str(stability) == f"{stability.magnitude:.4f}:{stability.band.value}"

    def test_evidence_contribution_str(self) -> None:
        contribution = EvidenceContribution(
            evidence_id=EvidenceId("ev-1"),
            evidence_type=EvidenceType.QUESTION_ANSWERED,
            contribution=0.5,
            weight=0.5,
            occurred_at=EvidenceTimestamp.of(AS_OF),
        )
        assert str(contribution) == f"{contribution.evidence_id.value}:+0.5000"

    def test_mastery_confidence_str_delegates_to_score(self) -> None:
        confidence = MasteryConfidence(score=ConfidenceScore(magnitude=0.7))
        assert str(confidence) == str(confidence.score)


class TestConfidenceScoreTypeGuards:
    def test_rejects_non_numeric_magnitude(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceScore(magnitude="high")  # type: ignore[arg-type]

    def test_is_at_least_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            ConfidenceScore(magnitude=0.5).is_at_least(0.5)  # type: ignore[arg-type]


class TestMasteryScoreTypeGuards:
    def test_rejects_non_numeric_magnitude(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasteryScore(magnitude="high")  # type: ignore[arg-type]

    def test_rejects_non_integer_evidence_count(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasteryScore(magnitude=0.5, evidence_count=1.5)  # type: ignore[arg-type]

    def test_is_at_least_rejects_wrong_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasteryScore(magnitude=0.5, evidence_count=1).is_at_least(0.5)  # type: ignore[arg-type]


class TestLearningStabilityTypeGuards:
    def test_rejects_non_numeric_magnitude(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningStability(magnitude="high", evidence_count=2, variance=0.1)  # type: ignore[arg-type]

    def test_rejects_non_integer_evidence_count(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningStability(magnitude=0.5, evidence_count=1.5, variance=0.1)  # type: ignore[arg-type]

    def test_rejects_negative_evidence_count(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            LearningStability(magnitude=0.5, evidence_count=-1, variance=0.1)


class TestEvidenceContributionTypeGuards:
    def test_rejects_wrong_evidence_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceContribution(
                evidence_id=EvidenceId("ev-1"),
                evidence_type="question_answered",  # type: ignore[arg-type]
                contribution=0.5,
                weight=0.5,
                occurred_at=EvidenceTimestamp.of(AS_OF),
            )

    def test_rejects_non_numeric_contribution(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceContribution(
                evidence_id=EvidenceId("ev-1"),
                evidence_type=EvidenceType.QUESTION_ANSWERED,
                contribution="high",  # type: ignore[arg-type]
                weight=0.5,
                occurred_at=EvidenceTimestamp.of(AS_OF),
            )

    def test_rejects_non_numeric_weight(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceContribution(
                evidence_id=EvidenceId("ev-1"),
                evidence_type=EvidenceType.QUESTION_ANSWERED,
                contribution=0.5,
                weight="high",  # type: ignore[arg-type]
                occurred_at=EvidenceTimestamp.of(AS_OF),
            )

    def test_rejects_non_timestamp_occurred_at(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceContribution(
                evidence_id=EvidenceId("ev-1"),
                evidence_type=EvidenceType.QUESTION_ANSWERED,
                contribution=0.5,
                weight=0.5,
                occurred_at=AS_OF,  # type: ignore[arg-type]
            )


class TestKnowledgeGapTypeGuards:
    def test_rejects_wrong_competency_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGap(
                competency_id="not-an-id",  # type: ignore[arg-type]
                kind=KnowledgeGapKind.WEAK_EVIDENCE,
                severity=KnowledgeGapSeverity.MINOR,
                mastery_score=MasteryScore(magnitude=0.4, evidence_count=1),
            )

    def test_rejects_wrong_kind_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGap(
                competency_id=CompetencyId("comp-1"),
                kind="weak_evidence",  # type: ignore[arg-type]
                severity=KnowledgeGapSeverity.MINOR,
                mastery_score=MasteryScore(magnitude=0.4, evidence_count=1),
            )

    def test_rejects_wrong_severity_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGap(
                competency_id=CompetencyId("comp-1"),
                kind=KnowledgeGapKind.WEAK_EVIDENCE,
                severity="minor",  # type: ignore[arg-type]
                mastery_score=MasteryScore(magnitude=0.4, evidence_count=1),
            )

    def test_rejects_wrong_mastery_score_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGap(
                competency_id=CompetencyId("comp-1"),
                kind=KnowledgeGapKind.WEAK_EVIDENCE,
                severity=KnowledgeGapSeverity.MINOR,
                mastery_score=0.4,  # type: ignore[arg-type]
            )

    def test_rejects_wrong_related_competency_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGap(
                competency_id=CompetencyId("comp-1"),
                kind=KnowledgeGapKind.WEAK_PREREQUISITE,
                severity=KnowledgeGapSeverity.SEVERE,
                mastery_score=MasteryScore(magnitude=0.1, evidence_count=1),
                related_competency_id="not-an-id",  # type: ignore[arg-type]
                dependency_strength=DependencyStrength.critical(),
            )

    def test_rejects_wrong_dependency_strength_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            KnowledgeGap(
                competency_id=CompetencyId("comp-1"),
                kind=KnowledgeGapKind.WEAK_PREREQUISITE,
                severity=KnowledgeGapSeverity.SEVERE,
                mastery_score=MasteryScore(magnitude=0.1, evidence_count=1),
                related_competency_id=CompetencyId("comp-2"),
                dependency_strength="critical",  # type: ignore[arg-type]
            )


class TestAssessmentReasonTypeGuards:
    def test_rejects_wrong_subject_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentReason(
                reason_code=AssessmentReasonCode.INSUFFICIENT_EVIDENCE,
                subject_id="algebra",  # type: ignore[arg-type]
            )

    def test_rejects_wrong_competency_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentReason(
                reason_code=AssessmentReasonCode.INSUFFICIENT_EVIDENCE,
                competency_id="comp-1",  # type: ignore[arg-type]
            )

    def test_rejects_non_numeric_detail(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentReason(
                reason_code=AssessmentReasonCode.INSUFFICIENT_EVIDENCE,
                detail="high",  # type: ignore[arg-type]
            )


class TestMasteryConfidenceTypeGuards:
    def test_rejects_wrong_score_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasteryConfidence(score=0.5)  # type: ignore[arg-type]

    def test_rejects_non_integer_evidence_count(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasteryConfidence(score=ConfidenceScore.zero(), evidence_count=1.5)  # type: ignore[arg-type]

    def test_rejects_non_numeric_contradiction_ratio(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasteryConfidence(
                score=ConfidenceScore.zero(), contradiction_ratio="high"
            )  # type: ignore[arg-type]

    def test_rejects_non_boolean_prerequisite_penalty_applied(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            MasteryConfidence(
                score=ConfidenceScore.zero(), prerequisite_penalty_applied="yes"
            )  # type: ignore[arg-type]


class TestCompetencyAssessmentTypeGuards:
    def _kwargs(self, **overrides: object) -> dict:
        base = {
            "competency_id": CompetencyId("comp-1"),
            "subject_id": SubjectId("algebra"),
            "mastery": MasteryScore.not_assessed(),
            "confidence": MasteryConfidence.zero(),
            "stability": LearningStability.insufficient_data(),
        }
        base.update(overrides)
        return base

    def test_rejects_wrong_competency_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyAssessment(**self._kwargs(competency_id="comp-1"))

    def test_rejects_wrong_subject_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyAssessment(**self._kwargs(subject_id="algebra"))

    def test_rejects_wrong_mastery_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyAssessment(**self._kwargs(mastery=0.5))

    def test_rejects_wrong_confidence_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyAssessment(**self._kwargs(confidence=0.5))

    def test_rejects_wrong_stability_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyAssessment(**self._kwargs(stability=0.5))

    def test_rejects_wrong_supporting_evidence_member_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyAssessment(
                **self._kwargs(supporting_evidence=("not-a-contribution",))
            )

    def test_rejects_wrong_gap_member_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyAssessment(**self._kwargs(gaps=("not-a-gap",)))

    def test_rejects_wrong_reason_member_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            CompetencyAssessment(**self._kwargs(reasons=("not-a-reason",)))


class TestSubjectAssessmentTypeGuards:
    def _kwargs(self, **overrides: object) -> dict:
        base = {
            "subject_id": SubjectId("algebra"),
            "mastery": MasteryScore.not_assessed(),
            "confidence": MasteryConfidence.zero(),
            "stability": LearningStability.insufficient_data(),
        }
        base.update(overrides)
        return base

    def test_rejects_wrong_subject_id_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            SubjectAssessment(**self._kwargs(subject_id="algebra"))

    def test_rejects_wrong_mastery_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            SubjectAssessment(**self._kwargs(mastery=0.5))

    def test_rejects_wrong_confidence_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            SubjectAssessment(**self._kwargs(confidence=0.5))

    def test_rejects_wrong_stability_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            SubjectAssessment(**self._kwargs(stability=0.5))

    def test_rejects_wrong_competency_assessment_member_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            SubjectAssessment(
                **self._kwargs(competency_assessments=("not-a-competency",))
            )


class TestAssessmentSnapshotTypeGuards:
    def _kwargs(self, **overrides: object) -> dict:
        base = {
            "assessment_id": AssessmentId("assessment-1"),
            "student_id": "student-001",
            "overall_mastery": MasteryScore.not_assessed(),
            "overall_confidence": MasteryConfidence.zero(),
            "overall_stability": LearningStability.insufficient_data(),
            "subject_assessments": (),
            "knowledge_gaps": (),
            "supporting_evidence": (),
            "reasons": (),
            "assessed_at": AS_OF,
        }
        base.update(overrides)
        return base

    def test_rejects_wrong_overall_mastery_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentSnapshot(**self._kwargs(overall_mastery=0.5))

    def test_rejects_wrong_overall_confidence_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentSnapshot(**self._kwargs(overall_confidence=0.5))

    def test_rejects_wrong_overall_stability_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentSnapshot(**self._kwargs(overall_stability=0.5))

    def test_rejects_wrong_subject_assessment_member_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentSnapshot(
                **self._kwargs(subject_assessments=("not-a-subject-assessment",))
            )

    def test_rejects_wrong_supporting_evidence_member_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentSnapshot(
                **self._kwargs(supporting_evidence=("not-a-contribution",))
            )

    def test_rejects_wrong_reason_member_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentSnapshot(**self._kwargs(reasons=("not-a-reason",)))


class TestAssessmentValidationPolicyKnowledgeGapTypeGuard:
    def test_assert_knowledge_gaps_rejects_wrong_member_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            AssessmentValidationPolicy.assert_knowledge_gaps(
                ["not-a-gap"], subject_assessments=()
            )


class TestMasteryAssessmentPropertiesAndEquality:
    def test_supporting_evidence_and_reasons_properties(self) -> None:
        from domain.education.mastery_estimation.aggregates.mastery_assessment import (  # noqa: E501
            MasteryAssessment,
        )

        contribution = EvidenceContribution(
            evidence_id=EvidenceId("ev-1"),
            evidence_type=EvidenceType.QUESTION_ANSWERED,
            contribution=0.5,
            weight=0.5,
            occurred_at=EvidenceTimestamp.of(AS_OF),
        )
        reason = AssessmentReason(
            reason_code=AssessmentReasonCode.INSUFFICIENT_EVIDENCE
        )
        assessment = MasteryAssessment(
            assessment_id=AssessmentId("assessment-1"),
            student_id="student-001",
            assessed_at=AS_OF,
            overall_mastery=MasteryScore.not_assessed(),
            overall_confidence=MasteryConfidence.zero(),
            overall_stability=LearningStability.insufficient_data(),
            supporting_evidence=(contribution,),
            reasons=(reason,),
        )
        assert assessment.supporting_evidence == (contribution,)
        assert assessment.reasons == (reason,)

    def test_equality_short_circuits_on_identity(self) -> None:
        from domain.education.mastery_estimation.aggregates.mastery_assessment import (  # noqa: E501
            MasteryAssessment,
        )

        assessment = MasteryAssessment(
            assessment_id=AssessmentId("assessment-1"),
            student_id="student-001",
            assessed_at=AS_OF,
            overall_mastery=MasteryScore.not_assessed(),
            overall_confidence=MasteryConfidence.zero(),
            overall_stability=LearningStability.insufficient_data(),
        )
        assert assessment == assessment


class TestEngineAdvisoryEdgesAreSkipped:
    def test_advisory_relationship_is_not_treated_as_prerequisite(self) -> None:
        graph = KnowledgeGraph.create(KnowledgeGraphId("graph-advisory"))
        graph.add_node(
            KnowledgeNode(
                node_id=KnowledgeNodeId("comp-1"),
                label="comp-1",
                kind=KnowledgeNodeKind.SKILL,
            )
        )
        graph.add_node(
            KnowledgeNode(
                node_id=KnowledgeNodeId("comp-2"),
                label="comp-2",
                kind=KnowledgeNodeKind.SKILL,
            )
        )
        graph.connect(
            KnowledgeNodeId("comp-1"),
            KnowledgeNodeId("comp-2"),
            RelationshipType.RELATED,
        )
        gaps = MasteryEstimator.identify_prerequisite_weaknesses(
            CompetencyId("comp-1"), [], graph
        )
        assert gaps == ()


class TestEngineReasonBranches:
    def test_strong_negative_evidence_reason(self) -> None:
        from domain.education.educational_evidence import (
            EvidenceSource,
            LearningEnvironment,
        )
        from domain.education.educational_evidence.aggregates.educational_evidence import (  # noqa: E501
            EducationalEvidence,
        )
        from domain.education.educational_evidence.enums import (
            LearningEnvironmentKind,
        )

        graph = KnowledgeGraph.create(KnowledgeGraphId("graph-neg"))
        graph.add_node(
            KnowledgeNode(
                node_id=KnowledgeNodeId("comp-1"),
                label="comp-1",
                kind=KnowledgeNodeKind.SKILL,
            )
        )
        evidence = [
            EducationalEvidence.record_question_answer(
                EvidenceId(f"ev-{i}"),
                "student-001",
                AS_OF,
                EvidenceSource.student_action("app"),
                learning_environment=LearningEnvironment.of(
                    LearningEnvironmentKind.FREE_PRACTICE
                ),
                competency_id="comp-1",
                is_correct=False,
            )
            for i in range(2)
        ]
        assessment = MasteryEstimator.estimate_competency(
            evidence,
            graph,
            competency_id=CompetencyId("comp-1"),
            subject_id=SubjectId("algebra"),
            as_of=AS_OF,
        )
        assert any(
            reason.reason_code is AssessmentReasonCode.STRONG_NEGATIVE_EVIDENCE
            for reason in assessment.reasons
        )

    def test_volatile_performance_reason(self) -> None:
        from domain.education.educational_evidence import (
            EvidenceSource,
            LearningEnvironment,
        )
        from domain.education.educational_evidence.aggregates.educational_evidence import (  # noqa: E501
            EducationalEvidence,
        )
        from domain.education.educational_evidence.enums import (
            LearningEnvironmentKind,
        )

        graph = KnowledgeGraph.create(KnowledgeGraphId("graph-volatile"))
        graph.add_node(
            KnowledgeNode(
                node_id=KnowledgeNodeId("comp-1"),
                label="comp-1",
                kind=KnowledgeNodeKind.SKILL,
            )
        )
        evidence = [
            EducationalEvidence.record_question_answer(
                EvidenceId("ev-1"),
                "student-001",
                AS_OF,
                EvidenceSource.student_action("app"),
                learning_environment=LearningEnvironment.of(
                    LearningEnvironmentKind.FREE_PRACTICE
                ),
                competency_id="comp-1",
                is_correct=True,
                weight=1.0,
            ),
            EducationalEvidence.record_question_answer(
                EvidenceId("ev-2"),
                "student-001",
                AS_OF + timedelta(days=1),
                EvidenceSource.student_action("app"),
                learning_environment=LearningEnvironment.of(
                    LearningEnvironmentKind.FREE_PRACTICE
                ),
                competency_id="comp-1",
                is_correct=False,
                weight=1.0,
            ),
        ]
        assessment = MasteryEstimator.estimate_competency(
            evidence,
            graph,
            competency_id=CompetencyId("comp-1"),
            subject_id=SubjectId("algebra"),
            as_of=AS_OF + timedelta(days=1),
        )
        assert any(
            reason.reason_code is AssessmentReasonCode.VOLATILE_PERFORMANCE
            for reason in assessment.reasons
        )
