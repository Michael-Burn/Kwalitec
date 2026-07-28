"""Pipeline stage catalogue — operational identifiers only."""

from __future__ import annotations

from enum import StrEnum

from app.application.educational_intelligence_pipeline.versions import (
    PIPELINE_STAGE_ORDER,
)


class PipelineStage(StrEnum):
    """Named stages of the certified Educational Intelligence pipeline."""

    INTERPRETATION = "interpretation"
    DECISION = "decision"
    TWIN_UPDATE = "twin_update"
    GRAPH_PROJECTION = "graph_projection"
    MISSION_PLANNING = "mission_planning"
    TUTOR_EXPLANATION = "tutor_explanation"

    @classmethod
    def ordered(cls) -> tuple[PipelineStage, ...]:
        """Return stages in certified execution order."""
        return tuple(cls(token) for token in PIPELINE_STAGE_ORDER)
