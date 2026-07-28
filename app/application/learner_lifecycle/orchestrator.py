"""Learner Lifecycle Orchestrator — coordinates Educational Intelligence (LP-001).

Automates onboarding and evidence-driven refresh by invoking existing
EI-004 / EI-005 / EI-006 / EI-007 / EX-001 services in deterministic order.

Contains no educational reasoning, Twin inference rules, decision ranking,
or Experience Model presentation logic. Runtime Integration remains the
sole student-facing Preferred Authority read path.
"""

from __future__ import annotations

import logging
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from time import perf_counter
from typing import Any

from app.application.educational_experience_engine.experience_service import (
    ExperienceTransformationService,
)
from app.application.educational_reasoning_engine.reasoning_service import (
    DecisionReasoningService,
)
from app.application.learner_lifecycle.checkpoint_store import LifecycleCheckpointStore
from app.application.learner_lifecycle.consistency import LifecycleConsistencyService
from app.application.learner_lifecycle.dto import (
    ConsistencyReport,
    LifecycleResult,
    StageExecutionRecord,
)
from app.application.learner_lifecycle.exceptions import (
    LifecycleRetryExhaustedError,
    LifecycleStageError,
)
from app.application.learner_lifecycle.retry import LifecycleRetryPolicy
from app.application.learner_lifecycle.stages import (
    LifecycleStage,
    OperationStatus,
    OperationType,
)
from app.application.learner_lifecycle.versions import ORCHESTRATOR_VERSION
from app.application.learning_evidence.recording_service import (
    EvidenceRecordingService,
)
from app.application.student_curriculum_binding.binding_service import (
    StudentCurriculumBindingService,
)
from app.application.twin_inference.inference_service import BeliefInferenceService

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class LearnerLifecycleOrchestrator:
    """Coordinate existing Educational Intelligence capabilities for learners.

    Responsibilities:
    - Student onboarding pipeline (SCI → beliefs → decisions → experience)
    - Evidence refresh pipeline (twin rebuild → decisions → experience)
    - Technical retry and checkpointed recovery

    Non-responsibilities:
    - Educational reasoning / inference / ranking / presentation math
    - Bypassing Runtime Integration for student-facing delivery
    """

    version = ORCHESTRATOR_VERSION

    def __init__(
        self,
        *,
        binding: StudentCurriculumBindingService | None = None,
        evidence: EvidenceRecordingService | None = None,
        beliefs: BeliefInferenceService | None = None,
        decisions: DecisionReasoningService | None = None,
        experience: ExperienceTransformationService | None = None,
        checkpoints: LifecycleCheckpointStore | None = None,
        consistency: LifecycleConsistencyService | None = None,
        retry_policy: LifecycleRetryPolicy | None = None,
    ) -> None:
        self._binding = binding or StudentCurriculumBindingService()
        self._evidence = evidence or EvidenceRecordingService()
        self._beliefs = beliefs or BeliefInferenceService()
        self._decisions = decisions or DecisionReasoningService()
        self._experience = experience or ExperienceTransformationService()
        self._checkpoints = checkpoints or LifecycleCheckpointStore()
        self._consistency = consistency or LifecycleConsistencyService()
        self._retry = retry_policy or LifecycleRetryPolicy.technical()

    def onboard_student(
        self,
        *,
        student_id: int,
        edition_id: str,
        subject_code: str | None = None,
        as_of: datetime | None = None,
        correlation_id: str | None = None,
        operation_id: str | None = None,
    ) -> LifecycleResult:
        """Run the Student Onboarding Pipeline.

        Sequence (deterministic, idempotent):
          1. create Student Curriculum Instance + bind Published Curriculum
          2. initialise node state
          3. generate initial Twin Beliefs
          4. generate initial Educational Decisions
          5. generate Experience Models
        """
        when = as_of if as_of is not None else _utc_now()
        when = when.replace(tzinfo=None) if when.tzinfo else when
        op_id = (operation_id or "").strip() or f"llp-{uuid.uuid4().hex[:16]}"
        corr = (correlation_id or "").strip() or None

        self._checkpoints.start(
            operation_id=op_id,
            operation_type=OperationType.ONBOARD,
            student_id=student_id,
            correlation_id=corr,
        )

        stage_records: list[StageExecutionRecord] = []
        completed: list[LifecycleStage] = []
        binding_result = None
        beliefs_result = None
        decisions_result = None
        experience_result = None
        instance_id: str | None = None

        try:
            binding_result = self._run_stage(
                LifecycleStage.BIND_INSTANCE,
                operation_id=op_id,
                records=stage_records,
                call=lambda: self._binding.create_instance(
                    student_id=student_id,
                    edition_id=edition_id,
                    subject_code=subject_code,
                ),
            )
            instance_id = binding_result.instance.instance_id
            self._checkpoints.mark_stage_complete(
                op_id,
                LifecycleStage.BIND_INSTANCE,
                instance_id=instance_id,
                student_id=student_id,
            )
            completed.append(LifecycleStage.BIND_INSTANCE)

            self._run_stage(
                LifecycleStage.INITIALISE_NODE_STATE,
                operation_id=op_id,
                records=stage_records,
                call=lambda: self._binding.initialise_node_states(instance_id),
            )
            self._checkpoints.mark_stage_complete(
                op_id, LifecycleStage.INITIALISE_NODE_STATE, instance_id=instance_id
            )
            completed.append(LifecycleStage.INITIALISE_NODE_STATE)

            beliefs_result, decisions_result, experience_result = (
                self._refresh_derived_state(
                    instance_id=instance_id,
                    operation_id=op_id,
                    when=when,
                    stage_records=stage_records,
                    completed=completed,
                )
            )
        except LifecycleStageError as exc:
            self._checkpoints.mark_failed(
                op_id,
                stage=LifecycleStage(exc.stage),
                cause=str(exc),
                instance_id=instance_id,
            )
            logger.warning(
                "lifecycle onboard failed operation_id=%s stage=%s cause=%s",
                op_id,
                exc.stage,
                exc,
            )
            return LifecycleResult(
                operation_id=op_id,
                operation_type=OperationType.ONBOARD,
                status=OperationStatus.FAILED,
                student_id=student_id,
                instance_id=instance_id,
                correlation_id=corr,
                binding=binding_result,
                beliefs=beliefs_result,
                decisions=decisions_result,
                experience=experience_result,
                stages=tuple(stage_records),
                completed_stages=tuple(completed),
                failed_stage=LifecycleStage(exc.stage),
                failure_cause=str(exc),
            )

        self._checkpoints.mark_completed(op_id)
        return LifecycleResult(
            operation_id=op_id,
            operation_type=OperationType.ONBOARD,
            status=OperationStatus.COMPLETED,
            student_id=student_id,
            instance_id=instance_id,
            correlation_id=corr,
            binding=binding_result,
            beliefs=beliefs_result,
            decisions=decisions_result,
            experience=experience_result,
            stages=tuple(stage_records),
            completed_stages=tuple(completed),
        )

    def process_evidence(
        self,
        *,
        instance_id: str,
        node_stable_id: str,
        evidence_type: str,
        source: str,
        occurred_at: datetime | None = None,
        metadata: dict[str, Any] | None = None,
        corrects_evidence_id: str | None = None,
        as_of: datetime | None = None,
        correlation_id: str | None = None,
        operation_id: str | None = None,
    ) -> LifecycleResult:
        """Record Learning Evidence then refresh derived EI state.

        Sequence (deterministic, idempotent for derived stages):
          1. record evidence (EI-005)
          2. twin inference rebuild (EI-006)
          3. regenerate Educational Decisions (EI-007)
          4. regenerate Experience Models (EX-001)
        """
        when = as_of if as_of is not None else _utc_now()
        when = when.replace(tzinfo=None) if when.tzinfo else when
        op_id = (operation_id or "").strip() or f"llp-{uuid.uuid4().hex[:16]}"
        corr = (correlation_id or "").strip() or None

        self._checkpoints.start(
            operation_id=op_id,
            operation_type=OperationType.EVIDENCE_REFRESH,
            instance_id=instance_id,
            correlation_id=corr,
        )

        stage_records: list[StageExecutionRecord] = []
        completed: list[LifecycleStage] = []
        evidence_result = None
        beliefs_result = None
        decisions_result = None
        experience_result = None

        try:
            evidence_result = self._run_stage(
                LifecycleStage.RECORD_EVIDENCE,
                operation_id=op_id,
                records=stage_records,
                call=lambda: self._evidence.record_evidence(
                    instance_id=instance_id,
                    node_stable_id=node_stable_id,
                    evidence_type=evidence_type,
                    source=source,
                    occurred_at=occurred_at,
                    metadata=metadata,
                    corrects_evidence_id=corrects_evidence_id,
                ),
            )
            self._checkpoints.mark_stage_complete(
                op_id, LifecycleStage.RECORD_EVIDENCE, instance_id=instance_id
            )
            completed.append(LifecycleStage.RECORD_EVIDENCE)

            beliefs_result, decisions_result, experience_result = (
                self._refresh_derived_state(
                    instance_id=instance_id,
                    operation_id=op_id,
                    when=when,
                    stage_records=stage_records,
                    completed=completed,
                )
            )
        except LifecycleStageError as exc:
            self._checkpoints.mark_failed(
                op_id,
                stage=LifecycleStage(exc.stage),
                cause=str(exc),
                instance_id=instance_id,
            )
            logger.warning(
                "lifecycle evidence failed operation_id=%s stage=%s cause=%s",
                op_id,
                exc.stage,
                exc,
            )
            return LifecycleResult(
                operation_id=op_id,
                operation_type=OperationType.EVIDENCE_REFRESH,
                status=OperationStatus.FAILED,
                student_id=None,
                instance_id=instance_id,
                correlation_id=corr,
                evidence=evidence_result,
                beliefs=beliefs_result,
                decisions=decisions_result,
                experience=experience_result,
                stages=tuple(stage_records),
                completed_stages=tuple(completed),
                failed_stage=LifecycleStage(exc.stage),
                failure_cause=str(exc),
            )

        self._checkpoints.mark_completed(op_id)
        return LifecycleResult(
            operation_id=op_id,
            operation_type=OperationType.EVIDENCE_REFRESH,
            status=OperationStatus.COMPLETED,
            student_id=None,
            instance_id=instance_id,
            correlation_id=corr,
            evidence=evidence_result,
            beliefs=beliefs_result,
            decisions=decisions_result,
            experience=experience_result,
            stages=tuple(stage_records),
            completed_stages=tuple(completed),
        )

    def refresh_after_evidence(
        self,
        instance_id: str,
        *,
        as_of: datetime | None = None,
        correlation_id: str | None = None,
        operation_id: str | None = None,
    ) -> LifecycleResult:
        """Rebuild derived EI state after evidence was already recorded."""
        when = as_of if as_of is not None else _utc_now()
        when = when.replace(tzinfo=None) if when.tzinfo else when
        op_id = (operation_id or "").strip() or f"llp-{uuid.uuid4().hex[:16]}"
        corr = (correlation_id or "").strip() or None

        self._checkpoints.start(
            operation_id=op_id,
            operation_type=OperationType.EVIDENCE_REFRESH,
            instance_id=instance_id,
            correlation_id=corr,
        )

        stage_records: list[StageExecutionRecord] = []
        completed: list[LifecycleStage] = []
        beliefs_result = None
        decisions_result = None
        experience_result = None

        try:
            beliefs_result, decisions_result, experience_result = (
                self._refresh_derived_state(
                    instance_id=instance_id,
                    operation_id=op_id,
                    when=when,
                    stage_records=stage_records,
                    completed=completed,
                )
            )
        except LifecycleStageError as exc:
            self._checkpoints.mark_failed(
                op_id,
                stage=LifecycleStage(exc.stage),
                cause=str(exc),
                instance_id=instance_id,
            )
            return LifecycleResult(
                operation_id=op_id,
                operation_type=OperationType.EVIDENCE_REFRESH,
                status=OperationStatus.FAILED,
                student_id=None,
                instance_id=instance_id,
                correlation_id=corr,
                beliefs=beliefs_result,
                decisions=decisions_result,
                experience=experience_result,
                stages=tuple(stage_records),
                completed_stages=tuple(completed),
                failed_stage=LifecycleStage(exc.stage),
                failure_cause=str(exc),
            )

        self._checkpoints.mark_completed(op_id)
        return LifecycleResult(
            operation_id=op_id,
            operation_type=OperationType.EVIDENCE_REFRESH,
            status=OperationStatus.COMPLETED,
            student_id=None,
            instance_id=instance_id,
            correlation_id=corr,
            beliefs=beliefs_result,
            decisions=decisions_result,
            experience=experience_result,
            stages=tuple(stage_records),
            completed_stages=tuple(completed),
        )

    def ensure_complete(
        self,
        instance_id: str,
        *,
        as_of: datetime | None = None,
        correlation_id: str | None = None,
        operation_id: str | None = None,
    ) -> LifecycleResult:
        """Bring an SCI to complete EI state if anything is missing.

        Idempotent. Re-invokes derived stages required for consistency.
        Always regenerates experience models when decisions exist or are rebuilt.
        """
        report = self._consistency.inspect(instance_id)
        when = as_of if as_of is not None else _utc_now()
        when = when.replace(tzinfo=None) if when.tzinfo else when
        op_id = (operation_id or "").strip() or f"llp-{uuid.uuid4().hex[:16]}"
        corr = (correlation_id or "").strip() or None

        self._checkpoints.start(
            operation_id=op_id,
            operation_type=OperationType.ENSURE,
            instance_id=instance_id,
            correlation_id=corr,
        )

        stage_records: list[StageExecutionRecord] = []
        completed: list[LifecycleStage] = []
        beliefs_result = None
        decisions_result = None
        experience_result = None

        try:
            if "node_states" in report.missing:
                self._run_stage(
                    LifecycleStage.INITIALISE_NODE_STATE,
                    operation_id=op_id,
                    records=stage_records,
                    call=lambda: self._binding.initialise_node_states(instance_id),
                )
                self._checkpoints.mark_stage_complete(
                    op_id,
                    LifecycleStage.INITIALISE_NODE_STATE,
                    instance_id=instance_id,
                )
                completed.append(LifecycleStage.INITIALISE_NODE_STATE)

            need_beliefs = "twin_beliefs" in report.missing
            need_decisions = "educational_decisions" in report.missing
            if need_beliefs or need_decisions or not report.is_complete:
                beliefs_result, decisions_result, experience_result = (
                    self._refresh_derived_state(
                        instance_id=instance_id,
                        operation_id=op_id,
                        when=when,
                        stage_records=stage_records,
                        completed=completed,
                    )
                )
            else:
                experience_result = self._run_stage(
                    LifecycleStage.EXPERIENCE_MODELS,
                    operation_id=op_id,
                    records=stage_records,
                    call=lambda: self._experience.portfolio_for_instance(
                        instance_id, presented_at=when
                    ),
                )
                self._checkpoints.mark_stage_complete(
                    op_id,
                    LifecycleStage.EXPERIENCE_MODELS,
                    instance_id=instance_id,
                )
                completed.append(LifecycleStage.EXPERIENCE_MODELS)
        except LifecycleStageError as exc:
            self._checkpoints.mark_failed(
                op_id,
                stage=LifecycleStage(exc.stage),
                cause=str(exc),
                instance_id=instance_id,
            )
            return LifecycleResult(
                operation_id=op_id,
                operation_type=OperationType.ENSURE,
                status=OperationStatus.FAILED,
                student_id=None,
                instance_id=instance_id,
                correlation_id=corr,
                beliefs=beliefs_result,
                decisions=decisions_result,
                experience=experience_result,
                stages=tuple(stage_records),
                completed_stages=tuple(completed),
                failed_stage=LifecycleStage(exc.stage),
                failure_cause=str(exc),
            )

        self._checkpoints.mark_completed(op_id)
        return LifecycleResult(
            operation_id=op_id,
            operation_type=OperationType.ENSURE,
            status=OperationStatus.COMPLETED,
            student_id=None,
            instance_id=instance_id,
            correlation_id=corr,
            beliefs=beliefs_result,
            decisions=decisions_result,
            experience=experience_result,
            stages=tuple(stage_records),
            completed_stages=tuple(completed),
        )

    def recover(
        self,
        instance_id: str,
        *,
        as_of: datetime | None = None,
        correlation_id: str | None = None,
        failed_operation_id: str | None = None,
    ) -> LifecycleResult:
        """Recover from a failed lifecycle operation.

        Strategy: re-run derived EI stages from twin beliefs onward so
        beliefs, decisions, and experience models stay aligned. Binding and
        evidence appends are never undone (immutable / already durable).
        """
        when = as_of if as_of is not None else _utc_now()
        when = when.replace(tzinfo=None) if when.tzinfo else when
        prior = None
        if failed_operation_id:
            prior = self._checkpoints.require(failed_operation_id)
        else:
            prior = self._checkpoints.latest_failed_for_instance(instance_id)

        attempt = int(prior.attempt_count if prior is not None else 0) + 1
        op_id = f"llp-{uuid.uuid4().hex[:16]}"
        corr = (correlation_id or "").strip() or (
            prior.correlation_id if prior is not None else None
        )

        self._checkpoints.start(
            operation_id=op_id,
            operation_type=OperationType.RECOVER,
            instance_id=instance_id,
            student_id=prior.student_id if prior is not None else None,
            correlation_id=corr,
            attempt_count=attempt,
        )

        stage_records: list[StageExecutionRecord] = []
        completed: list[LifecycleStage] = []
        beliefs_result = None
        decisions_result = None
        experience_result = None

        try:
            self._run_stage(
                LifecycleStage.INITIALISE_NODE_STATE,
                operation_id=op_id,
                records=stage_records,
                call=lambda: self._binding.initialise_node_states(instance_id),
            )
            self._checkpoints.mark_stage_complete(
                op_id, LifecycleStage.INITIALISE_NODE_STATE, instance_id=instance_id
            )
            completed.append(LifecycleStage.INITIALISE_NODE_STATE)

            beliefs_result, decisions_result, experience_result = (
                self._refresh_derived_state(
                    instance_id=instance_id,
                    operation_id=op_id,
                    when=when,
                    stage_records=stage_records,
                    completed=completed,
                )
            )
        except LifecycleStageError as exc:
            self._checkpoints.mark_failed(
                op_id,
                stage=LifecycleStage(exc.stage),
                cause=str(exc),
                instance_id=instance_id,
            )
            return LifecycleResult(
                operation_id=op_id,
                operation_type=OperationType.RECOVER,
                status=OperationStatus.FAILED,
                student_id=prior.student_id if prior is not None else None,
                instance_id=instance_id,
                correlation_id=corr,
                beliefs=beliefs_result,
                decisions=decisions_result,
                experience=experience_result,
                stages=tuple(stage_records),
                completed_stages=tuple(completed),
                failed_stage=LifecycleStage(exc.stage),
                failure_cause=str(exc),
                attempt_count=attempt,
            )

        self._checkpoints.mark_completed(op_id)
        return LifecycleResult(
            operation_id=op_id,
            operation_type=OperationType.RECOVER,
            status=OperationStatus.COMPLETED,
            student_id=prior.student_id if prior is not None else None,
            instance_id=instance_id,
            correlation_id=corr,
            beliefs=beliefs_result,
            decisions=decisions_result,
            experience=experience_result,
            stages=tuple(stage_records),
            completed_stages=tuple(completed),
            attempt_count=attempt,
        )

    def inspect_consistency(self, instance_id: str) -> ConsistencyReport:
        """Return whether the SCI has complete Educational Intelligence state."""
        return self._consistency.inspect(instance_id)

    def _refresh_derived_state(
        self,
        *,
        instance_id: str,
        operation_id: str,
        when: datetime,
        stage_records: list[StageExecutionRecord],
        completed: list[LifecycleStage],
    ):
        """Invoke Twin → Decisions → Experience in fixed order."""
        beliefs_result = self._run_stage(
            LifecycleStage.TWIN_BELIEFS,
            operation_id=operation_id,
            records=stage_records,
            call=lambda: self._beliefs.rebuild_beliefs(
                instance_id, as_of=when, project_to_node_state=True
            ),
        )
        self._checkpoints.mark_stage_complete(
            operation_id, LifecycleStage.TWIN_BELIEFS, instance_id=instance_id
        )
        completed.append(LifecycleStage.TWIN_BELIEFS)

        decisions_result = self._run_stage(
            LifecycleStage.EDUCATIONAL_DECISIONS,
            operation_id=operation_id,
            records=stage_records,
            call=lambda: self._decisions.rebuild_decisions(
                instance_id, as_of=when, ensure_beliefs=False
            ),
        )
        self._checkpoints.mark_stage_complete(
            operation_id,
            LifecycleStage.EDUCATIONAL_DECISIONS,
            instance_id=instance_id,
        )
        completed.append(LifecycleStage.EDUCATIONAL_DECISIONS)

        experience_result = self._run_stage(
            LifecycleStage.EXPERIENCE_MODELS,
            operation_id=operation_id,
            records=stage_records,
            call=lambda: self._experience.portfolio_for_instance(
                instance_id, presented_at=when
            ),
        )
        self._checkpoints.mark_stage_complete(
            operation_id, LifecycleStage.EXPERIENCE_MODELS, instance_id=instance_id
        )
        completed.append(LifecycleStage.EXPERIENCE_MODELS)

        return beliefs_result, decisions_result, experience_result

    def _run_stage(
        self,
        stage: LifecycleStage,
        *,
        operation_id: str,
        records: list[StageExecutionRecord],
        call: Callable[[], Any],
    ) -> Any:
        """Invoke one EI/EX capability with technical retries."""
        attempt = 0
        while True:
            attempt += 1
            t0 = perf_counter()
            try:
                result = call()
            except Exception as exc:  # noqa: BLE001 — classify as stage failure
                duration_ms = (perf_counter() - t0) * 1000.0
                if self._retry.should_retry(attempt=attempt):
                    logger.info(
                        "lifecycle stage retry operation_id=%s stage=%s attempt=%s",
                        operation_id,
                        stage.value,
                        attempt,
                    )
                    continue
                cause = f"{exc.__class__.__name__}: {exc}"
                records.append(
                    StageExecutionRecord(
                        stage=stage,
                        succeeded=False,
                        attempts=attempt,
                        duration_ms=duration_ms,
                        error=cause,
                    )
                )
                raise LifecycleRetryExhaustedError(
                    f"Stage {stage.value} failed after {attempt} attempt(s): {cause}",
                    stage=stage.value,
                    operation_id=operation_id,
                    cause=exc,
                ) from exc

            duration_ms = (perf_counter() - t0) * 1000.0
            records.append(
                StageExecutionRecord(
                    stage=stage,
                    succeeded=True,
                    attempts=attempt,
                    duration_ms=duration_ms,
                )
            )
            return result
