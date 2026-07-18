"""Immutable RevisionSnapshot DTO for Student Experience."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)


@dataclass(frozen=True)
class RevisionOptionSnapshot:
    """Read-only revision option."""

    option_id: str
    topic_title: str
    priority_label: str = ""
    estimated_study_minutes: int | None = None
    expected_benefit: str = ""
    explanation: ExplanationSnapshot | None = None
    is_primary: bool = False


@dataclass(frozen=True)
class RevisionSnapshot:
    """Revision experience projection DTO."""

    student_id: str
    primary: RevisionOptionSnapshot | None = None
    alternatives: tuple[RevisionOptionSnapshot, ...] = field(
        default_factory=tuple
    )
    empty_message: str = ""
    has_revision: bool = False
    option_count: int = 0
