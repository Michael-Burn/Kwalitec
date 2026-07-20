"""DTO tests — application projections, not domain entities."""

from __future__ import annotations

from dataclasses import fields, is_dataclass

from application.dto import (
    DigitalTwinSummaryDTO,
    EvidenceHistoryDTO,
    EvidenceRecordDTO,
    LearnerStateDTO,
    LearningEpisodeDTO,
    LearningSessionDTO,
    LearningTrajectoryDTO,
    TeachingPlanDTO,
    TeachingPlanStepDTO,
    TrajectoryPointDTO,
)
from application.services.mappers import (
    to_learner_state_dto,
    to_learning_trajectory_dto,
    to_teaching_plan_dto,
)
from domain.education.digital_twin import EducationalDigitalTwin
from domain.education.foundation.ids import DigitalTwinId
from tests.education_os.application.helpers import make_planned_episode


def test_dtos_are_frozen_dataclasses() -> None:
    for cls in (
        LearnerStateDTO,
        TeachingPlanDTO,
        TeachingPlanStepDTO,
        EvidenceRecordDTO,
        EvidenceHistoryDTO,
        LearningEpisodeDTO,
        LearningSessionDTO,
        LearningTrajectoryDTO,
        TrajectoryPointDTO,
        DigitalTwinSummaryDTO,
    ):
        assert is_dataclass(cls)
        assert cls.__dataclass_params__.frozen  # type: ignore[attr-defined]


def test_learner_state_dto_has_no_domain_entity_fields() -> None:
    names = {f.name for f in fields(LearnerStateDTO)}
    assert names == {
        "twin_id",
        "student_id",
        "learner_state_id",
        "activity_status",
        "twin_status",
        "concept_count",
        "evidence_count",
        "intervention_count",
    }
    for name in names:
        assert "EducationalDigitalTwin" not in name
        assert "LearnerState" not in name or name == "learner_state_id"


def test_mapper_projects_twin_to_dto() -> None:
    twin = EducationalDigitalTwin.create(
        twin_id=DigitalTwinId("twin-dto"),
        student_id="student-ada",
    )
    dto = to_learner_state_dto(twin)
    assert isinstance(dto, LearnerStateDTO)
    assert dto.twin_id == "twin-dto"
    assert dto.student_id == "student-ada"
    assert dto.activity_status == "engaged"
    traj = to_learning_trajectory_dto(twin)
    assert traj.length >= 1
    assert traj.points[0].kind == "created"


def test_mapper_projects_episode_to_teaching_plan_dto() -> None:
    episode = make_planned_episode()
    dto = to_teaching_plan_dto(episode, plan_id="plan-001")
    assert isinstance(dto, TeachingPlanDTO)
    assert dto.plan_id == "plan-001"
    assert dto.episode_id == "episode-001"
    assert dto.status == "planned"
    assert len(dto.steps) == 2
    assert dto.steps[0].kind == "explanation"


def test_evidence_history_count() -> None:
    history = EvidenceHistoryDTO(student_id="student-ada", records=())
    assert history.count == 0
