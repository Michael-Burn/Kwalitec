"""Daily Mission Intelligence application DTOs (ILE-004)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DailyMissionIntelligenceSnapshot:
    """Student-safe projection of today's primary educational mission."""

    title: str = "Today's Mission"
    educational_purpose: str = ""
    why_today: str = ""
    why_not_something_else: str = ""
    supporting_evidence: tuple[str, ...] = ()
    estimated_effort: str = ""
    expected_learning_outcome: str = ""
    what_happens_after_completion: str = ""
    reflection_prompt: str = ""
    mission_confidence: str = ""
    uncertainty: str = ""
    mission_explanation: str = ""
    skip_consequence: str = ""
    optimisation_axis_label: str = ""
    lifecycle_phase: str = ""
    qualitative_confidence: str = ""
    recommendation_key: str = ""
    mission_id: str = ""
    session_id: str = ""
    has_mission: bool = False
    empty: bool = True
    journal_entry_id: str = ""
    # Study Sensei chrome
    eyebrow: str = "Today's Mission"
    focus_question: str = "What should I focus on today?"
    explainability_heading: str = "Why this Mission"
    evidence_heading: str = "Supporting evidence"
    after_heading: str = "After you finish"
    reflection_heading: str = "Reflection"
    skip_heading: str = "If you skip today"
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
