"""Policy enforcing required stage sequencing within orchestration.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
    ORCHESTRATION_INVARIANTS.md
Concept
    Sequencing Policy
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.orchestrator.entities.orchestration_stage import (
    OrchestrationStage,
    OrchestrationStageId,
)
from domain.education.orchestrator.enums import StageStatus
from domain.education.orchestrator.value_objects.orchestration_progress import (
    OrchestrationProgress,
)


class SequencingPolicy:
    """Enforces ordered advancement through orchestration stages."""

    @staticmethod
    def ordered(
        stages: tuple[OrchestrationStage, ...] | list[OrchestrationStage],
    ) -> tuple[OrchestrationStage, ...]:
        return tuple(sorted(stages, key=lambda s: s.sequence_index))

    @staticmethod
    def progress_of(
        stages: tuple[OrchestrationStage, ...] | list[OrchestrationStage],
    ) -> OrchestrationProgress:
        ordered = SequencingPolicy.ordered(stages)
        completed = sum(1 for stage in ordered if stage.is_completed())
        required = [stage for stage in ordered if stage.required]
        completed_required = sum(1 for stage in required if stage.is_completed())
        evidence_points = [
            stage for stage in ordered if stage.is_evidence_collection_point()
        ]
        evidence_reached = sum(
            1 for stage in evidence_points if stage.is_completed()
        )
        active = next((stage for stage in ordered if stage.is_active()), None)
        if active is not None:
            current_index = active.sequence_index
        elif completed == len(ordered):
            current_index = len(ordered)
        else:
            pending = next((stage for stage in ordered if stage.is_pending()), None)
            current_index = pending.sequence_index if pending else 0
        return OrchestrationProgress(
            current_index=current_index,
            completed_stages=completed,
            total_stages=len(ordered),
            completed_required_stages=completed_required,
            total_required_stages=len(required),
            evidence_collection_points_reached=evidence_reached,
            total_evidence_collection_points=len(evidence_points),
        )

    @staticmethod
    def required_stages_complete(
        stages: tuple[OrchestrationStage, ...] | list[OrchestrationStage],
    ) -> bool:
        return SequencingPolicy.progress_of(stages).required_sequence_complete

    @staticmethod
    def assert_can_advance(
        stages: tuple[OrchestrationStage, ...] | list[OrchestrationStage],
    ) -> OrchestrationStage:
        """Return the stage that must be advanced next; forbid skipping."""
        ordered = SequencingPolicy.ordered(stages)
        active = [stage for stage in ordered if stage.is_active()]
        if len(active) > 1:
            raise EducationalInvariantViolation(
                "at most one orchestration stage may be active",
                invariant="SequencingPolicy.single_active",
            )
        if active:
            return active[0]

        for index, stage in enumerate(ordered):
            if stage.is_completed():
                continue
            for prior in ordered[:index]:
                if prior.required and not prior.is_completed():
                    raise EducationalInvariantViolation(
                        "cannot skip a required orchestration stage in sequence",
                        invariant="SequencingPolicy.no_skip_required",
                    )
            if stage.is_pending():
                return stage
            raise EducationalInvariantViolation(
                "orchestration stage is not advanceable",
                invariant="SequencingPolicy.not_advanceable",
            )

        raise EducationalInvariantViolation(
            "no remaining orchestration stage to advance",
            invariant="SequencingPolicy.exhausted",
        )

    @staticmethod
    def assert_stage_belongs(
        stages: tuple[OrchestrationStage, ...] | list[OrchestrationStage],
        stage_id: OrchestrationStageId,
    ) -> OrchestrationStage:
        for stage in stages:
            if stage.stage_id == stage_id:
                return stage
        raise EducationalInvariantViolation(
            "orchestration stage is not owned by this orchestrator",
            invariant="SequencingPolicy.stage.not_found",
        )

    @staticmethod
    def replace_stage(
        stages: list[OrchestrationStage],
        updated: OrchestrationStage,
    ) -> list[OrchestrationStage]:
        """Return a new stage list with ``updated`` substituted by identity."""
        found = False
        result: list[OrchestrationStage] = []
        for stage in stages:
            if stage.stage_id == updated.stage_id:
                result.append(updated)
                found = True
            else:
                result.append(stage)
        if not found:
            raise EducationalInvariantViolation(
                "cannot replace unknown orchestration stage",
                invariant="SequencingPolicy.replace.not_found",
            )
        return result

    @staticmethod
    def activate_first_pending(
        stages: list[OrchestrationStage],
    ) -> list[OrchestrationStage]:
        """Activate the first pending stage when starting orchestration."""
        ordered = sorted(stages, key=lambda s: s.sequence_index)
        for stage in ordered:
            if stage.status is StageStatus.PENDING:
                return SequencingPolicy.replace_stage(stages, stage.activate())
        raise EducationalInvariantViolation(
            "no pending stage available to activate on start",
            invariant="SequencingPolicy.start.no_pending",
        )
