"""Query handlers — thin delegates to application services."""

from __future__ import annotations

from application.dto.evidence import EvidenceHistoryDTO
from application.dto.learner import LearnerStateDTO
from application.dto.teaching_plan import TeachingPlanDTO
from application.dto.trajectory import LearningTrajectoryDTO
from application.queries.get_evidence_history import GetEvidenceHistory
from application.queries.get_learner_state import GetLearnerState
from application.queries.get_learning_trajectory import GetLearningTrajectory
from application.queries.get_teaching_plan import GetTeachingPlan
from application.services.assessment_application_service import (
    AssessmentApplicationService,
)
from application.services.planning_application_service import PlanningApplicationService
from application.services.twin_application_service import TwinApplicationService


class GetLearnerStateHandler:
    """Handle GetLearnerState."""

    def __init__(self, service: TwinApplicationService) -> None:
        self._service = service

    def handle(self, query: GetLearnerState) -> LearnerStateDTO:
        return self._service.get_learner_state(query)


class GetTeachingPlanHandler:
    """Handle GetTeachingPlan."""

    def __init__(self, service: PlanningApplicationService) -> None:
        self._service = service

    def handle(self, query: GetTeachingPlan) -> TeachingPlanDTO:
        return self._service.get_teaching_plan(query)


class GetEvidenceHistoryHandler:
    """Handle GetEvidenceHistory."""

    def __init__(self, service: AssessmentApplicationService) -> None:
        self._service = service

    def handle(self, query: GetEvidenceHistory) -> EvidenceHistoryDTO:
        return self._service.get_evidence_history(query)


class GetLearningTrajectoryHandler:
    """Handle GetLearningTrajectory."""

    def __init__(self, service: TwinApplicationService) -> None:
        self._service = service

    def handle(self, query: GetLearningTrajectory) -> LearningTrajectoryDTO:
        return self._service.get_learning_trajectory(query)
