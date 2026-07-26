"""DayExperienceAssembler — DailyMission + Timeline → DayExperience (P2-MS004/005).

Builds today's canonical Experience representation. Does not generate
educational recommendations or modify Programme I outputs.
"""

from __future__ import annotations

from app.application.unified_journey.daily_mission import (
    DailyMission,
    empty_daily_mission,
)
from app.application.unified_journey.day_experience import (
    DayExperience,
    empty_day_experience,
    phase_from_completion_status,
    progress_summary_for,
    upcoming_transition_for_phase,
)
from app.application.unified_journey.reflection_states import (
    ReflectionState,
    resolve_reflection_state,
)
from app.application.unified_journey.session_outcome import SessionOutcome
from app.application.unified_journey.session_phases import (
    SessionPhase,
    resolve_session_phase,
    session_status_label,
)
from app.application.unified_journey.timeline import (
    ExperienceTimeline,
    empty_experience_timeline,
    timeline_from_daily_mission,
    timeline_with_reflection,
)


class DayExperienceAssembler:
    """Assemble immutable DayExperience from Programme I presentation outputs.

    Responsibilities:
    - Combine DailyMission + ExperienceTimeline into DayExperience
    - Derive presentation phase / session status / upcoming transition
    - Expose reflection_available / session_outcome / reflection_state

    Non-responsibilities:
    - Educational calculations
    - Persistence / evidence writes
    - Runtime A / Strategy / Adaptive / Twin mutations
    """

    def assemble(
        self,
        mission: DailyMission | None,
        *,
        timeline: ExperienceTimeline | None = None,
        phase: SessionPhase | str | None = None,
        reflection_state: ReflectionState | str | None = None,
        session_outcome: SessionOutcome | None = None,
    ) -> DayExperience:
        """Derive DayExperience from DailyMission (and optional phase override)."""
        if mission is None:
            return empty_day_experience()

        resolved_phase = (
            resolve_session_phase(phase)
            if phase is not None
            else phase_from_completion_status(mission.completion_status)
        )
        post_session = resolved_phase in {
            SessionPhase.WRAPPING_UP,
            SessionPhase.COMPLETE,
        }
        active_outcome = session_outcome
        active_reflection = resolve_reflection_state(reflection_state)

        if post_session and active_outcome is None:
            active_outcome = _assemble_session_outcome(
                mission=mission,
                phase=resolved_phase,
            )

        # Guided Reflection unlocks when the session presentation is Complete.
        if (
            resolved_phase is SessionPhase.COMPLETE
            and active_outcome is not None
            and active_outcome.reflection_available
            and active_reflection is None
        ):
            active_reflection = ReflectionState.AVAILABLE

        upcoming = _upcoming_transition(
            phase=resolved_phase,
            reflection_state=active_reflection,
        )
        active_timeline = timeline or _timeline_for(
            mission,
            reflection_state=active_reflection,
        )
        reflection_flag = bool(
            post_session
            and (
                active_reflection
                in {ReflectionState.AVAILABLE, ReflectionState.IN_PROGRESS}
                or (
                    active_reflection is None
                    and resolved_phase
                    in {SessionPhase.WRAPPING_UP, SessionPhase.COMPLETE}
                )
            )
        )
        # Terminal reflection clears the "available" presentation flag.
        if active_reflection in {
            ReflectionState.COMPLETED,
            ReflectionState.SKIPPED,
        }:
            reflection_flag = False

        return DayExperience(
            daily_mission=mission,
            timeline=active_timeline,
            current_phase=resolved_phase,
            session_status=session_status_label(resolved_phase),
            reflection_available=reflection_flag,
            upcoming_transition=upcoming,
            progress_summary=progress_summary_for(
                mission=mission, phase=resolved_phase
            ),
            session_outcome=active_outcome if post_session else None,
            reflection_state=active_reflection,
            metadata=mission.metadata
            + (
                ("phase", resolved_phase.value),
                ("via", "day_experience_assembler"),
            ),
        )

    def assemble_placeholder(self) -> DayExperience:
        """Explicit placeholder DayExperience."""
        return self.assemble(
            empty_daily_mission(),
            timeline=empty_experience_timeline(),
            phase=SessionPhase.READY,
        )


def _assemble_session_outcome(
    *,
    mission: DailyMission,
    phase: SessionPhase,
) -> SessionOutcome:
    from app.application.unified_journey.session_outcome_assembler import (
        SessionOutcomeAssembler,
    )

    shell = DayExperience(
        daily_mission=mission,
        timeline=timeline_from_daily_mission(mission),
        current_phase=phase,
        session_status=session_status_label(phase),
        reflection_available=True,
        upcoming_transition=upcoming_transition_for_phase(phase),
        progress_summary=progress_summary_for(mission=mission, phase=phase),
    )
    return SessionOutcomeAssembler().assemble(shell)


def _upcoming_transition(
    *,
    phase: SessionPhase,
    reflection_state: ReflectionState | None,
) -> str:
    if reflection_state is ReflectionState.AVAILABLE:
        return "Take a brief moment to reflect"
    if reflection_state is ReflectionState.IN_PROGRESS:
        return "Finish or skip when ready"
    if reflection_state in {
        ReflectionState.COMPLETED,
        ReflectionState.SKIPPED,
    }:
        return "Today's learning day is complete"
    return upcoming_transition_for_phase(phase)


def _timeline_for(
    mission: DailyMission,
    *,
    reflection_state: ReflectionState | None,
) -> ExperienceTimeline:
    if reflection_state in {
        ReflectionState.AVAILABLE,
        ReflectionState.IN_PROGRESS,
    }:
        return timeline_with_reflection(mission)
    return timeline_from_daily_mission(mission)
