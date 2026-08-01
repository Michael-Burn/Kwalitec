"""Educational Authoring DTOs — Learning Episodes & Mission composition (KWP-015).

Immutable projections. Educational Authoring owns educational composition
only — it never mutates Strategy, Diagnostics, Difficulty, Evidence,
Progress, Forecast, Memory, Knowledge Architecture graphs, Adaptive
Workspace engines, or Mission Runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class EpisodeActivityKind(StrEnum):
    """Deterministic activity kinds inside a Learning Episode."""

    READ = "read"
    WORKED_EXAMPLE = "worked_example"
    PRACTICE = "practice"
    REFLECTION = "reflection"
    REVISION = "revision"
    CHECKPOINT = "checkpoint"


class ExtraStudyKind(StrEnum):
    """Offers when available time exceeds today's mission."""

    CONTINUE_REVISION = "continue_revision"
    START_TOMORROW = "start_tomorrow"


ACTIVITY_TITLES: dict[EpisodeActivityKind, str] = {
    EpisodeActivityKind.READ: "Read",
    EpisodeActivityKind.WORKED_EXAMPLE: "Worked Example",
    EpisodeActivityKind.PRACTICE: "Practice",
    EpisodeActivityKind.REFLECTION: "Reflection",
    EpisodeActivityKind.REVISION: "Revision",
    EpisodeActivityKind.CHECKPOINT: "Checkpoint",
}


@dataclass(frozen=True)
class AuthoringContext:
    """Inputs for educational composition — curriculum-grounded only."""

    topic_id: str = ""
    topic_title: str = ""
    topic_code: str = ""
    objective_text: str = ""
    objective_ids: tuple[str, ...] = ()
    concept_titles: tuple[str, ...] = ()
    prerequisite_titles: tuple[str, ...] = ()
    successor_titles: tuple[str, ...] = ()
    foundation_titles: tuple[str, ...] = ()
    estimated_effort_minutes: int = 0
    difficulty_band: str = ""
    student_pace_factor: float = 1.0
    previous_evidence_minutes: int = 0
    weak_topic: bool = False
    available_minutes: int | None = None
    tomorrow_topic_id: str = ""
    tomorrow_topic_title: str = ""
    tomorrow_topic_code: str = ""
    tomorrow_effort_minutes: int = 0
    recently_strengthened_titles: tuple[str, ...] = ()
    revision_available: bool = False
    mission_instance_id: str = ""
    subject_code: str = ""
    # RO1-R1 — bind composition / Tomorrow Preview to approved package identity
    educational_package_id: str = ""
    completed_package_ids: frozenset[str] | None = None
    last_completed_package_id: str = ""
    prefer_completed_package: bool = False


@dataclass(frozen=True)
class EpisodeActivity:
    """One deterministic activity within a Learning Episode."""

    kind: EpisodeActivityKind
    title: str
    prompt: str
    sequence: int = 1
    estimated_minutes: int = 0

    def to_opaque(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "title": self.title,
            "prompt": self.prompt,
            "sequence": self.sequence,
            "estimated_minutes": self.estimated_minutes,
        }


@dataclass(frozen=True)
class LearningEpisode:
    """Smallest educational experience — authored, not assembled from CMP text.

    Every mission consists of one or more Learning Episodes.
    """

    episode_id: str
    educational_context: str
    learning_objective: str
    concept_focus: tuple[str, ...]
    activities: tuple[EpisodeActivity, ...]
    success_criteria: tuple[str, ...]
    estimated_duration_minutes: int
    connection: str
    topic_id: str = ""
    topic_title: str = ""
    sequence: int = 1
    alignment_codes: tuple[str, ...] = ()

    @property
    def estimated_duration_label(self) -> str:
        return _minutes_label(self.estimated_duration_minutes)

    @property
    def has_episode(self) -> bool:
        return bool(self.learning_objective or self.educational_context)

    def to_opaque(self) -> dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "educational_context": self.educational_context,
            "learning_objective": self.learning_objective,
            "concept_focus": list(self.concept_focus),
            "activities": [a.to_opaque() for a in self.activities],
            "success_criteria": list(self.success_criteria),
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "estimated_duration_label": self.estimated_duration_label,
            "connection": self.connection,
            "topic_id": self.topic_id,
            "topic_title": self.topic_title,
            "sequence": self.sequence,
            "alignment_codes": list(self.alignment_codes),
        }


