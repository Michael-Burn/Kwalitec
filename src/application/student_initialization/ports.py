"""Outbound ports for Student Twin Initialization.

Persistence, identity, time, and first-run Educational OS session context are
injected. This package never imports Flask, SQLAlchemy, or AI SDKs.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

from application.onboarding.results import StudentTwinInitializationRequest
from application.pipeline.pipeline_request import PipelineSessionContext
from domain.education.digital_twin import EducationalDigitalTwin
from domain.education.evidence import EvidenceRecord
from domain.study_planning import LearnerAvailability

if TYPE_CHECKING:
    from application.pipeline.pipeline_request import PipelineRequest
    from application.pipeline.pipeline_result import PipelineResult


class Clock(ABC):
    """Injectable time source for initialization timestamps."""

    @abstractmethod
    def now(self) -> datetime:
        """Return a timezone-aware UTC timestamp."""


class TwinIdGenerator(ABC):
    """Allocate Educational Digital Twin identities."""

    @abstractmethod
    def next_identity(self, *, onboarding_id: str, student_id: str) -> str:
        """Return a new twin id string (deterministic for a given onboarding)."""


class PipelineSessionContextFactory(ABC):
    """Build first-run Educational OS session context for the pipeline.

    Produces twin/diagnosis/priority/strategy/availability already decided for
    the initial run. Must not generate recommendations or missions — those
    remain Educational Pipeline responsibilities.
    """

    @abstractmethod
    def build(
        self,
        *,
        twin: EducationalDigitalTwin,
        declarations: StudentTwinInitializationRequest,
        evidence: tuple[EvidenceRecord, ...],
        availability: LearnerAvailability,
    ) -> PipelineSessionContext:
        """Return session context aligned to the new twin and seeded evidence."""


class EducationalPipelinePort(ABC):
    """Outbound port for executing the Educational Pipeline."""

    @abstractmethod
    def run(self, request: PipelineRequest) -> PipelineResult:
        """Execute the Educational Pipeline and return its result."""
