"""Application Layer configuration — progressive Integration rollout.

Owns framework-independent product configuration such as Educational
Intelligence feature flags. Does not own educational reasoning or Flask
runtime config. Internal Alpha env resolution lives in ``internal_alpha``.
"""

from __future__ import annotations

from app.application.config.feature_flags import (
    ENABLE_EDUCATIONAL_ORCHESTRATOR,
    ENABLE_EI_EXPLAINABILITY,
    ENABLE_EI_MISSIONS,
    ENABLE_EI_PROGRESS,
    ENABLE_EI_RECOMMENDATIONS,
    FEATURE_FLAGS,
    EducationalIntelligenceFeatureFlags,
)
from app.application.config.internal_alpha import (
    build_twin_provider,
    is_internal_alpha_enabled,
    resolve_feature_flags,
)
from app.application.config.v2_flags import (
    V2_FEATURE_FLAGS,
    Version2FeatureFlags,
    resolve_v2_feature_flags,
)

__all__ = [
    "ENABLE_EDUCATIONAL_ORCHESTRATOR",
    "ENABLE_EI_EXPLAINABILITY",
    "ENABLE_EI_MISSIONS",
    "ENABLE_EI_PROGRESS",
    "ENABLE_EI_RECOMMENDATIONS",
    "FEATURE_FLAGS",
    "EducationalIntelligenceFeatureFlags",
    "V2_FEATURE_FLAGS",
    "Version2FeatureFlags",
    "build_twin_provider",
    "is_internal_alpha_enabled",
    "resolve_feature_flags",
    "resolve_v2_feature_flags",
]
