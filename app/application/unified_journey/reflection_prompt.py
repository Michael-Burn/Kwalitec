"""Immutable ReflectionPrompt DTO (P2-MS005).

Presentation-only reflection prompts. Responses are never persisted.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from app.application.unified_journey.contracts import CONTRACT_VERSION

RESPONSE_TYPE_CHOICE = "choice"
RESPONSE_TYPE_NOTE = "note"
RESPONSE_TYPE_VALUES = frozenset(
    {
        RESPONSE_TYPE_CHOICE,
        RESPONSE_TYPE_NOTE,
        "",
    }
)


class ReflectionResponseType(StrEnum):
    """Presentation response kinds for Guided Reflection."""

    CHOICE = RESPONSE_TYPE_CHOICE
    NOTE = RESPONSE_TYPE_NOTE


@dataclass(frozen=True)
class ReflectionPrompt:
    """One student-facing reflection prompt (presentation only).

    Does not persist responses. Does not interpret educational meaning.
    """

    prompt: str = ""
    response_type: str = RESPONSE_TYPE_CHOICE
    available_options: tuple[str, ...] = ()
    optional_note_placeholder: str = ""
    contract_version: str = CONTRACT_VERSION
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "prompt", (self.prompt or "").strip())
        response = (self.response_type or "").strip().lower()
        if response not in RESPONSE_TYPE_VALUES:
            raise ValueError(
                f"unknown reflection response_type: {self.response_type!r}"
            )
        object.__setattr__(self, "response_type", response)
        options = tuple(
            str(item).strip()
            for item in (self.available_options or ())
            if str(item).strip()
        )
        object.__setattr__(self, "available_options", options)
        object.__setattr__(
            self,
            "optional_note_placeholder",
            (self.optional_note_placeholder or "").strip(),
        )


def default_reflection_prompts() -> tuple[ReflectionPrompt, ...]:
    """Lightweight presentation prompts for Guided Reflection.

    Fixed copy — no AI generation, no educational interpretation.
    """
    return (
        ReflectionPrompt(
            prompt="How did today's session feel?",
            response_type=RESPONSE_TYPE_CHOICE,
            available_options=("Good", "Okay", "Challenging"),
            metadata=(("key", "session_feel"),),
        ),
        ReflectionPrompt(
            prompt="Was today's mission manageable?",
            response_type=RESPONSE_TYPE_CHOICE,
            available_options=("Yes", "Somewhat", "No"),
            metadata=(("key", "mission_manageable"),),
        ),
        ReflectionPrompt(
            prompt="Would you like to add a note?",
            response_type=RESPONSE_TYPE_NOTE,
            available_options=(),
            optional_note_placeholder="Optional. A short note for yourself",
            metadata=(("key", "optional_note"),),
        ),
    )
