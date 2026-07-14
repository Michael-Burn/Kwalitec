"""Educational Intelligence Version 1.0 learning loop Integration.

Wires Educational Evidence → Twin Update Coordinator → Knowledge Strategy →
Twin Composer → Twin Repository → Twin Provider → Educational Intelligence →
Recommendation.

Owns dependency wiring, orchestration integration, repository/provider
interaction, and pipeline observability. Never reasons educationally, never
redesigns Strategies / Composer / Coordinator / Intelligence, never bypasses
TwinProvider on the read path.
"""

from __future__ import annotations

from app.application.learning_loop.pipeline import (
    EducationalLearningLoop,
    LearningLoopContext,
    LearningLoopFailure,
    LearningLoopFailureReason,
    LearningLoopResult,
    LearningLoopSuccess,
    build_version_1_0_learning_loop,
    build_version_1_0_twin_update_coordinator,
)

__all__ = [
    "EducationalLearningLoop",
    "LearningLoopContext",
    "LearningLoopFailure",
    "LearningLoopFailureReason",
    "LearningLoopResult",
    "LearningLoopSuccess",
    "build_version_1_0_learning_loop",
    "build_version_1_0_twin_update_coordinator",
]
