"""Same-day sitting precedence: overdue > due > adaptive > sequential.

Owns the V1 arbitration rule between Spacing Scheduler lifecycle states and
Adaptive Decision candidates. The Spacing Scheduler never imports this module.
Policy V1 weakness scoring never encodes this precedence; it delegates here.

V1 policy (locked): overdue and due spaced reviews are always protected.
Adaptive may win only when no protected spaced review exists. No adaptive
preemption of protected review. No session-split mixing.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.application.educational_runtime_engine.selection_reasons import (
    SELECTION_REASON_ADAPTIVE_REVIEW,
    SELECTION_REASON_SEQUENTIAL,
    SELECTION_REASON_SPACED_REVIEW,
)
from app.domain.spacing_scheduler.types import SchedulingStatus


class ArbitrationLabel(StrEnum):
    """Internal-only observability labels for arbitration outcomes.

    Never surface these strings as student-facing speech. Student copy stays
    a plain-language account of what today's session is and why.
    """

    SPACED_DUE = "spaced_due"
    SPACED_OVERDUE = "spaced_overdue"
    ADAPTIVE_CANDIDATE = "adaptive_candidate"
    ADAPTIVE_PREEMPTED_DUE = "adaptive_preempted_due"
    ADAPTIVE_PREEMPTED_OVERDUE = "adaptive_preempted_overdue"
    DUE_PROTECTED = "due_protected"
    OVERDUE_PROTECTED = "overdue_protected"
    ADAPTIVE_DEFERRED = "adaptive_deferred"
    SEQUENTIAL_FALLBACK = "sequential_fallback"


class PrecedenceWinner(StrEnum):
    """Who won same-day sitting precedence under V1."""

    OVERDUE = "overdue"
    DUE = "due"
    ADAPTIVE = "adaptive"
    SEQUENTIAL = "sequential"


REASON_ARBITRATION_OVERDUE_PROTECTED = "arbitration_overdue_protected"
REASON_ARBITRATION_DUE_PROTECTED = "arbitration_due_protected"
REASON_ARBITRATION_ADAPTIVE_SELECTED = "arbitration_adaptive_selected"
REASON_ARBITRATION_SEQUENTIAL = "arbitration_sequential"


@dataclass(frozen=True, slots=True)
class ArbitrationResult:
    """Pure arbitration outcome for one daily sitting decision."""

    winner: PrecedenceWinner
    labels: tuple[ArbitrationLabel, ...]
    reason_code: str
    protected_status: SchedulingStatus | None
    composer_selection_reason: str


def protected_status_from_value(
    raw: object | None,
) -> SchedulingStatus | None:
    """Parse a spacing lifecycle status from composer/trace input."""
    if raw is None:
        return None
    if isinstance(raw, SchedulingStatus):
        if raw in {SchedulingStatus.DUE, SchedulingStatus.OVERDUE}:
            return raw
        return None
    text = str(raw or "").strip().lower()
    if text == SchedulingStatus.OVERDUE.value:
        return SchedulingStatus.OVERDUE
    if text == SchedulingStatus.DUE.value:
        return SchedulingStatus.DUE
    return None


def arbitrate_sitting_precedence(
    *,
    protected_status: SchedulingStatus | None,
    has_adaptive_candidate: bool,
) -> ArbitrationResult:
    """Apply locked V1 precedence: overdue > due > adaptive > sequential.

    ``protected_status`` is a Spacing Scheduler calendar lifecycle state only
    (DUE or OVERDUE). This function does not evaluate intervals or consult Twin.
    """
    if protected_status is SchedulingStatus.OVERDUE:
        labels: list[ArbitrationLabel] = [
            ArbitrationLabel.OVERDUE_PROTECTED,
            ArbitrationLabel.SPACED_OVERDUE,
        ]
        if has_adaptive_candidate:
            labels.extend(
                [
                    ArbitrationLabel.ADAPTIVE_PREEMPTED_OVERDUE,
                    ArbitrationLabel.ADAPTIVE_DEFERRED,
                ]
            )
        return ArbitrationResult(
            winner=PrecedenceWinner.OVERDUE,
            labels=tuple(labels),
            reason_code=REASON_ARBITRATION_OVERDUE_PROTECTED,
            protected_status=SchedulingStatus.OVERDUE,
            composer_selection_reason=SELECTION_REASON_SPACED_REVIEW,
        )

    if protected_status is SchedulingStatus.DUE:
        labels = [
            ArbitrationLabel.DUE_PROTECTED,
            ArbitrationLabel.SPACED_DUE,
        ]
        if has_adaptive_candidate:
            labels.extend(
                [
                    ArbitrationLabel.ADAPTIVE_PREEMPTED_DUE,
                    ArbitrationLabel.ADAPTIVE_DEFERRED,
                ]
            )
        return ArbitrationResult(
            winner=PrecedenceWinner.DUE,
            labels=tuple(labels),
            reason_code=REASON_ARBITRATION_DUE_PROTECTED,
            protected_status=SchedulingStatus.DUE,
            composer_selection_reason=SELECTION_REASON_SPACED_REVIEW,
        )

    if has_adaptive_candidate:
        return ArbitrationResult(
            winner=PrecedenceWinner.ADAPTIVE,
            labels=(ArbitrationLabel.ADAPTIVE_CANDIDATE,),
            reason_code=REASON_ARBITRATION_ADAPTIVE_SELECTED,
            protected_status=None,
            composer_selection_reason=SELECTION_REASON_ADAPTIVE_REVIEW,
        )

    return ArbitrationResult(
        winner=PrecedenceWinner.SEQUENTIAL,
        labels=(ArbitrationLabel.SEQUENTIAL_FALLBACK,),
        reason_code=REASON_ARBITRATION_SEQUENTIAL,
        protected_status=None,
        composer_selection_reason=SELECTION_REASON_SEQUENTIAL,
    )
