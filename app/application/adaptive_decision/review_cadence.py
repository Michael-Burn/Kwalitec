"""Standalone review-day cadence for Policy V1 (ADR-027 Phase 3).

Reimplements Runtime A's discrete 4 / 3 / 2 new-topic bands as continuous
piecewise-linear interpolation so Policy V1 does not import PlanningService
(M0 / Phase 2 boundary: Decision Engine must not couple to Runtime A modules).

Runtime A reference (not imported):
``PlanningService._consolidation_cadence`` — days > 60 → 4; 30–60 → 3; <30 → 2.
"""

from __future__ import annotations


def continuous_review_cadence(days_remaining: int) -> float:
    """New topics between review days as a smooth function of days-to-exam.

    Anchors match Runtime A's discrete bands exactly at the band edges:

    * ``days_remaining >= 60`` → ``4.0``
    * ``days_remaining == 30`` → ``3.0``
    * ``days_remaining == 0`` → ``2.0``

    Between anchors, cadence is piecewise linear:

    * ``[30, 60)``: interpolate ``3 → 4`` as days go ``30 → 60``
    * ``[0, 30)``: interpolate ``2 → 3`` as days go ``0 → 30``

    That continuous ramp is how exam proximity tightens without step jumps at
    60 and 30. Through the six-week window (~42 days) cadence is already below
    4 and falling; through the final two to three weeks (~14–21 days) it sits
    on the near-exam segment approaching 2 (strongly review-weighted).

    Negative ``days_remaining`` (exam passed) clamps to the near-exam floor.
    """
    d = int(days_remaining)
    if d >= 60:
        return 4.0
    if d >= 30:
        # Linear: 4 at 60, 3 at 30.
        return 3.0 + (d - 30) * (1.0 / 30.0)
    if d <= 0:
        return 2.0
    # Linear: 3 at 30, 2 at 0.
    return 2.0 + d * (1.0 / 30.0)


def is_review_day(
    *,
    days_remaining: int | None,
    topics_since_last_review: int,
) -> bool:
    """True when new-topic watermark meets the continuous cadence threshold.

    Missing exam date (``days_remaining is None``) means proximity cannot be
    applied; treat as not a review day so Policy V0 remains the authority.
    """
    if days_remaining is None:
        return False
    watermark = max(0, int(topics_since_last_review))
    cadence = continuous_review_cadence(days_remaining)
    return watermark >= cadence
