"""In-memory fakes for application port contracts (tests only)."""

from __future__ import annotations

from datetime import UTC, datetime

from application.events.base import ApplicationEvent
from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.repositories import (
    DecisionRepository,
    DiagnosisRepository,
    DigitalTwinRepository,
    EvidenceRepository,
    HypothesisRepository,
    LearningEpisodeRepository,
    OrchestratorRepository,
    PriorityRepository,
    SubjectKnowledgeRepository,
    TeachingIntentionRepository,
    TeachingPlanRepository,
    TeachingStrategyRepository,
)
from application.ports.transaction_manager import TransactionManager
from application.ports.unit_of_work import UnitOfWork
from application.ports.uuid_generator import UUIDGenerator
from domain.education.decision import EducationalDecision
from domain.education.diagnosis import EducationalDiagnosis
from domain.education.digital_twin import EducationalDigitalTwin
from domain.education.evidence import EvidenceRecord
from domain.education.foundation.ids import (
    ConceptId,
    DecisionId,
    DiagnosisId,
    DigitalTwinId,
    EvidenceId,
    HypothesisId,
    LearningEpisodeId,
    OrchestratorId,
    PriorityId,
    TeachingIntentionId,
    TeachingStrategyId,
)
from domain.education.hypothesis import EducationalHypothesis
from domain.education.learning_episode import LearningEpisode
from domain.education.orchestrator import EducationalOrchestrator
from domain.education.priority import EducationalPriority
from domain.education.subject_knowledge import Concept
from domain.education.teaching_intention import TeachingIntention
from domain.education.teaching_strategy import TeachingStrategy


class InMemoryEventPublisher(ApplicationEventPublisher):
    """Collects published application events for assertions."""

    def __init__(self) -> None:
        self.events: list[ApplicationEvent] = []

    def publish(self, event: ApplicationEvent) -> None:
        self.events.append(event)

    def of_type(self, event_type: type[ApplicationEvent]) -> list[ApplicationEvent]:
        return [event for event in self.events if isinstance(event, event_type)]


class FixedClock(Clock):
    """Deterministic clock for application service tests."""

    def __init__(self, instant: datetime | None = None) -> None:
        self._instant = instant or datetime(2026, 7, 20, 12, 0, tzinfo=UTC)

    def now(self) -> datetime:
        return self._instant


class SequenceUUIDGenerator(UUIDGenerator):
    """Deterministic identity generator for tests."""

    def __init__(self, *, prefix: str = "id") -> None:
        self._prefix = prefix
        self._counter = 0

    def new_id(self) -> str:
        self._counter += 1
        return f"{self._prefix}-{self._counter:04d}"


class InMemoryTransactionManager(TransactionManager):
    """Records transaction lifecycle for assertions."""

    def __init__(self) -> None:
        self.begun = 0
        self.committed = 0
        self.rolled_back = 0
        self._active = False

    def begin(self) -> None:
        self.begun += 1
        self._active = True

    def commit(self) -> None:
        self.committed += 1
        self._active = False

    def rollback(self) -> None:
        self.rolled_back += 1
        self._active = False


class InMemoryDigitalTwinRepository(DigitalTwinRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, EducationalDigitalTwin] = {}
        self._by_student: dict[str, str] = {}

    def get(self, twin_id: DigitalTwinId) -> EducationalDigitalTwin | None:
        return self._by_id.get(twin_id.value)

    def get_by_student(self, student_id: str) -> EducationalDigitalTwin | None:
        twin_key = self._by_student.get(student_id)
        if twin_key is None:
            return None
        return self._by_id.get(twin_key)

    def save(self, twin: EducationalDigitalTwin) -> None:
        self._by_id[twin.twin_id.value] = twin
        self._by_student[twin.student_id] = twin.twin_id.value


class InMemoryLearningEpisodeRepository(LearningEpisodeRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, LearningEpisode] = {}

    def get(self, episode_id: LearningEpisodeId) -> LearningEpisode | None:
        return self._by_id.get(episode_id.value)

    def list_by_student(self, student_id: str) -> list[LearningEpisode]:
        return [ep for ep in self._by_id.values() if ep.student_id == student_id]

    def save(self, episode: LearningEpisode) -> None:
        self._by_id[episode.episode_id.value] = episode


