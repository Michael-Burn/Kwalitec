"""CompleteLearningEpisode command."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CompleteLearningEpisode:
    """Complete an in-progress learning episode.

    Reflection and outcome values are supplied by callers; application does not
    invent educational judgements. Domain aggregate enforces completion rules.
    """

    episode_id: str
    reflection_id: str
    reflection_type: str
    reflection_content: str
    outcome_id: str
    outcome_kind: str
    outcome_summary: str
    perceived_difficulty: str | None = None
    perceived_understanding: str | None = None
