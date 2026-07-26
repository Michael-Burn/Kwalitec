"""Map authored readiness MES onto Student Experience Home snapshots.

EP-006.4 presentation delivery only — never recalculates readiness scores or
invents drivers. Prefer Runtime A ReadinessService surface + presentation
adapter pass-through; fail open when the surface is unavailable.
"""

from __future__ import annotations

import logging
from typing import Any

from app.application.student_experience.dto.readiness_explanation_snapshot import (
    ReadinessExplanationSnapshot,
)

logger = logging.getLogger(__name__)


def readiness_explanation_from_narrative(
    narrative: Any,
    *,
    schema_complete: bool = False,
) -> ReadinessExplanationSnapshot:
    """Project a ReadinessNarrative onto the Home readiness explanation DTO."""
    drivers = tuple(
        str(d).strip()
        for d in (narrative.readiness_drivers or ())
        if str(d).strip()
    )
    evidence = tuple(
        str(item).strip()
        for item in (getattr(narrative, "supporting_evidence", ()) or ())
        if str(item).strip()
    )
    why = str(
        getattr(narrative, "why_this_estimate", "")
        or getattr(narrative, "explanation", "")
        or ""
    ).strip()
    confidence = str(getattr(narrative, "confidence_label", "") or "").strip()
    basis = str(getattr(narrative, "confidence_basis", "") or "").strip()
    if not basis and confidence:
        # Lexical confidence is the student-safe basis when no separate field.
        basis = confidence
    next_action = str(getattr(narrative, "suggested_next_action", "") or "").strip()
    review = str(getattr(narrative, "review_point", "") or "").strip()
    complete = bool(
        schema_complete
        or (
            why
            and confidence
            and next_action
            and drivers
        )
    )
    return ReadinessExplanationSnapshot(
        why_this_estimate=why,
        confidence_label=confidence,
        confidence_basis=basis,
        suggested_next_action=next_action,
        review_point=review,
        readiness_drivers=drivers[:4],
        supporting_evidence=evidence[:5],
        expected_benefit=str(getattr(narrative, "expected_benefit", "") or "").strip(),
        can_estimate=bool(getattr(narrative, "can_estimate", True)),
        is_complete=complete,
    )


def load_home_readiness_explanation(
    student_id: str,
) -> ReadinessExplanationSnapshot | None:
    """Load authored readiness MES for Home; fail-open to None.

    Uses the same ReadinessService dashboard surface as Analytics so Home and
    Analytics share Runtime A readiness speech without a second narrator.
    """
    user_id = _as_user_id(student_id)
    if user_id is None:
        return None
    try:
        from app.presentation.intelligence_surface.adapter import (
            RuntimeAPresentationAdapter,
        )
        from app.services.readiness_quality import (
            has_complete_readiness_explanation_schema,
        )
        from app.services.readiness_service import ReadinessService

        surface = ReadinessService.get_dashboard_readiness_surface(user_id)
        if not isinstance(surface, dict) or not surface:
            return None
        narrative = RuntimeAPresentationAdapter.readiness_narrative(surface)
        return readiness_explanation_from_narrative(
            narrative,
            schema_complete=has_complete_readiness_explanation_schema(surface),
        )
    except Exception:
        logger.debug(
            "home readiness explanation unavailable for student_id=%s",
            student_id,
            exc_info=True,
        )
        return None


def _as_user_id(student_id: str) -> int | None:
    try:
        return int(str(student_id).strip())
    except (TypeError, ValueError):
        return None
