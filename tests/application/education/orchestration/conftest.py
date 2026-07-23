"""Shared fakes and factories for Educational Orchestration tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from application.education.orchestration.educational_orchestrator import (
    EducationalOrchestrator,
)
from application.education.orchestration.ports.assessment_publisher import (
    AssessmentPublisher,
)
from application.education.orchestration.ports.evidence_provider import (
    EvidenceProvider,
)
from application.education.orchestration.ports.knowledge_graph_provider import (
    KnowledgeGraphProvider,
)
from application.education.orchestration.ports.recommendation_publisher import (
    RecommendationPublisher,
)
from application.education.orchestration.ports.student_state_provider import (
    StudentStateProvider,
)
from application.errors import NotFoundError
from application.ports.uuid_generator import UUIDGenerator
from domain.education.educational_evidence.aggregates.educational_evidence import (
    EducationalEvidence,
)
from domain.education.knowledge_graph import (
    KnowledgeGraph,
    KnowledgeGraphId,
    KnowledgeNode,
    KnowledgeNodeId,
    KnowledgeNodeKind,
)
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.recommendation_engine.aggregates.recommendation_set import (
    RecommendationSet,
)
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

AS_OF = datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC)
STUDENT_ID = "student-orch-001"
SUBJECT_ALGEBRA = "algebra"
COMP_LINEAR = "linear-equations"
COMP_QUADRATIC = "quadratic-equations"


class SequenceUUIDGenerator(UUIDGenerator):
    """Deterministic identity sequence for orchestration tests."""

    def __init__(self, prefix: str = "id") -> None:
        self._prefix = prefix
        self._counter = 0

    def new_id(self) -> str:
        self._counter += 1
        return f"{self._prefix}-{self._counter:04d}"


class FakeStudentStateProvider(StudentStateProvider):
    def __init__(
        self,
        states: dict[str, StudentEducationalState] | None = None,
        *,
        error: Exception | None = None,
    ) -> None:
        self._states = dict(states or {})
        self._error = error
        self.calls: list[str] = []

    def get_student_state(self, student_id: str) -> StudentEducationalState:
        self.calls.append(student_id)
        if self._error is not None:
            raise self._error
        if student_id not in self._states:
            raise NotFoundError("StudentEducationalState", student_id)
        return self._states[student_id]


class FakeEvidenceProvider(EvidenceProvider):
    def __init__(
        self,
        evidence: dict[str, list[EducationalEvidence]] | None = None,
        *,
        list_error: Exception | None = None,
        record_error: Exception | None = None,
    ) -> None:
        self._evidence: dict[str, list[EducationalEvidence]] = {
            key: list(value) for key, value in (evidence or {}).items()
        }
        self._list_error = list_error
        self._record_error = record_error
        self.recorded: list[EducationalEvidence] = []
        self.list_calls: list[str] = []

    def list_evidence(self, student_id: str) -> tuple[EducationalEvidence, ...]:
        self.list_calls.append(student_id)
        if self._list_error is not None:
            raise self._list_error
        return tuple(self._evidence.get(student_id, ()))

    def record_evidence(self, evidence: EducationalEvidence) -> None:
        if self._record_error is not None:
            raise self._record_error
        self.recorded.append(evidence)
        bucket = self._evidence.setdefault(evidence.student_id, [])
        bucket.append(evidence)


class FakeKnowledgeGraphProvider(KnowledgeGraphProvider):
    def __init__(
        self,
        graphs: dict[str, KnowledgeGraph] | None = None,
        *,
        error: Exception | None = None,
    ) -> None:
        self._graphs = dict(graphs or {})
        self._error = error
        self.calls: list[str] = []

    def get_knowledge_graph(self, student_id: str) -> KnowledgeGraph:
        self.calls.append(student_id)
        if self._error is not None:
            raise self._error
        if student_id not in self._graphs:
            raise NotFoundError("KnowledgeGraph", student_id)
        return self._graphs[student_id]


class FakeAssessmentPublisher(AssessmentPublisher):
    def __init__(self, *, error: Exception | None = None) -> None:
        self.published: list[MasteryAssessment] = []
        self._error = error

    def publish_assessment(self, assessment: MasteryAssessment) -> None:
        if self._error is not None:
            raise self._error
        self.published.append(assessment)


class FakeRecommendationPublisher(RecommendationPublisher):
    def __init__(self, *, error: Exception | None = None) -> None:
        self.published: list[RecommendationSet] = []
        self._error = error

    def publish_recommendations(
        self, recommendation_set: RecommendationSet
    ) -> None:
        if self._error is not None:
            raise self._error
        self.published.append(recommendation_set)


def make_student_state(
    *,
    student_id: str = STUDENT_ID,
    subject_id: str = SUBJECT_ALGEBRA,
    competency_ids: tuple[str, ...] = (COMP_LINEAR,),
) -> StudentEducationalState:
    state = StudentEducationalState.create(
        StudentEducationalStateId("state-orch-001"), student_id
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
    graph_id: str = "graph-orch-001",
    nodes: tuple[str, ...] = (COMP_LINEAR, COMP_QUADRATIC),
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
    return graph


def make_orchestrator(
    *,
    state: StudentEducationalState | None = None,
    graph: KnowledgeGraph | None = None,
    evidence: list[EducationalEvidence] | None = None,
    student_state_provider: StudentStateProvider | None = None,
    evidence_provider: EvidenceProvider | None = None,
    knowledge_graph_provider: KnowledgeGraphProvider | None = None,
    assessment_publisher: AssessmentPublisher | None = None,
    recommendation_publisher: RecommendationPublisher | None = None,
    uuid_generator: UUIDGenerator | None = None,
) -> tuple[
    EducationalOrchestrator,
    FakeStudentStateProvider,
    FakeEvidenceProvider,
    FakeKnowledgeGraphProvider,
    FakeAssessmentPublisher,
    FakeRecommendationPublisher,
    SequenceUUIDGenerator,
]:
    resolved_state = state or make_student_state()
    resolved_graph = graph or make_knowledge_graph()
    state_provider = student_state_provider or FakeStudentStateProvider(
        {STUDENT_ID: resolved_state}
    )
    evidence_port = evidence_provider or FakeEvidenceProvider(
        {STUDENT_ID: list(evidence or [])}
    )
    graph_provider = knowledge_graph_provider or FakeKnowledgeGraphProvider(
        {STUDENT_ID: resolved_graph}
    )
    assessment_pub = assessment_publisher or FakeAssessmentPublisher()
    recommendation_pub = (
        recommendation_publisher or FakeRecommendationPublisher()
    )
    uuids = uuid_generator or SequenceUUIDGenerator()
    orchestrator = EducationalOrchestrator(
        student_state_provider=state_provider,
        evidence_provider=evidence_port,
        knowledge_graph_provider=graph_provider,
        uuid_generator=uuids,
        assessment_publisher=assessment_pub,
        recommendation_publisher=recommendation_pub,
    )
    return (
        orchestrator,
        state_provider,  # type: ignore[return-value]
        evidence_port,  # type: ignore[return-value]
        graph_provider,  # type: ignore[return-value]
        assessment_pub,  # type: ignore[return-value]
        recommendation_pub,  # type: ignore[return-value]
        uuids,  # type: ignore[return-value]
    )


@pytest.fixture
def as_of() -> datetime:
    return AS_OF


@pytest.fixture
def orchestrator_bundle():
    return make_orchestrator()
