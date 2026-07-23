"""Shared factories for Recommendation Engine domain tests."""

from __future__ import annotations

from datetime import UTC, datetime

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
from domain.education.mastery_estimation.enums import (
    AssessmentReasonCode,
    KnowledgeGapKind,
    KnowledgeGapSeverity,
    LearningStabilityBand,
)
from domain.education.mastery_estimation.ids import (
    AssessmentId,
)
from domain.education.mastery_estimation.ids import (
    CompetencyId as MasteryCompetencyId,
)
from domain.education.mastery_estimation.ids import (
    SubjectId as MasterySubjectId,
)
from domain.education.mastery_estimation.value_objects.assessment_reason import (
    AssessmentReason,
)
from domain.education.mastery_estimation.value_objects.competency_assessment import (
    CompetencyAssessment,
)
from domain.education.mastery_estimation.value_objects.confidence_score import (
    ConfidenceScore,
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
from domain.education.recommendation_engine import (
    CompetencyId,
    RecommendationSetId,
    SubjectId,
)
from domain.education.student_state.aggregates.student_educational_state import (
    StudentEducationalState,
)
from domain.education.student_state.enums import MasteryBand as StateMasteryBand
from domain.education.student_state.enums import SubjectStatus
from domain.education.student_state.ids import (
    CheckpointId,
    MissionId,
    StudentEducationalStateId,
)
from domain.education.student_state.ids import (
    CompetencyId as StateCompetencyId,
)
from domain.education.student_state.ids import SubjectId as StateSubjectId
from domain.education.student_state.value_objects.competency_state import (
    CompetencyState,
)
from domain.education.student_state.value_objects.state_references import (
    CheckpointReference,
    MissionReference,
)
from domain.education.student_state.value_objects.subject_state import SubjectState

STUDENT_ID = "student-001"
SUBJECT_ALGEBRA = "algebra"
COMPETENCY_LINEAR_EQUATIONS = "linear-equations"
COMPETENCY_QUADRATIC_EQUATIONS = "quadratic-equations"


@pytest.fixture
def as_of() -> datetime:
    return datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def set_id() -> RecommendationSetId:
    return RecommendationSetId("recset-001")


@pytest.fixture
def subject_id() -> SubjectId:
    return SubjectId(SUBJECT_ALGEBRA)


@pytest.fixture
def competency_id() -> CompetencyId:
    return CompetencyId(COMPETENCY_LINEAR_EQUATIONS)


def make_evidence_source() -> EvidenceSource:
    return EvidenceSource.student_action("practice-app")


def make_learning_environment() -> LearningEnvironment:
    return LearningEnvironment.of(LearningEnvironmentKind.FREE_PRACTICE)


def make_question_evidence(
    *,
    evidence_id: str,
    competency_id: str = COMPETENCY_LINEAR_EQUATIONS,
    is_correct: bool,
    occurred_at: datetime,
    weight: float | None = None,
) -> EducationalEvidence:
    return EducationalEvidence.record_question_answer(
        EvidenceId(evidence_id),
        STUDENT_ID,
        occurred_at,
        make_evidence_source(),
        learning_environment=make_learning_environment(),
        competency_id=competency_id,
        is_correct=is_correct,
        subject_id=SUBJECT_ALGEBRA,
        weight=weight,
    )


def make_student_state(
    *,
    subject_id: str = SUBJECT_ALGEBRA,
    competency_ids: tuple[str, ...] = (COMPETENCY_LINEAR_EQUATIONS,),
    with_mission: bool = False,
    with_checkpoint: bool = False,
) -> StudentEducationalState:
    state = StudentEducationalState.create(
        StudentEducationalStateId("state-001"), STUDENT_ID
    )
    state.update_subject_state(
        SubjectState(
            subject_id=StateSubjectId(subject_id),
            status=SubjectStatus.ACTIVE,
        )
    )
    for competency in competency_ids:
        state.update_competency(
            CompetencyState(
                competency_id=StateCompetencyId(competency),
                subject_id=StateSubjectId(subject_id),
                band=StateMasteryBand.DEVELOPING,
            )
        )
    if with_mission:
        state.attach_current_mission(
            MissionReference(mission_id=MissionId("mission-001"), label="Daily")
        )
    if with_checkpoint:
        state.attach_checkpoint(
            CheckpointReference(
                checkpoint_id=CheckpointId("checkpoint-001"),
                label="Midterm",
            )
        )
    return state


def make_knowledge_graph(
    *,
    graph_id: str = "graph-001",
    nodes: tuple[str, ...] = (
        COMPETENCY_LINEAR_EQUATIONS,
        COMPETENCY_QUADRATIC_EQUATIONS,
    ),
    edges: tuple[tuple[str, str, DependencyStrength | None], ...] = (),
) -> KnowledgeGraph:
    graph = KnowledgeGraph.create(KnowledgeGraphId(graph_id))
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


def make_mastery_confidence(
    *,
    magnitude: float = 0.5,
    evidence_count: int = 3,
    contradiction_ratio: float = 0.0,
) -> MasteryConfidence:
    return MasteryConfidence(
        score=ConfidenceScore(magnitude=magnitude),
        evidence_count=evidence_count,
        contradiction_ratio=contradiction_ratio,
        recency_factor=0.7,
    )


def make_stability(
    *,
    magnitude: float = 0.8,
    evidence_count: int = 3,
    band_hint: LearningStabilityBand | None = None,
) -> LearningStability:
    if band_hint is LearningStabilityBand.VOLATILE:
        return LearningStability(
            magnitude=0.2, evidence_count=evidence_count, variance=0.8
        )
    if band_hint is LearningStabilityBand.STABLE:
        return LearningStability(
            magnitude=0.9, evidence_count=evidence_count, variance=0.1
        )
    if band_hint is LearningStabilityBand.MODERATE:
        return LearningStability(
            magnitude=0.6, evidence_count=evidence_count, variance=0.4
        )
    if band_hint is LearningStabilityBand.INSUFFICIENT_DATA:
        return LearningStability.insufficient_data()
    return LearningStability(
        magnitude=magnitude, evidence_count=evidence_count, variance=1.0 - magnitude
    )


def make_competency_assessment(
    *,
    competency_id: str = COMPETENCY_LINEAR_EQUATIONS,
    subject_id: str = SUBJECT_ALGEBRA,
    mastery_magnitude: float = 0.5,
    evidence_count: int = 3,
    confidence_magnitude: float = 0.5,
    contradiction_ratio: float = 0.0,
    stability_band: LearningStabilityBand | None = None,
    gaps: tuple[KnowledgeGap, ...] = (),
    reasons: tuple[AssessmentReason, ...] = (),
) -> CompetencyAssessment:
    return CompetencyAssessment(
        competency_id=MasteryCompetencyId(competency_id),
        subject_id=MasterySubjectId(subject_id),
        mastery=MasteryScore(
            magnitude=mastery_magnitude, evidence_count=evidence_count
        ),
        confidence=make_mastery_confidence(
            magnitude=confidence_magnitude,
            evidence_count=evidence_count,
            contradiction_ratio=contradiction_ratio,
        ),
        stability=make_stability(
            evidence_count=evidence_count, band_hint=stability_band
        ),
        gaps=gaps,
        reasons=reasons,
    )


def make_prerequisite_gap(
    *,
    prerequisite_id: str = COMPETENCY_LINEAR_EQUATIONS,
    dependent_id: str = COMPETENCY_QUADRATIC_EQUATIONS,
    severity: KnowledgeGapSeverity = KnowledgeGapSeverity.SEVERE,
    mastery_magnitude: float = 0.2,
) -> KnowledgeGap:
    return KnowledgeGap(
        competency_id=MasteryCompetencyId(prerequisite_id),
        kind=KnowledgeGapKind.WEAK_PREREQUISITE,
        severity=severity,
        mastery_score=MasteryScore(magnitude=mastery_magnitude, evidence_count=3),
        related_competency_id=MasteryCompetencyId(dependent_id),
        dependency_strength=DependencyStrength.critical(weight=0.9),
    )


def make_direct_gap(
    *,
    competency_id: str = COMPETENCY_LINEAR_EQUATIONS,
    severity: KnowledgeGapSeverity = KnowledgeGapSeverity.MODERATE,
    mastery_magnitude: float = 0.3,
) -> KnowledgeGap:
    return KnowledgeGap(
        competency_id=MasteryCompetencyId(competency_id),
        kind=KnowledgeGapKind.WEAK_EVIDENCE,
        severity=severity,
        mastery_score=MasteryScore(magnitude=mastery_magnitude, evidence_count=3),
    )


def make_subject_assessment(
    *,
    subject_id: str = SUBJECT_ALGEBRA,
    competencies: tuple[CompetencyAssessment, ...] | None = None,
) -> SubjectAssessment:
    if competencies is None:
        competencies = (make_competency_assessment(),)
    mastery = competencies[0].mastery if competencies else MasteryScore.not_assessed()
    confidence = (
        competencies[0].confidence
        if competencies
        else make_mastery_confidence(magnitude=0.0, evidence_count=0)
    )
    stability = (
        competencies[0].stability
        if competencies
        else make_stability(band_hint=LearningStabilityBand.INSUFFICIENT_DATA)
    )
    return SubjectAssessment(
        subject_id=MasterySubjectId(subject_id),
        mastery=mastery,
        confidence=confidence,
        stability=stability,
        competency_assessments=competencies,
    )


def make_mastery_assessment(
    *,
    competencies: tuple[CompetencyAssessment, ...] | None = None,
    assessed_at: datetime | None = None,
) -> MasteryAssessment:
    subject = make_subject_assessment(competencies=competencies)
    gaps = subject.knowledge_gaps()
    reasons = tuple(
        reason
        for competency in subject.competency_assessments
        for reason in competency.reasons
    )
    return MasteryAssessment(
        assessment_id=AssessmentId("assessment-001"),
        student_id=STUDENT_ID,
        assessed_at=assessed_at or datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC),
        overall_mastery=subject.mastery,
        overall_confidence=subject.confidence,
        overall_stability=subject.stability,
        subject_assessments=(subject,),
        knowledge_gaps=gaps,
        supporting_evidence=subject.supporting_evidence(),
        reasons=reasons,
    )


def contradictory_reason(
    competency_id: str = COMPETENCY_LINEAR_EQUATIONS,
) -> AssessmentReason:
    return AssessmentReason(
        reason_code=AssessmentReasonCode.CONTRADICTORY_EVIDENCE,
        subject_id=MasterySubjectId(SUBJECT_ALGEBRA),
        competency_id=MasteryCompetencyId(competency_id),
        detail=0.5,
    )
