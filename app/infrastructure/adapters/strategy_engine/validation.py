"""Strategy Engine validation (MS-005 S1).

Validates StrategyContext / LearningIntervention structural integrity.
Does not estimate missing educational state or mutate inputs.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.adapters.strategy_engine.contracts import (
    AVAILABILITY_VALUES,
    INTERVENTION_KINDS,
    LearningIntervention,
    StrategyContext,
)


class StrategyValidationError(ValueError):
    """Raised when Strategy context or intervention fails structural validation."""


def validate_student_id(student_id: str) -> str:
    """Return stripped non-empty student_id or raise StrategyValidationError."""
    sid = (student_id or "").strip()
    if not sid:
        raise StrategyValidationError("student_id must be a non-empty string")
    return sid


def validate_as_of(as_of: str | None) -> str | None:
    """Validate optional decision clock (ISO string or None — never wall-clock)."""
    if as_of is None:
        return None
    if not isinstance(as_of, str):
        raise StrategyValidationError("as_of must be an ISO string or None")
    clock = as_of.strip()
    return clock or None


def validate_strategy_context(context: StrategyContext) -> StrategyContext:
    """Validate an assembled StrategyContext (identity + availability honesty)."""
    if not isinstance(context, StrategyContext):
        raise StrategyValidationError("context must be a StrategyContext")
    validate_student_id(context.student_id)
    validate_as_of(context.as_of)
    for attr in (
        "adaptive_availability",
        "twin_availability",
        "runtime_a_availability",
    ):
        value = getattr(context, attr)
        if value not in AVAILABILITY_VALUES:
            raise StrategyValidationError(
                f"{attr} must be 'available', 'unavailable', or empty"
            )
    for kind in context.intervention_kinds:
        if kind not in INTERVENTION_KINDS:
            raise StrategyValidationError(f"unknown intervention kind: {kind}")
    return context


def validate_learning_intervention(
    intervention: LearningIntervention,
) -> LearningIntervention:
    """Validate a composed LearningIntervention structure."""
    if not isinstance(intervention, LearningIntervention):
        raise StrategyValidationError("intervention must be a LearningIntervention")
    if intervention.kind and intervention.kind not in INTERVENTION_KINDS:
        raise StrategyValidationError(f"unknown intervention kind: {intervention.kind}")
    primary = intervention.sequencing.primary_kind
    if primary and primary not in INTERVENTION_KINDS:
        raise StrategyValidationError(f"unknown sequencing primary_kind: {primary}")
    if primary and intervention.kind and primary != intervention.kind:
        raise StrategyValidationError(
            "intervention.kind must equal sequencing.primary_kind"
        )
    return intervention


def assert_adaptive_topic_order_preserved(
    *,
    adaptive_focus_topics: list[str] | tuple[str, ...],
    study_focus_topics: list[str] | tuple[str, ...],
) -> None:
    """Ensure Strategy study focus preserves Adaptive ranking (no re-rank).

    Strategy may subset / window topics but must not reorder Adaptive topics.
    """
    adaptive = [str(t) for t in adaptive_focus_topics if str(t).strip()]
    study = [str(t) for t in study_focus_topics if str(t).strip()]
    if not adaptive or not study:
        return
    # Study topics that appear in Adaptive must appear in Adaptive relative order.
    adaptive_index = {topic: idx for idx, topic in enumerate(adaptive)}
    previous = -1
    for topic in study:
        if topic not in adaptive_index:
            continue
        idx = adaptive_index[topic]
        if idx < previous:
            raise StrategyValidationError(
                "Strategy must not re-rank Adaptive focus topics"
            )
        previous = idx


def mapping_nonempty(value: Any) -> bool:
    """True when an opaque mapping payload has material keys."""
    if value is None:
        return False
    if hasattr(value, "to_canonical_dict"):
        payload = value.to_canonical_dict()
        return bool(payload)
    if isinstance(value, dict):
        return bool(value)
    return bool(value)
