"""Unit tests for the MasteryEstimator engine — the core reasoning surface."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from domain.education.educational_evidence import EvidenceSource, LearningEnvironment
from domain.education.educational_evidence.aggregates.educational_evidence import (
    EducationalEvidence,
)
from domain.education.educational_evidence.enums import LearningEnvironmentKind
from domain.education.educational_evidence.ids import EvidenceId
from domain.education.knowledge_graph import (
    DependencyStrength,
    KnowledgeGraph,
    KnowledgeGraphId,
    KnowledgeNode,
    KnowledgeNodeId,
    KnowledgeNodeKind,
    RelationshipType,
)
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.mastery_estimation.engines.mastery_estimator import (
    MasteryEstimator,
)
from domain.education.mastery_estimation.enums import (
    AssessmentReasonCode,
    KnowledgeGapKind,
    MasteryBand,
)
from domain.education.mastery_estimation.ids import (
    AssessmentId,
    CompetencyId,
    SubjectId,
)
from domain.education.mastery_estimation.value_objects.mastery_score import (
    MasteryScore,
)
from domain.education.student_state.aggregates.student_educational_state import (
    StudentEducationalState,
)
from domain.education.student_state.enums import MasteryBand as StateMasteryBand
from domain.education.student_state.enums import SubjectStatus
from domain.education.student_state.ids import (
    CompetencyId as StateCompetencyId,
)
from domain.education.student_state.ids import StudentEducationalStateId
from domain.education.student_state.ids import SubjectId as StateSubjectId
from domain.education.student_state.value_objects.competency_state import (
    CompetencyState,
)
from domain.education.student_state.value_objects.subject_state import SubjectState

AS_OF = datetime(2026, 7, 21, 12, 0, 0, tzinfo=UTC)
STUDENT_ID = "student-001"
SUBJECT_ALGEBRA = "algebra"
COMP_LINEAR = "linear-equations"
COMP_QUADRATIC = "quadratic-equations"


def make_evidence_source() -> EvidenceSource:
    return EvidenceSource.student_action("practice-app")


def make_learning_environment() -> LearningEnvironment:
    return LearningEnvironment.of(LearningEnvironmentKind.FREE_PRACTICE)


def make_question_evidence(
    *,
    evidence_id: str,
    competency_id: str = COMP_LINEAR,
    is_correct: bool,
    occurred_at: datetime = AS_OF,
    subject_id: str | None = SUBJECT_ALGEBRA,
) -> EducationalEvidence:
    return EducationalEvidence.record_question_answer(
        EvidenceId(evidence_id),
        STUDENT_ID,
        occurred_at,
        make_evidence_source(),
        learning_environment=make_learning_environment(),
        competency_id=competency_id,
        is_correct=is_correct,
        subject_id=subject_id,
    )


def make_confidence_evidence(
    *,
    evidence_id: str,
    competency_id: str = COMP_LINEAR,
    confidence_level: str,
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
        subject_id=SUBJECT_ALGEBRA,
        competency_id=competency_id,
    )


def make_student_state(
    *,
    subject_id: str = SUBJECT_ALGEBRA,
    competency_ids: tuple[str, ...] = (COMP_LINEAR,),
) -> StudentEducationalState:
    state = StudentEducationalState.create(
        StudentEducationalStateId("state-001"), STUDENT_ID
    )
    state.update_subject_state(
        SubjectState(subject_id=StateSubjectId(subject_id), status=SubjectStatus.ACTIVE)
    )
    for competency in competency_ids:
        state.update_competency(
            CompetencyState(
                competency_id=StateCompetencyId(competency),
                subject_id=StateSubjectId(subject_id),
                band=StateMasteryBand.DEVELOPING,
            )
        )
    return state


def make_knowledge_graph(
    *,
    nodes: tuple[str, ...] = (COMP_LINEAR, COMP_QUADRATIC),
    edges: tuple[tuple[str, str, DependencyStrength], ...] = (),
) -> KnowledgeGraph:
    graph = KnowledgeGraph.create(KnowledgeGraphId("graph-001"))
    for node_id in nodes:
        graph.add_node(
            KnowledgeNode(
                node_id=KnowledgeNodeId(node_id),
                label=node_id,
                kind=KnowledgeNodeKind.SKILL,
            )
        )
    for source, target, strength in edges:
        graph.connect(
            KnowledgeNodeId(source),
            KnowledgeNodeId(target),
            RelationshipType.PREREQUISITE,
            strength=strength,
        )
    return graph


class TestEstimateCompetency:
    def test_no_evidence_yields_not_assessed(self) -> None:
        graph = make_knowledge_graph()
        assessment = MasteryEstimator.estimate_competency(
            [],
            graph,
            competency_id=CompetencyId(COMP_LINEAR),
            subject_id=SubjectId(SUBJECT_ALGEBRA),
            as_of=AS_OF,
        )
        assert assessment.mastery.band is MasteryBand.NOT_ASSESSED
        assert assessment.reasons[0].reason_code is (
            AssessmentReasonCode.INSUFFICIENT_EVIDENCE
        )

    def test_correct_answers_yield_high_mastery(self) -> None:
        graph = make_knowledge_graph()
        evidence = [
            make_question_evidence(evidence_id="ev-1", is_correct=True),
            make_question_evidence(evidence_id="ev-2", is_correct=True),
        ]
        assessment = MasteryEstimator.estimate_competency(
            evidence,
            graph,
            competency_id=CompetencyId(COMP_LINEAR),
            subject_id=SubjectId(SUBJECT_ALGEBRA),
            as_of=AS_OF,
        )
        assert assessment.mastery.magnitude == pytest.approx(1.0)

    def test_evidence_only_influences_referenced_competency(self) -> None:
        graph = make_knowledge_graph()
        evidence = [
            make_question_evidence(
                evidence_id="ev-1", competency_id=COMP_QUADRATIC, is_correct=True
            )
        ]
        assessment = MasteryEstimator.estimate_competency(
            evidence,
            graph,
            competency_id=CompetencyId(COMP_LINEAR),
            subject_id=SubjectId(SUBJECT_ALGEBRA),
            as_of=AS_OF,
        )
        assert assessment.mastery.band is MasteryBand.NOT_ASSESSED
        assert assessment.evidence_count() == 0

    def test_contradictory_evidence_reduces_confidence_not_mastery_undefined(
        self,
    ) -> None:
        graph = make_knowledge_graph()
        evidence = [
            make_question_evidence(evidence_id="ev-1", is_correct=True),
            make_question_evidence(evidence_id="ev-2", is_correct=False),
        ]
        assessment = MasteryEstimator.estimate_competency(
            evidence,
            graph,
            competency_id=CompetencyId(COMP_LINEAR),
            subject_id=SubjectId(SUBJECT_ALGEBRA),
            as_of=AS_OF,
        )
        assert assessment.confidence.is_contradicted()
        assert 0.0 <= assessment.mastery.magnitude <= 1.0
        assert any(
            reason.reason_code is AssessmentReasonCode.CONTRADICTORY_EVIDENCE
            for reason in assessment.reasons
        )

    def test_weak_prerequisite_dampens_dependent_mastery(self) -> None:
        graph = make_knowledge_graph(
            edges=((COMP_QUADRATIC, COMP_LINEAR, DependencyStrength.critical()),)
        )
        weak_prereq_evidence = [
            make_question_evidence(evidence_id="ev-1", is_correct=False),
            make_question_evidence(evidence_id="ev-2", is_correct=False),
        ]
        dependent_evidence = [
            make_question_evidence(
                evidence_id="ev-3", competency_id=COMP_QUADRATIC, is_correct=True
            )
        ]
        evidence = weak_prereq_evidence + dependent_evidence

        with_prereq = MasteryEstimator.estimate_competency(
            evidence,
            graph,
            competency_id=CompetencyId(COMP_QUADRATIC),
            subject_id=SubjectId(SUBJECT_ALGEBRA),
            as_of=AS_OF,
        )
        without_prereq_graph = make_knowledge_graph()
        without_prereq = MasteryEstimator.estimate_competency(
            evidence,
            without_prereq_graph,
            competency_id=CompetencyId(COMP_QUADRATIC),
            subject_id=SubjectId(SUBJECT_ALGEBRA),
            as_of=AS_OF,
        )
        assert with_prereq.mastery.magnitude < without_prereq.mastery.magnitude
        assert with_prereq.weak_prerequisites()
        assert with_prereq.weak_prerequisites()[0].kind is (
            KnowledgeGapKind.WEAK_PREREQUISITE
        )

    def test_strong_prerequisite_does_not_dampen(self) -> None:
        graph = make_knowledge_graph(
            edges=((COMP_QUADRATIC, COMP_LINEAR, DependencyStrength.critical()),)
        )
        strong_prereq_evidence = [
            make_question_evidence(evidence_id="ev-1", is_correct=True),
            make_question_evidence(evidence_id="ev-2", is_correct=True),
        ]
        dependent_evidence = [
            make_question_evidence(
                evidence_id="ev-3", competency_id=COMP_QUADRATIC, is_correct=True
            )
        ]
        assessment = MasteryEstimator.estimate_competency(
            strong_prereq_evidence + dependent_evidence,
            graph,
            competency_id=CompetencyId(COMP_QUADRATIC),
            subject_id=SubjectId(SUBJECT_ALGEBRA),
            as_of=AS_OF,
        )
        assert not assessment.weak_prerequisites()
        assert assessment.mastery.magnitude == pytest.approx(1.0)

    def test_unregistered_competency_has_no_prerequisite_weaknesses(self) -> None:
        graph = make_knowledge_graph(nodes=(COMP_QUADRATIC,))
        gaps = MasteryEstimator.identify_prerequisite_weaknesses(
            CompetencyId(COMP_LINEAR), [], graph
        )
        assert gaps == ()

    def test_direct_gap_identified_for_weak_evidence(self) -> None:
        graph = make_knowledge_graph()
        evidence = [make_question_evidence(evidence_id="ev-1", is_correct=False)]
        assessment = MasteryEstimator.estimate_competency(
            evidence,
            graph,
            competency_id=CompetencyId(COMP_LINEAR),
            subject_id=SubjectId(SUBJECT_ALGEBRA),
            as_of=AS_OF,
        )
        assert assessment.direct_gaps()
        assert assessment.direct_gaps()[0].kind is KnowledgeGapKind.WEAK_EVIDENCE

    def test_secure_competency_has_no_direct_gap(self) -> None:
        graph = make_knowledge_graph()
        evidence = [
            make_question_evidence(evidence_id=f"ev-{i}", is_correct=True)
            for i in range(3)
        ]
        assessment = MasteryEstimator.estimate_competency(
            evidence,
            graph,
            competency_id=CompetencyId(COMP_LINEAR),
            subject_id=SubjectId(SUBJECT_ALGEBRA),
            as_of=AS_OF,
        )
        assert not assessment.direct_gaps()


class TestIdentifyKnowledgeGaps:
    def test_not_assessed_is_not_a_gap(self) -> None:
        gaps = MasteryEstimator.identify_knowledge_gaps(
            CompetencyId(COMP_LINEAR), MasteryScore.not_assessed()
        )
        assert gaps == ()

    def test_secure_mastery_is_not_a_gap(self) -> None:
        gaps = MasteryEstimator.identify_knowledge_gaps(
            CompetencyId(COMP_LINEAR),
            MasteryScore(magnitude=0.9, evidence_count=3),
        )
        assert gaps == ()

    def test_weak_mastery_is_a_gap(self) -> None:
        gaps = MasteryEstimator.identify_knowledge_gaps(
            CompetencyId(COMP_LINEAR),
            MasteryScore(magnitude=0.1, evidence_count=2),
        )
        assert len(gaps) == 1
        assert gaps[0].kind is KnowledgeGapKind.WEAK_EVIDENCE


class TestCalculateConfidenceAndStability:
    def test_calculate_confidence_delegates_to_policy_shape(self) -> None:
        evidence = [make_question_evidence(evidence_id="ev-1", is_correct=True)]
        contributions = MasteryEstimator._contributions_for(
            CompetencyId(COMP_LINEAR), evidence
        )
        confidence = MasteryEstimator.calculate_confidence(
            contributions, as_of=AS_OF
        )
        assert confidence.evidence_count == 1

    def test_calculate_learning_stability_insufficient_with_one_point(self) -> None:
        evidence = [make_question_evidence(evidence_id="ev-1", is_correct=True)]
        contributions = MasteryEstimator._contributions_for(
            CompetencyId(COMP_LINEAR), evidence
        )
        stability = MasteryEstimator.calculate_learning_stability(contributions)
        assert stability.band.value == "insufficient_data"


class TestEstimateSubject:
    def test_aggregates_across_tracked_competencies(self) -> None:
        state = make_student_state(
            competency_ids=(COMP_LINEAR, COMP_QUADRATIC)
        )
        graph = make_knowledge_graph()
        evidence = [
            make_question_evidence(evidence_id="ev-1", is_correct=True),
            make_question_evidence(
                evidence_id="ev-2", competency_id=COMP_QUADRATIC, is_correct=False
            ),
        ]
        subject_assessment = MasteryEstimator.estimate_subject(
            state,
            evidence,
            graph,
            subject_id=SubjectId(SUBJECT_ALGEBRA),
            as_of=AS_OF,
        )
        assert subject_assessment.competency_count() == 2
        assert subject_assessment.mastery.evidence_count == 2

    def test_untracked_competency_is_excluded(self) -> None:
        state = make_student_state(competency_ids=(COMP_LINEAR,))
        graph = make_knowledge_graph()
        evidence = [
            make_question_evidence(
                evidence_id="ev-1", competency_id=COMP_QUADRATIC, is_correct=True
            )
        ]
        subject_assessment = MasteryEstimator.estimate_subject(
            state,
            evidence,
            graph,
            subject_id=SubjectId(SUBJECT_ALGEBRA),
            as_of=AS_OF,
        )
        assert subject_assessment.competency_count() == 1
        assert subject_assessment.mastery.evidence_count == 0

    def test_empty_subject_yields_not_assessed(self) -> None:
        state = make_student_state(competency_ids=())
        graph = make_knowledge_graph()
        subject_assessment = MasteryEstimator.estimate_subject(
            state,
            [],
            graph,
            subject_id=SubjectId(SUBJECT_ALGEBRA),
            as_of=AS_OF,
        )
        assert subject_assessment.competency_count() == 0
        assert subject_assessment.mastery.band is MasteryBand.NOT_ASSESSED


class TestEstimateFullAssessment:
    def test_produces_assessment_for_every_tracked_subject(self) -> None:
        state = make_student_state(competency_ids=(COMP_LINEAR, COMP_QUADRATIC))
        graph = make_knowledge_graph()
        evidence = [
            make_question_evidence(evidence_id="ev-1", is_correct=True),
            make_question_evidence(
                evidence_id="ev-2", competency_id=COMP_QUADRATIC, is_correct=True
            ),
        ]
        assessment = MasteryEstimator.estimate(
            state,
            evidence,
            graph,
            assessment_id=AssessmentId("assessment-1"),
            assessed_at=AS_OF,
        )
        assert isinstance(assessment, MasteryAssessment)
        assert assessment.subject_count() == 1
        assert assessment.student_id == STUDENT_ID
        assert assessment.assessed_at == AS_OF

    def test_is_deterministic_for_identical_inputs(self) -> None:
        state = make_student_state(competency_ids=(COMP_LINEAR, COMP_QUADRATIC))
        graph = make_knowledge_graph(
            edges=((COMP_QUADRATIC, COMP_LINEAR, DependencyStrength.important()),)
        )
        evidence = [
            make_question_evidence(evidence_id="ev-1", is_correct=True),
            make_question_evidence(evidence_id="ev-2", is_correct=False),
            make_question_evidence(
                evidence_id="ev-3", competency_id=COMP_QUADRATIC, is_correct=True
            ),
        ]
        first = MasteryEstimator.estimate(
            state,
            evidence,
            graph,
            assessment_id=AssessmentId("assessment-1"),
            assessed_at=AS_OF,
        )
        second = MasteryEstimator.estimate(
            state,
            evidence,
            graph,
            assessment_id=AssessmentId("assessment-1"),
            assessed_at=AS_OF,
        )
        assert first == second
        assert first.overall_mastery == second.overall_mastery
        assert first.overall_confidence == second.overall_confidence
        assert first.overall_stability == second.overall_stability
        assert first.knowledge_gaps == second.knowledge_gaps

    def test_no_evidence_at_all_yields_not_assessed_overall(self) -> None:
        state = make_student_state(competency_ids=(COMP_LINEAR,))
        graph = make_knowledge_graph()
        assessment = MasteryEstimator.estimate(
            state,
            [],
            graph,
            assessment_id=AssessmentId("assessment-1"),
            assessed_at=AS_OF,
        )
        assert assessment.overall_mastery.band is MasteryBand.NOT_ASSESSED
        assert assessment.overall_confidence.score.magnitude == 0.0

    def test_no_subjects_tracked_yields_empty_assessment(self) -> None:
        state = StudentEducationalState.create(
            StudentEducationalStateId("state-empty"), STUDENT_ID
        )
        graph = make_knowledge_graph()
        assessment = MasteryEstimator.estimate(
            state,
            [],
            graph,
            assessment_id=AssessmentId("assessment-1"),
            assessed_at=AS_OF,
        )
        assert assessment.subject_count() == 0
        assert not assessment.has_knowledge_gaps()

    def test_produce_snapshot_matches_aggregate_snapshot(self) -> None:
        state = make_student_state()
        graph = make_knowledge_graph()
        evidence = [make_question_evidence(evidence_id="ev-1", is_correct=True)]
        assessment = MasteryEstimator.estimate(
            state,
            evidence,
            graph,
            assessment_id=AssessmentId("assessment-1"),
            assessed_at=AS_OF,
        )
        snapshot = MasteryEstimator.produce_snapshot(assessment)
        assert snapshot == assessment.produce_snapshot()

    def test_reasons_reflect_recency(self) -> None:
        state = make_student_state()
        graph = make_knowledge_graph()
        stale_time = AS_OF - timedelta(days=60)
        evidence = [
            make_question_evidence(
                evidence_id="ev-1", is_correct=True, occurred_at=stale_time
            )
        ]
        assessment = MasteryEstimator.estimate(
            state,
            evidence,
            graph,
            assessment_id=AssessmentId("assessment-1"),
            assessed_at=AS_OF,
        )
        competency_assessment = assessment.competency_assessment_for(
            CompetencyId(COMP_LINEAR)
        )
        assert any(
            reason.reason_code is AssessmentReasonCode.STALE_EVIDENCE
            for reason in competency_assessment.reasons
        )

    def test_confidence_report_evidence_contributes(self) -> None:
        state = make_student_state()
        graph = make_knowledge_graph()
        evidence = [
            make_confidence_evidence(evidence_id="ev-1", confidence_level="very_low")
        ]
        assessment = MasteryEstimator.estimate(
            state,
            evidence,
            graph,
            assessment_id=AssessmentId("assessment-1"),
            assessed_at=AS_OF,
        )
        competency_assessment = assessment.competency_assessment_for(
            CompetencyId(COMP_LINEAR)
        )
        assert competency_assessment.evidence_count() == 1
        assert competency_assessment.mastery.magnitude < 0.5
