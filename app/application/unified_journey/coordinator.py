"""Journey Coordinator — Experience Layer orchestration (P2-MS001–P2-MS005).

Determines current stage, requests JourneyContext, assembles DailyMission /
DayExperience / StudySession / ReflectionExperience, resolves next action,
coordinates subsystem outputs, and maintains in-memory journey state.

Orchestration sequence: Stage → Context → DailyMission → DayExperience →
StudySession / SessionOutcome → ReflectionExperience / NextBestAction.

Authority boundaries:
- MAY consume Runtime A / Digital Twin / Adaptive / Strategy / Evidence
  projections read-only.
- MUST NOT modify, replace, or recalculate those projections.
- MUST NOT contain educational logic or invent recommendations.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.application.unified_journey.assembler import JourneyContextAssembler
from app.application.unified_journey.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_PLACEHOLDER,
    SOURCE_ADAPTIVE,
    SOURCE_DIGITAL_TWIN,
    SOURCE_EVIDENCE,
    SOURCE_PLACEHOLDER,
    SOURCE_RUNTIME_A,
    SOURCE_STRATEGY,
    HomePrimaryMission,
    JourneyContext,
    JourneyProgress,
    JourneyState,
    JourneySubsystemInputs,
    NextBestAction,
    empty_journey_progress,
    empty_journey_state,
    empty_next_best_action,
    home_mission_from_context,
    next_action_from_context,
)
from app.application.unified_journey.daily_mission import DailyMission
from app.application.unified_journey.daily_mission_assembler import (
    DailyMissionAssembler,
)
from app.application.unified_journey.day_experience import DayExperience
from app.application.unified_journey.day_experience_assembler import (
    DayExperienceAssembler,
)
from app.application.unified_journey.navigation_map import endpoint_for_stage
from app.application.unified_journey.reflection_assembler import (
    ReflectionAssembler,
)
from app.application.unified_journey.reflection_controls import (
    ReflectionControlResult,
    apply_reflection_control,
)
from app.application.unified_journey.reflection_experience import (
    ReflectionExperience,
)
from app.application.unified_journey.reflection_states import (
    ReflectionControl,
    ReflectionState,
)
from app.application.unified_journey.session_controls import (
    SessionControlResult,
    apply_session_control,
)
from app.application.unified_journey.session_outcome import SessionOutcome
from app.application.unified_journey.session_outcome_assembler import (
    SessionOutcomeAssembler,
)
from app.application.unified_journey.session_phases import (
    SessionControl,
    SessionPhase,
)
from app.application.unified_journey.stages import (
    JourneyStage,
    resolve_journey_stage,
)
from app.application.unified_journey.study_session import StudySession
from app.application.unified_journey.study_session_assembler import (
    StudySessionAssembler,
)
from app.application.unified_journey.timeline import (
    ExperienceTimeline,
    timeline_from_daily_mission,
)

_STAGE_KEY = "journey_stage"
_SOURCE_PRIORITY: tuple[tuple[str, str], ...] = (
    ("strategy", SOURCE_STRATEGY),
    ("adaptive", SOURCE_ADAPTIVE),
    ("digital_twin", SOURCE_DIGITAL_TWIN),
    ("runtime_a", SOURCE_RUNTIME_A),
    ("evidence", SOURCE_EVIDENCE),
)


class JourneyCoordinator:
    """Orchestrates the unified student journey without deciding education.

    Stateless by default: each call accepts optional subsystem inputs and
    returns immutable DTOs. No persistence. No educational calculations.

    Sequence: resolve stage → assemble JourneyContext → project NextBestAction.
    """

    def __init__(
        self,
        *,
        assembler: JourneyContextAssembler | None = None,
        daily_mission_assembler: DailyMissionAssembler | None = None,
        day_experience_assembler: DayExperienceAssembler | None = None,
        study_session_assembler: StudySessionAssembler | None = None,
        session_outcome_assembler: SessionOutcomeAssembler | None = None,
        reflection_assembler: ReflectionAssembler | None = None,
    ) -> None:
        self._assembler = assembler or JourneyContextAssembler()
        self._daily_mission_assembler = (
            daily_mission_assembler or DailyMissionAssembler()
        )
        self._day_experience_assembler = (
            day_experience_assembler or DayExperienceAssembler()
        )
        self._study_session_assembler = (
            study_session_assembler or StudySessionAssembler()
        )
        self._session_outcome_assembler = (
            session_outcome_assembler or SessionOutcomeAssembler()
        )
        self._reflection_assembler = (
            reflection_assembler or ReflectionAssembler()
        )

    def current_stage(
        self,
        student_id: str,
        *,
        inputs: JourneySubsystemInputs | None = None,
    ) -> JourneyStage:
        """Resolve the current journey stage from pass-through signals.

        Prefers explicit ``stage_hint``, then opaque subsystem ``journey_stage``
        fields, then the Daily Mission placeholder. Never infers stage from
        mastery, readiness, or other educational formulas.
        """
        _require_student_id(student_id)
        active = inputs or JourneySubsystemInputs()
        if active.stage_hint is not None:
            return resolve_journey_stage(active.stage_hint)
        for attr, _source in _SOURCE_PRIORITY:
            projection = getattr(active, attr)
            stage = _stage_from_projection(projection)
            if stage is not None:
                return stage
        return JourneyStage.DAILY_MISSION

    def journey_context(
        self,
        student_id: str,
        *,
        inputs: JourneySubsystemInputs | None = None,
    ) -> JourneyContext:
        """Request presentation-ready JourneyContext for the active stage.

        Orchestration only — assembly is delegated to JourneyContextAssembler.
        """
        sid = _require_student_id(student_id)
        active = inputs or JourneySubsystemInputs()
        stage = self.current_stage(sid, inputs=active)
        return self._assembler.assemble(
            student_id=sid,
            stage=stage,
            inputs=active,
        )

    def next_action(
        self,
        student_id: str,
        *,
        inputs: JourneySubsystemInputs | None = None,
    ) -> NextBestAction:
        """Resolve the next Experience action from JourneyContext.

        Passes through an explicit next action when provided; otherwise
        projects from the assembled JourneyContext. Never invents education.
        """
        active = inputs or JourneySubsystemInputs()
        if active.next_action is not None:
            return active.next_action
        context = self.journey_context(student_id, inputs=active)
        if context.availability == AVAILABILITY_AVAILABLE and context.mission_title:
            return next_action_from_context(context)
        stage = context.stage
        placeholder = empty_next_best_action(stage=stage)
        return NextBestAction(
            action_id=placeholder.action_id,
            stage=stage,
            title=placeholder.title,
            summary=placeholder.summary,
            cta_label=placeholder.cta_label,
            endpoint=endpoint_for_stage(stage),
            estimated_minutes=None,
            why_it_matters=placeholder.why_it_matters,
            expected_outcome=placeholder.expected_outcome,
            source=SOURCE_PLACEHOLDER,
            availability=AVAILABILITY_PLACEHOLDER,
            unavailable_reason="engines_not_connected",
        )

    def progress(
        self,
        student_id: str,
        *,
        inputs: JourneySubsystemInputs | None = None,
    ) -> JourneyProgress:
        """Return journey progress projection or a placeholder."""
        stage = self.current_stage(student_id, inputs=inputs)
        active = inputs or JourneySubsystemInputs()
        if active.progress is not None:
            return active.progress
        return empty_journey_progress(current_stage=stage)

    def journey_state(
        self,
        student_id: str,
        *,
        inputs: JourneySubsystemInputs | None = None,
    ) -> JourneyState:
        """Assemble immutable journey state for Experience chrome / Home."""
        sid = _require_student_id(student_id)
        active = inputs or JourneySubsystemInputs()
        stage = self.current_stage(sid, inputs=active)
        context = self.journey_context(sid, inputs=active)
        next_action = self.next_action(sid, inputs=active)
        progress = self.progress(sid, inputs=active)
        if (
            active.stage_hint is None
            and active.next_action is None
            and active.progress is None
            and active.journey_context is None
            and active.home_mission is None
            and not _any_projection(active)
        ):
            state = empty_journey_state(sid)
            return JourneyState(
                student_id=sid,
                current_stage=stage,
                next_action=next_action,
                progress=progress,
                availability=state.availability,
                unavailable_reason=state.unavailable_reason,
                metadata=(("journey_context_source", context.source),),
            )
        available = (
            context.availability == AVAILABILITY_AVAILABLE
            or active.next_action is not None
            or active.stage_hint is not None
            or active.journey_context is not None
        )
        return JourneyState(
            student_id=sid,
            current_stage=stage,
            next_action=next_action,
            progress=progress,
            availability=(
                AVAILABILITY_AVAILABLE if available else AVAILABILITY_PLACEHOLDER
            ),
            unavailable_reason="" if available else "engines_not_connected",
            metadata=(("journey_context_source", context.source),),
        )

    def home_primary_mission(
        self,
        student_id: str,
        *,
        inputs: JourneySubsystemInputs | None = None,
    ) -> HomePrimaryMission:
        """Home architecture projection derived from JourneyContext.

        Uses pass-through home mission when provided; otherwise projects from
        JourneyContext. Does not invent educational behaviour.
        """
        _require_student_id(student_id)
        active = inputs or JourneySubsystemInputs()
        if active.home_mission is not None:
            return active.home_mission
        context = self.journey_context(student_id, inputs=active)
        return home_mission_from_context(context)

    def daily_mission(
        self,
        student_id: str,
        *,
        inputs: JourneySubsystemInputs | None = None,
    ) -> DailyMission:
        """Canonical Home presentation model derived from JourneyContext.

        Experience Layer only — never invents educational recommendations.
        """
        context = self.journey_context(student_id, inputs=inputs)
        return self._daily_mission_assembler.assemble(context)

    def experience_timeline(
        self,
        student_id: str,
        *,
        inputs: JourneySubsystemInputs | None = None,
    ) -> ExperienceTimeline:
        """Today's journey timeline from the assembled DailyMission."""
        mission = self.daily_mission(student_id, inputs=inputs)
        return timeline_from_daily_mission(mission)

    def day_experience(
        self,
        student_id: str,
        *,
        inputs: JourneySubsystemInputs | None = None,
        phase: SessionPhase | str | None = None,
        reflection_state: ReflectionState | str | None = None,
    ) -> DayExperience:
        """Canonical daily Experience object for guided study (P2-MS004/005).

        Assembled from DailyMission + ExperienceTimeline. Presentation only.
        """
        mission = self.daily_mission(student_id, inputs=inputs)
        timeline = timeline_from_daily_mission(mission)
        return self._day_experience_assembler.assemble(
            mission,
            timeline=timeline,
            phase=phase,
            reflection_state=reflection_state,
        )

    def study_session(
        self,
        student_id: str,
        *,
        inputs: JourneySubsystemInputs | None = None,
        phase: SessionPhase | str | None = None,
        day: DayExperience | None = None,
    ) -> StudySession:
        """Guided StudySession view model from DayExperience (P2-MS004)."""
        active_day = day or self.day_experience(
            student_id, inputs=inputs, phase=phase
        )
        return self._study_session_assembler.assemble(active_day)

    def session_outcome(
        self,
        student_id: str,
        *,
        inputs: JourneySubsystemInputs | None = None,
        phase: SessionPhase | str | None = None,
        day: DayExperience | None = None,
    ) -> SessionOutcome:
        """Canonical post-session presentation object (P2-MS005)."""
        active_day = day or self.day_experience(
            student_id, inputs=inputs, phase=phase
        )
        if active_day.session_outcome is not None:
            return active_day.session_outcome
        return self._session_outcome_assembler.assemble(active_day)

    def reflection_experience(
        self,
        student_id: str,
        *,
        inputs: JourneySubsystemInputs | None = None,
        phase: SessionPhase | str | None = None,
        day: DayExperience | None = None,
        reflection_state: ReflectionState | str | None = None,
    ) -> ReflectionExperience:
        """Guided ReflectionExperience from SessionOutcome (P2-MS005)."""
        active_day = day or self.day_experience(
            student_id,
            inputs=inputs,
            phase=phase,
            reflection_state=reflection_state,
        )
        outcome = (
            active_day.session_outcome
            or self._session_outcome_assembler.assemble(active_day)
        )
        state = reflection_state or active_day.reflection_state
        return self._reflection_assembler.assemble(outcome, state=state)

    def apply_session_control(
        self,
        student_id: str,
        control: SessionControl | str,
        *,
        inputs: JourneySubsystemInputs | None = None,
        day: DayExperience | None = None,
        phase: SessionPhase | str | None = None,
    ) -> SessionControlResult:
        """Apply Start / Resume / Finish presentation controls (no persistence)."""
        _require_student_id(student_id)
        active_day = day or self.day_experience(
            student_id, inputs=inputs, phase=phase
        )
        return apply_session_control(active_day, control)

    def apply_reflection_control(
        self,
        student_id: str,
        control: ReflectionControl | str,
        *,
        inputs: JourneySubsystemInputs | None = None,
        day: DayExperience | None = None,
        phase: SessionPhase | str | None = None,
        reflection_state: ReflectionState | str | None = None,
    ) -> ReflectionControlResult:
        """Apply Start / Complete / Skip reflection controls (no persistence)."""
        _require_student_id(student_id)
        active_day = day or self.day_experience(
            student_id,
            inputs=inputs,
            phase=phase,
            reflection_state=reflection_state,
        )
        return apply_reflection_control(active_day, control)


def _require_student_id(student_id: str) -> str:
    if not isinstance(student_id, str) or not student_id.strip():
        raise ValueError("student_id must be a non-empty string")
    return student_id.strip()


def _any_projection(inputs: JourneySubsystemInputs) -> bool:
    return any(bool(getattr(inputs, attr)) for attr, _ in _SOURCE_PRIORITY)


def _stage_from_projection(
    projection: Mapping[str, Any],
) -> JourneyStage | None:
    if not projection:
        return None
    raw = projection.get(_STAGE_KEY)
    if raw is None:
        nested = projection.get("next_action")
        if isinstance(nested, Mapping):
            raw = nested.get("stage") or nested.get(_STAGE_KEY)
    if raw is None:
        return None
    try:
        return resolve_journey_stage(str(raw))
    except ValueError:
        return None