class InMemoryEvidenceRepository(EvidenceRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, EvidenceRecord] = {}

    def get(self, evidence_id: EvidenceId) -> EvidenceRecord | None:
        return self._by_id.get(evidence_id.value)

    def list_by_student(self, student_id: str) -> list[EvidenceRecord]:
        return [rec for rec in self._by_id.values() if rec.student_id == student_id]

    def save(self, evidence: EvidenceRecord) -> None:
        self._by_id[evidence.evidence_id.value] = evidence


class InMemorySubjectKnowledgeRepository(SubjectKnowledgeRepository):
    def __init__(self) -> None:
        self._concepts: dict[str, Concept] = {}
        self._known: set[str] = set()

    def register_existence(self, concept_id: str) -> None:
        """Mark a concept id as known without requiring a full aggregate."""
        self._known.add(concept_id)

    def get_concept(self, concept_id: ConceptId) -> Concept | None:
        return self._concepts.get(concept_id.value)

    def save_concept(self, concept: Concept) -> None:
        self._concepts[concept.concept_id.value] = concept
        self._known.add(concept.concept_id.value)

    def exists(self, concept_id: ConceptId) -> bool:
        return concept_id.value in self._known or concept_id.value in self._concepts


class InMemoryTeachingPlanRepository(TeachingPlanRepository):
    def __init__(self) -> None:
        self._plan_to_episode: dict[str, str] = {}
        self._episode_to_plan: dict[str, str] = {}

    def get_episode_id(self, plan_id: str) -> LearningEpisodeId | None:
        episode_key = self._plan_to_episode.get(plan_id)
        if episode_key is None:
            return None
        return LearningEpisodeId(episode_key)

    def get_plan_id(self, episode_id: LearningEpisodeId) -> str | None:
        return self._episode_to_plan.get(episode_id.value)

    def save(self, plan_id: str, episode_id: LearningEpisodeId) -> None:
        self._plan_to_episode[plan_id] = episode_id.value
        self._episode_to_plan[episode_id.value] = plan_id


class InMemoryDiagnosisRepository(DiagnosisRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, EducationalDiagnosis] = {}

    def get(self, diagnosis_id: DiagnosisId) -> EducationalDiagnosis | None:
        return self._by_id.get(diagnosis_id.value)

    def list_by_student(self, student_id: str) -> list[EducationalDiagnosis]:
        return [d for d in self._by_id.values() if d.student_id == student_id]

    def save(self, diagnosis: EducationalDiagnosis) -> None:
        self._by_id[diagnosis.diagnosis_id.value] = diagnosis


class InMemoryHypothesisRepository(HypothesisRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, EducationalHypothesis] = {}

    def get(self, hypothesis_id: HypothesisId) -> EducationalHypothesis | None:
        return self._by_id.get(hypothesis_id.value)

    def list_by_student(self, student_id: str) -> list[EducationalHypothesis]:
        return [h for h in self._by_id.values() if h.student_id == student_id]

    def save(self, hypothesis: EducationalHypothesis) -> None:
        self._by_id[hypothesis.hypothesis_id.value] = hypothesis


class InMemoryPriorityRepository(PriorityRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, EducationalPriority] = {}

    def get(self, priority_id: PriorityId) -> EducationalPriority | None:
        return self._by_id.get(priority_id.value)

    def list_by_student(self, student_id: str) -> list[EducationalPriority]:
        return [p for p in self._by_id.values() if p.student_id == student_id]

    def save(self, priority: EducationalPriority) -> None:
        self._by_id[priority.priority_id.value] = priority


class InMemoryTeachingIntentionRepository(TeachingIntentionRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, TeachingIntention] = {}

    def get(self, intention_id: TeachingIntentionId) -> TeachingIntention | None:
        return self._by_id.get(intention_id.value)

    def list_by_student(self, student_id: str) -> list[TeachingIntention]:
        return [i for i in self._by_id.values() if i.student_id == student_id]

    def save(self, intention: TeachingIntention) -> None:
        self._by_id[intention.intention_id.value] = intention


class InMemoryTeachingStrategyRepository(TeachingStrategyRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, TeachingStrategy] = {}

    def get(self, strategy_id: TeachingStrategyId) -> TeachingStrategy | None:
        return self._by_id.get(strategy_id.value)

    def list_by_student(self, student_id: str) -> list[TeachingStrategy]:
        return [s for s in self._by_id.values() if s.student_id == student_id]

    def save(self, strategy: TeachingStrategy) -> None:
        self._by_id[strategy.strategy_id.value] = strategy


