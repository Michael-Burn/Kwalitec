"""Already-selected learning check for Quick Check presentation.

ILE-001B does not perform adaptive selection. The Quick Check experience
presents a fixed, product-authored learning check provided here as
presentation content only — no Assessment Engine, Twin, or selection logic.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LearningCheckItem:
    """One presentation item in an already-selected learning check.

    Attributes:
        item_id: Stable presentation id (not an engine question id).
        stem: Learner-facing prompt.
        response_kind: ``free_text`` or ``choice``.
        choices: Optional choice labels when ``response_kind`` is ``choice``.
        hint: Optional calm hint text.
    """

    item_id: str
    stem: str
    response_kind: str = "free_text"
    choices: tuple[str, ...] = ()
    hint: str = ""


@dataclass(frozen=True)
class SelectedLearningCheck:
    """Immutable already-selected learning check (presentation payload).

    Attributes:
        check_id: Stable identifier for this presentation pack.
        focus_label: Optional syllabus / topic focus label (display only).
        items: Ordered presentation items.
    """

    check_id: str
    focus_label: str
    items: tuple[LearningCheckItem, ...]


# Canonical already-selected Quick Check used by ILE-001B.
# Not adaptive. Not Assessment Engine output. Presentation only.
QUICK_CHECK_SELECTED: SelectedLearningCheck = SelectedLearningCheck(
    check_id="qc-mission-daily-v1",
    focus_label="Today's Mission ideas",
    items=(
        LearningCheckItem(
            item_id="qc-item-1",
            stem=(
                "In your own words, what is the main idea you are working "
                "on in today's Mission?"
            ),
            hint=(
                "A short sentence is enough — this helps us understand "
                "what feels clear."
            ),
        ),
        LearningCheckItem(
            item_id="qc-item-2",
            stem=(
                "Which part of today's work still feels a little unclear?"
            ),
            response_kind="choice",
            choices=(
                "The core idea",
                "How to apply it",
                "How it connects to earlier work",
                "Nothing specific — I just want to confirm",
            ),
            hint="Choose the closest option; honesty is more useful than polish.",
        ),
        LearningCheckItem(
            item_id="qc-item-3",
            stem=(
                "What would you like to practise next so today's Mission "
                "stays useful?"
            ),
            hint=(
                "Think of one small next step — a concept to revisit or "
                "a short practice focus."
            ),
        ),
    ),
)


def get_already_selected_quick_check() -> SelectedLearningCheck:
    """Return the already-selected Quick Check presentation pack."""
    return QUICK_CHECK_SELECTED
