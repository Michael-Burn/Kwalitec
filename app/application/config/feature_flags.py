"""Educational Intelligence feature flags — progressive product rollout.

Single source of truth for Stage A coexistence. Safe defaults keep unfinished
Twin-first student experiences hidden until cutover enables them.

Framework-independent Application Layer configuration. No web framework,
HTTP handlers, or environment loading in this milestone (Capability 3.3.1).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EducationalIntelligenceFeatureFlags:
    """Immutable EI rollout switches.

    All flags default to ``False`` so Stage A product surfaces continue to
    consume legacy peers until progressive cutover explicitly enables each
    Educational Intelligence experience.
    """

    ENABLE_EDUCATIONAL_ORCHESTRATOR: bool = False
    ENABLE_EI_RECOMMENDATIONS: bool = False
    ENABLE_EI_MISSIONS: bool = False
    ENABLE_EI_EXPLAINABILITY: bool = False
    ENABLE_EI_PROGRESS: bool = False


# Single source of truth for Educational Intelligence product rollout.
FEATURE_FLAGS = EducationalIntelligenceFeatureFlags()

# Convenience aliases — values are taken from FEATURE_FLAGS only.
ENABLE_EDUCATIONAL_ORCHESTRATOR = FEATURE_FLAGS.ENABLE_EDUCATIONAL_ORCHESTRATOR
ENABLE_EI_RECOMMENDATIONS = FEATURE_FLAGS.ENABLE_EI_RECOMMENDATIONS
ENABLE_EI_MISSIONS = FEATURE_FLAGS.ENABLE_EI_MISSIONS
ENABLE_EI_EXPLAINABILITY = FEATURE_FLAGS.ENABLE_EI_EXPLAINABILITY
ENABLE_EI_PROGRESS = FEATURE_FLAGS.ENABLE_EI_PROGRESS
