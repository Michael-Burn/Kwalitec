"""Educational Intelligence Internal Alpha — developer daily-use glue.

Enables the Stage A Recommendation vertical slice for personal CS1 study
without public rollout. Does not redesign Educational Intelligence, enable
unfinished widgets, or claim TwinRepository persistence.

Environment:
    KWALITEC_EI_INTERNAL_ALPHA — truthy (1/true/yes/on) enables orchestrator +
    recommendations only. Missions / explainability / progress stay off.
"""

from __future__ import annotations

import os

from app.application.config.feature_flags import (
    FEATURE_FLAGS,
    EducationalIntelligenceFeatureFlags,
)
from app.application.twin.internal_alpha_twin_source import InternalAlphaTwinSource
from app.application.twin.twin_provider import TwinProvider

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def is_internal_alpha_enabled(
    *,
    environ: dict[str, str] | None = None,
) -> bool:
    """Return True when Internal Alpha env switch is on.

    Args:
        environ: Optional env mapping for tests. Defaults to ``os.environ``.
    """
    env = environ if environ is not None else os.environ
    raw = env.get("KWALITEC_EI_INTERNAL_ALPHA", "")
    return raw.strip().lower() in _TRUTHY


def resolve_feature_flags(
    *,
    environ: dict[str, str] | None = None,
) -> EducationalIntelligenceFeatureFlags:
    """Resolve EI flags for the current process.

    Internal Alpha turns on orchestrator + recommendations only. Public
    default remains the safe ``FEATURE_FLAGS`` singleton (all false).
    """
    if not is_internal_alpha_enabled(environ=environ):
        return FEATURE_FLAGS
    return EducationalIntelligenceFeatureFlags(
        ENABLE_EDUCATIONAL_ORCHESTRATOR=True,
        ENABLE_EI_RECOMMENDATIONS=True,
        ENABLE_EI_MISSIONS=False,
        ENABLE_EI_EXPLAINABILITY=False,
        ENABLE_EI_PROGRESS=False,
    )


def build_twin_provider(
    *,
    flags: EducationalIntelligenceFeatureFlags | None = None,
    environ: dict[str, str] | None = None,
) -> TwinProvider:
    """Wire TwinProvider for dashboard composition.

    Internal Alpha installs the interim cold-start TwinSource so the
    Recommendation card is reachable. Without alpha, no source is configured
    (honest TwinAbsent until TwinRepository lands).
    """
    active = flags if flags is not None else resolve_feature_flags(environ=environ)
    if active.ENABLE_EDUCATIONAL_ORCHESTRATOR and is_internal_alpha_enabled(
        environ=environ
    ):
        return TwinProvider(source=InternalAlphaTwinSource())
    return TwinProvider()
