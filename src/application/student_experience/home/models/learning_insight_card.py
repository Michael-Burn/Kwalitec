"""LearningInsightCard — deterministic student-facing insights."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.home.enums import InsightKind
from application.student_experience.home.errors import HomeInvariantViolation


@dataclass(frozen=True, slots=True)
class LearningInsight:
    """One deterministic learning insight — never AI-generated."""

    kind: InsightKind
    title: str
    message: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, InsightKind):
            raise HomeInvariantViolation(
                "kind must be an InsightKind",
                invariant="LearningInsight.kind.type",
            )
        title = (self.title or "").strip()
        if not title:
            raise HomeInvariantViolation(
                "title must be a non-empty string",
                invariant="LearningInsight.title.required",
            )
        object.__setattr__(self, "title", title)
        message = (self.message or "").strip()
        if not message:
            raise HomeInvariantViolation(
                "message must be a non-empty string",
                invariant="LearningInsight.message.required",
            )
        object.__setattr__(self, "message", message)


@dataclass(frozen=True, slots=True)
class LearningInsightCard:
    """Immutable card surfacing deterministic learning insights."""

    insights: tuple[LearningInsight, ...] = ()
    headline: str = "Learning insights"
    has_insights: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "insights", tuple(self.insights))
        for insight in self.insights:
            if not isinstance(insight, LearningInsight):
                raise HomeInvariantViolation(
                    "insights must contain LearningInsight values",
                    invariant="LearningInsightCard.insights.type",
                )
        headline = (self.headline or "").strip()
        if not headline:
            raise HomeInvariantViolation(
                "headline must be a non-empty string",
                invariant="LearningInsightCard.headline.required",
            )
        object.__setattr__(self, "headline", headline)
        object.__setattr__(self, "has_insights", bool(self.insights))
