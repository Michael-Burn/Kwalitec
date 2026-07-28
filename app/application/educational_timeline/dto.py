"""Educational Timeline application DTOs (ILE-003)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NarrativeMomentSnapshot:
    """Student-safe projection of one narrative beat."""

    title: str
    when_label: str
    observation: str
    pattern: str
    educational_meaning: str
    reflection_question: str
    certainty_label: str
    evidence_decision_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class TimelineSectionSnapshot:
    """One named timeline section for presentation."""

    kind: str
    label: str
    intro: str
    moments: tuple[NarrativeMomentSnapshot, ...] = ()
    anchor_id: str = ""


@dataclass(frozen=True)
class EducationalTimelineSnapshot:
    """Full Educational Timeline page projection."""

    sections: tuple[TimelineSectionSnapshot, ...] = ()
    entry_count: int = 0
    empty: bool = True
    certainty_label: str = ""
    page_title: str = "Educational Timeline"
    page_eyebrow: str = "Study Sensei"
    page_description: str = (
        "Your chronological educational record — a learning story drawn "
        "from the Decision Journal, not from scores or History stats."
    )
    empty_title: str = "Your timeline begins with journal entries"
    empty_description: str = (
        "As Study Sensei records significant guidance in your Decision "
        "Journal, this Timeline interprets those memories as a "
        "chronological learning story — growth, recovery, and consistency. "
        "It is not a second memory store and not a scoreboard; History "
        "keeps practice archives and stats as context."
    )
    primary_cta_label: str = "Open Decision Journal"
    intro_line: str = (
        "The Educational Timeline is your chronological educational record. "
        "It interprets Decision Journal memories as a learning story — "
        "it never rewrites the Journal, never invents certainty beyond "
        "that evidence, and never replaces History’s practice context "
        "with mentor meaning."
    )
    journal_link_label: str = "View Decision Journal entries"
    section_nav_label: str = "Timeline sections"
