"""ExplanationCards — deterministic explanation cards for coaching."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.coach.enums import ExplanationCardKind
from application.student_experience.coach.errors import CoachInvariantViolation


@dataclass(frozen=True, slots=True)
class ExplanationCard:
    """One deterministic explanation card — narrates existing decisions only."""

    kind: ExplanationCardKind
    title: str
    body: str
    available: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.kind, ExplanationCardKind):
            raise CoachInvariantViolation(
                "kind must be an ExplanationCardKind",
                invariant="ExplanationCard.kind.type",
            )
        for name in ("title", "body"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise CoachInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ExplanationCard.{name}.required",
                )
            object.__setattr__(self, name, value)


@dataclass(frozen=True, slots=True)
class ExplanationCards:
    """Immutable collection of explanation cards."""

    cards: tuple[ExplanationCard, ...] = ()

    def __post_init__(self) -> None:
        cards = tuple(self.cards or ())
        for card in cards:
            if not isinstance(card, ExplanationCard):
                raise CoachInvariantViolation(
                    "cards must contain ExplanationCard instances",
                    invariant="ExplanationCards.cards.type",
                )
        object.__setattr__(self, "cards", cards)

    @property
    def available(self) -> bool:
        return any(card.available for card in self.cards)

    def by_kind(self, kind: ExplanationCardKind) -> ExplanationCard | None:
        for card in self.cards:
            if card.kind is kind:
                return card
        return None
