"""ReflectionAssembler — SessionOutcome → ReflectionExperience (P2-MS005).

Prepares concise wording, determines the next journey transition, and
exposes available prompts. No educational interpretation.
"""

from __future__ import annotations

from app.application.unified_journey.reflection_experience import (
    ReflectionExperience,
    empty_reflection_experience,
)
from app.application.unified_journey.reflection_prompt import (
    default_reflection_prompts,
)
from app.application.unified_journey.reflection_states import (
    ReflectionState,
    resolve_reflection_state,
)
from app.application.unified_journey.session_outcome import (
    SessionOutcome,
    empty_session_outcome,
)


class ReflectionAssembler:
    """Transform SessionOutcome into a presentation-ready reflection experience.

    Responsibilities:
    - Prepare concise student-facing wording
    - Determine the next journey transition
    - Expose available reflection prompts

    Non-responsibilities:
    - Educational interpretation
    - Persistence / evidence writes
    - AI-generated feedback
    """

    def assemble(
        self,
        outcome: SessionOutcome | None,
        *,
        state: ReflectionState | str | None = None,
    ) -> ReflectionExperience:
        """Derive an immutable ReflectionExperience from SessionOutcome."""
        if outcome is None or not outcome.reflection_available:
            return empty_reflection_experience()

        resolved = resolve_reflection_state(state)
        if resolved is None:
            resolved = ReflectionState.AVAILABLE

        title = (outcome.mission_title or "").strip() or "today's session"
        supporting = (outcome.summary_message or "").strip() or (
            f"A short reflection on {title}"
        )
        # Prefer state-aware wording once reflection has moved past Available.
        if resolved is ReflectionState.AVAILABLE and outcome.next_transition:
            next_transition = outcome.next_transition.strip()
        else:
            next_transition = _default_next_transition(resolved)

        return ReflectionExperience(
            session_outcome=outcome,
            prompts=default_reflection_prompts(),
            reflection_state=resolved,
            headline="Brief reflection",
            supporting_message=supporting,
            next_transition=next_transition,
            skip_available=resolved
            in {ReflectionState.AVAILABLE, ReflectionState.IN_PROGRESS},
            metadata=outcome.metadata
            + (
                ("reflection_state", resolved.value),
                ("via", "reflection_assembler"),
            ),
        )

    def assemble_placeholder(self) -> ReflectionExperience:
        """Assemble from an explicit placeholder SessionOutcome."""
        return self.assemble(empty_session_outcome())


def _default_next_transition(state: ReflectionState) -> str:
    if state is ReflectionState.AVAILABLE:
        return "Take a brief moment to reflect"
    if state is ReflectionState.IN_PROGRESS:
        return "Finish or skip when ready"
    if state is ReflectionState.COMPLETED:
        return "Today's learning day is complete"
    return "Today's learning day is complete"
