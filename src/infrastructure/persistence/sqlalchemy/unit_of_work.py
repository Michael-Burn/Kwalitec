"""SQLAlchemy UnitOfWork adapter for Education OS application services."""

from __future__ import annotations

from collections.abc import Callable
from types import TracebackType
from typing import Any, Self, TypeVar

from sqlalchemy.orm import Session

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
from application.ports.unit_of_work import UnitOfWork
from infrastructure.events.collector import EventSource
from infrastructure.events.dispatcher import EventDispatcher
from infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyDecisionRepository,
    SqlAlchemyDiagnosisRepository,
    SqlAlchemyDigitalTwinRepository,
    SqlAlchemyEvidenceRepository,
    SqlAlchemyHypothesisRepository,
    SqlAlchemyLearningEpisodeRepository,
    SqlAlchemyOrchestratorRepository,
    SqlAlchemyPriorityRepository,
    SqlAlchemySubjectKnowledgeRepository,
    SqlAlchemyTeachingIntentionRepository,
    SqlAlchemyTeachingPlanRepository,
    SqlAlchemyTeachingStrategyRepository,
)

SessionFactory = Callable[[], Session]
RepositoryT = TypeVar("RepositoryT")


class SqlAlchemyUnitOfWork(UnitOfWork):
    """Coordinate repositories and one SQLAlchemy session per unit of work.

    When an ``EventDispatcher`` is provided, domain events are collected
    automatically: aggregates are tracked when repositories persist them,
    events are staged before commit, published after a successful commit,
    and discarded on rollback.
    """

    def __init__(
        self,
        session_factory: SessionFactory,
        event_dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._dispatcher = event_dispatcher
        self._session: Session | None = None
        self._is_active = False
        self._digital_twins: DigitalTwinRepository | None = None
        self._episodes: LearningEpisodeRepository | None = None
        self._evidence: EvidenceRepository | None = None
        self._subject_knowledge: SubjectKnowledgeRepository | None = None
        self._diagnosis: DiagnosisRepository | None = None
        self._hypothesis: HypothesisRepository | None = None
        self._priority: PriorityRepository | None = None
        self._teaching_intention: TeachingIntentionRepository | None = None
        self._teaching_strategy: TeachingStrategyRepository | None = None
        self._decision: DecisionRepository | None = None
        self._orchestrator: OrchestratorRepository | None = None
        self._teaching_plan: TeachingPlanRepository | None = None

    @property
    def digital_twins(self) -> DigitalTwinRepository:
        return self._require_repository(self._digital_twins)

    @property
    def episodes(self) -> LearningEpisodeRepository:
        return self._require_repository(self._episodes)

    @property
    def evidence(self) -> EvidenceRepository:
        return self._require_repository(self._evidence)

    @property
    def subject_knowledge(self) -> SubjectKnowledgeRepository:
        return self._require_repository(self._subject_knowledge)

    @property
    def diagnosis(self) -> DiagnosisRepository:
        return self._require_repository(self._diagnosis)

    @property
    def hypothesis(self) -> HypothesisRepository:
        return self._require_repository(self._hypothesis)

    @property
    def priority(self) -> PriorityRepository:
        return self._require_repository(self._priority)

    @property
    def teaching_intention(self) -> TeachingIntentionRepository:
        return self._require_repository(self._teaching_intention)

    @property
    def teaching_strategy(self) -> TeachingStrategyRepository:
        return self._require_repository(self._teaching_strategy)

    @property
    def decision(self) -> DecisionRepository:
        return self._require_repository(self._decision)

    @property
    def orchestrator(self) -> OrchestratorRepository:
        return self._require_repository(self._orchestrator)

    @property
    def teaching_plan(self) -> TeachingPlanRepository:
        return self._require_repository(self._teaching_plan)

    @property
    def is_active(self) -> bool:
        return self._is_active

    def begin(self) -> None:
        """Open a session and wire all repositories to its transaction."""
        if self._is_active:
            raise RuntimeError("unit of work is already active")

        session = self._session_factory()
        try:
            session.begin()
            self._wire_repositories(session)
        except Exception:
            session.close()
            raise

        self._session = session
        self._is_active = True

    def __enter__(self) -> Self:
        self.begin()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        try:
            if self._is_active:
                self.rollback()
        finally:
            self._close_session()
        return False

    def commit(self) -> None:
        """Commit the active transaction, dispatching domain events on success."""
        session = self._require_active_session()

        if self._dispatcher is not None:
            self._dispatcher.stage()

        try:
            session.commit()
        except Exception:
            try:
                session.rollback()
            finally:
                self._is_active = False
                if self._dispatcher is not None:
                    self._dispatcher.discard()
            raise

        self._is_active = False

        if self._dispatcher is not None:
            self._dispatcher.dispatch_after_commit()

    def rollback(self) -> None:
        """Roll back the active transaction and discard pending domain events."""
        if not self._is_active:
            return
        session = self._require_active_session()
        try:
            session.rollback()
        finally:
            self._is_active = False
            if self._dispatcher is not None:
                self._dispatcher.discard()

    def _track_aggregate(self, aggregate: Any) -> None:
        """Register an aggregate as an event source when a dispatcher is wired."""
        if self._dispatcher is not None and isinstance(aggregate, EventSource):
            self._dispatcher.track(aggregate)

    def _wire_repositories(self, session: Session) -> None:
        tracker = self._track_aggregate
        self._digital_twins = SqlAlchemyDigitalTwinRepository(session, tracker)
        self._episodes = SqlAlchemyLearningEpisodeRepository(session, tracker)
        self._evidence = SqlAlchemyEvidenceRepository(session, tracker)
        self._subject_knowledge = SqlAlchemySubjectKnowledgeRepository(session, tracker)
        self._diagnosis = SqlAlchemyDiagnosisRepository(session, tracker)
        self._hypothesis = SqlAlchemyHypothesisRepository(session, tracker)
        self._priority = SqlAlchemyPriorityRepository(session, tracker)
        self._teaching_intention = SqlAlchemyTeachingIntentionRepository(
            session, tracker
        )
        self._teaching_strategy = SqlAlchemyTeachingStrategyRepository(session, tracker)
        self._decision = SqlAlchemyDecisionRepository(session, tracker)
        self._orchestrator = SqlAlchemyOrchestratorRepository(session, tracker)
        self._teaching_plan = SqlAlchemyTeachingPlanRepository(session)

    def _require_active_session(self) -> Session:
        if not self._is_active or self._session is None:
            raise RuntimeError("unit of work is not active")
        return self._session

    @staticmethod
    def _require_repository(
        repository: RepositoryT | None,
    ) -> RepositoryT:
        if repository is None:
            raise RuntimeError("unit of work is not active")
        return repository

    def _close_session(self) -> None:
        if self._session is not None:
            self._session.close()
        self._session = None
        self._clear_repositories()

    def _clear_repositories(self) -> None:
        self._digital_twins = None
        self._episodes = None
        self._evidence = None
        self._subject_knowledge = None
        self._diagnosis = None
        self._hypothesis = None
        self._priority = None
        self._teaching_intention = None
        self._teaching_strategy = None
        self._decision = None
        self._orchestrator = None
        self._teaching_plan = None
