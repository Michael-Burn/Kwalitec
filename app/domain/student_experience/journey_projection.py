"""Journey projection — learner journey progress without graph jargon."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class JourneyTopicCard:
    """Student-facing topic summary for journey surfaces."""

    topic_id: str
    title: str
    status_label: str = ""
    prerequisite_note: str = ""

    @classmethod
    def create(
        cls,
        topic_id: str,
        title: str,
        *,
        status_label: str = "",
        prerequisite_note: str = "",
    ) -> JourneyTopicCard:
        """Build a topic card after validating identities."""
        return cls(
            topic_id=_require_non_empty(topic_id, "topic_id"),
            title=_require_non_empty(title, "title"),
            status_label=(status_label or "").strip(),
            prerequisite_note=(prerequisite_note or "").strip(),
        )


@dataclass(frozen=True)
class JourneyProjection:
    """Domain projection for the Journey experience.

    Represents current / completed / upcoming topics and overall progress.
    Does not expose curriculum graph concepts.
    """

    student_id: str
    current_topic: JourneyTopicCard | None = None
    completed_topics: tuple[JourneyTopicCard, ...] = field(default_factory=tuple)
    upcoming_topics: tuple[JourneyTopicCard, ...] = field(default_factory=tuple)
    overall_progress_ratio: float = 0.0
    estimated_completion_label: str = ""
    prerequisite_visibility: tuple[str, ...] = field(default_factory=tuple)
    examination_label: str = ""

    @classmethod
    def create(
        cls,
        student_id: str,
        *,
        current_topic: JourneyTopicCard | None = None,
        completed_topics: (
            list[JourneyTopicCard] | tuple[JourneyTopicCard, ...] | None
        ) = None,
        upcoming_topics: (
            list[JourneyTopicCard] | tuple[JourneyTopicCard, ...] | None
        ) = None,
        overall_progress_ratio: float = 0.0,
        estimated_completion_label: str = "",
        prerequisite_visibility: list[str] | tuple[str, ...] | None = None,
        examination_label: str = "",
    ) -> JourneyProjection:
        """Build a journey projection."""
        ratio = float(overall_progress_ratio)
        if not 0.0 <= ratio <= 1.0:
            raise ValueError("overall_progress_ratio must be between 0 and 1")
        notes = prerequisite_visibility or ()
        return cls(
            student_id=_require_non_empty(student_id, "student_id"),
            current_topic=current_topic,
            completed_topics=tuple(completed_topics or ()),
            upcoming_topics=tuple(upcoming_topics or ()),
            overall_progress_ratio=ratio,
            estimated_completion_label=(estimated_completion_label or "").strip(),
            prerequisite_visibility=tuple(
                str(p).strip() for p in notes if str(p).strip()
            ),
            examination_label=(examination_label or "").strip(),
        )

    @property
    def completed_count(self) -> int:
        return len(self.completed_topics)

    @property
    def upcoming_count(self) -> int:
        return len(self.upcoming_topics)

    @property
    def progress_percent(self) -> int:
        return int(round(self.overall_progress_ratio * 100))


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
