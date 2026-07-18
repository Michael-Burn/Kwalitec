"""Experience session — presentation handle for starting today's learning.

References mission / session identities provided by upstream ports.
Never generates missions or owns educational progression.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ExperienceSessionStatus(StrEnum):
    """Presentation status of a student experience session handle."""

    READY = "ready"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class StartSessionAction:
    """Student-facing call-to-action to begin today's session."""

    label: str = "Start Session"
    enabled: bool = True
    mission_id: str | None = None
    session_id: str | None = None
    estimated_minutes: int | None = None
    topic_title: str = ""

    @classmethod
    def create(
        cls,
        *,
        label: str = "Start Session",
        enabled: bool = True,
        mission_id: str | None = None,
        session_id: str | None = None,
        estimated_minutes: int | None = None,
        topic_title: str = "",
    ) -> StartSessionAction:
        """Build a Start Session action from port identities."""
        minutes = estimated_minutes
        if minutes is not None and minutes < 0:
            raise ValueError("estimated_minutes must be non-negative")
        mid = None if mission_id is None else str(mission_id).strip() or None
        sid = None if session_id is None else str(session_id).strip() or None
        return cls(
            label=(label or "Start Session").strip() or "Start Session",
            enabled=bool(enabled),
            mission_id=mid,
            session_id=sid,
            estimated_minutes=minutes,
            topic_title=(topic_title or "").strip(),
        )

    @property
    def can_start(self) -> bool:
        """True when the action is enabled and has an upstream identity."""
        return self.enabled and bool(self.mission_id or self.session_id)


@dataclass(frozen=True)
class ExperienceSession:
    """Presentation handle for one learning session in the student experience.

    Holds references only — educational execution belongs to Mission /
    Session Runtime engines.
    """

    experience_session_id: str
    student_id: str
    status: ExperienceSessionStatus = ExperienceSessionStatus.READY
    mission_id: str | None = None
    session_id: str | None = None
    topic_title: str = ""
    estimated_minutes: int | None = None
    started_at: str = ""
    completed_at: str = ""
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        experience_session_id: str,
        student_id: str,
        *,
        status: ExperienceSessionStatus | str = ExperienceSessionStatus.READY,
        mission_id: str | None = None,
        session_id: str | None = None,
        topic_title: str = "",
        estimated_minutes: int | None = None,
        started_at: str = "",
        completed_at: str = "",
        metadata: list[tuple[str, str]] | tuple[tuple[str, str], ...] | None = None,
    ) -> ExperienceSession:
        """Construct an experience session handle."""
        minutes = estimated_minutes
        if minutes is not None and minutes < 0:
            raise ValueError("estimated_minutes must be non-negative")
        return cls(
            experience_session_id=_require_non_empty(
                experience_session_id, "experience_session_id"
            ),
            student_id=_require_non_empty(student_id, "student_id"),
            status=_resolve_status(status),
            mission_id=(
                None if mission_id is None else str(mission_id).strip() or None
            ),
            session_id=(
                None if session_id is None else str(session_id).strip() or None
            ),
            topic_title=(topic_title or "").strip(),
            estimated_minutes=minutes,
            started_at=(started_at or "").strip(),
            completed_at=(completed_at or "").strip(),
            metadata=tuple(metadata or ()),
        )

    def start_action(self) -> StartSessionAction:
        """Derive the Start Session CTA from this handle."""
        enabled = self.status in {
            ExperienceSessionStatus.READY,
            ExperienceSessionStatus.IN_PROGRESS,
        }
        return StartSessionAction.create(
            enabled=enabled and bool(self.mission_id or self.session_id),
            mission_id=self.mission_id,
            session_id=self.session_id,
            estimated_minutes=self.estimated_minutes,
            topic_title=self.topic_title,
        )

    def with_status(
        self, status: ExperienceSessionStatus | str
    ) -> ExperienceSession:
        """Return a copy with updated status."""
        return ExperienceSession(
            experience_session_id=self.experience_session_id,
            student_id=self.student_id,
            status=_resolve_status(status),
            mission_id=self.mission_id,
            session_id=self.session_id,
            topic_title=self.topic_title,
            estimated_minutes=self.estimated_minutes,
            started_at=self.started_at,
            completed_at=self.completed_at,
            metadata=self.metadata,
        )


def _resolve_status(
    value: ExperienceSessionStatus | str,
) -> ExperienceSessionStatus:
    if isinstance(value, ExperienceSessionStatus):
        return value
    return ExperienceSessionStatus(str(value).strip().lower())


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
