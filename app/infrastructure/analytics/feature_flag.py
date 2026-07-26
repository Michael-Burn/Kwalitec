"""Analytics feature flag — ``ANALYTICS_EVENTS_V1`` (PRD-001 Phase A).

Defaults OFF. When disabled, the dispatcher is a pure no-op and application
behaviour is unchanged.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

_TRUTHY = frozenset({"1", "true", "yes", "on"})

# Canonical flag name from PRD-001.
ANALYTICS_EVENTS_V1 = "ANALYTICS_EVENTS_V1"
_ENV_ALIASES = (ANALYTICS_EVENTS_V1, "KWALITEC_ANALYTICS_EVENTS_V1")


def _env_truthy(name: str, *, environ: dict[str, str] | None = None) -> bool:
    env = environ if environ is not None else os.environ
    return env.get(name, "").strip().lower() in _TRUTHY


@dataclass(frozen=True)
class AnalyticsFeatureFlag:
    """Immutable analytics rollout switch.

    Attributes:
        events_v1: When True, dispatcher may enqueue validated events.
    """

    events_v1: bool = False

    @property
    def enabled(self) -> bool:
        """True when analytics event emit path is active."""
        return self.events_v1


def resolve_analytics_feature_flag(
    *,
    environ: dict[str, str] | None = None,
) -> AnalyticsFeatureFlag:
    """Resolve ``ANALYTICS_EVENTS_V1`` from the process environment.

    Safe default is disabled (False) when unset or non-truthy.
    """
    enabled = False
    for name in _ENV_ALIASES:
        if environ is not None:
            if name in environ:
                enabled = _env_truthy(name, environ=environ)
                break
        elif name in os.environ:
            enabled = _env_truthy(name)
            break
    return AnalyticsFeatureFlag(events_v1=enabled)


# Process default — prefer resolve_* in call sites / tests.
ANALYTICS_FEATURE_FLAG = resolve_analytics_feature_flag()
