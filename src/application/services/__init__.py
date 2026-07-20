"""Application services — workflow coordination without educational intelligence."""

from __future__ import annotations

from application.services.assessment_application_service import (
    AssessmentApplicationService,
)
from application.services.dashboard_application_service import (
    DashboardApplicationService,
)
from application.services.learning_application_service import LearningApplicationService
from application.services.planning_application_service import PlanningApplicationService
from application.services.twin_application_service import TwinApplicationService

__all__ = [
    "AssessmentApplicationService",
    "DashboardApplicationService",
    "LearningApplicationService",
    "PlanningApplicationService",
    "TwinApplicationService",
]
