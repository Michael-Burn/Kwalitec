"""Rules package for Mission Execution Engine."""

from __future__ import annotations

from application.education.mission_execution.rules.lifecycle_rules import (
    LifecycleRules,
)
from application.education.mission_execution.rules.metrics_rules import MetricsRules
from application.education.mission_execution.rules.progress_rules import ProgressRules

# EvidenceMappingRules imports MissionExecution and is loaded lazily by callers
# (engine / package __init__) to avoid a circular import with models.


def __getattr__(name: str):
    if name == "EvidenceMappingRules":
        from application.education.mission_execution.rules.evidence_mapping_rules import (  # noqa: E501
            EvidenceMappingRules,
        )

        return EvidenceMappingRules
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "EvidenceMappingRules",
    "LifecycleRules",
    "MetricsRules",
    "ProgressRules",
]
