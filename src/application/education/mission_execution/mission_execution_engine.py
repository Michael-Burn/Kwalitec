"""MissionExecutionEngine — runtime layer of the Education OS.

Architecture Source
    PRD-001.5 Mission Execution Engine

Executes MissionPlans and converts execution events into structured
EducationalEvidence.

Must not:
    - estimate mastery
    - generate recommendations
    - generate missions
    - mutate MissionPlan
    - mutate StudentEducationalState
    - persist, call Flask/SQLAlchemy, invoke AI, or read wall-clock time

Every method is a pure function of its explicit, caller-supplied inputs —
including ``at`` timestamps. Invalid lifecycle transitions return
``ExecutionCommandResult`` failures; they are never raised.
"""

from __future__ import annotations

from datetime import datetime

from application.education.mission_execution.enums import ExecutionStatus
from application.education.mission_execution.errors import MissionExecutionError
from application.education.mission_execution.events import (
    ConfidenceRecorded,
    MissionAbandoned,
    MissionCompleted,
    MissionExpired,
    MissionPaused,
    MissionResumed,
    MissionStarted,
    ReflectionRecorded,
    StepCompleted,
    StepSkipped,
)
from application.education.mission_execution.execution_command_result import (
    ExecutionCommandResult,
)
from application.education.mission_execution.ids import ExecutionId
from application.education.mission_execution.models.confidence_record import (
    ConfidenceRecord,
)
from application.education.mission_execution.models.execution_snapshot import (
    ExecutionSnapshot,
)
from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)
from application.education.mission_execution.models.reflection_record import (
    ReflectionRecord,
)
from application.education.mission_execution.rules.evidence_mapping_rules import (
    EvidenceMappingRules,
)
from application.education.mission_execution.rules.lifecycle_rules import (
    LifecycleRules,
)
from application.education.mission_execution.rules.metrics_rules import MetricsRules
from application.education.mission_execution.rules.progress_rules import ProgressRules
from application.education.mission_generation.ids import MissionId, MissionStepId
from application.education.mission_generation.models.mission_plan import MissionPlan
from domain.education.foundation.enums import ConfidenceLevel


