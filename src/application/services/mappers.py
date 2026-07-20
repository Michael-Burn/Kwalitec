"""Map domain aggregates to application DTOs.

Mapping is structural projection only — no educational interpretation.
"""

from __future__ import annotations

from application.dto.evidence import EvidenceHistoryDTO, EvidenceRecordDTO
from application.dto.learner import LearnerStateDTO
from application.dto.learning import LearningEpisodeDTO, LearningSessionDTO
from application.dto.teaching_plan import TeachingPlanDTO, TeachingPlanStepDTO
from application.dto.trajectory import LearningTrajectoryDTO, TrajectoryPointDTO
from application.dto.twin import DigitalTwinSummaryDTO
from domain.education.digital_twin import EducationalDigitalTwin
from domain.education.evidence import EvidenceRecord
from domain.education.learning_episode import LearningEpisode


def to_learner_state_dto(twin: EducationalDigitalTwin) -> LearnerStateDTO:
    return LearnerStateDTO(
        twin_id=twin.twin_id.value,
        student_id=twin.student_id,
        learner_state_id=twin.learner_state.learner_state_id.value,
        activity_status=twin.learner_state.activity_status.value,
        twin_status=twin.status.value,
        concept_count=twin.concept_count(),
        evidence_count=twin.evidence_count(),
        intervention_count=twin.intervention_count(),
    )


def to_learning_trajectory_dto(twin: EducationalDigitalTwin) -> LearningTrajectoryDTO:
    points = tuple(
        TrajectoryPointDTO(
            sequence=point.sequence,
            kind=point.kind.value,
            label=point.label,
        )
        for point in twin.trajectory.points
    )
    return LearningTrajectoryDTO(
        twin_id=twin.twin_id.value,
        student_id=twin.student_id,
        points=points,
    )


def to_learning_episode_dto(episode: LearningEpisode) -> LearningEpisodeDTO:
    outcome = episode.outcome
    return LearningEpisodeDTO(
        episode_id=episode.episode_id.value,
        student_id=episode.student_id,
        status=episode.status.value,
        teaching_goal_statement=episode.teaching_goal.statement,
        teaching_strategy_id=episode.teaching_strategy_id.value,
        primary_dimension=episode.primary_dimension.value,
        step_count=len(episode.steps),
        evidence_count=len(episode.evidence_ids),
        has_reflection=episode.reflection is not None,
        outcome_kind=outcome.kind.value if outcome is not None else None,
    )


def to_learning_session_dto(episode: LearningEpisode) -> LearningSessionDTO:
    active = next((step for step in episode.steps if step.is_active()), None)
    return LearningSessionDTO(
        episode_id=episode.episode_id.value,
        student_id=episode.student_id,
        status=episode.status.value,
        first_active_step_id=active.step_id.value if active is not None else None,
    )


def to_teaching_plan_dto(episode: LearningEpisode, *, plan_id: str) -> TeachingPlanDTO:
    steps = tuple(
        TeachingPlanStepDTO(
            step_id=step.step_id.value,
            kind=step.kind.value,
            sequence_index=step.sequence_index,
            label=step.label,
            required=step.required,
            status=step.status.value,
        )
        for step in episode.steps
    )
    return TeachingPlanDTO(
        plan_id=plan_id,
        episode_id=episode.episode_id.value,
        student_id=episode.student_id,
        teaching_goal_statement=episode.teaching_goal.statement,
        teaching_strategy_id=episode.teaching_strategy_id.value,
        primary_dimension=episode.primary_dimension.value,
        status=episode.status.value,
        learning_objective_ids=tuple(
            ref.objective_id.value for ref in episode.learning_objectives
        ),
        concept_ids=tuple(ref.concept_id.value for ref in episode.concept_references),
        steps=steps,
    )


def to_evidence_record_dto(record: EvidenceRecord) -> EvidenceRecordDTO:
    return EvidenceRecordDTO(
        evidence_id=record.evidence_id.value,
        student_id=record.student_id,
        status=record.status.value,
        strength_level=record.strength.level.value,
        confidence_level=record.confidence.level.value,
        item_count=len(record.items),
        concept_ids=tuple(ref.concept_id.value for ref in record.concept_references),
        learning_episode_ids=tuple(eid.value for eid in record.learning_episode_ids),
        occurred_at=record.timestamp.occurred_at.isoformat(),
    )


def to_evidence_history_dto(
    student_id: str, records: list[EvidenceRecord]
) -> EvidenceHistoryDTO:
    ordered = sorted(records, key=lambda r: r.timestamp.occurred_at)
    return EvidenceHistoryDTO(
        student_id=student_id,
        records=tuple(to_evidence_record_dto(record) for record in ordered),
    )


def to_twin_summary_dto(
    twin: EducationalDigitalTwin, *, update_kind: str
) -> DigitalTwinSummaryDTO:
    return DigitalTwinSummaryDTO(
        twin_id=twin.twin_id.value,
        student_id=twin.student_id,
        status=twin.status.value,
        update_kind=update_kind,
        evidence_count=twin.evidence_count(),
        concept_count=twin.concept_count(),
        trajectory_length=twin.trajectory.length(),
    )
