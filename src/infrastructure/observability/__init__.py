"""Operational observability for the Educational Operating System.

Architecture Source
    APP-004 Production Readiness & Version 2 Release

Metrics and logs are operational only — never educational scores.
"""

from __future__ import annotations

from infrastructure.observability.enrichment_observer import (
    ObservedMissionEnricher,
    ObservedRecommendationEnricher,
)
from infrastructure.observability.logging import (
    StructuredLogger,
    configure_structured_logging,
)
from infrastructure.observability.metrics import PipelineMetrics
from infrastructure.observability.pipeline_observer import ObservedEducationalPipeline
from infrastructure.observability.timing import TimingRecorder, timed

__all__ = [
    "ObservedEducationalPipeline",
    "ObservedMissionEnricher",
    "ObservedRecommendationEnricher",
    "PipelineMetrics",
    "StructuredLogger",
    "TimingRecorder",
    "configure_structured_logging",
    "timed",
]
