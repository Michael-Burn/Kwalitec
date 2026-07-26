"""JourneyService — Journey experience projection."""

from __future__ import annotations

from typing import Any

from app.application.educational_state import (
    EducationalStateService,
    EducationalStateSnapshot,
)
from app.application.student_experience._snapshots import journey_snapshot
from app.application.student_experience.dto.journey_snapshot import JourneySnapshot
from app.application.student_experience.exceptions import (
    JourneyError,
    PortUnavailable,
)
from app.application.student_experience.ports.learning_journey_port import (
    LearningJourneyPort,
)
from app.domain.student_experience.journey_projection import (
    JourneyProjection,
    JourneyTopicCard,
)
from app.domain.student_experience.recommendation_explanation import (
    translate_to_student_language,
)


class JourneyService:
    """Project the Journey surface from shared Educational State.

    Projection only. No journey progression authority.
    """

    def __init__(
        self,
        *,
        learning_journey: LearningJourneyPort | None = None,
        educational_state: EducationalStateService | None = None,
    ) -> None:
        self._journey = learning_journey
        self._educational_state = educational_state

    def journey(self, student_id: str) -> JourneySnapshot:
        """Build the Journey projection for ``student_id``."""
        sid = _require_id(student_id)
        progress, topics = self._progress_for(sid)

        current = None
        completed: list[JourneyTopicCard] = []
        upcoming: list[JourneyTopicCard] = []
        prereq_notes: list[str] = []

        for raw in topics:
            card = _topic_card(raw)
            status = str(raw.get("status") or card.status_label).strip().lower()
            if status in {"current", "in_progress", "active"}:
                current = card
            elif status in {"completed", "mastered", "done"}:
                completed.append(card)
            else:
                upcoming.append(card)
            if card.prerequisite_note:
                prereq_notes.append(card.prerequisite_note)

        if current is None and progress.get("current_topic_id"):
            current = JourneyTopicCard.create(
                str(progress["current_topic_id"]),
                translate_to_student_language(
                    str(progress.get("current_topic_title") or "Current topic")
                ),
                status_label="Current",
            )

        ratio = float(
            progress.get("overall_progress_ratio")
            or progress.get("progress")
            or 0.0
        )
        try:
            projection = JourneyProjection.create(
                sid,
                current_topic=current,
                completed_topics=completed,
                upcoming_topics=upcoming,
                overall_progress_ratio=max(0.0, min(1.0, ratio)),
                estimated_completion_label=translate_to_student_language(
                    str(progress.get("estimated_completion_label") or "")
                ),
                prerequisite_visibility=tuple(
                    translate_to_student_language(n) for n in prereq_notes
                ),
                examination_label=str(progress.get("examination_label") or ""),
            )
        except ValueError as exc:
            raise JourneyError(str(exc)) from exc
        return journey_snapshot(projection)

    def _progress_for(
        self, student_id: str
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if self._educational_state is not None:
            state = self._educational_state.load(student_id)
            if not state.journey_available:
                raise PortUnavailable("learning_journey port unavailable")
            return state.journey_progress, list(state.journey_topics)
        port = self._require_journey()
        return (
            port.get_journey_progress(student_id) or {},
            list(port.get_topic_list(student_id) or ()),
        )

    def _require_journey(self) -> LearningJourneyPort:
        if self._journey is None or not self._journey.is_available():
            raise PortUnavailable("learning_journey port unavailable")
        return self._journey

    def _state_snapshot(self, student_id: str) -> EducationalStateSnapshot | None:
        if self._educational_state is None:
            return None
        return self._educational_state.load(student_id)


def _topic_card(raw: dict[str, Any]) -> JourneyTopicCard:
    note = translate_to_student_language(
        str(raw.get("prerequisite_note") or raw.get("prerequisite") or "")
    )
    # Strip curriculum-graph jargon if an adapter leaked it.
    lowered = note.lower()
    if "graph" in lowered or "edge" in lowered or "node" in lowered:
        note = "Complete the earlier topics first to unlock this one."
    status = str(raw.get("status_label") or raw.get("status") or "").strip()
    return JourneyTopicCard.create(
        str(raw.get("topic_id") or raw.get("id") or "topic"),
        translate_to_student_language(
            str(raw.get("title") or raw.get("topic_title") or "Topic")
        ),
        status_label=status.title() if status else "",
        prerequisite_note=note,
    )


def _require_id(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise JourneyError("student_id must be a non-empty string")
    return value.strip()
