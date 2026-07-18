"""Intervention types supported by the Adaptive Decision Engine.

Phase 1 implements REVISION only. Other types exist as domain vocabulary
so future intervention strategies can plug in without redesign.
"""

from __future__ import annotations

from enum import StrEnum


class InterventionType(StrEnum):
    """Educational intervention kinds the engine may recommend."""

    REVISION = "revision"
    CONTINUE = "continue"
    REPEAT = "repeat"
    ASSESS = "assess"
    BREAK = "break"
    SKIP = "skip"


# Phase 1: only revision decisions are produced by the application engine.
PHASE1_IMPLEMENTED_TYPES: frozenset[InterventionType] = frozenset(
    {InterventionType.REVISION}
)


def resolve_intervention_type(value: InterventionType | str) -> InterventionType:
    """Resolve a string or enum to InterventionType."""
    if isinstance(value, InterventionType):
        return value
    token = (value or "").strip().lower()
    try:
        return InterventionType(token)
    except ValueError as exc:
        raise ValueError(f"unknown intervention type: {value!r}") from exc


def is_phase1_implemented(value: InterventionType | str) -> bool:
    """True when the intervention type is implemented in Phase 1."""
    return resolve_intervention_type(value) in PHASE1_IMPLEMENTED_TYPES
