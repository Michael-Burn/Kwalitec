"""CurriculumPort — structural curriculum reads for the composition layer."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.application.education_platform.dto.education_request import EducationRequest
from app.application.education_platform.dto.subject_plan import SubjectPlan


@runtime_checkable
class CurriculumPort(Protocol):
    """Structural contract for Curriculum Graph / Navigation reads.

    The composition layer may resolve subject outlines and topic ordering.
    It must never invent curriculum content or select pedagogical strategies.
    """

    @property
    def component_id(self) -> str:
        """Stable component identity (e.g. ``curriculum``)."""

    @property
    def component_version(self) -> str:
        """Version string for health / diagnostics."""

    def resolve_subject(self, request: EducationRequest) -> SubjectPlan:
        """Return a deterministic subject outline for the request context."""

    def topic_available(self, topic_id: str) -> bool:
        """True when ``topic_id`` is present in the curriculum order."""

    def ordered_topic_ids(self, subject_id: str | None = None) -> tuple[str, ...]:
        """Canonical topic id order, optionally scoped to a subject."""

    def is_available(self) -> bool:
        """True when the curriculum port can accept work."""
