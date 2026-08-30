"""ADR-027 Phase 2 permanent Twin cutover helpers.

Application-layer only: Twin 0-1 -> 0-100 display scale. The cutover is
unconditional and has no feature flag.
ORM / StudyPlan / Twin adapter wiring lives in infrastructure cutover_bridge.
"""

from __future__ import annotations

from app.application.student_twin.query import TopicKnowledgeFact


def ek_display_0_100(fact: TopicKnowledgeFact | None) -> float | None:
    """Map Twin 0-1 Estimated Knowledge to Stage A 0-100 display scale.

    Returns None when there is no evidence-backed EK (never invents 0).
    """
    if fact is None or not fact.has_estimated_knowledge:
        return None
    if fact.estimated_knowledge is None:
        return None
    return round(float(fact.estimated_knowledge) * 100.0, 1)
