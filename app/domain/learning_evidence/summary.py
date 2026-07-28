"""Deterministic evidence count summaries (EI-005).

Read-side aggregation of observation counts only — no mastery or confidence.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EvidenceCountSummary:
    """Count of evidence events, optionally broken down by type."""

    total: int
    by_type: tuple[tuple[str, int], ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "by_type": {evidence_type: count for evidence_type, count in self.by_type},
        }


def count_by_type(evidence_types: Iterable[str]) -> EvidenceCountSummary:
    """Summarise evidence counts keyed by type (deterministic key order)."""
    counter = Counter(evidence_types)
    by_type = tuple(sorted(counter.items(), key=lambda item: item[0]))
    return EvidenceCountSummary(total=sum(counter.values()), by_type=by_type)
