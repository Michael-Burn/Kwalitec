"""Map mission execution events to EducationalEvidence.

Does not estimate mastery. Emits structured evidence only.
"""

from __future__ import annotations

from application.education.mission_execution.enums import ExecutionEventKind
from application.education.mission_execution.events import (
    ConfidenceRecorded,
    MissionAbandoned,
    MissionCompleted,
    MissionExecutionEvent,
    MissionExpired,
    MissionPaused,
    MissionResumed,
    MissionStarted,
    ReflectionRecorded,
    StepCompleted,
    StepSkipped,
)
from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)
from domain.education.educational_evidence.aggregates.educational_evidence import (
    EducationalEvidence,
)
from domain.education.educational_evidence.enums import LearningEnvironmentKind
from domain.education.educational_evidence.ids import EvidenceId
from domain.education.educational_evidence.value_objects.evidence_source import (
    EvidenceSource,
)
from domain.education.educational_evidence.value_objects.learning_environment import (
    LearningEnvironment,
)
from domain.education.foundation.ids import LearningEpisodeId

_ORIGIN = "mission_execution_engine"
_ENVIRONMENT = LearningEnvironment.of(
    LearningEnvironmentKind.MISSION, label="mission_execution"
)


class EvidenceMappingRules:
    """Deterministic mapping from execution events → EducationalEvidence."""

    @staticmethod
    def map_event(
        event: MissionExecutionEvent,
        execution: MissionExecution,
    ) -> tuple[EducationalEvidence, ...]:
        """Map one event to zero or more evidence records.

        Evidence identities are derived deterministically from
        ``execution_id`` + event sequence so repeated mapping is stable.
        """
        kind = event.kind
        if kind is ExecutionEventKind.MISSION_STARTED:
            assert isinstance(event, MissionStarted)
            return EvidenceMappingRules._study_session_started(event, execution)
        if kind is ExecutionEventKind.STEP_COMPLETED:
            assert isinstance(event, StepCompleted)
            return EvidenceMappingRules._practice_activity(event, execution)
        if kind is ExecutionEventKind.CONFIDENCE_RECORDED:
            assert isinstance(event, ConfidenceRecorded)
            return EvidenceMappingRules._self_confidence(event, execution)
        if kind is ExecutionEventKind.REFLECTION_RECORDED:
            assert isinstance(event, ReflectionRecorded)
            return EvidenceMappingRules._reflection(event, execution)
        if kind is ExecutionEventKind.MISSION_COMPLETED:
            assert isinstance(event, MissionCompleted)
            return EvidenceMappingRules._mission_completion(event, execution)
        if kind is ExecutionEventKind.MISSION_ABANDONED:
            assert isinstance(event, MissionAbandoned)
            return EvidenceMappingRules._engagement_abandoned(event, execution)
        if kind is ExecutionEventKind.MISSION_EXPIRED:
            assert isinstance(event, MissionExpired)
            return EvidenceMappingRules._study_time(event, execution)
        if kind is ExecutionEventKind.MISSION_PAUSED:
            assert isinstance(event, MissionPaused)
            return ()
        if kind is ExecutionEventKind.MISSION_RESUMED:
            assert isinstance(event, MissionResumed)
            return ()
        if kind is ExecutionEventKind.STEP_SKIPPED:
            assert isinstance(event, StepSkipped)
            return ()
        return ()

    @staticmethod
    def _evidence_id(
        execution: MissionExecution, sequence: int, suffix: str
    ) -> EvidenceId:
        return EvidenceId(
            f"{execution.execution_id.value}:ev:{sequence}:{suffix}"
        )

    @staticmethod
    def _episode_id(execution: MissionExecution) -> LearningEpisodeId:
        return LearningEpisodeId(f"episode:{execution.execution_id.value}")

    @staticmethod
    def _source_student() -> EvidenceSource:
        return EvidenceSource.student_action(_ORIGIN)

    @staticmethod
    def _source_system() -> EvidenceSource:
        return EvidenceSource.system_observation(_ORIGIN)

    @staticmethod
    def _source_self() -> EvidenceSource:
        return EvidenceSource.self_report(_ORIGIN)

    @staticmethod
    def _study_session_started(
        event: MissionStarted, execution: MissionExecution
    ) -> tuple[EducationalEvidence, ...]:
        evidence = EducationalEvidence.record_session_start(
            EvidenceMappingRules._evidence_id(
                execution, event.sequence, "session_start"
            ),
            execution.student_id.value,
            event.occurred_at,
            EvidenceMappingRules._source_system(),
            learning_environment=_ENVIRONMENT,
            learning_episode_id=EvidenceMappingRules._episode_id(execution),
            subject_id=execution.mission.subject_id,
        )
        return (evidence,)

    @staticmethod
    def _practice_activity(
        event: StepCompleted, execution: MissionExecution
    ) -> tuple[EducationalEvidence, ...]:
        step = execution.find_step(event.step_id)
        competency = None
        subject = execution.mission.subject_id
        if step is not None:
            competency = step.competency_id or execution.mission.competency_id
            subject = step.subject_id or subject
        else:
            competency = execution.mission.competency_id
        if competency is None:
            # Without a competency target, emit study time instead of practice.
            return EvidenceMappingRules._time_invested_for_event(
                execution, event.sequence, event.occurred_at, duration_seconds=0.0
            )
        evidence = EducationalEvidence.record_competency_practice(
            EvidenceMappingRules._evidence_id(execution, event.sequence, "practice"),
            execution.student_id.value,
            event.occurred_at,
            EvidenceMappingRules._source_student(),
            learning_environment=_ENVIRONMENT,
            competency_id=competency,
            subject_id=subject,
            extra_metadata={
                "step_id": event.step_id.value,
                "execution_id": execution.execution_id.value,
            },
        )
        return (evidence,)

    @staticmethod
    def _self_confidence(
        event: ConfidenceRecorded, execution: MissionExecution
    ) -> tuple[EducationalEvidence, ...]:
        subject_id = execution.mission.subject_id
        competency_id = execution.mission.competency_id
        if event.step_id is not None:
            step = execution.find_step(event.step_id)
            if step is not None:
                subject_id = step.subject_id or subject_id
                competency_id = step.competency_id or competency_id
        if subject_id is None and competency_id is None:
            # Confidence evidence requires a curriculum target.
            return ()
        extra: dict[str, str] = {"execution_id": execution.execution_id.value}
        if event.step_id is not None:
            extra["step_id"] = event.step_id.value
        evidence = EducationalEvidence.record_confidence(
            EvidenceMappingRules._evidence_id(execution, event.sequence, "confidence"),
            execution.student_id.value,
            event.occurred_at,
            EvidenceMappingRules._source_self(),
            learning_environment=_ENVIRONMENT,
            confidence_level=event.level.value,
            subject_id=subject_id,
            competency_id=competency_id,
            extra_metadata=extra,
        )
        return (evidence,)

    @staticmethod
    def _reflection(
        event: ReflectionRecorded, execution: MissionExecution
    ) -> tuple[EducationalEvidence, ...]:
        evidence = EducationalEvidence.record_reflection(
            EvidenceMappingRules._evidence_id(execution, event.sequence, "reflection"),
            execution.student_id.value,
            event.occurred_at,
            EvidenceMappingRules._source_self(),
            learning_environment=_ENVIRONMENT,
            reflection_text=event.text,
            subject_id=execution.mission.subject_id,
            competency_id=execution.mission.competency_id,
            mission_id=execution.mission_id.value,
            learning_episode_id=EvidenceMappingRules._episode_id(execution),
            extra_metadata={"execution_id": execution.execution_id.value},
        )
        return (evidence,)

    @staticmethod
    def _mission_completion(
        event: MissionCompleted, execution: MissionExecution
    ) -> tuple[EducationalEvidence, ...]:
        completion = EducationalEvidence.record_mission_completion(
            EvidenceMappingRules._evidence_id(
                execution, event.sequence, "mission_done"
            ),
            execution.student_id.value,
            event.occurred_at,
            EvidenceMappingRules._source_system(),
            learning_environment=_ENVIRONMENT,
            mission_id=execution.mission_id.value,
            completed=True,
            subject_id=execution.mission.subject_id,
            extra_metadata={"execution_id": execution.execution_id.value},
        )
        session = EducationalEvidence.record_session_completion(
            EvidenceMappingRules._evidence_id(
                execution, event.sequence, "session_done"
            ),
            execution.student_id.value,
            event.occurred_at,
            EvidenceMappingRules._source_system(),
            learning_environment=_ENVIRONMENT,
            learning_episode_id=EvidenceMappingRules._episode_id(execution),
            subject_id=execution.mission.subject_id,
            extra_metadata={"execution_id": execution.execution_id.value},
        )
        time_ev = EvidenceMappingRules._time_invested_for_event(
            execution,
            event.sequence,
            event.occurred_at,
            duration_seconds=execution.elapsed_study_time_seconds,
            suffix="time",
        )
        return (completion, session, *time_ev)

    @staticmethod
    def _engagement_abandoned(
        event: MissionAbandoned, execution: MissionExecution
    ) -> tuple[EducationalEvidence, ...]:
        abandoned = EducationalEvidence.record_mission_completion(
            EvidenceMappingRules._evidence_id(
                execution, event.sequence, "mission_abandoned"
            ),
            execution.student_id.value,
            event.occurred_at,
            EvidenceMappingRules._source_system(),
            learning_environment=_ENVIRONMENT,
            mission_id=execution.mission_id.value,
            completed=False,
            subject_id=execution.mission.subject_id,
            extra_metadata={
                "execution_id": execution.execution_id.value,
                "engagement": "abandoned",
            },
        )
        time_ev = EvidenceMappingRules._time_invested_for_event(
            execution,
            event.sequence,
            event.occurred_at,
            duration_seconds=execution.elapsed_study_time_seconds,
            suffix="time",
        )
        return (abandoned, *time_ev)

    @staticmethod
    def _study_time(
        event: MissionExpired, execution: MissionExecution
    ) -> tuple[EducationalEvidence, ...]:
        return EvidenceMappingRules._time_invested_for_event(
            execution,
            event.sequence,
            event.occurred_at,
            duration_seconds=execution.elapsed_study_time_seconds,
            suffix="time",
        )

    @staticmethod
    def _time_invested_for_event(
        execution: MissionExecution,
        sequence: int,
        occurred_at: object,
        *,
        duration_seconds: float,
        suffix: str = "time",
    ) -> tuple[EducationalEvidence, ...]:
        duration = float(duration_seconds)
        if duration <= 0.0:
            # TIME_INVESTED evidence requires a positive duration.
            return ()
        evidence = EducationalEvidence.record_time_invested(
            EvidenceMappingRules._evidence_id(execution, sequence, suffix),
            execution.student_id.value,
            occurred_at,  # type: ignore[arg-type]
            EvidenceMappingRules._source_system(),
            learning_environment=_ENVIRONMENT,
            duration_seconds=duration,
            subject_id=execution.mission.subject_id,
            competency_id=execution.mission.competency_id,
            mission_id=execution.mission_id.value,
            extra_metadata={"execution_id": execution.execution_id.value},
        )
        return (evidence,)
