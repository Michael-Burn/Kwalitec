"""MissionExecution — runtime aggregate for student mission interaction.

Architecture Source
    PRD-001.5 Mission Execution Engine

Holds immutable execution state derived from a MissionPlan reference.
Never mutates the MissionPlan. Never estimates mastery. Never generates
recommendations or missions.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime

from application.education.mission_execution.enums import (
    ExecutionStatus,
    StepOutcome,
)
from application.education.mission_execution.errors import (
    MissionExecutionInvariantViolation,
)
from application.education.mission_execution.ids import ExecutionId, StudentId
from application.education.mission_execution.models.confidence_record import (
    ConfidenceRecord,
)
from application.education.mission_execution.models.execution_metrics import (
    ExecutionMetrics,
)
from application.education.mission_execution.models.execution_progress import (
    ExecutionProgress,
)
from application.education.mission_execution.models.execution_snapshot import (
    ExecutionSnapshot,
)
from application.education.mission_execution.models.execution_summary import (
    ExecutionSummary,
)
from application.education.mission_execution.models.reflection_record import (
    ReflectionRecord,
)
from application.education.mission_execution.rules.metrics_rules import MetricsRules
from application.education.mission_execution.rules.progress_rules import ProgressRules
from application.education.mission_generation.ids import (
    MissionId,
    MissionPlanId,
    MissionStepId,
)
from application.education.mission_generation.models.mission import Mission
from application.education.mission_generation.models.mission_plan import MissionPlan
from application.education.mission_generation.models.mission_step import MissionStep

_TERMINAL = frozenset(
    {
        ExecutionStatus.COMPLETED,
        ExecutionStatus.ABANDONED,
        ExecutionStatus.EXPIRED,
    }
)

_ACTIVE = frozenset(
    {
        ExecutionStatus.STARTED,
        ExecutionStatus.RESUMED,
    }
)


@dataclass(frozen=True, slots=True)
class MissionExecution:
    """Immutable runtime aggregate for executing one Mission from a plan.

    Progress derives only from completed steps. Confidence history is
    preserved. Reflection history is append-only. The referenced
    ``MissionPlan`` / ``Mission`` are never mutated.
    """

    execution_id: ExecutionId
    mission_id: MissionId
    plan_id: MissionPlanId
    student_id: StudentId
    status: ExecutionStatus
    mission: Mission
    plan: MissionPlan
    started_at: datetime | None = None
    finished_at: datetime | None = None
    pause_started_at: datetime | None = None
    last_active_at: datetime | None = None
    paused_duration_seconds: float = 0.0
    elapsed_study_time_seconds: float = 0.0
    completed_step_ids: tuple[MissionStepId, ...] = ()
    skipped_step_ids: tuple[MissionStepId, ...] = ()
    current_step_id: MissionStepId | None = None
    confidence_history: tuple[ConfidenceRecord, ...] = ()
    reflection_history: tuple[ReflectionRecord, ...] = ()
    event_sequence: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.execution_id, ExecutionId):
            raise MissionExecutionInvariantViolation(
                "execution_id must be an ExecutionId",
                invariant="MissionExecution.execution_id.type",
            )
        if not isinstance(self.mission_id, MissionId):
            raise MissionExecutionInvariantViolation(
                "mission_id must be a MissionId",
                invariant="MissionExecution.mission_id.type",
            )
        if not isinstance(self.plan_id, MissionPlanId):
            raise MissionExecutionInvariantViolation(
                "plan_id must be a MissionPlanId",
                invariant="MissionExecution.plan_id.type",
            )
        if not isinstance(self.student_id, StudentId):
            raise MissionExecutionInvariantViolation(
                "student_id must be a StudentId",
                invariant="MissionExecution.student_id.type",
            )
        if not isinstance(self.status, ExecutionStatus):
            raise MissionExecutionInvariantViolation(
                "status must be an ExecutionStatus",
                invariant="MissionExecution.status.type",
            )
        if not isinstance(self.mission, Mission):
            raise MissionExecutionInvariantViolation(
                "mission must be a Mission",
                invariant="MissionExecution.mission.type",
            )
        if not isinstance(self.plan, MissionPlan):
            raise MissionExecutionInvariantViolation(
                "plan must be a MissionPlan",
                invariant="MissionExecution.plan.type",
            )
        if self.mission.mission_id != self.mission_id:
            raise MissionExecutionInvariantViolation(
                "mission.mission_id must match mission_id",
                invariant="MissionExecution.mission_id.consistent",
            )
        if self.plan.plan_id != self.plan_id:
            raise MissionExecutionInvariantViolation(
                "plan.plan_id must match plan_id",
                invariant="MissionExecution.plan_id.consistent",
            )
        if self.plan.student_id != self.student_id.value:
            raise MissionExecutionInvariantViolation(
                "plan.student_id must match student_id",
                invariant="MissionExecution.student_id.consistent",
            )
        plan_mission_ids = {m.mission_id for m in self.plan.missions}
        if self.mission_id not in plan_mission_ids:
            raise MissionExecutionInvariantViolation(
                "mission must belong to the referenced MissionPlan",
                invariant="MissionExecution.mission.in_plan",
            )
        object.__setattr__(
            self, "completed_step_ids", tuple(self.completed_step_ids)
        )
        object.__setattr__(self, "skipped_step_ids", tuple(self.skipped_step_ids))
        object.__setattr__(
            self, "confidence_history", tuple(self.confidence_history)
        )
        object.__setattr__(
            self, "reflection_history", tuple(self.reflection_history)
        )
        if isinstance(self.event_sequence, bool) or not isinstance(
            self.event_sequence, int
        ):
            raise MissionExecutionInvariantViolation(
                "event_sequence must be an integer",
                invariant="MissionExecution.event_sequence.type",
            )
        if self.event_sequence < 0:
            raise MissionExecutionInvariantViolation(
                "event_sequence must be >= 0",
                invariant="MissionExecution.event_sequence.non_negative",
            )
        for duration_name in (
            "paused_duration_seconds",
            "elapsed_study_time_seconds",
        ):
            value = getattr(self, duration_name)
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise MissionExecutionInvariantViolation(
                    f"{duration_name} must be a real number",
                    invariant=f"MissionExecution.{duration_name}.type",
                )
            if float(value) < 0:
                raise MissionExecutionInvariantViolation(
                    f"{duration_name} must be >= 0",
                    invariant=f"MissionExecution.{duration_name}.non_negative",
                )

    # --- factories ----------------------------------------------------------

    @classmethod
    def plan_execution(
        cls,
        *,
        execution_id: ExecutionId,
        mission_plan: MissionPlan,
        mission_id: MissionId,
    ) -> MissionExecution:
        """Create a PLANNED execution referencing an immutable MissionPlan."""
        mission = cls._require_mission(mission_plan, mission_id)
        current = mission.steps[0].step_id if mission.steps else None
        return cls(
            execution_id=execution_id,
            mission_id=mission_id,
            plan_id=mission_plan.plan_id,
            student_id=StudentId(mission_plan.student_id),
            status=ExecutionStatus.PLANNED,
            mission=mission,
            plan=mission_plan,
            current_step_id=current,
        )

    @staticmethod
    def _require_mission(
        mission_plan: MissionPlan, mission_id: MissionId
    ) -> Mission:
        for mission in mission_plan.missions:
            if mission.mission_id == mission_id:
                return mission
        raise MissionExecutionInvariantViolation(
            f"mission {mission_id} not found in plan {mission_plan.plan_id}",
            invariant="MissionExecution.mission.not_found",
        )

    # --- derived views ------------------------------------------------------

    @property
    def progress(self) -> ExecutionProgress:
        return ProgressRules.build_progress(
            mission=self.mission,
            completed_step_ids=self.completed_step_ids,
            skipped_step_ids=self.skipped_step_ids,
            current_step_id=self.current_step_id,
        )

    @property
    def metrics(self) -> ExecutionMetrics:
        return MetricsRules.build_metrics(
            mission=self.mission,
            completed_step_ids=self.completed_step_ids,
            skipped_step_ids=self.skipped_step_ids,
            elapsed_study_time_seconds=self.elapsed_study_time_seconds,
            paused_duration_seconds=self.paused_duration_seconds,
            started_at=self.started_at,
            finished_at=self.finished_at,
            confidence_history=self.confidence_history,
            reflection_history=self.reflection_history,
        )

    @property
    def summary(self) -> ExecutionSummary:
        progress = self.progress
        return ExecutionSummary(
            execution_id=self.execution_id,
            mission_id=self.mission_id,
            student_id=self.student_id.value,
            status=self.status,
            completed_steps=progress.completed_count,
            skipped_steps=progress.skipped_count,
            total_steps=progress.total_steps,
            completion_percentage=progress.completion_percentage,
            elapsed_study_time_seconds=self.elapsed_study_time_seconds,
            reflection_count=len(self.reflection_history),
            confidence_count=len(self.confidence_history),
            started_at=self.started_at,
            finished_at=self.finished_at,
        )

    @property
    def confidence(self) -> ConfidenceRecord | None:
        if not self.confidence_history:
            return None
        return self.confidence_history[-1]

    @property
    def reflection(self) -> ReflectionRecord | None:
        if not self.reflection_history:
            return None
        return self.reflection_history[-1]

    @property
    def current_step(self) -> MissionStep | None:
        if self.current_step_id is None:
            return None
        for step in self.mission.steps:
            if step.step_id == self.current_step_id:
                return step
        return None

    def is_terminal(self) -> bool:
        return self.status in _TERMINAL

    def is_active(self) -> bool:
        return self.status in _ACTIVE

    def produce_snapshot(self, *, captured_at: datetime) -> ExecutionSnapshot:
        return ExecutionSnapshot(
            execution_id=self.execution_id,
            mission_id=self.mission_id,
            plan_id=self.plan_id,
            student_id=self.student_id.value,
            status=self.status,
            mission=self.mission,
            progress=self.progress,
            metrics=self.metrics,
            summary=self.summary,
            confidence_history=self.confidence_history,
            reflection_history=self.reflection_history,
            started_at=self.started_at,
            finished_at=self.finished_at,
            captured_at=captured_at,
        )

    def next_event_sequence(self) -> int:
        return self.event_sequence + 1

    def with_updates(self, **kwargs: object) -> MissionExecution:
        """Return a new MissionExecution with selected fields replaced."""
        return replace(self, **kwargs)

    def step_outcome(self, step_id: MissionStepId) -> StepOutcome:
        if step_id in self.completed_step_ids:
            return StepOutcome.COMPLETED
        if step_id in self.skipped_step_ids:
            return StepOutcome.SKIPPED
        return StepOutcome.PENDING

    def find_step(self, step_id: MissionStepId) -> MissionStep | None:
        for step in self.mission.steps:
            if step.step_id == step_id:
                return step
        return None
