"""Evidence preparation helpers for Twin inference (EI-006).

Corrections are additional events; corrected rows are excluded from scoring
but remain in the immutable store.
"""

from __future__ import annotations

from app.domain.learning_evidence.evidence_event import EvidenceEvent


def filter_usable_evidence(
    events: tuple[EvidenceEvent, ...] | list[EvidenceEvent],
) -> tuple[EvidenceEvent, ...]:
    """Exclude events that have been corrected by a later event.

    Ordering: chronological by ``occurred_at`` then ``evidence_id`` for
    deterministic ties.
    """
    ordered = sorted(
        events,
        key=lambda e: (e.occurred_at, e.evidence_id),
    )
    corrected: set[str] = set()
    for event in ordered:
        if event.corrects_evidence_id:
            corrected.add(event.corrects_evidence_id)
    usable = tuple(e for e in ordered if e.evidence_id not in corrected)
    return usable


def evidence_ids(events: tuple[EvidenceEvent, ...]) -> tuple[str, ...]:
    """Stable sorted unique evidence ids (explainability order = chrono)."""
    return tuple(e.evidence_id for e in events)
