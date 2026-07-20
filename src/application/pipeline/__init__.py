"""Educational Pipeline — primary Educational Operating System workflow.

Pure orchestration from evidence to student-facing output. Educational
decisions are delegated to domain engines; AI enrichment is optional and
never required for a successful pipeline run.
"""

from __future__ import annotations

from application.pipeline.educational_pipeline import (
    PIPELINE_STAGES,
    EducationalPipeline,
    PipelineStage,
)
from application.pipeline.pipeline_request import (
    PipelineRequest,
    PipelineSessionContext,
)
from application.pipeline.pipeline_result import (
    EnhancedMissionView,
    EnhancedRecommendationsView,
    PipelineResult,
    deterministic_enhanced_mission,
    deterministic_enhanced_recommendations,
)

__all__ = [
    "PIPELINE_STAGES",
    "EducationalPipeline",
    "EnhancedMissionView",
    "EnhancedRecommendationsView",
    "PipelineRequest",
    "PipelineResult",
    "PipelineSessionContext",
    "PipelineStage",
    "deterministic_enhanced_mission",
    "deterministic_enhanced_recommendations",
]
