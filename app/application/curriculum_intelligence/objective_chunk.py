"""Size learning-objective batches to a student's session length.

Runtime C publishes one syllabus topic with many LOs. Study Sessions must
fit the student's preferred session minutes — not dump an entire chapter
into one sitting.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

# When LO estimates are missing, assume a focused block that still leaves
# room for Read → Worked example → Practice within the sitting.
_DEFAULT_LO_MINUTES = 20
# Keep a single sitting teachable even when LO estimates are tiny.
_HARD_CAP = 3
# Syllabus LO minutes are often multi-hour chapter estimates; clamp to the
# sitting budget so one LO can occupy a full session when needed.
_MIN_LO_MINUTES = 15


def select_objectives_for_session(
    ordered_objective_ids: Sequence[str],
    *,
    session_minutes: int | None,
    objective_minutes: Mapping[str, int] | None = None,
) -> tuple[str, ...]:
    """Return a prefix of uncovered LOs that fit one Study Session.

    Always returns at least one objective when any are available. Prefer
    fewer, deeper LOs over packing an entire topic into sixty minutes.
    """
    ids = [str(oid).strip() for oid in ordered_objective_ids if str(oid).strip()]
    if not ids:
        return ()

    budget = (
        int(session_minutes)
        if session_minutes and int(session_minutes) > 0
        else 60
    )
    hard_cap = max(1, min(_HARD_CAP, max(1, budget // _DEFAULT_LO_MINUTES)))
    minutes_map = objective_minutes or {}

    selected: list[str] = []
    used = 0
    for oid in ids:
        raw = 0
        if oid in minutes_map:
            try:
                raw = int(minutes_map[oid] or 0)
            except (TypeError, ValueError):
                raw = 0
        if raw <= 0:
            cost = _DEFAULT_LO_MINUTES
        elif raw > budget:
            # Chapter-scale estimate → this LO alone fills the sitting.
            cost = budget
        else:
            cost = max(_MIN_LO_MINUTES, raw)

        if selected and (used + cost > budget or len(selected) >= hard_cap):
            break
        selected.append(oid)
        used += cost
        if len(selected) >= hard_cap:
            break

    return tuple(selected or ids[:1])
