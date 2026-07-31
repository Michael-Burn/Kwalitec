"""Tomorrow Preview composition (KWP-015).

Surfaces tomorrow's mission continuity. Optional Start Early begins the
introduction today; Mission Runtime remains responsible for scheduling
adjustments — Educational Authoring only authors the preview language.
"""

from __future__ import annotations

from app.application.educational_authoring.dto import AuthoringContext, TomorrowPreview
from app.application.educational_authoring.duration import estimate_duration_minutes
from app.application.educational_authoring.guidance import scrub


def build_tomorrow_preview(context: AuthoringContext) -> TomorrowPreview:
    """Compose Tomorrow Preview from curriculum-aligned next topic."""
    tomorrow = scrub(context.tomorrow_topic_title)
    today = scrub(context.topic_title)
    if not tomorrow:
        # Soft fallback: first successor title when explicit tomorrow absent.
        successors = context.successor_titles
        tomorrow = scrub(successors[0]) if successors else ""
    if not tomorrow:
        return TomorrowPreview(has_preview=False)

    if today and tomorrow.lower() != today.lower():
        continuity = scrub(
            f"Building directly on today's {today} work."
        )
    else:
        continuity = scrub(
            "Continuing the same line of reasoning from today's session."
        )

    minutes = int(context.tomorrow_effort_minutes or 0)
    if minutes <= 0:
        minutes = estimate_duration_minutes(
            base_effort_minutes=context.estimated_effort_minutes or 45,
            difficulty_band=context.difficulty_band,
            student_pace_factor=context.student_pace_factor,
            activity_count=4,
        )

    return TomorrowPreview(
        topic_title=tomorrow,
        topic_id=(context.tomorrow_topic_id or "").strip(),
        topic_code=(context.tomorrow_topic_code or "").strip(),
        continuity_line=continuity,
        estimated_duration_minutes=minutes,
        start_early_available=True,
        start_early_label="Start Early",
        start_early_detail=scrub(
            "You may begin the introduction today. Tomorrow's Mission "
            "will adjust automatically."
        ),
        has_preview=True,
    )