class MissionExecutionEngine:
    """Deterministic engine managing student interaction with mission work.

    Pure application composition. Domain EducationalEvidence factories
    produce evidence; this engine only orchestrates lifecycle, metrics,
    events, and evidence mapping.
    """

    # --- lifecycle ----------------------------------------------------------

    @staticmethod
    def start_execution(
        mission_plan: MissionPlan,
        mission_id: MissionId,
        *,
        execution_id: ExecutionId,
        at: datetime,
        execution: MissionExecution | None = None,
    ) -> ExecutionCommandResult:
        """Start execution for a mission in a plan (PLANNED → STARTED).

        When ``execution`` is omitted, a PLANNED aggregate is created first.
        When provided, it must already be PLANNED.
        """
        if execution is None:
            current = MissionExecution.plan_execution(
                execution_id=execution_id,
                mission_plan=mission_plan,
                mission_id=mission_id,
            )
        else:
            err = MissionExecutionEngine._guard_identity(
                execution, execution_id=execution_id, mission_id=mission_id
            )
            if err is not None:
                return ExecutionCommandResult.failure(err)
            current = execution

        transition_error = LifecycleRules.validate(
            current.status, ExecutionStatus.STARTED, attempted="start"
        )
        if transition_error is not None:
            return ExecutionCommandResult.failure(transition_error)

        sequence = current.next_event_sequence()
        updated = current.with_updates(
            status=ExecutionStatus.STARTED,
            started_at=at,
            last_active_at=at,
            event_sequence=sequence,
        )
        event = MissionStarted(
            execution_id=updated.execution_id,
            mission_id=updated.mission_id,
            student_id=updated.student_id.value,
            occurred_at=at,
            sequence=sequence,
        )
        evidence = EvidenceMappingRules.map_event(event, updated)
        return ExecutionCommandResult.success(
            updated, events=(event,), evidence=evidence
        )

    @staticmethod
    def pause_execution(
        execution: MissionExecution, *, at: datetime
    ) -> ExecutionCommandResult:
        """Pause an active execution (STARTED|RESUMED → PAUSED)."""
        transition_error = LifecycleRules.validate(
            execution.status, ExecutionStatus.PAUSED, attempted="pause"
        )
        if transition_error is not None:
            return ExecutionCommandResult.failure(transition_error)

        delta = MetricsRules.elapsed_delta_seconds(
            last_active_at=execution.last_active_at, at=at
        )
        sequence = execution.next_event_sequence()
        updated = execution.with_updates(
            status=ExecutionStatus.PAUSED,
            elapsed_study_time_seconds=execution.elapsed_study_time_seconds + delta,
            pause_started_at=at,
            last_active_at=None,
            event_sequence=sequence,
        )
        event = MissionPaused(
            execution_id=updated.execution_id,
            mission_id=updated.mission_id,
            student_id=updated.student_id.value,
            occurred_at=at,
            sequence=sequence,
        )
        evidence = EvidenceMappingRules.map_event(event, updated)
        return ExecutionCommandResult.success(
            updated, events=(event,), evidence=evidence
        )

    @staticmethod
    def resume_execution(
        execution: MissionExecution, *, at: datetime
    ) -> ExecutionCommandResult:
        """Resume a paused execution (PAUSED → RESUMED)."""
        transition_error = LifecycleRules.validate(
            execution.status, ExecutionStatus.RESUMED, attempted="resume"
        )
        if transition_error is not None:
            return ExecutionCommandResult.failure(transition_error)

        pause_delta = 0.0
        if execution.pause_started_at is not None:
            pause_delta = max(
                0.0, (at - execution.pause_started_at).total_seconds()
            )
        sequence = execution.next_event_sequence()
        updated = execution.with_updates(
            status=ExecutionStatus.RESUMED,
            paused_duration_seconds=execution.paused_duration_seconds + pause_delta,
            pause_started_at=None,
            last_active_at=at,
            event_sequence=sequence,
        )
        event = MissionResumed(
            execution_id=updated.execution_id,
            mission_id=updated.mission_id,
            student_id=updated.student_id.value,
            occurred_at=at,
            sequence=sequence,
        )
        evidence = EvidenceMappingRules.map_event(event, updated)
        return ExecutionCommandResult.success(
            updated, events=(event,), evidence=evidence
        )

    @staticmethod
    def complete_execution(
        execution: MissionExecution, *, at: datetime
    ) -> ExecutionCommandResult:
        """Complete an execution (STARTED|PAUSED|RESUMED → COMPLETED)."""
        transition_error = LifecycleRules.validate(
            execution.status, ExecutionStatus.COMPLETED, attempted="complete"
        )
        if transition_error is not None:
            return ExecutionCommandResult.failure(transition_error)

        updated = MissionExecutionEngine._finalise_timing(execution, at=at)
        sequence = updated.next_event_sequence()
        updated = updated.with_updates(
            status=ExecutionStatus.COMPLETED,
            finished_at=at,
            event_sequence=sequence,
            pause_started_at=None,
            last_active_at=None,
        )
        event = MissionCompleted(
            execution_id=updated.execution_id,
            mission_id=updated.mission_id,
            student_id=updated.student_id.value,
            occurred_at=at,
            sequence=sequence,
        )
        evidence = EvidenceMappingRules.map_event(event, updated)
        return ExecutionCommandResult.success(
            updated, events=(event,), evidence=evidence
        )

    @staticmethod
    def abandon_execution(
        execution: MissionExecution, *, at: datetime
    ) -> ExecutionCommandResult:
        """Abandon an execution (STARTED|PAUSED|RESUMED → ABANDONED)."""
        transition_error = LifecycleRules.validate(
            execution.status, ExecutionStatus.ABANDONED, attempted="abandon"
        )
        if transition_error is not None:
            return ExecutionCommandResult.failure(transition_error)

        updated = MissionExecutionEngine._finalise_timing(execution, at=at)
        sequence = updated.next_event_sequence()
        updated = updated.with_updates(
            status=ExecutionStatus.ABANDONED,
            finished_at=at,
            event_sequence=sequence,
            pause_started_at=None,
            last_active_at=None,
        )
        event = MissionAbandoned(
            execution_id=updated.execution_id,
            mission_id=updated.mission_id,
            student_id=updated.student_id.value,
            occurred_at=at,
            sequence=sequence,
        )
        evidence = EvidenceMappingRules.map_event(event, updated)
        return ExecutionCommandResult.success(
            updated, events=(event,), evidence=evidence
        )

    @staticmethod
    def expire_execution(
        execution: MissionExecution, *, at: datetime
    ) -> ExecutionCommandResult:
        """Expire an execution (non-terminal → EXPIRED)."""
        transition_error = LifecycleRules.validate(
            execution.status, ExecutionStatus.EXPIRED, attempted="expire"
        )
        if transition_error is not None:
            return ExecutionCommandResult.failure(transition_error)

        updated = MissionExecutionEngine._finalise_timing(execution, at=at)
        sequence = updated.next_event_sequence()
        updated = updated.with_updates(
            status=ExecutionStatus.EXPIRED,
            finished_at=at,
            event_sequence=sequence,
            pause_started_at=None,
            last_active_at=None,
        )
        event = MissionExpired(
            execution_id=updated.execution_id,
            mission_id=updated.mission_id,
            student_id=updated.student_id.value,
            occurred_at=at,
            sequence=sequence,
        )
        evidence = EvidenceMappingRules.map_event(event, updated)
        return ExecutionCommandResult.success(
            updated, events=(event,), evidence=evidence
        )

    # --- steps --------------------------------------------------------------

    @staticmethod
    def complete_step(
        execution: MissionExecution,
        step_id: MissionStepId,
        *,
        at: datetime,
    ) -> ExecutionCommandResult:
        """Mark a step completed. Progress derives from completed steps only."""
        active_error = MissionExecutionEngine._require_active_work(
            execution, attempted="complete_step"
        )
        if active_error is not None:
            return ExecutionCommandResult.failure(active_error)

        step_error = MissionExecutionEngine._require_pending_step(
            execution, step_id, attempted="complete_step"
        )
        if step_error is not None:
            return ExecutionCommandResult.failure(step_error)

        completed = execution.completed_step_ids + (step_id,)
        current = ProgressRules.next_current_step(
            mission=execution.mission,
            completed_step_ids=completed,
            skipped_step_ids=execution.skipped_step_ids,
        )
        sequence = execution.next_event_sequence()
        updated = execution.with_updates(
            completed_step_ids=completed,
            current_step_id=current,
            event_sequence=sequence,
        )
        # Accrue study time while active.
        if execution.is_active() and execution.last_active_at is not None:
            delta = MetricsRules.elapsed_delta_seconds(
                last_active_at=execution.last_active_at, at=at
            )
            updated = updated.with_updates(
                elapsed_study_time_seconds=execution.elapsed_study_time_seconds
                + delta,
                last_active_at=at,
            )
        event = StepCompleted(
            execution_id=updated.execution_id,
            mission_id=updated.mission_id,
            student_id=updated.student_id.value,
            occurred_at=at,
            sequence=sequence,
            status_after=updated.status,
            step_id=step_id,
        )
        evidence = EvidenceMappingRules.map_event(event, updated)
        return ExecutionCommandResult.success(
            updated, events=(event,), evidence=evidence
        )

    @staticmethod
    def skip_step(
        execution: MissionExecution,
        step_id: MissionStepId,
        *,
        at: datetime,
    ) -> ExecutionCommandResult:
        """Skip a pending step. Skipped steps do not count as progress."""
        active_error = MissionExecutionEngine._require_active_work(
            execution, attempted="skip_step"
        )
        if active_error is not None:
            return ExecutionCommandResult.failure(active_error)

        step_error = MissionExecutionEngine._require_pending_step(
            execution, step_id, attempted="skip_step"
        )
        if step_error is not None:
            return ExecutionCommandResult.failure(step_error)

        skipped = execution.skipped_step_ids + (step_id,)
        current = ProgressRules.next_current_step(
            mission=execution.mission,
            completed_step_ids=execution.completed_step_ids,
            skipped_step_ids=skipped,
        )
        sequence = execution.next_event_sequence()
        updated = execution.with_updates(
            skipped_step_ids=skipped,
            current_step_id=current,
            event_sequence=sequence,
        )
        if execution.is_active() and execution.last_active_at is not None:
            delta = MetricsRules.elapsed_delta_seconds(
                last_active_at=execution.last_active_at, at=at
            )
            updated = updated.with_updates(
                elapsed_study_time_seconds=execution.elapsed_study_time_seconds
                + delta,
                last_active_at=at,
            )
        event = StepSkipped(
            execution_id=updated.execution_id,
            mission_id=updated.mission_id,
            student_id=updated.student_id.value,
            occurred_at=at,
            sequence=sequence,
            status_after=updated.status,
            step_id=step_id,
        )
        evidence = EvidenceMappingRules.map_event(event, updated)
        return ExecutionCommandResult.success(
            updated, events=(event,), evidence=evidence
        )

    # --- observations -------------------------------------------------------

    @staticmethod
    def record_confidence(
        execution: MissionExecution,
        level: ConfidenceLevel,
        *,
        at: datetime,
        step_id: MissionStepId | None = None,
        note: str | None = None,
    ) -> ExecutionCommandResult:
        """Append a confidence observation (history preserved)."""
        active_error = MissionExecutionEngine._require_active_work(
            execution, attempted="record_confidence"
        )
        if active_error is not None:
            return ExecutionCommandResult.failure(active_error)
        if level is ConfidenceLevel.UNKNOWN:
            return ExecutionCommandResult.failure(
                MissionExecutionError(
                    code="invalid_confidence",
                    message="confidence level must not be UNKNOWN",
                    from_status=execution.status.value,
                    attempted="record_confidence",
                )
            )

        record = ConfidenceRecord(
            level=level,
            recorded_at=at,
            step_id=step_id.value if step_id else None,
            note=note,
        )
        sequence = execution.next_event_sequence()
        updated = execution.with_updates(
            confidence_history=execution.confidence_history + (record,),
            event_sequence=sequence,
        )
        event = ConfidenceRecorded(
            execution_id=updated.execution_id,
            mission_id=updated.mission_id,
            student_id=updated.student_id.value,
            occurred_at=at,
            sequence=sequence,
            status_after=updated.status,
            level=level,
            step_id=step_id,
        )
        evidence = EvidenceMappingRules.map_event(event, updated)
        return ExecutionCommandResult.success(
            updated, events=(event,), evidence=evidence
        )

    @staticmethod
    def record_reflection(
        execution: MissionExecution,
        text: str,
        *,
        at: datetime,
        step_id: MissionStepId | None = None,
    ) -> ExecutionCommandResult:
        """Append a reflection observation (append-only history)."""
        active_error = MissionExecutionEngine._require_active_work(
            execution, attempted="record_reflection"
        )
        if active_error is not None:
            return ExecutionCommandResult.failure(active_error)
        cleaned = (text or "").strip()
        if not cleaned:
            return ExecutionCommandResult.failure(
                MissionExecutionError(
                    code="invalid_reflection",
                    message="reflection text must be non-empty",
                    from_status=execution.status.value,
                    attempted="record_reflection",
                )
            )

        record = ReflectionRecord(
            text=cleaned,
            recorded_at=at,
            step_id=step_id.value if step_id else None,
        )
        sequence = execution.next_event_sequence()
        updated = execution.with_updates(
            reflection_history=execution.reflection_history + (record,),
            event_sequence=sequence,
        )
        event = ReflectionRecorded(
            execution_id=updated.execution_id,
            mission_id=updated.mission_id,
            student_id=updated.student_id.value,
            occurred_at=at,
            sequence=sequence,
            status_after=updated.status,
            text=cleaned,
            step_id=step_id,
        )
        evidence = EvidenceMappingRules.map_event(event, updated)
        return ExecutionCommandResult.success(
            updated, events=(event,), evidence=evidence
        )

    @staticmethod
    def produce_snapshot(
        execution: MissionExecution, *, at: datetime
    ) -> ExecutionSnapshot:
        """Produce an immutable snapshot of the current execution."""
        return execution.produce_snapshot(captured_at=at)

    # --- helpers ------------------------------------------------------------

    @staticmethod
    def _finalise_timing(
        execution: MissionExecution, *, at: datetime
    ) -> MissionExecution:
        elapsed = execution.elapsed_study_time_seconds
        paused = execution.paused_duration_seconds
        if execution.is_active() and execution.last_active_at is not None:
            elapsed += MetricsRules.elapsed_delta_seconds(
                last_active_at=execution.last_active_at, at=at
            )
        elif (
            execution.status is ExecutionStatus.PAUSED
            and execution.pause_started_at is not None
        ):
            paused += max(0.0, (at - execution.pause_started_at).total_seconds())
        return execution.with_updates(
            elapsed_study_time_seconds=elapsed,
            paused_duration_seconds=paused,
        )

    @staticmethod
    def _require_active_work(
        execution: MissionExecution, *, attempted: str
    ) -> MissionExecutionError | None:
        if execution.is_terminal():
            return MissionExecutionError(
                code="execution_terminal",
                message=(
                    f"Cannot {attempted}: execution is already "
                    f"{execution.status.value}"
                ),
                from_status=execution.status.value,
                attempted=attempted,
            )
        if not LifecycleRules.requires_active_work(execution.status):
            return MissionExecutionError(
                code="execution_not_active",
                message=(
                    f"Cannot {attempted}: execution status "
                    f"{execution.status.value} does not allow work recording"
                ),
                from_status=execution.status.value,
                attempted=attempted,
            )
        return None

    @staticmethod
    def _require_pending_step(
        execution: MissionExecution,
        step_id: MissionStepId,
        *,
        attempted: str,
    ) -> MissionExecutionError | None:
        if execution.find_step(step_id) is None:
            return MissionExecutionError(
                code="step_not_found",
                message=f"Step {step_id.value} not found in mission",
                from_status=execution.status.value,
                attempted=attempted,
            )
        if step_id in execution.completed_step_ids:
            return MissionExecutionError(
                code="step_already_completed",
                message=f"Step {step_id.value} is already completed",
                from_status=execution.status.value,
                attempted=attempted,
            )
        if step_id in execution.skipped_step_ids:
            return MissionExecutionError(
                code="step_already_skipped",
                message=f"Step {step_id.value} is already skipped",
                from_status=execution.status.value,
                attempted=attempted,
            )
        return None

    @staticmethod
    def _guard_identity(
        execution: MissionExecution,
        *,
        execution_id: ExecutionId,
        mission_id: MissionId,
    ) -> MissionExecutionError | None:
        if execution.execution_id != execution_id:
            return MissionExecutionError(
                code="execution_id_mismatch",
                message="Provided execution_id does not match execution",
                attempted="start",
            )
        if execution.mission_id != mission_id:
            return MissionExecutionError(
                code="mission_id_mismatch",
                message="Provided mission_id does not match execution",
                attempted="start",
            )
        return None
