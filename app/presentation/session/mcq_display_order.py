"""Shuffle MCQ choice display order at presentation time.

Stored package content is never reordered: choice ids, labels, misconception
tags, hints, explanations, and ``correct_choice_id`` stay as authored.
Radio values remain stored choice ids, so scoring, choice-aware feedback,
and Progression Readiness keep resolving by id rather than by the row the
student happened to see.
"""

from __future__ import annotations

import random
from collections.abc import Sequence


def shuffle_mcq_display_order(
    choices: Sequence[tuple[str, str]],
    *,
    rng: random.Random | None = None,
) -> tuple[tuple[str, str], ...]:
    """Return a shuffled copy of ``(id, label)`` pairs.

    Pairing of id to label is preserved. Empty or single-choice lists are
    returned unchanged. A fresh shuffle is produced on every call unless a
    seeded ``rng`` is supplied (tests).
    """
    items = [(cid, label) for cid, label in choices]
    if len(items) < 2:
        return tuple(items)
    shuffler = rng if rng is not None else random.SystemRandom()
    shuffler.shuffle(items)
    return tuple(items)
