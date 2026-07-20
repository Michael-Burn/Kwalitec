"""Immutable reflection DTO for Learning Session Experience."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ReflectionSnapshot:
    """Reflection checkpoint projection DTO."""

    session_id: str
    key_insight: str = ""
    concept_confidence: str = ""
    suggested_improvement: str = ""
    reflection_prompt: str = ""
    topic_title: str = ""
    next_action_label: str = "Continue to Summary"
    has_insight: bool = False
    is_complete: bool = False
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
