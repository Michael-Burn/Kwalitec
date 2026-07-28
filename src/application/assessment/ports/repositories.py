"""Repository and builder ports for the Assessment application layer.

Implementations are deferred — AP-002A defines contracts only.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from domain.assessment.entities.assessment_instrument import AssessmentInstrument
from domain.assessment.entities.assessment_observation import AssessmentObservation
from domain.assessment.entities.assessment_result import AssessmentResult
from domain.assessment.entities.assessment_session import AssessmentSession
from domain.assessment.enums import AssessmentPurpose, AssessmentType
from domain.assessment.value_objects.configuration import (
    AssessmentConfiguration,
    AssessmentMetadata,
)
from domain.assessment.value_objects.ids import (
    InstrumentId,
    ObservationId,
    ResultId,
    SessionId,
)
from domain.assessment.value_objects.references import (
    LearningObjectiveReference,
    QuestionReference,
)


class AssessmentRepository(ABC):
    """Persistence boundary for assessment coordination identities (future)."""

    @abstractmethod
    def get_session(self, session_id: SessionId) -> AssessmentSession | None:
        """Load a session by identity, or ``None`` if absent."""

    @abstractmethod
    def save_session(self, session: AssessmentSession) -> None:
        """Persist (insert or replace) a session aggregate."""


class AssessmentSessionRepository(ABC):
    """Persistence boundary for AssessmentSession aggregates."""

    @abstractmethod
    def get(self, session_id: SessionId) -> AssessmentSession | None:
        """Load a session by identity, or ``None`` if absent."""

    @abstractmethod
    def list_by_student(self, student_id: str) -> list[AssessmentSession]:
        """Return sessions for the student (order unspecified)."""

    @abstractmethod
    def save(self, session: AssessmentSession) -> None:
        """Persist (insert or replace) a session aggregate."""


class AssessmentInstrumentRepository(ABC):
    """Persistence boundary for AssessmentInstrument catalogue entries."""

    @abstractmethod
    def get(self, instrument_id: InstrumentId) -> AssessmentInstrument | None:
        """Load an instrument by identity, or ``None`` if absent."""

    @abstractmethod
    def list_by_purpose(
        self, purpose: AssessmentPurpose
    ) -> list[AssessmentInstrument]:
        """Return instruments matching educational purpose."""

    @abstractmethod
    def save(self, instrument: AssessmentInstrument) -> None:
        """Persist (insert or replace) an instrument."""


class AssessmentObservationRepository(ABC):
    """Persistence boundary for AssessmentObservation facts."""

    @abstractmethod
    def get(self, observation_id: ObservationId) -> AssessmentObservation | None:
        """Load an observation by identity, or ``None`` if absent."""

    @abstractmethod
    def list_by_session(self, session_id: SessionId) -> list[AssessmentObservation]:
        """Return observations for a session."""

    @abstractmethod
    def save(self, observation: AssessmentObservation) -> None:
        """Persist an observation (append-only semantics expected later)."""


class AssessmentResultRepository(ABC):
    """Persistence boundary for AssessmentResult packaging."""

    @abstractmethod
    def get(self, result_id: ResultId) -> AssessmentResult | None:
        """Load a result by identity, or ``None`` if absent."""

    @abstractmethod
    def get_by_session(self, session_id: SessionId) -> AssessmentResult | None:
        """Load the result for a session, or ``None`` if absent."""

    @abstractmethod
    def save(self, result: AssessmentResult) -> None:
        """Persist (insert or replace) a result."""


class AssessmentInstrumentBuilder(ABC):
    """Builder port for constructing instruments from authoring inputs."""

    @abstractmethod
    def build(
        self,
        instrument_id: InstrumentId,
        assessment_type: AssessmentType,
        purpose: AssessmentPurpose,
        questions: Sequence[QuestionReference],
        learning_objectives: Sequence[LearningObjectiveReference],
        metadata: AssessmentMetadata,
        *,
        configuration: AssessmentConfiguration | None = None,
    ) -> AssessmentInstrument:
        """Build a validated instrument."""


class AssessmentSessionBuilder(ABC):
    """Builder port for constructing sessions from instruments."""

    @abstractmethod
    def build_from_instrument(
        self,
        session_id: SessionId,
        student_id: str,
        instrument: AssessmentInstrument,
        *,
        twin_id: str | None = None,
        mission_id: str | None = None,
    ) -> AssessmentSession:
        """Build a session from a catalogue instrument."""


class QuestionContentRepository(ABC):
    """Persistence boundary for renderable question content (stems / options)."""

    @abstractmethod
    def get(self, question_id: str) -> Any | None:
        """Load question content by id, or ``None`` if absent."""

    @abstractmethod
    def save(self, content: Any) -> None:
        """Persist (insert or replace) question content."""


class SessionDeliveryStateRepository(ABC):
    """Persistence boundary for delivery cursor / resume state."""

    @abstractmethod
    def get(self, session_id: str) -> Any | None:
        """Load delivery state, or ``None`` if absent."""

    @abstractmethod
    def save(self, state: Any) -> None:
        """Persist delivery state."""


class EvidenceBundleRepository(ABC):
    """Persistence / export boundary for packaged EvidenceBundle artefacts."""

    @abstractmethod
    def get(self, bundle_id: Any) -> Any | None:
        """Load a packaged evidence bundle by identity, or ``None`` if absent."""

    @abstractmethod
    def get_by_session(self, session_id: SessionId) -> Any | None:
        """Load the packaged evidence bundle for a session, or ``None``."""

    @abstractmethod
    def save(self, bundle: Any) -> None:
        """Persist (insert or replace) a packaged evidence bundle."""
