"""Repository port interfaces for the application layer.

Implementations live in infrastructure. This module defines contracts only.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

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


class DigitalTwinRepository(ABC):
    """Persistence boundary for EducationalDigitalTwin aggregates."""

    @abstractmethod
    def get(self, twin_id: DigitalTwinId) -> EducationalDigitalTwin | None:
        """Load a Twin by identity, or ``None`` if absent."""

    @abstractmethod
    def get_by_student(self, student_id: str) -> EducationalDigitalTwin | None:
        """Load the Twin for a student, or ``None`` if absent."""

    @abstractmethod
    def save(self, twin: EducationalDigitalTwin) -> None:
        """Persist (insert or replace) a Twin aggregate."""


class LearningEpisodeRepository(ABC):
    """Persistence boundary for LearningEpisode aggregates."""

    @abstractmethod
    def get(self, episode_id: LearningEpisodeId) -> LearningEpisode | None:
        """Load an episode by identity, or ``None`` if absent."""

    @abstractmethod
    def list_by_student(self, student_id: str) -> list[LearningEpisode]:
        """Return episodes owned by the student (order unspecified)."""

    @abstractmethod
    def save(self, episode: LearningEpisode) -> None:
        """Persist (insert or replace) an episode aggregate."""


class EvidenceRepository(ABC):
    """Persistence boundary for EvidenceRecord aggregates."""

    @abstractmethod
    def get(self, evidence_id: EvidenceId) -> EvidenceRecord | None:
        """Load evidence by identity, or ``None`` if absent."""

    @abstractmethod
    def list_by_student(self, student_id: str) -> list[EvidenceRecord]:
        """Return evidence records for the student (order unspecified)."""

    @abstractmethod
    def save(self, evidence: EvidenceRecord) -> None:
        """Persist (insert or replace) an evidence aggregate."""


class SubjectKnowledgeRepository(ABC):
    """Persistence boundary for subject-knowledge Concept aggregates."""

    @abstractmethod
    def get_concept(self, concept_id: ConceptId) -> Concept | None:
        """Load a Concept by identity, or ``None`` if absent."""

    @abstractmethod
    def save_concept(self, concept: Concept) -> None:
        """Persist (insert or replace) a Concept aggregate."""

    @abstractmethod
    def exists(self, concept_id: ConceptId) -> bool:
        """Return whether the concept is known to the repository."""


class TeachingPlanRepository(ABC):
    """Persistence boundary for teaching-plan coordination (plan ↔ episode).

    Teaching plans are application coordination state linking a plan identity
    to a planned Learning Episode. There is no separate teaching-plan aggregate
    in the domain.
    """

    @abstractmethod
    def get_episode_id(self, plan_id: str) -> LearningEpisodeId | None:
        """Resolve the episode bound to a plan, or ``None`` if absent."""

    @abstractmethod
    def get_plan_id(self, episode_id: LearningEpisodeId) -> str | None:
        """Resolve the plan identity for an episode, or ``None`` if absent."""

    @abstractmethod
    def save(self, plan_id: str, episode_id: LearningEpisodeId) -> None:
        """Persist (insert or replace) a plan ↔ episode binding."""


class DiagnosisRepository(ABC):
    """Persistence boundary for EducationalDiagnosis aggregates."""

    @abstractmethod
    def get(self, diagnosis_id: DiagnosisId) -> EducationalDiagnosis | None:
        """Load a diagnosis by identity, or ``None`` if absent."""

    @abstractmethod
    def list_by_student(self, student_id: str) -> list[EducationalDiagnosis]:
        """Return diagnoses for the student (order unspecified)."""

    @abstractmethod
    def save(self, diagnosis: EducationalDiagnosis) -> None:
        """Persist (insert or replace) a diagnosis aggregate."""


class HypothesisRepository(ABC):
    """Persistence boundary for EducationalHypothesis aggregates."""

    @abstractmethod
    def get(self, hypothesis_id: HypothesisId) -> EducationalHypothesis | None:
        """Load a hypothesis by identity, or ``None`` if absent."""

    @abstractmethod
    def list_by_student(self, student_id: str) -> list[EducationalHypothesis]:
        """Return hypotheses for the student (order unspecified)."""

    @abstractmethod
    def save(self, hypothesis: EducationalHypothesis) -> None:
        """Persist (insert or replace) a hypothesis aggregate."""


class PriorityRepository(ABC):
    """Persistence boundary for EducationalPriority aggregates."""

    @abstractmethod
    def get(self, priority_id: PriorityId) -> EducationalPriority | None:
        """Load a priority by identity, or ``None`` if absent."""

    @abstractmethod
    def list_by_student(self, student_id: str) -> list[EducationalPriority]:
        """Return priorities for the student (order unspecified)."""

    @abstractmethod
    def save(self, priority: EducationalPriority) -> None:
        """Persist (insert or replace) a priority aggregate."""


class TeachingIntentionRepository(ABC):
    """Persistence boundary for TeachingIntention aggregates."""

    @abstractmethod
    def get(self, intention_id: TeachingIntentionId) -> TeachingIntention | None:
        """Load a teaching intention by identity, or ``None`` if absent."""

    @abstractmethod
    def list_by_student(self, student_id: str) -> list[TeachingIntention]:
        """Return teaching intentions for the student (order unspecified)."""

    @abstractmethod
    def save(self, intention: TeachingIntention) -> None:
        """Persist (insert or replace) a teaching intention aggregate."""


class TeachingStrategyRepository(ABC):
    """Persistence boundary for TeachingStrategy aggregates."""

    @abstractmethod
    def get(self, strategy_id: TeachingStrategyId) -> TeachingStrategy | None:
        """Load a teaching strategy by identity, or ``None`` if absent."""

    @abstractmethod
    def list_by_student(self, student_id: str) -> list[TeachingStrategy]:
        """Return teaching strategies for the student (order unspecified)."""

    @abstractmethod
    def save(self, strategy: TeachingStrategy) -> None:
        """Persist (insert or replace) a teaching strategy aggregate."""


class DecisionRepository(ABC):
    """Persistence boundary for EducationalDecision aggregates."""

    @abstractmethod
    def get(self, decision_id: DecisionId) -> EducationalDecision | None:
        """Load a decision by identity, or ``None`` if absent."""

    @abstractmethod
    def list_by_student(self, student_id: str) -> list[EducationalDecision]:
        """Return decisions for the student (order unspecified)."""

    @abstractmethod
    def save(self, decision: EducationalDecision) -> None:
        """Persist (insert or replace) a decision aggregate."""


class OrchestratorRepository(ABC):
    """Persistence boundary for EducationalOrchestrator aggregates."""

    @abstractmethod
    def get(self, orchestrator_id: OrchestratorId) -> EducationalOrchestrator | None:
        """Load an orchestrator by identity, or ``None`` if absent."""

    @abstractmethod
    def list_by_student(self, student_id: str) -> list[EducationalOrchestrator]:
        """Return orchestrator turns for the student (order unspecified)."""

    @abstractmethod
    def save(self, orchestrator: EducationalOrchestrator) -> None:
        """Persist (insert or replace) an orchestrator aggregate."""
