"""Decision Journal application DTOs (ILE-002)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EvidenceUpdateSnapshot:
    """One append-only evidence evolution line."""

    summary: str
    recorded_at_label: str


@dataclass(frozen=True)
class DecisionJournalEntrySnapshot:
    """Student-safe projection of one journal entry."""

    decision_id: str
    timestamp_label: str
    kind: str
    kind_label: str
    lifecycle_status: str
    lifecycle_label: str
    educational_context: str
    observation: str
    meaning: str
    recommendation: str
    supporting_evidence_summary: str
    confidence_label: str
    expected_benefit: str
    uncertainty: str
    student_action_label: str
    outcome_summary: str
    reflection_label: str
    reflection_note: str
    what_happened: str
    why: str
    what_i_chose: str
    what_happened_afterwards: str
    what_to_learn: str
    evidence_updates: tuple[EvidenceUpdateSnapshot, ...] = ()
    is_archived: bool = False
    # ILE-005 — optional reflection invite (never required).
    reflection_pending: bool = False
    can_reflect: bool = False


@dataclass(frozen=True)
class DecisionJournalTimelineSnapshot:
    """Chronology page projection for the Decision Journal."""

    entries: tuple[DecisionJournalEntrySnapshot, ...] = ()
    entry_count: int = 0
    empty: bool = True
    page_title: str = "Decision Journal"
    page_eyebrow: str = "Study Sensei"
    page_description: str = (
        "Study Sensei’s durable educational memory — significant guidance, "
        "the choices you made, and what was learned afterwards."
    )
    empty_title: str = "Your journal starts with the next guidance"
    empty_description: str = (
        "Respond to Mission guidance and it will appear here as durable "
        "educational memory. The Educational Timeline reads these entries "
        "later; History keeps practice archives separately. Open Home to "
        "continue studying."
    )
    primary_cta_label: str = "Back to Home"
    intro_line: str = (
        "Study Sensei’s durable educational memory of significant guidance "
        "and your choices."
    )


@dataclass
class DecisionJournalRecordRequest:
    """Application input for recording a journal entry."""

    user_id: int
    kind: str
    educational_context: str
    observation: str
    meaning: str
    recommendation: str
    supporting_evidence_summary: str = ""
    qualitative_confidence: str = "emerging"
    expected_benefit: str = ""
    uncertainty: str = ""
    catalogue_decision_id: str = ""
    student_action: str = "none_yet"
    legacy_decision_id: int | None = None
    commitment_id: int | None = None
    extra: dict = field(default_factory=dict)
