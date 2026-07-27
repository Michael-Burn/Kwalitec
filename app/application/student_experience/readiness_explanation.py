"""Map authored readiness MES onto Student Experience Home snapshots.

EP-006.4 presentation delivery only — never recalculates readiness scores or
invents drivers. Prefer Runtime A ReadinessService surface + presentation
adapter pass-through; fail open when the surface is unavailable.
"""

from __future__ import annotations

import logging
from typing import Any, Protocol, runtime_checkable

from app.application.student_experience.dto.readiness_explanation_snapshot import (
    ReadinessExplanationSnapshot,
)

logger = logging.getLogger(__name__)


@runtime_checkable
class ReadinessSurfacePort(Protocol):
    """Structural contract for the Runtime A readiness explanation surface.

    Implementations own fetching + narrative mapping (services/presentation);
    this layer only decides Home-projection fallback / logging.
    """

    def load_readiness_explanation(
        self, user_id: int
    ) -> ReadinessExplanationSnapshot | None:
        """Return the readiness explanation for ``user_id``, or None."""


# Process-local port (bound by presentation composition / tests).
_readiness_surface_port: ReadinessSurfacePort | None = None


def bind_readiness_surface_port(port: ReadinessSurfacePort | None) -> None:
    """Bind the process-local ReadinessSurfacePort."""
    global _readiness_surface_port
    _readiness_surface_port = port


def get_readiness_surface_port() -> ReadinessSurfacePort | None:
    """Return the bound ReadinessSurfacePort, or None when unbound."""
    return _readiness_surface_port


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
    *,
    port: ReadinessSurfacePort | None = None,
) -> ReadinessExplanationSnapshot | None:
    """Load authored readiness MES for Home; fail-open to None.

    Delegates to the same ReadinessService dashboard surface as Analytics
    (via the injected/bound ``ReadinessSurfacePort``) so Home and Analytics
    share Runtime A readiness speech without a second narrator.
    """
    user_id = _as_user_id(student_id)
    if user_id is None:
        return None
    active_port = port or get_readiness_surface_port()
    if active_port is None:
        return None
    try:
        return active_port.load_readiness_explanation(user_id)
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
