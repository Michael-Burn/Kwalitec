"""DailyMissionAssembler — JourneyContext → DailyMission (P2-MS003).

Simplifies presentation, removes subsystem terminology, and prepares
concise student-facing content. Does not generate educational
recommendations or modify subsystem outputs.
"""

from __future__ import annotations

import re

from app.application.unified_journey.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_PLACEHOLDER,
    COMPLETION_COMPLETE,
    COMPLETION_IN_PROGRESS,
    COMPLETION_NOT_STARTED,
    COMPLETION_UNKNOWN,
    JourneyContext,
    empty_journey_context,
)
from app.application.unified_journey.daily_mission import (
    DailyMission,
    MissionStartAction,
    empty_daily_mission,
    priority_from_urgency,
)
from app.application.unified_journey.stages import JourneyStage

# Internal terms that must never appear in learner-facing DailyMission copy.
_SUBSYSTEM_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = tuple(
    (
        re.compile(pattern, re.IGNORECASE),
        replacement,
    )
    for pattern, replacement in (
        (r"\bdigital\s+twin\b", "learning profile"),
        (r"\bstudent\s+twin\b", "learning profile"),
        (r"\badaptive\s+(?:engine|decision|recommendation)s?\b", "study guidance"),
        (r"\blearning\s+orchestrator\b", "study plan"),
        (r"\bmission\s+engine\b", "study plan"),
        (r"\bstrategy\s+engine\b", "study plan"),
        (r"\bevidence\s+platform\b", "learning progress"),
        (r"\bcurriculum\s+graph\b", "syllabus"),
        (r"\bgraph\s+node\b", "topic"),
        (r"\bgraph\s+edge\b", "link"),
        (r"\bruntime\s+a\b", "learning system"),
        (r"\bprogramme\s+i\b", ""),
    )
)

_WHITESPACE = re.compile(r"\s+")


class DailyMissionAssembler:
    """Transform JourneyContext into a presentation DailyMission.

    Responsibilities:
    - Simplify presentation fields
    - Remove subsystem terminology from student-facing copy
    - Prepare concise mission summary / CTA

    Non-responsibilities:
    - Educational recommendations
    - Modifying Programme I / subsystem outputs
    - Persistence
    """

    def assemble(self, context: JourneyContext | None) -> DailyMission:
        """Derive an immutable DailyMission from JourneyContext."""
        if context is None:
            return empty_daily_mission()

        title = _student_copy(context.mission_title) or "Today's Mission"
        reason = _student_copy(context.mission_reason)
        outcome = _student_copy(context.expected_outcome)
        duration = (context.estimated_duration or "").strip()
        completion = _resolve_completion(context)
        priority = priority_from_urgency(context.urgency)
        summary = _mission_summary(title=title, reason=reason, outcome=outcome)
        start_action = _start_action(context, completion=completion)

        return DailyMission(
            title=title,
            reason=reason,
            estimated_duration=duration,
            expected_outcome=outcome,
            priority=priority,
            completion_status=completion,
            start_action=start_action,
            mission_summary=summary,
            stage=context.stage or JourneyStage.DAILY_MISSION,
            metadata=context.metadata
            + (
                ("source", context.source),
                ("availability", context.availability),
                ("via", "daily_mission_assembler"),
            ),
        )

    def assemble_placeholder(
        self,
        *,
        stage: JourneyStage | str = JourneyStage.DAILY_MISSION,
    ) -> DailyMission:
        """Assemble from an explicit placeholder JourneyContext."""
        return self.assemble(empty_journey_context(stage=stage))


def _resolve_completion(context: JourneyContext) -> str:
    """Map JourneyContext completion onto UI completion vocabulary."""
    raw = (context.completion_state or "").strip().lower()
    if raw in {
        COMPLETION_NOT_STARTED,
        COMPLETION_IN_PROGRESS,
        COMPLETION_COMPLETE,
    }:
        return raw
    if raw == COMPLETION_UNKNOWN:
        # Available mission with no explicit state → Not Started (UI default).
        if (
            context.availability == AVAILABILITY_AVAILABLE
            and (context.mission_title or "").strip()
        ):
            return COMPLETION_NOT_STARTED
        return COMPLETION_UNKNOWN
    return COMPLETION_UNKNOWN


def _start_action(
    context: JourneyContext,
    *,
    completion: str,
) -> MissionStartAction:
    """Build presentation CTA from context — no educational decisions."""
    if completion == COMPLETION_COMPLETE:
        label = "Mission complete"
        enabled = False
    elif completion == COMPLETION_IN_PROGRESS:
        label = _student_copy(context.cta_label) or "Continue Mission"
        enabled = bool(context.cta_enabled)
    else:
        label = _student_copy(context.cta_label) or "Start Today's Mission"
        enabled = bool(context.cta_enabled)
    if context.availability == AVAILABILITY_PLACEHOLDER:
        enabled = False
    return MissionStartAction(
        label=label,
        enabled=enabled,
        endpoint=(context.endpoint or "").strip(),
    )


def _mission_summary(*, title: str, reason: str, outcome: str) -> str:
    """Concise student-facing summary — presentation only."""
    if reason:
        return _first_sentence(reason)
    if outcome:
        return _first_sentence(outcome)
    if title and title.casefold() != "today's mission":
        return title
    return ""


def _first_sentence(text: str) -> str:
    cleaned = _WHITESPACE.sub(" ", (text or "").strip())
    if not cleaned:
        return ""
    for sep in (". ", "! ", "? "):
        if sep in cleaned:
            head, _sep, _rest = cleaned.partition(sep)
            return f"{head}{sep.strip()}"
    if len(cleaned) <= 160:
        return cleaned
    return cleaned[:157].rstrip() + "…"


def _student_copy(text: str) -> str:
    """Strip / soften subsystem terminology for learner-facing display."""
    value = (text or "").strip()
    if not value:
        return ""
    for pattern, replacement in _SUBSYSTEM_PATTERNS:
        value = pattern.sub(replacement, value)
    value = _WHITESPACE.sub(" ", value).strip(" -–,;")
    return value
