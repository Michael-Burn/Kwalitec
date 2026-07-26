"""Immutable ReflectionExperience DTO (P2-MS005).

Presentation-ready Guided Reflection view model. Experience state only —
does not persist responses or interpret educational meaning.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.unified_journey.contracts import CONTRACT_VERSION
from app.application.unified_journey.reflection_prompt import ReflectionPrompt
from app.application.unified_journey.reflection_states import (
    ReflectionState,
    resolve_reflection_state,
)
from app.application.unified_journey.session_outcome import (
    SessionOutcome,
    empty_session_outcome,
)


@dataclass(frozen=True)
class ReflectionExperience:
    """Student-facing Guided Reflection experience (Experience Layer).

    Assembled from ``SessionOutcome``. Optional and lightweight —
    responses are never persisted in this milestone.
    """

    session_outcome: SessionOutcome = field(default_factory=empty_session_outcome)
    prompts: tuple[ReflectionPrompt, ...] = ()
    reflection_state: ReflectionState = ReflectionState.AVAILABLE
    headline: str = "Brief reflection"
    supporting_message: str = ""
    next_transition: str = ""
    skip_available: bool = True
    contract_version: str = CONTRACT_VERSION
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.session_outcome, SessionOutcome):
            raise TypeError("session_outcome must be a SessionOutcome")
        state = resolve_reflection_state(self.reflection_state)
        if state is None:
            state = ReflectionState.AVAILABLE
        object.__setattr__(self, "reflection_state", state)
        object.__setattr__(self, "prompts", tuple(self.prompts or ()))
        object.__setattr__(self, "headline", (self.headline or "").strip())
        object.__setattr__(
            self,
            "supporting_message",
            (self.supporting_message or "").strip(),
        )
        object.__setattr__(
            self, "next_transition", (self.next_transition or "").strip()
        )
        object.__setattr__(self, "skip_available", bool(self.skip_available))

    @property
    def is_available(self) -> bool:
        return self.reflection_state is ReflectionState.AVAILABLE

    @property
    def is_in_progress(self) -> bool:
        return self.reflection_state is ReflectionState.IN_PROGRESS

    @property
    def is_completed(self) -> bool:
        return self.reflection_state is ReflectionState.COMPLETED

    @property
    def is_skipped(self) -> bool:
        return self.reflection_state is ReflectionState.SKIPPED

    @property
    def is_active(self) -> bool:
        return self.reflection_state in {
            ReflectionState.AVAILABLE,
            ReflectionState.IN_PROGRESS,
        }


def empty_reflection_experience() -> ReflectionExperience:
    """Placeholder ReflectionExperience when SessionOutcome is unavailable."""
    return ReflectionExperience(
        session_outcome=empty_session_outcome(),
        prompts=(),
        reflection_state=ReflectionState.AVAILABLE,
        headline="Brief reflection",
        supporting_message="",
        next_transition="",
        skip_available=True,
        metadata=(("availability", "placeholder"),),
    )
