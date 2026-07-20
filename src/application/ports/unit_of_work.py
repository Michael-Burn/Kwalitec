"""Unit of Work port — transactional boundary with repository accessors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

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


class UnitOfWork(ABC):
    """Coordinates a single transactional unit across educational repositories.

    Typical usage::

        with uow:
            twin = uow.digital_twins.get(...)
            ...
            uow.commit()

    ``__enter__`` begins the unit. Explicit ``commit()`` persists work.
    ``__exit__`` rolls back on exception or when the unit is still active
    (uncommitted). Nested units are not part of this contract.
    """

    @property
    @abstractmethod
    def digital_twins(self) -> DigitalTwinRepository:
        """Digital Twin persistence boundary."""

    @property
    @abstractmethod
    def episodes(self) -> LearningEpisodeRepository:
        """Learning Episode persistence boundary."""

    @property
    @abstractmethod
    def evidence(self) -> EvidenceRepository:
        """Evidence Record persistence boundary."""

    @property
    @abstractmethod
    def subject_knowledge(self) -> SubjectKnowledgeRepository:
        """Subject-knowledge Concept persistence boundary."""

    @property
    @abstractmethod
    def diagnosis(self) -> DiagnosisRepository:
        """Educational Diagnosis persistence boundary."""

    @property
    @abstractmethod
    def hypothesis(self) -> HypothesisRepository:
        """Educational Hypothesis persistence boundary."""

    @property
    @abstractmethod
    def priority(self) -> PriorityRepository:
        """Educational Priority persistence boundary."""

    @property
    @abstractmethod
    def teaching_intention(self) -> TeachingIntentionRepository:
        """Teaching Intention persistence boundary."""

    @property
    @abstractmethod
    def teaching_strategy(self) -> TeachingStrategyRepository:
        """Teaching Strategy persistence boundary."""

    @property
    @abstractmethod
    def decision(self) -> DecisionRepository:
        """Educational Decision persistence boundary."""

    @property
    @abstractmethod
    def orchestrator(self) -> OrchestratorRepository:
        """Educational Orchestrator persistence boundary."""

    @property
    @abstractmethod
    def teaching_plan(self) -> TeachingPlanRepository:
        """Teaching-plan coordination persistence boundary."""

    @property
    @abstractmethod
    def is_active(self) -> bool:
        """True while a transactional unit is open."""

    @abstractmethod
    def begin(self) -> None:
        """Open a transactional unit."""

    @abstractmethod
    def commit(self) -> None:
        """Persist all work performed in this unit and close it."""

    @abstractmethod
    def rollback(self) -> None:
        """Discard work performed in this unit and close it."""

    def __enter__(self) -> Self:
        self.begin()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        if self.is_active:
            self.rollback()
        return False
