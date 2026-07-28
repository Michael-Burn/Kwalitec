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
        "A calm reading of how your learning has evolved — "
        "drawn from your Decision Journal, not from scores."
    )
    empty_title: str = "Your timeline begins with journal entries"
    empty_description: str = (
        "As the Study Sensei records significant guidance in your "
        "Decision Journal, patterns of growth, recovery, and "
        "consistency will appear here as a learning story."
    )
    primary_cta_label: str = "Open Decision Journal"
    intro_line: str = (
        "This timeline interprets educational memories. "
        "It never rewrites your journal, and it never invents certainty "
        "beyond the evidence recorded there."
    )
    journal_link_label: str = "View Decision Journal entries"
    section_nav_label: str = "Timeline sections"