class InMemoryDecisionRepository(DecisionRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, EducationalDecision] = {}

    def get(self, decision_id: DecisionId) -> EducationalDecision | None:
        return self._by_id.get(decision_id.value)

    def list_by_student(self, student_id: str) -> list[EducationalDecision]:
        return [d for d in self._by_id.values() if d.student_id == student_id]

    def save(self, decision: EducationalDecision) -> None:
        self._by_id[decision.decision_id.value] = decision


class InMemoryOrchestratorRepository(OrchestratorRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, EducationalOrchestrator] = {}

    def get(self, orchestrator_id: OrchestratorId) -> EducationalOrchestrator | None:
        return self._by_id.get(orchestrator_id.value)

    def list_by_student(self, student_id: str) -> list[EducationalOrchestrator]:
        return [o for o in self._by_id.values() if o.student_id == student_id]

    def save(self, orchestrator: EducationalOrchestrator) -> None:
        self._by_id[orchestrator.orchestrator_id.value] = orchestrator


class InMemoryUnitOfWork(UnitOfWork):
    """In-memory UnitOfWork with shared repository instances and lifecycle tracking."""

    def __init__(
        self,
        *,
        digital_twins: InMemoryDigitalTwinRepository | None = None,
        episodes: InMemoryLearningEpisodeRepository | None = None,
        evidence: InMemoryEvidenceRepository | None = None,
        subject_knowledge: InMemorySubjectKnowledgeRepository | None = None,
        diagnosis: InMemoryDiagnosisRepository | None = None,
        hypothesis: InMemoryHypothesisRepository | None = None,
        priority: InMemoryPriorityRepository | None = None,
        teaching_intention: InMemoryTeachingIntentionRepository | None = None,
        teaching_strategy: InMemoryTeachingStrategyRepository | None = None,
        decision: InMemoryDecisionRepository | None = None,
        orchestrator: InMemoryOrchestratorRepository | None = None,
        teaching_plan: InMemoryTeachingPlanRepository | None = None,
    ) -> None:
        self._digital_twins = digital_twins or InMemoryDigitalTwinRepository()
        self._episodes = episodes or InMemoryLearningEpisodeRepository()
        self._evidence = evidence or InMemoryEvidenceRepository()
        self._subject_knowledge = (
            subject_knowledge or InMemorySubjectKnowledgeRepository()
        )
        self._diagnosis = diagnosis or InMemoryDiagnosisRepository()
        self._hypothesis = hypothesis or InMemoryHypothesisRepository()
        self._priority = priority or InMemoryPriorityRepository()
        self._teaching_intention = (
            teaching_intention or InMemoryTeachingIntentionRepository()
        )
        self._teaching_strategy = (
            teaching_strategy or InMemoryTeachingStrategyRepository()
        )
        self._decision = decision or InMemoryDecisionRepository()
        self._orchestrator = orchestrator or InMemoryOrchestratorRepository()
        self._teaching_plan = teaching_plan or InMemoryTeachingPlanRepository()
        self._active = False
        self.begin_count = 0
        self.commit_count = 0
        self.rollback_count = 0

    @property
    def digital_twins(self) -> DigitalTwinRepository:
        return self._digital_twins

    @property
    def episodes(self) -> LearningEpisodeRepository:
        return self._episodes

    @property
    def evidence(self) -> EvidenceRepository:
        return self._evidence

    @property
    def subject_knowledge(self) -> SubjectKnowledgeRepository:
        return self._subject_knowledge

    @property
    def diagnosis(self) -> DiagnosisRepository:
        return self._diagnosis

    @property
    def hypothesis(self) -> HypothesisRepository:
        return self._hypothesis

    @property
    def priority(self) -> PriorityRepository:
        return self._priority

    @property
    def teaching_intention(self) -> TeachingIntentionRepository:
        return self._teaching_intention

    @property
    def teaching_strategy(self) -> TeachingStrategyRepository:
        return self._teaching_strategy

    @property
    def decision(self) -> DecisionRepository:
        return self._decision

    @property
    def orchestrator(self) -> OrchestratorRepository:
        return self._orchestrator

    @property
    def teaching_plan(self) -> TeachingPlanRepository:
        return self._teaching_plan

    @property
    def is_active(self) -> bool:
        return self._active

    def begin(self) -> None:
        if self._active:
            raise RuntimeError("unit of work already active")
        self._active = True
        self.begin_count += 1

    def commit(self) -> None:
        if not self._active:
            raise RuntimeError("unit of work is not active")
        self._active = False
        self.commit_count += 1

    def rollback(self) -> None:
        if not self._active:
            return
        self._active = False
        self.rollback_count += 1
