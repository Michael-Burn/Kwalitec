"""Constants for canonical coverage reconciliation (shadow-safe)."""

from __future__ import annotations

# Evidence sources that may establish coverage under the coverage contract.
EVIDENCE_LEGACY_COMPLETION = "LEGACY_COMPLETION"
EVIDENCE_VERIFIED_COMPLETION = "VERIFIED_COMPLETION"

EVIDENCE_SOURCES = frozenset(
    {
        EVIDENCE_LEGACY_COMPLETION,
        EVIDENCE_VERIFIED_COMPLETION,
    }
)

# Shadow eligibility categories (interpretive only; not live display authority).
CATEGORY_CONFIRMED_COVERED = "CONFIRMED_COVERED"
CATEGORY_HISTORICALLY_COMPLETED = "HISTORICALLY_COMPLETED"
CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY = "AMBIGUOUS_HISTORICAL_ACTIVITY"
CATEGORY_NOT_COVERED = "NOT_COVERED"

ELIGIBILITY_CATEGORIES = frozenset(
    {
        CATEGORY_CONFIRMED_COVERED,
        CATEGORY_HISTORICALLY_COMPLETED,
        CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY,
        CATEGORY_NOT_COVERED,
    }
)

# Mapping statuses that may contribute a defensible canonical link.
ACCEPTABLE_MAPPING_STATUSES = frozenset({"exact", "defensible_but_changed"})
