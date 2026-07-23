"""CelebrationMoments — deterministic moments worth celebrating."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.coach.enums import CelebrationKind
from application.student_experience.coach.errors import CoachInvariantViolation


@dataclass(frozen=True, slots=True)
class CelebrationMoment:
    """One deterministic celebration moment projected from existing signals."""

    kind: CelebrationKind
    title: str
    message: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, CelebrationKind):
            raise CoachInvariantViolation(
                "kind must be a CelebrationKind",
                invariant="CelebrationMoment.kind.type",
            )
        for name in ("title", "message"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise CoachInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"CelebrationMoment.{name}.required",
                )
            object.__setattr__(self, name, value)


@dataclass(frozen=True, slots=True)
class CelebrationMoments:
    """Immutable collection of celebration moments."""

    moments: tuple[CelebrationMoment, ...] = ()
    summary: str = "Celebrations will appear as you make progress."

    def __post_init__(self) -> None:
        moments = tuple(self.moments or ())
        for moment in moments:
            if not isinstance(moment, CelebrationMoment):
                raise CoachInvariantViolation(
                    "moments must contain CelebrationMoment instances",
                    invariant="CelebrationMoments.moments.type",
                )
        object.__setattr__(self, "moments", moments)
        summary = (self.summary or "").strip()
        if not summary:
            raise CoachInvariantViolation(
                "summary must be a non-empty string",
                invariant="CelebrationMoments.summary.required",
            )
        object.__setattr__(self, "summary", summary)

    @property
    def available(self) -> bool:
        return bool(self.moments)
