"""Educational Intelligence Pipeline — production orchestration (PR-001).

Coordinates certified stage services. No educational logic lives here.
"""

from __future__ import annotations

from app.application.educational_intelligence_pipeline.events import (
    PipelineEvent,
    PipelineEventCollector,
    PipelineEventType,
)
from app.application.educational_intelligence_pipeline.health import (
    EducationalPlatformHealth,
    PlatformHealthReport,
)
from app.application.educational_intelligence_pipeline.metrics import (
    MetricsCollector,
    PipelineMetrics,
    StageTiming,
)
from app.application.educational_intelligence_pipeline.orchestrator import (
    EducationalPipelineOrchestrator,
)
from app.application.educational_intelligence_pipeline.registry import (
    COMPONENT_REGISTRATIONS,
    pipeline_manifest,
    probe_all_registrations,
)
from app.application.educational_intelligence_pipeline.result import (
    PipelineExecutionResult,
)
from app.application.educational_intelligence_pipeline.stages import PipelineStage
from app.application.educational_intelligence_pipeline.versions import (
    CERTIFICATION_PROGRAMME,
    CERTIFICATION_STATUS,
    ORCHESTRATOR_VERSION,
    PIPELINE_STAGE_ORDER,
)

__all__ = [
    "CERTIFICATION_PROGRAMME",
    "CERTIFICATION_STATUS",
    "COMPONENT_REGISTRATIONS",
    "EducationalPipelineOrchestrator",
    "EducationalPlatformHealth",
    "MetricsCollector",
    "ORCHESTRATOR_VERSION",
    "PIPELINE_STAGE_ORDER",
    "PipelineEvent",
    "PipelineEventCollector",
    "PipelineEventType",
    "PipelineExecutionResult",
    "PipelineMetrics",
    "PipelineStage",
    "PlatformHealthReport",
    "StageTiming",
    "pipeline_manifest",
    "probe_all_registrations",
]
