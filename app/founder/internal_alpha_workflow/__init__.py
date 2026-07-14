"""Internal Alpha Live Workflow (FSI-003).

Integrates FOS-003 → FOS-005 → FOS-006 → FOS-007 against the live
``research/internal_alpha/week_NNN/`` repository layout.

Coordinator only. No AI. No Dashboard or Recommendation Engine changes.
"""

from __future__ import annotations

from app.founder.internal_alpha_workflow.config import (
    InternalAlphaWorkflowConfig,
    default_config,
)
from app.founder.internal_alpha_workflow.discovery import WeekDiscoveryService
from app.founder.internal_alpha_workflow.dto import (
    WeekReference,
    WorkflowError,
    WorkflowResult,
)
from app.founder.internal_alpha_workflow.exporters import WorkflowOutputManager
from app.founder.internal_alpha_workflow.services import InternalAlphaWorkflowService

__all__ = [
    "InternalAlphaWorkflowConfig",
    "InternalAlphaWorkflowService",
    "WeekDiscoveryService",
    "WeekReference",
    "WorkflowError",
    "WorkflowOutputManager",
    "WorkflowResult",
    "default_config",
]
