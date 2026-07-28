"""Educational Timeline service (ILE-003).

Loads Decision Journal educational memory and interprets it into a
reflective chronological narrative. Preference / narrative only —
never mastery mutation, Twin changes, or recommendation ranking.
"""

from __future__ import annotations

import logging
from typing import Any

from app.domain.educational_timeline import (
    EducationalNarrative,
    NarrativeCertainty,
    assert_narrative_humble,
    build_educational_narrative,
)
from app.services.decision_journal_service import DecisionJournalService

logger = logging.getLogger(__name__)

CERTAINTY_LABELS: dict[str, str] = {
    NarrativeCertainty.INSUFFICIENT.value: (
        "Limited journal evidence so far — readings stay tentative."
    ),
    NarrativeCertainty.SUGGESTIVE.value: (
        "Patterns are suggested by your journal, not proven."
    ),
    NarrativeCertainty.SUPPORTED.value: (
        "Patterns below are supported by several journal entries."
    ),
}


class EducationalTimelineService:
    """Interpret Decision Journal entries as an Educational Timeline."""

    @staticmethod
    def build_for_user(
        user_id: int,
        *,
        limit: int = 100,
        include_archived: bool = True,
    ) -> EducationalNarrative:
        """Load journal evidence and build the reflective narrative.

        Args:
            user_id: Owning learner.
            limit: Max journal entries to consider (newest window).
            include_archived: Whether archived journal rows contribute.

        Returns:
            ``EducationalNarrative`` derived solely from journal evidence.
        """
        rows = DecisionJournalService.get_timeline(
            user_id,
            limit=limit,
            include_archived=include_archived,
        )
        # Oldest-first evidence for chronological story; service returns newest-first.
        chronological = list(reversed(rows))
        payloads: list[dict[str, Any]] = []
        for row in chronological:
            payload = DecisionJournalService.to_student_dict(row)
            payload["recorded_at"] = row.recorded_at
            payloads.append(payload)

        narrative = build_educational_narrative(payloads)
        EducationalTimelineService._validate_narrative(narrative)
        logger.info(
            "educational_timeline_built user_id=%s entries=%s sections=%s",
            user_id,
            narrative.entry_count,
            len(narrative.sections),
        )
        return narrative

    @staticmethod
    def certainty_label(certainty: NarrativeCertainty | str) -> str:
        """Student-safe label for overall narrative certainty."""
        key = str(certainty)
        return CERTAINTY_LABELS.get(
            key,
            CERTAINTY_LABELS[NarrativeCertainty.SUGGESTIVE.value],
        )

    @staticmethod
    def _validate_narrative(narrative: EducationalNarrative) -> None:
        """Enforce humility and student-safe language on generated speech."""
        for section in narrative.sections:
            for moment in section.moments:
                for field, text in (
                    ("observation", moment.observation),
                    ("pattern", moment.pattern),
                    ("educational_meaning", moment.educational_meaning),
                    ("reflection_question", moment.reflection_question),
                    ("title", moment.title),
                ):
                    if not text:
                        continue
                    assert_narrative_humble(
                        text,
                        certainty=moment.certainty,
                        field=field,
                    )
