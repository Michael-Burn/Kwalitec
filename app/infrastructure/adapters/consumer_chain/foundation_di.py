"""Shared Foundation DI for EP-001 consumer-chain composition (EP-002.2).

Provides a single Twin-ON Foundation resolve helper and composition-local
Canonical Learner State assembly that can be injected through Planner →
Readiness → Insight without process-global caches or mutable shared state.

Rules:
- No process-global Foundation singleton
- No cross-request CLS cache
- Assembled ``CanonicalLearnerState`` is frozen/immutable — safe to share
  by reference within one composition call tree
- Observational telemetry only; never influences student payloads
"""

from __future__ import annotations

import logging
from typing import Any

from app.infrastructure.adapters.consumer_chain.telemetry import (
    get_consumer_chain_telemetry,
)

logger = logging.getLogger(__name__)

ASSEMBLE_SOURCE_INJECTED = "injected"
ASSEMBLE_SOURCE_ASSEMBLED = "assembled"


def resolve_enabled_twin_foundation(
    *,
    environ: dict[str, str] | None = None,
) -> object | None:
    """Resolve EP-001.1 Foundation when Digital Twin flag is ON.

    Shared replacement for the triplicate
    ``PlanningService`` / ``ReadinessService`` / ``RecommendationService``
    ``_resolve_twin_foundation`` helpers. Constructs a Foundation instance
    per call — never stores process-global state.
    """
    try:
        from app.application.config.v2_flags import resolve_v2_feature_flags
        from app.infrastructure.adapters.digital_twin import (
            build_student_digital_twin_foundation,
        )

        flags = resolve_v2_feature_flags(environ=environ)
        if not flags.ENABLE_DIGITAL_TWIN:
            return None
        return build_student_digital_twin_foundation(enabled=True)
    except Exception:  # noqa: BLE001
        logger.debug(
            "Twin Foundation unavailable for consumer-chain DI",
            exc_info=True,
        )
        return None


def assemble_shared_canonical_state(
    foundation: object,
    student_id: str,
    *,
    canonical_state: object | None = None,
    service_name: str = "",
    api_name: str = "",
    telemetry: Any | None = None,
) -> object:
    """Return injected CLS or assemble once via Foundation.

    When ``canonical_state`` is provided, Foundation.assemble is not called
    and an observational share-hit is recorded. Otherwise Foundation.assemble
    runs and an assemble event is recorded.

    Args:
        foundation: Enabled ``StudentDigitalTwinFoundation`` (or test double).
        student_id: Student id string passed to ``assemble``.
        canonical_state: Optional already-assembled immutable CLS.
        service_name: Observability host service label.
        api_name: Observability API label.
        telemetry: Optional telemetry sink (tests).

    Returns:
        Canonical learner state object (injected or freshly assembled).
    """
    sink = telemetry or get_consumer_chain_telemetry()
    sid = str(student_id)

    if canonical_state is not None:
        sink.emit_foundation_assemble(
            service_name=service_name,
            api_name=api_name,
            student_id=sid,
            assemble_source=ASSEMBLE_SOURCE_INJECTED,
            assembled=False,
        )
        return canonical_state

    state = foundation.assemble(sid)  # type: ignore[attr-defined]
    sink.emit_foundation_assemble(
        service_name=service_name,
        api_name=api_name,
        student_id=sid,
        assemble_source=ASSEMBLE_SOURCE_ASSEMBLED,
        assembled=True,
    )
    return state


__all__ = [
    "ASSEMBLE_SOURCE_ASSEMBLED",
    "ASSEMBLE_SOURCE_INJECTED",
    "assemble_shared_canonical_state",
    "resolve_enabled_twin_foundation",
]
