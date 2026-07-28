"""Decision Journal application service (ILE-002).

Orchestrates educational memory for presentation. No HTTP; no Twin;
no recommendation ranking.
"""

from __future__ import annotations

from datetime import datetime

from app.application.decision_journal.dto import (
    DecisionJournalEntrySnapshot,
    DecisionJournalTimelineSnapshot,
    EvidenceUpdateSnapshot,
)
from app.domain.decision_journal import JournalLifecycleStatus
from app.services.decision_journal_service import DecisionJournalService


def _format_when(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.strftime("%d %b %Y, %H:%M")


class DecisionJournalApplicationService:
    """Application façade over ``DecisionJournalService``."""

    @staticmethod
    def timeline(
        user_id: int,
        *,
        limit: int = 50,
        include_archived: bool = True,
    ) -> DecisionJournalTimelineSnapshot:
        """Build the student timeline snapshot."""
        rows = DecisionJournalService.get_timeline(
            user_id,
            limit=limit,
            include_archived=include_archived,
        )
        entries = tuple(
            DecisionJournalApplicationService._entry_snapshot(row)
            for row in rows
        )
        return DecisionJournalTimelineSnapshot(
            entries=entries,
            entry_count=len(entries),
            empty=len(entries) == 0,
        )

    @staticmethod
    def entry_detail(
        user_id: int, entry_id: str
    ) -> DecisionJournalEntrySnapshot:
        """Build one entry snapshot for detail views."""
        row = DecisionJournalService.get_entry(user_id, entry_id)
        return DecisionJournalApplicationService._entry_snapshot(row)

    @staticmethod
    def _entry_snapshot(row) -> DecisionJournalEntrySnapshot:
        payload = DecisionJournalService.to_student_dict(row)
        evidence = tuple(
            EvidenceUpdateSnapshot(
                summary=item["summary"],
                recorded_at_label=_format_when(
                    datetime.fromisoformat(item["recorded_at"])
                    if item.get("recorded_at")
                    else None
                ),
            )
            for item in payload.get("evidence_updates") or []
        )
        return DecisionJournalEntrySnapshot(
            decision_id=payload["decision_id"],
            timestamp_label=_format_when(row.recorded_at),
            kind=payload["kind"],
            kind_label=payload["kind_label"],
            lifecycle_status=payload["lifecycle_status"],
            lifecycle_label=payload["lifecycle_label"],
            educational_context=payload["educational_context"],
            observation=payload["observation"],
            meaning=payload["meaning"],
            recommendation=payload["recommendation"],
            supporting_evidence_summary=payload[
                "supporting_evidence_summary"
            ],
            confidence_label=payload["confidence_label"],
            expected_benefit=payload["expected_benefit"],
            uncertainty=payload["uncertainty"],
            student_action_label=payload["student_action_label"],
            outcome_summary=payload["outcome_summary"],
            reflection_label=payload["reflection_label"],
            reflection_note=payload["reflection_note"],
            what_happened=payload["what_happened"],
            why=payload["why"],
            what_i_chose=payload["what_i_chose"],
            what_happened_afterwards=payload["what_happened_afterwards"],
            what_to_learn=payload["what_to_learn"],
            evidence_updates=evidence,
            is_archived=(
                row.lifecycle_status
                == JournalLifecycleStatus.ARCHIVED.value
            ),
        )
