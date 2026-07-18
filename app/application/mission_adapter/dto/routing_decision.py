"""Immutable RoutingDecision — deterministic engine selection outcome."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RoutingMode(str, Enum):
    """Supported adapter routing modes."""

    LEGACY = "legacy"
    V2_ONLY = "v2_only"
    PARALLEL = "parallel"
    SHADOW = "shadow"
    A_B = "a_b"


class SelectedEngine(str, Enum):
    """Which engine result is exposed to the caller."""

    V1 = "v1"
    V2 = "v2"
    NONE = "none"


@dataclass(frozen=True)
class RoutingDecision:
    """Deterministic routing outcome for one adapter invocation.

    Attributes:
        mode: Active routing mode.
        primary_engine: Engine whose result is returned to the caller.
        shadow_engine: Optional secondary engine (shadow / parallel).
        compare: True when comparison must run.
        expose_v2: True when V2 may be returned to production callers.
        reason: Stable machine-readable reason code.
        fallback_engine: Engine to use if primary fails (may be None).
        ab_bucket: Deterministic A/B bucket when mode is A_B.
    """

    mode: RoutingMode
    primary_engine: SelectedEngine
    shadow_engine: SelectedEngine | None
    compare: bool
    expose_v2: bool
    reason: str
    fallback_engine: SelectedEngine | None = None
    ab_bucket: str | None = None
