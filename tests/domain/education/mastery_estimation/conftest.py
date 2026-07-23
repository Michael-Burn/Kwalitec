"""Shared factories for Mastery Estimation domain tests."""

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
from domain.education.mastery_estimation import AssessmentId, CompetencyId, SubjectId
from domain.education.student_state.aggregates.student_educational_state import (
    StudentEducationalState,
)
from domain.education.student_state.enums import MasteryBand as StateMasteryBand
from domain.education.student_state.enums import SubjectStatus
from domain.education.student_state.ids import (
    CompetencyId as StateCompetencyId,
)
from domain.education.student_state.ids import (
    StudentEducationalStateId,
)
from domain.education.student_state.ids import (
    SubjectId as StateSubjectId,
)
from domain.education.student_state.value_objects.competency_state import (
    CompetencyState,
)
from domain.education.student_state.value_objects.subject_state import SubjectState

STUDENT_ID = "student-001"
SUBJECT_ALGEBRA = "algebra"
COMPETENCY_LINEAR_EQUATIONS = "linear-equations"
COMPETENCY_QUADRATIC_EQUATIONS = "quadratic-equations"


@pytest.fixture
def as_of() -> datetime:
    return datetime(2026, 7, 21, 12, 0, 0, tzinfo=UTC)


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


def make_confidence_evidence(
    *,
    evidence_id: str,
    competency_id: str = COMPETENCY_LINEAR_EQUATIONS,
    confidence_level: str,
    occurred_at: datetime,
) -> EducationalEvidence:
    return EducationalEvidence.record_confidence(
        EvidenceId(evidence_id),
        STUDENT_ID,
        occurred_at,
        make_evidence_source(),
        learning_environment=make_learning_environment(),
        confidence_level=confidence_level,
        subject_id=SUBJECT_ALGEBRA,
        competency_id=competency_id,
    )


def make_student_state(
    *,
    subject_id: str = SUBJECT_ALGEBRA,
    competency_ids: tuple[str, ...] = (COMPETENCY_LINEAR_EQUATIONS,),
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


@pytest.fixture
def assessment_id() -> AssessmentId:
    return AssessmentId("assessment-001")


@pytest.fixture
def subject_id() -> SubjectId:
    return SubjectId(SUBJECT_ALGEBRA)


@pytest.fixture
def competency_id() -> CompetencyId:
    return CompetencyId(COMPETENCY_LINEAR_EQUATIONS)
