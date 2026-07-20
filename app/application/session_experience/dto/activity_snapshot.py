"""Immutable activity DTO for Learning Session Experience."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ActivitySnapshot:
    """Learning activity projection DTO."""

    activity_id: str
    session_id: str
    question: str = ""
    context: str = ""
    supporting_material: str = ""
    hints: tuple[str, ...] = ()
    answer_prompt: str = "Your answer"
    explanation: str = ""
    phase: str = "ready"
    activity_index: int = 1
    activities_total: int = 1
    next_action_label: str = "Continue"
    topic_title: str = ""
    has_hints: bool = False
    has_explanation: bool = False
    is_final_activity: bool = False
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
