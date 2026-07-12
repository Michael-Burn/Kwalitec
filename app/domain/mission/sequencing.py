"""Pure sequencing helpers for Mission composition.

Preserve Decision-authored batch order. Constraints may omit trailing unfit
work with acknowledgement — never re-rank educational value.
"""

from __future__ import annotations

from app.domain.decision.decision import Decision


def preserve_decision_order(
    decisions: list[Decision] | tuple[Decision, ...],
) -> tuple[Decision, ...]:
    """Return Decision batch in author order (identity-preserving copy).

    Mission Intelligence must not reorder for packing / engagement heuristics.
    """
    return tuple(decisions)


def authorise_prefix(
    ordered: tuple[Decision, ...],
    include_count: int,
) -> tuple[tuple[Decision, ...], tuple[Decision, ...]]:
    """Split ordered Decisions into included prefix and omitted trailing.

    Args:
        ordered: Decision-authored batch order.
        include_count: How many leading Decisions fit under capacity.

    Returns:
        (included, omitted) — omission is load shaping, not re-selection.
    """
    if include_count < 0:
        raise ValueError("include_count must be non-negative")
    include_count = min(include_count, len(ordered))
    return ordered[:include_count], ordered[include_count:]
