"""Command handlers — thin delegates to application services."""

from __future__ import annotations

from application.commands.complete_learning_episode import CompleteLearningEpisode
from application.commands.generate_teaching_plan import GenerateTeachingPlan
from application.commands.record_evidence import RecordEvidence
from application.commands.start_learning_session import StartLearningSession
from application.commands.update_digital_twin import UpdateDigitalTwin
from application.dto.evidence import EvidenceRecordDTO
from application.dto.learning import LearningEpisodeDTO, LearningSessionDTO
from application.dto.teaching_plan import TeachingPlanDTO
from application.dto.twin import DigitalTwinSummaryDTO
from application.services.assessment_application_service import (
    AssessmentApplicationService,
)
from application.services.learning_application_service import LearningApplicationService
from application.services.planning_application_service import PlanningApplicationService
from application.services.twin_application_service import TwinApplicationService


class StartLearningSessionHandler:
    """Handle StartLearningSession."""

    def __init__(self, service: LearningApplicationService) -> None:
        self._service = service

    def handle(self, command: StartLearningSession) -> LearningSessionDTO:
        return self._service.start_learning_session(command)


class CompleteLearningEpisodeHandler:
    """Handle CompleteLearningEpisode."""

    def __init__(self, service: LearningApplicationService) -> None:
        self._service = service

    def handle(self, command: CompleteLearningEpisode) -> LearningEpisodeDTO:
        return self._service.complete_learning_episode(command)


class RecordEvidenceHandler:
    """Handle RecordEvidence."""

    def __init__(self, service: AssessmentApplicationService) -> None:
        self._service = service

    def handle(self, command: RecordEvidence) -> EvidenceRecordDTO:
        return self._service.record_evidence(command)


class UpdateDigitalTwinHandler:
    """Handle UpdateDigitalTwin."""

    def __init__(self, service: TwinApplicationService) -> None:
        self._service = service

    def handle(self, command: UpdateDigitalTwin) -> DigitalTwinSummaryDTO:
        return self._service.update_digital_twin(command)


class GenerateTeachingPlanHandler:
    """Handle GenerateTeachingPlan."""

    def __init__(self, service: PlanningApplicationService) -> None:
        self._service = service

    def handle(self, command: GenerateTeachingPlan) -> TeachingPlanDTO:
        return self._service.generate_teaching_plan(command)
