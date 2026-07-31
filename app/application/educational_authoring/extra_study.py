"""Extra Study flow (KWP-015).

When available time exceeds today's mission, offer Continue Revision
or Start Tomorrow — never leave students asking "What now?"
"""

from __future__ import annotations

from app.application.educational_authoring.dto import (
    AuthoringContext,
    ExtraStudyKind,
    ExtraStudyOffer,
)
from app.application.educational_authoring.guidance import scrub


def build_extra_study_offers(
    context: AuthoringContext,
    *,
    mission_minutes: int,
) -> tuple[ExtraStudyOffer, ...]:
    """Return offers when spare capacity remains after today's mission."""
    available = context.available_minutes
    if available is None:
        return ()
    spare = int(available) - max(0, int(mission_minutes or 0))
    if spare < 15:
        return ()

    offers: list[ExtraStudyOffer] = []
    if context.revision_available or context.weak_topic:
        offers.append(
            ExtraStudyOffer(
                kind=ExtraStudyKind.CONTINUE_REVISION,
                label="Continue Revision",
                detail=scrub(
                    "Use the remaining time to consolidate topics that "
                    "still need careful attention."
                ),
                href_hint="revision",
            )
        )

    tomorrow = scrub(context.tomorrow_topic_title)
    if not tomorrow and context.successor_titles:
        tomorrow = scrub(context.successor_titles[0])
    if tomorrow:
        offers.append(
            ExtraStudyOffer(
                kind=ExtraStudyKind.START_TOMORROW,
                label="Start Tomorrow",
                detail=scrub(
                    f"Begin the introduction to {tomorrow}. Tomorrow's "
                    f"Mission will adjust automatically."
                ),
                href_hint="start_tomorrow",
            )
        )
    elif not offers:
        offers.append(
            ExtraStudyOffer(
                kind=ExtraStudyKind.CONTINUE_REVISION,
                label="Continue Revision",
                detail=scrub(
                    "Use the remaining time for calm consolidation of "
                    "today's foundations."
                ),
                href_hint="revision",
            )
        )

    return tuple(offers)
