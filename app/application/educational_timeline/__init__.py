"""Educational Timeline application service (ILE-003).

Orchestrates reflective narrative for presentation. No HTTP; no Twin;
no recommendation ranking. Reads Decision Journal; does not duplicate it.
"""

from __future__ import annotations

from app.application.educational_timeline.dto import (
    EducationalTimelineSnapshot,
    NarrativeMomentSnapshot,
    TimelineSectionSnapshot,
)
from app.domain.educational_timeline import NarrativeCertainty
from app.services.educational_timeline_service import (
    CERTAINTY_LABELS,
    EducationalTimelineService,
)


class EducationalTimelineApplicationService:
    """Application façade over ``EducationalTimelineService``."""

    @staticmethod
    def timeline(
        user_id: int,
        *,
        limit: int = 100,
        include_archived: bool = True,
    ) -> EducationalTimelineSnapshot:
        """Build the student Educational Timeline snapshot."""
        narrative = EducationalTimelineService.build_for_user(
            user_id,
            limit=limit,
            include_archived=include_archived,
        )
        sections = tuple(
            TimelineSectionSnapshot(
                kind=section.kind.value,
                label=section.label,
                intro=section.intro,
                anchor_id=f"timeline-{section.kind.value.replace('_', '-')}",
                moments=tuple(
                    NarrativeMomentSnapshot(
                        title=moment.title,
                        when_label=moment.when_label,
                        observation=moment.observation,
                        pattern=moment.pattern,
                        educational_meaning=moment.educational_meaning,
                        reflection_question=moment.reflection_question,
                        certainty_label=CERTAINTY_LABELS.get(
                            str(moment.certainty),
                            CERTAINTY_LABELS[
                                NarrativeCertainty.SUGGESTIVE.value
                            ],
                        ),
                        evidence_decision_ids=moment.evidence_decision_ids,
                    )
                    for moment in section.moments
                ),
            )
            for section in narrative.sections
        )
        return EducationalTimelineSnapshot(
            sections=sections,
            entry_count=narrative.entry_count,
            empty=narrative.empty or len(sections) == 0,
            certainty_label=EducationalTimelineService.certainty_label(
                narrative.certainty
            ),
        )