@dataclass(frozen=True)
class TomorrowPreview:
    """Tomorrow's Mission preview — continuity without fabricating content."""

    topic_title: str = ""
    topic_id: str = ""
    topic_code: str = ""
    continuity_line: str = ""
    estimated_duration_minutes: int = 0
    start_early_available: bool = False
    start_early_label: str = "Start Early"
    start_early_detail: str = ""
    has_preview: bool = False

    @property
    def estimated_duration_label(self) -> str:
        return _minutes_label(self.estimated_duration_minutes)

    def to_opaque(self) -> dict[str, Any]:
        return {
            "topic_title": self.topic_title,
            "topic_id": self.topic_id,
            "topic_code": self.topic_code,
            "continuity_line": self.continuity_line,
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "estimated_duration_label": self.estimated_duration_label,
            "start_early_available": self.start_early_available,
            "start_early_label": self.start_early_label,
            "start_early_detail": self.start_early_detail,
            "has_preview": self.has_preview,
        }


@dataclass(frozen=True)
class ExtraStudyOffer:
    """What to do when available time exceeds today's mission."""

    kind: ExtraStudyKind
    label: str
    detail: str
    href_hint: str = ""

    def to_opaque(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "label": self.label,
            "detail": self.detail,
            "href_hint": self.href_hint,
        }


@dataclass(frozen=True)
class MissionComposition:
    """Authored mission arc for Adaptive Workspace.

    Morning Brief (workspace) → Learning Episode(s) → Checkpoint →
    Reflection → Tomorrow Preview. Educational Authoring owns composition
    language; Mission Runtime still owns selection and scheduling.
    """

    episodes: tuple[LearningEpisode, ...] = ()
    checkpoint_prompt: str = ""
    reflection_prompt: str = ""
    tomorrow_preview: TomorrowPreview | None = None
    extra_study: tuple[ExtraStudyOffer, ...] = ()
    mission_narrative: str = ""
    total_duration_minutes: int = 0
    alignment_codes: tuple[str, ...] = ()
    has_composition: bool = False

    @property
    def primary_episode(self) -> LearningEpisode | None:
        return self.episodes[0] if self.episodes else None

    @property
    def total_duration_label(self) -> str:
        return _minutes_label(self.total_duration_minutes)

    def to_opaque(self) -> dict[str, Any]:
        return {
            "episodes": [e.to_opaque() for e in self.episodes],
            "checkpoint_prompt": self.checkpoint_prompt,
            "reflection_prompt": self.reflection_prompt,
            "tomorrow_preview": (
                self.tomorrow_preview.to_opaque()
                if self.tomorrow_preview
                else None
            ),
            "extra_study": [o.to_opaque() for o in self.extra_study],
            "mission_narrative": self.mission_narrative,
            "total_duration_minutes": self.total_duration_minutes,
            "total_duration_label": self.total_duration_label,
            "alignment_codes": list(self.alignment_codes),
            "has_composition": self.has_composition,
        }


@dataclass(frozen=True)
class EducationalAuthoringSnapshot:
    """Founder / diagnostics snapshot of authoring output."""

    episode_count: int = 0
    total_duration_minutes: int = 0
    activity_kinds: tuple[str, ...] = ()
    has_tomorrow_preview: bool = False
    extra_study_kinds: tuple[str, ...] = ()
    alignment_codes: tuple[str, ...] = ()
    subject_label: str = ""
    event_counts: dict[str, int] = field(default_factory=dict)

    def to_opaque(self) -> dict[str, Any]:
        return {
            "episode_count": self.episode_count,
            "total_duration_minutes": self.total_duration_minutes,
            "activity_kinds": list(self.activity_kinds),
            "has_tomorrow_preview": self.has_tomorrow_preview,
            "extra_study_kinds": list(self.extra_study_kinds),
            "alignment_codes": list(self.alignment_codes),
            "subject_label": self.subject_label,
            "event_counts": dict(self.event_counts),
        }


def _minutes_label(minutes: int) -> str:
    mins = max(0, int(minutes or 0))
    if mins <= 0:
        return ""
    if mins < 60:
        return f"{mins} minutes"
    hours, rem = divmod(mins, 60)
    if rem == 0:
        return f"{hours} h" if hours != 1 else "1 h"
    return f"{hours} h {rem} min"
